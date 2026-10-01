"""Offline original FF12 instruction tests; reuses cap_policy_probe mapping/tracing.

Controlled service providers are explicit stubs. This does not establish a live
party, resource binding, native actor position providers or ordinary scheduling.
"""
import hashlib, json, struct, sys
from pathlib import Path
sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *
WORK = Path('Database/Tools/work/ASTRA')
catalog = {int(b['address'],16): b for n in ('primary','callees')
           for b in json.loads((WORK/('spawn-lifecycle-'+n+'.json')).read_text())['bodies']}
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
SHA = hashlib.sha256(raw).hexdigest()
assert SHA == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I',raw,60)[0]
ib = struct.unpack_from('<Q',raw,pe+48)[0]
st = pe+24+struct.unpack_from('<H',raw,pe+20)[0]
assert ib == 0x120000
def extract(a,n):
    for j in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,size,disk = struct.unpack_from('<IIII',raw,st+j*40+8)
        d = a-ib-rva
        if 0 <= d and d+n <= size: return raw[disk+d:disk+d+n]
    raise ValueError(hex(a))
ENTRIES = (0x234DA0,0x235720,0x31E620,0x3A1960,0x3273B0,0x239020)
bodies = {a:extract(a,catalog[a]['bytes']) for a in ENTRIES}
assert all(hashlib.sha256(b).hexdigest()==catalog[a]['sha256'] for a,b in bodies.items())
instructions = {int(i['address'],16) for a in ENTRIES for i in catalog[a]['instructions']}
STUBS = {0x31B810:'controlled mapped-slot provider',0x313F60:'controlled field permission',
 0x3590D0:'controlled focus handle',0x265020:'controlled position provider',
 0x808C40:'stack-cookie check boundary (no check performed)',0x308D90:'controlled active count',
 0x31B760:'controlled actor-to-unit lookup',0x32A150:'controlled raw clock',
 0x234AF0:'controlled candidate service (return/output chosen separately)'}
