"""Execute the complete original append helper, including explicit malformed-state cases."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import UC_X86_REG_RIP,UC_X86_REG_RSP,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_RAX
HERE=Path(__file__).resolve().parent
EXE=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
raw=EXE.read_bytes();exe_sha=hashlib.sha256(raw).hexdigest()
assert exe_sha=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];base=struct.unpack_from('<Q',raw,pe+48)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
offsets=[]
for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
    virtual,rva,size,disk=struct.unpack_from('<4I',raw,table+40*i+8)
    if rva<=0x316CD0-base<rva+size:offsets.append(disk+0x316CD0-base-rva)
assert len(offsets)==1
code=raw[offsets[0]:offsets[0]+24]
assert code[9:12]==bytes.fromhex('4803c0') and code[-1:]==b'\xc3'
MEMORY,BUFFER,STACK,RETURN=0x50000000,0x50000100,0x60000800,0x60001000
ACTOR=0xFEDCBA9876543210


def execute(blob,count,actor=ACTOR,duplicate=False):
    uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    uc.mem_map(0x316000,0x1000);uc.mem_write(0x316CD0,blob)
    before=bytearray((i*29+11)%256 for i in range(0x1000))
    struct.pack_into('<i',before,BUFFER-MEMORY+4,count)
    if duplicate:struct.pack_into('<Q',before,BUFFER-MEMORY+8,actor)
    uc.mem_map(MEMORY,0x1000);uc.mem_write(MEMORY,bytes(before))
    uc.mem_map(0x60000000,0x2000);uc.mem_write(STACK,struct.pack('<Q',RETURN))
    uc.reg_write(UC_X86_REG_RSP,STACK);uc.reg_write(UC_X86_REG_RCX,BUFFER);uc.reg_write(UC_X86_REG_RDX,actor)
    visited=[];writes=[]
    def step(u,address,size,data):
        visited.append(address)
        if address==RETURN:u.emu_stop()
    uc.hook_add(unicorn.UC_HOOK_CODE,step)
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,data:writes.append(dict(address=address,bytes=size)))
    uc.emu_start(0x316CD0,0,count=20)
    assert uc.reg_read(UC_X86_REG_RIP)==RETURN and uc.reg_read(UC_X86_REG_RSP)==STACK+8 and len(visited)<20
    assert uc.reg_read(UC_X86_REG_RAX)==((count+1)&0xFFFFFFFF if count<32 else count)
    after=bytes(uc.mem_read(MEMORY,0x1000));expected=bytearray(before)
    expected_writes=[]
    if count<32:
        address=BUFFER+8+count*16
        struct.pack_into('<Q',expected,address-MEMORY,actor)
        struct.pack_into('<i',expected,BUFFER-MEMORY+4,count+1)
        expected_writes=[dict(address=address,bytes=8),dict(address=BUFFER+4,bytes=4)]
    return dict(count=count,actor=actor,duplicate_preexisting=duplicate,
                domain='valid_count' if 0<=count<=32 else 'malformed_count',
                matches=after==bytes(expected) and writes==expected_writes,
                resulting_count=struct.unpack_from('<i',after,BUFFER-MEMORY+4)[0],
                visited=visited,writes=writes,rax=uc.reg_read(UC_X86_REG_RAX),
                changed_offsets_from_buffer=[i+MEMORY-BUFFER for i,(a,b) in enumerate(zip(before,after)) if a!=b],
                buffer_before=bytes(before[BUFFER-MEMORY:BUFFER-MEMORY+0x208]).hex(),
                buffer_after=after[BUFFER-MEMORY:BUFFER-MEMORY+0x208].hex(),
                prefix_before=bytes(before[BUFFER-MEMORY-32:BUFFER-MEMORY]).hex(),
                prefix_after=after[BUFFER-MEMORY-32:BUFFER-MEMORY].hex())


cases=[execute(code,n) for n in (0,1,31,32,33,0x7FFFFFFF,-1,-2)]
cases += [execute(code,0,actor=0),execute(code,1,duplicate=True)]
assert all(case['matches'] for case in cases)
mutant=code[:9]+b'\x90'*3+code[12:]
fault=execute(mutant,1);assert not fault['matches']
assert code==raw[offsets[0]:offsets[0]+24]
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disassembly='\n'.join(('%08X %-24s %s %s'%(i.address,i.bytes.hex(),i.mnemonic,i.op_str)).rstrip()
                      for i in cs.disasm(code,0x316CD0))+'\n'
result=dict(status='PASS',scope='isolated complete original append; no live engine or actor dereference',
            exe_sha256=exe_sha,image_base=base,function_va=0x316CD0,file_offset=offsets[0],function_bytes=24,
            function_sha256=hashlib.sha256(code).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            unicorn=unicorn.__version__,capstone=capstone.__version__,cases=cases,
            mutant=dict(name='remove_index_doubling',sha256=hashlib.sha256(mutant).hexdigest(),result=fault))
for name,data in [('function.bin',code),('disassembly.txt',disassembly.encode()),('result.json',(json.dumps(result,indent=2)+'\n').encode())]:
    with (HERE/name).open('xb') as output:output.write(data)
print(disassembly)
print('PASS: ten original cases; one private stride mutant detected')
