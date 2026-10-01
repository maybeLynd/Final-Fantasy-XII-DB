"""Original procedural RNG helpers: exact state, scratch writes and binary32 arithmetic."""
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

ONE,BOUNDED=0x4005E0,0x3A6E60
STATE,MODE,SCRATCH,COPY=0x1EF93E8,0x22D9138,0x22D92E0,0x22D91A0
ONECOPY=0x22D8F90
STACK,STOP=0x60001800,0x70000000
BODIES={ONE:extract(ONE,108),BOUNDED:extract(BOUNDED,345)}
INIT,TAIL=0x259180,0x36C140
CALLS=[0x36C1D0,0x3CD6E0,0x3AC890,0x3B4790,0x376A80,0x24C970,0x3D7F10,0x3D8C30,0x3773C0,0x3B3E10,0x259250,0x39CD50,0x3A3670,0x375120,0x2FC200,0x3B0660,0x3B16B0,0x26F9F0,0x3B3160,0x3CBFF0,0x25A600]
BODIES[INIT]=extract(INIT,179)
CONSTANTS={a:extract(a,4) for a in (0x1CEBBA8,0x1EF93FC)}
assert all(b==bytes.fromhex('0000803f') for b in CONSTANTS.values())
CONSTANTS.update({a:extract(a,4) for a in [0x8C5F6C,0x8C5F78]})
assert CONSTANTS[0x8C5F6C].hex()=='cdcccc3d' and CONSTANTS[0x8C5F78].hex()=='00007a44'
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def bits(x):return struct.unpack('<I',struct.pack('<f',x))[0]
def floating(x):return struct.unpack('<f',struct.pack('<I',x))[0]
def signed(x):return x if x<0x80000000 else x-0x100000000
def cvtt(x):
    import math
    return (int(x)&0xFFFFFFFF) if math.isfinite(x) and -2147483648<=x<2147483648 else 0x80000000
def advance(s):return (((s&0x3FFFFF)|0x1FC00000)*2)|((((s>>18)^s)>>4)&1)

