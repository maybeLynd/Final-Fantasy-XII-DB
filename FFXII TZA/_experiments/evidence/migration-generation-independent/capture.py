import contextlib, hashlib, importlib.util, io, json, os, subprocess, sys, time, warnings, zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists(),'Preserve original run'
R.mkdir();rel='Database/Tools/analysis-kit/gfz-scripts/generation.py'
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
data=subprocess.check_output(['git','show',commit+':'+rel]);src=R/'generation.py';src.write_bytes(data)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('original_generation',src)
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
old=Path('Database/FFXII TZA/_experiments/evidence/migration-dashboard-incident')
retained_source=old/'run-01/source'/rel
assert data==retained_source.read_bytes()
prior=json.loads((old/'run-01/raw.json').read_text())
reuse={'missing-output-failed-build-preserves-current','strict-input-mid-build-rejected','volatile-change-coherent-commit','warm-output-tamper-rejected','snapshot-tamper-no-fallback'}
retained=[c for c in prior['cases'] if c['name'] in reuse]
assert len(retained)==len(reuse) and all(c['passed'] for c in retained)
raw={'method':'A original Python tooling/labelled private fixtures; not FF12 original-code or live',
 'source_tree_commit':commit,'source_last_commit':subprocess.check_output(['git','log','-1','--format=%H',commit,'--',rel],text=True).strip(),
 'source_path':rel,'source_sha256':sha(src),'source_blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip(),
 'driver_sha256':sha(__file__),'worker_sha256':sha(W/'interrupt-worker.py'),'python':sys.version,'executable':sys._base_executable,
 'retained':{'commit':'51660c616f8fec23c7ae140a721be58cc54c38cc','raw_sha256':sha(old/'run-01/raw.json'),'source_sha256':sha(retained_source),'cases':retained},
 'cases':[],'owned_process_cleanup':[],'finished':False}
(R/'retained-raw.json').write_bytes((old/'run-01/raw.json').read_bytes())
base=str(Path(sys._base_executable))
def cli(*args):
 q=subprocess.run([base,'-B',str(src),*map(str,args)],capture_output=True,text=True,timeout=10)
 return {'args':q.args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True}
def fixture(name):
 d=R/name;d.mkdir();(d/'input').write_bytes(b'[]');s=G.Store(str(d/'store'))
 gid=build(s,d,'OLD');return d,s,gid
def build(s,d,mark):
 b=s.begin({'data':{'path':str(d/'input')}})
 Path(b.output_path('view.json')).write_text(json.dumps({'sentinel':mark}))
 return s.commit(b,['view.json'],validated={'data':None})
