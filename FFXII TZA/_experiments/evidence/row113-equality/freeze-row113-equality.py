"""Actual prerequisite map preflight before this immutable scientific delivery."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'row113-equality';F=W/'row113-equality-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('proof-01','prove.py'),('control-01','control.py')]:
 st=json.loads((P/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('required producer failed/incomplete '+tag)
controls=json.loads((P/'proof-controls-01/result.json').read_text())
if controls.get('complete') is not True or len(controls['cases'])!=3 or not all(c['passed'] for c in controls['cases']):raise RuntimeError('invalid/incomplete controls')
spec=importlib.util.spec_from_file_location('row113_actual_publisher',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
guard=pub.verify_packet_annotations(P,'result-01.json')
if guard['status']!='VERIFIED_PREREQUISITE' or len(guard['source_checks'])!=3:raise RuntimeError('publication source prerequisites incomplete')
pre=P/'publication-source-preflight-01.json'
if pre.exists():raise RuntimeError('immutable preflight exists')
pre.write_text(json.dumps({'actual_guard':guard,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py'),'scope':'Required actual annotation path before publication claim; not another semantic experiment/independent acceptance.'},indent=2)+'\n')
if F.exists():raise RuntimeError('immutable freeze exists')
shutil.copytree(P,F);(F/'.gitattributes').write_text('* -text\n');D=F/'dependencies';D.mkdir()
pins={'capture-index-path.py':'cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','validate-title-source-annotations.py':'7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','prove_owner_reload_order.py':'43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864'}
for n,pin in pins.items():
 if sha(W/n)!=pin:raise RuntimeError('shared dependency changed')
 shutil.copyfile(W/n,D/n)
shutil.copyfile(Path(__file__),F/'freeze-row113-equality.py')
members=[{'path':str(p.relative_to(F)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'row113-equality','method':'A source/bounded-width invariant','members':members,'limits':'Producer proof/control receipts not independent acceptance/natural type or stability proof.'},indent=2)+'\n');print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
