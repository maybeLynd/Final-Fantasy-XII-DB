import ast,copy,hashlib,importlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();S=R/'source';sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):
 q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(args,q.stderr);return q.stdout
C=git('rev-parse','HEAD').decode().strip();raw=dict(method='A original repository Python on labelled private verified Store histories; synthetic function composition, not full builder/deployment/game',source_commit=C,driver_sha256=sha(Path(__file__).read_bytes()),sources={},cases=[],terminal=False,exception=None,python=dict(version=sys.version,base=sys._base_executable,base_sha256=sha(Path(sys._base_executable).read_bytes())))
(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
try:
 for p in ['Database/Tools/dashboard/build_views.py','Database/Tools/dashboard/requirements.py','Database/Tools/analysis-kit/gfz-scripts/generation.py','Database/Tools/dashboard/VIEW-SCHEMA.md','Database/FFXII TZA/_index/workflow/MY-PROGRESS-METRICS.md']:
  b=git('show',C+':'+p);f=S/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);current=Path(p).read_bytes();pre=R/'current-preimages'/p;pre.parent.mkdir(parents=True,exist_ok=True);pre.write_bytes(current)
  raw['sources'][p]=dict(sha256=sha(b),blob=git('rev-parse',C+':'+p).decode().strip(),current_sha256=sha(current),current_equal=current==b)
 sys.path.insert(0,str(S/'Database/Tools/dashboard'));B=importlib.import_module('build_views');Q=importlib.import_module('requirements');G=B.G
 raw['loaded_paths']={n:m.__file__ for n,m in [('build_views',B),('requirements',Q),('generation',G)]}
 tree=ast.parse((S/'Database/Tools/dashboard/build_views.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_build');calls=[dict(name=n.func.id,line=n.lineno) for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('prior_progress','prior_generation','annotate_deltas')];raw['static_build_calls']=sorted(calls,key=lambda x:x['line']);assert [x['name'] for x in raw['static_build_calls']]==['prior_progress','prior_generation','annotate_deltas']
 inp=R/'labelled-input.json';inp.write_bytes(b'{"fixture":"synthetic prior-selector control, not database measurements"}\n');ish=sha(inp.read_bytes());raw['fixture_input_sha256']=ish
 def create(st,value,with_progress):
  b=st.begin({'fixture':{'path':str(inp)}},{'name':'ASTRA-labelled-selector-fixture','sha256':raw['driver_sha256']});names=['view-overview.json'];Path(b.output_path(names[0])).write_text(json.dumps(dict(view='overview',status='OK',definition='v1',measures=[]))+'\n')
  if with_progress:
   v=dict(view='progress',status='OK',definition=Q.VERSION,measures=[dict(id='union',numerator=value,denominator=100,scope='labelled synthetic requirement population')],progress=dict(version=Q.VERSION,scopes={'union':dict(accepted=value,total=100)},categories=[]));names.append('view-progress.json');Path(b.output_path(names[-1])).write_text(json.dumps(v)+'\n')
  gid=st.commit(b,names);man,d,probs=st.open_current();assert not probs and man['generation']==gid
  q=subprocess.run([sys.executable,'-B',str(S/'Database/Tools/analysis-kit/gfz-scripts/generation.py'),'verify',st.root],capture_output=True,text=True,timeout=10);assert q.returncode==0 and q.stdout.strip()=='PASS' and not q.stderr,(q.returncode,q.stdout,q.stderr)
  return dict(generation=gid,manifest_sha256=sha(Path(d,G.MANIFEST).read_bytes()),required_outputs=names,verify=dict(argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True))
 for name in ['empty-history','aligned-latest','latest-missing-progress']:
  st=G.Store(str(R/name/'store'));made=[]
  if name=='aligned-latest':made.append(create(st,30,True))
  elif name=='latest-missing-progress':made.extend([create(st,20,True),create(st,0,False)])
  before={f.relative_to(Path(st.root)).as_posix():sha(f.read_bytes()) for f in Path(st.root).rglob('*') if f.is_file()}
  pp=B.prior_progress(st,'labelled-build-time');pm,pd=B.prior_generation(st)
  v={'progress':dict(view='progress',definition=Q.VERSION,measures=[dict(id='union',numerator=40,denominator=100,scope='labelled synthetic requirement population')])};B.annotate_deltas(v,pd,pm);change=Q.change(pp,{'union':dict(accepted=40,total=100)},{}) if pp is not None else None
  row=dict(name=name,generations=made,progress_prior=pp,general_prior=pm,general_prior_dir=pd,annotated=v['progress'],composed_change=change,store_unchanged=before=={f.relative_to(Path(st.root)).as_posix():sha(f.read_bytes()) for f in Path(st.root).rglob('*') if f.is_file()},store_hashes=before)
  if name=='empty-history':assert pp is None and pm is None and change is None and v['progress']['measures'][0]['delta']['na']=='no prior'
  elif name=='aligned-latest':assert pp['generation']==pm['generation']==made[-1]['generation'] and change['scopes']['union']['pct']==v['progress']['measures'][0]['delta']['pp']==10.0
  else:assert pp['generation']==made[0]['generation'] and pm['generation']==made[1]['generation'] and pp['generation']!=pm['generation'] and change['scopes']['union']['pct']==20.0 and v['progress']['measures'][0]['delta']['na']=='no prior'
  assert row['store_unchanged'];raw['cases'].append(row)
 assert sha(inp.read_bytes())==ish
 for p,z in raw['sources'].items():assert sha((S/p).read_bytes())==z['sha256']
 raw['verdict']='REJECT_UNIVERSAL_SAME_PRIOR_FOR_VERIFIED_MISSING_PROGRESS_VIEW'
except BaseException as e:raw['exception']=dict(type=type(e).__name__,text=str(e));raw['verdict']='INVALID'
finally:raw['terminal']=True;(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print(raw['verdict'],raw['exception']);sys.exit(1 if raw['exception'] else 0)
