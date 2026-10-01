import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-assignment-attribution-boundary');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'raw.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'PASS66' in r.stdout and 'CAPTURE66' not in r.stdout and sha((W/'raw.json').read_bytes())==before
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr);(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=0,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_before_sha256=before,raw_after_sha256=sha((W/'raw.json').read_bytes()),path='Actual retained raw default; no bytecode/native/live execution or recapture'),indent=2)+'\n')
rr=[]
for arg,msg in [('--fault-tagged-group-as-statement','Tagged group incorrectly required'),('--fault-literal-only-attribution','Literal-only matcher falsely identifies'),('--fault-universal-minus-one','Universal minus-one misattributes')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and msg in r.stderr;(W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);rr.append(dict(argument=arg,returncode=r.returncode,expected=msg))
(W/'regression-controls.json').write_text(json.dumps(rr,indent=2)+'\n')
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','raw.json','result.json','reuse-call-control.py','correct-helper-label.py','helper-label-correction.json','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json']+[x['argument'][2:]+ext for x in rr for ext in ['.stdout','.stderr']]:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));pins=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b; pins.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(pins,indent=2)+'\n');members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()];assert not any('__pycache__' in m['path'] for m in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Four original assignment/tag boundary samples, no universal shift/compiler cause/native effects or semantic acceptance.65 original incomplete publication explicitly qualified by additive correction.'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN66',len(members),flush=True)
