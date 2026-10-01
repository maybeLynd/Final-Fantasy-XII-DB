"""Original action MP cost, modifier and pointer resolver with synthetic tables."""
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



COST,MOD,CHANNEL,RESOLVE=0x309110,0x2F95D0,0x2F9820,0x20E600
UNIT,STATS,HEAD,EHEAD,BASE,ROWS,EROWS,STACK,STOP=0x50000100,0x50001000,0x50002000,0x50002020,0x40000000,0x40010000,0x40020000,0x60001800,0x70000000
BODIES={a:extract(a,n) for a,n in [(COST,165),(MOD,589),(CHANNEL,51),(RESOLVE,10)]}
CONSTANTS={a:extract(a,4) for a in (0x8F3130,0x8F3134,0x916318)}
assert [struct.unpack('<f',CONSTANTS[a])[0] for a in CONSTANTS]==[50.0,100.0,64.0]
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]

def run(name,action=12,cost=31,category=0,kind=0,effects=(),percent=(10,15,20),unit=UNIT,header=True,stats=True,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for a in sorted({v&~4095 for v in [*BODIES,*CONSTANTS,0x2EBF138,0x1F83530,STOP]}):u.mem_map(a,4096)
    for a,n in [(BASE,0x30000),(UNIT&~4095,0x4000),(0x60000000,0x3000)]:u.mem_map(a,n)
    for a,b in {**BODIES,**CONSTANTS}.items():u.mem_write(a,b)
    if mutant:
        assert bytes(u.mem_read(0x309128,2))==bytes.fromhex('777e');u.mem_write(0x309128,b'\x73')
    def put(a,n,v):u.mem_write(a,(v&((1<<(n*8))-1)).to_bytes(n,'little'))
    u.mem_write(UNIT&~4095,b'\xA5'*0x4000)
    put(0x1F83530,8,BASE);put(0x2EBF138,8,HEAD if header else 0);put(0x2EBF040,8,EHEAD)
    put(HEAD+8,2,0x40);put(HEAD+0xC,4,0x10000);put(EHEAD+8,2,8);put(EHEAD+0xC,4,0x20000)
    aid=action&0xFFFF
    if aid<=0x21E:put(ROWS+aid*0x40+0xA,1,cost);put(ROWS+aid*0x40+0x1E,1,category)
    put(UNIT+0x698,8,STATS if stats else 0);put(STATS+5,1,kind)
    for off in (0x6C,0x7C,0x6E,0x7E,0x73,0x83):put(STATS+off,1,0)
    for off,mask in effects:put(STATS+off,1,int.from_bytes(u.mem_read(STATS+off,1),'little')|mask)
    for i,v in enumerate(percent):put(EROWS+(0x5B+i)*8+4,2,v)
    put(STACK,8,STOP)
    pages={a:bytes(u.mem_read(a,n)) for a,n in [(BASE,0x30000),(UNIT&~4095,0x4000),(0x2EBF000,4096),(0x1F83000,4096)]}
    expected=[]
    def call(a,args):expected.append([a,args])
    def resolve():call(RESOLVE,[0x10000]);call(RESOLVE,[0x10000])
    masks=dict()
    for off,mask in effects:masks[off]=masks.get(off,0)|mask
    def effect(off,mask):return bool((masks.get(off,0)|masks.get(off+0x10,0))&mask)
    fault=None;value=0;call(COST,[unit,action&0xFFFFFFFF])
    if aid<=0x21E:
        if not header:fault=0x1E
        else:
            resolve()
            if category not in (5,6):
                if not unit:value=cost
                else:
                    call(CHANNEL,[unit])
                    if not stats:fault=0x6C
                    elif kind!=1 and effect(0x6C,1):value=0
                    else:
                        call(MOD,[unit,aid]);resolve()
                        if kind!=1 and (0xD0<=aid<=0xE1 or 0x106<=aid<=0x112):value=cost
                        elif effect(0x6C,1):value=int(f32(f32(cost*64.0)/50.0))*10
                        else:
                            reduction=0
                            for bit,p in zip((8,16,32),percent):
                                if effect(0x73,bit):call(RESOLVE,[0x20000]);call(RESOLVE,[0x20000]);reduction+=p
                            value=int(f32(f32(cost)-f32(f32(f32(cost)/100.0)*f32(reduction))))
                            if effect(0x6E,8):value=0
                            elif effect(0x6C,16):value=int(value/2)
    events=[];writes=[];reads=[];visits=[];invalid=[]
    widths={COST:2,MOD:2,CHANNEL:1,RESOLVE:1}
    def step(uc,a,n,d):
        visits.append(a)
        if a in widths:
            regs=[UC_X86_REG_ECX] if a==RESOLVE else [UC_X86_REG_RCX,UC_X86_REG_EDX]
            events.append([a,[uc.reg_read(r) for r in regs[:widths[a]]]])
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    def bad(uc,t,a,n,v,d):invalid.append([t,a,n]);return False
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
    saved={r:0x12340000+n for n,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
    for r,v in saved.items():u.reg_write(r,v)
    for r,v in [(UC_X86_REG_RCX,unit),(UC_X86_REG_EDX,action&0xFFFFFFFF),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
    error=None
    try:u.emu_start(COST,STOP,count=2000)
    except unicorn.UcError as ex:error=str(ex)
    eax=u.reg_read(UC_X86_REG_EAX)
    if fault is None:
        assert error is None and u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8, (name,error,hex(u.reg_read(UC_X86_REG_RIP)),invalid,visits[-8:])
        assert all(u.reg_read(r)==v for r,v in saved.items())
        match=eax==(value&0xFFFFFFFF) and not invalid
    else:match=error is not None and len(invalid)==1 and invalid[0][1]==fault
    match=match and events==expected and not writes and all(bytes(u.mem_read(a,len(b)))==b for a,b in pages.items())
    return dict(name=name,action=action,cost=cost,category=category,kind=kind,effects=effects,percent=percent,unit=unit,header=header,stats=stats,expected_value=value,expected_fault=fault,eax=eax,events=events,expected_events=expected,writes=writes,reads=reads,invalid=invalid,error=error,stop=u.reg_read(UC_X86_REG_RIP),visited=visits,matches=match)

cases=[run('base'),run('no-unit',unit=0),run('upper-id',action=0x21E),run('over-upper',action=0x21F),run('id-low16',action=0x1021E),run('category5',category=5),run('category6',category=6),run('category7',category=7),run('channel-layer0',effects=((0x6C,1),)),run('channel-layer1',effects=((0x7C,1),)),run('kind1-special-cost',kind=1,effects=((0x6C,1),)),run('reduce91',effects=((0x73,8),)),run('reduce92-layer1',effects=((0x83,16),)),run('reduce93',effects=((0x73,32),)),run('reduce-combined',effects=((0x73,8),(0x83,48))),run('half',effects=((0x6C,16),)),run('half-after-reduction',effects=((0x73,56),(0x7C,16))),run('zero-cost-layer0',effects=((0x6E,8),)),run('zero-cost-layer1',effects=((0x7E,8),)),run('over-reduction-negative-half',effects=((0x73,56),(0x6C,16)),percent=(80,80,80))]
for a in (0xCF,0xD0,0xE1,0xE2,0x105,0x106,0x112,0x113):cases.append(run(f'range-{a:X}',action=a,effects=((0x6E,8),)))
cases+=[run('kind1-no-range-bypass',action=0xD0,kind=1,effects=((0x6E,8),)),run('missing-header',header=False),run('missing-stats',stats=False)]
assert all(c['matches'] for c in cases),[(c['name'],c['eax'],c['expected_value'],c['events'],c['expected_events'],c['invalid']) for c in cases if not c['matches']]
fault=run('mutant-upper-exclusive',action=0x21E,mutant=True);assert not fault['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,upper_bound_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in {**BODIES,**CONSTANTS}.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} original MP cost controls; exclusive-upper-bound mutant detected')
