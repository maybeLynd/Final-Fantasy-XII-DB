"""Regression for the demonstrated real invocation-path stdlib-shadow failure."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'inspect-02.status.json').read_text());v=json.loads((P/'inspection-02.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'inspect-slot-source.py') or v.get('inspection_complete') is not True or v['driver_sha256']!=sha(P/'inspect-slot-source.py') or len(v['ranges'])!=4:raise RuntimeError('required actual positive missing')
Q=P/'shadow-control-01';Q.mkdir(exist_ok=False)
files=['inspect-slot-source.py','capture.py','capture-index-path.py','source-01.json','capture-01.status.json','capture-01.stdout','capture-01.stderr','validate-title-source-annotations.py','prove_owner_reload_order.py']
for n in files:shutil.copy2(P/n,Q/n)
shutil.copy2(P/'inspect-01-driver.py',Q/'inspect.py')
argv=[sys.executable,'-B',str(Q/'inspect-slot-source.py'),'refused-result.json']
row={'argv':argv,'terminal':False,'exit':None,'exception':None,'driver_sha256':sha(Q/'inspect-slot-source.py'),'files':[{'path':p.name,'sha256':sha(p)} for p in sorted(Q.iterdir())]}
try:
 r=subprocess.run(argv,capture_output=True,stdin=subprocess.DEVNULL,timeout=25)
 (Q/'stdout.raw').write_bytes(r.stdout);(Q/'stderr.raw').write_bytes(r.stderr)
 row.update(terminal=True,exit=r.returncode,diagnostic_matched=b'local inspect.py would shadow required standard library' in r.stderr,result_absent=not(Q/'refused-result.json').exists(),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest())
except Exception as e:
 row['exception']=repr(e);(Q/'stdout.raw').write_bytes(b'');(Q/'stderr.raw').write_bytes(repr(e).encode())
(Q/'receipt.json').write_bytes((json.dumps(row,indent=2)+'\n').encode())
if row['terminal'] is not True or row['exit']==0 or row['exception'] is not None or not row['diagnostic_matched'] or not row['result_absent']:raise RuntimeError('invalid/incomplete shadow refusal')
out=P/'shadow-control-result-01.json'
if out.exists():raise RuntimeError('immutable result exists')
out.write_bytes((json.dumps({'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_driver_sha256':sha(P/'inspect-slot-source.py'),'case':row,'limits':'One actual disposable CLI refusal plus checked four-body source-inspection positive. No semantic/native/live conclusion or independent acceptance.'},indent=2)+'\n').encode())
print('CONTROLLED concrete stdlib-shadow refusal before output; positive remains checked; no FF12 execution')
