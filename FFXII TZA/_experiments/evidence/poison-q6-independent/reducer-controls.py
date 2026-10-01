import copy,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'reducer-controls';R.mkdir(exist_ok=False);r=json.loads((W/'run-01/raw.json').read_text());out=[]
for name,mut,why in [('upstream-fail',lambda z:z['prerequisite'].update(ok=False),'UPSTREAM_FAILED_OR_MISSING'),('missing-boundary',lambda z:z['independent_boundaries'].pop('equal_critical_line'),'INCOMPLETE_BOUNDARIES'),('exception-with-good-results',lambda z:z.update(exception={'type':'RuntimeError','text':'labelled control'}),'INVALID_OR_INCOMPLETE_CAPTURE')]:
 z=copy.deepcopy(r);mut(z);f=R/(name+'.json');f.write_text(json.dumps(z,indent=2)+'\n');q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f)],capture_output=True,text=True);assert q.returncode!=0 and why in q.stderr,(name,q.returncode,q.stderr);out.append(dict(name=name,argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,shipping_code_executed=False))
(W/'reducer-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('THREE_REQUIRED_RECEIPT_REFUSALS')
