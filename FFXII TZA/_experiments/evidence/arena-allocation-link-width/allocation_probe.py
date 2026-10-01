"""EXP078: original allocator/list composition on sealed EXP077 output fixtures. Offline."""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *
ROOT=Path('Database/FFXII TZA/_experiments/evidence')
raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
SHA=hashlib.sha256(raw).hexdigest()
assert SHA=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
fixtures=(ROOT/'resource-arena-backing/initializer-result.json').read_bytes()
assert hashlib.sha256(fixtures).hexdigest()=='d7214b5fe028612a111796be5ecfff7c5aedce3832fa26b9bcfb313e0f90c283'
F=json.loads(fixtures)
receipts=[ROOT/'resource-arena-backing/primary.json',ROOT/'authored-reference-lifetime-review/primary.json',Path('Database/Tools/work/ASTRA/arena-allocation-primary.json')]
allb={int(b['address'],16):b for p in receipts for b in json.loads(p.read_text())['bodies']}
addresses=(0x36BC60,0x36C900,0x36C9D0,0x36B5F0,0x36B7F0,0x36B8B0,0x36B670,0x36B730,0x36B210,0x36B2C0,0x36A490,0x20E600,0x20E620,0x36C1F0,0x36C140)
pe=struct.unpack_from('<I',raw,60)[0];ib=struct.unpack_from('<Q',raw,pe+48)[0]
assert ib==0x120000
st=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
def extract(va,n):
    for j in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,sz,disk=struct.unpack_from('<IIII',raw,st+j*40+8)
        d=va-ib-rva
        if 0<=d and d+n<=sz:return raw[disk+d:disk+d+n]
    raise ValueError(hex(va))
