"""Getter-source prerequisites plus the actual Close effect checker controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing checked actual positive')
def load(n,f):
 sp=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('producer','prove.py');G=load('graph','prove_owner_reload_order.py');R=load('retained_predicate','retained-open/prove.py')
x=json.loads((P/'source-01.json').read_text());ix={int(i['pc'],16):i for i in x['ranges'][0]['instructions']}
y=json.loads((P/'retained-open/source-01.json').read_text());predicate=R.getter({int(i['pc'],16):i for i in y['ranges'][0]['instructions']},G)
if M.derive(ix,G,predicate)!=v['facts']:raise RuntimeError('controls target a different actual effect path')
checks=[]
for name,pc,key,value,diag in [('signed-nonpositive-not-zero-only',0x59bd66,'mnemonic','je','Close phase changed'),('cache-reset-fullQWORD',0x59bd70,'size',4,'Close backing width/role changed'),('Close-AL-not-EAX',0x59bd78,'args','eax, 1','Close phase changed'),('skip-release-also-skips-reset',0x59bd66,'args','0x59bd70','Close phase changed')]:
 q=copy.deepcopy(ix)
 if key=='size':q[pc]['memory'][0][key]=value
 else:q[pc][key]=value
 try:M.derive(q,G,predicate)
 except RuntimeError as e:
  if diag not in str(e):raise RuntimeError('wrong focused refusal '+name)
  checks.append({'name':name,'pc':hex(pc),'synthetic_change':{key:value},'refused':True,'diagnostic':str(e)})
 else:raise RuntimeError('effect change accepted '+name)
D.mkdir(exist_ok=False);rows=[]
for name,diag,removed in [('failed-Close-capture','required Close capture failed',[]),('missing-retained-predicate-result','result-01.json',['retained-open/result-01.json']),('missing-Close-source','source-01.json',['source-01.json'])]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-Close-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 for f in removed:(q/f).unlink()
 argv=[sys.executable,'-B',str(q/'prove.py'),'control-output.json'];z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=120)
 (q/'case.stdout').write_bytes(z.stdout);(q/'case.stderr').write_bytes(z.stderr)
 r={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':True,'exit':z.returncode,'exception':None,'diagnostic_matched':diag in z.stderr.decode(errors='replace'),'refused_result_absent':not(q/'control-output.json').exists(),'explicit_removed_base_files':removed}
 if not r['exit'] or not r['diagnostic_matched'] or not r['refused_result_absent']:raise RuntimeError('actual CLI refusal failed '+name)
 (q/'case.status.json').write_text(json.dumps(r,indent=2)+'\n');rows.append(r)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':len(rows),'predicate_controls':checks,'predicate_count':len(checks),'limits':'Three actual producer CLI prerequisite refusals and four synthetic mutations of actual Close derive checker. Original Close logical partitions are mathematical analysis, not machine-code/native/emulated/live executions or parent independent acceptance.'}
(P/'control-result-01.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS checked CLI prerequisite refusals and signedguard/width/skip-reset/return-byte controls')
