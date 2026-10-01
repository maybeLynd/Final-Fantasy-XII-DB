import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];D=W/'run-01';assert not D.exists();D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 q=subprocess.run(['git',*args],cwd=ROOT,capture_output=True);assert q.returncode==0,q.stderr
 return q.stdout
commit=git('rev-parse','69bbf8c81').decode().strip();src=D/'source'
prior='037557884af3ed9b687b6bb8b2a34855c0703cdd';E=ROOT/'Database/FFXII TZA/_experiments/evidence/migration-my-progress-independent'
mb=(E/'manifest.json').read_bytes();assert git('show',prior+':'+(E/'manifest.json').relative_to(ROOT).as_posix())==mb
(D/'retained-manifest.json').write_bytes(mb);idx={m['path']:m for m in json.loads(mb)['members']}
def retained(rel):
 data=(E/rel).read_bytes();p=idx[rel];assert sha(data)==p['sha256'] and len(data)==p['bytes']
 assert git('show',prior+':'+(E/rel).relative_to(ROOT).as_posix())==data
 return data
raw={'method':'A exact published repository Python measure/check_progress via checked external probe CLI; labelled pre-resolved fixtures, not FF12/native/live',
 'commit':commit,'driver_sha256':sha(Path(__file__).read_bytes()),'probe_sha256':sha((W/'probe.py').read_bytes()),
 'python':sys.version,'base_executable':sys._base_executable,'base_executable_sha256':sha(Path(sys._base_executable).read_bytes()),
 'prior_commit':prior,'retained_manifest_sha256':sha(mb),'sources':{},'cases':[],'finished':False,
 'limits':'Synthetic pre-resolved MET/acceptanceOK gate not actual thirty audits or normal producer reachability; no deployed UI/fullM0M5/L1L2 claim'}
try:
 for rel in ('Database/Tools/dashboard/requirements.py','Database/Tools/dashboard/server.py','Database/Tools/analysis-kit/gfz-scripts/generation.py'):
  data=git('show',commit+':'+rel);p=src/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  raw['sources'][rel]={'sha256':sha(data),'bytes':len(data),'blob':git('rev-parse',commit+':'+rel).decode().strip()}
 tsv=D/'subsystems.tsv';tsv.write_bytes(retained('core-01/subsystems.tsv'));raw['subsystems_sha256']=sha(tsv.read_bytes())
 decls=[('zero-measure','measure','core-01/invalid-terminal-required0-input.json'),
        ('thirty-measure','measure','core-01/all-accepted-final30-input.json'),
        ('zero-ready-view','view','admission-01/invalid-terminal0/view-input.json'),
        ('thirty-ready-view','view','admission-01/valid-final30/view-input.json')]
 for name,kind,oldpath in decls:
  d=D/name;d.mkdir();inp=d/'input.json';data=retained(oldpath);inp.write_bytes(data)
  args=[sys._base_executable,'-B',str(W/'probe.py'),'--source',str(src),'--input',str(inp),'--kind',kind,'--subsystems',str(tsv)]
  q=subprocess.run(args,capture_output=True,text=True,timeout=10)
  parsed=None;parse_error=None
  try:parsed=json.loads(q.stdout)
  except json.JSONDecodeError as e:parse_error=str(e)
  c={'name':name,'kind':kind,'origin':oldpath,'input_sha256':sha(data),'args':args,'returncode':q.returncode,
     'stdout':q.stdout,'stderr':q.stderr,'parsed':parsed,'parse_error':parse_error,'terminal':True}
  (d/'receipt.json').write_text(json.dumps(c,indent=2)+'\n');raw['cases'].append(c)
  assert q.returncode==0 and not q.stderr and parse_error is None and parsed and 'result' in parsed and parsed['exception'] is None
  expected_modules={'requirements':src/'Database/Tools/dashboard/requirements.py','server':src/'Database/Tools/dashboard/server.py','generation':src/'Database/Tools/analysis-kit/gfz-scripts/generation.py'}
  assert parsed['modules']=={n:str(p.resolve()) for n,p in expected_modules.items()}
  result=parsed['result']
  if name=='zero-measure':assert result['ready'] is False and result['measured'] is False and 'T' in result['failed'] and result['terminal']=={'accepted':None,'required':30}
  elif name=='thirty-measure':assert result['ready'] is True and result['measured'] is True and result['terminal']=={'accepted':30,'required':30}
  elif name=='zero-ready-view':assert isinstance(result,str) and 'DATABASE READY claimed' in result
  else:assert result is None
  assert inp.read_bytes()==data
 for rel,p in raw['sources'].items():assert sha((src/rel).read_bytes())==p['sha256']
 raw['source_and_inputs_unchanged']=True;raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('MY_PROGRESS_R3_CHANGED_READER',[(c['name'],c['returncode']) for c in raw['cases']])
