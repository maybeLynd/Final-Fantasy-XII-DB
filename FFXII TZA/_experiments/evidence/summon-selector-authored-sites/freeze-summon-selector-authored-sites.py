"""Seal the explicit partial-prefix/completed-suffix composite, not a green rerun."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'summon-selector-authored-sites';F=W/'summon-selector-authored-sites-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('resume-01','resume.py'),('reduce-01','reduce.py'),('control-01','control.py')]:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('required actual success missing '+tag)
v=json.loads((P/'result-01.json').read_text());c=json.loads((P/'controls-01/result.json').read_text())
if v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'reduce.py') or v['entry_count']!=10045 or v['literal_target_calls']!=0 or c.get('complete') is not True or len(c['cases'])!=3 or not all(r['passed'] for r in c['cases']):raise RuntimeError('incomplete/scoped result or controls')
s=importlib.util.spec_from_file_location('authored_sites_actual_pub',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub);g=pub.verify_packet_annotations(P,'result-01.json')
if g['status']!='VERIFIED_PREREQUISITE' or len(g['source_checks'])!=1:raise RuntimeError('native source-map admission failed')
pre=P/'publication-source-preflight-01.json'
if pre.exists() or F.exists():raise RuntimeError('immutable frozen output exists')
pre.write_text(json.dumps({'actual_guard':g,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py'),'limits':'Native source lineage/annotation only; original resource collection independently qualified by reducer.'},indent=2)+'\n')
shutil.copytree(P,F);(F/'.gitattributes').write_text('* -text\n');D=F/'dependencies';D.mkdir()
n='validate-title-source-annotations.py'
if sha(W/n)!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':raise RuntimeError('source validator changed')
shutil.copyfile(W/n,D/n);shutil.copyfile(Path(__file__),F/'freeze-summon-selector-authored-sites.py')
members=[{'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'summon-selector-authored-sites','method':'A scoped original-resource composite','members':members,'limits':'No literal3044 in covered source spans/whole suffix/gaps, not universal nativeunreachability or actor type/parity; firstfullbatch invalid preserved.'},indent=2)+'\n');print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
