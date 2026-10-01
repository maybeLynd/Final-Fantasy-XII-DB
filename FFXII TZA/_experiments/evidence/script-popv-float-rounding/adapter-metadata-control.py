"""Regression for actual producer's string adapter and returned initial labels."""
import ast,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;src=(W/'feasibility.py').read_bytes();tree=ast.parse(src);old=(W/'retained/original70-capture.py').read_bytes();fn=next(n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef) and n.name=='run')
selected=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['original','changed'] for t in n.targets)];assert len(selected)>=5
ns=dict(ast=ast,fn=fn);exec(compile(ast.fix_missing_locations(ast.Module(body=selected,type_ignores=[])),'actual producer string adapter assignments','exec'),ns);changed=ns['changed'];assert 'u.reg_write(UC_X86_REG_MXCSR, mxcsr)' in changed and 'u.reg_write(UC_X86_REG_R8D, 1)' in changed
ret=next(n for n in ast.parse(changed).body[0].body if isinstance(n,ast.Return));initial=next(k.value for k in ret.value.keywords if k.arg=='initial');expr=compile(ast.fix_missing_locations(ast.Expression(body=initial)),'actual producer initial metadata constructor','eval');labels=[]
for m in [0x1f80,0x5f80]:
 v=eval(expr,dict(ram=b'',rec=b'',RSP=0x60001800,store_rsp=0x600017f8,SENT=0x60000200,ENTRY=0x267e9c,STOP=0x267f1e,mxcsr=m));assert v['mxcsr']==hex(m) and v['kind_selector_r8d']==1;labels.append(v)
assert labels[0]['mxcsr']!=labels[1]['mxcsr'],'Actual default constructor must not repeat nearest label'
p=W/'runner-adapted-corrected.py';out=(changed+'\n').encode()
if p.exists():assert p.read_bytes()==out
else:p.write_bytes(out)
receipt=dict(status='PASS_ACTUAL_STRING_ADAPTER_METADATA_PATH',producer_sha256=hashlib.sha256(src).hexdigest(),selected_ast_sha256=hashlib.sha256(ast.dump(ast.Module(body=selected,type_ignores=[]),include_attributes=True).encode()).hexdigest(),corrected_adapter_sha256=hashlib.sha256(changed.encode()).hexdigest(),actual_initial_constructor_labels=labels,old_literal_label_would_fail=labels[1]['mxcsr']!='0x1f80',limits='Execute only actual producer adapter construction/initial metadata expression with dummy buffers; no original/guest/native/live run. Two original cases not repeated, raw immutable.')
p=W/'adapter-metadata-control.json';out=(json.dumps(receipt,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out
else:p.write_bytes(out)
print('PASS actual producer adapter/initial-state metadata constructor',flush=True)
