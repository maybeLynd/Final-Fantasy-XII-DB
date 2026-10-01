"""Actual Windows read transport controls on one owned, disposable Python child.
These are instrument controls, not execution/observation of FF12 instructions.
No peer processes, game state or native FF12 effects are exercised.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import bj1_guard_capture as target


def child():
    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    k32.VirtualAlloc.restype = ctypes.c_void_p
    k32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
    allocation = k32.VirtualAlloc(None, 0x4000, 0x3000, 4)
    if not allocation:
        raise OSError('fixture allocation failed')
    # Deliberately patterned, with zero and all three exceptional classifications.
    words = [0, 0xFFFFFFFF, 0x80000001, 0x80000000, 1] + [0x80000000+i for i in range(6, 1682)]
    assert len(words) == target.COUNT
    ctypes.memmove(allocation, (ctypes.c_uint32 * len(words))(*words), 4*len(words))
    control = b'\x19\x93\x0d\x0a\x1a\x0a'
    ctypes.memmove(allocation+0x2000, control, len(control))
    ctypes.memmove(allocation+0x2010, (ctypes.c_uint32*1)(0x80000691), 4)
    old = ctypes.c_ulong()
    if not k32.VirtualProtect(allocation+0x3000, 0x1000, 1, ctypes.byref(old)):
        raise OSError('fixture noaccess page failed')
    print(json.dumps(dict(pid=os.getpid(), base=allocation, control=allocation+0x2000, epoch=allocation+0x2010,
                          inaccessible=allocation+0x3000, words=words)), flush=True)
    sys.stdin.buffer.read(1)  # Parent-owned pipe closes on normal exit or exception.


def main(output):
    if output.exists():
        raise ValueError('immutable controls output already exists')
    kit = target.ROOT / 'Database/Tools/analysis-kit/gfz-scripts'
    sys.path.insert(0, str(kit))
    import runtime_probe as rp
    rp.k32.OpenProcess.restype = ctypes.c_void_p
    rp.k32.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
    rp.k32.CloseHandle.argtypes = [ctypes.c_void_p]
    rp.k32.ReadProcessMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    result = dict(status='INVALID', evidence_kind='owned synthetic process instrument control, not FF12',
                  driver_sha256=target.digest(__file__), collector_sha256=target.digest(target.__file__),
                  reused_reader_sha256=target.digest(kit/'runtime_probe.py'), controls=[])
    process = None
    handle = None
    try:
        # Windows venv python.exe can be a redirector: Popen.pid then belongs to
        # the waiting launcher, while the allocation belongs to its interpreter.
        # Use the actual base interpreter and require a child-reported PID match.
        child_command = [sys._base_executable, __file__, '--child']
        result['child_command'] = child_command
        process = subprocess.Popen(child_command, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   creationflags=0x08000000)
        # Child handshake read is bounded by process.communicate fallback cleanup.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(process.stdout.readline)
            try:
                fixture = json.loads(future.result(timeout=10))
            except BaseException:
                process.kill()  # Only the exact child object this driver owns.
                process.wait(timeout=5)
                raise
        result['popen_pid'] = process.pid
        assert fixture['pid']==process.pid, 'child memory owner differs from Popen process'
        handle = rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION|rp.PROCESS_VM_READ, False, fixture['pid'])
        if not handle:
            raise OSError('owned fixture read access unavailable')
        result['fixture'] = {k:v for k,v in fixture.items() if k!='words'}
        result['child_pid'] = process.pid
        rp.k32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        exit_state = ctypes.c_ulong()
        assert rp.k32.GetExitCodeProcess(handle, ctypes.byref(exit_state))
        result['child_state_before_read'] = exit_state.value
        assert exit_state.value == 259, 'fixture exited before observation'
        # Capture the immediate native failure, before any other Win32 operation.
        class DiagnosticProbe(rp.Probe):
            def read(self, address, size):
                ctypes.set_last_error(0)
                raw = super().read(address, size)
                self.last_error = ctypes.get_last_error() if raw is None else 0
                return raw
        reader = DiagnosticProbe(handle)
        rows = [dict(guard_va='%08X' % (target.BASE+4*i), replay_step='fixture')
                for i in range(target.COUNT)]
        kwargs = dict(load_base=fixture['base'], epoch_address=fixture['epoch'],
                      control_address=fixture['control'], control_bytes=rp.CONTROL_BYTES)
        good = target.collect(reader, rows, **kwargs)
        result['positive_capture'] = good
        result['positive_read_win32_error'] = reader.last_error
        assert good['status'] == 'COLLECTED_CONTEXT_PENDING', good.get('error')
        assert [x['value'] for x in good['guard_values']] == fixture['words']
        assert good['epoch_before'] == good['epoch_after'] == 0x80000691
        assert good['guard_values'][0]['observed_state'] == 'zero'
        assert good['guard_values'][1]['observed_state'] == 'building_sentinel'
        assert good['guard_values'][2]['observed_state'] == 'completion_token'
        assert all(good['guard_values'][i]['observed_state']=='outside_prepared_rule' for i in [3,4])
        assert reader.read(fixture['inaccessible']-4, 8) is None
        result['controls'].append(dict(name='actual partial/unreadable crossing', refused=True))
        bad = [dict(x) for x in rows]
        bad[3]['guard_va'] = '%X' % (target.BASE+fixture['inaccessible']-fixture['base'])
        short = target.collect(reader, bad, **kwargs)
        assert short['status']=='INVALID' and len(short['guard_values'])==3 and 'failed/short read' in short['error']
        result['controls'].append(dict(name='actual capture unreadable guard', raw=short, refused=True))
        wrong = dict(kwargs, control_bytes=b'BADBAD')
        bad_control = target.collect(reader, rows, **wrong)
        assert bad_control['status']=='INVALID' and not bad_control['guard_values']
        result['controls'].append(dict(name='actual capture wrong positive constant', raw=bad_control, refused=True))
        try:
            target.collect(reader, rows[:-1], **kwargs)
        except ValueError as exc:
            result['controls'].append(dict(name='missing population prerequisite', error=repr(exc), refused=True))
        else:
            raise AssertionError('missing population accepted')
        assert len(result['controls'])==4
        result['status']='PASS_TRANSPORT_ONLY_CONTEXT_STILL_REQUIRED'
    except Exception as exc:
        result['error']=repr(exc)
    finally:
        result['handle_closed'] = True if handle is None else bool(rp.k32.CloseHandle(handle))
        if process:
            try:
                remaining, errors = process.communicate('x', timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                remaining, errors = process.communicate(timeout=5)
            result.update(child_exit=process.returncode, child_stderr=errors, child_stdout_remaining=remaining)
        if not result['handle_closed'] or result.get('child_exit')!=0 or result.get('child_stderr'):
            result['status']='INVALID_CLEANUP'
        output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result.get(k) for k in ['status','handle_closed','child_exit','error']}))
    return 0 if result['status']=='PASS_TRANSPORT_ONLY_CONTEXT_STILL_REQUIRED' else 1


if __name__=='__main__':
    if sys.argv[1:]==['--child']:
        child()
    else:
        raise SystemExit(main(Path(sys.argv[1])))
