import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/native-divide-consumer-scope');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'raw.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30)
assert r.returncode==0 and 'PASS84' in r.stdout and 'CAPTURE84' not in r.stdout and sha((W/'raw.json').read_bytes())==before
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr)
(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_unchanged_sha256=before,path='Actual retained-only reduction of producer-fragment controls, not full peer default/original-code/native execution'),indent=2)+'\n')
controls=[]
for arg,msg in [('--fault-rejects-analysis','Exact source Z suppresses required register-analysis failure and still passes'),('--fault-rejects-short-decode','Exact source Z accepts incomplete declared-range decoding'),('--fault-retract-baseline','Current independent declared-range baseline is complete and error-free; preserve its valid scoped facts')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and msg in r.stderr
 (W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);controls.append(dict(argument=arg,returncode=r.returncode,expected=msg))
(W/'regression-controls.json').write_text(json.dumps(controls,indent=2)+'\n');P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','raw.json','result.json','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json','failed-no-cmp-capture.py','failed-no-cmp-receipt.json']+[x['argument'][2:]+ext for x in controls for ext in ['.stdout','.stderr']]:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b;receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(receipts,indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()];assert not any('__pycache__' in x['path'] for x in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A exact Z producer-fragment controls/current complete literal-range baseline, not full peer default/original-code/native/no-catch/independent acceptance'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN84',len(members),flush=True)
