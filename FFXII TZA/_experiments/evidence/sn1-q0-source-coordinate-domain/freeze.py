import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');assert not P.exists()
sha=lambda b:hashlib.sha256(b).hexdigest();before=sha((W/'raw.json').read_bytes());driver=sha((W/'capture.py').read_bytes())
r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30)
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr)
(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,driver_sha256=driver,raw_before_sha256=before,raw_after_sha256=sha((W/'raw.json').read_bytes()),stdout_sha256=sha(r.stdout.encode()),stderr_sha256=sha(r.stderr.encode()),path='Actual capture.py default with retained raw present invokes corrected check.py; no recapture or new native execution'),indent=2)+'\n')
assert r.returncode==0 and 'PASS60' in r.stdout and 'CAPTURE60' not in r.stdout and sha((W/'raw.json').read_bytes())==before and sha((W/'capture.py').read_bytes())==driver
receipts=[]
for arg,expected in [('--fault-clamp-missing-line','Missing-coordinate control must not clamp'),('--fault-two-padding','Two-record suffix assumption')]:
 c=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);name=arg[2:];(W/(name+'.stdout')).write_text(c.stdout);(W/(name+'.stderr')).write_text(c.stderr);receipts.append(dict(argument=arg,returncode=c.returncode,expected=expected,stdout_sha256=sha(c.stdout.encode()),stderr_sha256=sha(c.stderr.encode())));(W/'regression-controls.json').write_text(json.dumps(receipts,indent=2)+'\n');assert c.returncode==1 and expected in c.stderr
subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','repair.py','raw.json','result.json','in-progress-modules.json','freeze.py','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json','fault-clamp-missing-line.stdout','fault-clamp-missing-line.stderr','fault-two-padding.stdout','fault-two-padding.stderr']:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__'));rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b,p;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=rr),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A physical source-coordinate domain only; internal EOF+1 exceptions and0..3 suffixes, index convention/cause/X unresolved; original/failure/control/default-path receipts preserved and independent acceptance pending'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN60',len(members),flush=True)
