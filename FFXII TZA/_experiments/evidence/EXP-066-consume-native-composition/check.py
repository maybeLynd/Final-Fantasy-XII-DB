"""Original cost, consumption and resource writers composed in one synthetic state."""
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






ENTRY,COST,TIER,MOD,CHANNEL,RESOLVE,MP,SEC,REC,NOOP=0x305640,0x309110,0x308FF0,0x2F95D0,0x2F9820,0x20E600,0x300CE0,0x300BC0,0x30E060,0x16D6A0
OWNER,GLOBAL,ELIG,GET,SET=0x31B860,0x30B770,0x30B7F0,0x253690,0x254EE0
UNIT,STATS,HEAD,EHEAD,BASE,ROWS,EROWS,STACK,STOP=0x50000100,0x50002000,0x50003000,0x50003020,0x40000000,0x40010000,0x40020000,0x60001800,0x70000000
BODIES={a:extract(a,n) for a,n in [(ENTRY,393),(COST,165),(TIER,110),(MOD,589),(CHANNEL,51),(RESOLVE,10),(MP,351),(SEC,207),(REC,200),(NOOP,3)]}
CONSTANTS={a:extract(a,4) for a in (0x8F3130,0x8F3134,0x916318)}
assert [struct.unpack('<f',b)[0] for b in CONSTANTS.values()]==[50.0,100.0,64.0]
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def sx(v,b):return v-(1<<b) if v&(1<<(b-1)) else v
def u32(v):return v&0xFFFFFFFF
def run(name,action=12,category=3,cost=31,kind=0,effects=(),percent=(10,15,20),flag=0,live=40,secondary=150,cap=100,mult=3,tier=1,gm=(),mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 stubs={OWNER:1,GLOBAL:0,ELIG:2,GET:0,SET:1}
 for a in sorted({v&~4095 for v in [*BODIES,*CONSTANTS,*stubs,0x2EBF138,0x1F83530,STOP]}):u.mem_map(a,4096)
 for a,n in [(BASE,0x30000),(UNIT&~4095,0x4000),(0x60000000,0x3000)]:u.mem_map(a,n)
 for a,b in {**BODIES,**CONSTANTS}.items():u.mem_write(a,b)
 for a in stubs:u.mem_write(a,b'\xc3')
 if mutant:
  assert bytes(u.mem_read(0x3056EC,2))==bytes.fromhex('f7db');u.mem_write(0x3056EC,b'\x90\x90')
 def put(a,n,v):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
 u.mem_write(UNIT&~4095,b'\xa5'*0x4000)
 for a,n,v in [(0x2EBF138,8,HEAD),(0x2EBF040,8,EHEAD),(0x1F83530,8,BASE),(HEAD+8,2,64),(HEAD+12,4,0x10000),(EHEAD+8,2,8),(EHEAD+12,4,0x20000),(UNIT+0x698,8,STATS),(UNIT+0xE58,4,123),(UNIT+0xDC8,2,0x4567),(UNIT+0xE54,4,7),(STATS+5,1,kind),(STATS+6,2,secondary),(STATS+0x28,2,cap),(STATS+0x37,1,mult),(STATS+0x4C,2,live),(STATS+0x4E,1,tier)]:put(a,n,v)
 row=ROWS+action*64;put(row+10,1,cost);put(row+30,1,category)
 for off in (0x6C,0x7C,0x6E,0x7E,0x73,0x83):put(STATS+off,1,0)
 masks={}
 for off,mask in effects:masks[off]=masks.get(off,0)|mask;put(STATS+off,1,masks[off])
 for i,v in enumerate(percent):put(EROWS+(0x5B+i)*8+4,2,v)
 put(STACK,8,STOP)
 before={a:bytes(u.mem_read(a,n)) for a,n in [(BASE,0x30000),(UNIT&~4095,0x4000),(0x2EBF000,4096),(0x1F83000,4096)]}
 expected_pages={a:bytearray(b) for a,b in before.items()};events=[];gidx=0
 def call(a,args):events.append(['call',a,args])
 def write(a,n,v):
  v&=(1<<(8*n))-1;events.append(['write',a,n,v]);k=UNIT&~4095;expected_pages[k][a-k:a-k+n]=v.to_bytes(n,'little')
 def get(off,n):k=UNIT&~4095;return int.from_bytes(expected_pages[k][STATS+off-k:STATS+off-k+n],'little')
 def effect(off,mask):return bool((masks.get(off,0)|masks.get(off+16,0))&mask)
 def resolves(token=0x10000):call(RESOLVE,[token]);call(RESOLVE,[token])
 def gates():
  nonlocal gidx
  call(GLOBAL,[]);g=gm[gidx] if gidx<len(gm) else 0;gidx+=1;call(ELIG,[0,0]);return g
 f=0x10+bool(flag&0xFFFFFFFF)
 def reconcile():
  call(REC,[STATS,f]);call(OWNER,[STATS]);maximum=sx(get(0x28,2),16)
  if maximum<=0:return
  old=get(0x4E,1);new=int(sx(get(6,2),16)/maximum) if get(0x37,1)>0 else 0
  if old!=new:call(NOOP,[STATS,u32(new-old)])
  write(STATS+0x4E,1,new)
 def sec(delta):
  call(SEC,[STATS,u32(delta),f]);call(OWNER,[STATS])
  if not(f&1) and gates()&0xFFFF:return
  total=sx(u32(sx(get(6,2),16)+delta),32);maximum=0 if effect(0x6C,128) else sx(get(0x28,2),16)*(get(0x37,1) or 1)
  write(STATS+6,2,0 if total<0 else min(total,maximum));reconcile()
 call(ENTRY,[UNIT,row,flag&0xFFFFFFFF]);call(RESOLVE,[0x10000])
 if kind==0:write(UNIT+0xE58,4,0);write(UNIT+0xDC8,2,0xFFFF)
 call(COST,[UNIT,action]);resolves();amount=0
 if category not in (5,6):
  call(CHANNEL,[UNIT])
  if kind==1 or not effect(0x6C,1):
   call(MOD,[UNIT,action]);resolves()
   if kind!=1 and (0xD0<=action<=0xE1 or 0x106<=action<=0x112):amount=cost
   elif effect(0x6C,1):amount=10*int(f32(f32(cost*64.0)/50.0))
   else:
    reduction=0
    for bit,p in zip((8,16,32),percent):
     if effect(0x73,bit):resolves(0x20000);reduction+=p
    amount=int(f32(f32(cost)-f32(f32(f32(cost)/100.0)*f32(reduction))))
    if effect(0x6E,8):amount=0
    elif effect(0x6C,16):amount=int(amount/2)
 call(TIER,[UNIT,action]);resolves();tieramount=cost if category in (5,6) else 0
 delta=-amount;call(MP,[STATS,u32(delta),f]);call(OWNER,[STATS])
 admitted=True
 if not(f&1) and gates()&0xFFFF:admitted=False
 if admitted:
  old=sx(get(0x4C,2),16);total=sx(u32(old+delta),32);maximum=0 if effect(0x6C,128) else sx(get(0x28,2),16);value=0 if total<0 else min(total,maximum)
  if delta<0 and gates()&0xFFFF0000:admitted=False
  if admitted:
   write(STATS+0x4C,2,value)
   if delta>0:sec(delta)
 sec(-sx(get(0x28,2),16)*tieramount);call(GET,[]);call(SET,[93])
 observed=[];visited=[];gi=0
 widths={ENTRY:3,COST:2,TIER:2,MOD:2,CHANNEL:1,RESOLVE:1,MP:3,SEC:3,REC:2,NOOP:2,**stubs}
 def hook(uc,a,n,d):
  nonlocal gi
  visited.append(a)
  if a not in widths:return
  regs=[UC_X86_REG_RCX,UC_X86_REG_EDX,UC_X86_REG_R8D]
  if a==ENTRY:regs[1]=UC_X86_REG_RDX
  if a in (RESOLVE,SET):regs[0]=UC_X86_REG_ECX
  observed.append(['call',a,[uc.reg_read(r) for r in regs[:widths[a]]]])
  if a not in stubs:return
  ret=100 if a==GET else 0
  if a==GLOBAL:ret=gm[gi] if gi<len(gm) else 0;gi+=1
  for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
  uc.reg_write(UC_X86_REG_RAX,ret)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:observed.append(['write',a,n,v&((1<<(8*n))-1)]),begin=0,end=0x5FFFFFFF)
 saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_RCX,UNIT),(UC_X86_REG_RDX,row),(UC_X86_REG_R8D,flag&0xFFFFFFFF),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
 u.emu_start(ENTRY,STOP,count=5000)
 assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
 assert all(u.reg_read(r)==v for r,v in saved.items())
 actual={a:bytes(u.mem_read(a,len(b))) for a,b in before.items()}
 final={hex(off):int.from_bytes(u.mem_read(STATS+off,n),'little') for off,n in [(6,2),(0x4C,2),(0x4E,1)]}
 return dict(name=name,fixture=dict(action=action,category=category,cost=cost,kind=kind,effects=effects,percent=percent,flag=flag,live=live,secondary=secondary,cap=cap,mult=mult,tier=tier,gm=gm),mp_cost=amount,tier_cost=tieramount,events=observed,expected_events=events,visited=visited,final=final,fixture_pages_match=all(actual[a]==b for a,b in expected_pages.items()),matches=observed==events and all(actual[a]==b for a,b in expected_pages.items()))
cases=[run('base'),run('half',effects=((0x6C,16),)),run('reduce10',effects=((0x73,8),)),run('free',effects=((0x6E,8),)),run('gil-channel',effects=((0x6C,1),)),run('kind1-channel',kind=1,effects=((0x6C,1),)),run('tier-category5',category=5,cost=2),run('tier-category6',category=6,cost=1),run('range-bypass',action=0xD0,effects=((0x6E,8),)),run('negative-cost-gain',effects=((0x73,56),(0x6C,16)),percent=(80,80,80)),run('capacity-zero',effects=((0x7C,128),)),run('late-gate-reject',gm=(0,0x10000,0)),run('flag1-still-late-reject',flag=1,gm=(0x10000,)),run('initial-reject',gm=(1,0)),run('flag1-bypass-low',flag=1,gm=(1,))]
assert all(c['matches'] for c in cases),[(c['name'],c['events'],c['expected_events'],c['final']) for c in cases if not c['matches']]
mutant=run('mutant-cost-not-negated',mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for a,b in {**BODIES,**CONSTANTS}.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for a,b in BODIES.items() for i in cs.disasm(b,a))+'\n')
print(f'PASS: {len(cases)} native cost/consume/write composition controls; negation mutant detected')
