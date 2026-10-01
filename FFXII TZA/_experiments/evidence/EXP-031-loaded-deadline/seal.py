"""Seal interrupted baseline without promoting the unrun capture."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
read=lambda name:json.loads((HERE/name).read_text())
window,run=read('baseline-window.json'),read('baseline-run.json')
assert window['status']=='OBSERVED' and run['status']=='COMPLETED'
assert not run['live_children'] and all(c['exit_code']==0 for c in run['commands'])
assert all(c['label']!='debugger' for c in run['commands'])
for name,digest in run['sources'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
samples=window['samples']
assert len(samples)==6154 and samples[-1]['seconds']>64.9
assert all(s['foreground_pid']==13964 and not s['debugger_present'] for s in samples)
assert all(set(s['held'])<={49,2} for s in samples)
assert window['module_verdict']=='clean' and window['modules']
assert len(window['code_identity'])==1 and window['code_identity'][0]['matches']
assert window['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
for key,index in [('Enter',49),('C',2)]:
    r=read('baseline-'+key+'.json')
    assert r['status']=='COMPLETED' and r['exit_code']==0
    text=r['stdout']
    for expected in ['baseline: all 256 bytes zero','foreground: the game','CONTROL, no key held for 0.35 s : clean',
                     'indices while held: [%d]'%index,'still set after release: none','polls that lost focus : 0']:
        assert expected in text,expected
    assert text.count('accepted=2 requested=2')==3
    for name,digest in r['source_sha256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest
rates=[]
for start,end in [(0,10),(10,20),(20,30),(30,40),(40,50),(50,60),(60,64.9)]:
    a=min(samples,key=lambda s:abs(s['seconds']-start))
    b=min(samples,key=lambda s:abs(s['seconds']-end))
    rates.append(dict(start=a['seconds'],end=b['seconds'],core_seconds_per_second=
                      (b['cpu_seconds']-a['cpu_seconds'])/(b['seconds']-a['seconds'])))
restored=read('save-restored.json')
assert restored['verified_files']==26 and restored['after']==read('save-before.json')['files']
assert not read('close-receipt.json')['remaining']
assert not (HERE/'deadline-capture').exists() and not (HERE/'capture-run.json').exists()
result=dict(status='INCOMPLETE',reason='UI stopped with physical Escape after baseline; no armed/post windows',
 baseline_receipts_verified=True,samples=len(samples),cpu_intervals=rates,restore_verified=True,
 missing=['armed deadline capture','post-capture window','baseline menu-closed screenshot'],
 scope='baseline execution/identity/input receipts only; no debugger validation')
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
files={p.relative_to(HERE).as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print(json.dumps(result))
