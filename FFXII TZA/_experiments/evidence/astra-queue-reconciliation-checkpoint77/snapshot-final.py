"""Durable partial audit receipt from current authoritative board, not dashboard."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
out=H/'result-partial-01.json';rawout=H/'accepted-operations-01.json'
if out.exists() or rawout.exists():raise ValueError('immutable output already exists')
c=subprocess.run([sys.executable,str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
if c.returncode or not c.stdout.strip().startswith('board ok: ') or c.stderr.strip():raise ValueError('checked board unavailable')
s=importlib.util.spec_from_file_location('team',T);team=importlib.util.module_from_spec(s);s.loader.exec_module(team)
raw=team.BOARD.read_bytes();b=json.loads(raw.decode('utf-8'));by={t['id']:t for t in b['tasks']}
accepted={};failed=[]
for folder in [H/'apply-01',*sorted(H.glob('bounded-*'))]:
    for p in sorted(folder.glob('[0-9][0-9][0-9].receipt.json')):
        r=json.loads(p.read_text());serial=int(p.name[:3]);op=json.loads(p.with_name('%03d.op.json'%serial).read_text())
        entry=dict(serial=serial,path=p.relative_to(H).as_posix(),operation=op,receipt=r)
        if r['status']=='SUPPORTED_TRANSACTION_COMMITTED':
            if serial in accepted:raise ValueError('duplicate accepted serial')
            if not any(h.get('agent')=='ASTRA' and h['operation']==op['operation'] for h in b['history']):raise ValueError('accepted operation missing from current history')
            accepted[serial]=entry
        else:failed.append(entry)
if set(accepted)!=set(range(1,62)):raise ValueError('accepted prefix is not1..61')
rawout.write_text(json.dumps(dict(accepted=[accepted[k] for k in sorted(accepted)],failed=failed,limits='Exact supported operation/receipt content compacted additively; original individual receipts remain unchanged.'),indent=2))
ready=[t for t in team.ready(b,'ASTRA') if t.get('assigned_to')=='ASTRA']
snapshot=json.loads((H/'input-snapshot-01.json').read_text())
handled=[i['notification']['id'] for i in snapshot['items'] if by[i['notification']['id']]['status']=='DONE']
finished=[i['underlying']['id'] for i in snapshot['items'] if i['underlying'] and i['underlying']['status']!='DONE' and by[i['underlying']['id']]['status']=='DONE']
route=json.loads((H/'write-denial-additive-current-receipt-01.json').read_text())
request=by['ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003']
if route['status']!='ROUTED_ONCE_VERIFIED_CURRENT':raise ValueError('FRONTIER route is not verified')
r=dict(status='PARTIAL_OWNER_RECONCILIATION_WAITING_FOR_SUPPORTED_WRITE_CONTROL',boardcheck=dict(exit=c.returncode,stdout=c.stdout,stderr=c.stderr),revision=b['revision'],epoch=b['recovery_epoch'],board_sha256=hashlib.sha256(raw).hexdigest(),before=snapshot['assigned_ready'],ready_after=len(ready),active_after=sum(t['status']=='ACTIVE' and t.get('agent')=='ASTRA' for t in b['tasks']),handled_notices=handled,finished_original_scoped_deliveries=finished,ready=[dict(id=t['id'],priority=t['priority']) for t in ready],accepted_prefix='1..61',prepared_uncommitted=62,frontier_request=dict(id=request['id'],status=request['status'],checkpoint=request['checkpoint']),next_action='After FRONTIER control: re-check current board/task/history and continue only uncommitted62 claim/63 revised block; no accepted-prefix replay. Rear-half voice READY afterresume61 is not a prepared live task.',limits='Administrative notice handling is not scientific closure. EXP031 staysPARTIAL; no new runtime observations. Eighteen original unknown-residue dispositions in plan are NOT all applied. FullL1L2/M0M5 goal ACTIVE/NOT_MET. Gauge source package independently advances while queue writes wait.')
out.write_text(json.dumps(r,indent=2))
print(json.dumps(dict(status=r['status'],ready_before=r['before'],ready_after=r['ready_after'],handled_notices=len(handled),finished_scoped_deliveries=finished,frontier=request['status']),indent=2))
