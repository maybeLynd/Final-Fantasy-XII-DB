"""Bounded immutable source/control freeze using existing publisher qualification."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'filecache-source-key-initialization';F=W/'filecache-source-key-initialization-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('prove-01','prove-before-nonzero-carrier-check-01.py'),('prove-02','prove.py'),('control-01','control.py')]:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('missing actual success '+tag)
v=json.loads((P/'result-02.json').read_text());c=json.loads((P/'control-result-01.json').read_text())
if v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py') or c.get('producer_complete') is not True or c['driver_sha256']!=sha(P/'control.py') or c['positive_producer_sha256']!=sha(P/'prove.py') or c['count']!=3 or len(c['cases'])!=3 or not all(r['terminal'] is True and r['exit']!=0 and r['exception'] is None and r['diagnostic_matched'] and r['refused_result_absent'] for r in c['cases']):raise RuntimeError('incomplete producer/controls')
s=importlib.util.spec_from_file_location('pub',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub);g=pub.verify_packet_annotations(P,'result-02.json')
if g['status']!='VERIFIED_PREREQUISITE' or len(g['source_checks'])!=1:raise RuntimeError('actual source prerequisite failed')
pre=P/'publication-source-preflight-01.json'
if pre.exists() or F.exists():raise RuntimeError('immutable freeze exists')
pre.write_text(json.dumps({'actual_guard':g,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py')},indent=2)+'\n');F.mkdir()
for q in P.iterdir():
 if q.name in ['controls-01','__pycache__']:continue
 if q.is_dir():shutil.copytree(q,F/q.name)
 else:shutil.copy2(q,F/q.name)
for case in (P/'controls-01').iterdir():
 d=F/'controls-01'/case.name;d.mkdir(parents=True);inputs=[]
 for f in sorted(case.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(case);base=P/rel;r={'case_path':rel.as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}
  if base.is_file() and sha(base)==r['sha256']:r['inherited_base']=rel.as_posix()
  else:
   to=d/rel;to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,to);r['retained_overlay']=rel.as_posix()
  inputs.append(r)
 removed=['source-01.json'] if case.name=='missing-source' else []
 (d/'input-identities.json').write_text(json.dumps({'complete_case_file_set':True,'files':inputs,'explicit_removed_base_files':removed},indent=2)+'\n')
 for r in inputs:
  q=F/r['inherited_base'] if 'inherited_base' in r else d/r['retained_overlay'];assert q.is_file() and sha(q)==r['sha256'] and q.stat().st_size==r['bytes']
(F/'.gitattributes').write_text('* -text\n');shutil.copyfile(Path(__file__),F/Path(__file__).name)
members=[{'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'filecache-source-key-initialization','members':members,'limits':'Conditional source initialization/local rebind retention, not live lifetime/allwriter/natural empty archive hit proof; independent acceptance pending'},indent=2)+'\n');print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
