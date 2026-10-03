"""Apply this exact owner audit once through team.transaction, never board dumps.

Fresh CAS for every operation. Preserve accepted prefix and stop on any refusal;
the same tag is never replayed. Narrow claims are disposition-only, not runtime
or peer-page claims. Completion of wakeups is separate from game semantics.
"""
import gc
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T = ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
P = HERE/'dispositions-01.json'

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--apply':
        raise ValueError('usage: apply-dispositions.py --apply FRESH_TAG')
    folder = HERE/sys.argv[2]
    folder.mkdir()  # Existing tag refuses, never replays accepted prefix.
    plan = json.loads(P.read_text(encoding='utf-8'))
    def check(name):
        c = subprocess.run([sys.executable,str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
        (folder/(name+'.json')).write_text(json.dumps(dict(exit_code=c.returncode,stdout=c.stdout,stderr=c.stderr),indent=2))
        if c.returncode or 'board ok: ok' not in c.stdout:
            raise ValueError('current supported boardcheck failed')
    check('boardcheck-before')
    spec = importlib.util.spec_from_file_location('team',T)
    team = importlib.util.module_from_spec(spec); spec.loader.exec_module(team)
    b = json.loads(team.BOARD.read_text(encoding='utf-8'))
    by = {t['id']:t for t in b['tasks']}
    parent = by['FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929']
    if parent['status']!='ACTIVE' or parent['agent']!='ASTRA' or not any(r['key']=='file:database/tools/work/astra/runtime-residue-method-retriage' for r in team.hold_set(parent)):
        raise ValueError('current ASTRA W hold not confirmed')
    if b['recovery_epoch'] != plan['snapshot_epoch']:
        raise ValueError('epoch moved; audit not automatically rebased')
    expected = {}
    for r in plan['records']:
        for key in ('notification','underlying'):
            old = r['preimages'].get(key)
            if old:
                if by.get(old['id']) != old:
                    raise ValueError('task preimage moved: '+old['id'])
                expected[old['id']] = digest(old)
        for old in r['preimages'].get('dependency_returns',[]):
            if by.get(old['id']) != old or old['status']!='DONE':
                raise ValueError('returned dependency moved: '+old['id'])
    for p in plan['primary_records']:
        if hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()!=p['sha256']:
            raise ValueError('primary record changed: '+p['path'])
    before = dict(revision=b['revision'],epoch=b['recovery_epoch'],ready=sum(t['assigned_to']=='ASTRA' for t in team.ready(b,'ASTRA') if t.get('assigned_to')),active=sum(t['status']=='ACTIVE' and t.get('agent')=='ASTRA' for t in b['tasks']))
    (folder/'preflight.json').write_text(json.dumps(dict(status='CURRENT_PREIMAGES_VERIFIED',before=before,plan_sha256=hashlib.sha256(P.read_bytes()).hexdigest()),indent=2))
    del parent,by,b; gc.collect()
    serial = 0
    refs = ['file:'+P.relative_to(ROOT).as_posix(), 'file:'+(HERE/'DISPOSITIONS.md').relative_to(ROOT).as_posix()]

    def tx(op):
        nonlocal serial
        serial += 1
        b = json.loads(team.BOARD.read_text(encoding='utf-8'))
        task = next(t for t in b['tasks'] if t['id']==op['task'])
        if digest(task)!=expected[task['id']] or b['recovery_epoch']!=plan['snapshot_epoch']:
            raise ValueError('current preimage/epoch moved: '+op['task'])
        rev=b['revision']; del task,b; gc.collect()
        prefix = folder/('%03d'%serial)
        prefix.with_suffix('.op.json').write_text(json.dumps(dict(expect_revision=rev,operation=op),indent=2))
        try:
            result=team.transaction(team.BOARD,'ASTRA',op,session='SOL-ASTRA-queue-reconciliation-1003',expect_revision=rev)
        except Exception as e:
            prefix.with_suffix('.receipt.json').write_text(json.dumps(dict(status='REFUSED_STOP_NO_REPLAY',error=repr(e)),indent=2)); raise
        new=next(t for t in result['tasks'] if t['id']==op['task'])
        expected[new['id']]=digest(new)
        receipt=dict(status='SUPPORTED_TRANSACTION_COMMITTED',revision=result['revision'],task=op['task'],action=op['action'],task_sha256=expected[new['id']])
        prefix.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2))
        del new,result; gc.collect()

    for r in plan['records']:
        note = 'Owner reconciliation: '+r['accepted_or_returned']+' LIMITS: '+r['unresolved']+' Record: '+(HERE/'DISPOSITIONS.md').relative_to(ROOT).as_posix()
        u = r['underlying']
        if u and r['disposition']!='ALREADY_DONE':
            tx(dict(action='resume',task=u,note='Returned dependencies read; resume for bounded owner disposition only. '+note))
            tx(dict(action='claim',task=u,resources=[{'key':'target:astra/queue-reconciliation/'+u.lower()}],note='Disposition-only owner claim; no runtime or peer file writes. '+note))
            if r['disposition']=='FINISH_SCOPED':
                tx(dict(action='finish',task=u,note='Original bounded delivery complete; residual game questions remain explicit. '+note,result_refs=refs+r['evidence_refs']))
            else:
                tx(dict(action='block',task=u,note=note,resume_when=r['resume_when']))
        n=r['notification']
        tx(dict(action='claim',task=n,note='Consume this notice/request from its reviewed current owner disposition. '+note))
        tx(dict(action='finish',task=n,note='Notice handled; original request '+('remains OPEN on revised prerequisites.' if r['disposition']=='REBLOCK' else 'has the exact disposition recorded above.')+' No new experiment credit. '+note,result_refs=refs+r['evidence_refs']))
        print(json.dumps(dict(handled=n,disposition=r['disposition'],operations=serial)),flush=True)
    check('boardcheck-after')
    b=json.loads(team.BOARD.read_text(encoding='utf-8'))
    after=dict(revision=b['revision'],epoch=b['recovery_epoch'],ready=[t['id'] for t in team.ready(b,'ASTRA') if t.get('assigned_to')=='ASTRA'],active=[t['id'] for t in b['tasks'] if t['status']=='ACTIVE' and t.get('agent')=='ASTRA'])
    (folder/'result.json').write_text(json.dumps(dict(status='OWNER_RECONCILIATION_COMPLETE',before=before,after=after,operations=serial,limits=plan['limits']),indent=2))
    print(json.dumps(dict(status='COMPLETE',operations=serial,ready_before=before['ready'],ready_after=len(after['ready']),active_after=len(after['active']))),flush=True)

if __name__=='__main__': main()
