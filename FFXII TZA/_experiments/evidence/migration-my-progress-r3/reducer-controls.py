import json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir();results=[]
for name in ('incomplete-good-cases','nonzero-good-json','missing-null-result','wrong-argv-flag'):
 p=D/name;shutil.copytree(W/'run-01',p);r=json.loads((p/'raw.json').read_text())
 if name=='incomplete-good-cases':r['finished']=False;marker='INCOMPLETE_CAPTURE'
 else:
  c=next(x for x in r['cases'] if x['name']=='thirty-ready-view')
  if name=='nonzero-good-json':c['returncode']=1;marker='UPSTREAM_FAILED'
  elif name=='missing-null-result':
   del c['parsed']['result'];c['stdout']=json.dumps(c['parsed'])+'\n';marker='MISSING_RESULT'
  else:c['args'][9]='--unexpected';marker='WRONG_INVOCATION'
  (p/c['name']/'receipt.json').write_text(json.dumps(c,indent=2)+'\n')
 (p/'raw.json').write_text(json.dumps(r,indent=2)+'\n')
 args=[sys.executable,'-B',str(W/'check.py'),'--raw',str(p/'raw.json')]
 q=subprocess.run(args,capture_output=True,text=True,timeout=10)
 assert q.returncode!=0 and marker in q.stderr and 'ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT' not in q.stdout
 c={'name':name,'args':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'expected':marker,'terminal':True}
 (D/(name+'-receipt.json')).write_text(json.dumps(c,indent=2)+'\n');results.append(c)
(W/'reducer-controls.json').write_text(json.dumps({'finished':True,'controls':results,'credit':'producer reducer tests only; no new original-function observations or independent acceptance'},indent=2)+'\n')
print('MY_PROGRESS_R3_REDUCER_REFUSALS',len(results))
