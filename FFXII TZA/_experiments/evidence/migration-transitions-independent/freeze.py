import copy, hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-independent')
assert not P.exists(),'Preserve published package'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((W/'read-only-01/raw.json').read_text());D=W/'reducer-controls';D.mkdir();receipts=[]
for name in ('incomplete','missing-case','hide-admitted-typed-commit'):
 x=copy.deepcopy(r)
 if name=='incomplete':x['finished']=False
 elif name=='missing-case':x['cases'].pop()
 else:next(c for c in x['cases'] if c['name']=='typed-commit')['parsed_report'][0]['transition']='MALFORMED'
 f=D/(name+'.json');out=D/(name+'-result.json');f.write_text(json.dumps(x,indent=2)+'\n')
 q=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(f),'--out',str(out)],capture_output=True,text=True)
 receipts.append({'name':name,'input_sha256':sha(f),'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'result_exists':out.exists()})
 assert q.returncode!=0 and not out.exists()
q=subprocess.run([sys.executable,'-B',str(W/'check.py')],capture_output=True,text=True);assert q.returncode==0,q.stderr
(W/'reducer-controls.json').write_text(json.dumps({'baseline':{'returncode':q.returncode,'stdout':q.stdout},'negative_controls':receipts},indent=2)+'\n')
P.mkdir(parents=True);(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','capture.py','read-only-controls.py','inmemory-control.py','inmemory-controls.json','check.py','freeze.py','result.json','reducer-controls.json'):shutil.copyfile(W/n,P/n)
for n in ('run-01','read-only-01','reducer-controls'):shutil.copytree(W/n,P/n)
members=[{'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(P.rglob('*')) if f.is_file()]
(P/'manifest.json').write_text(json.dumps({'package':P.name,'members':members},indent=2)+'\n')
for f in P.rglob('*'):
 if f.is_file():
  filtered=subprocess.check_output(['git','hash-object','--',f.as_posix()],text=True).strip();plain=subprocess.check_output(['git','hash-object','--no-filters','--',f.as_posix()],text=True).strip()
  assert filtered==plain,f
q=subprocess.run([sys.executable,'-B',str(P/'check.py'),'--out',str(P/'result.json')],capture_output=True,text=True);assert q.returncode==0,q.stderr
print('FROZEN_TRANSITION_REJECT',len(members),'full apply remains INCOMPLETE',flush=True)