SP,STOP = 0x60001808,0x70000000
UNIT,ACTOR,STATS = 0x50010000,0x50020000,0x50030000
DATA,BANK,LANES = 0x50040000,0x50050000,0x50060000
NV=(UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,
    UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
ARGS=(UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9)
def d(v): return struct.pack('<I',v&0xffffffff)
def q(v): return struct.pack('<Q',v&0xffffffffffffffff)
def f(v): return struct.pack('<f',v)
def run(name,entry,config):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    writes=[(UNIT,bytes(0x4000)),(ACTOR,bytes(0x4000)),(STATS,bytes(0x4000)),
            (DATA,bytes(0x100)),(BANK,bytes([0xA5])*0x500),(LANES,bytes(0x100)),
            (0x1F44830,q(0xB12C)),(0x2F973B8,d(config.get('limit',0x7F800000))),
            (0x208D458,bytes([config.get('cap',28)])),(0x208D457,bytes([config.get('attempts',1)])),
            (0x1DFE0B8,f(1)),(0x8F8D80,extract(0x8F8D80,4)),
            (0x2089360,f(39)),(0x2089364,f(42)),(0x208E690,q(BANK))]
    writes += [(UNIT,q(config.get('flags',0))), (UNIT+0x38,q(LANES)),(UNIT+0x40,q(DATA+0x60)),
               (DATA+0x60,bytes([2,0,1])), (LANES,struct.pack('<4H',2,0,4,5)),
               (LANES+8,struct.pack('<H',7)),(BANK+0x250,bytes(0x250)),
               (DATA,f(0)+d(config.get('candidate_y',0))+f(0)),
               (DATA+0x20,d(config.get('minimum',0))),
               (DATA+0x24,d(config.get('maximum',0x42C80000))),
               (DATA+0x28,d(0xC47A0000)),
               (SP-0xE8+0x34,d(config.get('stale_observed',0xC47A0000))),
               (SP-0xE8+0x60,struct.pack('<4I',0x41200000,0x41A00000,0x41F00000,0x42200000)),
               (SP+0x28,d(config.get('all_slots',1)))]
    slots=config.get('slots',[])
    for i,s in enumerate(slots):
        writes += [(UNIT+i*0x1000+8,d(s.get('handle',i+1))),
                   (UNIT+i*0x1000+0x10,q(ACTOR+i*0x1000)),
                   (UNIT+i*0x1000+0x698,q(0 if s.get('no_stats') else STATS+i*0x1000)),
                   (STATS+i*0x1000+0x64,d(s.get('status',0)))]
    regions=[(DATA,0x100),(BANK,0x500),(UNIT,0x4000),(0x208D457,2)]
    pages=set(range(0x60000000,0x60003000,4096))
    for a,b in list(bodies.items())+writes+[(a,b'\xCC') for a in STUBS]:
        pages.update(range(a&~4095,(a+len(b)+4095)&~4095,4096))
    for a in pages: u.mem_map(a,4096)
    for a,b in bodies.items(): u.mem_write(a,b)
    for a in STUBS: u.mem_write(a,b'\xCC')  # Trap sentinel; hook returns before executing it.
    for a,b in writes: u.mem_write(a,b)
    saved={r:0xA100000000000000+i for i,r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i:0x123456789ABCDEF0123456789ABCDEF^i for i in range(10)})
    for r,v in saved.items(): u.reg_write(r,v)
    args=(DATA,0 if config.get('null_min') else DATA+0x20,
          0 if config.get('null_max') else DATA+0x24,0 if config.get('null_out') else DATA+0x28)
    if entry==0x235720: args=(ACTOR,0,0,0)
    if entry==0x239020: args=(config['setter'],0,0,0)
    for r,v in zip(ARGS,args): u.reg_write(r,v&0xffffffffffffffff)
    u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_EFLAGS,2);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
    u.mem_write(SP,q(STOP))
    before={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions}
    events,calls,visited,invalid=[],[],{},[]
    def hostwrite(a,b):
        events.append([hex(u.reg_read(UC_X86_REG_RIP)),'STUB-W',hex(a),len(b),b.hex()])
        u.mem_write(a,b)
    def code(uc,a,n,_):
        visited[hex(a)]=visited.get(hex(a),0)+1
        if a in bodies or a in STUBS:
            calls.append(dict(event_index=len(events),target=hex(a),stub=a in STUBS,
                 args=[hex(uc.reg_read(r)) for r in ARGS],xmm2=hex(uc.reg_read(UC_X86_REG_XMM2)&0xffffffff),
                 xmm3=hex(uc.reg_read(UC_X86_REG_XMM3)&0xffffffff)))
        if a not in STUBS:
            assert a in instructions,hex(a)
            return
        rcx,rdx,r8,r9=[uc.reg_read(r) for r in ARGS]
        v=0
        if a==0x31B810: v=UNIT+rcx*0x1000 if rcx<len(slots) and not slots[rcx].get('absent') else 0
        elif a==0x313F60: v=config.get('field_permission',0)
        elif a==0x3590D0: v=config.get('focus',1)
        elif a==0x265020:
            s=slots[(rcx-ACTOR)//0x1000]
            for ptr,bits in zip((rdx,r8,r9),s.get('position',[0x40A00000,0,0])): hostwrite(ptr,d(bits))
        elif a==0x308D90: v=config.get('active_count',0)
        elif a==0x31B760: v=UNIT
        elif a==0x32A150: v=300
        elif a==0x234AF0:
            v=config.get('candidate_return',1)
            if config.get('candidate_writes',True):
                hostwrite(rdx,struct.pack('<3f',1,2,3))
                # Fifth caller argument lies at the callee's rsp+28.
                outptr=struct.unpack('<Q',uc.mem_read(uc.reg_read(UC_X86_REG_RSP)+0x28,8))[0]
                hostwrite(outptr,d(config.get('observed',0x41C80000)))
        elif a==0x808C40: v=uc.reg_read(UC_X86_REG_RAX)
        else: raise AssertionError(hex(a))
        uc.reg_write(UC_X86_REG_RAX,v&0xffffffffffffffff)
        rsp=uc.reg_read(UC_X86_REG_RSP)
        ret=struct.unpack('<Q',uc.mem_read(rsp,8))[0]
        uc.reg_write(UC_X86_REG_RSP,rsp+8);uc.reg_write(UC_X86_REG_RIP,ret)
    def memory(uc,access,a,n,v,_):
        if 0x60000000<=a and a+n<=0x60003000: return
        events.append([hex(uc.reg_read(UC_X86_REG_RIP)),'W' if access==unicorn.UC_MEM_WRITE else 'R',hex(a),n,
            int(v&((1<<(n*8))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else bytes(uc.mem_read(a,n)).hex()])
    def bad(uc,access,a,n,v,_): invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)),access,hex(a),n]);return False
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
    error=None
    try:u.emu_start(entry,STOP,count=100000)
    except (unicorn.UcError,AssertionError) as e:error=str(e)
    return dict(name=name,entry=hex(entry),config=config,injected_writes=[[hex(a),b.hex()] for a,b in writes],
        before=before,after={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions},calls=calls,visited=visited,
        memory=events,invalid=invalid,error=error,rax=hex(u.reg_read(UC_X86_REG_RAX)),
        returned=error is None and u.reg_read(UC_X86_REG_RIP)==STOP,stack_ok=u.reg_read(UC_X86_REG_RSP)==SP+8,
        nonvolatile_ok=all(u.reg_read(r)==v for r,v in saved.items()),
        code_unchanged=all(bytes(u.mem_read(a,len(b)))==b for a,b in bodies.items()))
