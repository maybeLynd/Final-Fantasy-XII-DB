"""Three bounded actual producer CLI refusals, not FF12 execution."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';D.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-02.status.json').read_text());v=json.loads((P/'result-02.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('actual positive missing')
rows=[]
for name,diag in [('failed-capture','required capture failed'),('missing-source','source-01.json'),('coherent-nonzero-key-initializer','original byte mismatch')]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-02.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 elif name=='missing-source':(q/'source-01.json').unlink()
 else:
  f=q/'source-01.json';x=json.loads(f.read_text());found=0
  for r in x['ranges']:
   for i in r['instructions']:
    if i['pc']=='0x597951':
     if i['bytes']!='894128' or i['args']!='dword ptr [rcx + 0x28], eax':raise RuntimeError('mutation preimage changed')
     i['bytes']='894928';i['args']='dword ptr [rcx + 0x28], ecx';found+=1
   r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
  if found!=1:raise RuntimeError('zero/ambiguous mutation')
  f.write_text(json.dumps(x,indent=2)+'\n')
 argv=[sys.executable,'-B',str(q/'prove.py'),'refused-result.json'];row={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':False,'exit':None,'exception':None}
 try:
  r=subprocess.run(argv,capture_output=True,timeout=25,stdin=subprocess.DEVNULL);(q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
  row.update(terminal=True,exit=r.returncode,diagnostic=diag,diagnostic_matched=diag.encode() in r.stderr,refused_result_absent=not(q/'refused-result.json').exists())
 except Exception as e:row['exception']=repr(e);(q/'stdout.raw').write_bytes(b'');(q/'stderr.raw').write_bytes(repr(e).encode())
 (q/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
 if row['terminal'] is not True or row['exception'] is not None or row['exit']==0 or not row['diagnostic_matched'] or not row['refused_result_absent']:raise RuntimeError('invalid/incomplete refusal '+name)
 rows.append(row)
if len(rows)!=3:raise RuntimeError('incomplete controls')
(P/'control-result-01.json').write_bytes((json.dumps({'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':3,'limits':'Three actual disposable producer CLI refusals plus reused positive. Not original instructions/native/game tests or independent acceptance.'},indent=2)+'\n').encode());print('PASS three actual producer CLI refusals; no game execution')
