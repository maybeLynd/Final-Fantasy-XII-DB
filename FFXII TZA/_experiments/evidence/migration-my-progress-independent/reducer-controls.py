import copy,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir();rr=[]
for name,phase,src in [('incomplete-admission','admission','admission-01/raw.json'),('missing-admission-case','admission','admission-01/raw.json'),('hide-zero-admission','admission','admission-01/raw.json'),('author-upstream-fails','author','author-622-01/raw.json')]:
 r=json.loads((W/src).read_text())
 if name=='incomplete-admission':r['finished']=False
 elif name=='missing-admission-case':r['cases']=[x for x in r['cases'] if x['name']!='invalid-terminal0']
 elif name=='hide-zero-admission':next(x for x in r['cases'] if x['name']=='invalid-terminal0')['admitted']=False
 else:r['returncode']=1
 p=D/(name+'.json');p.write_text(json.dumps(r,indent=2)+'\n');out=D/(name+'-result.json')
 cmd=[sys.executable,'-B',str(W/'check.py'),'--phase',phase,'--raw',str(p),'--out',str(out)]
 q=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
 assert q.returncode!=0 and 'AssertionError' in q.stderr and 'FileNotFoundError' not in q.stderr and not out.exists()
 rr.append({'name':name,'args':cmd,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'result_created':out.exists()})
# The real normalization invocation must reject a missing item identity rather
# than treating a wrong schema as a valid empty drilldown. No new HTTP/UI run.
pdoc=json.loads((W/'deployed-ui-02/progress.json').read_text());next(x for x in pdoc['view']['progress']['categories'] if x['code']=='W')['items'][0].pop('k')
p=D/'missing-item-identity.json';p.write_text(json.dumps(pdoc,indent=2)+'\n');out=D/'missing-item-identity-result.json'
cmd=[sys.executable,'-B',str(W/'browser-normalize.py'),'--progress',str(p),'--out',str(out)]
q=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
assert q.returncode!=0 and 'Missing/empty original item k' in q.stderr and not out.exists()
rr.append({'name':'missing-item-identity','args':cmd,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'result_created':out.exists()})
(W/'reducer-controls.json').write_text(json.dumps(rr,indent=2)+'\n')
print('FIVE_CONCRETE_INVOCATION_FAILURE_CONTROLS_REFUSED',flush=True)
