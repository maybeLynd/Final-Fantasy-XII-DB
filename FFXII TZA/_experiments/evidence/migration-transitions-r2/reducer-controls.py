"""Small changed-receipt controls through actual reducer CLI, never recapture."""
import copy,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir()
raw=json.loads((W/'run-01/raw.json').read_text());results=[]
for name in ('nonzero-with-good-json','empty-cases','wrong-route-owner'):
    d=D/name;shutil.copytree(W/'run-01',d)
    r=copy.deepcopy(raw)
    if name=='nonzero-with-good-json': r['cases'][0]['returncode']=1
    elif name=='empty-cases':r['cases']=[]
    else:r['cases'][0]['original_plan'][0][3]['task']['assigned_to']='FABLE'
    (d/'raw.json').write_text(json.dumps(r,indent=2)+'\n')
    for c in r['cases']:(d/c['name']/'receipt.json').write_text(json.dumps(c,indent=2)+'\n')
    args=[sys.executable,'-B',str(W/'check.py'),'--run',str(d)]
    q=subprocess.run(args,capture_output=True,text=True,timeout=10)
    expected={'nonzero-with-good-json':'UPSTREAM_FAILED','empty-cases':'MISSING_OR_DUPLICATE_CASE','wrong-route-owner':'WRONG_ROUTE_OWNER'}[name]
    assert q.returncode!=0 and expected in q.stderr and 'ACCEPT_SCOPED_ADMISSION' not in q.stdout
    receipt={'name':name,'args':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'expected_refusal':expected,'terminal':True}
    (D/(name+'-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');results.append(receipt)
(W/'reducer-controls.json').write_text(json.dumps({'finished':True,'controls':results,'purpose':'producer reducer checks, not independent acceptance or original writer fault controls'},indent=2)+'\n')
print('REDUCER_REFUSALS',len(results))
