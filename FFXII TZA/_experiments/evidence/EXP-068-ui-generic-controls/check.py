"""Original generic UI scheduler with controlled registration and cookie boundaries."""
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








ENTRY,EMIT,SCHEDULE,FINAL,COOKIE=0x280A00,0x252B40,0x244F50,0x28E860,0x808C40
ROOTPTR,COOKIEPTR,ROOT,STACK,STOP=0x209AC30,0x1F44830,0x50000000,0x60001800,0x70000000
PAYLOAD,DESC=STACK-0x38,STACK-0x28
COOKIEVALUE=0x123456789ABC
CODE=extract(ENTRY,193)
def run(name,request=2,param=0x12345678,flag=0x87654321,busy0=0,busy1=0,root=True,ret=0,change=False,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 stubs={EMIT,SCHEDULE,FINAL,COOKIE}
 for a in sorted({v&~4095 for v in [ENTRY,*stubs,ROOTPTR,COOKIEPTR,ROOT,STOP]}):u.mem_map(a,4096)
 u.mem_map(0x60000000,0x3000);u.mem_write(0x60000000,b'\xa5'*0x3000);u.mem_write(ENTRY,CODE)
 for a in stubs:u.mem_write(a,b'\xc3')
 if mutant:
  assert bytes(u.mem_read(0x280A4F,3))==bytes.fromhex('4863c1');u.mem_write(0x280A4F,bytes.fromhex('8bc190'))
 def put(a,n,v):u.mem_write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
 put(ROOTPTR,8,ROOT if root else 0);put(COOKIEPTR,8,COOKIEVALUE);put(ROOT+0xC0,8,busy0);put(ROOT+0xB8,8,busy1);put(STACK,8,STOP)
 before={a:bytes(u.mem_read(a,4096)) for a in [ROOT,ROOTPTR&~4095,COOKIEPTR&~4095]}
 request&=0xFFFFFFFF;param&=0xFFFFFFFF;flag&=0xFFFFFFFF
 token=request if request<0x80000000 else request|0xFFFFFFFF00000000
 expected=[];planned=[];payload=[request,param,flag,0];tag=token
 def packet():return dict(descriptor=DESC,head=0,padding='a5a5a5a5',payload_pointer=PAYLOAD,token=tag,payload=payload.copy())
 if root:
  if not(busy0 or busy1):
   expected.append([EMIT,[request,1]])
   expected.append([SCHEDULE,[0xD8,0x27FB70],packet()])
   if change:planned=[[PAYLOAD,4,0x55],[DESC+16,8,0xFFFFFFFFFFFFFF9D],[ROOT+0xC0,8,1]];payload[0]=0x55;tag=0xFFFFFFFFFFFFFF9D
   expected.append([SCHEDULE,[0xD8,0x280140],packet()]);expected.append([FINAL,[]])
  expected.append([COOKIE,[COOKIEVALUE]])
 events=[];writes=[];interventions=[];reads=[];visited=[];invalid=[];schedule_count=0
 def hook(uc,a,n,d):
  nonlocal schedule_count
  visited.append(a)
  if a not in stubs:return
  if a==EMIT:events.append([a,[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX)]])
  elif a==SCHEDULE:
   p=uc.reg_read(UC_X86_REG_R8);d=bytes(uc.mem_read(p,24));pp=int.from_bytes(d[8:16],'little')
   pk=dict(descriptor=p,head=int.from_bytes(d[:4],'little'),padding=d[4:8].hex(),payload_pointer=pp,token=int.from_bytes(d[16:24],'little'),payload=list(struct.unpack('<4I',uc.mem_read(pp,16))))
   events.append([a,[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_RDX)],pk]);schedule_count+=1
   if change and schedule_count==1:
    for addr,n,v in planned:put(addr,n,v);interventions.append([addr,n,v])
  elif a==COOKIE:events.append([a,[uc.reg_read(UC_X86_REG_RCX)]]);return
  else:events.append([a,[]])
  for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
  uc.reg_write(UC_X86_REG_EAX,ret&0xFFFFFFFF)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
 u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
 def bad(uc,t,a,n,v,d):invalid.append([t,a,n]);return False
 u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
 saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_ECX,request),(UC_X86_REG_EDX,param),(UC_X86_REG_R8D,flag),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
 error=None
 try:u.emu_start(ENTRY,STOP,count=1000)
 except unicorn.UcError as ex:error=str(ex)
 eax=u.reg_read(UC_X86_REG_EAX)
 if root:
  assert error is None and u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
  assert all(u.reg_read(r)==v for r,v in saved.items());match=not invalid and eax==int(not(busy0 or busy1))
 else:match=invalid==[[19,0xC0,8]] and error is not None
 ep={a:bytearray(b) for a,b in before.items()}
 for a,n,v in planned:
  if a<0x60000000:ep[ROOT][a-ROOT:a-ROOT+n]=v.to_bytes(n,'little')
 same=all(bytes(u.mem_read(a,len(b)))==b for a,b in ep.items())
 return dict(name=name,request=request,parameter=param,flag=flag,busy_c0=busy0,busy_b8=busy1,root=root,stub_return=ret,change=change,eax=eax,events=events,expected_events=expected,writes=writes,interventions=interventions,expected_interventions=planned,reads=reads,visited=visited,invalid=invalid,error=error,stop=u.reg_read(UC_X86_REG_RIP),fixture_pages_match=same,matches=bool(match and events==expected and not writes and interventions==planned and same))
cases=[run('base'),run('zero-id',request=0),run('out-of-router-range',request=25),run('high-flag-id',request=0x8002),run('negative-id',request=-1),run('signed-min-id',request=0x80000000),run('all-zero-params',param=0,flag=0),run('full-params',param=-1,flag=-1),run('busy-c0',busy0=1),run('busy-b8',busy1=1),run('busy-both',busy0=1,busy1=1),run('busy-upper-qword',busy0=0x100000000),run('callback-return-ignored',ret=0xFFFFFFFF),run('shared-packet-and-late-busy',change=True),run('null-root',root=False)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-zero-extends-token',request=-1,mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'00280A00.bin').write_bytes(CODE)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for i in cs.disasm(CODE,ENTRY))+'\n')
print(f'PASS: {len(cases)} original generic scheduler controls; signed-token mutant detected')
