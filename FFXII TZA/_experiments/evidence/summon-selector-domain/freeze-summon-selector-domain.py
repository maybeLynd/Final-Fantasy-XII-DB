"""Seal the corrected actual CLI path and source-domain evidence."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'summon-selector-domain';F=W/'summon-selector-domain-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('proof-02','prove.py'),('control-02','control.py')]:
 st=json.loads((P/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('failed/incomplete '+tag)
v=json.loads((P/'result-02.json').read_text());c=json.loads((P/'proof-controls-01/result.json').read_text());source=json.loads((P/'source-01.json').read_text())
if v.get('producer_complete') is not True or len(v['slot3_stores'])!=3 or len(v['byte_partition'])!=256 or len(v['graphs'])!=4 or c.get('complete') is not True or len(c['cases'])!=3 or not all(r['passed'] for r in c['cases']):raise RuntimeError('incomplete proof/control')
if v['driver_sha256']!=sha(P/'prove.py') or source['driver_sha256']!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':raise RuntimeError('source/proof driver identity changed')
# Concrete output-path regression: the corrected actual CLI ran from repository
# root with a filename argument, and produced only the expected package output.
root=next(p for p in W.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
if (root/'result-02.json').exists():raise RuntimeError('output path regression: root result exists')
status=json.loads((P/'proof-02.status.json').read_text())
if status['argv'][-1]!='result-02.json' or not(P/'proof-02-output-path-regression.json').exists():
 receipt=P/'proof-02-output-path-regression.json'
 if receipt.exists():raise RuntimeError('regression receipt already exists')
 if status['argv'][-1]!='result-02.json':raise RuntimeError('actual output-path control missing')
 receipt.write_text(json.dumps({'actual_cli_status_sha256':sha(P/'proof-02.status.json'),'argv':status['argv'],'expected_package_result_sha256':sha(P/'result-02.json'),'root_result_absent':True,'producer_sha256':sha(P/'prove.py'),'scope':'Actual relative filename invocation; no generic filesystem or game proof.'},indent=2)+'\n')
spec=importlib.util.spec_from_file_location('summon_selector_actual_publication',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub);g=pub.verify_packet_annotations(P,'result-02.json')
if g['status']!='VERIFIED_PREREQUISITE' or len(g['source_checks'])!=1:raise RuntimeError('source map admission incomplete')
pre=P/'publication-source-preflight-01.json'
if pre.exists() or F.exists():raise RuntimeError('immutable output exists')
pre.write_text(json.dumps({'actual_guard':g,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py'),'scope':'Actual required source admission only, not independent semantics.'},indent=2)+'\n')
shutil.copytree(P,F);(F/'.gitattributes').write_text('* -text\n');D=F/'dependencies';D.mkdir()
pins={'capture-index-path.py':'cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','validate-title-source-annotations.py':'7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','prove_owner_reload_order.py':'43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864'}
for n,pin in pins.items():
 if sha(W/n)!=pin:raise RuntimeError('shared dependency changed')
 shutil.copyfile(W/n,D/n)
shutil.copyfile(Path(__file__),F/'freeze-summon-selector-domain.py')
members=[{'path':str(p.relative_to(F)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'summon-selector-domain','method':'A original producer/map domain','members':members,'limits':'Local source domain only; actor application, authored reachability and independent acceptance remain open.'},indent=2)+'\n');print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
