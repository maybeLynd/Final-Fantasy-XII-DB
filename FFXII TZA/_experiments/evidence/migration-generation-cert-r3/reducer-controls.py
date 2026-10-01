import json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir();results=[]
for name in ('incomplete-good-cases','unknown-zero-exit'):
 p=D/name;shutil.copytree(W/'run-01',p);r=json.loads((p/'raw.json').read_text())
 if name=='incomplete-good-cases':r['finished']=False;marker='INCOMPLETE_CAPTURE'
 else:
  c=next(x for x in r['cases'] if x['name']=='unknown-input-state');c['cli']['returncode']=0
  (p/'unknown-input-state-receipt.json').write_text(json.dumps(c,indent=2)+'\n');marker='WRONG_CLI_STATUS'
 (p/'raw.json').write_text(json.dumps(r,indent=2)+'\n')
 args=[sys.executable,'-B',str(W/'check.py'),'--raw',str(p/'raw.json')]
 q=subprocess.run(args,capture_output=True,text=True,timeout=10)
 assert q.returncode!=0 and marker in q.stderr and 'ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR' not in q.stdout
 c={'name':name,'args':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'expected':marker,'terminal':True}
 (D/(name+'-receipt.json')).write_text(json.dumps(c,indent=2)+'\n');results.append(c)
(W/'reducer-controls.json').write_text(json.dumps({'finished':True,'controls':results,'credit':'two producer reducer tests, not extra archive-reader executions or independent acceptance'},indent=2)+'\n')
print('GEN_R3_REDUCER_REFUSALS',len(results))
