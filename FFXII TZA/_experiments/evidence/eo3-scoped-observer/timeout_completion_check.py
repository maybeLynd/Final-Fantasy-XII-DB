"""An incomplete event sequence cannot count as a completed EO3 observation.

Method A plus synthetic dispatch only. Reuses the retained event fixture; no
process access, original-code execution or new native control is performed.
"""
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
FIX=ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'
sys.path.insert(0,str(FIX))
spec=importlib.util.spec_from_file_location('timeout_old_fixture',FIX/'check.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def run(source,decisions,cleanup_ok=True):
    clock=old.Clock();f=old.Fixture(clock,'owned','capture')
    f.events=f.events[:1]+[f.step() for _ in decisions]
    original=f.read_regs
    def regs(tid):
        ctx=original(tid)
        if ctx is not None:
            for n in ('Rdi','R10','Rbx','Rax'):setattr(ctx,n,0x123456789ab)
        return ctx
    f.read_regs=regs;pending=list(decisions);callbacks=[]
    def observe(m,pid,handle,tid,ctx,audit):
        assert f.stopped and f.pending_step=='owned'
        decision=pending.pop(0);callbacks.append(decision)
        return dict(decision=decision,source='supplied incomplete/complete sequence')
    def abort(*args):raise AssertionError('this control does not request abort')
    ns=dict(ctypes=ctypes,time=clock,owned_step=old.owned_step)
    old.selected(FIX/'cleanup_candidate.py',['cleanup'],ns)
    cleanup=ns['cleanup']
    def wrapped_cleanup(*args,**kwargs):
        result=cleanup(*args,**kwargs)
        if not cleanup_ok:result.update(status='INVALID',reason='supplied cleanup failure')
        return result
    ns['cleanup']=wrapped_cleanup
    old.selected(source,['capture'],ns)
    result=ns['capture'](f,1,[0x200],1,f,observe,abort)
    assert not pending,'control failed to deliver its event sequence'
    return dict(result=result,callbacks=callbacks,resumes=f.resumes,calls=f.calls)


def main():
    v1=W/'capture_scoped.py';v2=W/'capture_scoped_v2.py'
    historical=run(v1,['CONTINUE'])
    assert historical['result']['status']=='MATCHED_PENDING_HEALTH'
    assert historical['callbacks']==['CONTINUE']
    arms={}
    for label,decisions,wanted in (
        ('no_event',[],'INCOMPLETE'),
        ('partial_then_timeout',['CONTINUE'],'INCOMPLETE'),
        ('more_partial_then_timeout',['CONTINUE','CONTINUE'],'INCOMPLETE'),
        ('first_complete',['STOP_MATCHED_PENDING_HEALTH'],'MATCHED_PENDING_HEALTH'),
        ('partial_then_complete',['CONTINUE','STOP_MATCHED_PENDING_HEALTH'],'MATCHED_PENDING_HEALTH')):
        r=run(v2,decisions);assert r['result']['status']==wanted,label
        assert r['result']['matched']==(wanted=='MATCHED_PENDING_HEALTH')
        assert len(r['resumes'])==len(decisions) and r['result']['detach']
        arms[label]=r
    failed=run(v2,['STOP_MATCHED_PENDING_HEALTH'],cleanup_ok=False)
    assert failed['result']['status']=='INVALID' and failed['result']['matched']
    arms['complete_but_cleanup_failed']=failed
    # Positive remains discriminating: v1's actual native-normal decision has
    # the identical API/dispatch sequence in v2. This is not a new native run.
    previous=run(v1,['STOP_MATCHED_PENDING_HEALTH'])
    current=arms['first_complete']
    assert previous['calls']==current['calls']
    assert previous['result']=={k:v for k,v in current['result'].items() if k!='matched'}
    out=dict(method='Offline synthetic event sequence; no native/game execution',
             sources={p.name:sha(p) for p in (v1,v2,Path(__file__))},
             historical_counterexample=historical,arms=arms,
             affected='v1 status alone is not proof of complete observation; original raw controls retained.',
             limits=['No actual FF12 three-site or game-health result.',
                     'The old native controls used explicit stop/abort decisions, not timeout CONTINUE.',
                     'EO3 Recorder.finish remains required; instrument status never closes the game claim.'])
    out=json.loads(json.dumps(out))
    if '--write' in sys.argv:
        with (W/'timeout-completion-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'timeout-completion-observation.json').read_text())==out
    print('Incomplete timeout/zero-event rejected as matches; completed sequence positive and failed-cleanup invalidity preserved. Synthetic only.')


if __name__=='__main__':main()
