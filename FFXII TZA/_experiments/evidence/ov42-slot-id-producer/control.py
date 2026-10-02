"""Focused real prerequisite failures and labelled slot-gate countermodels."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load('producer','prove.py');G=load('cfg','prove_owner_reload_order.py');old=json.loads((P/'retained/slot-action-id-raw-01.json').read_text());tail=json.loads((P/'source-tail-01.json').read_text());positive=json.loads((P/'result-01.json').read_text());s=json.loads((P/'prove-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or positive.get('producer_complete') is not True or positive['driver_sha256']!=sha(P/'prove.py') or json.loads(json.dumps(R.derive(old,tail,G)))!=positive['facts']:raise ValueError('positive producer prerequisite incomplete/different')
D=P/'controls-01'
if D.exists():raise ValueError('immutable control directory exists')
D.mkdir();cli=[]
for label in ['missing-capture-status','failed-capture-exit','missing-retained-source']:
 d=D/label;d.mkdir()
 for q in P.iterdir():
  if q.is_file():shutil.copyfile(q,d/q.name)
 shutil.copytree(P/'retained',d/'retained')
 if label=='missing-capture-status':(d/'capture-01.status.json').unlink()
 elif label=='failed-capture-exit':
  x=json.loads((d/'capture-01.status.json').read_text());x['exit']=7;(d/'capture-01.status.json').write_text(json.dumps(x)+'\n')
 else:(d/'retained/slot-action-id-raw-01.json').unlink()
 z=subprocess.run([sys.executable,'-B',str(d/'prove.py'),'must-not-exist.json'],capture_output=True,timeout=30)
 (d/'stdout').write_bytes(z.stdout);(d/'stderr').write_bytes(z.stderr)
 st=dict(terminal=True,exit=z.returncode,exception=None,result_written=(d/'must-not-exist.json').exists(),driver_sha256=sha(d/'prove.py'));(d/'status.json').write_bytes((json.dumps(st,indent=2)+'\n').encode())
 if z.returncode==0 or st['result_written'] or not z.stderr:raise ValueError('actual invalid prerequisite accepted '+label)
 cli.append(dict(case=label,status=st))
synthetic=[]
for label,pc,key,value in [
 ('wrong-scan-step',0x30d0b1,'mnemonic','dec'),('wrong-slot-stride',0x30d09e,'args','r9, 5'),('wrong-free-sentinel',0x30d07f,'args','ecx, 0xfffe'),
 ('stores-identity-instead-of-action',0x30d14f,'args','word ptr [rcx + 0x1c], r11w'),('capacity-bound-off-by-one',0x30d0b4,'args','r8b, 0x21'),
 ('wrapper-forwards-identity-as-action',0x30d04c,'args','edx, esi'),('missing-post-call-unit-binding',0x30d056,'args','byte ptr [rdi + 5], al')]:
 x,y=copy.deepcopy(old),copy.deepcopy(tail);i=next(i for v in [x,y] for r in v['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc);before=i[key];i[key]=value
 try:R.derive(x,y,G)
 except(ValueError,KeyError,RuntimeError) as e:reason=str(e)
 else:raise ValueError('static mutation accepted '+label)
 synthetic.append(dict(case=label,pc=hex(pc),field=key,before=before,after=value,refusal=reason,limits='Synthetic annotation derive control, no FF12 code patch/execution'))
out=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-01.json'),CLI_cases=cli,synthetic_source_cases=synthetic,limits='Producer invocation controls and original-source analytical mutations, not independent acceptance, native execution or natural reachability.')
(P/'control-result-01.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print('CONTROLLED three actual prerequisite refusals/seven source changes; capacity/value-transfer proof validated')
