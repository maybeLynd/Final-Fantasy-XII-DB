import hashlib,json,shutil,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/save-pointer-record-alias');P.mkdir(exist_ok=False)
(P/'.gitattributes').write_bytes(b'* -text\n') # Existing project evidence policy.
for n in ('PLAN.md','README.md','derive.py','check.py','result.json'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained')
m=[dict(path=x.relative_to(P).as_posix(),bytes=x.stat().st_size,sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in sorted(P.rglob('*')) if x.is_file()]
assert m
for x in sorted(P.rglob('*')):
 if x.is_file():assert subprocess.check_output(['git','hash-object','--',x.as_posix()])==subprocess.check_output(['git','hash-object','--no-filters','--',x.as_posix()]),'Git filters alter recorded bytes: '+str(x)
(P/'manifest.json').write_text(json.dumps(dict(members=m,limits='STATIC_CONDITIONAL source ordering and count1 examples only; independent acceptance/caller reachability/general overlap unproved'),indent=2)+'\n')
print('Frozen exact source/conditional controls/consumer preimage',len(m),'members')
