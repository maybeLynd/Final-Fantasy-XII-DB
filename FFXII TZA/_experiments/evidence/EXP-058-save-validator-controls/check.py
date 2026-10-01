"""Original 00255260 header predicate with exact reads and return controls."""
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
ENTRY,DATA,STACK,RETURN=0x255260,0x50000000,0x60000808,0x60002000
BODY=extract(ENTRY,45)

def run(name,first=0,second=0,null=False,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    u.mem_map(ENTRY&~4095,4096);u.mem_map(DATA,4096);u.mem_map(0x60000000,0x3000)
    body=BODY
    if mutant:
        # Replace the conditional second-dword result with unconditional true.
        at=0x255283-ENTRY;assert body[at:at+3]==bytes.fromhex('0f94c0')
        body=body[:at]+bytes.fromhex('b00190')+body[at+3:]
    u.mem_write(ENTRY,body)
    fixture=struct.pack('<II',first,second)+b'\xA5'*(4096-8);u.mem_write(DATA,fixture)
    reads=[];writes=[];visits=[]
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,access,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_CODE,lambda uc,a,n,d:visits.append(a))
    saved={r:1000+r for r in (UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)}
    for r,v in saved.items():u.reg_write(r,v)
    u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RCX,0 if null else DATA)
    u.emu_start(ENTRY,RETURN,count=100)
    assert u.reg_read(UC_X86_REG_RIP)==RETURN and u.reg_read(UC_X86_REG_RSP)==STACK+8
    assert all(u.reg_read(r)==v for r,v in saved.items())
    expected=int(null or (first==second==0) or (first==0x0131F3EA and second==0x4818))
    expected_reads=[] if null else [[DATA,4]]+([[DATA+4,4]] if first in (0,0x0131F3EA) else [])
    value=u.reg_read(UC_X86_REG_EAX)
    matches=value==expected and reads==expected_reads and not writes and bytes(u.mem_read(DATA,4096))==fixture
    return dict(name=name,first=first,second=second,null=null,expected=expected,observed=value,reads=reads,expected_reads=expected_reads,writes=writes,visited=visits,matches=matches)

cases=[run('null',null=True),run('zero-pair'),run('valid-pair',0x0131F3EA,0x4818),run('zero-first-only',0,0x4818),
    run('magic-size-zero',0x0131F3EA,0),run('magic-short-size',0x0131F3EA,0x4817),run('magic-large-size',0x0131F3EA,0x4819),
    run('wrong-magic',0x0131F3EB,0x4818),run('both-ones',0xFFFFFFFF,0xFFFFFFFF),run('other-save-stamps',0x20050223,0x1538)]
assert all(c['matches'] for c in cases)
fault=run('mutant-ignores-size',0x0131F3EA,0x4819,mutant=True)
assert not fault['matches'] and fault['observed']==1 and fault['reads']==fault['expected_reads']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,size_check_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'00255260.bin').write_bytes(BODY)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for i in cs.disasm(BODY,ENTRY))+'\n')
print('PASS: ten original header-predicate controls; ignored-size mutant detected')
