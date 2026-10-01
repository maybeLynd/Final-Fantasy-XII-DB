"""Bounded offline FF12 original-code queue probe; reuse prior Unicorn tracing.

Only 0025BFB0 executes. Its initialization/unload callbacks are controlled
providers, not native effects. No live process, saves, input or instrumentation.
"""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *
W=Path('Database/Tools/work/ASTRA')
ns={}
s=(W/'spawn_manager_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x25BFB0')],str(W/'spawn_manager_primary.py'),'exec'),ns)
cat=next(b for b in json.loads((W/'spawn-manager-primary.json').read_text())['bodies'] if b['address']=='0x25bfb0')
ENTRY=0x25BFB0
body=ns['raw'][ns['off'](ENTRY-ns['ib']):ns['off'](ENTRY-ns['ib'])+cat['bytes']]
assert len(body)==179 and hashlib.sha256(body).hexdigest()==cat['sha256']
instructions={int(i['address'],16) for i in cat['instructions']}
CALLS={0x26CE60:'controlled initialization boundary',0x2628B0:'controlled unload boundary'}
MASK,ROSTER=0x2099ABC,0x209A1F0
SP,STOP=0x60001808,0x70000000
NV=(UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
def d(v):return struct.pack('<I',v&0xffffffff)
def q(v):return struct.pack('<Q',v&0xffffffffffffffff)
def run(name,mask,changes=None):
    changes=changes or []
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    injected=[(MASK,d(mask)),(ROSTER,bytes(range(1,33)))]
    pages=set(range(0x60000000,0x60003000,4096))
    for a,b in [(ENTRY,body),*injected,*[(a,b'\xCC') for a in CALLS]]:
        pages.update(range(a&~4095,(a+len(b)+4095)&~4095,4096))
    for a in pages:u.mem_map(a,4096)
    u.mem_write(ENTRY,body)
    for a in CALLS:u.mem_write(a,b'\xCC')
    for a,b in injected:u.mem_write(a,b)
    saved={r:0xA100000000000000+i for i,r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i:0x123456789ABCDEF0123456789ABCDEF^i for i in range(10)})
    for r,v in saved.items():u.reg_write(r,v)
    u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_EFLAGS,2);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
    u.mem_write(SP,q(STOP))
    regions=[(MASK,4),(ROSTER,32)]
    before={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions}
    events,trace,invalid,visited=[],[],[],[]
    def code(uc,a,n,_):
        visited.append(hex(a))
        if a not in CALLS:
            assert a in instructions,hex(a)
            return
        idx=uc.reg_read(UC_X86_REG_ECX)
        trace.append(dict(target=hex(a),index=idx,event_index=len(events),mask=bytes(uc.mem_read(MASK,4)).hex(),roster=bytes(uc.mem_read(ROSTER,32)).hex()))
        for change in changes:
            if change['target']==hex(a) and change['index']==idx:
                old=struct.unpack('<I',uc.mem_read(MASK,4))[0]
                b=d((old|change.get('set',0))&~change.get('clear',0))
                events.append([hex(a),'STUB-W',hex(MASK),4,b.hex()])
                uc.mem_write(MASK,b)
        # Volatile return is irrelevant; deliberately avoid returning the mask.
        uc.reg_write(UC_X86_REG_RAX,0xDEADC0DE)
        rsp=uc.reg_read(UC_X86_REG_RSP)
        ret=struct.unpack('<Q',uc.mem_read(rsp,8))[0]
        uc.reg_write(UC_X86_REG_RSP,rsp+8);uc.reg_write(UC_X86_REG_RIP,ret)
    def memory(uc,access,a,n,v,_):
        if 0x60000000<=a and a+n<=0x60003000:return
        events.append([hex(uc.reg_read(UC_X86_REG_RIP)),'W' if access==unicorn.UC_MEM_WRITE else 'R',hex(a),n,
            int(v&((1<<(n*8))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else bytes(uc.mem_read(a,n)).hex()])
    def bad(uc,access,a,n,v,_):invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)),access,hex(a),n]);return False
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
    error=None
    try:u.emu_start(ENTRY,STOP,count=10000)
    except (unicorn.UcError,AssertionError) as e:error=str(e)
    return dict(name=name,mask=mask,changes=changes,before=before,after={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions},
        trace=trace,memory=events,visited=visited,invalid=invalid,error=error,
        returned=error is None and u.reg_read(UC_X86_REG_RIP)==STOP,stack_ok=u.reg_read(UC_X86_REG_RSP)==SP+8,
        nonvolatile_ok=all(u.reg_read(r)==v for r,v in saved.items()),code_unchanged=bytes(u.mem_read(ENTRY,len(body)))==body)
cases=[]
def case(name,mask,changes=None):
    r=run(name,mask,changes);cases.append(r)
    if not(r['returned'] and r['stack_ok'] and r['nonvolatile_ok'] and r['code_unchanged'] and not r['invalid']):
        (W/'spawn-manager-incomplete.json').write_text(json.dumps(cases,indent=2)+'\n',newline='\n')
        raise AssertionError((name,r['error']))
    print(name,[(x['target'],x['index']) for x in r['trace']],r['after'][hex(MASK)])
case('empty-control',0)
case('bit0-control',1)
if '--feasibility' not in sys.argv:
    for mask in (2,16,31,32,0x8000001F):case('mask-'+hex(mask),mask)
    case('init4-clears-bit0',17,[dict(target='0x26ce60',index=4,clear=1)])
    case('init4-adds-bit2',17,[dict(target='0x26ce60',index=4,set=4)])
    case('unload4-adds-bit2',16,[dict(target='0x2628b0',index=4,set=4)])
    case('unload0-adds-bit4',1,[dict(target='0x2628b0',index=0,set=16)])
    case('unload2-requeues-self',4,[dict(target='0x2628b0',index=2,set=4)])
out=dict(exe_sha256=ns['sha'],entry=hex(ENTRY),body_sha256=cat['sha256'],body_bytes=len(body),
    probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),unicorn_version=unicorn.__version__,
    method='B isolated original-code execution',live_game=False,stubs={hex(a):n for a,n in CALLS.items()},
    limits=['Injected queue mask and distinctive nonzero roster, Windows x64 entry ABI.',
        'Initialization/unload callbacks are controlled providers; their native effects and live scheduling are omitted.',
        'Callback queue changes are explicit interventions, not proof native callbacks issue those requests.',
        'Non-stack reads/writes and callback boundary state retained; all complete returns and code/ABI checked.'],cases=cases)
p=W/('spawn-manager-feasibility.json' if '--feasibility' in sys.argv else 'spawn-manager-execution.json')
p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Saved',p,len(cases))
