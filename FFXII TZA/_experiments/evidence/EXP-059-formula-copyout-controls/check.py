"""Original formula numeric copy-out segment with synthetic scratch and result state."""
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
START,STOP,SCRATCH,RESULT,STACK=0x38643F,0x3866C1,0x2AEDFB8,0x50000100,0x60000800
BODY=extract(START,STOP-START)
ABSENT=0xFFFFFFFF
# Field keys are offsets from 02AEDFB8, not claims about their upstream producers.
TH0,TH1,TM0,TM1,SH0,SH1,SM0,SM1,SHABS,SMABS,THABS,TMABS=range(0x4C,0x7C,4)

def run(name,values=None,flags=0xA0000001,fallback=17,mutant=False):
    values=values or {}
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    u.mem_map(START&~4095,4096);u.mem_map(SCRATCH&~4095,8192);u.mem_map(RESULT&~4095,4096);u.mem_map(0x60000000,0x2000)
    blob=BODY
    if mutant:
        at=0x3864A4-START;assert blob[at:at+3]==bytes.fromhex('83ffff')
        blob=blob[:at+2]+b'\x00'+blob[at+3:]
    u.mem_write(START,blob)
    u.mem_write(SCRATCH&~4095,b'\xA5'*8192);u.mem_write(RESULT&~4095,b'\x5A'*4096)
    vals={k:0 for k in range(0,0xA8,4)}
    vals.update({k:ABSENT for k in range(0x4C,0x94,4)});vals.update(values)
    for k,v in vals.items():u.mem_write(SCRATCH+k,struct.pack('<I',v&ABSENT))
    u.mem_write(RESULT+0x2C,struct.pack('<I',flags));u.mem_write(STACK+0x38,struct.pack('<I',fallback))
    regions={SCRATCH&~4095:bytearray(u.mem_read(SCRATCH&~4095,8192)),RESULT&~4095:bytearray(u.mem_read(RESULT&~4095,4096))}
    expected=[];events=[];visits=[]
    before=bytes(u.mem_read(SCRATCH,0xA8)).hex()
    def write(a,n,v):
        v&=(1<<(8*n))-1;expected.append(dict(address=a,bytes=n,value=v))
        p=next(p for p,b in regions.items() if p<=a<a+n<=p+len(b));regions[p][a-p:a-p+n]=v.to_bytes(n,'little')
    flag_now=flags
    def mark(mask):
        nonlocal flag_now
        flag_now|=mask;write(RESULT+0x2C,4,flag_now)
    def present(*keys):return any(vals[k]!=ABSENT for k in keys)
    if present(TH1,TH0,THABS):mark(1<<8)
    if present(SH1,SH0,SHABS):mark(1<<7)
    if present(TH1):mark(1<<10)
    if present(SH1):mark(1<<9)
    if present(TH1,TH0):mark(1<<6)
    if present(SH1,SH0):mark(1<<5)
    if present(TM1,TM0,TMABS):mark(1<<14)
    if present(SM1,SM0,SMABS):mark(1<<13)
    if present(TM1):mark(1<<16)
    if present(SM1):mark(1<<15)
    if present(TM1,TM0) or vals[0x48]!=0:mark(1<<12)
    if present(SM1,SM0):mark(1<<11)
    if present(TH0):mark(1<<18)
    if present(0x7C,0x80,0x84,0x88):mark(1<<18)
    normalized={k:0 if vals[k]==ABSENT else vals[k] for k in (TH1,SH1,TM1,SM1,TH0,SH0,TM0,SM0)}
    for k,v in normalized.items():write(SCRATCH+k,4,v)
    private_b=0 if vals[0x44]==ABSENT else vals[0x44]
    private_a=fallback if vals[0x40]==ABSENT else vals[0x40]
    write(SCRATCH+0x44,4,private_b);write(SCRATCH+0x40,4,private_a)
    write(RESULT+0x1D,1,private_b-private_a)
    write(RESULT+0x24,4,normalized[TH1]-normalized[TH0]);write(RESULT+0x20,4,normalized[SH1]-normalized[SH0])
    write(RESULT+0x2A,2,normalized[TM1]-normalized[TM0]);write(RESULT+0x28,2,normalized[SM1]-normalized[SM0])
    for key,offset,width,setbit,clearbit in [(THABS,0x24,4,3,6),(SHABS,0x20,4,1,5),(TMABS,0x2A,2,4,12),(SMABS,0x28,2,2,11)]:
        if present(key):
            write(RESULT+offset,width,vals[key]);flag_now=(flag_now|(1<<setbit))&~(1<<clearbit);write(RESULT+0x2C,4,flag_now)
    def onwrite(uc,access,a,n,v,data):
        if not 0x60000000<=a<0x60002000:events.append(dict(address=a,bytes=n,value=v&((1<<(8*n))-1)))
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
    u.hook_add(unicorn.UC_HOOK_CODE,lambda uc,a,n,d:visits.append(a))
    u.reg_write(UC_X86_REG_RBX,RESULT);u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(START,STOP,count=500)
    assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK and u.reg_read(UC_X86_REG_RBX)==RESULT
    match=events==expected and all(bytes(u.mem_read(p,len(b)))==bytes(b) for p,b in regions.items())
    return dict(name=name,input_values=values,input_flags=flags,fallback=fallback,before_scratch=before,after_scratch=bytes(u.mem_read(SCRATCH,0xA8)).hex(),
        after_result=bytes(u.mem_read(RESULT,0x148)).hex(),events=events,expected_events=expected,visited=visits,matches=match)

cases=[run('all-absent'),run('zero-is-present',{TH1:0}),run('minus-two-is-present',{TH0:0xFFFFFFFE}),
    run('target-hp-pair',{TH0:100,TH1:25}),run('source-hp-pair',{SH0:10,SH1:35}),
    run('mp-low-word-wrap',{TM0:0x10001,TM1:0,SM0:0,SM1:0x18000}),
    run('absolute-overrides',{TH0:100,TH1:25,SH0:10,SH1:35,TM0:1,TM1:2,SM0:3,SM1:4,THABS:0,SHABS:0xFFFFFFFE,TMABS:0x12345678,SMABS:0x80000000}),
    run('absolute-only',{THABS:0,SHABS:0,TMABS:0,SMABS:0}),run('force-target-mp',{0x48:1}),
    run('stat-modifier-zero',{0x7C:0}),run('private-fallback',{0x40:ABSENT,0x44:ABSENT},fallback=0x123),
    run('private-byte-wrap',{0x40:0x100,0x44:0xFE}),run('preexisting-flags-retained',flags=0xFFFFFFFF)]
assert all(c['matches'] for c in cases),[(c['name'],c['events'],c['expected_events']) for c in cases if not c['matches']]
fault=run('mutant-zero-treated-as-absent',{TH1:0},mutant=True)
assert not fault['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,zero_sentinel_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'0038643F.bin').write_bytes(BODY)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for i in cs.disasm(BODY,START))+'\n')
print('PASS: thirteen original numeric-copy controls; zero/absent confusion detected')
