import ast,copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();H=R/'source/Database/Tools/analysis-kit/gfz-scripts';H.mkdir(parents=True);sha=lambda b:hashlib.sha256(b).hexdigest();C='f21fe80440fc9d24df09fc19172753394fe61773';OLD=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-r2');OC='117f85ab6889eb7915d01e2a8f7596e762bbf25f'
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0,q.stderr;return q.stdout
manifest=(OLD/'manifest.json').read_bytes();assert git('show',OC+':'+(OLD/'manifest.json').as_posix())==manifest
member=next(x for x in json.loads(manifest)['members'] if x['path']=='run-01/valid-accept/TEAM.json');base=(OLD/member['path']).read_bytes();assert sha(base)==member['sha256'] and git('show',OC+':'+(OLD/member['path']).as_posix())==base
(R/'prior-valid-input.json').write_bytes(base);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
r={'method':'A original repository Python CLI/plan, synthetic private JSON variants; not FF12 or applied board writes','source_commit':C,'prior_commit':OC,'prior_manifest_sha256':sha(manifest),'prior_input_sha256':sha(base),'driver_sha256':sha(Path(__file__).read_bytes()),'python':dict(version=sys.version,path=sys.executable,base=sys._base_executable,base_sha256=sha(Path(sys._base_executable).read_bytes())),'sources':{},'cases':[],'terminal':False,'exception':None}
for name in ['transitions.py','team.py']:
 path='Database/Tools/analysis-kit/gfz-scripts/'+name;b=git('show',C+':'+path);(H/name).write_bytes(b);r['sources'][name]={'path':path,'sha256':sha(b),'blob':git('rev-parse',C+':'+path).decode().strip(),'current_sha256':sha(Path(path).read_bytes())}
def selected(s):
 out={}
 for n in ast.parse(s).body:
  if isinstance(n,(ast.FunctionDef,ast.Assign)):
   key=n.name if isinstance(n,ast.FunctionDef) else (n.targets[0].id if isinstance(n.targets[0],ast.Name) else '')
   if key in ['VERDICT','SHA','link_problem','plan','_op']:out[key]=ast.dump(n,include_attributes=False)
 return out
r['selected_current_admission_ast_equal']=selected((H/'transitions.py').read_text())==selected(Path(r['sources']['transitions.py']['path']).read_text());assert r['selected_current_admission_ast_equal']
sys.path.insert(0,str(H));sp=importlib.util.spec_from_file_location('original_transitions',H/'transitions.py');T=importlib.util.module_from_spec(sp);sp.loader.exec_module(T);assert Path(T.team.__file__).resolve()==(H/'team.py').resolve();r['module_paths']={'transitions':T.__file__,'team':T.team.__file__}
b=json.loads(base);assert len(b['tasks'])==1 and b['tasks'][0]['status']=='DONE';b['tasks'][0]['reviews']['commit']=C;assert b['tasks'][0]['result_refs']==['verdict:ACCEPT','fixture:review-record']
variants=[('valid-full40',None),('commit-full40-lf','commit_lf'),('commit-full40-crlf','commit_crlf'),('verdict-lf','verdict_lf')]
try:
 for name,change in variants:
  x=copy.deepcopy(b)
  if change=='commit_lf':x['tasks'][0]['reviews']['commit']+='\n'
  if change=='commit_crlf':x['tasks'][0]['reviews']['commit']+='\r\n'
  if change=='verdict_lf':x['tasks'][0]['result_refs'][0]+='\n'
  T.team.validate(x);f=R/(name+'.json');data=(json.dumps(x,indent=2)+'\n').encode();f.write_bytes(data)
  args=[sys._base_executable,'-B',str(H/'transitions.py'),'--board',str(f),'--json'];assert '--apply' not in args;q=subprocess.run(args,capture_output=True,text=True,timeout=5)
  assert q.returncode==0 and not q.stderr and sha(f.read_bytes())==sha(data);rows=json.loads(q.stdout);assert len(rows)==1
  plans=T.plan(copy.deepcopy(x));assert len(plans)==1
  z={'name':name,'input_sha256':sha(data),'argv':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True,'report':rows,'original_plan':plans,'board_unchanged':True,'writer_invoked':False};r['cases'].append(z);(R/(name+'-receipt.json')).write_text(json.dumps(z,indent=2)+'\n')
 for name,z in r['sources'].items():assert sha((H/name).read_bytes())==z['sha256']
except BaseException as e:
 r['exception']={'type':type(e).__name__,'text':str(e)};raise
finally:
 r['terminal']=True;(R/'raw.json').write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURE_COMPLETE',[(x['name'],x['report'][0]['transition']) for x in r['cases']])
