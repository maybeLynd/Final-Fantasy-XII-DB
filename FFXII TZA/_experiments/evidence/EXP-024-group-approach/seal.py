"""Validate scoped approach receipts; never turn progress or cleanup into a kill claim."""
import ast
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
repo=root.parents[4]
kit=repo/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(kit));import team
board=json.loads(team.BOARD.read_text())
assert any(t['id']=='ASTRA-GROUP-APPROACH-PUB' and t['status']=='ACTIVE' and t['agent']=='ASTRA' for t in board['tasks'])
def read(name):return json.loads((root/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
controls=read('step-cleanup-controls.json')
assert controls['success'] and len(controls['cases'])==3 and controls['input_events_delivered']==0
receipts=[];sources={}
for path in root.glob('*.json'):
    d=json.loads(path.read_text())
    if not isinstance(d,dict) or 'sources' not in d:continue
    assert d['status'] in ('CONTROLLED_PULSE','READ_ONLY_SNAPSHOT') and d['pid']==17072
    for file,digest in d['sources'].items():
        assert sha(Path(file))==digest
        sources[file]=digest
    if d['status']=='CONTROLLED_PULSE':
        assert d['seen_indices']==[d['expected_code']-28] and not any(bytes.fromhex(d['after_release']))
        assert d['foreground']['ok'] and 0<d['hold']<=1
    receipts.append(dict(file=path.name,status=d['status'],key=d.get('key'),actual_hold=d.get('actual_hold')))
assert len(receipts)==16
block=read('approachB-block.json')
assert block['status']=='PULSE_LIMIT' and len(block['pulses'])==10
steps=block['pulses'][2:]
assert all(p['exit_code']==0 and p['player_hp']==103 and p['target_hp']==134 for p in steps)
assert all(p['nonprogress']==0 for p in steps)
assert block['end_unix']-block['start_unix']<20
last=read('approachB-09.json')['after']['rows']
player=next(r for r in last if r['slot']==0);target=next(r for r in last if r['actor']==block['tracked_actor'])
assert math.isclose(math.dist(player['position'],target['position']),steps[-1]['gap'])
q=read('qualified.json')
assert q['pid']==17072 and q['status']=='OBSERVED' and q['module_verdict']=='clean'
assert q['code_identity'][0]['sha256']=='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
assert read('save-restored.json')['after']==read('save-before.json')['files']
assert read('save-restored.json')['verified_files']==26
assert not read('close-receipt.json')['remaining']
for file,digest in q['source_sha256'].items():
    assert sha(Path(file))==digest;sources[file]=digest
for file in sources:
    p=Path(file);(root/('validated-'+p.name+'.bin')).write_bytes(p.read_bytes())
for p in root.glob('*.py'):ast.parse(p.read_bytes())
runs=[]
for name,args in [('check_source_hygiene.py',['--paths',str(root)]),('check_links.py',['--db',str(repo/'Database/FFXII TZA')]),('team.py',['validate'])]:
    command=[sys.executable,str(kit/name),*args]
    run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    runs.append(dict(command=command,exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))
    assert run.returncode==0,runs[-1]
report=dict(status='PARTIAL_APPROACH_VALIDATED_NO_KILL',publication_revision=board['revision'],receipts=receipts,
            initial_gap=block['initial_gap'],final_gap=steps[-1]['gap'],block_elapsed=block['end_unix']-block['start_unix'],runs=runs,
            limits=['First agent-paced window expired','Second block hit pulse limit','Wolf attacked after post-pulse health reads; screenshot HP86','No group actor visible identity or final death','No combat ledger trace'])
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
files={p.relative_to(root).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n',encoding='utf-8')
print('PASS: 16 control receipts, 3 injected cleanup cases, bounded progress, identity and exact restoration;',len(files),'sealed files; NO KILL CLAIM')
