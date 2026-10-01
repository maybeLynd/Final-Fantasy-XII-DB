"""Bounded original initializer address-width probe. No game process access."""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *

raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
EXE_SHA=hashlib.sha256(raw).hexdigest()
assert EXE_SHA=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0]
base=struct.unpack_from('<Q',raw,pe+48)[0]
assert base==0x120000
st=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
def extract(va,n):
    for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,sz,disk=struct.unpack_from('<IIII',raw,st+i*40+8)
        d=va-base-rva
        if 0<=d and d+n<=sz:return raw[disk+d:disk+d+n]
    raise ValueError(hex(va))
BODIES={0x369D30:extract(0x369D30,707),0x36A490:extract(0x36A490,215),0x20E620:extract(0x20E620,9)}
assert BODIES[0x369D30][0x14:0x17]==bytes.fromhex('4c8bf2')
G0,GN,SP,STOP,FMT=0x22D7000,0x2000,0x60001808,0x70000000,0x17D2E0
ARENA=0x22D7FD0
NV=(UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
VOL=(UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11)
def run(name,p,ident=2,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages={a&~4095 for a in (*BODIES,FMT,0x1F83530)}
    for a in pages:u.mem_map(a,4096)
    u.mem_map(G0,GN)
    u.mem_map(p,0x100000)
    u.mem_map(0x60000000,0x3000)
    for a,b in BODIES.items():u.mem_write(a,b)
    if mutant:u.mem_write(0x369D44,bytes.fromhex('448bf2')) # MOV R14D,EDX truncates backing
    u.mem_write(FMT,b'\xc3') # explicit no-write formatter stub; native formatting unproved
    u.mem_write(p,b'\xa5'*0x100000)
    u.mem_write(SP,struct.pack('<Q',STOP))
    u.mem_write(0x1F83530,b'\0'*8)
    initial={G0:bytes(u.mem_read(G0,GN)),p:bytes(u.mem_read(p,0x100000)),0x1F83530:bytes(u.mem_read(0x1F83530,8))}
    saved={r:0xA100000000000000+i for i,r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i:0x13579BDF2468ACE00123456789ABCDEF ^ i for i in range(10)})
    for r,v in saved.items():u.reg_write(r,v)
    u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_RCX,ident&0xFFFFFFFF)
    u.reg_write(UC_X86_REG_RDX,p);u.reg_write(UC_X86_REG_R8,0x100000);u.reg_write(UC_X86_REG_R9,16)
    u.reg_write(UC_X86_REG_EFLAGS,2);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
    assert all(bytes(u.mem_read(a,len(b)))==b for a,b in initial.items())
    assert all(u.reg_read(r)==v for r,v in saved.items())
    calls=[];visited=[];writes=[]
    def code(uc,a,n,_):
        visited.append(a)
        if a==FMT:
            calls.append(dict(target=hex(a),args=[uc.reg_read(r) for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9)]))
            for i,r in enumerate(VOL):uc.reg_write(r,0xCCCC000000000000+i)
            for i in range(6):uc.reg_write(UC_X86_REG_XMM0+i,(1<<128)-1-i)
            uc.reg_write(UC_X86_REG_RAX,0)
        elif a==0x20E620:calls.append(dict(target=hex(a),args=[uc.reg_read(UC_X86_REG_RCX)]))
        elif not any(lo<=a<lo+len(b) for lo,b in BODIES.items()):
            raise AssertionError('unexpected target '+hex(a))
    def write(uc,access,a,n,v,_):
        if 0x60000000<=a<0x60003000:return
        writes.append([hex(uc.reg_read(UC_X86_REG_RIP)),hex(a),n,hex(v&((1<<(8*n))-1))])
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
    error=None
    try:u.emu_start(0x369D30,STOP,count=6000)
    except unicorn.UcError as e:error=str(e)
    valid=0<=ident<=14
    r=ARENA+ident*0xA8 if valid else ARENA
    q=lambda a:struct.unpack('<Q',u.mem_read(a,8))[0]
    d=lambda a:struct.unpack('<I',u.mem_read(a,4))[0]
    first=(p+0x280) # aligned1MiB fixture,32 page entries,1 map group,16 bookkeeping slots
    observed={hex(o):q(r+o) for o in (8,0x20,0x28,0x30,0x38,0x40,0x90,0x98)} if valid else {}
    expected={8:p,0x20:p+0x40,0x28:p+0x80,0x30:p+0x180,0x38:p+0x280,0x40:p+0x180,0x90:first,0x98:first}
    checks=dict(returned=error is None and u.reg_read(UC_X86_REG_RIP)==STOP,
                stack=u.reg_read(UC_X86_REG_RSP)==SP+8,
                nonvolatile=all(u.reg_read(k)==v for k,v in saved.items()),
                resolver_base_unchanged=bytes(u.mem_read(0x1F83530,8))==initial[0x1F83530],
                expected_calls=(len(calls)==10 and calls[0]['args'][0]==p and calls[0]['args'][2:]==[ident,p] and all(c['target']=='0x20e620' and c['args']==[0] for c in calls[1:])) if valid else calls==[],
                pointer_layout=all(q(r+o)==v for o,v in expected.items()) if valid else True,
                initial_free_block=(d(r+0x5C)==0xFFD80 and bytes(u.mem_read(first,2))==b'\x12\xff' and d(first+0x18)==0xFFD40) if valid else True,
                bounded_writes=all(G0<=int(a,16) and int(a,16)+n<=G0+GN or p<=int(a,16) and int(a,16)+n<=p+0x2C0 for _,a,n,_ in writes),
                rejected_ids_unchanged=True if valid else all(bytes(u.mem_read(a,len(b)))==b for a,b in initial.items()))
    return dict(name=name,inputs=dict(backing=hex(p),id=ident,size=0x100000,bookkeeping_slots=16,base=0,mutant=mutant),
                evidence_scope='native initializer+block-header writer+encoder; no-write sprintf stub; no CRT/native malloc or live process',
                initialized_sha256={hex(a):hashlib.sha256(b).hexdigest() for a,b in initial.items()},
                error=error,rip=hex(u.reg_read(UC_X86_REG_RIP)),observed_pointer_fields=observed,calls=calls,visited=[hex(a) for a in visited],writes=writes,checks=checks,matches=all(checks.values()),
                final_arena_record=bytes(u.mem_read(r,0xA8)).hex(),final_prefix_and_first_block=bytes(u.mem_read(p,0x2C0)).hex())
cases=[run('low-address',0x40010000),run('above-2GiB',0x80010000),run('above-4GiB',0x100010000),run('last-valid-id',0x40010000,14),run('first-invalid-id',0x40010000,15),run('negative-id',0x40010000,-1)]
mutant=run('truncate-backing-register',0x100010000,mutant=True)
out=dict(exe_sha256=EXE_SHA,body_sha256={hex(a):hashlib.sha256(b).hexdigest() for a,b in BODIES.items()},unicorn_version=unicorn.__version__,cases=cases,mutant=mutant,all_original_pass=all(c['matches'] for c in cases),mutant_detected=not mutant['matches'] and mutant['error'] is not None and mutant['rip']=='0x369e4c')
Path('Database/Tools/work/ASTRA/arena-init-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('cases','mutant')},indent=2))
for c in [*cases,mutant]:print(c['name'],c['matches'],c['checks'],c['error'],c['rip'])
assert out['all_original_pass'] and out['mutant_detected']
