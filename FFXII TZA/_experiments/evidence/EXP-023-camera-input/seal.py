"""Verify positive camera evidence, retained failures and exact cleanup; seal source identities."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import team
board = json.loads(team.BOARD.read_text())
assert any(t['id']=='ASTRA-CAMERA-INPUT-PUB' and t['status']=='ACTIVE' and t['agent']=='ASTRA' for t in board['tasks'])
def read(name):
    return json.loads((root/name).read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for file,index,code in [('original-right.json',78,106),('candidate-right.json',64,92),('candidate-left.json',63,91)]:
    d=read(file)
    assert d['exit_code']==0 and d['status']=='COMPLETED' and d['pid']==15600
    s=d['stdout']
    assert 'indices while held: [%d]' % index in s
    assert 'code %3d' % code in s and 'still set after release: none' in s
    assert 'CONTROL, no key held for 1.00 s : clean' in s and 'polls that lost focus : 0' in s
    assert 'accepted=0' not in s and not d['stderr']
    for path,value in d['source_hashes'].items():
        assert sha(Path(path))==value
    rows.append(dict(file=file,index=index,code=code,hold_seconds=1.0,baseline_clean=True,release_clean=True,focus_lost=0))
identities=[]
for file in ['identity-before-elevated.json','identity-after.json']:
    d=read(file)
    assert d['status']=='OBSERVED' and d['pid']==15600 and d['module_verdict']=='clean'
    assert d['code_identity'][0]['sha256']=='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    for path,value in d['source_sha256'].items():
        assert sha(Path(path))==value
    for state in d['states']:
        assert state['units'][0]['hp']==103 and state['slot3']==0
    samples=d['samples']
    identities.append(dict(file=file,samples=len(samples),first_frame=samples[0]['frame_before'],last_frame=samples[-1]['frame_after'],cross_frame_reads=sum(s['frame_before']!=s['frame_after'] for s in samples)))
assert read('packet-controls.json')['input_events_delivered']==0
assert len(read('packet-controls.json')['cases'])==10
assert read('initial-packet-control-failure.json')['exit_code']==1
assert read('identity-before.json')['status']=='INVALID'
assert read('load-menu.json')['exit_code']!=0
assert read('launch.json')['error']
assert read('save-restored.json')['after']==read('save-before.json')['files']
assert read('save-restored.json')['verified_files']==26 and not read('close-receipt.json')['remaining']
sources=[kit/n for n in ['runtime_probe.py','runtime_input_probe.py','runtime_poke.py','window_focus.py','ffxii_runtime.py']]
sources += [root/'key_packet.py',root/'input_receipt.py',root.parent/'EXP-019-ledger/observe_ledger.py',root.parent/'EXP-019-ledger/probe_extension.py']
for p in sources:
    (root/('validated-'+p.name+'.bin')).write_bytes(p.read_bytes())
runs=[]
for name,args in [('check_source_hygiene.py',['--paths',str(root)]),('check_links.py',['--db',str(repo/'Database/FFXII TZA')]),('team.py',['validate'])]:
    command=[sys.executable,str(kit/name),*args]
    run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    runs.append(dict(command=command,exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))
    assert run.returncode==0,runs[-1]
report=dict(status='BOUNDED_POSITIVE_CONTROL_VALIDATED',publication_revision=board['revision'],live_controls=rows,identity_windows=identities,runs=runs,
            limits=['No enemy kill or group completion','No exact camera angles','No live vertical-arrow test','Two packet differences: one event and E0 flag','General shared probe negative verdicts not certified'])
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
files={p.relative_to(root).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n',encoding='utf-8')
print('PASS: exact three positive live controls, identity/state receipts, retained failures, cleanup, links/hygiene/board;',len(files),'sealed files')
