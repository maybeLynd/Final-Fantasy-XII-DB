"""Bounded native instrument qualification on Popen-owned Python children only.

No FF12 discovery, launch, memory/input access, saved games or UI automation.
Reuses the EXP029 RET heartbeat and exact frozen EXP030 helpers. Adds a known
vectored handler and one deliberately raised exception to distinguish delivery.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

E = Path(__file__).resolve().parent
FIX = E.parent / 'exp127-instrument-control'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def write(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def dll():
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32]
    k.VirtualAlloc.restype = ctypes.c_void_p
    k.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32]
    k.AddVectoredExceptionHandler.argtypes = [ctypes.c_ulong, ctypes.c_void_p]
    k.AddVectoredExceptionHandler.restype = ctypes.c_void_p
    k.RemoveVectoredExceptionHandler.argtypes = [ctypes.c_void_p]
    k.RaiseException.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p]
    k.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    k.OpenProcess.restype = ctypes.c_void_p
    k.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    k.CloseHandle.argtypes = [ctypes.c_void_p]
    k.GetCurrentThreadId.restype = ctypes.c_uint32
    return k


def target(folder):
    # A baseline self-raise must reach this handler before any debugger attaches.
    k = dll()
    k.SetErrorMode(0x0001 | 0x0002 | 0x8000)  # own disposable process only
    callbacks = []
    CALLBACK = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p)

    def handler(pointers):
        record = ctypes.c_void_p.from_address(pointers).value
        code = ctypes.c_ulong.from_address(record).value
        if code != 0x80000004:
            return 0  # EXCEPTION_CONTINUE_SEARCH
        address = ctypes.c_void_p.from_address(record + 16).value
        callbacks.append(dict(code=code, address=address, tid=k.GetCurrentThreadId(), unix=time.time()))
        return -1  # EXCEPTION_CONTINUE_EXECUTION for our continuable self-raise

    callback = CALLBACK(handler)
    registration = k.AddVectoredExceptionHandler(1, callback)
    assert registration
    address = k.VirtualAlloc(None, 4096, 0x3000, 0x40)
    assert address
    ctypes.memmove(address, b'\xc3\xc3', 2)  # unchanged EXP029 heartbeat body
    beat = ctypes.CFUNCTYPE(None)(address)
    normal_exit = False
    try:
        k.RaiseException(0x80000004, 0, 0, None)
        assert len(callbacks) == 1, 'baseline target handler did not receive self-raise'
        write(folder / 'target-ready.json', dict(pid=os.getpid(), tid=k.GetCurrentThreadId(),
              address=address, python=sys.executable, source_sha256=sha(Path(__file__)),
              baseline_handler=list(callbacks), created_unix=time.time()))
        fired = False
        with (folder / 'heartbeat.bin').open('xb', buffering=0) as out:
            end = time.monotonic() + 15
            while not (folder / 'stop.flag').exists():
                assert time.monotonic() < end, 'owned-target deadline'
                beat()
                out.write(b'.')
                if (folder / 'fire.flag').exists() and not fired:
                    fired = True
                    before = len(callbacks)
                    k.RaiseException(0x80000004, 0, 0, None)
                    write(folder / 'delivery.json', dict(before=before, after=len(callbacks),
                          handler_events=list(callbacks), returned_from_raise=True))
                time.sleep(0.05)
        normal_exit = True
    finally:
        removed = bool(k.RemoveVectoredExceptionHandler(registration))
        freed = bool(k.VirtualFree(address, 0, 0x8000))
        write(folder / 'target-exit.json', dict(normal_exit=normal_exit, handler_events=callbacks,
              handler_removed=removed, allocation_freed=freed, debugger_present=bool(k.IsDebuggerPresent())))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def debug_child(folder, mode):
    info = json.loads((folder / 'target-ready.json').read_text())
    plan = json.loads((folder / 'plan.json').read_text())
    assert info['pid'] == plan['owned_child_pid']
    assert info['source_sha256'] == plan['sources']['run.py'] == sha(Path(__file__))
    for name, digest in plan['sources'].items():
        if name != 'run.py': assert sha(FIX / name) == digest, name
    sys.path.insert(0, str(FIX / 'original'))
    original = load('native_original_capture', FIX / 'original/capture.py')
    m = original.load_source()
    from api_receipts import Audit

    class TriggerAudit(Audit):
        def __init__(self, api, output):
            super().__init__(api, output)
            self.event = None
            self.fired = False

        def __getattr__(self, name):
            call = super().__getattr__(name)
            if name not in ('WaitForDebugEvent', 'ContinueDebugEvent'): return call

            def observed(*args):
                result = call(*args)
                if result and name == 'WaitForDebugEvent':
                    ev = args[0]._obj
                    self.event = None
                    if ev.dwDebugEventCode == 1:
                        rec = ev.u.Exception.ExceptionRecord
                        self.event = (rec.ExceptionCode, rec.ExceptionAddress)
                        self.mark('exception_chance', tid=ev.dwThreadId, exception=rec.ExceptionCode,
                                  address=rec.ExceptionAddress, first_chance=ev.u.Exception.dwFirstChance)
                if result and name == 'ContinueDebugEvent' and mode != 'positive' and not self.fired:
                    if self.event == (0x80000004, info['address']):
                        write(folder / 'fire.flag', dict(after_owned_hit=True, unix=time.time()))
                        self.fired = True
                return result
            return observed

    audit = TriggerAudit(m.k32, folder / 'api.json')
    m.k32 = audit
    if mode == 'original':
        capture = original.capture
    else:
        sys.path.insert(0, str(FIX))
        capture = load('native_candidate_capture', FIX / 'capture_candidate.py').capture
    try:
        result = capture(m, info['pid'], [info['address']], 1.0, audit)
        result['mode'] = mode
        result['trigger_issued'] = audit.fired
        write(folder / 'capture.json', result)
    finally:
        audit.save()


def run_arm(mode):
    folder = E / mode
    folder.mkdir()
    k = dll()
    child = debugger = None
    handle = None
    record = dict(status='INVALID', mode=mode, method='native disposable instrument control; not FF12',
                  start_unix=time.time(), forced_termination=[], sources={
                      'run.py': sha(Path(__file__)), **{p.relative_to(FIX).as_posix(): sha(p) for p in
                      [FIX/'capture_candidate.py', FIX/'cleanup_candidate.py', FIX/'ownership.py',
                       *sorted((FIX/'original').glob('*.py'))]}})
    try:
        child = subprocess.Popen([sys._base_executable, str(Path(__file__).resolve()), '--target', str(folder)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        record['owned_child_pid'] = child.pid
        write(folder / 'plan.json', record)
        end = time.monotonic()+5
        while not (folder/'target-ready.json').exists() or not (folder/'heartbeat.bin').exists():
            assert child.poll() is None and time.monotonic()<end, 'target baseline control failed'
            time.sleep(.02)
        info = json.loads((folder/'target-ready.json').read_text())
        assert info['pid'] == child.pid and len(info['baseline_handler']) == 1
        handle = k.OpenProcess(0x400, False, child.pid)
        assert handle

        def snap():
            present = ctypes.c_int()
            assert k.CheckRemoteDebuggerPresent(handle, ctypes.byref(present))
            return dict(unix=time.time(), debugger=bool(present.value), exit=child.poll(),
                        beats=(folder/'heartbeat.bin').stat().st_size)

        record['baseline'] = snap()
        assert record['baseline']['debugger'] is False
        with (folder/'debugger.log').open('xb') as log:
            debugger = subprocess.Popen([sys._base_executable, str(Path(__file__).resolve()),
                                       '--debugger', str(folder), '--mode', mode], stdout=log,
                                       stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
            record['debugger_pid'] = debugger.pid
            record['debugger_exit'] = debugger.wait(timeout=10)
        assert record['debugger_exit'] == 0
        result = json.loads((folder/'capture.json').read_text())
        assert result['detach'] and result['cleanup']['status'] == 'PASS'
        assert result['hits'], 'missing owned-breakpoint positive'
        record['post'] = [snap()]
        for _ in range(3):
            time.sleep(.15)
            record['post'].append(snap())
        assert all(s['exit'] is None and not s['debugger'] for s in record['post'])
        assert all(b['beats'] > a['beats'] for a,b in zip(record['post'], record['post'][1:]))
        if mode == 'positive':
            assert result['status']=='PASS' and not result['errors'] and not result['trigger_issued']
            assert not (folder/'delivery.json').exists()
        else:
            assert result['status']=='INVALID' and result['trigger_issued']
            delivery = json.loads((folder/'delivery.json').read_text())
            assert delivery['before'] == 1 and delivery['returned_from_raise']
            assert delivery['after'] == (1 if mode=='original' else 2), delivery
            record['delivery'] = delivery
        write(folder/'stop.flag', {'normal_exit_requested': True})
        child.wait(timeout=3)
        exit_info = json.loads((folder/'target-exit.json').read_text())
        assert child.returncode == 0 and exit_info['normal_exit']
        assert exit_info['handler_removed'] and exit_info['allocation_freed'] and not exit_info['debugger_present']
        record.update(status='CONTROL_SATISFIED', target_exit=exit_info, owned_hits=len(result['hits']))
    except BaseException as error:
        record['error'] = repr(error)
    finally:
        # Only the two Popen-owned handles can be stopped; no name/PID discovery.
        for role, proc in [('debugger',debugger), ('target',child)]:
            if proc is not None:
                if proc.poll() is None:
                    proc.kill()
                    record['forced_termination'].append(role)
                proc.wait(timeout=3)
        if child:
            stdout,stderr = child.communicate()
            (folder/'target.log').write_bytes(stdout+b'\n'+stderr)
        if handle: k.CloseHandle(handle)
        record['final_exits'] = {role: proc.returncode if proc else None
                                 for role,proc in [('debugger',debugger),('target',child)]}
        record['end_unix'] = time.time()
        write(folder/'result.json',record)
    print(mode,record['status'],record.get('error',''),flush=True)
    assert record['status']=='CONTROL_SATISFIED' and not record['forced_termination'], record


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',type=Path)
    parser.add_argument('--debugger',type=Path)
    parser.add_argument('--mode',choices=['positive','original','candidate'])
    args=parser.parse_args()
    if args.target: target(args.target)
    elif args.debugger: debug_child(args.debugger,args.mode)
    else:
        root=E.parents[4]
        board=json.loads((root/'Database/FFXII TZA/_index/_inbox/TEAM.json').read_text())
        assert any(t['id']=='ASTRA-NATIVE-DISPATCH-CONTROL' and t['status']=='ACTIVE'
                   and t['agent']=='ASTRA' for t in board['tasks'])
        for mode in ('positive','original','candidate'): run_arm(mode)
