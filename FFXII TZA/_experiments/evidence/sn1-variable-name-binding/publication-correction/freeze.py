import hashlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding/publication-correction');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
subprocess.run([sys.executable,str(W/'check.py')],check=True)
fault=subprocess.run([sys.executable,str(W/'check.py'),'--fault-ignore-missing-member'],capture_output=True,text=True);assert fault.returncode==1 and 'Historical incomplete manifest falsely declared complete' in fault.stderr;(W/'fault-ignore-missing-member.stderr').write_text(fault.stderr)
rows=[]
for arg,msg in [('--fault-accept-shifted-operand','Shifted operand falsely accepted'),('--fault-ignore-name-directory','Changed name directory falsely accepted'),('--fault-ignore-count-domain','Count-domain defect accepted')]:
 r=subprocess.run([sys.executable,str(W.parent/'check.py'),arg],capture_output=True,text=True);assert r.returncode==1 and msg in r.stderr;(W/(arg[2:]+'.stderr')).write_text(r.stderr);rows.append(dict(argument=arg,returncode=r.returncode,expected=msg))
(W/'impacted-semantic-controls.json').write_text(json.dumps(rows,indent=2)+'\n')
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for p in sorted(W.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or 'fresh-copy-control' in p.parts or 'publication' in p.parts:continue
 relative=p.relative_to(W);out=P/relative;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(rr,indent=2)+'\n');members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()]
assert not any('__pycache__' in m['path'] or m['path'].endswith('.pyc') for m in members)
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Original strict65 manifest remains invalid. Additive exact46 original committed members plus one inert relocated auxiliary artifact; scientific producer/default controls fixed. Independent acceptance separate.'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'check.py')],check=True);print('FROZEN_CORRECTION65',len(members),flush=True)
