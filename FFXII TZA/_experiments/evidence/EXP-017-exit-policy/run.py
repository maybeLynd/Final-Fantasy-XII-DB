"""EXP-017: terminate only our debugger child; observe our disposable heartbeat child.

No FFXII process is opened. Old ordering is an intentional invalid-policy control.
The revised arm imports the actual shared hwbp setup helper. No context writes.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[3] / 'Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(KIT))
import hwbp


def write_new(path, data):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2)


class RecordedAPI:
    def __init__(self, raw):
        self.raw = raw
        self.rows = []

    def __getattr__(self, name):
        call = getattr(self.raw, name)
        if name not in ('DebugActiveProcess', 'DebugSetProcessKillOnExit', 'DebugActiveProcessStop'):
            return call
        def record(*args):
            ctypes.set_last_error(0)
            result = call(*args)
            self.rows.append(dict(unix=time.time(), operation=name, args=args,
                                  result=result, error=ctypes.get_last_error() if not result else None))
            return result
        return record


def debug_child(pid, mode, ready):
    api = RecordedAPI(hwbp.k32)
    hwbp.k32 = api
    if mode == 'old':
        api.DebugSetProcessKillOnExit(False)  # deliberate reproduction of old unchecked order
        if not api.DebugActiveProcess(pid):
            raise ctypes.WinError(ctypes.get_last_error())
    else:
        hwbp.attach_with_exit_policy(pid)
    event = hwbp.DEBUG_EVENT()
    announced = False
    while True:
        if not api.WaitForDebugEvent(ctypes.byref(event), 100):
            continue
        status = hwbp.DBG_CONTINUE
        initial_break = event.dwDebugEventCode == 1 and (
            event.u.Exception.ExceptionRecord.ExceptionCode == hwbp.EXCEPTION_BREAKPOINT)
        if event.dwDebugEventCode == 1 and not initial_break:
            status = hwbp.DBG_EXCEPTION_NOT_HANDLED
        if not api.ContinueDebugEvent(event.dwProcessId, event.dwThreadId, status):
            raise ctypes.WinError(ctypes.get_last_error())
        if initial_break and not announced:
            write_new(ready, dict(pid=pid, mode=mode, setup=api.rows, unix=time.time()))
            announced = True


def heartbeat(path):
    with path.open('xb', buffering=0) as stream:
        while True:
            stream.write(b'.')
            time.sleep(0.05)


def snapshot(child, heart):
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    k.OpenProcess.restype = ctypes.c_void_p
    k.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    k.CloseHandle.argtypes = [ctypes.c_void_p]
    result = dict(unix=time.time(), exit_code=child.poll(), beats=heart.stat().st_size if heart.exists() else 0)
    handle = k.OpenProcess(0x0400, False, child.pid)
    present = ctypes.c_int()
    try:
        ok = bool(handle and k.CheckRemoteDebuggerPresent(handle, ctypes.byref(present)))
        result.update(debug_read_ok=ok, debugger_present=bool(present.value) if ok else None)
    finally:
        if handle:
            k.CloseHandle(handle)
    return result


def run_case(mode):
    folder = HERE / mode
    folder.mkdir()  # fail on reuse, never overwrite a failed attempt
    heart = folder / 'heartbeat.bin'
    ready = folder / 'attached.json'
    target = debugger = None
    result = dict(mode=mode, status='INCOMPLETE', start_unix=time.time())
    with (folder/'target.txt').open('x') as target_log, (folder/'debugger.txt').open('x') as debug_log:
        try:
            target_cmd = [sys.executable, str(Path(__file__)), '--target', str(heart)]
            target = subprocess.Popen(target_cmd, stdout=target_log, stderr=subprocess.STDOUT)
            result.update(target_pid=target.pid, target_command=target_cmd)
            deadline = time.monotonic()+10
            while not heart.exists() and target.poll() is None and time.monotonic()<deadline:
                time.sleep(0.05)
            result['baseline'] = snapshot(target, heart)
            assert result['baseline']['beats'] > 0 and result['baseline']['debugger_present'] is False
            debug_cmd = [sys.executable, str(Path(__file__)), '--debug', str(target.pid), '--mode', mode, '--ready', str(ready)]
            debugger = subprocess.Popen(debug_cmd, stdout=debug_log, stderr=subprocess.STDOUT)
            result.update(debugger_pid=debugger.pid, debugger_command=debug_cmd)
            deadline = time.monotonic()+10
            while not ready.exists() and debugger.poll() is None and time.monotonic()<deadline:
                time.sleep(0.05)
            assert ready.exists(), 'debugger failed to reach serviced initial breakpoint'
            result['attached_start'] = snapshot(target, heart)
            time.sleep(0.5)
            result['attached_end'] = snapshot(target, heart)
            assert result['attached_end']['debugger_present'] is True
            assert result['attached_end']['beats'] > result['attached_start']['beats']
            result['intervention_unix'] = time.time()
            debugger.kill()  # only the Popen handle we just created; no finally/detach in that child
            result['debugger_exit_code'] = debugger.wait(timeout=5)
            time.sleep(0.5)
            result['post_start'] = snapshot(target, heart)
            time.sleep(0.5)
            result['post_end'] = snapshot(target, heart)
            if mode == 'old':
                assert result['post_end']['exit_code'] is not None, 'old-order failure control did not kill target'
            else:
                assert result['post_end']['exit_code'] is None
                assert result['post_end']['debugger_present'] is False
                assert result['post_end']['beats'] > result['post_start']['beats']
            result['status'] = 'PASS'
        finally:
            for child in (debugger, target):
                if child and child.poll() is None:
                    child.kill()
                    child.wait(timeout=5)
            result['cleanup'] = dict(debugger_exit=debugger.poll() if debugger else None,
                                     target_exit=target.poll() if target else None)
            result['end_unix'] = time.time()
            write_new(folder/'result.json', result)
    print(mode, result['status'], flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path)
    parser.add_argument('--debug', type=int)
    parser.add_argument('--mode', choices=['old', 'revised'])
    parser.add_argument('--ready', type=Path)
    args = parser.parse_args()
    if args.target:
        heartbeat(args.target)
    elif args.debug:
        debug_child(args.debug, args.mode, args.ready)
    else:
        write_new(HERE/'source-receipt.json', {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [Path(__file__), KIT/'hwbp.py', KIT/'test_hwbp_exit_policy.py']})
        (HERE/'hwbp-tested.py').write_bytes((KIT/'hwbp.py').read_bytes())
        run_case('old')
        run_case('revised')
