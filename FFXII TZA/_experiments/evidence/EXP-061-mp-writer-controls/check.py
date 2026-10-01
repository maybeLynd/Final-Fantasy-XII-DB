"""Original MP and secondary-resource writes with controlled native dependencies."""
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

MP,ABS,SEC,REC,NOOP=0x300CE0,0x300C90,0x300BC0,0x30E060,0x16D6A0
OWNER,GLOBAL,ELIG,REACTION,NUMBER,CLEAR=0x31B860,0x30B770,0x30B7F0,0x3283D0,0x28F1F0,0x2FA540
STATS,UNIT,STACK,STOP=0x50000100,0x50000800,0x60001800,0x70000000
BODIES={a:extract(a,n) for a,n in [(MP,351),(ABS,73),(SEC,207),(REC,200),(NOOP,3)]}
def sx(v,b):return v-(1<<b) if v&(1<<(b-1)) else v
def u32(v):return v&0xFFFFFFFF

def run(name,entry=MP,delta=20,flags=0,live=40,secondary=100,cap=100,mult=3,tier=1,effects=(0,0),owner=UNIT,gm=(),um=(),mutant=False):
    initial=bytearray(b'\xA5'*4096)
    def put(buf,off,n,v):buf[0x100+off:0x100+off+n]=(v&((1<<(8*n))-1)).to_bytes(n,'little')
    for off,n,v in [(6,2,secondary),(0x28,2,cap),(0x37,1,mult),(0x4C,2,live),(0x4E,1,tier),(0x6C,1,effects[0]),(0x7C,1,effects[1])]:put(initial,off,n,v)
    initial[0x808:0x80C]=(0xAABBCCDD).to_bytes(4,'little')
    expected=bytearray(initial);events=[];gi=ui=0
    def get(off,n):return int.from_bytes(expected[0x100+off:0x100+off+n],'little')
    def call(a,args):events.append(['call',a,args])
    def write(off,n,v):events.append(['write',STATS+off,n,v&((1<<(n*8))-1)]);put(expected,off,n,v)
    def ownercall():call(OWNER,[STATS])
    def gates():
        nonlocal gi,ui
        call(GLOBAL,[]);g=gm[gi] if gi<len(gm) else 0;gi+=1
        call(ELIG,[owner,0]);v=um[ui] if ui<len(um) else 0;ui+=1
        return g,v
    def blocked():return bool(get(0x6C,1)&128 or get(0x7C,1)&128)
    def reconcile(f):
        call(REC,[STATS,u32(f)]);ownercall();maximum=sx(get(0x28,2),16)
        if maximum<=0:return
        old=get(0x4E,1);new=int(sx(get(6,2),16)/maximum) if get(0x37,1)>0 else 0
        if not(f&2) and old!=new:call(NOOP,[STATS,u32(new-old)])
        if f&0x410==0x400 and owner and old!=new:call(REACTION,[owner,u32(new-old),int(new>old),1])
        write(0x4E,1,new)
    def sec(d,f):
        call(SEC,[STATS,u32(d),u32(f)]);ownercall()
        if not(f&1):
            g,v=gates()
            if (g|v)&0xFFFF:return
        total=sx(u32(sx(get(6,2),16)+d),32)
        maximum=0 if blocked() else sx(get(0x28,2),16)*(get(0x37,1) or 1)
        value=0 if total<0 else min(total,maximum)
        write(6,2,value);reconcile(f)
    def primary(d,f):
        call(MP,[STATS,u32(d),u32(f)]);ownercall()
        if not(f&1):
            g,v=gates()
            if (g|v)&0xFFFF:return
        old=sx(get(0x4C,2),16);total=sx(u32(old+d),32)
        maximum=0 if blocked() else sx(get(0x28,2),16)
        value=0 if total<0 else min(total,maximum)
        if owner:
            if not(f&16):call(REACTION,[owner,u32(d),int(d>0) if d else (f>>5)&1,1])
            if not(f&128):call(NUMBER,[0xAABBCCDD,u32(old),u32(value),1])
        if d<0:
            g,v=gates()
            if (g|v)&0xFFFF0000:return
        write(0x4C,2,value)
        if d>0:sec(d,f)
        if owner and value<old:call(CLEAR,[owner])
    if entry==MP:primary(delta,flags)
    elif entry==SEC:sec(delta,flags)
    elif entry==REC:reconcile(flags)
    else:
        call(ABS,[STATS,u32(delta),flags]);primary(sx(u32(delta-sx(get(0x4C,2),16)),32),flags)
        current=sx(get(6,2),16)
        if delta>current:sec(sx(u32(delta-current),32),flags)
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for page in sorted({a&~4095 for a in [*BODIES,OWNER,GLOBAL,ELIG,REACTION,NUMBER,CLEAR,STATS,STOP]}):u.mem_map(page,4096)
    u.mem_map(0x60000000,0x3000)
    for a,b in BODIES.items():u.mem_write(a,b)
    if mutant:
        assert bytes(u.mem_read(0x300DF6,2))==bytes.fromhex('7532');u.mem_write(0x300DF6,b'\x90\x90')
    u.mem_write(STATS&~4095,bytes(initial));u.mem_write(STACK,STOP.to_bytes(8,'little'))
    observed=[];visits=[];gidx=uidx=0
    stubs={OWNER:1,GLOBAL:0,ELIG:2,REACTION:4,NUMBER:4,CLEAR:1}
    widths={MP:3,ABS:3,SEC:3,REC:2,NOOP:2,**stubs}
    def hook(uc,a,n,data):
        nonlocal gidx,uidx
        visits.append(a)
        if a not in widths:return
        regs=[UC_X86_REG_RCX,UC_X86_REG_EDX,UC_X86_REG_R8D,UC_X86_REG_R9D]
        if a==NUMBER:regs[0]=UC_X86_REG_ECX
        observed.append(['call',a,[uc.reg_read(r) for r in regs[:widths[a]]]])
        if a not in stubs:return
        ret=0
        if a==OWNER:ret=owner
        elif a==GLOBAL:ret=gm[gidx] if gidx<len(gm) else 0;gidx+=1
        elif a==ELIG:ret=um[uidx] if uidx<len(um) else 0;uidx+=1
        for r in (UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBADF00D)
        uc.reg_write(UC_X86_REG_RAX,ret)
        rsp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,int.from_bytes(uc.mem_read(rsp,8),'little'));uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,hook)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:observed.append(['write',a,n,v&((1<<(8*n))-1)]),begin=0,end=0x5FFFFFFF)
    preserved={r:0x12340000+n for n,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
    for r,v in preserved.items():u.reg_write(r,v)
    for r,v in [(UC_X86_REG_RCX,STATS),(UC_X86_REG_EDX,u32(flags if entry==REC else delta)),(UC_X86_REG_R8D,flags),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
    u.emu_start(entry,STOP,count=3000)
    assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
    assert all(u.reg_read(r)==v for r,v in preserved.items())
    final=bytes(u.mem_read(STATS&~4095,4096))
    return dict(name=name,entry=entry,delta=delta,flags=flags,global_masks=gm,unit_masks=um,owner=owner,initial_page=bytes(initial).hex(),expected_page=bytes(expected).hex(),final_page=final.hex(),expected_events=events,events=observed,visited=visits,matches=observed==events and final==expected)

cases=[run('gain'),run('gain-at-cap',live=100),run('spend',delta=-15),run('floor',delta=-80),run('zero-direction-damage',delta=0),run('zero-direction-heal',delta=0,flags=32),run('silent',flags=0x90),run('no-owner',owner=0),run('effect39-layer1',effects=(128,0)),run('effect39-layer2',effects=(0,128)),run('initial-global-refusal',gm=(1,)),run('initial-unit-refusal',um=(1,)),run('late-global-refusal',delta=-15,gm=(0,0x10000)),run('late-unit-refusal',delta=-15,um=(0,0x10000)),run('bit0-still-late-refusal',delta=-15,flags=1,gm=(0x10000,)),run('bit0-skips-low-check',flags=1,gm=(1,)),run('secondary-gain-tier',entry=SEC,delta=150),run('secondary-loss-presentation',entry=SEC,delta=-100,flags=0x400),run('secondary-suppress-reaction',entry=SEC,delta=-100,flags=0x410),run('secondary-noop-suppressed',entry=SEC,delta=150,flags=2),run('secondary-cap',entry=SEC,delta=1000),run('secondary-zero-multiplier',entry=SEC,delta=20,mult=0),run('reconcile-zero-cap',entry=REC,cap=0),run('absolute-second-topup',entry=ABS,delta=80,secondary=0),run('absolute-no-topup',entry=ABS,delta=20,secondary=100),run('signed-cap',delta=1,cap=0xFFFF),run('secondary-word-wrap',entry=SEC,delta=40000,cap=20000,mult=3)]
assert all(c['matches'] for c in cases),[(c['name'],c['events'],c['expected_events']) for c in cases if not c['matches']]
fault=run('mutant-ignores-late-global',delta=-15,flags=1,gm=(0x10000,),mutant=True)
assert not fault['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,late_gate_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} native MP/secondary/reconcile controls; late-gate mutant detected')
