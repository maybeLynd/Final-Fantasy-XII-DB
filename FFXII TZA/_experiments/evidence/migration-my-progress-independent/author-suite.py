import ast, hashlib, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'author-622-01';assert not D.exists(),'Preserve authored-suite run';D.mkdir()
commit=subprocess.check_output(['git','rev-parse','622c0866d'],text=True).strip();root=D/'source'
available=set(subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--','Database/Tools/dashboard','Database/Tools/analysis-kit/gfz-scripts'],text=True).splitlines())
dirs=['Database/Tools/dashboard/','Database/Tools/analysis-kit/gfz-scripts/']
queue=['Database/Tools/dashboard/test_requirements.py'];done={}
while queue:
 rel=queue.pop(0)
 if rel in done:continue
 data=subprocess.check_output(['git','show',commit+':'+rel]);p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 done[rel]={'sha256':hashlib.sha256(data).hexdigest(),'blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip()}
 for n in ast.walk(ast.parse(data)):
  mods=[a.name.split('.')[0] for a in n.names] if isinstance(n,ast.Import) else [n.module.split('.')[0]] if isinstance(n,ast.ImportFrom) and n.module else []
  for m in mods:
   for prefix in dirs:
    candidate=prefix+m+'.py'
    if candidate in available and candidate not in done and candidate not in queue:queue.append(candidate)
for rel in ('Database/FFXII TZA/_index/workflow/my-progress/category-map.tsv','Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md','Database/FFXII TZA/_index/completion-packages/README.md'):
 data=subprocess.check_output(['git','show',commit+':'+rel]);p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 done[rel]={'sha256':hashlib.sha256(data).hexdigest(),'blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip()}
tmp=D/'tmp';tmp.mkdir();resolved=tmp.resolve();assert resolved.is_relative_to(W.resolve())
env=os.environ.copy();env.update(TMP=str(resolved),TEMP=str(resolved),TMPDIR=str(resolved),PYTHONDONTWRITEBYTECODE='1')
exe=str(Path(sys._base_executable));args=[exe,'-B',str(root/'Database/Tools/dashboard/test_requirements.py')]
q=subprocess.run(args,cwd=root,env=env,capture_output=True,text=True,timeout=90)
lines=q.stdout.splitlines();tags={line.split()[1]:line.split()[0] for line in lines if line.startswith(('PASS  MP','FAIL  MP'))}
raw={'method':'Requested unmodified producer-authored MP1-MP12 rerun, separate from independently derived controls; not whole acceptance',
 'commit':commit,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sources':done,'args':args,'python':sys.version,
 'stdout':q.stdout,'stderr':q.stderr,'returncode':q.returncode,'terminal':True,'tags':tags,
 'temp_root':str(resolved),'cleanup_limit':'Unmodified suite removes its own mkdtemp child under explicitly scoped TMP/TEMP root; no production fixture/board/game writes. Process terminal; no parent alive inference.',
 'all_sources_unchanged':all(hashlib.sha256((root/p).read_bytes()).hexdigest()==v['sha256'] for p,v in done.items()),
 'complete_case_set':set(tags)=={'MP'+str(i) for i in range(1,13)},'scope':'Requested622c0866d only, published DD/delta additions untested by this authored suite'}
(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
assert raw['all_sources_unchanged'] and raw['complete_case_set'],'Incomplete authored run, not PASS'
assert q.returncode==0 and lines[-1]=='FAILS 0' and all(x=='PASS' for x in tags.values()),'Authored suite rejected, preserve raw'
print('REQUESTED_AUTHORED_MP1_MP12_COMPLETE',len(done),'source members',flush=True)
