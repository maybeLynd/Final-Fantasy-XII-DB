"""EO3 stopped-read/abort control on directly owned disposable native children.

Reuses the frozen capture, API observer, Probe and native FP fixture. Added
markers/pointer seeds are explicit synthetic instrumentation, not FF12 code.
"""
import argparse
import ast
import ctypes as C
import hashlib
import importlib.util
import json
import mmap
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import uuid

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
EVIDENCE=ROOT/'Database/FFXII TZA/_experiments/evidence'
FIX=EVIDENCE/'exp127-instrument-control';FP=EVIDENCE/'native-fp-context-control'
PROBE=ROOT/'Database/Tools/analysis-kit/gfz-scripts/runtime_probe.py'
sys.path.insert(0,str(FIX/'original'));sys.path.insert(0,str(FIX))
from api_receipts import Audit
from project import project
from capture_scoped import capture

sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


sys.path.insert(0,str(FP))  # the reused runner imports its own fixture by name
prior=load('reused_native_fp_runner',FP/'run.py')
fixture=load('reused_native_fp_fixture',FP/'fixture.py')
write=prior.write
ABORT_CODE=0xea03
RAX_SEED=0x1122334455667788
PATH=b'PS2Data\\efb\\synthetic_stopped.efb\0'


def sources():
    paths=[W/'native_stop_control.py',W/'capture_scoped.py',W/'project.py',PROBE,
           FP/'run.py',FP/'fixture.py',FP/'preserve.bin',
           EVIDENCE/'exp127-native-dispatch-control/run.py',
           FIX/'ownership.py',FIX/'cleanup_candidate.py',*sorted((FIX/'original').glob('*.py'))]
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}


def configure(k):
    for name,args,ret in [
        ('VirtualProtect',[C.c_void_p,C.c_size_t,C.c_uint32,C.POINTER(C.c_uint32)],C.c_int),
        ('GetCurrentProcess',[],C.c_void_p),
        ('GetProcessId',[C.c_void_p],C.c_uint32),
        ('GetProcessTimes',[C.c_void_p,*([C.POINTER(C.c_ulonglong)]*4)],C.c_int),
        ('QueryFullProcessImageNameW',[C.c_void_p,C.c_uint32,C.c_wchar_p,C.POINTER(C.c_uint32)],C.c_int),
        ('FlushInstructionCache',[C.c_void_p,C.c_void_p,C.c_size_t],C.c_int),
        ('ReadProcessMemory',[C.c_void_p,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)],C.c_int),
        ('TerminateProcess',[C.c_void_p,C.c_uint32],C.c_int),
        ('WaitForSingleObject',[C.c_void_p,C.c_uint32],C.c_uint32),
        ('GetExitCodeProcess',[C.c_void_p,C.POINTER(C.c_uint32)],C.c_int)]:
        f=getattr(k,name);f.argtypes=args;f.restype=ret
    return k


def identity(k,handle):
    pid=k.GetProcessId(handle);assert pid
    stamp,exited,kernel,user=(C.c_ulonglong() for _ in range(4))
    assert k.GetProcessTimes(handle,C.byref(stamp),C.byref(exited),C.byref(kernel),C.byref(user))
    path=C.create_unicode_buffer(32768);n=C.c_uint32(len(path))
    assert k.QueryFullProcessImageNameW(handle,0,path,C.byref(n))
    return dict(pid=pid,creation=stamp.value,image=path.value,image_sha256=sha(path.value))


def make():
    original,oldgate=fixture.make('preserve');assert original==(FP/'preserve.bin').read_bytes()
    assert original[oldgate]==0x90
    before=bytes.fromhex('48 ff 83 00 0a 00 00 48 89 bb 10 0a 00 00 48 8d bb 00 0b 00 00 4c 8d 93 00 0a 00 00 48 b8')+struct.pack('<Q',RAX_SEED)
    after=bytes.fromhex('48 ff 83 08 0a 00 00 48 8b bb 10 0a 00 00')
    code=original[:oldgate]+before+b'\x90'+after+original[oldgate+1:]
    return code,oldgate+len(before),dict(original_sha256=hashlib.sha256(original).hexdigest(),original_gate=oldgate,
         inserted_before_hex=before.hex(),inserted_after_hex=after.hex(),
         meaning='Before counter; save/seed RDI; seed R10/RAX; original NOP gate; after counter; restore RDI. Existing FP body otherwise preserved.')


