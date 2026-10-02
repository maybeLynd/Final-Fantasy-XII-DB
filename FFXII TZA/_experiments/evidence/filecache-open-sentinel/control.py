"""Getter-source prerequisites plus the actual predicate checker controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing checked actual positive')
def load(n,f):
 sp=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('producer','prove.py');G=load('graph','prove_owner_reload_order.py');x=json.loads((P/'source-01.json').read_text());ix={int(i['pc'],16):i for i in x['ranges'][0]['instructions']}
base=M.getter(ix,G)
if base!={k:q for k,q in v['facts'].items() if k!='conditional_composition'}:raise RuntimeError('predicate controls target a different path')
checks=[]
for name,pc,key,value,diag in [('zero-versus-allones-sentinel',0x59d92e,'args','qword ptr [rcx + 0x40], 0','getter predicate changed'),('full64-bit-comparison',0x59d92e,'size',4,'getter predicate width/role changed'),('inequality-branch-polarity',0x59d933,'mnemonic','je','getter predicate changed'),('AL-versus-full-EAX',0x59d938,'args','eax, 1','getter predicate changed')]:
 q=copy.deepcopy(ix)
 if key=='size':q[pc]['memory'][0][key]=value
 else:q[pc][key]=value
 try:M.getter(q,G)
 except RuntimeError as e:
  if diag not in str(e):raise RuntimeError('wrong predicate refusal '+name)
  checks.append({'name':name,'pc':hex(pc),'synthetic_change':{key:value},'refused':True,'diagnostic':str(e)})
 else:raise RuntimeError('predicate change accepted '+name)
D.mkdir(exist_ok=False);rows=[]
for name,diag,removed in [('failed-getter-capture','required getter capture failed',[]),('missing-retained-zero-result','result-01.json',['parents/filecache-zero-handle-return/result-01.json']),('missing-getter-source','source-01.json',['source-01.json'])]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-getter-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 for f in removed:(q/f).unlink()
 argv=[sys.executable,'-B',str(q/'prove.py'),'control-output.json'];z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=120)
 (q/'case.stdout').write_bytes(z.stdout);(q/'case.stderr').write_bytes(z.stderr)
 r={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':True,'exit':z.returncode,'exception':None,'diagnostic_matched':diag in z.stderr.decode(errors='replace'),'refused_result_absent':not(q/'control-output.json').exists(),'explicit_removed_base_files':removed}
 if not r['exit'] or not r['diagnostic_matched'] or not r['refused_result_absent']:raise RuntimeError('actual CLI refusal failed '+name)
 (q/'case.status.json').write_text(json.dumps(r,indent=2)+'\n');rows.append(r)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':len(rows),'predicate_controls':checks,'predicate_count':len(checks),'limits':'Three actual producer CLI prerequisite refusals and four synthetic mutations of actual getter checker. Original predicate equality partitions are mathematical analysis, not machine-code/native/emulated/live executions or parent independent acceptance.'}
(P/'control-result-01.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS checked CLI prerequisite refusals and sentinel/width/branch/return-byte controls')
