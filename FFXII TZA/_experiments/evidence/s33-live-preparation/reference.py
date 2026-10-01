"""Bounded original source for pickup observation address qualification."""
import csv,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd()
path=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=path.read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
assert struct.unpack_from('<Q',raw,pe+24+24)[0]==0x120000
sections=[]
for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
 o=pe+24+opt+i*40;vs,va,rs,ro=struct.unpack_from('<IIII',raw,o+8);sections.append((0x120000+va,min(vs,rs),ro))
def read(a,n):
 for va,size,off in sections:
  if va<=a and a+n<=va+size:return raw[off+a-va:off+a-va+n]
 raise AssertionError('range not backed by reference bytes')
graphpath=ROOT/'Database/Tools/work/graph/functions.tsv'
functions={x['entry']:x for x in csv.DictReader(graphpath.open(),delimiter='\t')}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
record={'method':'A original address qualification only; no native fixture or live run',
 'exe_sha256':sha(raw),'capstone':capstone.__version__,'extent_source_sha256':sha(graphpath.read_bytes()),'bodies':[]}
for a in (0x3fa160,0x3fa730,0x3fa790):
 n=int(functions[f'{a:08X}']['body_bytes']);assert 0<n<=1024
 code=read(a,n);ins=list(md.disasm(code,a));assert sum(i.size for i in ins)==n
 record['bodies'].append({'address':hex(a),'bytes':n,'hex':code.hex(),'sha256':sha(code),
   'instructions':[{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
 print('BODY',hex(a),n)
 for i in ins:
  if a!=0x3fa160 or i.address<0x3fa1a0 or i.address>=0x3fa280 and i.address<0x3fa2f0 or '0x272' in i.op_str:
   print(f'{i.address:08X} {i.mnemonic:8} {i.op_str}')
fixture=ROOT/'Database/FFXII TZA/_index/candidates/s33-opus-replay-op1-real'
record['retained_fixture_files']={n:{'bytes':len((fixture/n).read_bytes()),'sha256':sha((fixture/n).read_bytes())} for n in ('README.md','check.py','result.json')}
record['handle_store_319E05']={'address':'0x319e05','hex':read(0x319e05,3).hex()}
(HERE/'reference.json').write_text(json.dumps(record,indent=2)+'\n')
