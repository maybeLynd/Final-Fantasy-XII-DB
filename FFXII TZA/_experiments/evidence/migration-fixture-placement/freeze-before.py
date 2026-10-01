import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/migration-my-progress-independent')
assert not P.exists(),'Frozen evidence immutable';P.mkdir(parents=True)
for n in ('PLAN.md','README.md','core-controls.py','admission-controls.py','author-suite.py','collection-controls.py','correct-collection-preparation.py','deployed-http.py','browser-receipt.py','browser-normalize.py','check.py','result.json','reducer-controls.py','reducer-controls.json'):
 shutil.copyfile(W/n,P/n)
for n in ('core-01','admission-01','author-622-01','collection-01','collection-02','collection-preparation-v1','deployed-01','deployed-ui-02','checker-preparation','reducer-controls'):
 shutil.copytree(W/n,P/n,ignore=shutil.ignore_patterns('__pycache__'))
(P/'.gitattributes').write_bytes(b'* -text\n')
def hashes():return {f.relative_to(P).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*') if f.is_file()}
before=hashes();q=subprocess.run([sys.executable,'-B',str(P/'check.py')],capture_output=True,text=True,timeout=10)
assert q.returncode==0 and 'REJECT_PROGRESS_TERMINAL' in q.stdout and not q.stderr,(q.returncode,q.stderr)
assert hashes()==before,'Default checker must not mutate evidence'
members=[{'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(P.rglob('*')) if f.is_file()]
(P/'manifest.json').write_text(json.dumps({'format':'ASTRA-immutable-evidence-1','members':members},indent=2)+'\n')
for f in P.rglob('*'):
 if f.is_file():assert subprocess.check_output(['git','hash-object','--',f.as_posix()])==subprocess.check_output(['git','hash-object','--no-filters','--',f.as_posix()]),f
print('FROZEN_PROGRESS_MEMBERS',len(members),'DEFAULT_CHECKER_READ_ONLY',flush=True)
