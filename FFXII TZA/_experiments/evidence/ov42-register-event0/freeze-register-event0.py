"""Freeze the bounded retained-code proof in the existing manifest format."""
import hashlib,json,platform,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'ov42-register-event0'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('proof-03','prove.py'),('control-01','control.py')]:
    s=json.loads((P/(tag+'.status.json')).read_bytes())
    if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s.get('driver_sha256')!=sha(P/driver) or not (P/(tag+'.stdout')).read_bytes() or (P/(tag+'.stderr')).read_bytes():
        raise ValueError('required actual producer failed: '+tag)
r=json.loads((P/'result-03.json').read_bytes());c=json.loads((P/'controls-01/result.json').read_bytes())
if r.get('producer_complete') is not True or len(r.get('paths',[]))!=2 or c.get('producer_complete') is not True or len(c.get('cli_refusals',[]))!=5 or len(c.get('path_controls',[]))!=4 or c.get('positive_result_sha256')!=sha(P/'result-03.json'):
    raise ValueError('missing/incomplete scientific result or controls')
for q in r['source_pins']:
    if sha(P/q['path'])!=q['sha256']:raise ValueError('source pin differs')
(P/'dependencies').mkdir()
shutil.copyfile(W/'validate-title-source-annotations.py',P/'dependencies/validate-title-source-annotations.py')
shutil.copyfile(W/'sd194-copier-limit/run.py',P/'run.py')
(P/'.gitattributes').write_bytes(b'* -text\n')
(P/'environment-01.json').write_text(json.dumps(dict(python=sys.version,interpreter_sha256=sha(Path(sys.executable)),platform=platform.platform(),method='A static retained-byte path analysis; no game or original execution'),indent=2)+'\n')
destination=W/'ov42-register-event0-frozen-ready';destination.mkdir();members=[]
for path in sorted(p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts):
    name=path.relative_to(P).as_posix();target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    if target.read_bytes()!=path.read_bytes():raise ValueError('frozen copy differs')
    members.append(dict(path=name,bytes=path.stat().st_size,sha256=sha(path)))
shutil.copyfile(Path(__file__),destination/Path(__file__).name)
members.append(dict(path=Path(__file__).name,bytes=Path(__file__).stat().st_size,sha256=sha(Path(__file__))))
(destination/'manifest.json').write_text(json.dumps(dict(package='ov42-register-event0',members=members,limits='Conditional prescribed handler/event0 local proof; no natural reachability/scheduling/lifetime/presentation; independent acceptance pending'),indent=2)+'\n')
row=dict(folder=destination.name,members=len(members),manifest_sha256=sha(destination/'manifest.json'))
(W/'freeze-register-event0-result.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row))
