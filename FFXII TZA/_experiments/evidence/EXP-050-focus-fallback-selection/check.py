"""Original focus-selection body with explicit controlled dependency returns."""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone,unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent
raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];base=struct.unpack_from('<Q',raw,pe+48)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
def extract(va,size):
    found=[]
    for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,length,disk=struct.unpack_from('<4I',raw,table+40*n+8)
        if rva<=va-base<rva+length:found.append(raw[disk+va-base-rva:disk+va-base-rva+size])
    assert len(found)==1
    return found[0]
code=extract(0x326500,274)
encoder=extract(0x3589B0,38)
assert encoder==(HERE.parent/'EXP-048-handle-discriminator-advance/003589B0.bin').read_bytes()
STUBS=(0x311E20,0x326620,0x30D9A0,0x377C70,0x31B770,0x322C50,0x2367A0,0x263750,0x317400)
PRIMARY,FALLBACK,ACTOR,STATE,STACK,RETURN=0x50000100,0x50002000,0x50004000,0x70000000,0x60000800,0x60001000
TAIL=0x3594B0


def run(name,mode=0,second_mode=None,primary=True,primary_stats=True,fallback_slot=None,
        actor=True,disabled=(),field_selector=0x123,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for page in sorted({a&~4095 for a in STUBS+(0x326500,0x3589B0,TAIL)}):u.mem_map(page,4096)
    blob=code
    if mutant:
        assert blob[0xC0:0xC3]==bytes.fromhex('83ff04')
        blob=blob[:0xC2]+b'\x03'+blob[0xC3:]
    u.mem_write(0x326500,blob);u.mem_write(0x3589B0,encoder)
    for addr,size in ((0x50000000,0x6000),(STATE,0x6000),(0x2EBF000,4096),(0x60000000,0x2000)):
        u.mem_map(addr,size)
    for address,fmt,value in ((0x2EBF190,'<Q',STATE),(STATE+0x5AA4,'<B',7),
        (PRIMARY+0x698,'<Q',0x12340000 if primary_stats else 0),(FALLBACK+0x698,'<Q',0x12350000),
        (PRIMARY+8,'<I',0xA1234567),(FALLBACK+8,'<I',0xB2345678),
        (ACTOR,'<H',5),(ACTOR+0x15,'<B',2),(ACTOR+0x16,'<H',9)):
        u.mem_write(address,struct.pack(fmt,value))
    for slot in range(4):u.mem_write(STATE+0x5A5A+2*slot,bytes([11+slot,0xE0+slot]))
    expected_selector=7 if mode in (0,1) else 0x1A if mode==2 else field_selector&255 if mode==3 else 255
    successful_primary=primary and primary_stats
    successful_fallback=not successful_primary and fallback_slot is not None and fallback_slot not in disabled
    chosen=PRIMARY if successful_primary else FALLBACK if successful_fallback else 0
    wanted_handle=0xA1234567 if chosen==PRIMARY else 0xB2345678 if chosen==FALLBACK else 0x920005 if actor else 0
    modes=iter([mode,mode if second_mode is None else second_mode])
    calls=[];visited=[];writes=[];tail=[]
    def step(uc,address,size,data):
        visited.append(address)
        if address==TAIL:
            tail.append(uc.reg_read(UC_X86_REG_RCX));uc.emu_stop();return
        if address==0x3589B0:
            calls.append(dict(va=address,args=[uc.reg_read(UC_X86_REG_RCX)],method='original encoder'))
            return
        if address not in STUBS:return
        rcx,rdx,r8=[uc.reg_read(r) for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8)]
        args=[];value=0
        if address==0x30D9A0:value=next(modes)
        elif address==0x377C70:value=field_selector
        elif address==0x31B770:
            args=[rcx];value=PRIMARY if primary else 0
        elif address==0x322C50:
            args=[rcx,rdx,r8];assert rcx==0x17 and r8==0 and rdx<4
            value=int(rdx not in disabled)
        elif address==0x2367A0:
            args=[rcx];value=FALLBACK if fallback_slot is not None and rcx==11+fallback_slot else 0
        elif address==0x263750:args=[rcx];assert rcx==0;value=ACTOR if actor else 0
        elif address==0x317400:args=[rcx]
        calls.append(dict(va=address,args=args,result=value,method='controlled return; native effects omitted'))
        rsp=uc.reg_read(UC_X86_REG_RSP);resume=struct.unpack('<Q',uc.mem_read(rsp,8))[0]
        uc.reg_write(UC_X86_REG_RAX,value);uc.reg_write(UC_X86_REG_RSP,rsp+8);uc.reg_write(UC_X86_REG_RIP,resume)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:
        writes.append(dict(address=address,bytes=size)) if not 0x60000000<=address<0x60002000 else None)
    u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(0x326500,0,count=500)
    assert u.reg_read(UC_X86_REG_RIP)==TAIL and u.reg_read(UC_X86_REG_RSP)==STACK
    assert struct.unpack('<Q',u.mem_read(STACK,8))[0]==RETURN and not writes
    expected=[(0x311E20,[]),(0x326620,[]),(0x30D9A0,[])]
    if mode==3:expected.append((0x377C70,[]))
    expected.append((0x31B770,[expected_selector]))
    if not successful_primary:
        for slot in range((fallback_slot+1) if successful_fallback else 4):
            expected.extend([(0x322C50,[0x17,slot,0]),(0x2367A0,[255 if slot in disabled else 11+slot])])
    if chosen:
        expected.append((0x30D9A0,[]))
        if (mode if second_mode is None else second_mode)==1:expected.append((0x317400,[chosen]))
    else:
        expected.append((0x263750,[0]))
        if actor:expected.append((0x3589B0,[ACTOR]))
    expected.append((0x311E20,[]))
    return dict(name=name,matches=[(c['va'],c['args']) for c in calls]==expected and tail==[wanted_handle],
        calls=calls,expected_calls=[dict(va=a,args=b) for a,b in expected],tail_handle=tail,
        expected_handle=wanted_handle,visited=visited,nonstack_writes=writes,
        boundary='tail dispatch entry; native dispatcher not executed')


cases=[run('preferred-mode0'),run('preferred-mode1',mode=1),run('mode2-fixed-selector',mode=2),
       run('mode3-low-byte-selector',mode=3),run('other-mode-ff',mode=4),
       run('second-mode-read',mode=0,second_mode=1),
       run('first-fallback',primary=False,fallback_slot=0),
       run('last-fallback-after-null-stats',primary_stats=False,fallback_slot=3,disabled=(0,)),
       run('fallback-disabled',primary=False,fallback_slot=0,disabled=(0,)),
       run('no-units-slot0-actor',primary=False),run('no-actor',primary=False,actor=False)]
assert all(c['matches'] for c in cases)
fault=run('three-slot-mutant',primary=False,fallback_slot=3,mutant=True);assert not fault['matches']
result=dict(status='PASS',method='original focus body and encoder; all other callees controlled; stop before native tail dispatcher',
    exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cases=cases,three_slot_mutant=fault)
(HERE/'function.bin').write_bytes(code);(HERE/'encoder.bin').write_bytes(encoder)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for i in cs.disasm(code,0x326500))+'\n')
print('PASS: eleven selection/call-order cases; omitted fourth fallback detected')
