"""Freeze exactly two validated, bounded packets; reuse existing source guard."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;slug=sys.argv[1]
configs={'filecache-open-sentinel':{'positive':'prove-01','sources':3,'cases':3,'success':[('capture-01','capture.py'),('prove-01','prove.py'),('control-01','control.py')]}}
if slug not in configs:raise RuntimeError('not a curated freeze target')
c=configs[slug];P=W/slug;F=W/(slug+'-frozen-ready');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if F.exists():raise RuntimeError('immutable freeze exists')
for tag,driver in c['success']:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('missing checked actual success '+tag)
v=json.loads((P/'result-01.json').read_text());control=json.loads((P/'control-result-01.json').read_text())
if v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py') or control.get('producer_complete') is not True or control['driver_sha256']!=sha(P/'control.py') or control['positive_producer_sha256']!=sha(P/'prove.py'):raise RuntimeError('incomplete producer/control binding')
cases=control['actual_CLI_refusals'] if slug.startswith('render-') else control['cases']
if len(cases)!=c['cases'] or not all(r['terminal'] is True and r['exit']!=0 and r['exception'] is None and r['diagnostic_matched'] and r['refused_result_absent'] for r in cases):raise RuntimeError('invalid/incomplete refusal cases')
if slug.startswith('render-') and (control['derive_count']!=5 or len(control['synthetic_derive_controls'])!=5 or not all(r['refused'] for r in control['synthetic_derive_controls'])):raise RuntimeError('missing focused derive controls')
if control['predicate_count']!=4 or len(control['predicate_controls'])!=4 or not all(r['refused'] for r in control['predicate_controls']):raise RuntimeError('missing focused predicate controls')
if slug=='filecache-zero-handle-return':
 s=json.loads((P/'prove-01.status.json').read_text())
 if s['terminal'] is not True or s['exit']!=1 or s['exception'] is not None or s['driver_sha256']!=sha(P/'prove-before-reachable-return-slice-01.py'):raise RuntimeError('historical failed invocation lost')
sp=importlib.util.spec_from_file_location('pub',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub)
guard=pub.verify_packet_annotations(P,'result-01.json')
if guard['status']!='VERIFIED_PREREQUISITE' or len(guard['source_checks'])!=c['sources']:raise RuntimeError('actual publication source prerequisite failed')
pre=P/'publication-source-preflight-01.json'
if pre.exists():raise RuntimeError('immutable preflight exists')
pre.write_text(json.dumps({'actual_guard':guard,'publisher_sha256':sha(W/'prepare-residue-packet-publication.py')},indent=2)+'\n');F.mkdir()
for q in P.iterdir():
 if q.name in ['controls-01','__pycache__']:continue
 if q.is_dir():shutil.copytree(q,F/q.name)
 else:shutil.copy2(q,F/q.name)
basefiles={q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file() and 'controls-01' not in q.relative_to(P).parts and '__pycache__' not in q.relative_to(P).parts and not q.name.startswith('control-') and q.name not in ['result-01.json','publication-source-preflight-01.json']}
for case in (P/'controls-01').iterdir():
 d=F/'controls-01'/case.name;d.mkdir(parents=True);inputs=[]
 casefiles={f.relative_to(case).as_posix() for f in case.rglob('*') if f.is_file()}
 for f in sorted(case.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(case);base=P/rel;r={'case_path':rel.as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}
  if base.is_file() and sha(base)==r['sha256']:r['inherited_base']=rel.as_posix()
  else:
   target=d/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target);r['retained_overlay']=rel.as_posix()
  inputs.append(r)
 removed=sorted(basefiles-casefiles)
 (d/'input-identities.json').write_text(json.dumps({'complete_case_file_set':True,'files':inputs,'explicit_removed_base_files':removed},indent=2)+'\n')
 for r in inputs:
  q=F/r['inherited_base'] if 'inherited_base' in r else d/r['retained_overlay']
  if not q.is_file() or sha(q)!=r['sha256'] or q.stat().st_size!=r['bytes']:raise RuntimeError('incomplete deduplicated case')
(F/'.gitattributes').write_text('* -text\n');shutil.copyfile(Path(__file__),F/Path(__file__).name)
members=[{'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':slug,'members':members,'limits':'Conditional retained/original source facts, no native/live/scheduling/lifetime closure; new independent review and actual canonical consumption required'},indent=2)+'\n')
print(json.dumps({'package':slug,'members':len(members),'manifest_sha256':sha(F/'manifest.json'),'source_guard':'VERIFIED_PREREQUISITE'}))
