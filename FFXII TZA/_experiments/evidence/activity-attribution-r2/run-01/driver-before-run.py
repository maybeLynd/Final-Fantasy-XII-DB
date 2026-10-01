import hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();S=W/'source';S.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();C=subprocess.check_output(['git','rev-parse','0bec2215d'],text=True).strip();E=Path('Database/FFXII TZA/_experiments/evidence/migration-activity-deltas-independent');EC='00fd54fdaa52dd65191d0cbdd4419f8ce4f1f6af'
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0,q.stderr;return q.stdout
mbytes=(E/'manifest.json').read_bytes();assert git('show',EC+':'+(E/'manifest.json').as_posix())==mbytes;members={x['path']:x for x in json.loads(mbytes)['members']};raw={'method':'A original Python activity.compute on byte-identical retained synthetic boards/feed/clock, no teamwrites or live observation','source_commit':C,'prior_commit':EC,'prior_manifest_sha256':sha(mbytes),'driver_sha256':sha(Path(__file__).read_bytes()),'probe_sha256':sha((W/'probe.py').read_bytes()),'sources':{},'cases':[],'terminal':False,'exception':None,'python':{'version':sys.version,'base':sys._base_executable,'base_sha256':sha(Path(sys._base_executable).read_bytes())}}
(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
try:
 for name in ['activity.py','requirements.py']:
  path='Database/Tools/dashboard/'+name;b=git('show',C+':'+path);(S/name).write_bytes(b);raw['sources'][name]={'path':path,'sha256':sha(b),'blob':git('rev-parse',C+':'+path).decode().strip()}
 decls=[('old-claim-no-feed','UNKNOWN','claimed'),('foreign-review-no-feed','UNKNOWN','claimed'),('foreign-review-explicit-unknown','UNKNOWN','claimed'),('own-note-no-feed','recent','working'),('busy-control','active','working'),('idle-control','idle','claimed')]
 for name,live,kind in decls:
  rel='activity-02/'+name+'/input.json';b=(E/rel).read_bytes();assert sha(b)==members[rel]['sha256'] and git('show',EC+':'+(E/rel).as_posix())==b
  d=R/name;d.mkdir();f=d/'input.json';f.write_bytes(b);argv=[sys.executable,'-B',str(W/'probe.py'),str(f)];q=subprocess.run(argv,capture_output=True,text=True,timeout=5);assert q.returncode==0 and not q.stderr;z=json.loads(q.stdout);assert z['exception'] is None and z['result'] is not None
  opus=next(p for p in z['result']['by_agent'] if p['lane']=='OPUS');item=next(p for p in z['result']['categories'] if p['code']=='C');claim=next(p for p in opus['working'] if p['task']=='LABELLED-OPUS-OLD-CLAIM')
  assert opus['liveness']==live and claim['kind']==kind,(name,opus['liveness'],claim['kind'])
  assert ('OPUS' in item['working'])==(kind=='working')
  row={'name':name,'expected_liveness':live,'expected_kind':kind,'input_sha256':sha(b),'argv':argv,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True,'result':z,'observed_liveness':opus['liveness'],'observed_kind':claim['kind'],'combat_colored':item['working'],'input_unchanged':sha(f.read_bytes())==sha(b)};(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');raw['cases'].append(row)
 for name,z in raw['sources'].items():assert sha((S/name).read_bytes())==z['sha256']
 raw['verdict']='ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR'
except BaseException as e:raw['exception']={'type':type(e).__name__,'text':str(e)};raw['verdict']='INVALID'
finally:raw['terminal']=True;(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print(raw['verdict'],raw['exception']);sys.exit(1 if raw['exception'] else 0)
