"""Concrete producer prerequisite and shipping-byte refusal controls. No FF12 execution."""
import ast,hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing checked actual positive')
tree=ast.parse((P/'prove.py').read_text());gates=[];outputs=[]
for n in tree.body:
 if isinstance(n,ast.If) and any(t in ast.unparse(n.test) for t in ["status.get('terminal')","x.get('wrapper_complete')","y.get('wrapper_complete')","codec_status.get('terminal')","z.get('wrapper_complete')"]):gates.append(n.lineno)
 if isinstance(n,ast.Expr):
  for q in ast.walk(n):
   if isinstance(q,ast.Call) and isinstance(q.func,ast.Attribute) and isinstance(q.func.value,ast.Name) and q.func.value.id=='out' and q.func.attr=='write_bytes':outputs.append(n.lineno)
if len(gates)!=5 or len(outputs)!=1 or max(gates)>=outputs[0]:raise RuntimeError('concrete prerequisite ordering failed')
rows=[]
for name,diag in [('failed-capture','required capture status failed'),('incomplete-capture-wrapper','actual capture incomplete'),('missing-source','source-01.json'),('coherent-failure-read-mutation','original byte mismatch')]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_bytes((json.dumps(x)+'\n').encode())
 elif name=='incomplete-capture-wrapper':
  f=q/'source-01.json';x=json.loads(f.read_text());x['wrapper_complete']=False;f.write_bytes((json.dumps(x)+'\n').encode())
 elif name=='missing-source':(q/'source-01.json').unlink()
 else:
  f=q/'source-01.json';x=json.loads(f.read_text());found=0
  for r in x['ranges']:
   for i in r['instructions']:
    if i['pc']=='0x41f595':
     if i['bytes']!='8b4e04' or i['args']!='ecx, dword ptr [rsi + 4]':raise RuntimeError('mutation preimage changed')
     i['bytes']='8b4e08';i['args']='ecx, dword ptr [rsi + 8]';i['memory'][0]['displacement']=8;found+=1
   r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
  if found!=1:raise RuntimeError('zero/ambiguous mutation')
  f.write_bytes((json.dumps(x,indent=2)+'\n').encode())
 argv=[sys.executable,'-B',str(q/'prove.py'),'refused-result.json']
 receipt={'name':name,'argv':argv,'terminal':False,'exit':None,'exception':None,'driver_sha256':sha(q/'prove.py')}
 try:
  r=subprocess.run(argv,capture_output=True,timeout=25,stdin=subprocess.DEVNULL)
  (q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
  receipt.update(terminal=True,exit=r.returncode,diagnostic=diag,diagnostic_matched=diag.encode() in r.stderr,refused_result_absent=not(q/'refused-result.json').exists(),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest())
 except Exception as e:
  receipt['exception']=repr(e);(q/'stdout.raw').write_bytes(b'');(q/'stderr.raw').write_bytes(repr(e).encode())
 (q/'receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
 if receipt['terminal'] is not True or receipt['exception'] is not None or receipt['exit']==0 or not receipt['diagnostic_matched'] or not receipt['refused_result_absent']:raise RuntimeError('invalid/incomplete refusal '+name)
 rows.append(receipt)
if len(rows)!=4:raise RuntimeError('incomplete/zero controls')
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),
 'source_order_control':{'driver_sha256':sha(P/'prove.py'),'gate_lines':gates,'output_line':outputs[0],'gate_before_output':True,'method':'Static AST actual producer path, not helper existence'},
 'cases':rows,'count':len(rows),'limits':'Four actual disposable producer CLI refusals plus checked positive. Not original-code/native/live execution, fault sampling or independent project acceptance.'}
(P/'control-result-01.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS four actual producer refusals and upstream-before-output control; no FF12 execution')
