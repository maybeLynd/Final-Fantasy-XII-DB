"""Re-review changed original source on retained histories, no new generation build.

Lessons: bind exact verifier text from its manifest before interpreting selectors;
record exit/result/exception before asserting; preserve sources and store bytes.
"""
import ast,hashlib,importlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir()
P=Path('Database/FFXII TZA/_experiments/evidence/delta-baseline-selection').resolve()
C='17d6cdc2915b22b1743cdd2e2c6acc2fcdf6f5e2';S=R/'source'
sha=lambda b:hashlib.sha256(b).hexdigest()
def put(p,b):p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b)
def js(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def git(*args):
 q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0 and not q.stderr
 return q.stdout
raw={'method':'A exact original repository selectors/change expression/annotator on copied retained verified Store histories',
 'source_commit':C,'driver_sha256':sha(Path(__file__).read_bytes()),'sources':{},'cases':[],
 'terminal':False,'exception':None,'verdict':'INCOMPLETE',
 'python':{'version':sys.version,'executable':sys.executable,'exe_sha256':sha(Path(sys.executable).read_bytes()),
 'base_executable':sys._base_executable,'base_sha256':sha(Path(sys._base_executable).read_bytes())}}
put(R/'capture.py',Path(__file__).read_bytes())
try:
 paths=['Database/Tools/dashboard/build_views.py','Database/Tools/dashboard/requirements.py',
 'Database/Tools/analysis-kit/gfz-scripts/generation.py','Database/Tools/dashboard/VIEW-SCHEMA.md',
 'Database/FFXII TZA/_index/workflow/MY-PROGRESS-METRICS.md']
 for p in paths:
  b=git('show',C+':'+p);put(S/p,b);cur=Path(p).read_bytes();put(R/'current-preimages'/p,cur)
  raw['sources'][p]={'sha256':sha(b),'blob':git('rev-parse',C+':'+p).decode().strip(),'current_sha256':sha(cur),'current_equal':cur==b}
 sys.path.insert(0,str(S/'Database/Tools/dashboard'));B=importlib.import_module('build_views');Q=importlib.import_module('requirements');G=B.G
 raw['loaded_paths']={n:m.__file__ for n,m in [('build_views',B),('requirements',Q),('generation',G)]}
 text=(S/paths[0]).read_text();tree=ast.parse(text);build=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_build')
 selected=[]
 for n in ast.walk(build):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('prior_generation','prior_progress','annotate_deltas'):
   selected.append({'name':n.func.id,'line':n.lineno,'args':[ast.unparse(a) for a in n.args]})
 raw['static_build_calls']=sorted(selected,key=lambda x:x['line'])
 assert [(x['name'],x['args']) for x in raw['static_build_calls']]==[('prior_generation',['st']),('prior_progress',['pman','pdir']),('annotate_deltas',['views','pdir','pman'])]
 qt=ast.parse((S/paths[1]).read_text());measure=next(n for n in qt.body if isinstance(n,ast.FunctionDef) and n.name=='measure')
 candidates=[]
 for n in ast.walk(measure):
  if isinstance(n,ast.Dict):
   candidates += [v for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='change']
 assert len(candidates)==1
 expr=candidates[0];raw['original_change_expression']={'ast_sha256':sha(ast.dump(expr,include_attributes=False).encode()),'source':ast.unparse(expr),'limit':'Exact extracted expression executed, not full measure/v_progress/_build.'}
 expression=compile(ast.Expression(expr),str(S/paths[1]),'eval')
 manifest=json.loads((P/'manifest.json').read_bytes());member={x['path']:x for x in manifest['members']}
 oldbytes=(P/'run-03/raw.json').read_bytes();assert sha(oldbytes)==member['run-03/raw.json']['sha256'];old=json.loads(oldbytes)
 put(R/'parent-raw.json',oldbytes);put(R/'parent-manifest.json',(P/'manifest.json').read_bytes())
 raw['parent']={'commit':'9e84de6209f585650fb242f3a40f3ed8dc3643cd','raw_sha256':sha(oldbytes),'manifest_sha256':sha((P/'manifest.json').read_bytes())}
 for name in ['empty-history','aligned-latest','latest-missing-progress']:
  prev=next(x for x in old['cases'] if x['name']==name);original=(P/'run-03'/prev['store_relative']).resolve();assert original.is_relative_to(P)
  copied=R/name/'store';copied.parent.mkdir();shutil.copytree(original,copied)
  before={f.relative_to(copied).as_posix():sha(f.read_bytes()) for f in copied.rglob('*') if f.is_file()}
  assert before==prev['store_hashes']
  for f in original.rglob('*'):
   if f.is_file():assert sha(f.read_bytes())==member[f.relative_to(P).as_posix()]['sha256']
  st=G.Store(str(copied));verifications=[]
  for gen in prev['generations']:
   m,d,probs=st.open_generation(gen['generation'],gen['manifest_sha256']);assert not probs and m['generation']==gen['generation']
   args=[sys.executable,'-B',str(S/paths[2]),'verify',str(copied)]
   q=subprocess.run(args,capture_output=True,text=True,timeout=10)
   receipt={'argv':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True}
   verifications.append(receipt)
   # CLI verifies CURRENT; for older admitted entries, open_generation above is the
   # distinct per-generation proof. Bind CLI output to the actual current manifest.
   cm,cd,cp=st.open_current();assert not cp
   expected='CURRENT %s committed %s; %d outputs; sources unchanged\n'%(cm['generation'],cm['committed_at'],len(cm['outputs']))
   assert q.returncode==0 and not q.stderr and q.stdout==expected,receipt
  pm,pd=B.prior_generation(st);pp=B.prior_progress(pm,pd)
  v={'progress':{'view':'progress','definition':Q.VERSION,'measures':[{'id':'union','numerator':40,'denominator':100,'scope':'labelled synthetic requirement population'}]}}
  B.annotate_deltas(v,pd,pm)
  change=eval(expression,Q.__dict__,{'prior':pp,'scopes':{'union':{'accepted':40,'total':100}},'cats':{}})
  row={'name':name,'store_hashes':before,'parent_store_relative':original.relative_to(P).as_posix(),
  'generations':prev['generations'],'verification_receipts':verifications,'general_prior':pm,'general_prior_dir':pd,
  'progress_prior':pp,'annotated':v['progress'],'change_expression_result':change,
  'store_unchanged':before=={f.relative_to(copied).as_posix():sha(f.read_bytes()) for f in copied.rglob('*') if f.is_file()}}
  raw['cases'].append(row)
  if name=='empty-history':assert pm is None and pp is None and change is None
  elif name=='aligned-latest':assert pp['generation']==pm['generation']==prev['generations'][-1]['generation'] and change['scopes']['union']['pct']==v['progress']['measures'][0]['delta']['pp']==10.0
  else:assert pp is None and change is None and pm['generation']==prev['generations'][-1]['generation'] and v['progress']['measures'][0]['delta']['na']=='no prior'
  assert row['store_unchanged']
 for p,z in raw['sources'].items():assert sha((S/p).read_bytes())==z['sha256']
 raw['verdict']='ACCEPT_SCOPED_ONE_PRIOR_BASIS_AT_RETAINED_HISTORY_BOUNDARY'
 raw['limits']='Copied synthetic histories; original selector/annotator and extracted original change expression only. Static actual build argument flow, not full measure/adapter/_build or deployment/browser/current database delta proof. Day-boundary wording owner debt remains.'
except BaseException as e:
 raw['exception']={'type':type(e).__name__,'message':str(e)};raw['verdict']='INVALID'
finally:
 raw['terminal']=True;put(R/'raw.json',js(raw));print(raw['verdict'],raw['exception']);sys.exit(1 if raw['exception'] else 0)
