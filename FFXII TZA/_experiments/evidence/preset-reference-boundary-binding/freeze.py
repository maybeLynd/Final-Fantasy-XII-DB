import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/preset-reference-boundary-binding')
assert not P.exists()
subprocess.run([sys.executable,str(W/'check.py')],check=True)
f=subprocess.run([sys.executable,str(W/'check.py'),'--fault-old-binding'],capture_output=True,text=True,timeout=30)
(W/'fault-old-binding.stdout').write_text(f.stdout);(W/'fault-old-binding.stderr').write_text(f.stderr)
(W/'regression-control.json').write_text(json.dumps(dict(returncode=f.returncode,command=[sys.executable,str(W/'check.py'),'--fault-old-binding'],expected='Old default source binding must fail actual refs(img) negative-control replay',stdout_sha256=hashlib.sha256(f.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(f.stderr.encode()).hexdigest(),limits='Deliberate local host producer mutation, not an invalid FF12/native experiment'),indent=2)+'\n')
assert f.returncode==1 and 'Default source binding regression' in f.stderr
subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','capture.py','adapter.py','check.py','raw.json','result.json','in-progress-cases.json','freeze.py','fault-old-binding.stdout','fault-old-binding.stderr','regression-control.json'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__'))
receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  filtered=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();plain=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert filtered==plain,p;receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=filtered))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=receipts),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A only bounded actual-producer source-binding control and disclosed local default repair. No historical original-image census disproof or whole-image/global reachability/native proof; independent acceptance pending'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'check.py')],check=True);print('FROZEN58',len(members),flush=True)
