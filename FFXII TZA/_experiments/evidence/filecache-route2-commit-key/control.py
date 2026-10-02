"""Focused actual CLI prerequisite/identity refusals, not FF12 executions."""
import ast,hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-02.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('actual positive prerequisite missing')
tree=ast.parse((P/'prove.py').read_text());gates=[];outputs=[]
for n in ast.walk(tree):
 if isinstance(n,ast.If) and any(q in ast.unparse(n.test) for q in ["s.get('terminal')","x.get('wrapper_complete')","t.get('terminal')"]):gates.append(n.lineno)
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='out' and n.func.attr=='write_bytes':outputs.append(n.lineno)
if len(gates)!=4 or len(outputs)!=1 or max(gates)>=outputs[0]:raise RuntimeError('concrete prerequisite ordering changed')
cases=[('failed-new-capture','required capture failed'),('partial-new-wrapper','actual capture incomplete'),('missing-retained-wrapper','filecache-key-boundaries-source-02.json'),('coherent-failed-retained-producer','required retained producer failed'),('coherent-failed-legacy-hash-receipt','legacy hash receipt changed or failed'),('coherent-empty-branch-mutation','original byte mismatch')]
rows=[]
for name,diag in cases:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-new-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 elif name=='partial-new-wrapper':
  f=q/'source-01.json';x=json.loads(f.read_text());x['wrapper_complete']=False;f.write_text(json.dumps(x)+'\n')
 elif name=='missing-retained-wrapper':(q/'retained/filecache-key-boundaries-source-02.json').unlink()
 elif name.startswith('coherent-failed-'):
  n='filecache-key-preprocessing-positive-02.status.json' if name=='coherent-failed-retained-producer' else 'filecache-hash-loop-capture-01.status.json'
  f=q/'retained'/n;x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
  f=q/'retained/manifest.json';x=json.loads(f.read_text())
  for r in x['members']:
   if r['path']==n:r.update(sha256=sha(q/'retained'/n),bytes=(q/'retained'/n).stat().st_size)
  f.write_text(json.dumps(x,indent=2)+'\n')
  f=q/'retained-identities.json';x=json.loads(f.read_text())
  for r in x['files']:
   if r['snapshot'] in ['manifest.json',n]:r['sha256']=sha(q/'retained'/r['snapshot'])
  f.write_text(json.dumps(x,indent=2)+'\n')
 else:
  f=q/'source-01.json';x=json.loads(f.read_text());found=0
  for r in x['ranges']:
   for i in r['instructions']:
    if i['pc']=='0x20c21d':
     if not i['bytes'].startswith('0f84') or i['mnemonic']!='je':raise RuntimeError('mutation preimage changed')
     i['bytes']='0f85'+i['bytes'][4:];i['mnemonic']='jne';found+=1
   r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
  if found!=1:raise RuntimeError('zero/ambiguous mutation')
  f.write_text(json.dumps(x,indent=2)+'\n')
 argv=[sys.executable,'-B',str(q/'prove.py'),'refused-result.json']
 row={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':False,'exit':None,'exception':None}
 try:
  r=subprocess.run(argv,capture_output=True,timeout=25,stdin=subprocess.DEVNULL)
  (q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
  row.update(terminal=True,exit=r.returncode,diagnostic=diag,diagnostic_matched=diag.encode() in r.stderr,refused_result_absent=not(q/'refused-result.json').exists(),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest())
 except Exception as e:
  row['exception']=repr(e);(q/'stdout.raw').write_bytes(b'');(q/'stderr.raw').write_bytes(repr(e).encode())
 (q/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
 if row['terminal'] is not True or row['exception'] is not None or row['exit']==0 or not row['diagnostic_matched'] or not row['refused_result_absent']:raise RuntimeError('invalid/incomplete refusal '+name)
 rows.append(row)
if len(rows)!=6:raise RuntimeError('incomplete controls')
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'source_order_control':{'gate_lines':gates,'output_line':outputs[0],'gate_before_output':True,'limits':'Actual CLI gates exercised as well; static order alone not acceptance'},'cases':rows,'count':len(rows),'limits':'Six disposable producer CLI refusals and one reused positive; not six FF12 runs, independent review or new native execution.'}
(P/'control-result-01.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS six actual bounded CLI refusals; no FF12 execution')
