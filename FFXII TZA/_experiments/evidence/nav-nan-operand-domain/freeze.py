import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/nav-nan-operand-domain');assert not P.exists()
subprocess.run([sys.executable,str(W/'check.py')],check=True);receipts=[]
for arg,expected in [('--fault-universal-nan-reject','Universal NaN rejection'),('--fault-physical-row-hash','Normalized row identity mismatch')]:
 f=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);name=arg[2:];(W/(name+'.stdout')).write_text(f.stdout);(W/(name+'.stderr')).write_text(f.stderr);receipts.append(dict(argument=arg,returncode=f.returncode,expected=expected,stdout_sha256=hashlib.sha256(f.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(f.stderr.encode()).hexdigest()));(W/'regression-controls.json').write_text(json.dumps(receipts,indent=2)+'\n');assert f.returncode==1 and expected in f.stderr
subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','capture.py','check.py','raw.json','result.json','in-progress-cases.json','freeze.py','repair_row_hash.py','regression-controls.json','fault-universal-nan-reject.stdout','fault-universal-nan-reject.stderr','fault-physical-row-hash.stdout','fault-physical-row-hash.stderr'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__'));rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b,p;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=rr),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A/B bounded NaNminA counterexample, finite/center/radius controls; no native status/game/whole malformed safety. Invalid first row reduction preserved, actual default fixed without guest rerun; independent review pending'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'check.py')],check=True);print('FROZEN59',len(members),flush=True)