def target(folder):
    plan=json.loads((folder/'plan.json').read_text());assert plan['sources']==sources()
    k=configure(prior.dll());k.SetErrorMode(0x0001|0x0002|0x8000)
    code,gate,_=make();address=None;view=None;file=None;normal=False
    try:
        file=(folder/'shared.bin').open('r+b');view=mmap.mmap(file.fileno(),4096,access=mmap.ACCESS_WRITE)
        data=C.addressof(C.c_char.from_buffer(view));assert data%16==0 and data>0xffffffff
        C.memmove(data,fixture.seed(),len(fixture.seed()));C.memmove(data+0xb00,PATH,len(PATH))
        address=k.VirtualAlloc(None,8192,0x3000,4);assert address and address>0xffffffff
        C.memmove(address,code,len(code));old=C.c_uint32()
        assert k.VirtualProtect(address,4096,0x20,C.byref(old))
        assert k.VirtualProtect(address+4096,4096,1,C.byref(old))
        assert k.FlushInstructionCache(k.GetCurrentProcess(),address,len(code))
        assert C.string_at(address,len(code))==code
        native=C.CFUNCTYPE(C.c_uint32,C.c_void_p)(address)
        def sample():
            returned=native(data)
            row=dict(unix=time.time(),returned=returned,buffer_hex=C.string_at(data,0xa00).hex(),
                     counters=list(struct.unpack_from('<QQ',view,0xa00)))
            fixture.verify_sample(row,'preserve',allow_fip_truncation=True)
            assert row['counters'][0]==row['counters'][1]
            return row
        baseline=sample();assert not k.IsDebuggerPresent();write(folder/'baseline.json',baseline)
        write(folder/'target-ready.json',dict(identity=identity(k,k.GetCurrentProcess()),parent_pid=os.getppid(),nonce=plan['nonce'],
              tid=k.GetCurrentThreadId(),code_address=address,gate_address=address+gate,guard_address=address+4096,
              buffer_address=data,path_address=data+0xb00,counter_address=data+0xa00,path_hex=PATH.hex(),
              code_hex=C.string_at(address,len(code)).hex(),sources=sources()))
        deadline=time.monotonic()+20
        with (folder/'samples.jsonl').open('x',buffering=1) as log:
            while not (folder/'stop.flag').exists():
                assert time.monotonic()<deadline,'bounded child deadline'
                log.write(json.dumps(sample())+'\n');time.sleep(.05)
        normal=True
    finally:
        freed=bool(k.VirtualFree(address,0,0x8000)) if address else None
        if view is not None:view.flush();view.close()
        if file is not None:file.close()
        write(folder/'target-exit.json',dict(normal=normal,code_freed=freed,shared_mapping_closed=view is not None,
                                           debugger_present=bool(k.IsDebuggerPresent())))


