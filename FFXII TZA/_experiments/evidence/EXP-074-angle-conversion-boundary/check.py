"""Original conversion-boundary controls: challenge blanket overflow pass-through."""
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

import math
ENTRY=0x2E5E10
BODY=extract(ENTRY,374)
WRAPPER,HELPER=0x2E5F90,0x33CB70
WRAPBODY,HELPBODY=extract(WRAPPER,26),extract(HELPER,128)
CONSTANTS={a:extract(a,4) for a in (0x1CEBC50,0x915620,0x1CEBC78)}
CALLS=(0x3DA850,0x3DAF20,0x3EC260)
ACTOR,STATE,CONTROL,NODE=0x40000000,0x40001000,0x40002000,0x40003000
STACK,STOP=0x60001808,0x70000000
RET=0xAABBCCDD

def floating(v):return struct.unpack('<f',struct.pack('<I',v))[0]
def bits(v):return struct.unpack('<I',struct.pack('<f',v))[0]
def f32(v):
    try:return floating(bits(v))
    except OverflowError:return math.copysign(math.inf,v)
PI=floating(int.from_bytes(CONSTANTS[0x1CEBC50],'little'))
NEGPI=floating(int.from_bytes(CONSTANTS[0x915620],'little'))
TAU=floating(int.from_bytes(CONSTANTS[0x1CEBC78],'little'))
assert (bits(PI),bits(NEGPI),bits(TAU))==(0x40490FDB,0xC0490FDB,0x40C90FDB)

def normalize(angle):
    bias=PI if angle>=0 else NEGPI
    shifted=f32(angle+bias)
    quotient=f32(shifted/TAU)
    integer=int(quotient) if math.isfinite(quotient) and -2147483648<=quotient<2147483648 else -2147483648
    result=f32(f32(shifted-f32(f32(integer)*TAU))-bias)
    return bits(result),dict(bias=bits(bias),shifted=bits(shifted),quotient=bits(quotient),integer=integer,result=bits(result))

