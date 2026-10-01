import hashlib,importlib.util,json,shutil,subprocess,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];D=W/'run-01';assert not D.exists();D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 q=subprocess.run(['git',*args],cwd=ROOT,capture_output=True);assert q.returncode==0,q.stderr
 return q.stdout
rev=git('rev-parse','b6e6de3f0').decode().strip();rel='Database/Tools/analysis-kit/gfz-scripts/generation.py'
src=D/'generation.py';src.write_bytes(git('show',rev+':'+rel))
E=ROOT/'Database/FFXII TZA/_experiments/evidence/migration-generation-cert-r2'
manifest=(E/'manifest.json').read_bytes();prior_commit='7d9b5ec17091dcb16cb33c6c302d3f5e5012b16d'
assert git('show',prior_commit+':'+(E/'manifest.json').relative_to(ROOT).as_posix())==manifest
(D/'retained-manifest.json').write_bytes(manifest);idx={x['path']:x for x in json.loads(manifest)['members']}
data=(E/'run-01/raw.json').read_bytes();assert sha(data)==idx['run-01/raw.json']['sha256']
(D/'retained-raw.json').write_bytes(data)
raw={'method':'A exact published original repository Python library/CLI; immutable archive reuse; no FF12/native/live',
 'commit':rev,'source_sha256':sha(src.read_bytes()),'source_blob':git('rev-parse',rev+':'+rel).decode().strip(),
 'driver_sha256':sha(Path(__file__).read_bytes()),'python':sys.version,'base_executable':sys._base_executable,
 'base_executable_sha256':sha(Path(sys._base_executable).read_bytes()),'prior_commit':prior_commit,
 'retained_manifest_sha256':sha(manifest),'retained_raw_sha256':sha(data),'cases':[],'finished':False,
 'limits':'No normal Store emission/deployed reader/whole-manifest authentication/completeM1 or fullL1L2; no original game instructions; old outcomes not fresh test credit'}
try:
 spec=importlib.util.spec_from_file_location('published_generation_r3',src);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
 for name in ('positive','unknown-input-state','duplicate-zip-member'):
  relp='run-01/'+name+'.zip';data=(E/relp).read_bytes();pin=idx[relp]
  assert len(data)==pin['bytes'] and sha(data)==pin['sha256']
  assert git('show',prior_commit+':'+(E/relp).relative_to(ROOT).as_posix())==data
  path=D/(name+'.zip');path.write_bytes(data)
  try:label,info=G.verify_zip(str(path));exc=None
  except BaseException as e:label=info=None;exc={'type':type(e).__name__,'detail':str(e)}
  args=[sys._base_executable,'-B',str(src),'verify-zip',str(path)]
  q=subprocess.run(args,capture_output=True,text=True,timeout=10)
  with zipfile.ZipFile(path) as z:entries=[{'name':x.filename,'sha256':sha(z.read(x))} for x in z.infolist()]
  c={'name':name,'origin':'Byte-identical 7d9b5ec17 archive; changed-reader execution','sha256':sha(data),'bytes':len(data),
     'label':label,'info':info,'exception':exc,'entries':entries,'cli':{'args':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True}}
  (D/(name+'-receipt.json')).write_text(json.dumps(c,indent=2)+'\n');raw['cases'].append(c)
  expected='VERIFIED' if name=='positive' else 'UNVERIFIED'
  assert exc is None and label==expected and q.returncode==(0 if name=='positive' else 1) and not q.stderr and q.stdout.startswith(expected+' ')
  if name=='unknown-input-state':assert 'unknown state' in info['reason'] and 'ASTRA_LABELLED_UNKNOWN_STATE' in info['reason']
  if name=='duplicate-zip-member':assert 'duplicate member names' in info['reason']
 assert sha(src.read_bytes())==raw['source_sha256'] and not G.reader_stale();raw['source_unchanged']=True;raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('GENERATION_R3_CHANGED_READER',[(x['name'],x['label'],x['cli']['returncode']) for x in raw['cases']])
