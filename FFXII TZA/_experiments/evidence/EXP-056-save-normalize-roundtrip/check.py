"""Original save normalization with explicit no-effect native dependencies."""
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

ENTRY,TAIL=0x584210,0x379CF0
SAVE,BATTLE,STACK,TIME=0x50000000,0x51000000,0x60000808,0x61000000
PTR,TIMER,RESET,IAT=0x2EBF190,0x1FD4A80,0x1E0C3EC,0x8C3060
BODY=extract(ENTRY,456)
STUBS=[0x2EF640,0x394450,0x320D50,0x322200,0x314DC0,0x329E40,0x269A20,0x2EF410,0x23A390,0x316810,TIME]
# Resolve the actual import descriptor/thunk; never infer its name from the address.
imports=struct.unpack_from('<I',raw,pe+24+112+8)[0]
def zstr(va):
    return extract(va,256).split(b'\0')[0].decode('ascii')
import_identity=None
for index in range(1000):
    original,stamp,chain,name,first=struct.unpack('<5I',extract(base+imports+20*index,20))
    if not any((original,stamp,chain,name,first)):break
    for n in range(2000):
        thunk=struct.unpack('<Q',extract(base+(original or first)+8*n,8))[0]
        if not thunk:break
        if base+first+8*n==IAT:
            import_identity=dict(iat=IAT,dll=zstr(base+name),name=zstr(base+thunk+2))
assert import_identity and import_identity['name']=='_time64',import_identity

def run(name,mode,flag,time=0x123456789ABCDEF0,timer=0x400000,initial=None,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    globals_pages=sorted({a&~4095 for a in (PTR,TIMER,RESET,IAT)})
    for page in sorted({v&~4095 for v in [ENTRY,TAIL,*STUBS,*globals_pages]}):u.mem_map(page,4096)
    u.mem_map(SAVE,0x50000);u.mem_map(BATTLE,0x8000);u.mem_map(0x60000000,0x3000)
    blob=BODY
    if mutant:
        offset=0x5843BE-ENTRY;assert blob[offset:offset+6]==bytes.fromhex('0fbaf11f03c8')
        blob=blob[:offset]+bytes.fromhex('03c80fbaf11f')+blob[offset+6:]
    u.mem_write(ENTRY,blob)
    u.mem_write(SAVE,bytes((i*13+7)&255 for i in range(0x50000)))
    u.mem_write(BATTLE,b'\xA5'*0x8000)
    for page in globals_pages:u.mem_write(page,b'\xC3'*4096)
    u.mem_write(PTR,struct.pack('<Q',BATTLE));u.mem_write(IAT,struct.pack('<Q',TIME))
    if initial:
        u.mem_write(SAVE,initial[0]);u.mem_write(BATTLE,initial[1])
    u.mem_write(SAVE+0x57,bytes([flag]));u.mem_write(TIMER,struct.pack('<I',timer))
    regions={SAVE:bytearray(u.mem_read(SAVE,0x50000)),BATTLE:bytearray(u.mem_read(BATTLE,0x8000))}
    regions.update({p:bytearray(u.mem_read(p,4096)) for p in globals_pages})
    expected=[];events=[];visits=[]
    def read(a,n):return bytes(u.mem_read(a,n))
    def call(a,args=()):return dict(kind='call',address=a,args=list(args))
    def write(a,n,v):
        expected.append(dict(kind='write',address=a,bytes=n,value=v))
        origin=next(p for p,b in regions.items() if p<=a<a+n<=p+len(b))
        regions[origin][a-origin:a-origin+n]=v.to_bytes(n,'little')
    def copy(dst,src,n):write(dst,n,int.from_bytes(read(src,n),'little'))
    def snapshot():return dict(active=read(SAVE+0xC,16).hex(),flag=read(SAVE+0x57,1).hex(),stash=read(SAVE+0x70,36).hex(),fields=read(SAVE+0x1244,20).hex(),battle_flag=read(BATTLE+0x5B04,4).hex())
    before=snapshot()
    expected.extend([call(0x2EF640),call(0x2EF640),call(0x394450)])
    path='stash' if (mode&255)==3 and not flag&1 else 'restore' if (mode&255)!=3 and flag&1 else 'neither'
    accumulator=0xFEDCBA98
    if path=='stash':
        for dst,src,n in [(0x70,0x10,8),(0x78,0x18,2),(0x7A,0x1A,1),(0x7B,0x1B,1)]:copy(SAVE+dst,SAVE+src,n)
        expected.append(call(0x320D50));write(SAVE+0x7C,4,accumulator)
        for n in range(5):copy(SAVE+0x80+4*n,SAVE+0x1244+4*n,4)
        write(SAVE+0x1248,4,0);write(BATTLE+0x5B04,4,int.from_bytes(read(BATTLE+0x5B04,4),'little')&0xFFFFFFFE)
        write(SAVE+0x10,8,0);write(SAVE+0x18,4,0);expected.append(call(0x322200))
        write(SAVE+0xC,4,0);expected.append(call(0x314DC0,[0x483]))
    if path=='restore':
        for dst,src,n in [(0x10,0x70,8),(0x18,0x78,2),(0x1A,0x7A,1),(0x1B,0x7B,1),(0xC,0x7C,4)]:copy(SAVE+dst,SAVE+src,n)
        expected.append(call(0x329E40,[int.from_bytes(read(SAVE+0x7C,4),'little')]))
        for n in range(5):copy(SAVE+0x1244+4*n,SAVE+0x80+4*n,4)
        expected.append(call(0x269A20,[SAVE+0xE240]));write(SAVE+0x57,1,flag&254)
        expected.append(call(0x2EF410,[SAVE+0x4E660]));write(RESET,4,0)
        write(BATTLE+0x5B04,4,int.from_bytes(read(BATTLE+0x5B04,4),'little')&0xFFFFFFFE)
        expected.append(call(0x23A390,[0]))
    expected.extend([call(0x316810),call(TIME,[0])])
    time_term=(((time+0x2B5A5)&0xFFFFFFFF)*33+(time>>32))&0x7FFFFFFF
    seed=(time_term+600*timer)&0xFFFFFFFF
    expected.append(dict(kind='seed-tail',address=TAIL,seed=seed))
    def step(uc,a,size,data):
        visits.append(a)
        if a==TAIL:
            events.append(dict(kind='seed-tail',address=a,seed=uc.reg_read(UC_X86_REG_ECX)));uc.emu_stop();return
        if a not in STUBS:return
        args=[]
        if a in (0x314DC0,0x329E40,0x23A390):args=[uc.reg_read(UC_X86_REG_ECX)]
        if a in (0x269A20,0x2EF410,TIME):args=[uc.reg_read(UC_X86_REG_RCX)]
        events.append(call(a,args))
        result={0x2EF640:SAVE,0x394450:mode,0x320D50:accumulator,TIME:time}.get(a,0xBADF00D)
        uc.reg_write(UC_X86_REG_RAX,result);uc.reg_write(UC_X86_REG_RCX,0xBADF00D);uc.reg_write(UC_X86_REG_RDX,0xBADF00D)
        rsp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,int.from_bytes(read(rsp,8),'little'));uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    def memory_write(uc,access,a,n,v,data):
        if not 0x60000000<=a<0x60003000:events.append(dict(kind='write',address=a,bytes=n,value=v&((1<<(8*n))-1)))
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory_write)
    saved={UC_X86_REG_RBX:111,UC_X86_REG_RSI:222,UC_X86_REG_RDI:333}
    for reg,v in saved.items():u.reg_write(reg,v)
    u.mem_write(STACK,struct.pack('<Q',0x60002000));u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(ENTRY,0,count=1000)
    assert u.reg_read(UC_X86_REG_RIP)==TAIL and u.reg_read(UC_X86_REG_RSP)==STACK
    assert all(u.reg_read(r)==v for r,v in saved.items()) and int.from_bytes(read(STACK,8),'little')==0x60002000
    memory_matches=all(read(p,len(b))==bytes(b) for p,b in regions.items())
    result=dict(name=name,mode=mode,flag=flag,time=time,timer=timer,path=path,before=before,after=snapshot(),
        expected_seed=seed,observed_seed=u.reg_read(UC_X86_REG_ECX),events=events,expected_events=expected,visited=visits,
        memory_matches=memory_matches,matches=memory_matches and events==expected)
    return result,(read(SAVE,0x50000),read(BATTLE,0x8000))

