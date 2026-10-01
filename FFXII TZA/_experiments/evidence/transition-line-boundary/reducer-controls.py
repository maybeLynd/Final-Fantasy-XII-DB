import copy,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'reducer-controls';R.mkdir(exist_ok=False);r=json.loads((W/'run-02/raw.json').read_text());out=[]
for name,mut,why in [('missing-case',lambda z:z['cases'].pop(),'MISSING_CASE'),('nonzero-with-good-json',lambda z:z['cases'][0].update(returncode=1),'FAILED_UPSTREAM')]:
 z=copy.deepcopy(r);mut(z);f=R/(name+'.json');f.write_text(json.dumps(z,indent=2)+'\n');q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f)],capture_output=True,text=True);assert q.returncode!=0 and why in q.stderr;out.append(dict(name=name,argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True))
(W/'reducer-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('TWO_REDUCER_REFUSALS')
