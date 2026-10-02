"""The classifier's original code and two embedded tables, not live state."""
import hashlib,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('wrong image')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise ValueError('unbacked original bytes')
body=read(0x306bd0,440);j=read(0x306cec,28);m=read(0x306d08,128)
with(P/'data-01.json').open('x') as f:json.dump(dict(complete=True,method='A original classifier embedded data',exe_sha256=PIN,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),physical_body_sha256=hashlib.sha256(body).hexdigest(),physical_body_hex=body.hex(),jump_dwords=list(struct.unpack('<7I',j)),jump_hex=j.hex(),mapping=list(m),mapping_hex=m.hex(),limits='Shipping file data only, no initialized runtime bindings or natural reachability.'),f,indent=2)
print('RETAINED original284code/28jump/128selector bytes; no classifier-name census')