cases=[]
for mode,flag in [(3,0xA4),(3,0xA5),(0,0xA4),(0,0xA5),(0x103,0xA4),(4,0xA5)]:
    cases.append(run(f'mode-{mode}-flag-{flag}',mode,flag)[0])
for time,timer in [(0,0),(0xFFFFFFFFFFFFFFFF,1),(0x8000000000000000,0xFFFFFFFF)]:
    cases.append(run(f'seed-{time}-{timer}',0,0xA4,time,timer)[0])
stash,state=run('roundtrip-stash',3,0xA4);cases.append(stash)
no_restore,_=run('roundtrip-mode-only-no-flag-set',0,0xA4,initial=state);cases.append(no_restore)
restore,_=run('roundtrip-external-flag-set',0,0xA5,initial=state);cases.append(restore)
assert restore['after']['active'][8:]==stash['before']['active'][8:]
assert restore['after']['fields']==stash['before']['fields']
assert restore['after']['active'][:8]==struct.pack('<I',0xFEDCBA98).hex()
assert all(c['matches'] for c in cases)
fault,_=run('mutant-masks-after-timer-add',0,0xA4,mutant=True)
assert not fault['matches'] and fault['memory_matches'] and fault['observed_seed']==fault['expected_seed']&0x7FFFFFFF
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    import_identity=import_identity,cases=cases,mask_order_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'00584210.bin').write_bytes(BODY)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for i in cs.disasm(BODY,ENTRY))+'\n')
print('PASS: twelve cases; mode/flag matrix, explicit-flag roundtrip, seed boundaries; wrong mask order detected')
print(import_identity)
