"""Fresh durable checkpoint in existing owned records; one supported operation."""
import gc, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
tag=sys.argv[1]
state=W/(tag+'-state.json');operation=W/(tag+'-op.json');receipt=W/(tag+'-receipt.json')
if any(p.exists() for p in [state,operation,receipt]):raise ValueError('fresh receipt required; no replay')
c=subprocess.run([sys.executable,str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
state.write_text(json.dumps(dict(boardcheck_exit=c.returncode,stdout=c.stdout,stderr=c.stderr),indent=2))
if c.returncode or not c.stdout.strip().startswith('board ok: ') or c.stderr.strip():raise ValueError('supported current boardcheck failed')
s=importlib.util.spec_from_file_location('team',T);team=importlib.util.module_from_spec(s);s.loader.exec_module(team)
b=json.loads(team.BOARD.read_text(encoding='utf-8'))
parent=next(t for t in b['tasks'] if t['id']=='FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929')
if parent['status']!='ACTIVE' or parent['agent']!='ASTRA' or not any(r['key']=='file:database/tools/work/astra/runtime-residue-method-retriage' for r in team.hold_set(parent)):raise ValueError('current W ownership absent')
rev=b['revision'];epoch=b['recovery_epoch'];del parent,b;gc.collect()
note=(W/'checkpoint77-note.txt').read_text().strip()
methods=W/'METHODS.md';before=methods.read_bytes();preimage=W/'METHODS-before-checkpoint77.txt'
if preimage.exists():raise ValueError('existing METHODS checkpoint; reconcile, do not append twice')
preimage.write_bytes(before)
if methods.read_bytes()!=before:raise ValueError('METHODS preimage moved')
with methods.open('a',encoding='utf-8') as f:f.write('\n\n## Checkpoint77: consumed reviews, callback boundary and queue disposition\n\n'+note+'\n')
op=dict(action='checkpoint',task='FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929',note=note)
operation.write_text(json.dumps(dict(expect_revision=rev,epoch=epoch,operation=op,methods_preimage_sha256=hashlib.sha256(before).hexdigest()),indent=2))
try:r=team.transaction(team.BOARD,'ASTRA',op,session='SOL-ASTRA-checkpoint77',expect_revision=rev)
except Exception as e:
    receipt.write_text(json.dumps(dict(status='REFUSED_NO_REPLAY',error=repr(e)),indent=2));raise
receipt.write_text(json.dumps(dict(status='SUPPORTED_TRANSACTION_COMMITTED',revision=r['revision'],checkpoint=77),indent=2))
print(receipt.read_text())
