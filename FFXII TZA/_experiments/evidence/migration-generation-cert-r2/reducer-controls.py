import copy,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir();raw=json.loads((W/'run-01/raw.json').read_text());rr=[]
for name in ('incomplete','omit-positive','hide-unknown-state-certification'):
 r=copy.deepcopy(raw)
 if name=='incomplete':r['finished']=False
 elif name=='omit-positive':r['cases']=[c for c in r['cases'] if c['name']!='positive']
 else:next(c for c in r['cases'] if c['name']=='unknown-input-state')['label']='UNVERIFIED'
 p=D/(name+'.json');p.write_text(json.dumps(r,indent=2)+'\n');out=D/(name+'-result.json')
 q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(p),'--out',str(out)],capture_output=True,text=True,timeout=10)
 assert q.returncode!=0 and 'AssertionError' in q.stderr and not out.exists()
 rr.append({'name':name,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'result_created':out.exists()})
(W/'reducer-controls.json').write_text(json.dumps(rr,indent=2)+'\n')
print('THREE_R2_RECEIPT_CONTROLS_REFUSED',flush=True)
