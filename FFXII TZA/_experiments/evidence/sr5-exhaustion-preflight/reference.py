import csv,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd()
path=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=path.read_bytes()
sha=hashlib.sha256(raw).hexdigest();assert sha=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0]
assert struct.unpack_from('<H',raw,pe+24)[0]==0x20b
base=struct.unpack_from('<Q',raw,pe+24+24)[0];assert base==0x120000
sections=[]
for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
 o=pe+24+os+i*40;vs,va,rs,ro=struct.unpack_from('<IIII',raw,o+8);sections.append((base+va,min(vs,rs),ro))
a=0x21b5b0;n=138
for va,size,off in sections:
 if va<=a and a+n<=va+size:code=raw[off+a-va:off+a-va+n];break
else:raise AssertionError('unbacked original function')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
ins=list(md.disasm(code,a));assert sum(x.size for x in ins)==n
r={'method':'A original byte/CFG observation-coverage qualification; not execution',
 'source_exe':str(path.relative_to(ROOT)).replace('\\','/'),'exe_sha256':sha,'image_base':hex(base),
 'capstone':capstone.__version__,'address':hex(a),'bytes':n,'code_hex':code.hex(),
 'code_sha256':hashlib.sha256(code).hexdigest(),
 'instructions':[{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins],
 'limits':'Direct decoded original control flow in one138B body; no actual callers, bank state, receipt effects or audio observed.'}
(HERE/'reference.json').write_text(json.dumps(r,indent=2)+'\n')
for i in ins:print(f'{i.address:08X} {i.mnemonic:8} {i.op_str}')