def run(name,seed=0,mode=0,bound=100,helper=BOUNDED,count=1,mutant=False,ret=0,early=False,tail_disable=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    addresses=[*BODIES,*CONSTANTS,*CALLS,TAIL,STATE,MODE,ONECOPY,STOP,0x2096ED0]
    for a in sorted({a&~4095 for a in addresses}):u.mem_map(a,4096)
    u.mem_map(0x60000000,0x3000)
    for a,b in {**BODIES,**CONSTANTS}.items():u.mem_write(a,b)
    for a in [*CALLS,TAIL]:u.mem_write(a,b'\xc3')
    if mutant:
        assert bytes(u.mem_read(0x259220,10))==bytes.fromhex('c7050eff070201000000')
        u.mem_write(0x259226,bytes(4))
    def put(a,v):u.mem_write(a,(v&0xFFFFFFFF).to_bytes(4,'little'))
    put(STATE,seed);put(MODE,mode)
    for i,x in enumerate((1.25,2.5,-3.5,4.75)):put(SCRATCH+i*4,bits(x))
    u.mem_write(COPY,b'\xa5'*16)
    pages={a:bytearray(u.mem_read(a,4096)) for a in sorted({STATE&~4095,MODE&~4095,ONECOPY&~4095,*[a&~4095 for a in CONSTANTS],0x2096ED0&~4095})}
    def pget(a):return int.from_bytes(pages[a&~4095][a&4095:(a&4095)+4],'little')
    def expected_write(ip,a,data):
        pages[a&~4095][a&4095:(a&4095)+len(data)]=data
        expected.append([ip,a,data.hex()])
    def w32(ip,a,v):expected_write(ip,a,(v&0xFFFFFFFF).to_bytes(4,'little'))
    events=[];pending=[];visited=[];reads=[]
    def flush():
        if not pending:return
        ip=pending[0][0];lo=min(a for _,a,n in pending);hi=max(a+n for _,a,n in pending)
        assert all(p==ip for p,a,n in pending)
        assert set(range(lo,hi))=={j for _,a,n in pending for j in range(a,a+n)}
        events.append([ip,lo,bytes(u.mem_read(lo,hi-lo)).hex()]);pending.clear()
    def snapshot():return [int.from_bytes(u.mem_read(x,4),'little') for x in [STATE,MODE,SCRATCH]]
    def code(uc,a,n,d):
        flush();visited.append(a)
        if a not in CALLS and a!=TAIL:return
        if a==CALLS[0]:args=[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)]
        elif a==0x3CBFF0:args=[uc.reg_read(UC_X86_REG_RCX)]
        elif a==0x25A600:args=[uc.reg_read(UC_X86_REG_XMM0)&0xFFFFFFFF,uc.reg_read(UC_X86_REG_XMM1)&0xFFFFFFFF]
        else:args=[]
        events.append(['stub',a,args,snapshot()])
        if early and a==CALLS[0]:
            put(STATE,0xDEADBEEF);put(MODE,9);events.append(['intervention','early',0xDEADBEEF,9])
        if tail_disable and a==TAIL:put(MODE,0);events.append(['intervention','tail-mode',0])
        for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
        for r in (UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5):uc.reg_write(r,0xBAD0BAD0)
        uc.reg_write(UC_X86_REG_EAX,ret)
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:pending.append([uc.reg_read(UC_X86_REG_RIP),a,n]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
    expected=[]
    before_values=[seed,mode,bits(1.25)]
    def oracle_put(a,v):pages[a&~4095][a&4095:(a&4095)+4]=(v&0xFFFFFFFF).to_bytes(4,'little')
    for a in CALLS:
        args=[8,10] if a==CALLS[0] else [0x2096ED0] if a==0x3CBFF0 else [0x3DCCCCCD,0x447A0000] if a==0x25A600 else []
        expected.append(['stub',a,args,before_values.copy()])
        if early and a==CALLS[0]:
            oracle_put(STATE,0xDEADBEEF);oracle_put(MODE,9);before_values=[0xDEADBEEF,9,bits(1.25)];expected.append(['intervention','early',0xDEADBEEF,9])
    for ip,a,v in [(0x25920C,SCRATCH,0x458DC800),(0x259216,STATE,0x458DC800),(0x259220,MODE,1)]:w32(ip,a,v)
    expected.append(['stub',TAIL,[],[0x458DC800,1,0x458DC800]])
    if tail_disable:oracle_put(MODE,0);expected.append(['intervention','tail-mode',0])
    for r,v in saved.items():u.reg_write(r,v)
    u.mem_write(STACK,STOP.to_bytes(8,'little'));u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(INIT,STOP,count=1000);flush()
    assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
    assert all(u.reg_read(r)==v for r,v in saved.items())
    same=all(bytes(u.mem_read(a,4096))==v for a,v in pages.items())
    init_result=dict(eax=u.reg_read(UC_X86_REG_EAX),events=events.copy(),expected_events=expected,visited=visited.copy(),reads=reads.copy(),snapshot=snapshot(),fixture_pages_match=same,matches=events==expected and same and u.reg_read(UC_X86_REG_EAX)==ret)
    results=[]
    for index in range(count):
        expected=[];events.clear();visited.clear();reads.clear()
        s=pget(STATE);enabled=bool(pget(MODE));b=signed(bound&0xFFFFFFFF)
        if helper==ONE:
            if enabled:s=advance(s);w32(0x400617,STATE,s)
            sample=floating(s) if enabled else 1.0
            w32(0x400625,SCRATCH,bits(sample))
            expected_write(0x400634,ONECOPY,bytes(pages[MODE&~4095][SCRATCH&4095:(SCRATCH&4095)+16]))
            answer=bits(f32(sample-1.0));naive=None
        else:
            if enabled:
                for _ in range(5):s=advance(s)
                w32(0x3A6F0C,STATE,s)
            sample=floating(s) if enabled else 1.0
            product=f32(sample*f32(b));difference=f32(product-f32(f32(b)*1.0))
            w32(0x3A6F39,COPY,bits(product));w32(0x3A6F45,SCRATCH,bits(difference))
            if enabled:
                for _ in range(2):s=advance(s)
                w32(0x3A6F8C,STATE,s)
            vector=[pget(SCRATCH+i*4) for i in range(4)]
            w32(0x3A6FA1,SCRATCH+16,bits(floating(s) if enabled else 1.0))
            expected_write(0x3A6FAD,SCRATCH,struct.pack('<4I',*[cvtt(floating(x)) for x in vector]))
            answer=cvtt(difference);naive=cvtt(f32(f32(sample-1.0)*f32(b)))
        for r,v in saved.items():u.reg_write(r,v)
        u.mem_write(STACK,STOP.to_bytes(8,'little'));u.reg_write(UC_X86_REG_RSP,STACK)
        u.reg_write(UC_X86_REG_ECX,bound&0xFFFFFFFF);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
        for r in (UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2):u.reg_write(r,0)
        u.emu_start(helper,STOP,count=500);flush()
        assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
        assert all(u.reg_read(r)==v for r,v in saved.items())
        actual=u.reg_read(UC_X86_REG_XMM0)&0xFFFFFFFF if helper==ONE else u.reg_read(UC_X86_REG_EAX)
        same=all(bytes(u.mem_read(a,4096))==v for a,v in pages.items())
        results.append(dict(index=index,answer=actual,expected_answer=answer,naive_answer=naive,state=int.from_bytes(u.mem_read(STATE,4),'little'),expected_state=pget(STATE),events=events.copy(),expected_events=expected,reads=reads.copy(),visited=visited.copy(),fixture_pages_match=same,matches=actual==answer and same and events==expected))
    return dict(name=name,helper=helper,seed=seed,mode=mode,bound=bound,count=count,stub_return=ret,early=early,tail_disable=tail_disable,initialization=init_result,results=results,matches=init_result['matches'] and all(r['matches'] for r in results))

cases=[run('cold-init-draw'),run('dirty-init',seed=0xFFFFFFFF,mode=2),run('stub-return',ret=0xFFFFFFFF),run('early-writes-overwritten',early=True),run('tail-disables',tail_disable=True),run('zero-bound',bound=0),run('negative-bound',bound=-100),run('rounding-bound',bound=1000000000),run('one-step-first',helper=ONE)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-initializes-disabled',mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in {**BODIES,**CONSTANTS}.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} native initialization/draw controls; disabled-init mutant detected')
