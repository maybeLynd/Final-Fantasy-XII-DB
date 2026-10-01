import copy,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'reducer-controls';R.mkdir(exist_ok=False);raw=json.loads((W/'run-03/raw.json').read_text());out=[]
for name,mut,reason in [('missing-case',lambda z:z['cases'].pop(),'MISSING_CASE'),('failed-verifier-good-observations',lambda z:z['cases'][1]['generations'][0]['verify'].update(returncode=1),'VERIFIER_PREREQUISITE')]:
 z=copy.deepcopy(raw);mut(z);f=R/(name+'.json');f.write_text(json.dumps(z,indent=2)+'\n');q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f)],capture_output=True,text=True,timeout=30);assert q.returncode!=0 and reason in q.stderr,(name,q.returncode,q.stderr)
 out.append(dict(name=name,argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,checker_sha256=hashlib.sha256((W/'check.py').read_bytes()).hexdigest()))
(W/'reducer-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('RECEIPT_CONTROLS_REFUSE; NO_SELECTOR_RECAPTURE')
