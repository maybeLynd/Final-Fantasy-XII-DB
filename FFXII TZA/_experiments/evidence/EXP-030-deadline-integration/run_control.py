"""Run the exact capture CLI on only owned EXP029 heartbeat children."""
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent/'EXP-029-timeout-cleanup/run.py'


def run(mode):
    folder = HERE/mode
    folder.mkdir()
    result = dict(status='INCOMPLETE',target_source_sha256=hashlib.sha256(TARGET.read_bytes()).hexdigest(),
                  harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    child = debugger = None
    k = ctypes.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes = [ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    k.OpenProcess.restype = ctypes.c_void_p
    k.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
    k.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = None
    try:
        child = subprocess.Popen([sys._base_executable,str(TARGET),'--target',str(folder)])
        deadline = time.monotonic()+10
        while not (folder/'heartbeat.bin').exists():
            assert child.poll() is None and time.monotonic()<deadline
            time.sleep(0.02)
        info = json.loads((folder/'target-ready.json').read_text())
        assert child.pid == info['pid']
        handle = k.OpenProcess(0x400,False,child.pid)
        assert handle
        def snap():
            present = ctypes.c_int()
            assert k.CheckRemoteDebuggerPresent(handle,ctypes.byref(present))
            return dict(unix=time.time(),exit=child.poll(),debugger=bool(present.value),
                        beats=(folder/'heartbeat.bin').stat().st_size)
        result['baseline'] = snap()
        assert result['baseline']['debugger'] is False
        cmd = [sys._base_executable,str(HERE/'capture.py'),'--pid',str(child.pid),'--addr',
               hex(info['address']+(mode=='cold')),'--seconds','2','--out',str(folder/'capture')]
        result['command'] = cmd
        with (folder/'capture-console.txt').open('x') as log:
            debugger = subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
            result['capture_exit'] = debugger.wait(timeout=12)
        result['post'] = [snap()]
        for _ in range(3):
            time.sleep(0.3)
            result['post'].append(snap())
        captured = json.loads((folder/'capture/result.json').read_text())
        assert result['capture_exit']==0 and captured['status']=='PASS'
        assert all(x['exit'] is None and x['debugger'] is False for x in result['post'])
        assert all(b['beats']>a['beats'] for a,b in zip(result['post'],result['post'][1:]))
        hits = len(captured['hits'])
        assert (hits==0) if mode=='cold' else (hits>0)
        result.update(status='PASS',hits=hits)
    finally:
        for process in (debugger,child):
            if process is not None:
                if process.poll() is None: process.kill()
                process.wait(timeout=5)
        if handle: k.CloseHandle(handle)
        result['final_exits'] = [p.poll() if p else None for p in (debugger,child)]
        (folder/'control.json').write_text(json.dumps(result,indent=2)+'\n')
    print(mode,result['status'],result['hits'])


if __name__=='__main__':
    run('cold')
    run('positive')
