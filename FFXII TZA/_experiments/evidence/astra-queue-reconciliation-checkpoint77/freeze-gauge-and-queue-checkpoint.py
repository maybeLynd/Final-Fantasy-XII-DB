"""Freeze validated gauge science and the explicitly PARTIAL queue audit once.

Queue receipts are evidence of supported board transitions, not new scientific
experiments. Never silently relabel the interrupted audit COMPLETE.
"""
import hashlib,json,platform,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
P=W/'ov42-gauge-callback-binding'
for tag,driver in [('extents-01','prepare-extents.py'),('capture-01','capture.py'),('target-extents-01','prepare-target-extents.py'),('capture-target-01','capture-target.py'),('prove-01','prove.py'),('control-01','control.py')]:
    s=json.loads((P/(tag+'.status.json')).read_text())
    if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s.get('driver_sha256')!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise ValueError('required successful current '+tag)
r=json.loads((P/'result-01.json').read_text());c=json.loads((P/'control-result-01.json').read_text())
if r.get('producer_complete') is not True or c.get('complete') is not True or len(r['source_controls'])!=4 or len(c['artifact_cases'])!=3:raise ValueError('missing/incomplete/zero gauge evidence')
if not(P/'.gitattributes').exists():(P/'.gitattributes').write_bytes(b'* -text\n')
if(P/'.gitattributes').read_bytes()!=b'* -text\n':raise ValueError('byte policy changed')
env=P/'environment-01.json'
if env.exists():raise ValueError('environment already frozen')
env.write_text(json.dumps(dict(python=sys.version,python_executable=str(Path(sys.executable)),python_sha256=sha(Path(sys.executable)),platform=platform.platform(),method=r['method']),indent=2))
def freeze(src,dst,files,kind,limits):
    if dst.exists():raise ValueError('immutable destination exists')
    dst.mkdir();members=[]
    for p,rel in files:
        q=dst/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
        members.append(dict(path=rel,bytes=p.stat().st_size,sha256=sha(p)))
    (dst/'manifest.json').write_text(json.dumps(dict(package=kind,members=members,limits=limits,acceptance='Immutable producer/owner records; no independent acceptance awarded'),indent=2))
    print(json.dumps(dict(folder=dst.name,members=len(members),manifest_sha256=sha(dst/'manifest.json'))))
selected=[(p,p.relative_to(P).as_posix()) for p in P.iterdir() if p.is_file()]+[(p,p.relative_to(P).as_posix()) for p in(P/'controls-01').rglob('*') if p.is_file()]
freeze(P,W/'ov42-gauge-callback-binding-frozen-ready',sorted(selected,key=lambda x:x[1]),'ov42-gauge-callback-binding','STATIC_ONLY original822B local dataflow/footprint. Prepared unrun handler capture is not another test. Natural state/transitive effects/lifetime/resource binding remain open.')
Q=W/'ready-queue-reconciliation-1002'
qr=json.loads((Q/'result-partial-01.json').read_text())
if qr['status']!='PARTIAL_OWNER_RECONCILIATION_WAITING_FOR_SUPPORTED_WRITE_CONTROL' or qr['accepted_prefix']!='1..61' or len(qr['handled_notices'])!=12 or len(qr['finished_original_scoped_deliveries'])!=3:raise ValueError('partial audit receipt missing/changed')
names=['build-dispositions.py','apply-dispositions.py','resume-bounded.py','route-write-denial.py','route-write-denial-current.py','route-additive-current.py','snapshot-final.py','input-snapshot-01.json','dispositions-01.json','DISPOSITIONS.md','refusal-adjudication-01.json','write-denial-route-01.json','write-denial-route-02.json','write-denial-additive-current-receipt-01.json','write-denial-additive-current-op-01.json','accepted-operations-01.json','result-partial-01.json']
files=[(Q/n,n) for n in names]+[(W/n,n) for n in ['checkpoint77.py','checkpoint77-note.txt','checkpoint77-op.json','checkpoint77-receipt.json','checkpoint77-current-owner-op.json','checkpoint77-current-owner-receipt.json']]+[(Path(__file__),'freeze-gauge-and-queue-checkpoint.py')]
bytepolicy=Q/'.gitattributes'
if not bytepolicy.exists():bytepolicy.write_bytes(b'* -text\n')
files.append((bytepolicy,'.gitattributes'))
freeze(Q,W/'astra-queue-reconciliation-checkpoint77-frozen-ready',files,'astra-queue-reconciliation-checkpoint77','PARTIAL owner queue audit;12 notices handled/3 existing scoped deliveries finished, snapshot19 READY.61 accepted operations/failed uncommitted62 preserved. Old long-lived audit launch driver identity was not pinned; current source is not fabricated as its original receipt. Board operation lineage checked against canonical history. No new empirical tests or scientific closure. Ownership audit waits FRONTIER request48428. Checkpoint77 current owner write verified; original CAS refusal retained.')
