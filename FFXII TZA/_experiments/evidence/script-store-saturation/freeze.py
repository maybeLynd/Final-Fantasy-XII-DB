import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'raw.json').read_bytes());extra=sha((W/'extra-s16-boundary.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'PASS67' in r.stdout and 'CAPTURE67' not in r.stdout and sha((W/'raw.json').read_bytes())==before and sha((W/'extra-s16-boundary.json').read_bytes())==extra
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr);(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=0,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_unchanged_sha256=before,extra_unchanged_sha256=extra,path='Actual retained raw-default; reducer only, original25 guest cases never replayed'),indent=2)+'\n')
rows=[]
for arg,msg in [('--fault-narrowing-wrap','Wrapping cast disagrees'),('--fault-standard-s16-bounds','Conventional signed16 clamp contradicts'),('--fault-no-write-as-undetected','No-write claim must retain positive'),('--fault-accept-clamp-mutation','Original clamp opcode matters')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and msg in r.stderr;(W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);rows.append(dict(argument=arg,returncode=r.returncode,expected=msg))
(W/'regression-controls.json').write_text(json.dumps(rows,indent=2)+'\n');P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
names=['PLAN.md','README.md','capture.py','check.py','freeze.py','raw.json','result.json','failure.json','repair-s16-policy.py','extra-s16-boundary.py','extra-s16-boundary.json','extra-runner-failure.json','repair-extra-runner-scope.py','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json']+[x['argument'][2:]+ext for x in rows for ext in ['.stdout','.stderr']]
for n in names:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(rr,indent=2)+'\n');members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()];assert not any('__pycache__' in x['path'] for x in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Original bounded resolved-store memory effects incl unusual signed16 bounds; injected state/disposable emulation, no original caller/nativegame/live/lifetime proof. Consumer repair/independent acceptance separate.'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN67',len(members),flush=True)
