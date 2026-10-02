"""Actual producer prerequisite refusals and labelled static source controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load('producer','prove.py');G=load('reviewed_graph','prove_owner_reload_order.py')
source=json.loads((P/'source-01.json').read_text());expected=json.loads((P/'result-01.json').read_text())
receipt=json.loads((P/'prove-02.status.json').read_text())
if receipt.get('terminal') is not True or receipt.get('exit')!=0 or receipt.get('exception') is not None or receipt['driver_sha256']!=sha(P/'prove.py') or expected.get('producer_complete') is not True or expected['driver_sha256']!=sha(P/'prove.py'):raise ValueError('required positive producer failed/stale')
if json.loads(json.dumps(R.derive(source,G)))!=expected['facts']:raise ValueError('positive original derive differs')
D=P/'controls-01'
if D.exists():raise ValueError('immutable controls directory exists')
D.mkdir()
files=['prove.py','capture.py','capture-index-path.py','validate-title-source-annotations.py','prove_owner_reload_order.py','source-01.json','capture-01.status.json','capture-01.stdout','capture-01.stderr','retained-manifest.stdout','retained-manifest.stderr','retained-manifest.status.json','retained-body-identities.json']
rows=[]
for label in ['missing-capture-receipt','failed-capture-exit','missing-retained-identity']:
 d=D/label;d.mkdir()
 for name in files:shutil.copyfile(P/name,d/name)
 if label=='missing-capture-receipt':(d/'capture-01.status.json').unlink()
 elif label=='failed-capture-exit':
  x=json.loads((d/'capture-01.status.json').read_text());x['exit']=7
  (d/'capture-01.status.json').write_text(json.dumps(x)+'\n')
 else:(d/'retained-manifest.stdout').unlink()
 z=subprocess.run([sys.executable,'-B',str(d/'prove.py'),'must-not-exist.json'],capture_output=True,timeout=45)
 (d/'stdout').write_bytes(z.stdout);(d/'stderr').write_bytes(z.stderr)
 status=dict(terminal=True,exit=z.returncode,exception=None,result_written=(d/'must-not-exist.json').exists(),driver_sha256=sha(d/'prove.py'))
 (d/'status.json').write_text(json.dumps(status,indent=2)+'\n')
 if z.returncode==0 or status['result_written'] or not z.stderr:raise ValueError('invalid prerequisite passed '+label)
 rows.append(dict(case=label,status=status,limits='Actual Python CLI refusal on disposable input; no original FF12 execution'))
mutations=[
 ('post-retargeted-as-free',0x3db37d,'args','0x3db650'),
 ('unhook-writes-actor-free-head',0x3dc233,'args','byte ptr [r9 + 0x60], 0'),
 ('removal-forwards-notification-result',0x3db402,'args','eax, eax'),
 ('notification-function-id-changed',0x3dc115,'args','dword ptr [rsp + 0x24], 0x80000001'),
 ('regression-wrong-entry-address-LEA',0x3dc1d1,'args','r8, [rax + rax*4]')]
synthetic=[]
for label,pc,key,value in mutations:
 x=copy.deepcopy(source)
 i=next(i for r in x['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc)
 before=i[key];i[key]=value
 try:R.derive(x,G)
 except (ValueError,KeyError,RuntimeError) as e:reason=str(e)
 else:raise ValueError('synthetic source mutation passed '+label)
 synthetic.append(dict(case=label,pc=hex(pc),field=key,before=before,after=value,refusal=reason,method='Synthetic annotation mutation of actual derive; no original instruction patch/execution'))
result=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-01.json'),positive='Exact original source derive reproduces all facts',CLI_cases=rows,synthetic_derive_cases=synthetic,limits='Prerequisite/derive controls are producer validation, not independent acceptance or new game/native samples.')
out=P/'control-result-01.json'
if out.exists():raise ValueError('immutable result exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('CONTROLLED actual failed/missing prerequisites and five focused source countermodels; no native/game runs')
