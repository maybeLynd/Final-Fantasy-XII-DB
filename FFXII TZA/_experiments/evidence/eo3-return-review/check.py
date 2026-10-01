"""Bounded static review of FABLE's returned same-stop EO3 pointer correction."""
import hashlib, json, struct
from pathlib import Path
import capstone

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
p=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
d=p.read_bytes()
sha=hashlib.sha256(d).hexdigest()
assert sha=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',d,0x3c)[0]
opt=struct.unpack_from('<H',d,pe+20)[0]
sec=[]
for k in range(struct.unpack_from('<H',d,pe+6)[0]):
 o=pe+24+opt+40*k;vs,va,rs,ro=struct.unpack_from('<IIII',d,o+8);sec.append((0x120000+va,min(vs,rs),ro))
def get(v,n):
 for s,size,ro in sec:
  if s<=v and v+n<=s+size:return d[ro+v-s:ro+v-s+n]
 raise ValueError('unbacked range')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
def decode(b,v):
 ins=list(md.disasm(b,v));assert ins and ins[-1].address+ins[-1].size==v+len(b)
 return ins
def rdi_writes(ins):
 return [hex(i.address) for i in ins if set(md.reg_name(r) for r in i.regs_access()[1])&{'rdi','edi','di','dil'}]
body=get(0x36c140,84);ins=decode(body,0x36c140)
assert not rdi_writes(ins)
assert not any(i.group(capstone.CS_GRP_CALL) for i in ins)
assert ins[-1].mnemonic=='ret'
for i in ins:
 if i.group(capstone.CS_GRP_JUMP):
  assert i.operands[0].type==capstone.x86.X86_OP_IMM and 0x36c140<=i.operands[0].imm<0x36c194
caller=get(0x32e816,60);ci=decode(caller,0x32e816)
assert rdi_writes(ci)==['0x32e816']
assert [(hex(i.address),hex(i.operands[0].imm)) for i in ci if i.group(capstone.CS_GRP_CALL)]==[('0x32e82e','0x36c140'),('0x32e84d','0x32e870')]
assert get(0x32e846,7)==bytes.fromhex('8bd7b9ff000000')
# Synthetic static detector control; never executed or written to the reference/game.
bad=bytes.fromhex('bf1122334490')+body[6:]
assert rdi_writes(decode(bad,0x36c140))==['0x36c140']
def receipt(b,v):
 return {'start':hex(v),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'raw_hex':b.hex(),
 'instructions':[[hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str,[md.reg_name(r) for r in i.regs_access()[1]]] for i in decode(b,v)]}
out={'method':'A static shipping byte review; no original execution or live','exe_sha256':sha,'capstone':capstone.__version__,
 'callee':receipt(body,0x36c140),'caller':receipt(caller,0x32e816),
 'controls':{'synthetic_EDI_write_detected':True,'full_nonzero_ranges':[84,60]},
 'conclusion':'If normal original flow reaches 0032E84D, RDI retains the allocator result, RDX contains zero_extend(low32(RDI)), ECX=FF in the same context.',
 'limits':['0036C140 can spin forever at0036C150 if its initial count is nonpositive; reaching the observation point remains conditional.',
 'No runtime caller, allocation placement, pointer readability, queue-consumer linkage, crash cause or live instrument health established.',
 'Callee also performs a 64-bit RAX load at0036C17C; literal only-EAX wording is too narrow.']}
(HERE/'observation.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
print('PASS exact shipping identity, full84/60B ranges, no RDI writes after definition, bounded callee branches/no calls, and synthetic EDI-write detector control.')
