"""Native decoder composed with installer: zero references and relocation bases."""
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
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert hashlib.sha256(raw).hexdigest() == EXE_SHA
pe = struct.unpack_from('<I', raw, 60)[0]
base = struct.unpack_from('<Q', raw, pe + 48)[0]
assert base == 0x120000
sect = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]
def extract(va, size):
    for n in range(struct.unpack_from('<H', raw, pe + 6)[0]):
        _, rva, length, disk = struct.unpack_from('<4I', raw, sect + 40*n + 8)
        offset = va - base - rva
        if 0 <= offset and offset + size <= length:
            out = raw[disk+offset:disk+offset+size]
            assert len(out) == size
            return out
    raise AssertionError(hex(va))

ENTRY, SIZE = 0x23A570, 1808
BODY = extract(ENTRY, SIZE)
CONST = {a:extract(a,4) for a in (0x1CEBC78,0x902438,0x901B3C)}
assert {a:b.hex() for a,b in CONST.items()} == {0x1CEBC78:'db0fc940',0x902438:'0000b443',0x901B3C:'0000c03f'}
UNIT, DEF, CLASS, SPAWN = 0x40000000, 0x40001000, 0x40002000, 0x40003000
DESCS, RB, RL, ORDER = 0x40004000, 0x40005000, 0x40006000, 0x40007000
STACK, STOP = 0x60001808, 0x70000000
RESET, SELECT, REKEY, RESOLVE, GETSPAWN = 0x236A60,0x303EC0,0x322050,0x20E600,0x236100
TEXT, TRACKED, ENGAGED, HP = 0x2B58B0,0x328FF0,0x237040,0x2FEAB0
STUBS = (RESET,SELECT,REKEY,GETSPAWN,TEXT,TRACKED,ENGAGED,HP)
RESOLVER_BODY = extract(RESOLVE,10)
assert hashlib.sha256(RESOLVER_BODY).hexdigest() == '8bde921e0db5b4c6b16e649c4df8172da2b8b8c3462664b675b377cf37450f65'
BASE_GUARD, LEVEL_GUARD = 0x23A747, 0x23A768
NONVOL = (UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
VOLATILE = (UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11)
def sha(b): return hashlib.sha256(b).hexdigest()

def run(name, ib=1, il=2, nb=2, nl=3, base_present=True, level_present=True,
        reloc=0x10000000, base_ref=None, level_ref=None, mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages={a&~4095 for a in (ENTRY,RESOLVE,*STUBS,*CONST,0x1F83530,0x2089300,0x2EBF120)}
    for p in sorted(pages): u.mem_map(p,4096)
    u.mem_map(UNIT,0x8000); u.mem_map(0x60000000,0x3000)
    u.mem_write(ENTRY,BODY)
    for a,b in CONST.items(): u.mem_write(a,b)
    for a in STUBS: u.mem_write(a,b'\xc3')
    decoder=RESOLVER_BODY
    if mutant:
        # Incorrect zero-sentinel handling, otherwise the same native addition.
        decoder=bytes.fromhex('85c9750331c0c38bc1480305')+struct.pack('<i',0x1F83530-(RESOLVE+16))+b'\xc3'
    u.mem_write(RESOLVE,decoder)
    def put(a,fmt,*v): u.mem_write(a,struct.pack('<'+fmt,*v))
    # All local records are initialized explicitly. Native reset is a NO-WRITE stub;
    # these are fixture preconditions, not a claim about that callee's native effects.
    u.mem_write(UNIT,b'\xa5'*0x1000)
    put(UNIT,'Q',1<<26);put(UNIT+0x40,'Q',0x13572468)
    put(UNIT+0x57,'B',0xFE);put(UNIT+0x698,'Q',0);put(UNIT+0xEA9,'B',0x27)
    put(DEF+0,'H',0);put(DEF+0x22,'H',ib);put(DEF+0x24,'H',il);put(DEF+0x50,'H',0)
    put(CLASS+4,'BBH',2,1,0x1234)
    put(SPAWN,'B',1) # existing initialized record; skips initialization/history paths
    put(0x2089300,'I',1)
    # Table descriptors: count +4, stride +8, encoded reference +12.
    def desc(a,count,stride,token): put(a,'IIHHI',0,count,stride,0,token)
    encoded=lambda pointer:(pointer-reloc)&0xFFFFFFFF
    refs={0x1111:encoded(DEF),0x2222:encoded(CLASS),0x3333:encoded(RB) if base_ref is None else base_ref,0x4444:encoded(RL) if level_ref is None else level_ref,0x5555:encoded(ORDER)}
    decode=lambda reference:(reference+reloc)&0xFFFFFFFFFFFFFFFF
    base_resolves=decode(refs[0x3333])!=0;level_resolves=decode(refs[0x4444])!=0
    put(0x1F83530,'Q',reloc)
    desc(DESCS,1,0x60,refs[0x1111]);desc(DESCS+0x20,1,0x60,refs[0x2222])
    desc(DESCS+0x40,nb,0x38,refs[0x3333]);desc(DESCS+0x60,nl,0x38,refs[0x4444])
    put(DESCS+0x80,'HHI',1,0,refs[0x5555])
    for slot,ptr in [(0x2EBF120,DESCS),(0x2EBF150,DESCS+0x20),
                     (0x2EBF148,DESCS+0x40 if base_present else 0),
                     (0x2EBF140,DESCS+0x60 if level_present else 0),
                     (0x2EBF168,DESCS+0x80),(0x2EBF170,0)]: put(slot,'Q',ptr)
    expected={p:bytearray(u.mem_read(p,4096)) for p in [*range(UNIT,UNIT+0x8000,4096),0x2089000,0x2EBF000,0x1F83000,*{a&~4095 for a in CONST}]}
    before={p:bytes(b) for p,b in expected.items()}
    # Independent guard expression retains unsigned count-1 underflow explicitly.
    reject_base = ib > (((nb if base_present else 0)-1)&0xFFFFFFFF)
    reject_level = not reject_base and il > (((nl if level_present else 0)-1)&0xFFFFFFFF)
    success = not (reject_base or reject_level)
    expected_rbp = (decode(refs[0x3333])+ib*0x38)&0xFFFFFFFF if base_present and base_resolves else 0
    expected_rlp = (decode(refs[0x4444])+il*0x38)&0xFFFFFFFF if level_present and level_resolves else 0
    wanted_calls=[(RESET,UNIT),(SELECT,None),(REKEY,UNIT),(RESOLVE,0x1111),(RESOLVE,0x1111),(RESOLVE,0x2222),(RESOLVE,0x2222)]
    if success:
        wanted_calls += [(GETSPAWN,(0x13572468,0xFFFFFFFE)),(RESOLVE,0x1111),(TEXT,0),(RESOLVE,0x5555)]
        if base_present: wanted_calls += [(RESOLVE,0x3333)]*(2 if base_resolves else 1)
        if level_present: wanted_calls += [(RESOLVE,0x4444)]*(2 if level_resolves else 1)
        wanted_calls += [(TRACKED,(0,0,0x27)),(ENGAGED,UNIT),(HP,UNIT)]
        def exp(a,fmt,*v):
            b=struct.pack('<'+fmt,*v);p=a&~4095;expected[p][a-p:a-p+len(b)]=b
        for off,v in [(0xE60,DEF),(0xE68,CLASS),(0x6E0,decode(refs[0x5555])),(0xE70,expected_rbp),(0xE78,expected_rlp),(0x698,SPAWN+0x80),(0x6A0,SPAWN),(0x18,0)]: exp(UNIT+off,'Q',v)
        for off in (0x64,0x6C,0x48,0x68):exp(UNIT+off,'I',0)
        exp(UNIT+0x55,'B',2);exp(UNIT+0x56,'B',1);exp(UNIT+0x52,'H',0x1234);exp(UNIT+0x54,'B',0xFF)
        exp(UNIT,'Q',(1<<26)|4)
    wanted_calls=[(a,refs[arg] if a==RESOLVE else arg) for a,arg in wanted_calls]
    put(STACK,'Q',STOP)
    for i,r in enumerate(VOLATILE): u.reg_write(r,0x1111111100000000+i)
    saved={r:0xA100000000000000+i for i,r in enumerate(NONVOL)}
    saved.update({UC_X86_REG_XMM6+i: (0x13579BDF2468ACE00123456789ABCDEF ^ (i*0x1010101010101010101010101010101)) for i in range(10)})
    for r,v in saved.items():u.reg_write(r,v)
    u.reg_write(UC_X86_REG_RCX,UNIT);u.reg_write(UC_X86_REG_RDX,0x100);u.reg_write(UC_X86_REG_RSP,STACK)
    u.reg_write(UC_X86_REG_MXCSR,0x1F80);u.reg_write(UC_X86_REG_EFLAGS,2)
    for r,v in saved.items(): assert u.reg_read(r)==v
    assert all(bytes(u.mem_read(p,4096))==b for p,b in before.items())
    visited=[];calls=[];reads=[];writes=[]
    def code(uc,a,n,_):
        visited.append(a)
        if a==RESOLVE:
            calls.append((a,uc.reg_read(UC_X86_REG_RCX)))
        elif a in STUBS:
            rcx=uc.reg_read(UC_X86_REG_RCX);rdx=uc.reg_read(UC_X86_REG_RDX)&0xFFFFFFFF;r8=uc.reg_read(UC_X86_REG_R8)&0xFFFFFFFF
            arg=None if a==SELECT else (rcx,rdx) if a==GETSPAWN else (rcx,rdx,r8) if a==TRACKED else rcx
            calls.append((a,arg))
            result=SPAWN if a==GETSPAWN else 0
            for i,r in enumerate(VOLATILE):uc.reg_write(r,0xCCCC000000000000+i)
            for i in range(6):uc.reg_write(UC_X86_REG_XMM0+i,(1<<128)-1-i)
            uc.reg_write(UC_X86_REG_RAX,result)
        elif not (ENTRY<=a<ENTRY+SIZE or RESOLVE<=a<RESOLVE+len(decoder)):
            raise AssertionError('unexpected original target '+hex(a))
    def mem(uc,access,a,n,v,_):
        if 0x60000000<=a<0x60003000:return
        rec=[uc.reg_read(UC_X86_REG_RIP),a,n]
        if access==unicorn.UC_MEM_WRITE: writes.append(rec+[int(v).to_bytes(n,'little',signed=False).hex()])
        else:reads.append(rec+[bytes(uc.mem_read(a,n)).hex()])
    u.hook_add(unicorn.UC_HOOK_CODE,code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,mem)
    u.emu_start(ENTRY,STOP,count=3000)
    after={p:bytes(u.mem_read(p,4096)) for p in expected}
    checks=dict(return_boundary=u.reg_read(UC_X86_REG_RIP)==STOP,stack=u.reg_read(UC_X86_REG_RSP)==STACK+8,
                nonvolatile=all(u.reg_read(r)==v for r,v in saved.items()),eax=u.reg_read(UC_X86_REG_RAX)==int(success),
                calls=calls==wanted_calls,fixture_pages=all(after[p]==b for p,b in expected.items()),
                guard_path=(BASE_GUARD in visited and ((LEVEL_GUARD in visited)==(not reject_base)) and ((0x23A76E in visited)==success)),
                reward_stores=((0x23A9A5 in visited)==success and (0x23A9F4 in visited)==success))
    deltas={f'{p:08X}':[[i,b,after[p][i]] for i,b in enumerate(old) if after[p][i]!=b] for p,old in before.items() if after[p]!=old}
    return dict(name=name,inputs=dict(ib=ib,il=il,nb=nb,nl=nl,base_present=base_present,level_present=level_present,reloc=reloc,refs=refs),mutant=mutant,
                expected=dict(success=success,reject_base=reject_base,reject_level=reject_level,base_pointer=expected_rbp,level_pointer=expected_rlp),
                eax=u.reg_read(UC_X86_REG_RAX),reward_pointers=list(struct.unpack('<QQ',u.mem_read(UNIT+0xE70,16))),order_pointer=struct.unpack('<Q',u.mem_read(UNIT+0x6E0,8))[0],calls=calls,expected_calls=wanted_calls,
                visited=visited,reads=reads,writes=writes,before_page_sha256={f'{p:08X}':sha(b) for p,b in before.items()},after_page_sha256={f'{p:08X}':sha(b) for p,b in after.items()},deltas=deltas,checks=checks,matches=all(checks.values()))

cases=[run('nonzero-relocation'),run('zero-reference-base',base_ref=0),run('zero-reference-level',level_ref=0),
       run('zero-base-zero-reference',reloc=0,base_ref=0),run('zero-base-level-reference',reloc=0,level_ref=0),
       run('wrapped-sum-null',reloc=0xFFFFFFFFFFFFF000,base_ref=0x1000),
       run('high-relocation-word',reloc=0x100000000)]
mutants=[run('mutant-zero-sentinel',base_ref=0,mutant=True)]
result=dict(status='PASS' if all(c['matches'] for c in cases) and all(not m['matches'] for m in mutants) else 'FAIL',
            exe_sha256=EXE_SHA,source_sha256=sha(Path(__file__).read_bytes()),body_sha256=sha(BODY),unicorn=unicorn.__version__,capstone=capstone.__version__,cases=cases,mutants=mutants)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'0023A570.bin').write_bytes(BODY)
(HERE/'0020E600.bin').write_bytes(RESOLVER_BODY)
for a,b in CONST.items():(HERE/f'{a:08X}.bin').write_bytes(b)
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in [(ENTRY,BODY),(RESOLVE,RESOLVER_BODY)] for i in md.disasm(b,a))+'\n')
print(result['status'],len(cases),'controls',len(mutants),'mutants')
for c in cases+mutants:print(c['name'],c['eax'],[f'{p:016X}' for p in c['reward_pointers']],c['checks'])
assert result['status']=='PASS'
