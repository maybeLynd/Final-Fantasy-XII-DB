"""Claim-connected upstream CLI refusals and synthetic decoded-record mutations."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;C=P/'controls-01';out=P/'control-result-01.json'
if C.exists() or out.exists():raise RuntimeError('immutable controls exist')
C.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
D=load('current_producer','prove.py');G=load('required_CFG','prove_owner_reload_order.py')
src=json.loads((P/'source-01.json').read_text());ix={int(i['pc'],16):i for q in src['ranges'] for i in q['instructions']}
for n in ['spattack-info-raw-01.json','effective-and-script-id-raw-01.json','spattack-queue-reader-raw-01.json','spattack-output-writers-raw-02.json']:
 r=json.loads((P/'retained/remap'/n).read_text());ix.update({int(i['pc'],16):i for q in r['ranges'] for i in q['instructions']})
baseline=json.loads((P/'result-02.json').read_text())
if baseline.get('producer_complete') is not True or baseline['driver_sha256']!=sha(P/'prove.py') or D.derive(ix,src['tables'],G)!=baseline['facts']:raise RuntimeError('complete actual producer positive missing')
cases=[]
for label in ['missing-capture-receipt','failed-upstream-capture','missing-historical-observations']:
 q=C/label;q.mkdir()
 for f in P.iterdir():
  if f.is_file():shutil.copyfile(f,q/f.name)
 shutil.copytree(P/'retained',q/'retained')
 if label=='missing-capture-receipt':(q/'capture-01.status.json').unlink()
 elif label=='failed-upstream-capture':
  v=json.loads((q/'capture-01.status.json').read_text());v['exit']=2;(q/'capture-01.status.json').write_text(json.dumps(v))
 else:(q/'retained/EXP013/observations.json').unlink()
 started=time.time();r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),str(q/'invalid-result.json')],capture_output=True,timeout=30)
 (q/'stdout').write_bytes(r.stdout);(q/'stderr').write_bytes(r.stderr)
 z=dict(case=label,terminal=True,exit=r.returncode,exception=None,result_exists=(q/'invalid-result.json').exists(),driver_sha256=sha(q/'prove.py'),start=started,end=time.time())
 (q/'status.json').write_text(json.dumps(z,indent=2))
 if r.returncode==0 or z['result_exists'] or not r.stderr:raise RuntimeError('invalid upstream admitted '+label)
 cases.append(z)
mutations=[('float-pop-no-conversion',0x267e42,'mnemonic','mov'),
 ('native-store-narrowed',0x309c13,'args','word ptr [rdx], ax'),
 ('selector-first-argument-changed',0x34888f,'args','edx, eax'),
 ('typed-payload-temporary-changed',0x26804b,'args','dword ptr [rbp - 0xc], ecx')]
synthetic=[]
for label,pc,field,value in mutations:
 bad=copy.deepcopy(ix);before=copy.deepcopy(bad[pc]);bad[pc][field]=value
 try:D.derive(bad,src['tables'],G)
 except (RuntimeError,ValueError) as e:reason=str(e)
 else:raise RuntimeError('relevant decoded mutation admitted '+label)
 synthetic.append(dict(case=label,pc=hex(pc),before=before,after=bad[pc],refused=True,reason=reason,
                       limits='synthetic decoded record, not executed or claimed original bytes'))
z=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),
 actual_positive='result02 complete/current producer exact derive equality',CLI_cases=cases,synthetic_derive_cases=synthetic,
 limits='Three actual prerequisite refusal invocations; four synthetic source-record controls. No new machine-code/emulator/game calls; historical EXP01314 not rerun.')
with out.open('x') as f:json.dump(z,f,indent=2)
print('CONTROLS complete: current producer positive, three actual upstream refusals, four claim-specific synthetic refusals')
