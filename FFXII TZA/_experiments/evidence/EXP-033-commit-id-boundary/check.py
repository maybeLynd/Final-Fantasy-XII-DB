"""Execute original local ID gate; stop before calls, stores or return epilogue.

Inputs are injected RDI/RAX values, not live state. Every case uses a fresh Unicorn
instance. Mutants are private immutable byte copies and never edit the reference.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import UC_X86_REG_RDI,UC_X86_REG_RAX,UC_X86_REG_R13,UC_X86_REG_RIP

HERE=Path(__file__).resolve().parent
EXE=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
raw=EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0]
base=struct.unpack_from('<Q',raw,pe+48)[0]
count=struct.unpack_from('<H',raw,pe+6)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
code=None
for i in range(count):
    _,rva,size,offset=struct.unpack_from('<4I',raw,table+40*i+8)
    if rva<=0x30F760-base<rva+size:
        start=offset+0x30F760-base-rva
        code=raw[start:start+570]
assert code is not None and len(code)==570
assert code[0x38:0x3E]==bytes.fromhex('41bd1e020000')
assert code[0x45:0x47]==bytes.fromhex('7732')
boundaries={0x30F7A7:'normal_before_handle_ops',0x30F7F2:'extended_before_commit',0x30F981:'reject_before_return0'}
ids=[0,0x21D,0x21E,0x21F,0x220,0x3FFF,0x4000,0x4165,0x4166,0x4167,0xFFFF]


def execute(blob,value):
    uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    uc.mem_map(0x30F000,0x1000)
    uc.mem_write(0x30F760,blob)
    uc.reg_write(UC_X86_REG_RDI,value)
    uc.reg_write(UC_X86_REG_RAX,0)
    visited=[]
    def hook(emu,address,size,user):
        visited.append(address)
        if address in boundaries:emu.emu_stop()
    uc.hook_add(unicorn.UC_HOOK_CODE,hook)
    uc.emu_start(0x30F798,0x30F99A,count=40)
    rip=uc.reg_read(UC_X86_REG_RIP)
    assert rip in boundaries,'did not reach a declared boundary'
    assert len(visited)<40
    return dict(id=value,path=boundaries[rip],boundary=rip,r13=uc.reg_read(UC_X86_REG_R13),visited=visited)


def expected(value):
    if value<=0x21E:return 'normal_before_handle_ops'
    if 0x4000<=value<=0x4166:return 'extended_before_commit'
    return 'reject_before_return0'


results=[execute(code,x) for x in ids]
assert all(r['path']==expected(r['id']) and r['r13']==0x21E for r in results)
mutants={}
for name,offset,value in [('threshold_plus_one',0x3A,0x1F),('ja_to_jae',0x45,0x73)]:
    changed=bytearray(code)
    changed[offset]=value
    blob=bytes(changed)
    rows=[execute(blob,x) for x in ids]
    mismatches=[r['id'] for r in rows if r['path']!=expected(r['id'])]
    assert mismatches
    mutants[name]=dict(mutation_offset=offset,original=code[offset],replacement=value,
                       sha256=hashlib.sha256(blob).hexdigest(),mismatches=mismatches,results=rows)
assert code==raw[start:start+570]
for name in ['function.bin','disassembly.txt','result.json','manifest.json']:
    assert not (HERE/name).exists(),'preserve prior run'
(HERE/'function.bin').write_bytes(code)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join('%08X %-24s %s %s'%(i.address,i.bytes.hex(),i.mnemonic,i.op_str)
                                            for i in cs.disasm(code,0x30F760))+'\n')
result=dict(status='PASS',scope='local original ID-gate execution, no downstream calls or live game',
 exe_sha256=hashlib.sha256(raw).hexdigest(),image_base=base,file_offset=start,function_va=0x30F760,
 function_bytes=len(code),function_sha256=hashlib.sha256(code).hexdigest(),
 source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 unicorn=unicorn.__version__,capstone=capstone.__version__,results=results,mutants=mutants)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in HERE.iterdir() if p.is_file() and p.name!='manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print('PASS11 original boundary cases;2 private off-by-one mutants detected')
