"""Freeze exact source/controls with hash-bound inherited case inputs."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'ov21-page-selection-invariant';F=W/'ov21-page-selection-invariant-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('proof-02','prove.py'),('control-02','control.py')]:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('required actual success missing '+tag)
v=json.loads((P/'result-02.json').read_text());c=json.loads((P/'control-result-02.json').read_text())
if v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py') or c.get('producer_complete') is not True or c['driver_sha256']!=sha(P/'control.py') or c['count']!=4 or len(c['cases'])!=4 or not all(r['exit']!=0 and r['diagnostic_matched'] and r['refused_result_absent'] for r in c['cases']):raise RuntimeError('incomplete result/controls')
s=importlib.util.spec_from_file_location('pub',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub);g=pub.verify_packet_annotations(P,'result-02.json')
if g['status']!='VERIFIED_PREREQUISITE' or len(g['source_checks'])!=2:raise RuntimeError('actual source-map prerequisite failed')
pre=P/'publication-source-preflight-01.json'
if pre.exists() or F.exists():raise RuntimeError('immutable freeze exists')
pre.write_text(json.dumps({'actual_guard':g,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py')},indent=2)+'\n')
failed=json.loads((P/'control-01.status.json').read_text())
if failed['exit']!=1 or failed['driver_sha256']!=sha(P/'control-01-driver.py') or b'control not discriminating failed-retained-capture' not in(P/'control-01.stderr').read_bytes():raise RuntimeError('incomplete control history lost')
F.mkdir()
for q in P.iterdir():
 if q.name.startswith('controls-'):continue
 if q.is_dir():shutil.copytree(q,F/q.name)
 else:shutil.copy2(q,F/q.name)
for base in [P/'controls-01',P/'controls-02']:
 for case in base.iterdir():
  d=F/base.name/case.name;d.mkdir(parents=True);inputs=[]
  for f in sorted(case.rglob('*')):
   if not f.is_file():continue
   rel=f.relative_to(case);base=P/rel;row={'case_path':rel.as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}
   if base.is_file() and sha(base)==row['sha256']:
    row['inherited_base']=rel.as_posix()
   else:
    to=d/rel;to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,to);row['retained_overlay']=rel.as_posix()
   inputs.append(row)
  removed=['source-01.json'] if case.name=='missing-source' else []
  (d/'input-identities.json').write_text(json.dumps({'complete_case_file_set':True,'files':inputs,'explicit_removed_base_files':removed,'limits':'Unchanged inputs are exact hash-bound base files; no inference from absent output'},indent=2)+'\n')
  for row in inputs:
   q=(F/row['inherited_base']) if 'inherited_base' in row else d/row['retained_overlay'];assert q.is_file() and sha(q)==row['sha256'] and q.stat().st_size==row['bytes']
(F/'.gitattributes').write_text('* -text\n');shutil.copyfile(Path(__file__),F/Path(__file__).name)
members=[{'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'ov21-page-selection-invariant','method':'A STATIC_ONLY original page endpoints/search and conditional occupancy','members':members,'limits':'Page endpoints/zero-count acquisition/conditional source lemma; not a natural allwriter invariant'},indent=2)+'\n')
print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