cases=[]
def case(n,e,**kw):
    r=run(n,e,kw);cases.append(r)
    if not (r['returned'] and r['stack_ok'] and r['nonvolatile_ok'] and r['code_unchanged'] and not r['invalid']):
        (WORK/'spawn-lifecycle-incomplete.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8',newline='\n')
    assert r['returned'] and r['stack_ok'] and r['nonvolatile_ok'] and r['code_unchanged'] and not r['invalid'],(n,r['error'])
    print(n,r['rax'],sum(x['target']=='0x234af0' for x in r['calls']))
case('validator-empty-control',0x234DA0)
case('validator-one-control',0x234DA0,slots=[{}])
if '--feasibility' not in sys.argv:
    case('validator-early-publish-later-reject',0x234DA0,slots=[{},dict(position=[0x41200000,0,0x41200000])])
    case('validator-reject-before-focus',0x234DA0,slots=[dict(handle=2,position=[0x41200000,0,0x41200000]),dict(handle=1)])
    case('validator-two-pass',0x234DA0,slots=[{},dict(handle=2)])
    case('validator-focus-only-skips-far',0x234DA0,all_slots=0,slots=[{},dict(handle=2,position=[0x41200000,0,0x41200000])])
    case('validator-no-focus',0x234DA0,all_slots=0,focus=77,slots=[{}])
    case('validator-status-skip',0x234DA0,slots=[dict(status=1)])
    case('validator-status-waiver',0x234DA0,slots=[dict(status=1)],field_permission=1)
    case('validator-no-stats',0x234DA0,slots=[dict(no_stats=True)])
    case('validator-bound-equality',0x234DA0,slots=[{}],minimum=0x41C80000,maximum=0x41C80000)
    case('validator-min-reject',0x234DA0,slots=[{}],minimum=0x41D00000)
    case('validator-nan-distance',0x234DA0,slots=[dict(position=[0x7FC12345,0,0])],minimum=0x41C80000)
    case('validator-infinite-distance',0x234DA0,slots=[dict(position=[0x7F800000,0,0])])
    case('validator-vertical-ignored',0x234DA0,slots=[dict(position=[0x40A00000,0x7FC12345,0])])
    case('validator-null-bounds',0x234DA0,slots=[dict(position=[0x41200000,0,0x41200000])],null_min=True,null_max=True,null_out=True)
    for n in (-1,0,1,127,128,255,256,257):case('setter-'+str(n),0x239020,setter=n)
    for n in (0,1,127,128,255):case('automatic-attempt-'+str(n),0x235720,attempts=n,candidate_return=0,candidate_writes=False)
    case('automatic-success-control',0x235720)
    case('automatic-nan-observed',0x235720,observed=0x7FC12345)
    case('automatic-infinite-observed',0x235720,observed=0x7F800000)
    case('automatic-no-output-finite-stack',0x235720,candidate_writes=False)
    case('automatic-no-output-infinite-stack',0x235720,candidate_writes=False,stale_observed=0x7F800000)
    for bit in (45,49,44,48):case('automatic-min-flag-'+str(bit),0x235720,flags=1<<bit)
    case('automatic-cap-boundary',0x235720,active_count=28)
    case('automatic-cap-signed128',0x235720,cap=128)
out=dict(exe_sha256=SHA,unicorn_version=unicorn.__version__,method='B isolated original-code execution',live_game=False,
    instruction_bodies={hex(a):catalog[a]['sha256'] for a in ENTRIES},stubs={hex(a):n for a,n in STUBS.items()},
    limits=['Injected Windows x64 ABI, mapped slots, focus, actor positions, field permission, clock and candidate service.',
            'Cookie stub preserves return register; no cookie validation. No live initialization or native stub effects.',
            'Automatic selector candidate is a stub; local signed-limit/output-consumption effects only. AREA no-output claim is separate method A.',
            'All MXCSR exceptions masked, FTZ/DAZ clear. No claim that nonfinite positions occur in ordinary play.'],cases=cases)
output=WORK/('spawn-lifecycle-feasibility.json' if '--feasibility' in sys.argv else 'spawn-lifecycle-execution.json')
output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Saved',output,len(cases))
