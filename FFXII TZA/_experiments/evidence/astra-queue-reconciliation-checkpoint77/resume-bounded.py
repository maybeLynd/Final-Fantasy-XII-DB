"""Carry forward only uncommitted audit operations in small finite batches.

The original session handle disappeared after receipted op56; op57 was prepared
but not committed. No cause or process-absence inference comes from denied CIM.
Check the canonical history and task preimage before each new supported CAS.
Do not replay old operations or restore a board. At most five operations/run.
"""
import gc, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
PLAN=json.loads((H/'dispositions-01.json').read_text())
REFS=['file:'+(H/'dispositions-01.json').relative_to(ROOT).as_posix(),'file:'+(H/'DISPOSITIONS.md').relative_to(ROOT).as_posix()]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def ops():
    result=[]
    for r in PLAN['records']:
        note='Owner reconciliation: '+r['accepted_or_returned']+' LIMITS: '+r['unresolved']+' Record: '+(H/'DISPOSITIONS.md').relative_to(ROOT).as_posix()
        u=r['underlying']
        if u and r['disposition']!='ALREADY_DONE':
            result += [dict(action='resume',task=u,note='Returned dependencies read; resume for bounded owner disposition only. '+note),dict(action='claim',task=u,resources=[{'key':'target:astra/queue-reconciliation/'+u.lower()}],note='Disposition-only owner claim; no runtime or peer file writes. '+note)]
            if r['disposition']=='FINISH_SCOPED':result.append(dict(action='finish',task=u,note='Original bounded delivery complete; residual game questions remain explicit. '+note,result_refs=REFS+r['evidence_refs']))
            else:result.append(dict(action='block',task=u,note=note,resume_when=r['resume_when']))
        n=r['notification']
        result += [dict(action='claim',task=n,note='Consume this notice/request from its reviewed current owner disposition. '+note),dict(action='finish',task=n,note='Notice handled; original request '+('remains OPEN on revised prerequisites.' if r['disposition']=='REBLOCK' else 'has the exact disposition recorded above.')+' No new experiment credit. '+note,result_refs=REFS+r['evidence_refs'])]
    return result
def main():
    start=int(sys.argv[1]);last=int(sys.argv[2]);tag=sys.argv[3]
    sequence=ops()
    if not 1<=start<=last<=len(sequence) or last-start>=5:raise ValueError('five-operation maximum; explicit range required')
    dest=H/tag;dest.mkdir()  # Always fresh; never restarts accepted prefix.
    check=subprocess.run([sys.executable,str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
    (dest/'boardcheck.json').write_text(json.dumps(dict(exit=check.returncode,stdout=check.stdout,stderr=check.stderr),indent=2))
    # Supported boardcheck also returns exit0 / "board ok: abort" when a
    # pending intent never landed. The next transaction safely journals the
    # abort. Do not turn a successful checked guard into an incident merely
    # because its valid recovery diagnostic differs from "ok".
    if check.returncode or not check.stdout.strip().startswith('board ok: ') or check.stderr.strip():raise ValueError('supported boardcheck failed')
    spec=importlib.util.spec_from_file_location('team',T);team=importlib.util.module_from_spec(spec);spec.loader.exec_module(team)
    adjudication_path=H/'refusal-adjudication-01.json'
    adjudication=json.loads(adjudication_path.read_text()) if adjudication_path.exists() else {}
    expected={old['id']:digest(old) for r in PLAN['records'] for old in r['preimages'].values() if isinstance(old,dict) and 'id' in old}
    receipts={}
    for folder in [H/'apply-01',*sorted(H.glob('bounded-*'))]:
        for p in folder.glob('[0-9][0-9][0-9].receipt.json'):
            x=json.loads(p.read_text());serial=int(p.stem.split('.')[0])
            if x['status']!='SUPPORTED_TRANSACTION_COMMITTED':
                if adjudication.get('serial')==serial and adjudication.get('refused_receipt_sha256')==hashlib.sha256(p.read_bytes()).hexdigest() and serial not in receipts:
                    continue
                raise ValueError('refusal requires adjudication, not automatic continuation')
            if serial in receipts:raise ValueError('duplicate accepted serial')
            operation=json.loads(p.with_name('%03d.op.json'%serial).read_text())['operation']
            if operation!=sequence[serial-1]:raise ValueError('operation lineage differs')
            receipts[serial]=(x,operation)
    if set(receipts)!=set(range(1,start)):raise ValueError('start does not follow exact receipted prefix')
    b=json.loads(team.BOARD.read_text(encoding='utf-8'))
    parent=next(t for t in b['tasks'] if t['id']=='FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929')
    if parent['status']!='ACTIVE' or parent['agent']!='ASTRA' or not any(r['key']=='file:database/tools/work/astra/runtime-residue-method-retriage' for r in team.hold_set(parent)):raise ValueError('current W ownership absent')
    for serial in sorted(receipts):
        receipt,operation=receipts[serial]
        # The full canonical history proves which prepared operation landed.
        if not any(h.get('agent')=='ASTRA' and h.get('operation')==operation for h in b['history']):raise ValueError('accepted operation not in current history')
        expected[operation['task']]=receipt['task_sha256']
    for serial in range(start,len(sequence)+1):
        old=(H/'apply-01'/('%03d.op.json'%serial))
        if old.exists() and any(h.get('agent')=='ASTRA' and h.get('operation')==sequence[serial-1] for h in b['history']):raise ValueError('unreceipted prepared operation landed; reconcile before continuing')
    del parent,b;gc.collect()
    for serial in range(start,last+1):
        operation=sequence[serial-1]
        b=json.loads(team.BOARD.read_text(encoding='utf-8'));row=next(t for t in b['tasks'] if t['id']==operation['task'])
        if b['recovery_epoch']!=PLAN['snapshot_epoch'] or digest(row)!=expected[row['id']]:raise ValueError('fresh task preimage/epoch moved')
        revision=b['revision'];del row,b;gc.collect()
        p=dest/('%03d'%serial)
        p.with_suffix('.op.json').write_text(json.dumps(dict(expect_revision=revision,operation=operation),indent=2))
        try:r=team.transaction(team.BOARD,'ASTRA',operation,session='SOL-ASTRA-queue-reconciliation-bounded-1003',expect_revision=revision)
        except Exception as e:
            p.with_suffix('.receipt.json').write_text(json.dumps(dict(status='REFUSED_STOP_NO_REPLAY',error=repr(e)),indent=2));raise
        row=next(t for t in r['tasks'] if t['id']==operation['task']);expected[row['id']]=digest(row)
        p.with_suffix('.receipt.json').write_text(json.dumps(dict(status='SUPPORTED_TRANSACTION_COMMITTED',revision=r['revision'],task=operation['task'],action=operation['action'],task_sha256=expected[row['id']]),indent=2))
        del row,r;gc.collect()
        print(json.dumps(dict(serial=serial,action=operation['action'],task=operation['task'])),flush=True)
    (dest/'terminal.json').write_text(json.dumps(dict(status='BOUNDED_BATCH_COMPLETE',start=start,last=last,next=last+1,total=len(sequence)),indent=2))
if __name__=='__main__':main()
