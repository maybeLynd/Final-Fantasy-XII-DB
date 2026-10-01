"""Reuse the existing synthetic event fixture to check the new callback branch."""
import ctypes
import importlib.util
import json
from pathlib import Path
import sys

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
FIX=ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'
sys.path.insert(0,str(FIX))
spec=importlib.util.spec_from_file_location('frozen_event_controls',FIX/'check.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def case(decision,variant='owned',raises=False,terminal=True):
    clock=old.Clock();f=old.Fixture(clock,variant,'capture');original=f.read_regs
    def regs(tid):
        ctx=original(tid)
        if ctx is not None:
            for n in ('Rdi','R10','Rbx','Rax'):setattr(ctx,n,0x123456789ab)
        return ctx
    f.read_regs=regs;called=[];aborted=[]
    def observe(m,pid,handle,tid,ctx,audit):
        assert f.stopped and f.pending_step=='owned' and not f.resumes
        called.append((tid,ctx.Rdi));f.calls.append(('observe',tid))
        if raises:raise OSError('supplied read failure')
        return dict(decision=decision,source='synthetic Python callback only')
    def abort(m,pid,handle,tid,audit):
        assert f.stopped and not f.resumes
        aborted.append(tid);f.calls.append(('abort_before_resume',tid))
        if terminal:f.ContinueDebugEvent(pid,tid,f.DBG_CONTINUE)
        return dict(terminal=terminal,pending_event_serviced=terminal)
    ns=dict(ctypes=ctypes,time=clock,owned_step=old.owned_step)
    old.selected(FIX/'cleanup_candidate.py',['cleanup'],ns)
    old.selected(W/'capture_scoped.py',['capture'],ns)
    result=ns['capture'](f,1,[0x200],1,f,observe,abort)
    return dict(result=result,callbacks=called,aborts=aborted,resumes=f.resumes,calls=f.calls)


def main():
    normal=case('STOP_MATCHED_PENDING_HEALTH')
    assert normal['result']['status']=='MATCHED_PENDING_HEALTH' and len(normal['callbacks'])==1
    assert normal['resumes']==['owned'] and not normal['aborts']
    controls={}
    for label,kwargs in [('hold',{}),('read_error',{'raises':True}),('unknown_decision',{'decision':'MAYBE'})]:
        args=dict(decision='HOLD_FOR_OWNED_ABORT');args.update(kwargs);r=case(**args)
        assert r['result']['status']=='CONTROL_ABORTED' and len(r['aborts'])==1 and not r['resumes']
        controls[label]=r
    for variant in ('foreign_rip','tf_same_rip','mixed_cause','wrong_slot','read_failure'):
        r=case('STOP_MATCHED_PENDING_HEALTH',variant)
        assert r['result']['status']=='INVALID' and not r['callbacks'] and not r['aborts'] and not r['resumes']
        controls[variant]=r
    r=case('HOLD_FOR_OWNED_ABORT',terminal=False)
    assert r['result']['status']=='INVALID' and not r['resumes'];controls['abort_not_terminal']=r
    out=dict(method='Synthetic callback-dispatch controls only',native_calls=0,normal=normal,controls=controls,
             limit='Checks the branch before resume; does not establish native termination/continuation semantics.')
    if '--write' in sys.argv:
        with (W/'scoped-dispatch-control.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'scoped-dispatch-control.json').read_text())==out
    print('Scoped callback is after ownership and before resume; abort/read-error/foreign-step controls reject continuation. Synthetic only.')


if __name__=='__main__':main()
