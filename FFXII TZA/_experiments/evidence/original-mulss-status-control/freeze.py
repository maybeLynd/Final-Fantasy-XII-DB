import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/original-mulss-status-control')
assert not P.exists();subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','capture.py','check.py','native-preflight.json','raw.json','result.json','in-progress-cases.json','freeze.py'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__'));receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  filtered=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();plain=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert filtered==plain,p
  receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=filtered))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=receipts),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts];assert members
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='B only4BshippingMULSS inside disclosed native Win64/guest wrapper, finite exact/inexact controls; bounded precision-status discrepancy, not live/full FP parity; required independent review pending'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'check.py')],check=True);print('FROZEN_STATUS57',len(members),'members',flush=True)
