"""Bounded native instrument qualification; only Popen-owned disposable targets.

No FF12 process discovery, launch, input, save/config access or live-game claim.
Reuses frozen capture/ownership/cleanup and prior native process conventions.
Historical receipts are exclusive-write; a failure must be investigated, not overwritten.
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

from fixture import make, seed, verify_sample

E = Path(__file__).resolve().parent
FIX = E.parent/'exp127-instrument-control'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prior = load('prior_native_fp_orchestration', E.parent/'exp127-native-dispatch-control/run.py')
dll, write = prior.dll, prior.write


def sources():
    paths = [E/'run.py', E/'fixture.py', E/'preserve.bin', E/'change.bin',
             E/'fixture-decode.json', E.parent/'exp127-native-dispatch-control/run.py',
             FIX/'capture_candidate.py', FIX/'cleanup_candidate.py', FIX/'ownership.py',
             *sorted((FIX/'original').glob('*.py'))]
    return {os.path.relpath(p,E).replace('\\','/'): sha(p) for p in paths}


def target(folder, mode):
    k = dll()
    k.SetErrorMode(0x0001 | 0x0002 | 0x8000)
    k.VirtualProtect.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32)]
    k.GetCurrentProcess.restype = ctypes.c_void_p
    k.FlushInstructionCache.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    code, gate = make(mode)
    assert code == (E/(mode+'.bin')).read_bytes()
    plan = json.loads((folder/'plan.json').read_text())
    assert plan['sources'] == sources()
    address = data = None
    normal = False
    try:
        address = k.VirtualAlloc(None,4096,0x3000,0x04)
        data = k.VirtualAlloc(None,4096,0x3000,0x04)
        assert address and data and not (data & 15)
        ctypes.memmove(address,code,len(code))
        old = ctypes.c_uint32()
        assert k.VirtualProtect(address,4096,0x20,ctypes.byref(old))
        assert k.FlushInstructionCache(k.GetCurrentProcess(),address,len(code))
        assert ctypes.string_at(address,len(code)) == code
        ctypes.memmove(data,seed(),len(seed()))
        call = ctypes.CFUNCTYPE(ctypes.c_uint32,ctypes.c_void_p)(address)
        def sample():
            returned = call(data)
            value = dict(unix=time.time(), returned=returned,
                         buffer_hex=ctypes.string_at(data,0xa00).hex())
            return value
        baseline = sample()
        assert not k.IsDebuggerPresent()
        write(folder/'baseline.json',baseline)
        verify_sample(baseline,mode)
        write(folder/'target-ready.json',dict(pid=os.getpid(),tid=k.GetCurrentThreadId(),
              code_address=address,gate_address=address+gate,buffer_address=data,
              code_hex=ctypes.string_at(address,len(code)).hex(),python=sys.executable,
              sources=sources(),created_unix=time.time()))
        end = time.monotonic()+15
        with (folder/'samples.jsonl').open('x',buffering=1) as log:
            while not (folder/'stop.flag').exists():
                assert time.monotonic()<end, 'owned-target deadline'
                row=sample()
                log.write(json.dumps(row)+'\n')
                verify_sample(row,mode)
                time.sleep(.05)
        normal=True
    finally:
        freed_code = bool(k.VirtualFree(address,0,0x8000)) if address else None
        freed_data = bool(k.VirtualFree(data,0,0x8000)) if data else None
        write(folder/'target-exit.json',dict(normal_exit=normal,code_freed=freed_code,
              data_freed=freed_data,debugger_present=bool(k.IsDebuggerPresent())))


def debug_child(folder):
    plan = json.loads((folder/'plan.json').read_text())
    info = json.loads((folder/'target-ready.json').read_text())
    owned = json.loads((folder/'owned-child.json').read_text())
    assert info['pid'] == owned['pid']
    assert plan['sources'] == info['sources'] == sources()
    sys.path.insert(0,str(FIX/'original'))
    sys.path.insert(0,str(FIX))
    original = load('fp_original_capture',FIX/'original/capture.py')
    m = original.load_source()
    from api_receipts import Audit
    class FullAudit(Audit):
        def __getattr__(self,name):
            call = super().__getattr__(name)
            if name not in ('GetThreadContext','SetThreadContext','WaitForDebugEvent'): return call
            def observed(*args):
                proposed = None
                if name == 'SetThreadContext':
                    proposed = bytes(args[1]._obj).hex()
                result = call(*args)
                error = ctypes.get_last_error()
                if name in ('GetThreadContext','SetThreadContext'):
                    ctx = args[1]._obj
                    self.mark('full_context',api=name,result=int(result),handle=int(args[0]),
                              requested_flags=ctx.ContextFlags,address=ctypes.addressof(ctx),
                              size=ctypes.sizeof(ctx),context_hex=proposed if proposed else bytes(ctx).hex(),
                              flt_offset=m.CONTEXT.FltSave.offset,flt_hex=bytes(ctx.FltSave).hex())
                elif result:
                    ev = args[0]._obj
                    if ev.dwDebugEventCode == 1:
                        self.mark('exception_chance',tid=ev.dwThreadId,
                                  exception=ev.u.Exception.ExceptionRecord.ExceptionCode,
                                  address=ev.u.Exception.ExceptionRecord.ExceptionAddress,
                                  first_chance=ev.u.Exception.dwFirstChance)
                ctypes.set_last_error(error)
                return result
            return observed
    audit=FullAudit(m.k32,folder/'api.json')
    m.k32=audit
    capture=load('fp_candidate_capture',FIX/'capture_candidate.py').capture
    try:
        write(folder/'capture.json',capture(m,info['pid'],[info['gate_address']],1.0,audit))
    finally:
        audit.save()


def run_arm(mode):
    folder=E/mode
    folder.mkdir()
    k=dll()
    child=debugger=handle=None
    record=dict(status='INVALID',mode=mode,method='native disposable instrument qualification, not FF12',
                start_unix=time.time(),sources=sources(),forced_termination=[])
    write(folder/'plan.json',record)
    try:
        child=subprocess.Popen([sys._base_executable,str(E/'run.py'),'--target',str(folder),'--mode',mode],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        record['owned_child_pid']=child.pid
        # Separate immutable process-identity receipt; don't rewrite the starting plan.
        write(folder/'owned-child.json',dict(pid=child.pid))
        end=time.monotonic()+5
        while not (folder/'target-ready.json').exists() or not (folder/'samples.jsonl').exists():
            assert child.poll() is None and time.monotonic()<end, 'target baseline failed'
            time.sleep(.02)
        info=json.loads((folder/'target-ready.json').read_text())
        assert info['pid']==child.pid
        verify_sample(json.loads((folder/'baseline.json').read_text()),mode)
        handle=k.OpenProcess(0x400,False,child.pid)
        assert handle
        def snap():
            present=ctypes.c_int()
            assert k.CheckRemoteDebuggerPresent(handle,ctypes.byref(present))
            return dict(unix=time.time(),debugger=bool(present.value),exit=child.poll(),
                        sample_bytes=(folder/'samples.jsonl').stat().st_size)
        record['baseline']=snap()
        assert not record['baseline']['debugger']
        with (folder/'debugger.log').open('xb') as log:
            debugger=subprocess.Popen([sys._base_executable,str(E/'run.py'),'--debugger',str(folder)],
                                      stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            record['debugger_pid']=debugger.pid
            record['debugger_exit']=debugger.wait(timeout=10)
        assert record['debugger_exit']==0, 'debugger failed'
        result=json.loads((folder/'capture.json').read_text())
        assert result['status']=='PASS' and result['detach'] and result['cleanup']['status']=='PASS'
        assert result['hits'] and not result['errors'], 'no owned breakpoint control'
        record['post']=[snap()]
        for _ in range(3):
            time.sleep(.15)
            record['post'].append(snap())
        assert all(s['exit'] is None and not s['debugger'] for s in record['post'])
        assert all(b['sample_bytes']>a['sample_bytes'] for a,b in zip(record['post'],record['post'][1:]))
        write(folder/'stop.flag',dict(normal_exit_requested=True))
        child.wait(timeout=3)
        exit_info=json.loads((folder/'target-exit.json').read_text())
        assert child.returncode==0 and exit_info['normal_exit']
        assert exit_info['code_freed'] and exit_info['data_freed'] and not exit_info['debugger_present']
        samples=[json.loads(s) for s in (folder/'samples.jsonl').read_text().splitlines()]
        assert samples
        for s in samples: verify_sample(s,mode)
        record.update(status='NATIVE_CONTROL_OBSERVED',target_exit=exit_info,
                      owned_hits=len(result['hits']),samples=len(samples))
    except BaseException as error:
        record['error']=repr(error)
    finally:
        for role,proc in [('debugger',debugger),('target',child)]:
            if proc is not None:
                if proc.poll() is None:
                    proc.kill()
                    record['forced_termination'].append(role)
                proc.wait(timeout=3)
        if child:
            stdout,stderr=child.communicate()
            (folder/'target.log').write_bytes(stdout+b'\n'+stderr)
        if handle: k.CloseHandle(handle)
        record['final_exits']={role:proc.returncode if proc else None for role,proc in [('debugger',debugger),('target',child)]}
        record['end_unix']=time.time()
        write(folder/'result.json',record)
    print(mode,record['status'],record.get('error',''),flush=True)
    assert record['status']=='NATIVE_CONTROL_OBSERVED' and not record['forced_termination']


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',type=Path)
    parser.add_argument('--debugger',type=Path)
    parser.add_argument('--mode',choices=['preserve','change'])
    args=parser.parse_args()
    if args.target: target(args.target,args.mode)
    elif args.debugger: debug_child(args.debugger)
    else:
        board=json.loads((E.parents[4]/'Database/FFXII TZA/_index/_inbox/TEAM.json').read_text())
        assert any(t['id']=='ASTRA-NATIVE-FP-CONTEXT-CONTROL' and t['status']=='ACTIVE' and t['agent']=='ASTRA' for t in board['tasks'])
        assert args.mode, 'one explicit arm at a time; inspect feasibility before proceeding'
        run_arm(args.mode)
