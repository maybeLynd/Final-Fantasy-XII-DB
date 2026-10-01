"""Original UI router with original policy and switch tables; controlled callees."""
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







ENTRY,POLICY=0x254B50,0x2E0FA0
PRE=(0x17E7D0,0x35DA80,0x3C8990)
GENERIC,RESET=0x280A00,0x28F970
SPECIAL={1:0x35D660,4:0x35D660,3:0x35D980,5:0x3C87B0,12:0x28E970,24:0x35D080}
GATE,STACK,STOP=0x2092734,0x60001800,0x70000000
CODE=extract(ENTRY,263)
DATA={a:extract(a,n) for a,n in [(0x1E0C2C0,88),(0x254C58,24),(0x254C70,24)]}
# Independently transcribed policy and route oracle, not derived from the executed tables.
MASKS=[4,42,8,4,0,32,16384,0,2097154,16416,8]+[0]*11
assert list(struct.unpack('<22I',DATA[0x1E0C2C0]))==MASKS
assert [base+x for x in struct.unpack('<6I',DATA[0x254C58])]==[0x254BFB,0x254C04,0x254C0D,0x254C16,0x254C24,0x254C2D]
assert list(DATA[0x254C70])==[0,5,1,0,2,5,5,5,5,5,5,3,5,5,5,5,5,5,5,5,5,5,5,4]
def run(name,request=2,param=0x12345678,flag=0x87654321,policy=0,gate=0,ret=0x89ABCDEF,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 stubs={POLICY,*PRE,GENERIC,RESET,*SPECIAL.values()}
 for p in sorted({a&~4095 for a in [ENTRY,*DATA,GATE,STOP,*stubs]}):u.mem_map(p,4096)
 u.mem_map(0x60000000,0x3000);u.mem_write(ENTRY,CODE)
 for a,b in DATA.items():u.mem_write(a,b)
 for a in stubs:u.mem_write(a,b'\xc3')
 if mutant:
  assert bytes(u.mem_read(0x254C37,2))==bytes.fromhex('8bcd');u.mem_write(0x254C37,bytes.fromhex('8bcb'))
 u.mem_write(GATE,(gate&0xFFFFFFFF).to_bytes(4,'little'));u.mem_write(STACK,STOP.to_bytes(8,'little'))
 before={a:bytes(u.mem_read(a,4096)) for a in (GATE&~4095,0x1E0C000)}
 request&=0xFFFFFFFF;param&=0xFFFFFFFF;flag&=0xFFFFFFFF;policy&=0xFFFFFFFF
 rid=request&0x7FFF;mask=0
 for i,m in enumerate(MASKS):
  if policy&(1<<i):mask|=m
 expected=[];answer=0
 if gate!=1:
  expected.append([POLICY,[]])
  if not(mask&(1<<(rid&31))):
   expected += [[a,[]] for a in PRE]
   if rid in SPECIAL:expected.append([SPECIAL[rid],[rid]]);answer=1 if rid==12 else ret&0xFFFFFFFF
   else:expected.extend([[RESET,[]],[GENERIC,[request,param,flag]]]);answer=ret&0xFFFFFFFF
 events=[];writes=[];reads=[];visited=[]
 def hook(uc,a,n,d):
  visited.append(a)
  if a not in stubs:return
  if a==GENERIC:args=[uc.reg_read(r) for r in (UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_R8D)]
  elif a in SPECIAL.values():args=[uc.reg_read(UC_X86_REG_ECX)]
  else:args=[]
  events.append([a,args])
  for r in (UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11):uc.reg_write(r,0xBAD0BAD0)
  uc.reg_write(UC_X86_REG_EAX,policy if a==POLICY else ret&0xFFFFFFFF)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append([a,n,v]),begin=0,end=0x5FFFFFFF)
 u.hook_add(unicorn.UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append([a,n]),begin=0,end=0x5FFFFFFF)
 saved={r:0x12340000+i for i,r in enumerate((UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15))}
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_ECX,request),(UC_X86_REG_EDX,param),(UC_X86_REG_R8D,flag),(UC_X86_REG_RSP,STACK)]:u.reg_write(r,v)
 u.emu_start(ENTRY,STOP,count=1500)
 assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==STACK+8
 assert all(u.reg_read(r)==v for r,v in saved.items())
 eax=u.reg_read(UC_X86_REG_EAX);same=all(bytes(u.mem_read(a,len(b)))==b for a,b in before.items())
 return dict(name=name,request=request,parameter=param,flag=flag,policy=policy,gate=gate,stub_return=ret&0xFFFFFFFF,normalized=rid,inhibit_mask=mask,expected_return=answer,eax=eax,events=events,expected_events=expected,writes=writes,reads=reads,visited=visited,fixture_pages_match=same,matches=events==expected and eax==answer and not writes and same)
cases=[run(f'id-{i}',request=i) for i in range(1,25)]
cases += [run('id-zero',request=0),run('id25',request=25),run('id32',request=32),run('id-high',request=0xFFFFFFFF),run('special-high-flag',request=0x8001),run('generic-high-flag',request=0x8002),run('generic-upper-word',request=0x10002),run('gate-one',gate=1),run('gate-two',gate=2),run('special-return-zero',request=1,ret=0),run('request12-forces-one',request=12,ret=0),run('generic-return-zero',ret=0)]
for bit in range(32):
 mask=MASKS[bit] if bit<22 else 0
 request=(mask&-mask).bit_length()-1 if mask else 2
 cases.append(run(f'policy-bit{bit}',request=request,policy=1<<bit))
cases += [run('policy-positive-allow',request=3,policy=1),run('policy-bt-alias',request=34,policy=1),run('policy-union',request=14,policy=(1<<8)|(1<<9)),run('all-policy',request=24,policy=0xFFFFFFFF)]
assert all(c['matches'] for c in cases),[c for c in cases if not c['matches']]
mutant=run('mutant-normalizes-generic',request=0x8002,mutant=True);assert not mutant['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,mutant=mutant)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'00254B50.bin').write_bytes(CODE)
for a,b in DATA.items():(HERE/f'{a:08X}.bin').write_bytes(b)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for i in cs.disasm(CODE,ENTRY))+'\n')
print(f'PASS: {len(cases)} original UI router controls; generic-normalization mutant detected')
