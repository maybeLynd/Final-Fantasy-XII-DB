"""EXP-016 diagnostic proxy. Preserve API results; buffer receipts until cleanup."""
import ctypes
import json
import time
from pathlib import Path


class Audit:
    def __init__(self, api, output):
        self.api = api
        self.output = Path(output)
        if self.output.exists():
            raise FileExistsError(self.output)
        self.rows = []

    def mark(self, name, **values):
        self.rows.append(dict(unix=time.time(), operation=name, **values))

    def save(self):
        self.output.write_text(json.dumps(self.rows, indent=2)+'\n')

    def __getattr__(self, name):
        native = getattr(self.api, name)
        if name not in {'GetThreadContext', 'SetThreadContext', 'ContinueDebugEvent',
                        'DebugActiveProcess', 'DebugActiveProcessStop', 'DebugBreakProcess',
                        'DebugSetProcessKillOnExit', 'WaitForDebugEvent', 'OpenThread'}:
            return native

        def call(*args):
            # Read the proposed context before calling SetThreadContext.
            values = {}
            if name in {'GetThreadContext', 'SetThreadContext'}:
                ctx = args[1]._obj
                values['handle'] = int(args[0])
                values['requested_flags'] = ctx.ContextFlags
                if name == 'SetThreadContext':
                    values['context'] = {k: getattr(ctx,k) for k in
                                         ['ContextFlags','Rip','Rsp','EFlags','Dr0','Dr1','Dr2','Dr3','Dr6','Dr7']}
            result = native(*args)
            error = ctypes.get_last_error()
            if name == 'WaitForDebugEvent':
                if not result:
                    # Timed waits normally return false; retain unusual failures.
                    if error not in (0, 121):
                        self.mark(name, result=int(result), error=error)
                    return result
                ev = args[0]._obj
                values.update(event=ev.dwDebugEventCode, pid=ev.dwProcessId, tid=ev.dwThreadId)
                if ev.dwDebugEventCode == 1:
                    values.update(exception=ev.u.Exception.ExceptionRecord.ExceptionCode,
                                  address=ev.u.Exception.ExceptionRecord.ExceptionAddress)
            elif name == 'GetThreadContext' and result:
                ctx = args[1]._obj
                values['context'] = {k: getattr(ctx,k) for k in
                                     ['ContextFlags','Rip','Rsp','EFlags','Dr0','Dr1','Dr2','Dr3','Dr6','Dr7']}
            elif name == 'ContinueDebugEvent':
                values.update(pid=args[0],tid=args[1],status=args[2])
            elif name == 'OpenThread':
                values.update(tid=args[2])
            self.mark(name, result=int(result), error=error if not result else None, **values)
            # Receipt construction must not change last-error observed by caller.
            ctypes.set_last_error(error)
            return result
        return call
