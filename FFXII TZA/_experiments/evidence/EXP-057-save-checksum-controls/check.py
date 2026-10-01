"""Original save checksum helper and finalizer tail against independent CRC controls."""
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import *

HERE = Path(__file__).resolve().parent
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
base = struct.unpack_from('<Q', raw, pe + 48)[0]
table = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]

def extract(va, size):
    for n in range(struct.unpack_from('<H', raw, pe + 6)[0]):
        _, rva, length, disk = struct.unpack_from('<4I', raw, table + 40*n + 8)
        if rva <= va-base < rva+length:
            return raw[disk+va-base-rva:disk+va-base-rva+size]
    raise AssertionError(hex(va))
import zlib

HELPER,GETTER,FINALIZER,SEGMENT,STOP=0x3BB220,0x2EF640,0x583D60,0x583F81,0x583FA3
ACTIVE,STAGING,STACK,RETURN=0x2164280,0x21BA940,0x60000808,0x60002000
BODIES={a:extract(a,n) for a,n in [(HELPER,160),(GETTER,8),(FINALIZER,622)]}
assert BODIES[GETTER][-1]==0xC3 and BODIES[FINALIZER][-1]==0xC3

def machine():
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for p in sorted({a&~4095 for a in BODIES}):u.mem_map(p,4096)
    for a,b in BODIES.items():u.mem_write(a,b)
    u.mem_map(0x60000000,0x3000)
    return u

def helper_case(name,data,length=None):
    u=machine();u.mem_map(0x50000000,4096);u.mem_write(0x50000000,data or b'\xA5')
    length=len(data) if length is None else length
    positive=0<length<0x80000000
    pointer=0x50000000 if positive else 0
    reads=[];writes=[]
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,access,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
    u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK)
    u.reg_write(UC_X86_REG_RCX,pointer);u.reg_write(UC_X86_REG_EDX,length)
    u.emu_start(HELPER,RETURN,count=100000)
    assert u.reg_read(UC_X86_REG_RIP)==RETURN and u.reg_read(UC_X86_REG_RSP)==STACK+8
    expected=zlib.crc32(data[:length]) if positive else 0
    assert u.reg_read(UC_X86_REG_EAX)==expected and reads==[[pointer+i,1] for i in range(length if positive else 0)] and not writes
    return dict(name=name,input_hex=data.hex(),length_u32=length,pointer=pointer,crc32=expected,reads=reads,writes=writes,returned=True)

def finalizer_case(name,destination=ACTIVE,flip=None,mutant=False):
    u=machine();u.mem_map(ACTIVE&~4095,0xAF000)
    original=bytearray((i*29+11)&255 for i in range(0x56690))
    if flip is not None:original[flip]^=1
    u.mem_write(ACTIVE,bytes(original));u.mem_write(STAGING,b'\xA5'*0x56690)
    if mutant:
        # Shorten the checksum interval by one byte, retaining valid native execution.
        a=0x583F8C;assert bytes(u.mem_read(a,6))==bytes.fromhex('8d9000e20000')
        u.mem_write(a,bytes.fromhex('8d90ffe10000'))
    expected_crc=zlib.crc32(original[8:0xE200])
    regions={a:bytearray(u.mem_read(a,0x56690)) for a in (ACTIVE,STAGING)}
    struct.pack_into('<I',regions[destination],0xE200,expected_crc)
    struct.pack_into('<I',regions[destination],0,(~expected_crc)&0xFFFFFFFF)
    writes=[];calls=[];count=0;contiguous=True;first=None;last=None
    def read_hook(uc,access,a,n,v,d):
        nonlocal count,contiguous,first,last
        if first is None:first=a
        if a!=ACTIVE+8+count or n!=1:contiguous=False
        count+=n;last=a+n-1
    u.hook_add(unicorn.UC_HOOK_MEM_READ,read_hook,begin=ACTIVE,end=STAGING+0x56690-1)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append(dict(address=a,bytes=n,value=v&((1<<(n*8))-1))),begin=ACTIVE,end=STAGING+0x56690-1)
    def helper_entry(uc,a,n,d):calls.append(dict(address=a,pointer=uc.reg_read(UC_X86_REG_RCX),length=uc.reg_read(UC_X86_REG_EDX)))
    u.hook_add(unicorn.UC_HOOK_CODE,helper_entry,begin=HELPER,end=HELPER)
    u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RDI,destination)
    saved={r:1000+r for r in (UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)}
    for r,v in saved.items():u.reg_write(r,v)
    u.emu_start(SEGMENT,STOP,count=5000000)
    assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK and u.reg_read(UC_X86_REG_RDI)==destination
    assert all(u.reg_read(r)==v for r,v in saved.items()) and bytes(u.mem_read(STACK,8))==struct.pack('<Q',RETURN)
    expected_writes=[dict(address=destination+0xE200,bytes=4,value=expected_crc),dict(address=destination,bytes=4,value=(~expected_crc)&0xFFFFFFFF)]
    matches=(calls==[dict(address=HELPER,pointer=ACTIVE+8,length=0xE1F8)] and count==0xE1F8 and contiguous and writes==expected_writes
        and all(bytes(u.mem_read(a,len(b)))==bytes(b) for a,b in regions.items()))
    return dict(name=name,destination=destination,flipped_offset=flip,expected_crc=expected_crc,observed_crc=struct.unpack('<I',u.mem_read(destination+0xE200,4))[0],
        helper_calls=calls,reads=dict(first=first,last=last,count=count,contiguous=contiguous),writes=writes,expected_writes=expected_writes,matches=matches,
        source_sha256=hashlib.sha256(original).hexdigest(),stop=STOP)

helpers=[helper_case('empty',b''),helper_case('negative-length',b'',0xFFFFFFFF),helper_case('minimum-signed-length',b'',0x80000000),
    helper_case('single-zero',b'\0'),helper_case('single-ff',b'\xFF'),helper_case('standard-nine-bytes',b'123456789'),helper_case('all-byte-values',bytes(range(256)))]
assert helpers[5]['crc32']==0xCBF43926
cases=[finalizer_case('active-destination'),finalizer_case('staging-destination',STAGING)]
for offset in (0,7,8,0xE1FF,0xE200,0x5668F):cases.append(finalizer_case(f'flip-{offset:x}',STAGING,offset))
assert all(c['matches'] for c in cases)
base_crc=cases[0]['expected_crc']
assert cases[1]['expected_crc']==base_crc
for c in cases[2:]:assert (c['expected_crc']!=base_crc)==(8<=c['flipped_offset']<0xE200)
fault=finalizer_case('mutant-omits-last-byte',STAGING,mutant=True)
assert not fault['matches'] and fault['reads']['count']==0xE1F7
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    helper_cases=helpers,finalizer_cases=cases,short_range_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print('PASS: seven helper and eight finalizer-segment cases; standard CRC32 vector; shortened range detected')