B={a:extract(a,allb[a]['bytes']) for a in addresses}
for a,b in B.items():assert hashlib.sha256(b).hexdigest()==allb[a]['sha256']
G,GN,BASE,SP,STOP=0x22D7000,0x2000,0x1F83530,0x60001808,0x70000000
ARENA=0x22D7FD0+2*0xA8
NV=(UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
ARGS=(UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9)
def run(name,fixture,direction=0,size=0x40,steps=2,alias=False):
    f=next(c for c in F['cases'] if c['name']==fixture)
    assert f['matches'] and f['inputs']['id']==2
    p=int(f['inputs']['backing'],16)
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for pg in sorted({x&~4095 for a,b in B.items() for x in range(a,a+len(b)+4095,4096)}|{BASE&~4095}):u.mem_map(pg,4096)
    u.mem_map(G,GN);u.mem_map(p,0x100000);u.mem_map(0x60000000,0x3000)
    for a,b in B.items():u.mem_write(a,b)
    u.mem_write(p,b'\xa5'*0x100000)
    # Reconstitute exact native output from the already sealed run, without executing its initializer again.
    for rip,a,n,v in f['writes']:
        a=int(a,16);assert G<=a and a+n<=G+GN or p<=a and a+n<=p+0x100000
        u.mem_write(a,int(v,16).to_bytes(n,'little'))
    assert bytes(u.mem_read(ARENA,0xA8)).hex()==f['final_arena_record']
    assert bytes(u.mem_read(p,0x2C0)).hex()==f['final_prefix_and_first_block']
    assert bytes(u.mem_read(BASE,8))==b'\0'*8
    fixture_hashes={hex(a):hashlib.sha256(bytes(u.mem_read(a,n))).hexdigest() for a,n in ((G,GN),(p,0x100000),(BASE,8))}
    saved={r:0xA100000000000000+i for i,r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i:0x13579BDF2468ACE00123456789ABCDEF ^ i for i in range(10)})
    active=None
    def code(uc,a,n,_):
        active['visited'].append(hex(a))
        if a in B:active['calls'].append(dict(target=hex(a),args=[hex(uc.reg_read(r)) for r in ARGS]))
        if not any(lo<=a<lo+len(b) for lo,b in B.items()):raise AssertionError('unexpected original target '+hex(a))
    def mem(uc,access,a,n,v,_):
        if 0x60000000<=a and a+n<=0x60003000:return
        active['memory'].append([hex(uc.reg_read(UC_X86_REG_RIP)),'W' if access==unicorn.UC_MEM_WRITE else 'R',hex(a),n,hex(v&((1<<(8*n))-1)) if access==unicorn.UC_MEM_WRITE else bytes(uc.mem_read(a,n)).hex()])
    def invalid(uc,access,a,n,v,_):
        active['invalid'].append(dict(rip=hex(uc.reg_read(UC_X86_REG_RIP)),access=access,address=hex(a),bytes=n,value=hex(v&((1<<(8*n))-1))))
        return False
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,mem)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
    results=[]
    def invoke(label,entry,args):
        nonlocal active
        for r,v in saved.items():u.reg_write(r,v)
        for r,v in zip(ARGS,args):u.reg_write(r,v)
        u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_EFLAGS,2);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
        u.mem_write(SP,struct.pack('<Q',STOP))
        assert all(u.reg_read(r)==v for r,v in saved.items()) and all(u.reg_read(r)==v for r,v in zip(ARGS,args))
        active=dict(label=label,entry=hex(entry),args=[hex(a) for a in args],visited=[],calls=[],memory=[],invalid=[])
        error=None
        try:u.emu_start(entry,STOP,count=20000)
        except unicorn.UcError as e:error=str(e)
        active.update(error=error,rip=hex(u.reg_read(UC_X86_REG_RIP)),rax=hex(u.reg_read(UC_X86_REG_RAX)),returned=error is None and u.reg_read(UC_X86_REG_RIP)==STOP,stack_ok=u.reg_read(UC_X86_REG_RSP)==SP+8,nonvolatile_ok=all(u.reg_read(r)==v for r,v in saved.items()),arena=bytes(u.mem_read(ARENA,0xA8)).hex(),prefix=bytes(u.mem_read(p,0x500)).hex(),tail=bytes(u.mem_read(p+0xFFF00,0x100)).hex())
        results.append(active)
        return active
    sel=invoke('select-logical2',0x36C1F0,(2,5,0,0))
    assert sel['returned'] and sel['stack_ok'] and sel['nonvolatile_ok']
    assert struct.unpack('<I',u.mem_read(0x22D89BC,4))[0]==2 and struct.unpack('<I',u.mem_read(0x22D89C0,4))[0]==1
    alias_hash=None
    for i in range(steps):
        if alias and i==1:
            lo=p&0xFFFFFFFF;assert lo!=p
            u.mem_map(lo,0x100000)
            mirror=bytes(u.mem_read(p,0x100000));u.mem_write(lo,mirror)
            assert bytes(u.mem_read(lo,0x100000))==mirror
            alias_hash=hashlib.sha256(mirror).hexdigest()
        result=invoke('allocation'+str(i+1),0x36BC60,(2,size,0,direction))
        if not result['returned']:break
    if results[-1]['returned']:invoke('restore-selection',0x36C140,(0,0,0,0))
    return dict(name=name,fixture=fixture,backing=hex(p),direction=direction,size=size,requested_allocations=steps,fixture_sha256=fixture_hashes,alias_intervention=alias,alias_initial_sha256=alias_hash,steps=results)
predictions={
 'low-two-front':'two allocations return P+2C0/P+340 with stack/nonvolatile preserved',
 'above2-two-front':'same full addresses above2GiB, no foreign access',
 'above4-two-front':'first allocation retains high return; second follows a truncated prior block link and faults at a low address',
 'above4-two-front-low-alias':'mirror low alias before second allocation; detect writes into that separate region even if return succeeds',
 'above4-whole-block':'one whole-block allocation returns high pointer without a remainder link',
 'low-two-back':'two reverse allocations return P+FFFC0/P+FFF40',
 'above4-two-back':'first reverse allocation returns high; second follows truncated physical successor link and faults low'
}
cases=[run('low-two-front','low-address'),run('above2-two-front','above-2GiB'),run('above4-two-front','above-4GiB'),run('above4-two-front-low-alias','above-4GiB',alias=True),run('above4-whole-block','above-4GiB',size=0xFFD40,steps=1),run('low-two-back','low-address',direction=1),run('above4-two-back','above-4GiB',direction=1)]
out=dict(exe_sha256=SHA,fixture_receipt_sha256=hashlib.sha256(fixtures).hexdigest(),body_sha256={hex(a):hashlib.sha256(b).hexdigest() for a,b in B.items()},unicorn_version=unicorn.__version__,stubs=[],predictions=predictions,cases=cases)
Path('Database/Tools/work/ASTRA/arena-allocation-result.json').write_text(json.dumps(out,indent=2)+'\n')
for c in cases:
 print(c['name'])
 for s in c['steps']:print(s['label'],s['returned'],s['rax'],s['rip'],s['error'],s['invalid'])
