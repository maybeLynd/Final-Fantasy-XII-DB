"""Getter-source prerequisites plus the actual Read effect checker controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-02.status.json').read_text());v=json.loads((P/'result-02.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing checked actual positive')
def load(n,f):
 sp=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('producer','prove.py');G=load('graph','prove_owner_reload_order.py');R=load('retained_predicate','retained-open/prove.py')
x=json.loads((P/'source-01.json').read_text());ix={int(i['pc'],16):i for i in x['ranges'][0]['instructions']}
y=json.loads((P/'retained-open/source-01.json').read_text());predicate=R.getter({int(i['pc'],16):i for i in y['ranges'][0]['instructions']},G)
if json.loads(json.dumps(M.derive(ix,G,predicate)))!={k:q for k,q in v['facts'].items() if k!='shipping_read_import'}:raise RuntimeError('controls target a different actual effect path')
checks=[]
for name,pc,key,value,diag in [('requested-bytecount-guard',0x59d4d1,'mnemonic','jne','Read source operation changed'),('fullQWORD-buffer-read',0x59d4b4,'size',4,'Read field/count width or role changed'),('signed-nonpositive-cache-skip',0x59d500,'mnemonic','jl','Read source operation changed'),('API-return-replaced-by-count',0x59d4f0,'args','eax, 1','Read source operation changed')]:
 q=copy.deepcopy(ix)
 if key=='size':q[pc]['memory'][0][key]=value
 else:q[pc][key]=value
 try:M.derive(q,G,predicate)
 except RuntimeError as e:
  if diag not in str(e):raise RuntimeError('wrong focused refusal '+name)
  checks.append({'name':name,'pc':hex(pc),'synthetic_change':{key:value},'refused':True,'diagnostic':str(e)})
 else:raise RuntimeError('effect change accepted '+name)
import ast
old=json.loads((P/'result-01.json').read_text())
if any(old[k]!=v[k] for k in ['facts','source_pins','exe_sha256','method','new_original_bytes']):raise RuntimeError('metadata correction changed scientific result')
a=ast.parse((P/'prove-before-Read-metadata-01.py').read_text());b=ast.parse((P/'prove.py').read_text())
functions=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ['derive','import_declaration']}
if functions(a)!=functions(b):raise RuntimeError('scientific derivation changed during metadata correction')
if 'AL-only returns, not fullRAX' in ' '.join(v['limits']) or len(v['facts']['source_partitions'])!=5 or v['facts']['zero_view_read_witness']['Read_fullRAX']!=0:raise RuntimeError('corrected Read contract inconsistent')
D.mkdir(exist_ok=False);rows=[]
for name,diag,removed in [('failed-Read-capture','required Read capture failed',[]),('missing-retained-predicate-result','result-01.json',['retained-open/result-01.json']),('missing-Read-source','source-01.json',['source-01.json'])]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json','result-02.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-Read-capture':
  f=q/'capture-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 for f in removed:(q/f).unlink()
 argv=[sys.executable,'-B',str(q/'prove.py'),'control-output.json'];z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=120)
 (q/'case.stdout').write_bytes(z.stdout);(q/'case.stderr').write_bytes(z.stderr)
 r={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':True,'exit':z.returncode,'exception':None,'diagnostic_matched':diag in z.stderr.decode(errors='replace'),'refused_result_absent':not(q/'control-output.json').exists(),'explicit_removed_base_files':removed}
 if not r['exit'] or not r['diagnostic_matched'] or not r['refused_result_absent']:raise RuntimeError('actual CLI refusal failed '+name)
 (q/'case.status.json').write_text(json.dumps(r,indent=2)+'\n');rows.append(r)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'cases':rows,'count':len(rows),'metadata_correction_control':'Exact derive/import AST and scientific facts/sourcepins unchanged; metadata corrected before publication','predicate_controls':checks,'predicate_count':len(checks),'limits':'Three actual producer CLI prerequisite refusals and four synthetic mutations of actual Close derive checker. Original Read logical partitions are mathematical analysis, not machine-code/native/emulated/live executions or parent independent acceptance.'}
(P/'control-result-01.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS checked CLI prerequisite refusals and bytecount/width/cacheguard/API-count controls')
