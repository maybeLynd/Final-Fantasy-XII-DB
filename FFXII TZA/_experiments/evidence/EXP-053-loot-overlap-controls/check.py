"""Original overlap selection and actor geometry, with controlled sqrtf."""
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

BODIES = {va: extract(va, size) for va, size in [(0x2FB150,253), (0x265020,61),
          (0x265090,27), (0x3DA710,21), (0x4686D0,35), (0x861F14,6)]}
# Resolve the actual IAT name rather than infer sqrt from the distance function.
import_rva = struct.unpack_from('<I',raw,pe+24+112+8)[0]
imports = []
for d in range(500):
    orig, stamp, chain, name, iat = struct.unpack('<5I',extract(base+import_rva+d*20,20))
    if not any((orig,stamp,chain,name,iat)):
        break
    for i in range(5000):
        entry = struct.unpack('<Q',extract(base+(orig or iat)+i*8,8))[0]
        if not entry:
            break
        if base+iat+i*8 == 0x8C2BB8:
            imports.append(dict(dll=extract(base+name,100).split(b'\0')[0].decode(),
                                name=extract(base+entry+2,100).split(b'\0')[0].decode()))
assert imports == [dict(dll='api-ms-win-crt-math-l1-1-0.dll',name='sqrtf')]
PRESENCE, COOKIE, CONSTANT = 0x22BE7F0, 0x1F44830, 0x1CEBBA8
UNIT, ACTOR, MOVE, STACK, RETURN, CHECK, SQRT = 0x50000000, 0x50001000, 0x50002000, 0x60000808, 0x60002000, 0x808C40, 0x70000000

def run(name, entries, expected, visited_slots, radii=(2.,3.), extra=0., actor_kind=3, null_unit=False, scratch=0, mutant=False):
    import math
    u = unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages = {a & ~4095 for a in list(BODIES)+[PRESENCE,PRESENCE+320,COOKIE,CONSTANT,UNIT,ACTOR,MOVE,CHECK,SQRT,0x8C2BB8]}
    for p in sorted(pages):
        u.mem_map(p,4096)
    u.mem_map(0x60000000,0x3000)
    u.mem_write(0x60000000,bytes([scratch])*0x3000)
    for va, blob in BODIES.items():
        if mutant and va == 0x2FB150:
            assert blob[0xBC:0xBE] == b'\x77\x3B'
            blob = blob[:0xBC]+b'\x73'+blob[0xBD:]
        u.mem_write(va,blob)
    u.mem_write(COOKIE,struct.pack('<Q',0x12345678))
    u.mem_write(CONSTANT,extract(CONSTANT,4))
    u.mem_write(0x8C2BB8,struct.pack('<Q',SQRT))
    u.mem_write(UNIT+16,struct.pack('<Q',ACTOR))
    u.mem_write(ACTOR+3,bytes([actor_kind<<5]))
    u.mem_write(ACTOR+0xB8,struct.pack('<Q',MOVE))
    u.mem_write(MOVE,struct.pack('<3f',10.,20.,30.))
    u.mem_write(MOVE+0x50,struct.pack('<2f',*radii))
    for slot, active, xyz in entries:
        u.mem_write(PRESENCE+slot*32,bytes([active]))
        u.mem_write(PRESENCE+slot*32+16,struct.pack('<4f',*xyz,777.))
    snapshots = {p:bytes(u.mem_read(p,4096)) for p in pages if p not in {v & ~4095 for v in BODIES}}
    u.mem_write(STACK,struct.pack('<Q',RETURN))
    u.reg_write(UC_X86_REG_RSP,STACK)
    u.reg_write(UC_X86_REG_RCX,0 if null_unit else UNIT)
    u.reg_write(UC_X86_REG_XMM1,struct.unpack('<I',struct.pack('<f',extra))[0])
    saved = {UC_X86_REG_RBX:111,UC_X86_REG_RSI:222,UC_X86_REG_RDI:333,
             UC_X86_REG_XMM6:444,UC_X86_REG_XMM7:555}
    for r,v in saved.items():
        u.reg_write(r,v)
    calls, visits, writes, checked, scanned = [], [], [], [], []
    def step(uc,address,size,data):
        visits.append(address)
        if address == RETURN:
            uc.emu_stop(); return
        if address == 0x2FB1E0:
            scanned.append(uc.reg_read(UC_X86_REG_EBX))
        if address in (0x265020,0x265090,0x3DA710,0x4686D0):
            call = dict(va=address,rcx=uc.reg_read(UC_X86_REG_RCX))
            if address == 0x4686D0:
                call = dict(va=address,slot=uc.reg_read(UC_X86_REG_EBX),
                            a=list(struct.unpack('<3f',uc.mem_read(uc.reg_read(UC_X86_REG_RCX),12))),
                            b=list(struct.unpack('<3f',uc.mem_read(uc.reg_read(UC_X86_REG_RDX),12))))
            calls.append(call)
        if address not in (CHECK,SQRT):
            return
        if address == CHECK:
            assert uc.reg_read(UC_X86_REG_RCX) == 0x12345678
            checked.append(True)
        else:
            bits = uc.reg_read(UC_X86_REG_XMM0)&0xFFFFFFFF
            squared = struct.unpack('<f',struct.pack('<I',bits))[0]
            root = math.sqrt(squared)
            root_bits = struct.unpack('<I',struct.pack('<f',root))[0]
            calls.append(dict(va=SQRT,method='controlled sqrtf surrogate',input_bits=bits,output_bits=root_bits))
            uc.reg_write(UC_X86_REG_XMM0,root_bits)
        rsp = uc.reg_read(UC_X86_REG_RSP)
        uc.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',uc.mem_read(rsp,8))[0])
        uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:
        writes.append([address,size,value]) if not 0x60000000<=address<0x60003000 else None)
    u.emu_start(0x2FB150,0,count=2000)
    assert u.reg_read(UC_X86_REG_RIP)==RETURN and u.reg_read(UC_X86_REG_RSP)==STACK+8
    assert checked==[True] and not writes
    assert all(u.reg_read(r)==v for r,v in saved.items())
    assert all(bytes(u.mem_read(p,4096))==data for p,data in snapshots.items())
    result = u.reg_read(UC_X86_REG_EAX)
    if result>=0x80000000: result-=0x100000000
    actual_slots = [c['slot'] for c in calls if c['va']==0x4686D0]
    expected_scan = [] if null_unit else list(range((result+1) if result>=0 else 10))
    assert scanned==expected_scan
    expected_call_ids = [] if null_unit else [0x265020,0x265090]+([0x3DA710] if actor_kind==3 else [])
    expected_call_ids += [a for slot in visited_slots for a in (0x4686D0,SQRT)]
    for c in calls:
        if c['va'] in (0x265020,0x265090): assert c['rcx']==ACTOR
        if c['va']==0x3DA710: assert c['rcx']==MOVE+0x50
        if c['va']==0x4686D0:
            assert c['a']==[10.,20.,30.]
            assert c['b']==list(next(xyz for slot,active,xyz in entries if slot==c['slot']))
    return dict(name=name,matches=result==expected and actual_slots==visited_slots and [c['va'] for c in calls]==expected_call_ids,
                result=result,expected=expected,scanned=scanned,calls=calls,visited=visits,
                input=dict(entries=entries,radii=radii,extra=extra,actor_kind=actor_kind,null_unit=null_unit,scratch=scratch),
                stop='returned',nonstack_writes=writes)

