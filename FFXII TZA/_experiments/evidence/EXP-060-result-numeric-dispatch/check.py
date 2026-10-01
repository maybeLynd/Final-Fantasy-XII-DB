"""Original applier numeric dispatch with explicit no-effect setter boundaries."""
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
START,STOP,RESULT,TARGET,SOURCE,STACK=0x311608,0x311778,0x50000100,0x50000400,0x50000800,0x60000800
HPDELTA,HPABS,MPDELTA,MPABS,SECONDARY=0x300530,0x300520,0x300CE0,0x300C90,0x300BC0
BODIES={0x3112F0:extract(0x3112F0,2040)}
PRESENCE=(1<<8)|(1<<14)|(1<<7)|(1<<13)

def signed(v,bits):return v-(1<<bits) if v&(1<<(bits-1)) else v

def run(name,flags=PRESENCE,multiplier=0,resource=0xFFFE,source=SOURCE,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for page in sorted({a&~4095 for a in [*BODIES,HPDELTA,HPABS,MPDELTA,MPABS,SECONDARY,RESULT]}):u.mem_map(page,4096)
    u.mem_map(0x60000000,0x2000)
    for a,b in BODIES.items():u.mem_write(a,b)
    if mutant:
        a=0x311679;assert bytes(u.mem_read(a,3))==bytes.fromhex('c1e80b')
        u.mem_write(a,bytes.fromhex('c1e806'))
    u.mem_write(RESULT&~4095,b'\xA5'*4096)
    u.mem_write(RESULT+0x2C,struct.pack('<I',flags));u.mem_write(RESULT+0x24,struct.pack('<I',0xFFFFFFFE))
    u.mem_write(RESULT+0x20,struct.pack('<I',0x80000001));u.mem_write(RESULT+0x2A,struct.pack('<H',0x8001));u.mem_write(RESULT+0x28,struct.pack('<H',0xFFFF))
    u.mem_write(RESULT+0x1D,bytes([multiplier]));u.mem_write(TARGET+0x28,struct.pack('<H',resource))
    u.mem_write(STACK+0x88,struct.pack('<Q',source));page=bytes(u.mem_read(RESULT&~4095,4096))
    calls=[];writes=[];visits=[]
    def bit(n):return (flags>>n)&1
    def event(address,args):return dict(address=address,args=args)
    expected=[]
    target_hp=(bit(19)<<8)|(bit(10)<<5)|((1-bit(18))<<6)|((1-bit(6))<<4)
    target_mp=(bit(16)<<5)|((1-bit(12))<<4)
    source_hp=((1-bit(5))<<4)|((1-bit(17))<<6)|(bit(9)<<5)
    source_mp=((1-bit(11))<<4)|(bit(15)<<5)
    if bit(8):expected.append(event(HPABS if bit(3) else HPDELTA,[TARGET,0xFFFFFFFE,source,target_hp]))
    if bit(14):expected.append(event(MPABS if bit(4) else MPDELTA,[TARGET,signed(0x8001,16)&0xFFFFFFFF,target_mp]))
    if multiplier:expected.append(event(SECONDARY,[TARGET,(signed(resource,16)*signed(multiplier,8))&0xFFFFFFFF,target_mp|(0x400 if multiplier&0x80 else 0)]))
    if source:
        if bit(7):expected.append(event(HPABS if bit(1) else HPDELTA,[source,0x80000001,0,source_hp]))
        if bit(13):expected.append(event(MPABS if bit(2) else MPDELTA,[source,0xFFFFFFFF,source_mp]))
    def step(uc,a,n,data):
        visits.append(a)
        if a not in (HPDELTA,HPABS,MPDELTA,MPABS,SECONDARY):return
        args=[uc.reg_read(UC_X86_REG_RCX),uc.reg_read(UC_X86_REG_EDX)]
        args+=[uc.reg_read(UC_X86_REG_R8),uc.reg_read(UC_X86_REG_R9D)] if a in (HPDELTA,HPABS) else [uc.reg_read(UC_X86_REG_R8D)]
        calls.append(event(a,args))
        for r in (UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9):uc.reg_write(r,0xBADF00D)
        rsp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,int.from_bytes(uc.mem_read(rsp,8),'little'));uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
    for r,v in [(UC_X86_REG_RBX,RESULT),(UC_X86_REG_RDI,TARGET),(UC_X86_REG_R12,HPDELTA),(UC_X86_REG_R15,MPDELTA),(UC_X86_REG_R13,0),(UC_X86_REG_R14,0x13579),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
    u.emu_start(START,STOP,count=500)
    assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK
    assert u.reg_read(UC_X86_REG_RBX)==RESULT and u.reg_read(UC_X86_REG_RDI)==TARGET and u.reg_read(UC_X86_REG_R13)==0 and u.reg_read(UC_X86_REG_R14)==0x13579
    matches=calls==expected and not writes and bytes(u.mem_read(RESULT&~4095,4096))==page
    return dict(name=name,flags=flags,multiplier=multiplier,resource=resource,source=source,calls=calls,expected_calls=expected,writes=writes,visited=visits,matches=matches)

cases=[run('no-effects',flags=0),run('all-four-delta')]
for n in (1,2,3,4,5,6,9,10,11,12,15,16,17,18,19):cases.append(run(f'one-bit-{n}',flags=PRESENCE|(1<<n)))
cases += [run('all-absolute',flags=PRESENCE|30),run('no-source',source=0),run('negative-secondary',flags=0,multiplier=0x80),
    run('positive-secondary-signed-base',flags=0,multiplier=0x7F,resource=0x8000),run('all-effects-and-flags',flags=0xFFFFFFFF,multiplier=0xFF)]
assert all(c['matches'] for c in cases),[(c['name'],c['calls'],c['expected_calls']) for c in cases if not c['matches']]
fault=run('mutant-target-mp-bit11-not16',flags=PRESENCE|(1<<16),mutant=True)
assert not fault['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,wrong_shift_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} original numeric-dispatch controls; wrong source-bit shift detected')
