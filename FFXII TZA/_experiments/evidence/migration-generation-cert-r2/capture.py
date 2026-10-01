import copy,hashlib,importlib.util,json,shutil,subprocess,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'run-01';assert not D.exists(),'Preserve original run';D.mkdir()
rev=subprocess.check_output(['git','rev-parse','f145d442f'],text=True).strip();rel='Database/Tools/analysis-kit/gfz-scripts/generation.py'
src=D/'generation.py';src.write_bytes(subprocess.check_output(['git','show',rev+':'+rel]))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('original_generation_repaired',src);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
E=Path('Database/FFXII TZA/_experiments/evidence/migration-generation-independent');m=json.loads((E/'manifest.json').read_text())
shutil.copyfile(E/'manifest.json',D/'retained-manifest.json');shutil.copyfile(E/'run-01/raw.json',D/'retained-raw.json')
idx={x['path']:x for x in m['members']}
raw={'method':'A exact original published Python library + actual external CLI; private archive/folder fixtures, not FF12/native/live',
 'commit':rev,'source_sha256':sha(src),'source_blob':subprocess.check_output(['git','rev-parse',rev+':'+rel],text=True).strip(),
 'driver_sha256':sha(__file__),'python':sys.version,'retained_manifest_sha256':sha(D/'retained-manifest.json'),
 'cases':[],'owned_cli_processes':[],'finished':False,'child_limit':'Main verify-zip/status branches inspected: no child launch; --self-test branch excluded from actual args. No earlier transition cleanup claim.'}
def cli(args):
 cmd=[sys._base_executable,'-B',str(src),*map(str,args)]
 q=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
 r={'args':cmd,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True}
 raw['owned_cli_processes'].append(r);return r
def archive(name,path,origin):
 try:label,info=G.verify_zip(str(path));exc=None
 except BaseException as e:label=info=None;exc={'type':type(e).__name__,'reason':str(e)}
 q=cli(['verify-zip',path]);assert q['returncode'] in (0,1) and not q['stderr'],'Invalid CLI observer/traceback'
 assert exc is None and q['stdout'].startswith(label+' ') and q['returncode']==(0 if label=='VERIFIED' else 1)
 with zipfile.ZipFile(path) as z:entries=[{'name':i.filename,'sha256':hashlib.sha256(z.read(i)).hexdigest()} for i in z.infolist()]
 c={'name':name,'archive':path.name,'sha256':sha(path),'origin':origin,'entries':entries,'label':label,'info':info,'exception':exc,'cli':q};raw['cases'].append(c)
 return c
try:
 for name in ('positive','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip'):
  relp='run-01/export/'+name+'.zip';p=E/relp
  assert sha(p)==idx[relp]['sha256'] and p.stat().st_size==idx[relp]['bytes']
  dst=D/(name+'.zip');shutil.copyfile(p,dst)
  c=archive(name,dst,'Exact immutable97c4c1b65 archive bytes verified against original manifest; new reader execution')
  assert c['label']==('VERIFIED' if name=='positive' else 'UNVERIFIED')
 with zipfile.ZipFile(D/'positive.zip') as z:
  baseline=[(i.filename,z.read(i)) for i in z.infolist()];man=json.loads(z.read(G.MANIFEST))
 for name in ('array-manifest','wrong-output-shape','typed-input-state','unknown-input-state'):
  mm=copy.deepcopy(man);removed=set()
  if name=='array-manifest':mm=[]
  elif name=='wrong-output-shape':mm['outputs']=[]
  elif name=='typed-input-state':next(iter(mm['inputs'].values()))['state']=[]
  else:
   key=next(k for k,v in mm['inputs'].items() if v['state']=='present' and not v.get('external'))
   mm['inputs'][key]['state']='ASTRA_LABELLED_UNKNOWN_STATE';removed.add('inputs/'+key)
  p=D/(name+'.zip')
  with zipfile.ZipFile(p,'w') as z:
   for n,b in baseline:
    if n not in removed:z.writestr(n,json.dumps(mm).encode() if n==G.MANIFEST else b)
  (D/(name+'-manifest.json')).write_text(json.dumps(mm,indent=2)+'\n')
  c=archive(name,p,'Labelled manifest intervention on retained valid ZIP; '+('removed one now-unrecognized input snapshot' if removed else 'original member bytes except manifest'))
  if name!='unknown-input-state':assert c['label']=='UNVERIFIED'
 # Original private store clone, not the current production dashboard store.
 folder=D/'malformed-folder';shutil.copytree(E/'run-01/export/store',folder)
 st=G.Store(str(folder));ptr=json.loads((folder/G.CURRENT).read_text());gid=ptr['generation']
 manifest=folder/gid/G.MANIFEST;before=sha(manifest);manifest.write_bytes(b'{labelled invalid JSON')
 try:obj,path,probs=st.open_generation(gid);exc=None
 except BaseException as e:obj=path=probs=None;exc={'type':type(e).__name__,'reason':str(e)}
 q=cli(['status',folder]);assert exc is None and obj is None and any('not JSON' in x for x in probs)
 assert q['returncode']==1 and q['stdout'].startswith('INVALID ') and not q['stderr']
 raw['cases'].append({'name':'malformed-folder','generation':gid,'before_manifest_sha256':before,'after_manifest_sha256':sha(manifest),
  'object':obj,'problems':probs,'exception':exc,'cli':q,'intervention':'MalformedJSON private copied store manifest; original CURRENT pointer retained, hash mismatch also expected in CLI'})
 assert sha(src)==raw['source_sha256'] and not G.reader_stale();raw['source_restored']=True;raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'reason':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('GENERATION_CERT_R2_CHANGED_BOUNDARIES',[(x['name'],x.get('label')) for x in raw['cases']],flush=True)
