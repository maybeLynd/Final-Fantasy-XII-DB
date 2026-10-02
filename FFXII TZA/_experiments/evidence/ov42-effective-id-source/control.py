"""Check actual prerequisite failures and source-bound ID/owner discriminators."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load('producer','prove.py');G=load('cfg','prove_owner_reload_order.py');R.receipt('prove-01','prove.py')
sources=[json.loads((P/n).read_text()) for n in ['source-01.json','source-owner-01.json','retained-callers-01.json']];positive=json.loads((P/'result-01.json').read_text())
if positive.get('producer_complete') is not True or positive['driver_sha256']!=sha(P/'prove.py') or json.loads(json.dumps(R.derive(*sources,G)))!=positive['facts']:raise ValueError('positive original derive incomplete/different')
D=P/'controls-01'
if D.exists():raise ValueError('immutable controls exist')
D.mkdir();cli=[]
for label in ['failed-feasibility-with-output-present','missing-feasibility-status','failed-capture-exit','missing-owner-source']:
 d=D/label;d.mkdir()
 for p in P.iterdir():
  if p.is_file():shutil.copyfile(p,d/p.name)
 if label=='failed-feasibility-with-output-present':
  x=json.loads((d/'feasibility-01.status.json').read_text());x['exit']=7;(d/'feasibility-01.status.json').write_text(json.dumps(x)+'\n')
  if not(d/'feasibility-01.json').is_file():raise ValueError('required apparent output absent from failure fixture')
 elif label=='missing-feasibility-status':(d/'feasibility-01.status.json').unlink()
 elif label=='failed-capture-exit':
  x=json.loads((d/'capture-01.status.json').read_text());x['exit']=7;(d/'capture-01.status.json').write_text(json.dumps(x)+'\n')
 else:(d/'source-owner-01.json').unlink()
 z=subprocess.run([sys.executable,'-B',str(d/'prove.py'),'must-not-exist.json'],capture_output=True,timeout=35)
 (d/'stdout').write_bytes(z.stdout);(d/'stderr').write_bytes(z.stderr);status=dict(terminal=True,exit=z.returncode,exception=None,result_written=(d/'must-not-exist.json').exists(),driver_sha256=sha(d/'prove.py'))
 (d/'status.json').write_bytes((json.dumps(status,indent=2)+'\n').encode())
 if z.returncode==0 or status['result_written'] or not z.stderr:raise ValueError('invalid actual prerequisite passed '+label)
 cli.append(dict(case=label,status=status,limits='Actual producer CLI on disposable input, no original-code execution'))
mutations=[('changes-special-ID',0x387100,'args','ecx, 0x1ff'),('widens-direct-return',0x387118,'args','eax, dword ptr [rax + 0x714]'),('safe-null-return-invented',0x3870f9,'args','0x387124'),('second-resolver-query-changed',0x3870e9,'args','rcx, rbx'),('owner-null-return-changed',0x31b86e,'mnemonic','mov'),('caller-truncates-to-byte',0x304e1a,'args','r8d, al'),('caller-passes-other-getter',0x304e12,'args','0x387a50')]
synthetic=[]
for label,pc,key,value in mutations:
 x=copy.deepcopy(sources);i=next(i for v in x for r in v['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc);before=i[key];i[key]=value
 try:R.derive(*x,G)
 except(ValueError,KeyError,RuntimeError) as e:reason=str(e)
 else:raise ValueError('source mutation accepted '+label)
 synthetic.append(dict(case=label,pc=hex(pc),field=key,before=before,after=value,refusal=reason,limits='Synthetic source annotation mutation of actual derive, no EXE patch or native run'))
out=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-01.json'),CLI_cases=cli,synthetic_source_cases=synthetic,limits='Producer controls/conditional source proof, not independent acceptance or observed natural values/owner identity/NULL fault.')
(P/'control-result-01.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print('CONTROLLED four actual prerequisite refusals/seven owner/value-transfer source mutations')
