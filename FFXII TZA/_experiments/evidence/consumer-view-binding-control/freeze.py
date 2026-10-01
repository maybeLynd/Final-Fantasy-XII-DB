import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/consumer-view-binding-control')
assert not P.exists();subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','capture.py','check.py','result.json','freeze.py','mutation.json','partial-receipts.json','cleanup.json'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained');receipts=[]
for p in sorted(P.rglob('*')):
    if p.is_file():
        f=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();u=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert f==u,p
        receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=f))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=receipts),indent=2)+'\n')
m=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts];assert m
(P/'manifest.json').write_text(json.dumps(dict(members=m,limits='A actualconfiguredhostproducer/inputpaircontrol, fourverifiedsources; privatechangedbinaryneverexecuted/removed. No original/native/live semantics or historicaldefaultcachewrongness.'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'check.py')],check=True);print('Frozen byte-safe view-binding control',len(m),'members',flush=True)
