"""Original resource consumption with native resolver and explicit downstream stubs."""
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





ENTRY,RESOLVE,MPCOST,TIERCOST,MP,SEC,GET,SET,RESET,COUNT=0x305640,0x20E600,0x309110,0x308FF0,0x300CE0,0x300BC0,0x253690,0x254EE0,0x316440,0x253770
UNIT,STATS,ALT,HEAD,BASE,ROW,STACK,STOP=0x50000100,0x50002000,0x50002800,0x50003000,0x40000000,0x400100C0,0x60001800,0x70000000
BODIES={ENTRY:extract(ENTRY,393),RESOLVE:extract(RESOLVE,10)}
STUBS=(MPCOST,TIERCOST,MP,SEC,GET,SET,RESET,COUNT)
def run(name,kind=0,category=0,flag=0,mpcost=31,tiercost=2,maximum=100,extra=7,gil=100,unit=UNIT,stats=True,header=True,stride=64,swap=False,reset_stride=None,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for a in sorted({v&~4095 for v in [*BODIES,*STUBS,0x2EBF138,0x1F83530,STOP]}):u.mem_map(a,4096)
 for a,n in [(BASE,0x20000),(UNIT&~4095,0x4000),(0x60000000,0x3000)]:u.mem_map(a,n)
 for a,b in BODIES.items():u.mem_write(a,b)
 for a in STUBS:u.mem_write(a,b'\xc3')
 if mutant:
  assert bytes(u.mem_read(0x3056F9,7))==bytes.fromhex('488b8d98060000');u.mem_write(0x3056F9,bytes.fromhex('488b8d90060000'))
 def put(a,n,v):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
 u.mem_write(UNIT&~4095,b'\xa5'*0x4000)
 put(0x2EBF138,8,HEAD if header else 0);put(0x1F83530,8,BASE);put(HEAD+12,4,0x10000);put(HEAD+8,2,stride)
 put(UNIT+0x698,8,STATS if stats else 0);put(UNIT+0x690,8,STATS)
 for a,m,k in [(STATS,maximum,kind),(ALT,200,1)]:put(a+5,1,k);put(a+0x28,2,m)
 put(UNIT+0xDC8,2,0x789A);put(UNIT+0xE58,4,0x11223344);put(UNIT+0xE54,4,extra)
 put(ROW+0x1E,1,category);put(STACK,8,STOP)
 before={a:bytes(u.mem_read(a,n)) for a,n in [(BASE,0x20000),(UNIT&~4095,0x4000),(0x2EBF000,4096),(0x1F83000,4096)]}
 expected=[];ew=[];interventions=[];planned=[];res=0x789A;bank=0x11223344
 def ev(a,args):expected.append([a,args,res,bank])
 def s16(v):v&=0xFFFF;return v-0x10000 if v&0x8000 else v
 def u32(v):return v&0xFFFFFFFF
 normal=header and stride!=0 and unit and stats
 if header:ev(RESOLVE,[0x10000])
 if header and stride:
  aid=(0xC0//stride)&0xFFFF
  if unit and stats and kind==0:bank=0;res=0xFFFF;ew.extend([[UNIT+0xE58,4,0],[UNIT+0xDC8,2,res]])
  ev(MPCOST,[unit,aid]);ev(TIERCOST,[unit,aid])
  if unit:
   p=STATS if stats else 0;f=0x10+(flag&0xFFFFFFFF!=0)
   ev(MP,[p,u32(-mpcost),f])
   if swap:
    planned.extend([[UNIT+0x698,8,ALT],[UNIT+0xE54,4,13]]);p=ALT
   if stats or swap:
    ev(SEC,[p,u32(-s16(200 if swap else maximum)*tiercost),f]);ev(GET,[])
    balance=u32(gil-(13 if swap else extra));ev(SET,[balance if balance<0x80000000 else 0])
    if not swap and kind==0:
     if category in (0,1,2):ev(COUNT,[category,1])
     elif category==10:
      ev(RESET,[])
      if reset_stride is not None:planned.append([HEAD+8,2,reset_stride])
      ev(RESOLVE,[0x10000]);ev(COUNT,[13,0xC0//(reset_stride if reset_stride is not None else stride)])
 expected_pages={a:bytearray(b) for a,b in before.items()}
 for a,n,v in ew+planned:
  k=UNIT&~4095;expected_pages[k][a-k:a-k+n]=(v&((1<<(8*n))-1)).to_bytes(n,'little')
 events=[];writes=[];reads=[];invalid=[];visited=[]
 def step(uc,a,n,d):
  visited.append(a)
  if a not in (RESOLVE,*STUBS):return
  if a in (RESOLVE,SET):args=[uc.reg_read(UC_X86_REG_ECX)]
  elif a in (MPCOST,TIERCOST):args=[uc.reg_read(UC_X86_REG_RCX),uc.reg_read(UC_X86_REG_EDX)]
  elif a in (MP,SEC):args=[uc.reg_read(UC_X86_REG_RCX),uc.reg_read(UC_X86_REG_EDX),uc.reg_read(UC_X86_REG_R8D)]
  elif a==COUNT:args=[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)]
  else:args=[]
  events.append([a,args,int.from_bytes(uc.mem_read(UNIT+0xDC8,2),'little'),int.from_bytes(uc.mem_read(UNIT+0xE58,4),'little')])
  changes=[]
  if a==MP and swap:changes=[[UNIT+0x698,8,ALT],[UNIT+0xE54,4,13]]
  if a==RESET and reset_stride is not None:changes=[[HEAD+8,2,reset_stride]]
  for addr,width,value in changes:put(addr,width,value);interventions.append([addr,width,value])
  if a!=RESOLVE:
   for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
   uc.reg_write(UC_X86_REG_EAX,u32(mpcost if a==MPCOST else tiercost if a==TIERCOST else gil if a==GET else 0xAABBCCDD))
 u.hook_add(unicorn.UC_HOOK_CODE,step)
 u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
 u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
 def bad(uc,t,a,n,v,d):invalid.append([t,a,n]);return False
 u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
 saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_RCX,unit),(UC_X86_REG_RDX,ROW),(UC_X86_REG_R8D,flag&0xFFFFFFFF),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
 error=None
 try:u.emu_start(ENTRY,STOP,count=2000)
 except unicorn.UcError as ex:error=str(ex)
 if normal:
  assert error is None and u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8,(name,error,visited[-5:])
  assert all(u.reg_read(r)==v for r,v in saved.items());match=not invalid
 elif not header:match=invalid==[[19,12,4]] and error is not None
 elif not stride:match=error is not None and u.reg_read(UC_X86_REG_RIP)==0x305690 and not invalid
 elif not unit:match=invalid==[[19,0x698,8]] and error is not None
 else:match=invalid==[[19,0x28,2]] and error is not None
 match=bool(match and events==expected and writes==ew and interventions==planned and all(bytes(u.mem_read(a,len(b)))==b for a,b in expected_pages.items()))
 return dict(name=name,fixture=dict(kind=kind,category=category,flag=flag,mpcost=mpcost,tiercost=tiercost,maximum=maximum,extra=extra,gil=gil,unit=unit,stats=stats,header=header,stride=stride,swap=swap,reset_stride=reset_stride),events=events,expected_events=expected,writes=writes,expected_writes=ew,interventions=interventions,expected_interventions=planned,reads=reads,invalid=invalid,error=error,stop=u.reg_read(UC_X86_REG_RIP),visited=visited,matches=match)
cases=[run('base'),run('flag-one',flag=1),run('flag-negative',flag=-1),run('flag-low32',flag=0x100000000),run('kind1',kind=1),run('kind3',kind=3),run('category1',category=1),run('category2',category=2),run('category3',category=3),run('category9',category=9),run('category10',category=10),run('category11',category=11),run('zero-costs',mpcost=0,tiercost=0,extra=0),run('negative-costs',mpcost=-31,tiercost=-2),run('signed-cap',maximum=-100),run('overflow',tiercost=0x40000001,maximum=4),run('extra-gil-floor',extra=110),run('callback-stats-and-extra',swap=True),run('callback-stride',category=10,reset_stride=32),run('null-unit',unit=0),run('null-stats',stats=False),run('missing-header',header=False),run('zero-stride',stride=0)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-stale-stats',swap=True,mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} original consumption controls; stale-stats mutant detected')
