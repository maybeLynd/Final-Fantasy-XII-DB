"""Original copy-out, dispatch and MP writer composition in one synthetic memory state."""
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


COPY,COPYSTOP,APPLY,APPLYSTOP=0x38643F,0x3866C1,0x311608,0x311778
MP,ABS,SEC,REC,NOOP=0x300CE0,0x300C90,0x300BC0,0x30E060,0x16D6A0
OWNER,GLOBAL,ELIG=0x31B860,0x30B770,0x30B7F0
SCRATCH,RESULT,TARGET,SOURCE,STACK=0x2AEDFB8,0x50000100,0x50000400,0x50000800,0x60001800
BODIES={a:extract(a,n) for a,n in [(COPY,COPYSTOP-COPY),(0x3112F0,2040),(MP,351),(ABS,73),(SEC,207),(REC,200),(NOOP,3)]}
NONE=0xFFFFFFFF
TM0,TM1,SM0,SM1,SMABS,TMABS=0x54,0x58,0x64,0x68,0x70,0x78
def sx(v,b):return v-(1<<b) if v&(1<<(b-1)) else v
def u32(v):return v&NONE

def run(name,inputs,private=0,source=SOURCE,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for page in sorted({a&~4095 for a in [*BODIES,OWNER,GLOBAL,ELIG,RESULT]}):u.mem_map(page,4096)
    u.mem_map(SCRATCH&~4095,8192);u.mem_map(0x60000000,0x3000)
    for a,b in BODIES.items():u.mem_write(a,b)
    if mutant:
        assert bytes(u.mem_read(0x311673,4))==bytes.fromhex('0fbf532a');u.mem_write(0x311674,b'\xb7')
    u.mem_write(SCRATCH&~4095,b'\xA5'*8192);u.mem_write(RESULT&~4095,b'\x5A'*4096)
    vals={k:0 for k in range(0,0xA8,4)};vals.update({k:NONE for k in range(0x4C,0x94,4)});vals.update(inputs);vals[0x44]=max(private,0);vals[0x40]=max(-private,0)
    def rawput(a,n,v):u.mem_write(a,(v&((1<<(n*8))-1)).to_bytes(n,'little'))
    for k,v in vals.items():rawput(SCRATCH+k,4,v)
    rawput(RESULT+0x2C,4,0);rawput(STACK+0x38,4,0)
    for p,live,sec in [(TARGET,40,80),(SOURCE,70,50)]:
        for off,n,v in [(6,2,sec),(0x28,2,100),(0x37,1,3),(0x4C,2,live),(0x4E,1,0),(0x6C,1,0),(0x7C,1,0)]:rawput(p+off,n,v)
    pages={SCRATCH&~4095:bytearray(u.mem_read(SCRATCH&~4095,8192)),RESULT&~4095:bytearray(u.mem_read(RESULT&~4095,4096))}
    initial={str(p):bytes(b).hex() for p,b in pages.items()}
    def put(a,n,v):
        p=next(p for p,b in pages.items() if p<=a<a+n<=p+len(b));pages[p][a-p:a-p+n]=(v&((1<<(8*n))-1)).to_bytes(n,'little')
    def get(a,n):
        p=next(p for p,b in pages.items() if p<=a<a+n<=p+len(b));return int.from_bytes(pages[p][a-p:a-p+n],'little')
    flag=0
    for sub,add,absolute,pres,added,diff,ab in [(TM0,TM1,TMABS,14,16,12,4),(SM0,SM1,SMABS,13,15,11,2)]:
        if any(vals[k]!=NONE for k in (sub,add,absolute)):flag|=1<<pres
        if vals[add]!=NONE:flag|=1<<added
        if vals[sub]!=NONE or vals[add]!=NONE:flag|=1<<diff
        if vals[absolute]!=NONE:flag=(flag|(1<<ab))&~(1<<diff)
    for off in (0x4C,0x50,0x54,0x58,0x5C,0x60,0x64,0x68):put(SCRATCH+off,4,0 if vals[off]==NONE else vals[off])
    put(RESULT+0x2C,4,flag);put(RESULT+0x1D,1,private);put(RESULT+0x24,4,0);put(RESULT+0x20,4,0)
    for sub,add,absolute,off in [(TM0,TM1,TMABS,0x2A),(SM0,SM1,SMABS,0x28)]:
        value=vals[absolute] if vals[absolute]!=NONE else (0 if vals[add]==NONE else vals[add])-(0 if vals[sub]==NONE else vals[sub])
        put(RESULT+off,2,value)
    events=[];visits=[];phase='copy'
    widths={MP:3,ABS:3,SEC:3,REC:2,NOOP:2,OWNER:1,GLOBAL:0,ELIG:2}
    def hook(uc,a,n,data):
        visits.append([phase,a])
        if a not in widths:return
        regs=(UC_X86_REG_RCX,UC_X86_REG_EDX,UC_X86_REG_R8D)
        events.append(['call',a,[uc.reg_read(r) for r in regs[:widths[a]]]])
        if a not in (OWNER,GLOBAL,ELIG):return
        for r in (UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBADF00D)
        uc.reg_write(UC_X86_REG_RAX,0)
        rsp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,int.from_bytes(uc.mem_read(rsp,8),'little'));uc.reg_write(UC_X86_REG_RSP,rsp+8)
    def onwrite(uc,t,a,n,v,d):
        if not 0x60000000<=a<0x60003000:events.append(['write',a,n,v&((1<<(8*n))-1)])
    u.hook_add(unicorn.UC_HOOK_CODE,hook);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
    u.reg_write(UC_X86_REG_RBX,RESULT);u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(COPY,COPYSTOP,count=500)
    assert u.reg_read(UC_X86_REG_RIP)==COPYSTOP and u.reg_read(UC_X86_REG_RSP)==STACK and u.reg_read(UC_X86_REG_RBX)==RESULT
    assert all(bytes(u.mem_read(p,len(b)))==bytes(b) for p,b in pages.items())
    after_copy={str(p):bytes(u.mem_read(p,len(b))).hex() for p,b in pages.items()}
    copy_events=events[:];events.clear();expected=[]
    def call(a,args):expected.append(['call',a,args])
    def write(a,n,v):expected.append(['write',a,n,v&((1<<(8*n))-1)]);put(a,n,v)
    def owner(p):call(OWNER,[p])
    def gates():call(GLOBAL,[]);call(ELIG,[0,0])
    def rec(p,f):
        call(REC,[p,f]);owner(p);old=get(p+0x4E,1);tier=int(sx(get(p+6,2),16)/100)
        if not(f&2) and old!=tier:call(NOOP,[p,u32(tier-old)])
        write(p+0x4E,1,tier)
    def sec(p,d,f):
        call(SEC,[p,u32(d),f]);owner(p);gates();write(p+6,2,max(0,min(300,sx(get(p+6,2),16)+d)));rec(p,f)
    def mp(p,d,f):
        call(MP,[p,u32(d),f]);owner(p);gates()
        if d<0:gates()
        write(p+0x4C,2,max(0,min(100,sx(get(p+0x4C,2),16)+d)))
        if d>0:sec(p,d,f)
    def absolute(p,v,f):
        call(ABS,[p,u32(v),f]);mp(p,v-sx(get(p+0x4C,2),16),f)
        now=sx(get(p+6,2),16)
        if v>now:sec(p,v-now,f)
    target_flags=(((flag>>16)&1)<<5)|((1-((flag>>12)&1))<<4)
    source_flags=(((flag>>15)&1)<<5)|((1-((flag>>11)&1))<<4)
    if flag&(1<<14):(absolute if flag&16 else mp)(TARGET,sx(get(RESULT+0x2A,2),16),target_flags)
    if private&255:sec(TARGET,100*sx(private&255,8),target_flags|(0x400 if private&128 else 0))
    if source and flag&(1<<13):(absolute if flag&4 else mp)(source,sx(get(RESULT+0x28,2),16),source_flags)
    # Explicit phase bridge: keep original scratch/result/stats bytes; install only parent-frame roles.
    rawput(STACK+0x88,8,source)
    for r,v in [(UC_X86_REG_RDI,TARGET),(UC_X86_REG_R12,0x300530),(UC_X86_REG_R15,MP),(UC_X86_REG_R13,0),(UC_X86_REG_R14,0)]:u.reg_write(r,v)
    phase='apply';u.emu_start(APPLY,APPLYSTOP,count=3000)
    assert u.reg_read(UC_X86_REG_RIP)==APPLYSTOP and u.reg_read(UC_X86_REG_RSP)==STACK and u.reg_read(UC_X86_REG_RBX)==RESULT and u.reg_read(UC_X86_REG_RDI)==TARGET
    final={str(p):bytes(u.mem_read(p,len(b))).hex() for p,b in pages.items()}
    return dict(name=name,inputs=inputs,private=private,source=source,initial_pages=initial,after_copy_pages=after_copy,copy_events=copy_events,expected_pages={str(p):bytes(b).hex() for p,b in pages.items()},final_pages=final,expected_events=expected,events=events,visited=visits,matches=events==expected and all(bytes(u.mem_read(p,len(b)))==bytes(b) for p,b in pages.items()))

cases=[run('absent',{}),run('explicit-zero',{TM1:0,SM1:0}),run('target-gain-source-spend',{TM1:30,SM0:25}),run('overrides-win',{TM0:90,TM1:2,TMABS:80,SM1:20,SMABS:10}),run('word-sign-boundary',{TM1:0x18001,SM1:0x10002}),run('null-source',{TM1:5,SM1:25},source=0),run('secondary-positive',{TM1:30},private=1),run('secondary-negative',{TM1:30},private=-1),run('absolute-zero',{TMABS:0,SMABS:0})]
assert all(c['matches'] for c in cases),[(c['name'],c['events'],c['expected_events']) for c in cases if not c['matches']]
fault=run('mutant-zero-extends-target-word',{TM1:0x18001,SM1:0x10002},mutant=True);assert not fault['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,sign_extension_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} copy-out/dispatch/native-MP compositions; sign-extension mutant detected')
