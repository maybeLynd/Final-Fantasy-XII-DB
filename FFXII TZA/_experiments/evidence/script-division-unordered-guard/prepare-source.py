import sys
sys.dont_write_bytecode=True
import hashlib,types,inspect
from pathlib import Path
import capstone
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=Path(__file__).resolve().parent
p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained/shipping-reader.py');b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
rd=types.ModuleType('shipping_reader');rd.__file__=str(p.resolve());exec(compile(b,str(p),'exec'),rd.__dict__);image,ss=rd.load_image();assert hashlib.sha256(image).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for i in cs.disasm(rd.img_rd(image,ss,0x25e4c0,512),0x25e4c0):
 if 'xmm7' in i.op_str or 'ebp' in i.op_str:print('INITIAL',f'{i.address:08X}',i.bytes.hex(),i.mnemonic,i.op_str)
for a,n in [(0x25f0ac,298),(0x25e682,64)]:
 for i in cs.disasm(rd.img_rd(image,ss,a,n),a):print(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}')
