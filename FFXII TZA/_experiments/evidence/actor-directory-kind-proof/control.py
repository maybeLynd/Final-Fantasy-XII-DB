"""Actual CLI prerequisite refusals and discriminating source/data controls.

Controls are static analytical countermodels; no native patched code executes.
"""
import copy,hashlib,importlib.util,json,shutil,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load('producer','prove.py');G=load('cfg','prove_owner_reload_order.py')
R.receipt('prove-03','prove.py');expected=json.loads((P/'result-02.json').read_text())
sources=[json.loads((P/n).read_text()) for n in ['source-01.json','source-binding-01.json','source-setup-01.json']]
tables=json.loads((P/'native-tables-01.json').read_text());region=json.loads((P/'region-switch-01.json').read_text());b=(P/'asp_a03-US-original-01.ebp').read_bytes()
if expected.get('producer_complete') is not True or expected['driver_sha256']!=sha(P/'prove.py') or json.loads(json.dumps(R.derive(sources,tables,region,b,G)))!=expected['facts']:raise ValueError('positive producer incomplete/different')
D=P/'controls-02'
if D.exists():raise ValueError('immutable controls exist')
D.mkdir();files=[p for p in P.iterdir() if p.is_file() and p.suffix in ['.py','.json','.stdout','.stderr','.ebp','.bin']]
cli=[]
for label in ['missing-binding-status','failed-capture-exit','missing-archive-block']:
 d=D/label;d.mkdir()
 for p in files:shutil.copyfile(p,d/p.name)
 if label=='missing-binding-status':(d/'binding-01.status.json').unlink()
 elif label=='failed-capture-exit':
  x=json.loads((d/'capture-01.status.json').read_text());x['exit']=7;(d/'capture-01.status.json').write_text(json.dumps(x)+'\n')
 else:(d/'archive-block-00.bin').unlink()
 z=subprocess.run([sys.executable,'-B',str(d/'prove.py'),'must-not-exist.json'],capture_output=True,timeout=35)
 (d/'stdout').write_bytes(z.stdout);(d/'stderr').write_bytes(z.stderr)
 status=dict(terminal=True,exit=z.returncode,exception=None,driver_sha256=sha(d/'prove.py'),result_written=(d/'must-not-exist.json').exists())
 (d/'status.json').write_bytes((json.dumps(status,indent=2)+'\n').encode())
 if z.returncode==0 or status['result_written'] or not z.stderr:raise ValueError('actual invalid prerequisite passed '+label)
 cli.append(dict(case=label,status=status,limits='Actual Python CLI on disposable owned input, no native/game execution'))
mutations=[('wrong-count-width',0x267aca,'args','ecx, dword ptr [rax + r12 + 2]'),('ordinal-reset-per-row',0x267b2a,'mnemonic','xor'),('wrong-directory-stride',0x266723,'args','rdi, 5'),('wrong-kind-table-row',0x267abb,'memory_target','0x1e0c32c'),('pre-preset-overwrites-kind',0x266b5b,'args','qword ptr [rdx + 3], rax'),('preset-bit17-absent',0x266c12,'args','dword ptr [rcx + 0x1c], 0x10004'),('unapproved-init-tail',0x266aca,'args','0x3db650')]
synthetic=[]
for label,pc,key,value in mutations:
 x=copy.deepcopy(sources);i=next(i for s in x for r in s['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc)
 if key=='memory_target':before=i['memory'][0]['rip_target'];i['memory'][0]['rip_target']=value
 else:
  before=i[key];i[key]=value
  if label=='pre-preset-overwrites-kind':i['memory'][0]['displacement']=3
 try:R.derive(x,tables,region,b,G)
 except (ValueError,KeyError,RuntimeError) as e:reason=str(e)
 else:raise ValueError('source mutation accepted '+label)
 synthetic.append(dict(case=label,pc=hex(pc),field=key,before=before,after=value,refusal=reason))
# A coherent data countermodel deliberately changes the entry's type label,
# leaving header counts and ordinal untouched. Native row/preset remains6.
labelled=bytearray(b);struct.pack_into('<H',labelled,128+int(expected['facts']['data']['entry_offset'],16)+4,7)
alternate=R.derive(sources,tables,region,bytes(labelled),G)
if alternate['data']['descriptor_script_type']!=7 or alternate['data']['row']!=6 or alternate['preset_at_266c12']!='0x30004':raise ValueError('descriptor label unexpectedly determines native row')
data_controls=[]
for label,offset,fmt,value in [('count-sum-mismatch',128+0x730+2,'<H',10),('wrong-name-pool-origin',128+76,'<I',0xe474)]:
 q=bytearray(b);struct.pack_into(fmt,q,offset,value)
 try:R.parse(bytes(q))
 except (ValueError,UnicodeError,struct.error) as e:reason=str(e)
 else:raise ValueError('malformed/incorrect data interpretation passed '+label)
 data_controls.append(dict(case=label,offset=offset,refusal=reason))
out=dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-02.json'),CLI_cases=cli,synthetic_source_cases=synthetic,data_refusals=data_controls,label_countermodel=dict(method='Synthetic bytearray label change, not original execution',descriptor_script_type=7,unchanged_native_row=6,unchanged_preset='0x30004',meaning='scriptType equality is not enforced/used by this assignment path'),limits='Producer/control validation only; not independent project acceptance, new native tests or shipped malformed-data occurrence.')
(P/'control-result-02.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print('CONTROLLED three actual prerequisites, seven source changes, two data errors and independent-label countermodel')
