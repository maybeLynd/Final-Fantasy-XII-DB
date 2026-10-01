"""Original UI router with original policy and switch tables; controlled callees."""
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







ENTRY,POLICY=0x254B50,0x2E0FA0
PRE=(0x17E7D0,0x35DA80,0x3C8990)
GENERIC,RESET=0x280A00,0x28F970
SPECIAL={1:0x35D660,4:0x35D660,3:0x35D980,5:0x3C87B0,12:0x28E970,24:0x35D080}
GATE,STACK,STOP=0x2092734,0x60001800,0x70000000
CODE=extract(ENTRY,263)
DATA={a:extract(a,n) for a,n in [(0x1E0C2C0,88),(0x254C58,24),(0x254C70,24)]}
# Independently transcribed policy and route oracle, not derived from the executed tables.
MASKS=[4,42,8,4,0,32,16384,0,2097154,16416,8]+[0]*11
assert list(struct.unpack('<22I',DATA[0x1E0C2C0]))==MASKS
assert [base+x for x in struct.unpack('<6I',DATA[0x254C58])]==[0x254BFB,0x254C04,0x254C0D,0x254C16,0x254C24,0x254C2D]
assert list(DATA[0x254C70])==[0,5,1,0,2,5,5,5,5,5,5,3,5,5,5,5,5,5,5,5,5,5,5,4]

SETTER,PRELUDE,FACTORY,FINAL,COOKIE=0x252B40,0x254740,0x244F50,0x28E860,0x808C40
ROOTPTR,ROOT,COOKIEPTR,COOKIEVALUE=0x209AC30,0x50000000,0x1F44830,0x123456789ABC
ID0,ID1=0x2092730,0x20927D8
PAYLOAD,DESC=STACK-0x68,STACK-0x58
BODIES={ENTRY:CODE,GENERIC:extract(GENERIC,193),SETTER:extract(SETTER,29)}