def run(name,angle_bits=0x3F800000,aux_bits=0xC0200000,flag=0,handle=0x1234,controller=True,node=True,fourth=0,mutant=False,count=2):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for p in sorted({a&~4095 for a in [ENTRY,*CONSTANTS,*CALLS,ACTOR,STATE,CONTROL,NODE,STOP]}):u.mem_map(p,4096)
    u.mem_map(0x60000000,0x3000)
    u.mem_write(ENTRY,BODY);u.mem_write(WRAPPER,WRAPBODY)
    for a,b in CONSTANTS.items():u.mem_write(a,b)
    for a in CALLS:u.mem_write(a,b'\xc3')
    if mutant:
        assert bytes(u.mem_read(0x2E5F9D,8))==bytes.fromhex('f30f1088a8000000')
        u.mem_write(0x2E5FA1,b'\xac') # wrong source field, private wrapper only
    for a in (ACTOR,STATE,CONTROL,NODE):u.mem_write(a,b'\xa5'*4096)
    def put(a,v,n=4):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
    put(ACTOR+0xB8,STATE,8);put(ACTOR+0xC0,CONTROL if controller else 0,8)
    put(ACTOR+0xD,flag,1);put(CONTROL,handle);put(CONTROL+0x138,NODE if node else 0,8)
    u.mem_write(STATE+0x104,bytes([0x12,0x80,0xFF]))
    put(STATE+0xA8,angle_bits)
    pages={a:bytearray(u.mem_read(a,4096)) for a in (ACTOR,STATE,CONTROL,NODE,*sorted({a&~4095 for a in CONSTANTS}))}
    arithmetic=[];expected=[];expected_angles=[];next_angle=angle_bits
    def ew(ip,a,v):
        data=v.to_bytes(4,'little');pages[a&~4095][a&4095:(a&4095)+4]=data
        expected.append(['write',ip,a,data.hex()])
    for iteration in range(count):
        normalized,details=normalize(floating(next_angle));arithmetic.append(details)
        if controller:
            ew(0x2E5E88,STATE+0xAC,aux_bits);ew(0x2E5EBE,STATE+0xA8,normalized)
            targets=[STATE+0x50]+([] if flag&0x20 else [STATE+0x70,STATE+0x60])+([NODE+0xF0] if node else [])
            for target in targets:expected.append(['stub',CALLS[0],[target,normalized],[normalized,aux_bits]])
            if node:expected.append(['stub',CALLS[1],[NODE,0x12,0x80,0xFF],[normalized,aux_bits]])
            if handle!=0xFFFFFFFF:expected.append(['stub',CALLS[2],[handle&0xFFFF,aux_bits,normalized,0,int(fourth!=0)],[normalized,aux_bits]])
        if controller:next_angle=normalized
        expected_angles.append(next_angle)
    events=[];visited=[];reads=[]
    def get(a,n=4):return int.from_bytes(u.mem_read(a,n),'little')
    def low(r):return u.reg_read(r)&0xFFFFFFFF
    def code(uc,a,n,d):
        visited.append(a)
        if a not in CALLS:return
        if a==CALLS[0]:args=[uc.reg_read(UC_X86_REG_RCX),low(UC_X86_REG_XMM1)]
        elif a==CALLS[1]:args=[uc.reg_read(UC_X86_REG_RCX),uc.reg_read(UC_X86_REG_EDX),uc.reg_read(UC_X86_REG_R8D),uc.reg_read(UC_X86_REG_R9D)]
        else:args=[uc.reg_read(UC_X86_REG_ECX),low(UC_X86_REG_XMM1),low(UC_X86_REG_XMM2),low(UC_X86_REG_XMM3),get(uc.reg_read(UC_X86_REG_RSP)+0x28)]
        events.append(['stub',a,args,[get(STATE+0xA8),get(STATE+0xAC)]])
        for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0BAD0BAD0)
        for r in (UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5):uc.reg_write(r,0xBAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD0)
        uc.reg_write(UC_X86_REG_EAX,RET)
    def write(uc,t,a,n,v,d):events.append(['write',uc.reg_read(UC_X86_REG_RIP),a,(v&((1<<(8*n))-1)).to_bytes(n,'little').hex()])
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write,begin=0,end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    saved={r:0x1234000000000000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
    saved.update({r:0x98765432101234567890ABCDEF000000+i for i,r in enumerate((UC_X86_REG_XMM6,UC_X86_REG_XMM7,UC_X86_REG_XMM8,UC_X86_REG_XMM9,UC_X86_REG_XMM10,UC_X86_REG_XMM11,UC_X86_REG_XMM12,UC_X86_REG_XMM13,UC_X86_REG_XMM14,UC_X86_REG_XMM15))})
    phases=[]
    for iteration in range(count):
        for r,v in saved.items():u.reg_write(r,v)
        put(STACK,STOP,8);u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RCX,ACTOR)
        u.reg_write(UC_X86_REG_XMM1,aux_bits);u.reg_write(UC_X86_REG_XMM2,0xDEADBEEF)
        u.reg_write(UC_X86_REG_R8D,fourth);u.reg_write(UC_X86_REG_R9D,0xBAD0BAD0)
        u.reg_write(UC_X86_REG_EAX,0x11223344);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
        start=len(events)
        u.emu_start(WRAPPER,STOP,count=1000)
        phases.append(dict(iteration=iteration,angle=get(STATE+0xA8),aux=get(STATE+0xAC),event_start=start,event_end=len(events),return_boundary=u.reg_read(UC_X86_REG_RIP)==STOP,stack=u.reg_read(UC_X86_REG_RSP)==STACK+8,nonvolatile=all(u.reg_read(r)==v for r,v in saved.items())))
    actual_eax=u.reg_read(UC_X86_REG_EAX)
    checks=dict(return_boundary=u.reg_read(UC_X86_REG_RIP)==STOP,stack=u.reg_read(UC_X86_REG_RSP)==STACK+8,nonvolatile=all(u.reg_read(r)==v for r,v in saved.items()),events=events==expected,fixture_pages=all(bytes(u.mem_read(a,4096))==v for a,v in pages.items()),eax=actual_eax==((CONTROL if not node and handle==0xFFFFFFFF else RET) if controller else STATE))
    checks["phases"]=all(p["return_boundary"] and p["stack"] and p["nonvolatile"] and p["angle"]==expected_angles[i] for i,p in enumerate(phases))
    out=get(STATE+0xA8)
    return dict(name=name,inputs=dict(angle_bits=angle_bits,aux_bits=aux_bits,flag=flag,handle=handle,controller=controller,node=node,fourth=fourth),count=count,phases=phases,expected_angles=expected_angles,arithmetic=arithmetic,events=events,expected_events=expected,visited=visited,reads=reads,stored_angle_bits=out,stored_aux_bits=get(STATE+0xAC),in_pi_range=abs(floating(out))<=PI,eax=actual_eax,mxcsr=u.reg_read(UC_X86_REG_MXCSR),checks=checks,matches=all(checks.values()))

HELP_CONSTANTS={**CONSTANTS,**{a:extract(a,4) for a in (0xD10B0C,0xD10B20,0x915624)}}
FOURPI=floating(int.from_bytes(HELP_CONSTANTS[0xD10B0C],'little'))
assert bits(FOURPI)==0x41490FDB
assert int.from_bytes(HELP_CONSTANTS[0xD10B20],'little')==0xC1490FDB
assert int.from_bytes(HELP_CONSTANTS[0x915624],'little')==0xC0C90FDB

