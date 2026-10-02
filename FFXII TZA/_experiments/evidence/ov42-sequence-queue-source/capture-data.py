"""Retain this entry's six original jump DWORDs and physical byte identity."""
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
 raise ValueError('unbacked original data')
table=read(0x306af0,24);body=read(0x306760,936)
with(P/'data-01.json').open('x') as f:json.dump(dict(complete=True,method='A original embedded data, not decoded instructions',driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exe_sha256=PIN,physical_body_sha256=hashlib.sha256(body).hexdigest(),physical_body_hex=body.hex(),padding_306aef=read(0x306aef,1).hex(),table_va='0x306af0',table_hex=table.hex(),relative_dwords=list(struct.unpack('<6I',table)),limits='Original relative dispatch table and file bytes, no runtime kind/state/row binding observed.'),f,indent=2)
print('RETAINED original six dispatch DWORDs and code/padding/table separation')
