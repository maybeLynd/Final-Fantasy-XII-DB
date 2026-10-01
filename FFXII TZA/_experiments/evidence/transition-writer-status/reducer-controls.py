import copy,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'reducer-controls';R.mkdir(exist_ok=False);r=json.loads((W/'run-01/raw.json').read_text());out=[]
for name,mut,why in [('missing-status-control',lambda z:z['cases'].pop(),'MISSING_CASE'),('relabelled-child-status',lambda z:z['cases'][1]['child'].update(exit_code=0),'AssertionError')]:
 z=copy.deepcopy(r);mut(z);f=R/(name+'.json');f.write_text(json.dumps(z,indent=2)+'\n');q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f)],capture_output=True,text=True);assert q.returncode!=0 and why in q.stderr;out.append(dict(argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,checker_sha256=hashlib.sha256((W/'check.py').read_bytes()).hexdigest()))
(W/'reducer-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('RECEIPT_CONTROLS_REFUSE')
