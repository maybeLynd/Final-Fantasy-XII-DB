"""Original loot caller dispatch segment; full caller retained for context."""
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

CALLER=0x310DB0
BODIES={CALLER:extract(CALLER,0x3112EA-CALLER),0x3273B0:extract(0x3273B0,28),0x3590D0:extract(0x3590D0,7),
        0x265680:extract(0x265680,149)}
# Scan is a bounded raw direct-E8 census, not an indirect-call or reachability proof.
candidates=[]
for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
    off=table+40*n
    if raw[off:off+8].rstrip(b'\0')==b'.text':
        _,rva,length,disk=struct.unpack_from('<4I',raw,off+8)
        section=raw[disk:disk+length]
        for i in range(len(section)-4):
            if section[i]==0xE8 and base+rva+i+5+struct.unpack_from('<i',section,i+1)[0]==0x2FB150:
                candidates.append(base+rva+i)
assert candidates==[0x311105]
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
decoded={i.address:i for i in cs.disasm(BODIES[CALLER],CALLER)}
assert decoded[0x311105].mnemonic=='call' and decoded[0x311105].op_str=='0x2fb150'
UNIT,STATS,STACK,FOCUS=0x50000000,0x50001000,0x60000800,0x22C7FE0
OVERLAP,PREP,GRANT,REMOVE,SKIP=0x2FB150,0x469E30,0x319A00,0x319830,0x311289

def run(name,focus,action,hit,kind,expected,mutation=None,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages={v&~4095 for v in list(BODIES)+[0x3112E9,FOCUS,UNIT,STATS,OVERLAP,PREP,GRANT,REMOVE,0x1CEBBA8]}
    for p in sorted(pages):u.mem_map(p,4096)
    u.mem_map(0x60000000,0x2000)
    for va,blob in BODIES.items():
        if mutant and va==CALLER:
            at=0x311136-CALLER
            assert blob[at:at+2]==b'\x0F\x85'
            blob=blob[:at]+b'\x0F\x84'+blob[at+2:]
        u.mem_write(va,blob)
    u.mem_write(FOCUS,struct.pack('<I',0x1234 if focus else 0x5678))
    u.mem_write(0x1CEBBA8,extract(0x1CEBBA8,4))
    u.mem_write(UNIT+8,struct.pack('<I',0x1234))
    u.mem_write(UNIT+0x698,struct.pack('<Q',STATS))
    u.mem_write(UNIT+0x714,struct.pack('<H',action))
    u.mem_write(STATS+5,bytes([kind]))
    before={p:bytes(u.mem_read(p,4096)) for p in (UNIT,STATS,FOCUS&~4095)}
    u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RSI,UNIT)
    calls=[];visits=[];writes=[];interventions=[];stops=[]
    def step(uc,address,size,data):
        visits.append(address)
        if address in (GRANT,REMOVE,SKIP):
            args=[] if address==SKIP else [uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)]
            stops.append(dict(va=address,args=args));uc.emu_stop();return
        if address==0x3273B0:calls.append(dict(va=address,args=[uc.reg_read(UC_X86_REG_ECX)],method='original'))
        if address==0x3590D0:calls.append(dict(va=address,args=[],method='original'))
        if address not in (OVERLAP,PREP):return
        if address==OVERLAP:
            arg=struct.unpack('<f',struct.pack('<I',uc.reg_read(UC_X86_REG_XMM1)&0xFFFFFFFF))[0]
            calls.append(dict(va=address,args=[uc.reg_read(UC_X86_REG_RCX),arg],result=hit,method='controlled'))
            uc.reg_write(UC_X86_REG_EAX,hit&0xFFFFFFFF)
        else:
            calls.append(dict(va=address,args=[uc.reg_read(UC_X86_REG_RCX)],method='controlled'))
            if mutation=='null-stats':
                uc.mem_write(UNIT+0x698,b'\0'*8);interventions.append(dict(address=UNIT+0x698,bytes=8,value=0))
            if mutation=='kind-one':
                uc.mem_write(STATS+5,b'\x01');interventions.append(dict(address=STATS+5,bytes=1,value=1))
            uc.reg_write(UC_X86_REG_RAX,0xBADF00D)
        rsp=uc.reg_read(UC_X86_REG_RSP)
        uc.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',uc.mem_read(rsp,8))[0]);uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:
        writes.append([address,size,value]) if not 0x60000000<=address<0x60002000 else None)
    u.emu_start(0x3110DC,0,count=300)
    assert len(stops)==1 and not writes
    assert u.reg_read(UC_X86_REG_RSP)==(STACK if stops[0]['va']==SKIP else STACK-8)
    expected_pages={p:bytearray(b) for p,b in before.items()}
    for w in interventions:expected_pages[w['address']&~4095][w['address']&4095:(w['address']&4095)+w['bytes']]=w['value'].to_bytes(w['bytes'],'little')
    assert all(bytes(u.mem_read(p,4096))==bytes(b) for p,b in expected_pages.items())
    expected_calls=[dict(va=0x3273B0,args=[0x1234],method='original'),dict(va=0x3590D0,args=[],method='original')]
    if focus or action==0x4165:
        expected_calls.append(dict(va=OVERLAP,args=[UNIT,1.0],result=hit,method='controlled'))
        if hit>=0:expected_calls.append(dict(va=PREP,args=[STATS],method='controlled'))
    expected_stop=dict(va=expected,args=[] if expected==SKIP else [hit,0x1234])
    return dict(name=name,matches=calls==expected_calls and stops==[expected_stop],calls=calls,stop=stops,
                interventions=interventions,original_writes=writes,visited=visits,
                fixture=dict(focus=focus,action=action,hit=hit,kind=kind,mutation=mutation),
                expected_stop=expected_stop)

cases=[run('not-focus-no-action',False,0,-1,0,SKIP),run('focus-no-hit',True,0,-1,0,SKIP),
 run('action4165-allows-unfocused',False,0x4165,3,0,GRANT),run('adjacent-action-rejected',False,0x4164,3,0,SKIP),
 run('focused-grant',True,0,9,0,GRANT),run('nonzero-kind-removes',True,0,2,1,REMOVE),
 run('preparation-clears-stats',True,0,2,0,REMOVE,mutation='null-stats'),
 run('preparation-changes-kind',True,0,2,0,REMOVE,mutation='kind-one'),
 run('any-negative-hit-skips',True,0,-2147483648,0,SKIP)]
assert all(c['matches'] for c in cases)
fault=run('mutant-reverses-kind-branch',True,0,2,0,GRANT,mutant=True)
assert not fault['matches'] and fault['stop'][0]['va']==REMOVE
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 method='original immediate caller segment and focus predicate/getter; controlled overlap/preparation; stop before grant/remove',
 direct_e8_candidates=candidates,cases=cases,kind_branch_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for va,blob in BODIES.items():(HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for va,blob in BODIES.items() for i in cs.disasm(blob,va))+'\n')
print('PASS: nine caller dispatch controls; reversed kind branch detected')
