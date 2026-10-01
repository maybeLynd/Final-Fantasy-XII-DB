"""Seal targeted source records; preserve invalid controller history additively."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'presentation-index-domain';F=W/'presentation-index-domain-frozen-ready'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('proof-01','prove.py'),('control-03','control.py')]:
 st=json.loads((P/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('failed/incomplete required '+tag)
v=json.loads((P/'result-01.json').read_text());controls=json.loads((P/'proof-controls-02/result.json').read_text())
if v.get('producer_complete') is not True or len(v['equal_branch']['cases'])!=256 or controls.get('complete') is not True or len(controls['cases'])!=4 or not all(r['passed'] for r in controls['cases']):raise RuntimeError('incomplete scoped proof/control')
if F.exists():raise RuntimeError('immutable freeze already exists')
shutil.copytree(P,F)
(F/'.gitattributes').write_text('* -text\n')
D=F/'dependencies';D.mkdir()
pins={'capture-index-path.py':'cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','validate-title-source-annotations.py':'7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','prove_owner_reload_order.py':'43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864'}
for name,pin in pins.items():
 if sha(W/name)!=pin:raise RuntimeError('shared dependency changed '+name)
 shutil.copyfile(W/name,D/name)
shutil.copyfile(Path(__file__),F/'freeze-presentation-index-domain.py')
members=[{'path':str(p.relative_to(F)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
manifest={'package':'presentation-index-domain','method':'A STATIC_ONLY source/address proof','members':members,'limits':'Immutable inputs/drivers/positive/counter-controls; producer proof not independent acceptance or natural reachability.'}
(F/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json'),'frozen':str(F)}))
