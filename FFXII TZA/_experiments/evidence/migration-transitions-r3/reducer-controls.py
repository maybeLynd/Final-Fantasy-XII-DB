import copy,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';D.mkdir(exist_ok=False);r=json.loads((W/'run-01/raw.json').read_text());out=[]
for name,mut,reason in [('missing-field',lambda z:z['fields'].pop(),'MISSING_FIELD'),('failed-writer-exit-hidden',lambda z:z['writer'][1].update(returncode=0),'WRITER_OUTCOME')]:
 z=copy.deepcopy(r);mut(z);f=D/(name+'.json');f.write_text(json.dumps(z,indent=2)+'\n');q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f)],capture_output=True,text=True,timeout=30);assert q.returncode!=0 and reason in q.stderr,(name,q.returncode,q.stderr)
 out.append(dict(name=name,argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,checker_sha256=hashlib.sha256((W/'check.py').read_bytes()).hexdigest()))
(W/'reducer-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('RECEIPT_CONTROLS_REFUSE; NO_ORIGINAL_CLI_RECAPTURE')
