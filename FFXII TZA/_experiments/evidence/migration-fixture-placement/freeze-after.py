import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/migration-my-progress-independent')
# OPUS fixture-placement notice: copytree must not export a live miniature
# database as canonical-looking .md pages. Published037557 bytes stay immutable.
# Keep active fixtures in work/; future evidence needs an inert byte capsule.
def fixture_preflight(source):
 roots=sorted(p.parent.parent.as_posix() for p in source.rglob('OPEN-QUESTIONS.md') if p.parent.name=='_index')
 assert not roots,'NESTED_FIXTURE_DATABASE_NEEDS_INERT_CAPSULE: '+', '.join(roots)
if '--preflight-only' in sys.argv:
 source=W
 if '--preflight-source' in sys.argv:source=Path(sys.argv[sys.argv.index('--preflight-source')+1])
 assert source.is_dir(),'Missing preparation source is not valid empty evidence'
 fixture_preflight(source)
 print('FIXTURE_PLACEMENT_PREFLIGHT_ONLY_NO_WRITES');sys.exit(0)
fixture_preflight(W)  # actual default invocation, BEFORE mkdir/copytree/publish
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
