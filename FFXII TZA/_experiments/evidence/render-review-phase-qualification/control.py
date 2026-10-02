"""Focused actual-invocation prerequisites and actual derive() discriminators."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('missing checked actual positive')
def load(n,f):
 sp=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('producer','prove.py');G=load('graph','prove_owner_reload_order.py');ix={}
for name in ['render-slot-identity-publication','render-clear-callee-footprints','render-removal-phase-contracts']:
 for r in json.loads((P/(name+'-source-01.json')).read_text())['ranges']:ix.update({int(i['pc'],16):i for i in r['instructions']})
if M.derive(ix,G)!=v['facts']:raise RuntimeError('control uses a different semantic path')
rules=[]
for name,pc,change,diag in [
 ('pending-tail-before-ID',0x427a47,('args','word ptr [rdi], si'),'required reviewed phase operation changed'),
 ('scalar-is-four-bytes',0x6c0526,('size',16),'scalar store width/class changed'),
 ('returned-helper-object-width',0x4291a9,('size',8),'reviewed phase width/role changed'),
 ('postclear-poolflag',0x427db3,('args','dword ptr [rdi + 0x48818], 0'),'required reviewed phase operation changed'),
 ('same-pool-source-root',0x429146,('rip_target','0x22c6f30'),'shared pool root changed')]:
 q=copy.deepcopy(ix);field,value=change
 if field=='args':q[pc][field]=value
 else:q[pc]['memory'][0][field]=value
 try:M.derive(q,G)
 except RuntimeError as e:
  if diag not in str(e):raise RuntimeError('wrong focused refusal '+name+':'+str(e))
  rules.append({'name':name,'pc':hex(pc),'synthetic_change':change,'refused':True,'diagnostic':str(e)})
 else:raise RuntimeError('focused rule accepted counterexample '+name)
D.mkdir(exist_ok=False);rows=[]
review='fable-render-removal-phase-contracts-REVIEW.md'
for name,diag,removed in [('failed-parent-producer','required parent invocation failed',[]),('missing-parent-result','result-01.json',['parents/render-removal-phase-contracts/result-01.json']),('missing-returned-review',review,[review])]:
 q=D/name;q.mkdir()
 for f in P.iterdir():
  if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
  if f.is_dir():shutil.copytree(f,q/f.name)
  else:shutil.copy2(f,q/f.name)
 if name=='failed-parent-producer':
  f=q/'parents/render-removal-phase-contracts/prove-01.status.json';x=json.loads(f.read_text());x['exit']=1;f.write_text(json.dumps(x)+'\n')
 for f in removed:(q/f).unlink()
 argv=[sys.executable,'-B',str(q/'prove.py'),'control-output.json'];z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=120)
 (q/'case.stdout').write_bytes(z.stdout);(q/'case.stderr').write_bytes(z.stderr)
 r={'name':name,'argv':argv,'driver_sha256':sha(q/'prove.py'),'terminal':True,'exit':z.returncode,'exception':None,'diagnostic_matched':diag in z.stderr.decode(errors='replace'),'refused_result_absent':not(q/'control-output.json').exists(),'explicit_removed_base_files':removed}
 if not r['exit'] or not r['diagnostic_matched'] or not r['refused_result_absent']:raise RuntimeError('failed actual CLI refusal '+name)
 (q/'case.status.json').write_text(json.dumps(r,indent=2)+'\n');rows.append(r)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),'actual_CLI_refusals':rows,'CLI_count':len(rows),'synthetic_derive_controls':rules,'derive_count':len(rules),'limits':'Three actual producer CLI prerequisite refusals and five synthetic mutations of the exact derive() used by the checked original-byte producer. No patched-EXE, native, emulator or FF12 executions; external reviewer runs not counted.'}
(P/'control-result-01.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS actual prerequisite refusals and discriminating phase/width/effect derive controls')