def record(name,obs):raw['cases'].append({'name':name,'observed':obs})
try:
 for name,mode in (('required-missing','missing'),('default-empty','empty'),('schema-allowed-empty','allowed'),('schema-malformed-nonempty','malformed')):
  d,s,gid=fixture(name);pointer=(Path(s.root)/G.CURRENT).read_bytes();hist=(Path(s.root)/G.HISTORY).read_bytes()
  if mode=='missing':(d/'input').unlink()
  elif mode in ('empty','allowed'):(d/'input').write_bytes(b'')
  else:(d/'input').write_bytes(b'{broken')
  observed_state=G.input_state(str(d/'input'));error=None;schema_error=None;new=None
  if mode=='malformed':
   try:json.loads((d/'input').read_bytes())
   except json.JSONDecodeError as e:schema_error=type(e).__name__+': '+str(e)
   assert schema_error
  try:
   b=s.begin({'data':{'path':str(d/'input'),'allow_empty':mode=='allowed'}})
   Path(b.output_path('view.json')).write_text('{"sentinel":"CANDIDATE"}')
   new=s.commit(b,['view.json'],validated={'data':schema_error})
  except Exception as e:error={'type':type(e).__name__,'reason':str(e)}
  record(name,{'state':observed_state,'schema_error':schema_error,'error':error,'old':gid,'new':new,
   'pointer_unchanged':(Path(s.root)/G.CURRENT).read_bytes()==pointer,'history_unchanged':(Path(s.root)/G.HISTORY).read_bytes()==hist,
   'failure':json.loads((Path(s.root)/G.FAILURE).read_text()) if (Path(s.root)/G.FAILURE).exists() else None,'cli':cli('status',s.root)})
 for stage in ('before-rename','after-rename'):
  d,s,gid=fixture('interrupt-'+stage);pointer=(Path(s.root)/G.CURRENT).read_bytes();hist=(Path(s.root)/G.HISTORY).read_bytes();gate=d/'gate.json'
  args=[base,'-B',str(W/'interrupt-worker.py'),str(src),str(d),stage,str(gate)]
  child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
  receipt={'pid':child.pid,'args':args,'gate':None,'terminal':False,'limit_seconds':10}
  raw['owned_process_cleanup'].append(receipt)
  try:
   until=time.monotonic()+10
   while not gate.exists() and child.poll() is None and time.monotonic()<until:time.sleep(.05)
   assert gate.exists(),'Missing discriminating timing gate; no semantic result'
   receipt['gate']=json.loads(gate.read_text());assert receipt['gate']['pid']==child.pid and child.poll() is None
   g=receipt['gate'];partial=Path(g['src']).exists();final=Path(g['dst']).exists()
   child.terminate();out,err=child.communicate(timeout=5)
   receipt.update(returncode=child.returncode,stdout=out,stderr=err,terminal=True,
    no_child_launch='Inspected immutable worker and generation import paths: worker launches no process; --self-test not called')
   record('interrupt-'+stage,{'old':gid,'gate':g,'partial_at_gate':partial,'final_at_gate':final,
    'pointer_unchanged':(Path(s.root)/G.CURRENT).read_bytes()==pointer,'history_unchanged':(Path(s.root)/G.HISTORY).read_bytes()==hist,
    'cli':cli('verify',s.root),'owned_pid':child.pid})
  finally:
   if child.poll() is None:child.kill();out,err=child.communicate(timeout=5);receipt.update(returncode=child.returncode,stdout=out,stderr=err,terminal=True,forced_cleanup=True)
 d,s,gid=fixture('export');positive={'status':cli('status',s.root),'verify':cli('verify',s.root),'export':cli('export',s.root,d/'positive.zip'),'zip':cli('verify-zip',d/'positive.zip')}
 record('cli-positive-export',dict(old=gid,cli=positive))
 # Explicit timing intervention around the unchanged dispatcher/export functions.
 original=G.zipfile.ZipFile.write;event=[]
 def refresh_write(z,filename,arcname=None,*a,**k):
  result=original(z,filename,arcname,*a,**k)
  if not event:
   (d/'input').write_bytes(b'[1]');new=build(s,d,'NEW');event.append({'after_member':arcname,'new_current':new})
  return result
 G.zipfile.ZipFile.write=refresh_write;out=io.StringIO();err=io.StringIO()
 try:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):rc=G.main(['generation.py','export',s.root,str(d/'refresh.zip')])
 finally:G.zipfile.ZipFile.write=original
 with zipfile.ZipFile(d/'refresh.zip') as z:exported=json.loads(z.read(G.MANIFEST));view=json.loads(z.read('outputs/view.json'))
 record('refresh-during-export',{'entry':'original main export with explicit ZipFile.write callback intervention','returncode':rc,'stdout':out.getvalue(),'stderr':err.getvalue(),'event':event,'old':gid,'current':s.current_id(),'export_generation':exported['generation'],'view':view,'cli':cli('verify-zip',d/'refresh.zip')})
 with zipfile.ZipFile(d/'positive.zip') as z:members={n:z.read(n) for n in z.namelist()}
 for name in ('mixed-zip','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip'):
  path=d/(name+'.zip');changed=dict(members)
  if name=='mixed-zip':changed['outputs/view.json']=b'{"sentinel":"NEW"}'
  elif name=='unknown-format-zip':m=json.loads(changed[G.MANIFEST]);m['format']='ff12-generation-unknown';changed[G.MANIFEST]=json.dumps(m).encode()
  elif name=='malformed-manifest-zip':changed[G.MANIFEST]=b'{broken'
  with warnings.catch_warnings(record=True) as warns:
   warnings.simplefilter('always')
   with zipfile.ZipFile(path,'w') as z:
    if name=='duplicate-zip-member':z.writestr('outputs/view.json',b'{"sentinel":"HIDDEN_DIFFERENT_FIRST_MEMBER"}')
    for n,b in changed.items():z.writestr(n,b)
  label=None;info=None;exc=None
  try:label,info=G.verify_zip(str(path))
  except Exception as e:exc={'type':type(e).__name__,'reason':str(e)}
  with zipfile.ZipFile(path) as z:names=z.namelist();entries=[{'name':i.filename,'sha256':hashlib.sha256(z.read(i)).hexdigest()} for i in z.infolist()]
  record(name,{'archive':path.name,'sha256':sha(path),'member_names':names,'entries':entries,'warnings':[str(w.message) for w in warns],
   'label':label,'info':info,'exception':exc,'cli':cli('verify-zip',path)})
 d,s,gid=fixture('added-output-membership');(Path(s.root)/gid/'outputs/uncited.json').write_text('{}')
 man,gen,probs=s.open_current();record('added-output-membership',{'problems':probs,'cli':cli('verify',s.root)})
 assert sha(src)==raw['source_sha256'];raw['source_restored']=True;raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'reason':str(e)};raise
finally:(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('GENERATION_BOUNDARIES_CAPTURE_FINISHED',len(raw['cases']),flush=True)