cases=[run('null-unit',[],-1,[],null_unit=True),run('no-presence',[],-1,[]),
 run('first-index-not-nearest',[(1,1,(12.,20.,30.)),(2,1,(10.,20.,30.))],1,[1]),
 run('last-slot',[(9,1,(12.,20.,30.))],9,[9]),
 run('exact-radius-excluded',[(0,1,(13.,20.,30.))],-1,[0]),
 run('extra-radius',[(0,1,(13.,20.,30.))],0,[0],extra=1.),
 run('larger-first-radius',[(0,1,(13.,20.,30.))],0,[0],radii=(4.,2.)),
 run('vertical-distance-ignored',[(0,1,(12.,9999.,30.))],0,[0]),
 run('inactive-slot-skipped',[(0,0,(10.,20.,30.)),(1,0x80,(12.,20.,30.))],1,[1]),
 run('class1-radius-unwritten-zero-scratch',[(0,1,(11.,20.,30.))],-1,[0],actor_kind=1,scratch=0),
 run('class1-radius-unwritten-large-scratch',[(0,1,(11.,20.,30.))],0,[0],actor_kind=1,scratch=0x40)]
assert all(c['matches'] for c in cases)
fault=run('mutant-includes-radius-equality',[(0,1,(13.,20.,30.))],-1,[0],mutant=True)
assert not fault['matches'] and fault['result']==0
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            method='six original bodies; controlled sqrtf and cookie dependencies; synthetic geometry and presence',imports=imports,cases=cases,equality_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for va,blob in BODIES.items():(HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for va,blob in BODIES.items() for i in cs.disasm(blob,va))+'\n')
print('PASS: eleven overlap controls; radius-equality mutation detected')

