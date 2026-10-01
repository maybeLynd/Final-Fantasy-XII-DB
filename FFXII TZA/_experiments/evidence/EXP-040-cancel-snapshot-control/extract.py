"""Extract certified PE runtime-function extent containing the documented cancel call."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone

HERE=Path(__file__).resolve().parent
EXE=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
raw=EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0]
base=struct.unpack_from('<Q',raw,pe+48)[0]
count=struct.unpack_from('<H',raw,pe+6)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<4I',raw,table+40*i+8) for i in range(count)]
def offset(rva):
    matches=[disk+rva-start for virtual,start,size,disk in sections if start<=rva<start+size]
    assert len(matches)==1
    return matches[0]
exception_rva,exception_size=struct.unpack_from('<2I',raw,pe+24+112+3*8)
matches=[]
for cursor in range(offset(exception_rva),offset(exception_rva)+exception_size,12):
    begin,end,unwind=struct.unpack_from('<3I',raw,cursor)
    if begin<=0x310618-base<end:matches.append((begin,end,unwind))
assert len(matches)==1
begin,end,unwind=matches[0]
code=raw[offset(begin):offset(end-1)+1]
assert len(code)==end-begin
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disassembly='\n'.join(('%08X %-24s %s %s'%(i.address,i.bytes.hex(),i.mnemonic,i.op_str)).rstrip()
                      for i in cs.disasm(code,base+begin))+'\n'
for name,data in [('function.bin',code),('disassembly.txt',disassembly.encode()),
                  ('identity.json',(json.dumps(dict(exe_sha256=hashlib.sha256(raw).hexdigest(),image_base=base,
                      begin=base+begin,end=base+end,unwind_rva=unwind,file_offset=offset(begin),
                      bytes=len(code),sha256=hashlib.sha256(code).hexdigest(),capstone=capstone.__version__),indent=2)+'\n').encode())]:
    with (HERE/name).open('xb') as output:output.write(data)
print(disassembly)
