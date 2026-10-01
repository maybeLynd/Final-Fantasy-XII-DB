import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-zero-total-correction');Q=W.parent/'sn1-q0-source-coordinate-domain';sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
subprocess.run([sys.executable,str(W/'check.py')],check=True)
rr=[]
for arg,expected in [('--fault-stale-total','Prose total must equal original reduced zero total'),('--fault-clamp-missing-line','Missing-coordinate control must not clamp'),('--fault-two-padding','Two-record suffix assumption')]:
 r=subprocess.run([sys.executable,str(W/'corrected60-check.py'),arg],capture_output=True,text=True,timeout=30);name=arg[2:];(W/(name+'.stdout')).write_text(r.stdout);(W/(name+'.stderr')).write_text(r.stderr)
 assert r.returncode==1 and expected in r.stderr;rr.append(dict(argument=arg,returncode=r.returncode,expected=expected,stdout_sha256=sha(r.stdout.encode()),stderr_sha256=sha(r.stderr.encode())))
(W/'regression-controls.json').write_text(json.dumps(rr,indent=2)+'\n')
subprocess.run([sys.executable,str(W/'check.py')],check=True)
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','prepare.py','check.py','corrected60-check.py','work60-default-check.py','raw.json','corrected-result.json','freeze.py','regression-controls.json','fault-stale-total.stdout','fault-stale-total.stderr','fault-clamp-missing-line.stdout','fault-clamp-missing-line.stderr','fault-two-padding.stdout','fault-two-padding.stderr']:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained')
# Supported own file claim + fresh preimage before actual default producer fix.
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-Q0-ZERO-TOTAL-CORRECTION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
old=(W/'retained/work60-check-preimage.py').read_bytes();assert (Q/'check.py').read_bytes()==old
capture_before=(Q/'capture.py').read_bytes();raw_before=(Q/'raw.json').read_bytes();assert capture_before==(W/'retained/work60-capture-preimage.py').read_bytes()
(Q/'check.py').write_bytes((W/'work60-default-check.py').read_bytes())
r=subprocess.run([sys.executable,str(Q/'capture.py')],capture_output=True,text=True,timeout=30)
(P/'default-invocation.stdout').write_text(r.stdout);(P/'default-invocation.stderr').write_text(r.stderr)
assert r.returncode==0 and 'PASS_CORRECTED60' in r.stdout and '59 all-zero' in r.stdout and 'CAPTURE60' not in r.stdout
assert (Q/'raw.json').read_bytes()==raw_before and (Q/'capture.py').read_bytes()==capture_before
receipt=dict(returncode=r.returncode,path='Actual W60 capture.py -> own corrected check.py forwarding shim -> additive E62 corrected60-check.py; immutable E60 retained unchanged',old_work_check_sha256=sha(old),new_work_check_sha256=sha((Q/'check.py').read_bytes()),expected_shim_sha256=sha((P/'work60-default-check.py').read_bytes()),capture_before_sha256=sha(capture_before),capture_after_sha256=sha((Q/'capture.py').read_bytes()),raw_before_sha256=sha(raw_before),raw_after_sha256=sha((Q/'raw.json').read_bytes()),stdout_sha256=sha(r.stdout.encode()),stderr_sha256=sha(r.stderr.encode()))
assert receipt['new_work_check_sha256']==receipt['expected_shim_sha256'];(P/'default-invocation-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b,p;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=rr),indent=2)+'\n')
members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Additive correction of60 prose/output total61 to original actual59; physical/parser/missing-coordinate/suffix findings unaffected. No recapture/native/game; owner review/propagation separate.'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'check.py')],check=True);print('FROZEN62',len(members),flush=True)