def helper(angle_bits,mutant=False):
    value=floating(angle_bits);expected=value;path='near';steps=0
    if value>FOURPI or value<-FOURPI:
        path='far';q=f32(value/TAU)
        integer=int(q) if math.isfinite(q) and -2147483648<=q<2147483648 else -2147483648
        expected=f32(value-f32(f32(integer)*TAU))
    else:
        while expected>PI:expected=f32(expected-TAU);steps+=1
        while expected<-PI:expected=f32(expected+TAU);steps+=1
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for a in sorted({x&~4095 for x in [HELPER,*HELP_CONSTANTS,STOP]}):u.mem_map(a,4096)
    u.mem_map(0x60000000,0x3000);u.mem_write(HELPER,HELPBODY)
    for a,b in HELP_CONSTANTS.items():u.mem_write(a,b)
    if mutant:
        assert bytes(u.mem_read(0x33CBE8,4))==bytes.fromhex('f30f5cd0')
        u.mem_write(0x33CBE8,b'\x90'*4) # bypass subtraction: erroneous pass-through
    pages={a:bytes(u.mem_read(a,4096)) for a in {a&~4095 for a in HELP_CONSTANTS}}
    writes=[];reads=[];visited=[]
    u.hook_add(unicorn.UC_HOOK_CODE,lambda uc,a,n,d:visited.append(a))
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]))
    u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
    saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15,UC_X86_REG_XMM6,UC_X86_REG_XMM7,UC_X86_REG_XMM8,UC_X86_REG_XMM9,UC_X86_REG_XMM10,UC_X86_REG_XMM11,UC_X86_REG_XMM12,UC_X86_REG_XMM13,UC_X86_REG_XMM14,UC_X86_REG_XMM15))}
    for r,v in saved.items():u.reg_write(r,v)
    u.mem_write(STACK,STOP.to_bytes(8,'little'));u.reg_write(UC_X86_REG_RSP,STACK)
    u.reg_write(UC_X86_REG_XMM0,angle_bits);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
    u.emu_start(HELPER,STOP,count=500)
    answer=u.reg_read(UC_X86_REG_XMM0)&0xFFFFFFFF
    checks=dict(answer=answer==bits(expected),return_boundary=u.reg_read(UC_X86_REG_RIP)==STOP,stack=u.reg_read(UC_X86_REG_RSP)==STACK+8,nonvolatile=all(u.reg_read(r)==v for r,v in saved.items()),no_writes=not writes,constant_pages=all(bytes(u.mem_read(a,4096))==v for a,v in pages.items()),path=(0x33CBCD in visited)==(path=='far'))
    return dict(input=angle_bits,answer=answer,expected_answer=bits(expected),expected_path=path,expected_loop_steps=steps,visited=visited,reads=reads,writes=writes,checks=checks,matches=all(checks.values()))

inputs=[0x50490FDA,0x50490FDB,0x50490FDC,0xD0490FDA,0xD0490FDB,0xD0490FDC,bits(1.4e10),bits(-1.4e10),bits(1e11),bits(-1e11)]
cases=[]
for v in inputs:
    w=run(f'angle-{v:08X}',angle_bits=v,count=1)
    h=helper(v)
    cases.append(dict(name=w['name'],wrapper=w,helper=h,wrapper_unchanged=w['phases'][0]['angle']==v,helper_unchanged=h['answer']==v,matches=w['matches'] and h['matches']))
mutant=helper(0x50490FDB,mutant=True)
result=dict(status='PASS' if all(c['matches'] for c in cases) and not mutant['matches'] else 'FAIL',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),unicorn=unicorn.__version__,capstone=capstone.__version__,cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in {ENTRY:BODY,WRAPPER:WRAPBODY,HELPER:HELPBODY,**HELP_CONSTANTS}.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in {WRAPPER:WRAPBODY,ENTRY:BODY,HELPER:HELPBODY}.items() for i in cs.disasm(b,a))+'\n')
print(result['status'],len(cases),'paired controls',[(c['name'],c['wrapper']['checks'],c['helper']['checks']) for c in cases if not c['matches']],'mutant',mutant['checks'])
for c in cases:print(c['name'],f"{c['wrapper']['phases'][0]['angle']:08X}",f"{c['helper']['answer']:08X}",c['wrapper']['arithmetic'][0]['integer'],c['wrapper_unchanged'],c['helper_unchanged'])
assert result['status']=='PASS'