class ScopedAudit(Audit):
    def __init__(self,api,path):
        super().__init__(api,path);self.event=None;self.event_id=0;self.thread_handles={};self.last_get=None

    def __getattr__(self,name):
        inherited=super().__getattr__(name)
        if name not in ('WaitForDebugEvent','ContinueDebugEvent','OpenThread','CloseHandle',
                        'GetThreadContext','SetThreadContext','ReadProcessMemory','TerminateProcess'):
            return inherited
        def call(*args):
            request=proposed=None
            if name in ('GetThreadContext','SetThreadContext'):
                request=args[1]._obj.ContextFlags
                if name=='SetThreadContext':proposed=bytes(args[1]._obj).hex()
            result=inherited(*args);error=C.get_last_error()
            if name=='WaitForDebugEvent' and result:
                ev=args[0]._obj;self.event_id+=1
                self.event=dict(id=self.event_id,pid=ev.dwProcessId,tid=ev.dwThreadId,code=ev.dwDebugEventCode)
                if ev.dwDebugEventCode==1:
                    self.event.update(address=ev.u.Exception.ExceptionRecord.ExceptionAddress,
                                      exception=ev.u.Exception.ExceptionRecord.ExceptionCode,first_chance=ev.u.Exception.dwFirstChance)
                self.mark('scoped_event',**self.event)
            elif name=='ContinueDebugEvent' and result:
                assert self.event and (args[0],args[1])==(self.event['pid'],self.event['tid'])
                self.event=None
            elif name=='OpenThread' and result:self.thread_handles[int(result)]=dict(tid=args[2],open_index=len(self.rows)-1)
            elif name=='CloseHandle':
                self.mark('CloseHandle',handle=int(args[0]),result=int(result),thread=self.thread_handles.get(int(args[0])))
                if result:self.thread_handles.pop(int(args[0]),None)
            elif name in ('GetThreadContext','SetThreadContext'):
                ctx=args[1]._obj;binding=self.thread_handles.get(int(args[0]))
                values=dict(api=name,result=int(result),handle=int(args[0]),requested_flags=request,
                            address=C.addressof(ctx),size=C.sizeof(ctx),context_hex=proposed if proposed else bytes(ctx).hex(),
                            thread_binding=binding,event=dict(self.event) if self.event else None)
                self.mark('full_context',**values)
                if name=='GetThreadContext':self.last_get=dict(operation='full_context',**values,api_index=len(self.rows)-1)
            elif name=='ReadProcessMemory':
                n=args[4]._obj.value
                self.mark('ReadProcessMemory',handle=int(args[0]),address=args[1].value,requested=args[3].value,
                          result=int(result),transferred=n,error=error,raw_hex=C.string_at(args[2],n).hex(),
                          event=dict(self.event) if self.event else None)
            elif name=='TerminateProcess':self.mark('TerminateProcess',handle=int(args[0]),exit_code=args[1],result=int(result),error=error)
            C.set_last_error(error);return result
        return call