def run(name,request=2,param=0x12345678,flag=0x87654321,gate=0,policy=0,busy=0,ret=0,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    stubs={POLICY,*PRE,RESET,*SPECIAL.values(),PRELUDE,FACTORY,FINAL,COOKIE}
    for p in sorted({a&~4095 for a in [*BODIES,*DATA,*stubs,GATE,ROOTPTR,ROOT,COOKIEPTR,STOP]}):u.mem_map(p,4096)
    u.mem_map(0x60000000,0x3000);u.mem_write(0x60000000,b'\xa5'*0x3000)
    for a,b in {**BODIES,**DATA}.items():u.mem_write(a,b)
    for a in stubs:u.mem_write(a,b'\xc3')
    if mutant:
        assert bytes(u.mem_read(0x280A3C,5))==bytes.fromhex('ba01000000')
        u.mem_write(0x280A3C,bytes.fromhex('ba00000000'))
    def put(a,n,v):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
    def get(a,n=4):return int.from_bytes(u.mem_read(a,n),'little')
    put(ROOTPTR,8,ROOT);put(ROOT+0xC0,8,busy);put(COOKIEPTR,8,COOKIEVALUE)
    put(GATE,4,gate);put(ID0,4,0xAAAAAAAA);put(ID1,4,0xBBBBBBBB)
    pages={a:bytearray(u.mem_read(a,4096)) for a in [GATE&~4095,ROOTPTR&~4095,ROOT,COOKIEPTR&~4095,0x1E0C000]}
    def globals_now():return [get(GATE),get(ID0),get(ID1)]
    expected_globals=[gate,0xAAAAAAAA,0xBBBBBBBB]
    events=[];reads=[];visited=[]
    def hook(uc,a,n,d):
        visited.append(a)
        if a in (ENTRY,GENERIC):
            events.append(['entry',a,[uc.reg_read(r) for r in (UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_R8D)]])
        elif a==SETTER:events.append(['entry',a,[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)]])
        if a not in stubs:return
        assert a not in SPECIAL.values(),'test escaped the intended generic route'
        if a==PRELUDE:events.append(['stub',a,[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)],globals_now()])
        elif a==FACTORY:
            p=uc.reg_read(UC_X86_REG_R8);rawdesc=bytes(uc.mem_read(p,24));pp=int.from_bytes(rawdesc[8:16],'little')
            packet=[p,int.from_bytes(rawdesc[:4],'little'),rawdesc[4:8].hex(),pp,int.from_bytes(rawdesc[16:24],'little'),list(struct.unpack('<4I',u.mem_read(pp,16)))]
            events.append(['stub',a,[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_RDX)],packet,globals_now()])
        elif a==COOKIE:events.append(['stub',a,[uc.reg_read(UC_X86_REG_RCX)]]);return
        else:events.append(['stub',a,[]])
        for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
        uc.reg_write(UC_X86_REG_EAX,policy if a==POLICY else ret)
    u.hook_add(unicorn.UC_HOOK_CODE,hook)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:events.append(['write',uc.reg_read(UC_X86_REG_RIP),a,n,v]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
    inputs=[[request&0xFFFFFFFF,param&0xFFFFFFFF,flag&0xFFFFFFFF],[6,0xABCDEF01,0x13579BDF]]
    steps=[]
    for args in inputs:
        events.clear();reads.clear();visited.clear()
        rid=args[0]&0x7FFF;mask=0
        for i,m in enumerate(MASKS):
            if policy&(1<<i):mask|=m
        expected=[['entry',ENTRY,args]];answer=0
        if expected_globals[0]!=1:
            expected.append(['stub',POLICY,[]])
            if not(mask&(1<<(rid&31))):
                assert rid not in SPECIAL
                expected += [['stub',a,[]] for a in (*PRE,RESET)]
                expected.append(['entry',GENERIC,args])
                if not busy:
                    expected.append(['entry',SETTER,[args[0],1]])
                    for ip,a,v in [(0x252B46,GATE,1),(0x252B4C,ID1,rid),(0x252B52,ID0,rid)]:
                        expected.append(['write',ip,a,4,v]);pages[GATE&~4095][a&4095:(a&4095)+4]=v.to_bytes(4,'little')
                    expected_globals=[1,rid,rid]
                    expected.append(['stub',PRELUDE,[rid,1],expected_globals.copy()])
                    token=args[0] if args[0]<0x80000000 else args[0]|0xFFFFFFFF00000000
                    for proc in (0x27FB70,0x280140):
                        expected.append(['stub',FACTORY,[0xD8,proc],[DESC,0,'a5a5a5a5',PAYLOAD,token,args+[0]],expected_globals.copy()])
                    expected.append(['stub',FINAL,[]]);answer=1
                expected.append(['stub',COOKIE,[COOKIEVALUE]])
        for r,v in saved.items():u.reg_write(r,v)
        put(STACK,8,STOP)
        for r,v in zip((UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_R8D),args):u.reg_write(r,v)
        u.reg_write(UC_X86_REG_RSP,STACK)
        u.emu_start(ENTRY,STOP,count=2000)
        assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
        assert all(u.reg_read(r)==v for r,v in saved.items())
        eax=u.reg_read(UC_X86_REG_EAX);same=all(bytes(u.mem_read(a,4096))==b for a,b in pages.items())
        steps.append(dict(arguments=args,eax=eax,expected_return=answer,globals=globals_now(),expected_globals=expected_globals.copy(),events=events.copy(),expected_events=expected,reads=reads.copy(),visited=visited.copy(),fixture_pages_match=same,matches=events==expected and eax==answer and globals_now()==expected_globals and same))
    return dict(name=name,initial_gate=gate,policy=policy,busy_c0=busy,stub_return=ret,steps=steps,matches=all(s['matches'] for s in steps))

cases=[run('accepted-then-gated'),run('high-request',request=0x8002),run('negative-request',request=-1),run('out-of-range',request=25),run('zero-parameter',param=0,flag=0),run('parameter-one',param=1),run('initial-gate-one',gate=1),run('initial-gate-two',gate=2),run('busy-root',busy=1),run('policy-refusal-then-admission',policy=1),run('callee-return-ignored',ret=0xFFFFFFFF)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-posts-zero-gate',mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in {**BODIES,**DATA}.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} two-call native feedback controls; gate-post mutant detected')
