"""Original resource preparation with native resolver and explicit downstream stubs."""
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




ENTRY,RESOLVE,INVENTORY,COST,GET,SET=0x30EF20,0x20E600,0x3008A0,0x309060,0x253690,0x254EE0
UNIT,STATS,HEAD,BASE,ROW,STACK,STOP=0x50000100,0x50002000,0x50003000,0x40000000,0x400100C0,0x60001800,0x70000000
BODIES={ENTRY:extract(ENTRY,205),RESOLVE:extract(RESOLVE,10)}
def run(name,unit=UNIT,stats=True,kind=0,row=ROW,category=3,item=0x1234,cost=30,gil=100,stride=64,header=True,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for a in sorted({v&~4095 for v in [*BODIES,INVENTORY,COST,GET,SET,0x2EBF138,0x1F83530,STOP]}):u.mem_map(a,4096)
 for a,n in [(BASE,0x20000),(UNIT&~4095,0x4000),(0x60000000,0x3000)]:u.mem_map(a,n)
 for a,b in BODIES.items():u.mem_write(a,b)
 for a in (INVENTORY,COST,GET,SET):u.mem_write(a,b'\xc3')
 if mutant:
  assert bytes(u.mem_read(0x30EF9D,2))==bytes.fromhex('7416');u.mem_write(0x30EF9D,b'\x75')
 def put(a,n,v):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
 u.mem_write(UNIT&~4095,b'\xa5'*0x4000)
 put(0x2EBF138,8,HEAD if header else 0);put(0x1F83530,8,BASE);put(HEAD+12,4,0x10000);put(HEAD+8,2,stride)
 put(UNIT+0x698,8,STATS if stats else 0);put(STATS+5,1,kind);put(UNIT+0xDC8,2,0x789A);put(UNIT+0xE58,4,0x11223344)
 if row:put(row+0x1E,1,category);put(row+0x22,2,item)
 put(STACK,8,STOP)
 before={a:bytes(u.mem_read(a,n)) for a,n in [(BASE,0x20000),(UNIT&~4095,0x4000),(0x2EBF000,4096),(0x1F83000,4096)]}
 expected=[];expected_writes=[];reserved=0x789A;bank=0x11223344
 def event(a,args):expected.append([a,args,reserved,bank])
 if header:event(RESOLVE,[0x10000])
 normal=header and stride!=0
 if normal and unit and stats and kind==0:
  aid=(((row&0xFFFFFFFF)-0x40010000)&0xFFFFFFFF)//stride
  reserved=item if row and category==3 else 0xFFFF
  expected_writes.append([UNIT+0xDC8,2,reserved])
  if reserved!=0xFFFF:event(INVENTORY,[reserved,0xFFFFFFFF,0,1,0])
  event(COST,[unit,aid&0xFFFF]);bank=cost&0xFFFFFFFF
  expected_writes.append([UNIT+0xE58,4,bank])
  if bank:
   event(GET,[]);balance=(gil-bank)&0xFFFFFFFF;event(SET,[balance if balance<0x80000000 else 0])
 expected_pages={a:bytearray(b) for a,b in before.items()}
 for a,n,v in expected_writes:
  k=UNIT&~4095;expected_pages[k][a-k:a-k+n]=v.to_bytes(n,'little')
 events=[];writes=[];reads=[];invalid=[];visited=[]
 def step(uc,a,n,d):
  visited.append(a)
  if a not in (RESOLVE,INVENTORY,COST,GET,SET):return
  args=[]
  if a==RESOLVE:args=[uc.reg_read(UC_X86_REG_ECX)]
  elif a==COST:args=[uc.reg_read(UC_X86_REG_RCX),uc.reg_read(UC_X86_REG_EDX)]
  elif a==SET:args=[uc.reg_read(UC_X86_REG_ECX)]
  elif a==INVENTORY:args=[uc.reg_read(r) for r in (UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_R8D,UC_X86_REG_R9D)]+[int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP)+40,4),'little')]
  events.append([a,args,int.from_bytes(uc.mem_read(UNIT+0xDC8,2),'little'),int.from_bytes(uc.mem_read(UNIT+0xE58,4),'little')])
  if a!=RESOLVE:
   for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
   uc.reg_write(UC_X86_REG_EAX,(cost if a==COST else gil if a==GET else 0xAABBCCDD)&0xFFFFFFFF)
 u.hook_add(unicorn.UC_HOOK_CODE,step)
 u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
 u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
 def bad(uc,t,a,n,v,d):invalid.append([t,a,n]);return False
 u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
 saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_RCX,unit),(UC_X86_REG_RDX,row),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
 error=None
 try:u.emu_start(ENTRY,STOP,count=1000)
 except unicorn.UcError as ex:error=str(ex)
 if normal:
  assert error is None and u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8,(name,error,visited[-5:])
  assert all(u.reg_read(r)==v for r,v in saved.items())
  match=not invalid
 elif not header:match=invalid==[[19,12,4]] and error is not None
 else:match=error is not None and u.reg_read(UC_X86_REG_RIP)==0x30EF5B and not invalid
 match=match and events==expected and writes==expected_writes and all(bytes(u.mem_read(a,len(b)))==b for a,b in expected_pages.items())
 return dict(name=name,fixture=dict(unit=unit,stats=stats,kind=kind,row=row,category=category,item=item,cost=cost,gil=gil,stride=stride,header=header),events=events,expected_events=expected,writes=writes,expected_writes=expected_writes,reads=reads,invalid=invalid,error=error,stop=u.reg_read(UC_X86_REG_RIP),visited=visited,matches=match)
cases=[run('item-and-gil'),run('zero-cost',cost=0),run('gil-floor',gil=5),run('gil-exact',gil=30),run('non-item',category=2),run('item-sentinel',item=0xFFFF),run('item-zero',item=0),run('null-unit',unit=0),run('null-stats',stats=False),run('kind1',kind=1),run('null-row',row=0),run('unaligned-row',row=ROW+1),run('stride-truncation',row=ROW+63),run('signed-negative-cost',cost=-1),run('dword-subtraction-wrap',cost=1,gil=0x80000000),run('null-unit-missing-header',unit=0,header=False),run('null-unit-zero-stride',unit=0,stride=0)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-item-gate',mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in BODIES.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} original preparation controls; item-gate mutant detected')
