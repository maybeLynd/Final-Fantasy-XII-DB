"""Connected runner on retained synthetic events/contexts/EO3 memory only."""
import copy
import ctypes as C
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
FIX=ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'
sys.path.insert(0,str(FIX))
import run_eo3 as runner
from native_stop_check import Context
from observe_control import context,memory
from control import fixture
from owned_game_abort import EXE,EXE_SHA

spec=importlib.util.spec_from_file_location('eo3_runner_old_events',FIX/'check.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
EXPECTED=dict(pid=1,creation=12345678,image=EXE,image_sha256=EXE_SHA)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


class Harness(old.Fixture):
    def __init__(self,clock,case):
        super().__init__(clock,'owned','capture');self.case=case
        self.f=fixture(0x18bc13000 if case=='high_pointer' else 0x6abcd000)
        self.blobs,self.read_memory=memory(self.f);self.audit=None;self.phase=None
        self.contexts=dict(producer=self.f[0],builder=self.f[3],issuer=self.f[6])
        self.events=self.events[:1]+[(1,self.contexts[n]['tid'],self.EXCEPTION_SINGLE_STEP,
                      self.contexts[n]['rip'],n) for n in ('producer','builder','issuer')]
        if case in ('partial_timeout','stop_in_cleanup'):self.events=self.events[:2]
        self.stop_value=False;self.terminated=False
    def mark(self,name,**values):
        self.rows.append(dict(operation=name,**values))
    def threads_of(self,pid):return [11,77,88]+([12] if self.requested else [])
    def set_slots(self,tid,slots):
        ok=super().set_slots(tid,slots)
        return False if self.case=='arming_failure' and slots and tid==77 else ok
    def DebugActiveProcess(self,pid):self.calls.append(('attach',pid));return 1
    def OpenProcess(self,*args):self.calls.append(('open',args[2]));return 91
    def CloseHandle(self,handle):self.calls.append(('close',handle));return 1
    def WaitForDebugEvent(self,ptr,timeout):
        ok=super().WaitForDebugEvent(ptr,timeout)
        if ok:
            ev=ptr._obj;self.phase=self.pending_step
            self.audit.event=dict(id=len(self.calls),pid=ev.dwProcessId,tid=ev.dwThreadId,code=ev.dwDebugEventCode)
            if ev.dwDebugEventCode==1:
                self.audit.event.update(exception=ev.u.Exception.ExceptionRecord.ExceptionCode,
                                        first_chance=1,address=ev.u.Exception.ExceptionRecord.ExceptionAddress)
            if self.phase=='issuer':self.blobs[-1]=(self.f[6]['rbx'],bytes(self.f[7]))
        return ok
    def ContinueDebugEvent(self,pid,tid,status):
        phase=self.pending_step;result=super().ContinueDebugEvent(pid,tid,status)
        self.audit.event=None
        if self.case=='stop_after_producer' and phase=='producer':self.stop_value=True
        return result
    def DebugBreakProcess(self,*args):
        if self.case=='stop_in_cleanup':self.stop_value=True
        return super().DebugBreakProcess(*args)
    def read_regs(self,tid):
        if self.cleared:return super().read_regs(tid)
        if self.pending_step not in self.contexts:return super().read_regs(tid)
        values=self.contexts[self.pending_step];assert tid==values['tid']
        ctx=Context.from_buffer_copy(bytes.fromhex(context(values)['context_hex']))
        ctx.ContextFlags=0x10001b;ctx.EFlags=0x202
        ctx.Dr0,ctx.Dr1,ctx.Dr2=runner.SITES;ctx.Dr3=0;ctx.Dr7=0x415
        ctx.Dr6=0xffff0ff0|(1<<runner.SITES.index(ctx.Rip))
        row=dict(operation='full_context',api='GetThreadContext',result=1,requested_flags=0x10001b,
                 event=dict(self.audit.event),thread_binding=dict(tid=tid),address=C.addressof(ctx),
                 size=C.sizeof(ctx),context_hex=bytes(ctx).hex(),api_index=len(self.rows),
                 source='Synthetic current-context fixture; no native API receipt')
        if self.case=='stale_context':row['event']['id']-=1
        self.audit.last_get=row;return ctx
    def TerminateProcess(self,handle,code):
        assert self.stopped and handle==91 and code==0xea03
        self.calls.append(('terminate',handle,code));self.terminated=True
        self.events=[(5,77,0,0,'terminal')];return 1
    def WaitForSingleObject(self,*args):return 0
    def GetExitCodeProcess(self,handle,ptr):ptr._obj.value=0xea03;return 1


class Audit:
    def __init__(self,f):self.f=f;self.event=None;self.last_get=None;self.rows=f.rows;f.audit=self
    def __getattr__(self,name):return getattr(self.f,name)
    def mark(self,*args,**kwargs):self.f.mark(*args,**kwargs)


def run_case(case):
    clock=old.Clock();f=Harness(clock,case);audit=Audit(f)
    ns=dict(ctypes=C,time=clock,owned_step=old.owned_step)
    old.selected(FIX/'cleanup_candidate.py',['cleanup'],ns)
    old.selected(W/'capture_scoped_v2.py',['capture'],ns)
    original=runner.capture;runner.capture=ns['capture']
    def identity(api,handle):
        assert handle==91;f.calls.append(('identity',handle))
        return dict(EXPECTED,creation=999 if case=='different_lifetime' else EXPECTED['creation'])
    def qualify(handle):
        assert handle==91;f.calls.append(('qualify',handle))
        clock.now+=120  # deliberately long supplied preparation, before Recorder starts
        return dict(status='INVALID' if case=='failed_reference' else 'REFERENCE_CONTROLS_PASS',
                    source='Supplied qualification result, not live reference evidence')
    class Probe:
        def __init__(self,handle):assert handle==91
        def read(self,address,size):return f.read_memory(address,size)
    notices=[]
    def ready(receipt):
        assert not f.stopped,'ready was delivered before initial continuation'
        if case=='ready_delivery_failure':raise OSError('supplied readiness I/O failure')
        notices.append(receipt)
    try:
        result=runner.run(f,EXPECTED,audit,Probe,identity,qualify,clock=clock,stop=lambda:f.stop_value,ready=ready)
    finally:runner.capture=original
    assert f.k32 is f,'runner did not restore its API binding'
    return dict(result=result,calls=f.calls,rows=f.rows,resumes=f.resumes,terminated=f.terminated,ready=notices)


def stable(value):
    if isinstance(value,list):return [stable(x) for x in value]
    if isinstance(value,tuple):return [stable(x) for x in value]
    if isinstance(value,dict):
        value={k:stable(v) for k,v in value.items()}
        if value.get('operation')=='full_context':value['address']='same current ctypes buffer validated during this synthetic run'
        return value
    return value


def main():
    declarations=runner.frozen_loader()
    assert callable(declarations.load_source) and Path(declarations.HERE).resolve()==(FIX/'original').resolve()
    assert not hasattr(declarations,'k32'),'declaration import should not load native target API'
    cases={name:run_case(name) for name in ('complete','partial_timeout','high_pointer',
             'stale_context','different_lifetime','failed_reference','stop_after_producer',
             'stop_in_cleanup','arming_failure','ready_delivery_failure')}
    positive=cases['complete'];r=positive['result']
    assert r['status']=='OBSERVATION_PENDING_SESSION_HEALTH' and r['normalized']['results'][0]['pointer_preserved']
    assert not r['health_observed'] and not r['restoration_verified'] and not r['input_sent']
    assert r['recorder']['started']==120 and positive['resumes']==['producer','builder','issuer']
    assert [c[0] for c in positive['calls']][:4]==['open','identity','qualify','attach']
    assert cases['partial_timeout']['result']['status']=='INCOMPLETE'
    assert cases['partial_timeout']['result']['normalized'] is None
    for name in ('different_lifetime','failed_reference'):
        c=cases[name];assert c['result']['status']=='INVALID' and c['result']['recorder'] is None
        assert 'attach' not in [x[0] for x in c['calls']] and c['calls'][-1]==('close',91)
    for name in ('high_pointer','stale_context'):
        c=cases[name];assert c['result']['status']=='CONTROL_ABORTED' and c['terminated'] and not c['resumes']
        assert c['result']['normalized'] is None and not c['result']['health_observed']
    stopped=cases['stop_after_producer'];r=stopped['result']
    assert r['stop_latched'] and r['status']=='INVALID' and not stopped['terminated']
    assert stopped['resumes']==['producer'] and r['capture']['cleanup']['status']=='PASS' and r['capture']['detach']
    assert len(r['recorder']['events'])==1,'captured new semantic events after stop'
    c=cases['stop_in_cleanup'];r=c['result']
    assert r['status']=='INCOMPLETE' and r['capture']['cleanup']['status']=='PASS' and r['capture']['detach']
    assert not c['terminated'] and c['resumes']==['producer']
    assert [x for x in c['calls'] if x[0]=='slots' and not x[2]],'stop prevented register clearing'
    c=cases['arming_failure'];assert c['result']['status']=='INVALID' and not c['ready']
    c=cases['ready_delivery_failure'];r=c['result']
    assert r['status']=='INVALID' and r['readiness_error'] and not c['ready'] and not c['resumes']
    assert r['capture']['cleanup']['status']=='PASS' and r['capture']['detach']
    assert len(positive['ready'])==1 and positive['ready'][0]['sites']==runner.SITES
    assert [t for t,ok in positive['ready'][0]['arming'] if ok]==[11,77,88]
    out=dict(method='Connected synthetic runner, native_calls=0; no original FF12 code or live process',
             cases=stable(cases),tool_sha256={p.name:sha(p) for p in (W/'run_eo3.py',W/'capture_scoped_v2.py',Path(__file__))},
             limits=['Reference/module qualification result is supplied; CLI native qualification is not executed here.',
                     'Actual live initial state, input, session health and restoration remain unobserved.',
                     'Stop is cooperative between events; existing cleanup runs once and does not restart capture.'])
    if '--write' in sys.argv:
        with (W/'runner-connection-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'runner-connection-observation.json').read_text())==out
    print('Connected runner: complete chain stays pending health; partial/foreign-reference/context and stop controls discriminate. Synthetic only.')


if __name__=='__main__':main()
