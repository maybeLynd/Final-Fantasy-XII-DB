"""Freeze validated caller-stack evidence once using the existing manifest form."""
import hashlib,importlib.util,json,platform,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'sd194-caller-frames'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('extents-01','prepare.py'),('capture-01','capture.py'),('proof-02','prove.py'),('control-01','control.py')]:
    row=json.loads((P/(tag+'.status.json')).read_text())
    if row.get('terminal') is not True or row.get('exit')!=0 or row.get('exception') is not None or row.get('driver_sha256')!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():
        raise ValueError('required current terminal producer failed: '+tag)
result=json.loads((P/'result-02.json').read_text())
control=json.loads((P/'controls-01/result.json').read_text())
if result.get('producer_complete') is not True or result['relative_to_331990_entry_rsp']['name_input_delta']!=48 or control['status']!='THREE_ACTUAL_PREREQUISITE_REFUSALS':
    raise ValueError('incomplete/zero scientific result')
if sha(P/'driver-preimages/prove-01.py')!='adfb220a3dad623af7d36f60d7f2638512988ea3653099b77ccaf745638be47b':
    raise ValueError('original producer preimage differs')
(P/'dependencies').mkdir()
for name in ['validate-title-source-annotations.py','prove_owner_reload_order.py','capture-index-path.py']:
    shutil.copyfile(W/name,P/'dependencies'/name)
shutil.copyfile(W/'ov42-gauge-callback-binding/prepare-handler-extents.py',P/'dependencies/prepare-handler-extents.py')
s=importlib.util.spec_from_file_location('reviewed_role_qualification',W/'validate-title-source-annotations.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for pin in result['source_pins']:
    path=P/pin['path']
    if sha(path)!=pin['sha256']:raise ValueError('prepared source-map identity changed')
    m.validate(json.loads(path.read_text()))
(P/'.gitattributes').write_bytes(b'* -text\n')
(P/'environment-01.json').write_text(json.dumps(dict(python=sys.version,executable_sha256=sha(Path(sys.executable)),platform=platform.platform()),indent=2))
destination=W/'sd194-caller-frames-frozen-ready';destination.mkdir();members=[]
for path in sorted([p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]):
    name=path.relative_to(P).as_posix();copied=destination/name;copied.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,copied)
    if copied.read_bytes()!=path.read_bytes():raise ValueError('copy differs')
    members.append(dict(path=name,bytes=path.stat().st_size,sha256=sha(path)))
shutil.copyfile(Path(__file__),destination/'freeze-sd194-caller-frames.py')
members.append(dict(path='freeze-sd194-caller-frames.py',bytes=Path(__file__).stat().st_size,sha256=sha(Path(__file__))))
(destination/'manifest.json').write_text(json.dumps(dict(package='sd194-caller-frames',members=members,
    limits='STATIC_ONLY normal-ABI relative stack addresses; no actual inherited bytes/field reachability/native effects; independent acceptance pending'),indent=2))
row=dict(folder=destination.name,members=len(members),manifest_sha256=sha(destination/'manifest.json'))
(W/'freeze-sd194-caller-frames-result.json').write_text(json.dumps(row,indent=2));print(json.dumps(row))
