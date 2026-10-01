import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/native-exception-filter-tail');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'raw.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30)
assert r.returncode==0 and 'PASS81' in r.stdout and 'CAPTURE81' not in r.stdout and sha((W/'raw.json').read_bytes())==before
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr)
(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_unchanged_sha256=before,path='Actual producer default retained-only reduction, no original-code/native/live execution'),indent=2)+'\n')
controls=[]
for arg,msg in [('--fault-return-zero','Original local RET is preceded by MOV EAX,1'),('--fault-cursor-before-text','Original text request precedes cursor call'),('--fault-name-ordinal','Ordinal identity is not a captured import-by-name')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and msg in r.stderr
 (W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);controls.append(dict(argument=arg,returncode=r.returncode,expected=msg))
(W/'regression-controls.json').write_text(json.dumps(controls,indent=2)+'\n');P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','raw.json','result.json','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json','import-preflight-failure.json','invocation-status-control.py','returned-reconciliation.json']+[x['argument'][2:]+ext for x in controls for ext in ['.stdout','.stderr']]:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
# Preserve controls/status/output; shared exact80 inputs remain in its frozen
# package and are identified by the control receipt. Do not duplicate seven inputs.
src=W/'invocation-status-controls';dst=P/'invocation-status-controls';dst.mkdir();shutil.copyfile(src/'receipt.json',dst/'receipt.json')
for arm in json.loads((src/'receipt.json').read_text())['arms']:
 q=dst/arm['name'];q.mkdir()
 for n in ['stdout.txt','stderr.txt']:shutil.copyfile(src/arm['name']/n,q/n)
 if arm['name'] in ('upstream-exit','upstream-exception'):shutil.copyfile(src/arm['name']/'check.py',q/'private-checker.py')
receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b;receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(receipts,indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()]
assert not any('__pycache__' in x['path'] for x in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A local source/control receipts only; no original-code/native/live/filterdispatch/presentation/EXP127cause/independent acceptance'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'capture.py')],check=True)
print('FROZEN81',len(members),flush=True)