def debugger(folder):
    plan=json.loads((folder/'plan.json').read_text());info=json.loads((folder/'target-ready.json').read_text())
    owned=json.loads((folder/'owned-child.json').read_text());assert plan['sources']==info['sources']==sources()
    assert owned['identity']==info['identity'] and info['nonce']==plan['nonce']
    assert owned['parent_pid']==info['parent_pid']==plan['parent_pid']
    original=load('frozen_native_capture_loader',FIX/'original/capture.py');m=original.load_source();configure(m.k32)
    audit=ScopedAudit(m.k32,folder/'api.json');m.k32=audit
    probe_defs=[n for n in ast.parse(PROBE.read_text()).body if isinstance(n,ast.ClassDef) and n.name=='Probe']
    assert len(probe_defs)==1
    ns={'ctypes':C,'k32':audit};exec(compile(ast.Module(body=probe_defs,type_ignores=[]),str(PROBE),'exec'),ns)
    pid=owned['identity']['pid']
    def observe(m,pid,handle,tid,ctx,audit):
        assert identity(m.k32,handle)==owned['identity'],'owned process identity changed'
        row=audit.last_get;event=audit.event
        assert event and event['pid']==pid and event['tid']==tid and event['first_chance']==1
        assert row['event']==event and row['thread_binding']['tid']==tid
        assert row['address']==C.addressof(ctx) and row['context_hex']==bytes(ctx).hex()
        values=project(row);assert values['rip']==info['gate_address'] and values['rax']==RAX_SEED
        assert values['rdi']==info['path_address'] and values['r10']==info['counter_address']
        assert values['rcx']==values['rbx']==info['buffer_address']
        reader=ns['Probe'](handle);begin=len(audit.rows)
        assert reader.read(info['code_address'],len(bytes.fromhex(info['code_hex'])))==bytes.fromhex(info['code_hex'])
        path=bytearray()
        for offset in range(128):
            b=reader.read(values['rdi']+offset,1)
            if b is None:raise OSError('path read failed')
            path+=b
            if b==b'\0':break
        assert bytes(path)==PATH
        raw=reader.read(values['r10'],24);assert raw is not None
        before,after,saved_rdi=struct.unpack('<QQQ',raw);assert before==after+1
        observed=dict(event=event,context_read=row,values=values,path_hex=bytes(path).hex(),
                      counter_hex=raw.hex(),before=before,after=after,saved_rdi=saved_rdi,read_begin=begin,read_end=len(audit.rows))
        write(folder/'stopped-observation.json',observed)
        if plan['arm']=='read-failure':
            assert reader.read(info['guard_address'],1) is None
            raise OSError('intentional NOACCESS read control; no resume permitted')
        return dict(decision='STOP_MATCHED_PENDING_HEALTH' if plan['arm']=='normal' else 'HOLD_FOR_OWNED_ABORT',**observed)
    def abort(m,pid,handle,tid,audit):
        assert identity(m.k32,handle)==owned['identity'],'abort ownership changed'
        assert audit.event and audit.event['pid']==pid and audit.event['tid']==tid
        out=dict(pending_event_serviced=False,terminal=False,exit_event=False)
        assert m.k32.TerminateProcess(handle,ABORT_CODE),'owned termination failed'
        # Acknowledging a terminated process's pending event is not assumed to
        # prevent execution. The shared successor marker is the actual control.
        assert m.k32.ContinueDebugEvent(pid,tid,m.DBG_CONTINUE)
        out['pending_event_serviced']=True
        ev=m.DEBUG_EVENT();deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            if not m.k32.WaitForDebugEvent(C.byref(ev),100):
                assert C.get_last_error() in (0,121),'abort drain wait failed'
                continue
            assert ev.dwProcessId==pid,'foreign event during abort drain'
            code=ev.dwDebugEventCode
            assert m.k32.ContinueDebugEvent(pid,ev.dwThreadId,m.DBG_CONTINUE)
            if code==5:out['exit_event']=True;break
        out['wait_result']=m.k32.WaitForSingleObject(handle,1000)
        status=C.c_uint32();assert m.k32.GetExitCodeProcess(handle,C.byref(status))
        out['exit_code']=status.value
        out['terminal']=out['exit_event'] and out['wait_result']==0 and status.value==ABORT_CODE
        audit.mark('owned_abort_terminal',**out)
        return out
    try:write(folder/'capture.json',capture(m,pid,[info['gate_address']],2,audit,observe,abort))
    finally:audit.save()


