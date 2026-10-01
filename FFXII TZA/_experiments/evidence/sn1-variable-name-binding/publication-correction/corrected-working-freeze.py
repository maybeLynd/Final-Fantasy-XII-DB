import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding');sha=lambda b:hashlib.sha256(b).hexdigest()
if P.exists():
 subprocess.run([sys.executable,str(W/'publication-correction/check.py')],check=True);sys.exit(0)
rawhash=sha((W/'raw.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'PASS65' in r.stdout and 'CAPTURE65' not in r.stdout and sha((W/'raw.json').read_bytes())==rawhash
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr);(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=0,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_before_sha256=rawhash,raw_after_sha256=sha((W/'raw.json').read_bytes()),path='Actual capture default with retained raw invokes corrected checker, no recapture or original code execution'),indent=2)+'\n')
faults=[]
for arg,message in [('--fault-accept-shifted-operand','Shifted operand falsely accepted'),('--fault-ignore-name-directory','Changed name directory falsely accepted'),('--fault-ignore-count-domain','Count-domain defect accepted')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and message in r.stderr;(W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);faults.append(dict(argument=arg,returncode=r.returncode,expected=message,stdout_sha256=sha(r.stdout.encode()),stderr_sha256=sha(r.stderr.encode())))
(W/'regression-controls.json').write_text(json.dumps(faults,indent=2)+'\n')
# Reuse validated actual codec-provider identity, not a nonexistent extension file.
tool=json.loads(Path('Database/FFXII TZA/_experiments/evidence/sn1-logical-coordinate-domain/tool-identity.json').read_text());assert tool['python']==sys.version and tool['interpreter_sha256']==sha(Path(sys.executable).read_bytes()) and sha(Path(tool['codec_provider']).read_bytes())==tool['codec_provider_sha256'];(W/'codec-tool-identity.json').write_text(json.dumps(tool,indent=2)+'\n')
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
names=['PLAN.md','README.md','capture.py','check.py','repair.py','freeze.py','feasibility.py','feasibility.json','raw.json','result.json','failure.json','codec-tool-identity.json','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json']
names.extend([f['argument'][2:]+e for f in faults for e in ['.stdout','.stderr']])
for n in names:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b,p;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=rr),indent=2)+'\n');members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Sampled original T0/operand/name/descriptor identity, not universal compiler order or live/native effects. Independent acceptance/consumer incorporation pending.'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN65',len(members),flush=True)
