import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/uc1-257-single-extent')
assert not P.exists();subprocess.run([sys.executable,str(W/'review.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','review.py','normalize.py','check.py','recover.py','raw.json','result.json','freeze.py'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__'));receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  f=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();u=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert f==u,p
  receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=f))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=receipts),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts];assert members
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A one requested353B extent only, current-at-capture source projection; other49held untouched; independent acceptance/admission/ABI/meaning/native reachability not awarded'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'review.py')],check=True);print('FROZEN_BOUNDARY54',len(members),'members with original failed normalization and unchanged raw',flush=True)