def run(folder,arm):
    import capstone
    folder.mkdir();code,gate,changes=make()
    decoded=list(capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64).disasm(code,0))
    assert sum(i.size for i in decoded)==len(code) and decoded[-1].mnemonic=='ret'
    assert next(i for i in decoded if i.address==gate).mnemonic=='nop'
    (folder/'fixture.bin').write_bytes(code)
    write(folder/'fixture.json',dict(gate=gate,changes=changes,capstone=capstone.__version__,
          instructions=[dict(offset=i.address,bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str) for i in decoded]))
    plan=dict(arm=arm,nonce=str(uuid.uuid4()),parent_pid=os.getpid(),sources=sources(),host=prior.host_identity(),
              method='native synthetic stopped-event/abort control; no FF12 or original instructions',
              question='Does the owned stopped callback precede resume, and does abort prevent the successor marker?')
    write(folder/'plan.json',plan)
    k=configure(prior.dll());child=debug=None;handle=None;view=None;file=None
    result=dict(status='INVALID',arm=arm,forced_termination=[])
    try:
        file=(folder/'shared.bin').open('x+b');file.write(bytes(4096));file.flush()
        view=mmap.mmap(file.fileno(),4096,access=mmap.ACCESS_WRITE)
        with (folder/'target.log').open('xb') as target_log:
            child=subprocess.Popen([sys._base_executable,str(Path(__file__).resolve()),'--target',str(folder.resolve())],
                    stdout=target_log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            deadline=time.monotonic()+6
            while not (folder/'target-ready.json').exists() or not (folder/'samples.jsonl').exists():
                assert child.poll() is None and time.monotonic()<deadline,'target baseline deadline/exit'
                time.sleep(.02)
            info=json.loads((folder/'target-ready.json').read_text());assert info['identity']['pid']==child.pid
            assert info['parent_pid']==os.getpid() and info['nonce']==plan['nonce']
            handle=k.OpenProcess(0x400,False,child.pid);assert handle
            assert identity(k,handle)==info['identity']
            write(folder/'owned-child.json',dict(identity=info['identity'],parent_pid=os.getpid(),popen_pid=child.pid))
            present=C.c_int();assert k.CheckRemoteDebuggerPresent(handle,C.byref(present)) and not present.value
            with (folder/'debugger.log').open('xb') as debug_log:
                debug=subprocess.Popen([sys._base_executable,str(Path(__file__).resolve()),'--debugger',str(folder.resolve())],
                        stdout=debug_log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
                assert debug.wait(timeout=12)==0,'scoped debugger exited unsuccessfully'
            captured=json.loads((folder/'capture.json').read_text());observed=json.loads((folder/'stopped-observation.json').read_text())
            if arm=='normal':
                assert captured['status']=='MATCHED_PENDING_HEALTH' and not captured['errors']
                assert captured['detach'] and captured['cleanup']['status']=='PASS' and captured['handle_closed']
                first=(folder/'samples.jsonl').stat().st_size;time.sleep(.2)
                assert child.poll() is None and (folder/'samples.jsonl').stat().st_size>first
                assert k.CheckRemoteDebuggerPresent(handle,C.byref(present)) and not present.value
                write(folder/'stop.flag',dict(normal_exit_requested=True));assert child.wait(timeout=3)==0
                ended=json.loads((folder/'target-exit.json').read_text())
                assert ended['normal'] and ended['code_freed'] and ended['shared_mapping_closed'] and not ended['debugger_present']
            else:
                assert captured['status']=='CONTROL_ABORTED' and captured['abort']['terminal']
                assert child.wait(timeout=3)==ABORT_CODE and captured['handle_closed']
                assert not (folder/'target-exit.json').exists(),'target finally unexpectedly ran during terminate control'
            post=list(struct.unpack_from('<QQ',view,0xa00))
            if arm=='normal':assert post[0]==post[1] and post[1]>=observed['before']
            else:assert post==[observed['before'],observed['after']],'successor ran during intended stopped abort'
            samples=[json.loads(s) for s in (folder/'samples.jsonl').read_text().splitlines()];assert samples
            for s in samples:fixture.verify_sample(s,'preserve',allow_fip_truncation=True)
            result.update(status='NATIVE_STOP_CONTROL_OBSERVED',stopped_counters=[observed['before'],observed['after']],
                          final_counters=post,capture_status=captured['status'],samples=len(samples))
    except BaseException as failure:result['error']=repr(failure)
    finally:
        for role,proc in [('debugger',debug),('target',child)]:
            if proc:
                if proc.poll() is None:proc.kill();result['forced_termination'].append(role)
                proc.wait(timeout=3)
        result['read_handle_closed']=bool(k.CloseHandle(handle)) if handle else None
        if view is not None:
            (folder/'shared-final.bin').write_bytes(view[:]);view.close();result['parent_mapping_closed']=True
        if file is not None:file.close()
        result['final_exits']={role:proc.returncode if proc else None for role,proc in [('target',child),('debugger',debug)]}
        write(folder/'result.json',result)
    print(arm,result['status'],result.get('error',''),flush=True)
    assert result['status']=='NATIVE_STOP_CONTROL_OBSERVED' and not result['forced_termination'] and result['read_handle_closed']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--target',type=Path);p.add_argument('--debugger',type=Path)
    p.add_argument('--arm',choices=['normal','abort','read-failure']);p.add_argument('--out',type=Path);args=p.parse_args()
    if args.target:target(args.target)
    elif args.debugger:debugger(args.debugger)
    else:
        board=json.loads((ROOT/'Database/FFXII TZA/_index/_inbox/TEAM.json').read_text())
        assert any(t['id']=='FABLE-REQ-ASTRA-EO3-PATH-POINTER' and t['status']=='ACTIVE' and t['agent']=='ASTRA' for t in board['tasks'])
        assert args.out and args.arm
        run(args.out,args.arm)
