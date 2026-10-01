"""Private duration-only EXP030 capture. No original-game validation yet.

Only arms while a debug event stops the process. No running-thread fallback.
An API failure invalidates the capture even if eventual cleanup succeeds.
Caller must independently verify target identity, liveness and debugger absence.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import time
from api_receipts import Audit
from timeout_cleanup import cleanup

HERE = Path(__file__).resolve().parent


def load_source():
    source = HERE/'hwbp-source.py'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == '81a8510288dc5a4e1d93c221659c49926039e66aa277da3f1fea59aa193879f6'
    spec = importlib.util.spec_from_file_location('exp018_snapshot',source)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.k32.OpenProcess.argtypes = [ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    m.k32.OpenProcess.restype = ctypes.c_void_p
    m.k32.DebugBreakProcess.argtypes = [ctypes.c_void_p]
    m.k32.DebugBreakProcess.restype = ctypes.c_int
    m.k32.CloseHandle.argtypes = [ctypes.c_void_p]
    return m


def capture(m, pid, slots, seconds, audit):
    if not slots or len(slots)>4 or seconds<=0:
        raise ValueError('one to four addresses and positive duration required')
    result = dict(status='INVALID', hits=[], arming=[], errors=[], cleanup=None, detach=False)
    handle = m.k32.OpenProcess(0x1FFFFF,False,pid)
    if not handle:
        result['errors'].append('OpenProcess failed')
        return result
    attached = ready = pending = False
    initial = None
    try:
        # Use explicit setup so even a failed policy records detach in this result.
        if not m.k32.DebugActiveProcess(pid):
            raise OSError('DebugActiveProcess failed')
        attached = True
        if not m.k32.DebugSetProcessKillOnExit(False):
            raise OSError('DebugSetProcessKillOnExit failed')
        event = m.DEBUG_EVENT()
        end = time.monotonic()+3.0
        while time.monotonic()<end:
            if not m.k32.WaitForDebugEvent(ctypes.byref(event),100):
                error = ctypes.get_last_error()
                if error not in (0,121): raise OSError('WaitForDebugEvent failed: %d' % error)
                continue
            pending = True
            code, tid = event.dwDebugEventCode,event.dwThreadId
            if event.dwProcessId != pid: raise OSError('unexpected process event')
            status = m.DBG_CONTINUE
            error = None
            arm_tids = []
            if code == 1:
                rec = event.u.Exception.ExceptionRecord
                if rec.ExceptionCode == m.EXCEPTION_BREAKPOINT and not ready:
                    initial = rec.ExceptionAddress
                    arm_tids = m.threads_of(pid)
                    if not arm_tids: error = 'empty initial thread enumeration'
                    ready = True
                    end = time.monotonic()+seconds
                elif rec.ExceptionCode == m.EXCEPTION_SINGLE_STEP and ready:
                    ctx = m.read_regs(tid)
                    if ctx is None or ctx.Rip not in slots:
                        error = 'unrecognized or unreadable single step'
                    else:
                        result['hits'].append(dict(unix=time.time(), tid=tid, rip=ctx.Rip,
                            rsp=ctx.Rsp, rcx=ctx.Rcx, rdx=ctx.Rdx, r8=ctx.R8, r9=ctx.R9))
                    if not m.resume_past_breakpoint(tid): error = 'resume context failed'
                else:
                    status = m.DBG_EXCEPTION_NOT_HANDLED
                    error = 'unexpected exception %x' % rec.ExceptionCode
            elif code == 2 and ready:
                arm_tids = [tid]
            elif code == 5:
                error = 'target exited'
            for t in arm_tids:
                ok = m.set_slots(t, slots)
                result['arming'].append((t,ok))
                if not ok: error = 'arming failed'
            if not m.k32.ContinueDebugEvent(pid,tid,status):
                raise OSError('ContinueDebugEvent failed')
            pending = False
            if error: raise OSError(error)
        if not ready: raise OSError('initial breakpoint deadline expired')
    except Exception as error:
        result['errors'].append(str(error))
    finally:
        if attached:
            try:
                if ready and not pending:
                    result['cleanup'] = cleanup(m,pid,handle,audit,ready=True,
                                                initial_break_address=initial)
                else:
                    result['errors'].append('no prepared cleanup boundary')
            except Exception as error:
                result['errors'].append('cleanup exception: '+str(error))
            result['detach'] = bool(m.k32.DebugActiveProcessStop(pid))
        m.k32.CloseHandle(handle)
    if (not result['errors'] and result['cleanup'] and result['cleanup']['status']=='PASS'
            and result['detach'] and result['arming'] and all(x[1] for x in result['arming'])):
        result['status'] = 'PASS'
    audit.mark('capture_end', status=result['status'], errors=result['errors'], detach=result['detach'])
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pid',type=int,required=True)
    ap.add_argument('--addr',action='append',required=True)
    ap.add_argument('--seconds',type=float,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args = ap.parse_args()
    args.out.mkdir()
    m = load_source()
    audit = Audit(m.k32,args.out/'api.json')
    m.k32 = audit
    try:
        result = capture(m,args.pid,[int(x,16) for x in args.addr],args.seconds,audit)
        result['sources'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                             [HERE/'capture.py',HERE/'timeout_cleanup.py',HERE/'api_receipts.py',HERE/'hwbp-source.py']}
        (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    finally:
        audit.save()
    print(result['status'], 'hits',len(result['hits']))
    return 0 if result['status']=='PASS' else 3


if __name__ == '__main__': raise SystemExit(main())
