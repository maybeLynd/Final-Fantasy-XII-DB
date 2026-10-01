"""Actual producer CLI prerequisite/mutation controls; not original-code execution."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((P/'proof-02.status.json').read_text());positive=json.loads((P/'result-02.json').read_text())
if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(P/'prove.py') or positive.get('producer_complete') is not True or positive['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing valid actual positive')
import ast
# Regression against the actual formerly-late gate, not helper presence.
def gate_order(f):
 tree=ast.parse(f.read_text());gates=[];outputs=[]
 for n in tree.body:
  if isinstance(n,ast.If) and "y.get('wrapper_complete')" in ast.unparse(n.test):gates.append(n.lineno)
  if isinstance(n,ast.Expr):
   for q in ast.walk(n):
    if isinstance(q,ast.Call) and isinstance(q.func,ast.Attribute) and isinstance(q.func.value,ast.Name) and q.func.value.id=='out' and q.func.attr=='write_text':outputs.append(n.lineno)
 if len(gates)!=1 or len(outputs)!=1:raise RuntimeError('missing/ambiguous concrete gate/output')
 return {'driver_sha256':sha(f),'gate_line':gates[0],'output_line':outputs[0],'gate_before_output':gates[0]<outputs[0]}
order={'old':gate_order(P/'prove-01-driver.py'),'current':gate_order(P/'prove.py'),'method':'Static AST concrete producer invocation ordering; not native execution'}
if order['old']['gate_before_output'] or not order['current']['gate_before_output']:raise RuntimeError('producer-order regression not discriminating')
rows=[]
for name,diag in [('failed-capture','required capture status failed'),('missing-source','source-01.json'),('coherent-skeletonref-store-mutation','original byte mismatch')]:
 q=D/name;q.mkdir()
 for s in P.iterdir():
  if s.name in ['controls-01','result-02.json','__pycache__'] or s.name.startswith('control-'):continue
  if s.is_dir():shutil.copytree(s,q/s.name)
  elif s.is_file():shutil.copy2(s,q/s.name)
 if name=='failed-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 elif name=='missing-source':(q/'source-01.json').unlink()
 else:
  f=q/'source-01.json';x=json.loads(f.read_text());found=0
  for rr in x['ranges']:
   for i in rr['instructions']:
    if i['pc']=='0x3729a9':
     assert i['bytes']=='898694000000' and i['args']=='dword ptr [rsi + 0x94], eax';i['bytes']='898698000000';i['args']='dword ptr [rsi + 0x98], eax';i['memory'][0]['displacement']=0x98;found+=1
   rr['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in rr['instructions']))).hexdigest()
  assert found==1;f.write_text(json.dumps(x,indent=2)+'\n')
 r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),'refused-result.json'],capture_output=True,timeout=20)
 (q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
 row={'name':name,'exit':r.returncode,'diagnostic':diag,'diagnostic_matched':diag.encode() in r.stderr,'refused_result_absent':not(q/'refused-result.json').exists(),'driver_sha256':sha(q/'prove.py'),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'terminal':True,'exception':None}
 (q/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
 if r.returncode==0 or not row['diagnostic_matched'] or not row['refused_result_absent']:raise RuntimeError('control not discriminating '+name)
 rows.append(row)
result={'producer_complete':True,'source_order_control':order,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':len(rows),'limits':'Disposable CLI evidence mutations only; no FF12 native/game, no original-code execution or live observation'}
if len(rows)!=3:raise RuntimeError('incomplete/zero controls')
(P/'control-result-01.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS three actual cause-specific refusals and prior actual positive; no native/game')
