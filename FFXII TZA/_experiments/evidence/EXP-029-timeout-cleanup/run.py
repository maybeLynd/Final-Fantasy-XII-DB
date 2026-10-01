"""Disposable child controls only. Never discovers or opens FFXII.

Cold and positive arms execute the same allocated RET every 50 ms; the cold
breakpoint is the unused byte immediately after RET. Both addresses are owned
by the child. All context writes use the EXP018 source snapshot helpers.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from api_receipts import Audit
from timeout_cleanup import cleanup

HERE = Path(__file__).resolve().parent


def write(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)


def target(folder):
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32]
    k.VirtualAlloc.restype = ctypes.c_void_p
    addr = k.VirtualAlloc(None, 4096, 0x3000, 0x40)
    if not addr: raise ctypes.WinError(ctypes.get_last_error())
    ctypes.memmove(addr, b'\xc3\xc3', 2)
    call = ctypes.CFUNCTYPE(None)(addr)
    write(folder/'target-ready.json', dict(pid=__import__('os').getpid(), address=addr))
    with (folder/'heartbeat.bin').open('xb', buffering=0) as stream:
        while True:
            call()
            stream.write(b'.')
            time.sleep(0.05)


def run(mode):
    folder = HERE/(mode+'-direct')
    folder.mkdir()
    spec = importlib.util.spec_from_file_location('snapshot_'+mode, HERE/'hwbp-source.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    raw = m.k32
    raw.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    raw.OpenProcess.restype = ctypes.c_void_p
    raw.DebugBreakProcess.argtypes = [ctypes.c_void_p]
    raw.DebugBreakProcess.restype = ctypes.c_int
    raw.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    raw.CloseHandle.argtypes = [ctypes.c_void_p]
    audit = Audit(raw, folder/'api.json')
    m.k32 = audit
    result = dict(status='INCOMPLETE', mode=mode, hits=0, sources={
        p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [HERE/'run.py',HERE/'timeout_cleanup.py',HERE/'hwbp-source.py',HERE/'api_receipts.py']})
    child = None
    handle = None
    attached = False
    try:
        # Windows venv python.exe can be a redirector with another PID. Launch
        # its base executable so the owned Popen handle is the actual target.
        child = subprocess.Popen([sys._base_executable, str(Path(__file__).resolve()), '--target',str(folder)])
        result['pid'] = child.pid
        deadline = time.monotonic()+10
        while not (folder/'heartbeat.bin').exists():
            assert child.poll() is None and time.monotonic()<deadline, 'target not ready'
            time.sleep(0.02)
        info = json.loads((folder/'target-ready.json').read_text())
        assert info['pid'] == child.pid
        address = info['address']+(mode == 'cold')
        result['breakpoint'] = address
        handle = raw.OpenProcess(0x1FFFFF, False, child.pid)
        assert handle
        def snapshot():
            present = ctypes.c_int()
            ok = bool(raw.CheckRemoteDebuggerPresent(handle, ctypes.byref(present)))
            return dict(unix=time.time(), exit=child.poll(), beats=(folder/'heartbeat.bin').stat().st_size,
                        debugger_read_ok=ok, debugger_present=bool(present.value) if ok else None)
        result['baseline'] = snapshot()
        assert result['baseline']['debugger_present'] is False
        m.attach_with_exit_policy(child.pid)
        attached = True
        event = m.DEBUG_EVENT()
        ready = False
        until = time.monotonic()+2
        arming = []
        while time.monotonic()<until:
            if not audit.WaitForDebugEvent(ctypes.byref(event), 100):
                assert ctypes.get_last_error() in (0,121)
                continue
            code, tid = event.dwDebugEventCode, event.dwThreadId
            status = m.DBG_CONTINUE
            if code == 3:
                arming += [(t,m.set_slots(t,[address])) for t in m.threads_of(child.pid)]
            elif code == 2:
                arming.append((tid,m.set_slots(tid,[address])))
            elif code == 1:
                exc = event.u.Exception.ExceptionRecord.ExceptionCode
                if exc == m.EXCEPTION_BREAKPOINT:
                    ready = True
                elif exc == m.EXCEPTION_SINGLE_STEP:
                    ctx = m.read_regs(tid)
                    assert ctx is not None and ctx.Rip == address
                    result['hits'] += 1
                    assert m.resume_past_breakpoint(tid)
                else:
                    raise AssertionError('unexpected exception %x' % exc)
            elif code == 5:
                raise AssertionError('target exited')
            assert audit.ContinueDebugEvent(child.pid, tid, status)
        result['arming'] = arming
        result['attached'] = snapshot()
        assert ready and arming and all(x[1] for x in arming)
        assert result['attached']['beats'] > result['baseline']['beats']
        result['cleanup'] = cleanup(m, child.pid, handle, audit, ready=ready)
        detached = bool(audit.DebugActiveProcessStop(child.pid))
        attached = not detached
        result['detach'] = detached
        result['post'] = [snapshot()]
        for _ in range(3):
            time.sleep(0.3)
            result['post'].append(snapshot())
        assert result['cleanup']['status'] == 'PASS' and detached
        assert all(x['exit'] is None and x['debugger_present'] is False for x in result['post'])
        assert all(b['beats']>a['beats'] for a,b in zip(result['post'], result['post'][1:]))
        assert (result['hits']==0) if mode=='cold' else (result['hits']>0)
        assert not [r for r in audit.rows if 'result' in r and not r['result']]
        result['status'] = 'PASS'
    finally:
        if attached:
            result['recovery_detach'] = bool(audit.DebugActiveProcessStop(child.pid))
        if child is not None:
            if child.poll() is None: child.kill()
            result['child_final_exit'] = child.wait(timeout=5)
        if handle: raw.CloseHandle(handle)
        audit.save()
        write(folder/'result.json', result)
    print(mode, result['status'], 'hits',result['hits'])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=Path)
    args = ap.parse_args()
    if args.target: target(args.target)
    else:
        run('cold')
        run('positive')
