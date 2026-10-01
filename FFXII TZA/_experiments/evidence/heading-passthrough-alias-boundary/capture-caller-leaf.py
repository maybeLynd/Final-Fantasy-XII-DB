"""One necessary original caller dependency; no repeat of the captured bodies."""
import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained'
assert not (W/'caller-leaf.json').exists() and not (R/'caller-intervening-leaf.bin').exists()
raw=json.loads((W/'raw.json').read_bytes());ident=raw['identity']
for s in ident['sources']:
 if s['copy'] in ['shipping-reader.py','reg_tracking.py']:assert hashlib.sha256((R/s['copy']).read_bytes()).hexdigest()==s['sha256']
tree=ast.parse((R/'shipping-reader.py').read_text('utf-8'))
ns={'EXE':ident['exe']['path'],'SHA':ident['exe']['sha256'],'IMG_LO':0x120000,'hashlib':hashlib,'struct':struct}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['load_image','img_rd']],type_ignores=[]),'original certified reader functions','exec'),ns)
image,sections=ns['load_image']();code=ns['img_rd'](image,sections,0x2e45e0,40)
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'shared reviewed adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x2e45e0));assert sum(i.size for i in ins)==40
rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'written':sorted(roles.written(i)),'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
assert not any(i.mnemonic=='call' for i in ins)
assert not any(set(x['written'])&{'r14','rbp','rbx'} for x in rows)
assert hashlib.sha256(Path(ns['EXE']).read_bytes()).hexdigest()==ident['exe']['sha256']
(R/'caller-intervening-leaf.bin').write_bytes(code)
out={'method':'A additional original40B intervening leaf only; no guest/native/live execution','entry':'002E45E0','sha256':hashlib.sha256(code).hexdigest(),'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256((R/'reg_tracking.py').read_bytes()).hexdigest(),'exe_sha256':ident['exe']['sha256'],'instructions':rows,'limits':'Local callee register preservation only; not global call reachability, runtime pointer values or actor/movement memory non-overlap.'}
(W/'caller-leaf.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print(json.dumps(out,indent=2))
