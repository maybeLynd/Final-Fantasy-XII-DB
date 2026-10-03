"""One supported FRONTIER request for the concrete atomic replacement failures."""
import gc, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
key='ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003'
ref=H.relative_to(ROOT).as_posix()
p=H/'write-denial-route-02.json'
if p.exists():raise ValueError('existing route receipt; no duplicate dispatch')
c=subprocess.run([sys.executable,str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
record=dict(boardcheck=dict(exit=c.returncode,stdout=c.stdout,stderr=c.stderr))
if c.returncode or not c.stdout.strip().startswith('board ok: ') or c.stderr.strip():
    record['status']='BOARD_CHECK_REFUSED_NO_WRITE';p.write_text(json.dumps(record,indent=2));raise ValueError('boardcheck refused')
s=importlib.util.spec_from_file_location('team',T);team=importlib.util.module_from_spec(s);s.loader.exec_module(team)
b=json.loads(team.BOARD.read_text(encoding='utf-8'))
if any(t['id']==key for t in b['tasks']):raise ValueError('request already exists; do not duplicate')
rev=b['revision'];epoch=b['recovery_epoch'];del b;gc.collect()
op=dict(action='add',task=dict(id=key,kind='request',priority='P1',requester='ASTRA',assigned_to='SWE2-FRONTIER',
 target='Supported team.transaction atomic replace of canonical TEAM.json',scope='Diagnose concrete intermittent Windows WinError5 atomic replace denial; preserve journal guards and current claims',
 question='Two current supported ASTRA transactions failed at team.py _write_board_text os.replace(temp,TEAM.json) with WinError5 access denied, after many positive transactions. Please identify the reader/file-sharing/access cause and repair the owning invocation/path if warranted; do not restore board, reap locks or bypass journal/CAS protections. Audit stopped after61 accepted operations; prepared62 claim never landed. Exact receipts in '+ref+'.',
 known_evidence='Current boardcheck exit0 remains authoritative and reports ok/abort. First failed59 intent never landed; fresh CAS successor59..61 committed. Second62 failed replace; no second retry. Accepted prefix and both failures retained. Missing old exec handle/CIM denial do not prove global process absence.',
 missing_information='Cause of intermittent replacement denial and a supported reliable next write/control; any concurrency/file-share-delete interaction is a hypothesis only.',
 why_it_matters='Current owner queue reconciliation cannot finish safely with blind write retries; partial resumed request needs exact owner disposition. No game or database semantic claims depend on this administrative failure.',
 what_is_blocked='Remaining queue-disposition writes, not independent offline FF12 evidence. FABLE-REQ-ASTRA-REAR-HALF-VOICE-PAN-LISTENING-TEST is currently READY only because resume61 committed; it is NOT a prepared live task.',
 completion='Concrete cause/control or bounded explanation and supported safe continuation; exact deployed path/check identities, no guard weakening.',
 checkpoint='Queued by ASTRA',dependencies=[],resources=[dict(key='request:'+key.lower())]))
(H/'write-denial-op-02.json').write_text(json.dumps(dict(expect_revision=rev,epoch=epoch,operation=op),indent=2))
try:r=team.transaction(team.BOARD,'ASTRA',op,session='SOL-ASTRA-write-denial-route-1003',expect_revision=rev)
except Exception as e:
    record.update(status='ROUTE_REFUSED_NO_RETRY',error=repr(e));p.write_text(json.dumps(record,indent=2));raise
record.update(status='ROUTED_ONCE_SUPPORTED',revision=r['revision'],task=key)
p.write_text(json.dumps(record,indent=2));print(json.dumps(record))
