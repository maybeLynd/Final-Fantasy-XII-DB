"""Actual producer CLI prerequisite/mutation controls; not original-code execution."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-02';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((P/'proof-02.status.json').read_text());positive=json.loads((P/'result-02.json').read_text())
if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(P/'prove.py') or positive.get('producer_complete') is not True or positive['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing valid actual positive')
rows=[]
# Reuse two actual prior refusals; changing the expected diagnostic does not
# justify rerunning an unchanged case. Bind raw status/driver/output identities.
for name,diag in [('failed-capture','required capture status failed'),('failed-retained-capture','retained input changed')]:
 q=P/'controls-01'/name;oldrow=json.loads((q/'receipt.json').read_text())
 if oldrow['exit']==0 or oldrow['driver_sha256']!=sha(P/'prove.py') or oldrow['stdout_sha256']!=sha(q/'stdout.raw') or oldrow['stderr_sha256']!=sha(q/'stderr.raw') or diag.encode() not in(q/'stderr.raw').read_bytes() or(q/'refused-result.json').exists():raise RuntimeError('invalid retained actual refusal')
 row=dict(oldrow,diagnostic=diag,diagnostic_matched=True,reused_actual_run=True,prior_receipt='controls-01/'+name+'/receipt.json',prior_receipt_sha256=sha(q/'receipt.json'),correction='Retained hash guard refuses before retained-status gate; original failedcontrol1 diagnostic expectation preserved')
 rows.append(row)
for name,diag in [('missing-source','source-01.json'),('coherent-page-head-mutation','original byte mismatch')]:
 q=D/name;q.mkdir()
 for s in P.iterdir():
  if s.name=='result-02.json' or s.name.startswith('controls-') or s.name.startswith('control-'):continue
  if s.is_dir():shutil.copytree(s,q/s.name)
  elif s.is_file():shutil.copy2(s,q/s.name)
 if name=='failed-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 elif name=='failed-retained-capture':
  f=q/'retained/capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 elif name=='missing-source':(q/'source-01.json').unlink()
 else:
  f=q/'source-01.json';x=json.loads(f.read_text());found=0
  for rr in x['ranges']:
   for i in rr['instructions']:
    if i['pc']=='0x51f743':
     assert i['bytes']=='837b18ff' and i['args']=='dword ptr [rbx + 0x18], -1';i['bytes']='837b1cff';i['args']='dword ptr [rbx + 0x1c], -1';i['memory'][0]['displacement']=0x1c;found+=1
   rr['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in rr['instructions']))).hexdigest()
  assert found==1;f.write_text(json.dumps(x,indent=2)+'\n')
 r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),'refused-result.json'],capture_output=True,timeout=20)
 (q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
 row={'name':name,'exit':r.returncode,'diagnostic':diag,'diagnostic_matched':diag.encode() in r.stderr,'refused_result_absent':not(q/'refused-result.json').exists(),'driver_sha256':sha(q/'prove.py'),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'terminal':True,'exception':None}
 (q/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
 if r.returncode==0 or not row['diagnostic_matched'] or not row['refused_result_absent']:raise RuntimeError('control not discriminating '+name)
 rows.append(row)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':len(rows),'limits':'Disposable CLI evidence mutations only; no FF12 native/game, no original-code execution or live observation'}
if len(rows)!=4:raise RuntimeError('incomplete/zero controls')
(P/'control-result-02.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS four actual cause-specific refusals (two retained/two new) and prior actual positive; no native/game')
