import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/native-filter-message-resource');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'raw.json').read_bytes());r=subprocess.run([sys.executable,str(W/'capture.py')],capture_output=True,text=True,timeout=30)
assert r.returncode==0 and 'PASS82' in r.stdout and 'CAPTURE82' not in r.stdout and sha((W/'raw.json').read_bytes())==before
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr)
(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,capture_sha256=sha((W/'capture.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),raw_unchanged_sha256=before,path='Actual retained-only default, no source recapture/execution'),indent=2)+'\n')
controls=[]
for arg,msg in [('--fault-index-six','Original id7837 selects entry7, not neighboring entry6'),('--fault-terminator','RT_STRING stores counted UTF16; no included nul terminator for this entry'),('--fault-trap-fallthrough','INT3 is a terminal boundary; adjacent routine is not local CFG evidence')]:
 r=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);assert r.returncode==1 and msg in r.stderr
 (W/(arg[2:]+'.stdout')).write_text(r.stdout);(W/(arg[2:]+'.stderr')).write_text(r.stderr);controls.append(dict(argument=arg,returncode=r.returncode,expected=msg))
# Concrete default capture path, not only provider-field/helper existence.
q=W/'private-bad-provider';assert not q.exists();q.mkdir()
for n in ['capture.py','check.py']:shutil.copyfile(W/n,q/n)
shutil.copytree(W/'retained',q/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
bad=json.loads((W/'raw.json').read_text());bad['tools']['provider_files'][0]['sha256']='0'*64;(q/'raw.json').write_text(json.dumps(bad,indent=2)+'\n')
r=subprocess.run([sys.executable,str(q/'capture.py')],capture_output=True,text=True,timeout=30)
assert r.returncode!=0 and 'Actual decoder provider identity mismatch' in r.stderr and 'CalledProcessError' in r.stderr and not(q/'result.json').exists() and 'CAPTURE82' not in r.stdout
(W/'bad-provider.stdout').write_text(r.stdout);(W/'bad-provider.stderr').write_text(r.stderr)
(W/'bad-provider-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,capture_sha256=sha((q/'capture.py').read_bytes()),check_sha256=sha((q/'check.py').read_bytes()),private_raw_sha256=sha((q/'raw.json').read_bytes()),intervention='Private required provider SHA=>zero, copied byte-identical actual producer and original retained inputs',result_present=False,source_raw_unchanged_sha256=before,limits='Concrete retained-only path; no native/live/execution. Does not retroactively measure81 provider.'),indent=2)+'\n')
assert sha((W/'raw.json').read_bytes())==before
(W/'regression-controls.json').write_text(json.dumps(controls,indent=2)+'\n');P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','raw.json','result.json','resource-feasibility.json','prepare-resource.py','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','regression-controls.json','bad-provider.stdout','bad-provider.stderr','bad-provider-receipt.json']+[x['argument'][2:]+ext for x in controls for ext in ['.stdout','.stderr']]:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b;receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(receipts,indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()];assert not any('__pycache__' in x['path'] for x in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='A selected shipping embeddedtext/helper source, no native/live/moduleinitialization/languageselection/visiblemessage/lifetime/EXP127cause/independent acceptance'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'capture.py')],check=True);print('FROZEN82',len(members),flush=True)
