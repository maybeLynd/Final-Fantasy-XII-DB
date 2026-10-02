"""Immutable bounded source/case freeze, existing publisher guard reused."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'filecache-route2-commit-key';F=W/'filecache-route2-commit-key-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,driver in [('capture-01','capture.py'),('prove-02','prove-before-publication-map-02.py'),('control-01','control.py'),('prove-03','prove.py'),('publication-control-01','control-publication-map.py')]:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('required actual success missing '+tag)
old=json.loads((P/'result-01.json').read_text());v=json.loads((P/'result-02.json').read_text());c=json.loads((P/'control-result-01.json').read_text());m=json.loads((P/'publication-control-result-01.json').read_text())
if old.get('producer_complete') is not True or old['driver_sha256']!=sha(P/'prove-before-publication-map-02.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('incomplete final/historical producer')
if c.get('producer_complete') is not True or c['driver_sha256']!=sha(P/'control.py') or c['positive_producer_sha256']!=old['driver_sha256'] or c['count']!=6 or len(c['cases'])!=6 or not all(r['terminal'] is True and r['exit']!=0 and r['exception'] is None and r['diagnostic_matched'] and r['refused_result_absent'] for r in c['cases']):raise RuntimeError('incomplete historical controls')
if m.get('producer_complete') is not True or m['driver_sha256']!=sha(P/'control-publication-map.py') or m['count']!=2 or len(m['cases'])!=2 or not m['scientific_ast_unchanged_except_source_map'] or not all(r['diagnostic_matched'] for r in m['cases']):raise RuntimeError('incomplete current publication controls')
s=importlib.util.spec_from_file_location('pub',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub);g=pub.verify_packet_annotations(P,'result-02.json')
if g['status']!='VERIFIED_PREREQUISITE' or len(g['source_checks'])!=3:raise RuntimeError('actual source-map guard failed')
pre=P/'publication-source-preflight-01.json'
if pre.exists() or F.exists():raise RuntimeError('immutable freeze exists')
pre.write_text(json.dumps({'actual_guard':g,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py')},indent=2)+'\n')
F.mkdir()
for q in P.iterdir():
 if q.name in ['controls-01','publication-controls-01','__pycache__']:continue
 if q.is_dir():shutil.copytree(q,F/q.name)
 else:shutil.copy2(q,F/q.name)
for name in ['controls-01','publication-controls-01']:
 for case in (P/name).iterdir():
  d=F/name/case.name;d.mkdir(parents=True);inputs=[]
  for f in sorted(case.rglob('*')):
   if not f.is_file():continue
   rel=f.relative_to(case);base_file=P/rel;row={'case_path':rel.as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}
   if base_file.is_file() and sha(base_file)==row['sha256']:row['inherited_base']=rel.as_posix()
   else:
    to=d/rel;to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,to);row['retained_overlay']=rel.as_posix()
   inputs.append(row)
  removed=['retained/filecache-key-boundaries-source-02.json'] if case.name=='missing-retained-wrapper' else []
  (d/'input-identities.json').write_text(json.dumps({'complete_case_file_set':True,'files':inputs,'explicit_removed_base_files':removed,'limits':'Exact case file set; unchanged case producer code resolves to archived metadata producer if necessary, not the current final driver.'},indent=2)+'\n')
  for r in inputs:
   q=F/r['inherited_base'] if 'inherited_base' in r else d/r['retained_overlay'];assert q.is_file() and sha(q)==r['sha256'] and q.stat().st_size==r['bytes']
(F/'.gitattributes').write_text('* -text\n');shutil.copyfile(Path(__file__),F/Path(__file__).name)
members=[{'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'filecache-route2-commit-key','method':'A STATIC_ONLY original caller/out-key provenance','members':members,'limits':'Conditional original caller and empty out-parameter rule; no natural empty archive hit/highbit key/lifetime proof; independent review/consumption pending'},indent=2)+'\n')
print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json')}))
