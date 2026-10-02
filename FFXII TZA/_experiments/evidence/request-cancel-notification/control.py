"""Focused real invocation prerequisites and cancel-specific source controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load('cancel_producer','prove.py');G=load('cfg','prove_owner_reload_order.py')
x=json.loads((P/'source-01.json').read_text());parent=json.loads((P/'retained/source-01.json').read_text());r=json.loads((P/'result-01.json').read_text());s=json.loads((P/'prove-02.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or r.get('producer_complete') is not True or r['driver_sha256']!=sha(P/'prove.py'):raise ValueError('required positive producer failed')
if json.loads(json.dumps(R.derive(x,parent,G)))!=r['facts']:raise ValueError('positive source derive differs')
D=P/'controls-01'
if D.exists():raise ValueError('immutable controls directory exists')
D.mkdir();rows=[]
files=['prove.py','capture.py','capture-index-path.py','validate-title-source-annotations.py','prove_owner_reload_order.py','source-01.json','capture-01.status.json','capture-01.stdout','capture-01.stderr','parent-identities.json']
for label in ['missing-capture-status','failed-capture-exit','truncated-first-unwind-fragment','missing-retained-source']:
 d=D/label;d.mkdir()
 for n in files:shutil.copyfile(P/n,d/n)
 shutil.copytree(P/'retained',d/'retained')
 if label=='missing-capture-status':(d/'capture-01.status.json').unlink()
 elif label=='failed-capture-exit':
  z=json.loads((d/'capture-01.status.json').read_text());z['exit']=7
  (d/'capture-01.status.json').write_text(json.dumps(z)+'\n')
 elif label=='missing-retained-source':(d/'retained/source-01.json').unlink()
 else:
  z=copy.deepcopy(x);q=z['ranges'][2]
  q['instructions']=[i for i in q['instructions'] if int(i['pc'],16)<0x3db43c]
  blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
  if len(blob)!=28:raise ValueError('first-unwind-fragment control not exact28B')
  q['end_exclusive']='0x3db43c';q['sha256']=hashlib.sha256(blob).hexdigest()
  (d/'source-01.json').write_text(json.dumps(z)+'\n')
 z=subprocess.run([sys.executable,'-B',str(d/'prove.py'),'must-not-exist.json'],capture_output=True,timeout=45)
 (d/'stdout').write_bytes(z.stdout);(d/'stderr').write_bytes(z.stderr)
 status=dict(terminal=True,exit=z.returncode,exception=None,driver_sha256=sha(d/'prove.py'),result_written=(d/'must-not-exist.json').exists())
 (d/'status.json').write_text(json.dumps(status,indent=2)+'\n')
 if z.returncode==0 or status['result_written'] or not z.stderr:raise ValueError('invalid prerequisite passed '+label)
 rows.append(dict(case=label,status=status,limits='Actual Python CLI disposable control, no original FF12 execution'))
mutants=[('wrong-native-mode',0x352991,'args','r8d, 1'),('wrong-mode4-normalization',0x3db484,'mnemonic','cmove'),('only-state3-admission',0x3db4ca,'mnemonic','cmp'),('same-channel-after-removal',0x3db50d,'args','rsi'),('return-false',0x3db51a,'args','eax, 0')]
synthetic=[]
for label,pc,key,value in mutants:
 z=copy.deepcopy(x);i=next(i for q in z['ranges'] for i in q['instructions'] if int(i['pc'],16)==pc);before=i[key];i[key]=value
 try:R.derive(z,parent,G)
 except (ValueError,KeyError,RuntimeError) as e:reason=str(e)
 else:raise ValueError('source countermodel passed '+label)
 synthetic.append(dict(case=label,pc=hex(pc),field=key,before=before,after=value,refusal=reason,method='Synthetic annotation mutation on actual derive, not original code execution'))
# Causal extent control reaches the actual graph helper, not just fixed metadata.
z=copy.deepcopy(x);q=z['ranges'][2];q['instructions']=[i for i in q['instructions'] if int(i['pc'],16)<0x3db43c];q['end_exclusive']='0x3db43c'
try:R.derive(z,parent,G)
except ValueError as e:reason=str(e)
else:raise ValueError('first-unwind-fragment CFG falsely complete')
if 'unclosed local CFG' not in reason:raise ValueError('extent regression did not reach actual CFG helper')
synthetic.append(dict(case='first-fragment-actual-CFG',refusal=reason,method='Synthetic truncated source passed to actual derive/CFG; no FF12 execution'))
out=P/'control-result-01.json'
if out.exists():raise ValueError('immutable result exists')
out.write_bytes((json.dumps(dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-01.json'),positive='Exact derive reproduces all original facts',CLI_cases=rows,synthetic_derive_cases=synthetic,limits='Producer controls, not independent acceptance or runtime samples.'),indent=2)+'\n').encode())
print('CONTROLLED four actual CLI prerequisites and six focused source/CFG refusals; no game/native execution')
