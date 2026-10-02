"""Focused original-source prerequisites and exact output/guard mutations."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;C=P/'controls-01';O=P/'control-result-01.json'
if C.exists() or O.exists():raise RuntimeError('immutable controls exist')
C.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
D=load('producer','prove.py');G=load('required_CFG','prove_owner_reload_order.py')
ix={}
for n in ['spattack-queue-reader-raw-01.json','spattack-info-raw-01.json']:
 r=json.loads((P/n).read_text());ix.update({int(i['pc'],16):i for q in r['ranges'] for i in q['instructions']})
base=json.loads((P/'result-01.json').read_text())
if base.get('producer_complete') is not True or base['driver_sha256']!=sha(P/'prove.py') or D.derive(ix,G)!=base['facts']:raise RuntimeError('required complete producer positive missing')
cli=[]
for label in ['missing-queue-source','coherently-repinned-output-width']:
 q=C/label;q.mkdir()
 for p in P.iterdir():
  if p.is_file():shutil.copyfile(p,q/p.name)
 if label=='missing-queue-source':(q/'spattack-queue-reader-raw-01.json').unlink()
 else:
  p=q/'spattack-queue-reader-raw-01.json';r=json.loads(p.read_text());i=next(i for x in r['ranges'] for i in x['instructions'] if i['pc']=='0x309c13');i['memory'][0]['size']=2;p.write_text(json.dumps(r))
  p=q/'input-identities-01.json';r=json.loads(p.read_text());next(x for x in r['inputs'] if x['path']=='spattack-queue-reader-raw-01.json')['sha256']=sha(q/'spattack-queue-reader-raw-01.json');p.write_text(json.dumps(r))
 r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),str(q/'invalid.json')],capture_output=True,timeout=30)
 (q/'stdout').write_bytes(r.stdout);(q/'stderr').write_bytes(r.stderr)
 z=dict(case=label,terminal=True,exit=r.returncode,exception=None,result_exists=(q/'invalid.json').exists());(q/'status.json').write_text(json.dumps(z,indent=2))
 if r.returncode==0 or z['result_exists'] or not r.stderr:raise RuntimeError('invalid actual prerequisite accepted')
 cli.append(z)
synthetic=[]
for label,pc,field,value in [('action-output-retargeted',0x309c13,'args','dword ptr [rcx], eax'),('null-guard-reversed',0x309c18,'mnemonic','jne'),('bridge-output-read-removed',0x3483a9,'args','ecx, ebx')]:
 bad=copy.deepcopy(ix);before=copy.deepcopy(bad[pc]);bad[pc][field]=value
 try:D.derive(bad,G)
 except (RuntimeError,ValueError) as e:reason=str(e)
 else:raise RuntimeError('semantic mutation admitted')
 synthetic.append(dict(case=label,pc=hex(pc),before=before,after=bad[pc],refused=True,reason=reason,limits='synthetic decoded-record mutation, not original code or execution'))
z=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive='exact actual producer facts/current driver equality',CLI_cases=cli,synthetic_derive_cases=synthetic,limits='two actual prerequisite refusals/three synthetic source mutations; no new capture or original-code/native/live executions')
with O.open('x') as f:json.dump(z,f,indent=2)
print('CONTROLS complete: retained-source positive, missing/repinned-width refusals, three claim-specific synthetic mutations')
