import hashlib, importlib.util, json, struct, sys
from pathlib import Path
import capstone, unicorn
from unicorn import UcError
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent
ROOT=Path.cwd()
sha=lambda b:hashlib.sha256(b).hexdigest()
reader=ROOT/'Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py'
sp=importlib.util.spec_from_file_location('verified_existing_image_reader',reader)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image()
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
bodies=[]
for a,n in [(0x22BFF0,0x8DC),(0x22C970,0x215)]:
 b=m.img_rd(raw,secs,a,n);ins=list(cs.disasm(b,a));assert sum(i.size for i in ins)==n
 assert ins[-1].mnemonic=='ret'
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
insmap={int(i['pc'],16):i for body in bodies for i in body['instructions']}
def rip_operand(pc):
 i=next(cs.disasm(m.img_rd(raw,secs,pc,15),pc));return i.address+i.size+i.operands[-1].mem.disp
WL=rip_operand(0x22BFF8);CL=rip_operand(0x22C001)
assert WL==0x2088E3C and CL==0x2088E40
TOPS=rip_operand(0x22C06F)
RET=0x62000000;STACK=0x61000808;DST=0x50000100;SRC=0x1002000100
nonvols={UC_X86_REG_RBX:0x1122334455667788,UC_X86_REG_RBP:0x1020304050607080,
 UC_X86_REG_RSI:0x2122232425262728,UC_X86_REG_RDI:0x3132333435363738,
 UC_X86_REG_R12:0x4142434445464748,UC_X86_REG_R13:0x5152535455565758,
 UC_X86_REG_R14:0x6162636465666768,UC_X86_REG_R15:0x7172737475767778}
def run_case(name,fmt,cycle,decoder=False,guard=False):
 uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);gm=m.GuestMem(uc)
 pages=set()
 def page(a):
  p=a&~0xFFF
  if p not in pages:gm.map(p,0x1000);pages.add(p)
 for body in bodies:
  a=int(body['entry'],16);n=body['size']
  for p in range(a&~0xFFF,(a+n+0xFFF)&~0xFFF,0x1000):page(p)
  uc.mem_write(a,bytes.fromhex(body['raw_hex']))
  assert bytes(uc.mem_read(a,n)).hex()==body['raw_hex']
 for a in [WL,CL,TOPS,0x2088E44,0x2088E50,DST,STACK,RET]:page(a)
 for r,v in nonvols.items():uc.reg_write(r,v)
 gm.w(WL,struct.pack('<I',cycle));gm.w(CL,struct.pack('<I',cycle));gm.w(TOPS,b'\0\0')
 gm.w(STACK,struct.pack('<Q',RET));gm.w(DST-16,b'\xA5'*128)
 payload=struct.pack('<24I',*[0x10203040+i*0x01010101 for i in range(24)])
 if fmt=='V4_5':payload=struct.pack('<48H',*[((i+1)&31)|(((i+3)&31)<<5)|(((i+5)&31)<<10)|((i&1)<<15) for i in range(48)])
 vn,vl={'V2-32':(1,0),'V4_5':(3,3),'V4-32':(3,0)}[fmt]
 src=(0x1002001000-8) if guard else SRC
 page(src)
 if decoder:
  packet=struct.pack('<II',0x01000000|(cycle<<8)|cycle,(0x60|(vn<<2)|vl)<<24|3<<16)+payload[:6]+b'\xCC\xDD'+struct.pack('<I',0x01000505)
  source=packet+payload[20:]
 else:source=payload[:8] if guard else payload
 gm.w(src,source)
 before={'destination':gm.r(DST-16,128).hex(),'source':source.hex(),'globals':gm.r(WL,12).hex()}
 uc.reg_write(UC_X86_REG_RSP,STACK);uc.reg_write(UC_X86_REG_RCX,DST)
 if decoder:
  uc.reg_write(UC_X86_REG_RDX,src);uc.reg_write(UC_X86_REG_R8,len(packet));uc.reg_write(UC_X86_REG_R9,0)
  gm.w(STACK+0x28,struct.pack('<QQ',0,0));entry=0x22C970
 else:
  uc.reg_write(UC_X86_REG_RDX,vn);uc.reg_write(UC_X86_REG_R8,vl);uc.reg_write(UC_X86_REG_R9,0)
  gm.w(STACK+0x28,struct.pack('<QQQQ',0,3,0,src));entry=0x22BFF0
 events=[];steps=[];calls=[];faults=[]
 def code(u,a,n,x):
  steps.append(hex(a));i=insmap.get(a)
  if not i:raise AssertionError('executed outside verified bodies '+hex(a))
  if i['op']=='call':calls.append(i)
 def memory(u,access,a,n,v,x):
  # Entire supplied source window plus destination and globals; stack ignored but protected registers checked.
  kind='write' if access==unicorn.UC_MEM_WRITE else 'read'
  if src<=a<src+len(source)+32 or DST-16<=a<DST+112 or WL<=a<WL+12:
   try:value_hex=(v&((1<<(n*8))-1)).to_bytes(n,'little').hex() if kind=='write' else gm.r(a,n).hex()
   except KeyError:value_hex=None
   events.append({'kind':kind,'pc':hex(u.reg_read(UC_X86_REG_RIP)),'address':hex(a),'size':n,'value_hex':value_hex})
 def invalid(u,access,a,n,v,x):
  faults.append({'access':access,'pc':hex(u.reg_read(UC_X86_REG_RIP)),'address':hex(a),'size':n});return False
 uc.hook_add(unicorn.UC_HOOK_CODE,code)
 uc.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
 uc.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,invalid)
 failure=None
 try:uc.emu_start(entry,RET,timeout=2_000_000,count=5000)
 except UcError as e:failure=str(e)
 end=uc.reg_read(UC_X86_REG_RIP);returned=end==RET
 if returned:
  assert uc.reg_read(UC_X86_REG_RSP)==STACK+8
  assert all(uc.reg_read(r)==v for r,v in nonvols.items())
 assert 0<len(steps)<5000
 return {'name':name,'format':fmt,'cycle':cycle,'decoder':decoder,'guard':guard,
 'entry':hex(entry),'entry_rsp':hex(STACK),'source_address':hex(src),'destination_address':hex(DST),
 'supplied_num':3,'supplied_unsigned':0,'supplied_add_tops':0,'supplied_addr':0,
 'packet_nominal_bytes':len(packet) if decoder else None,'nominal_payload_bytes':8 if fmt=='V4_5' else (24 if fmt=='V2-32' else 48),
 'before':before,'after':{'destination':gm.r(DST-16,128).hex(),'source':gm.r(src,len(source)).hex(),'globals':gm.r(WL,12).hex()},
 'events':events,'calls':calls,'steps':steps,'instruction_count':len(steps),'returned':returned,
 'return_eax':uc.reg_read(UC_X86_REG_RAX)&0xFFFFFFFF,'final_rsp':hex(uc.reg_read(UC_X86_REG_RSP)),
 'final_rip':hex(end),'nonvolatile_preserved':all(uc.reg_read(r)==v for r,v in nonvols.items()) if returned else None,
 'failure':failure,'faults':faults,'stubs':[]}
results=[]
# Small feasibility/observer control first; retain it rather than rerunning it in the batch.
for fmt in ['V2-32','V4_5','V4-32']:
 for cycle in [1,2,3]:
  r=run_case(fmt+'-CL'+str(cycle),fmt,cycle);results.append(r)
  (HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
  assert r['returned'] and not r['failure'] and not r['faults'] and not r['calls']
  print(r['name'],'return',r['return_eax'],'instructions',r['instruction_count'],flush=True)
for name,cycle,decoder,guard in [('V4_5-decoder-CL2',2,True,False),('V4_5-guard-CL1',1,False,True),('V4_5-guard-CL2',2,False,True)]:
 r=run_case(name,'V4_5',cycle,decoder,guard);results.append(r)
 (HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(r['name'],'returned',r['returned'],'failure',r['failure'],'return',r['return_eax'],flush=True)
refs=['Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md',
 'Database/FFXII TZA/_index/candidates/uq215-unpack-strides/unpack_strides.py']
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 b=Path(p).read_bytes();name=f'{i:02d}-'+Path(p).name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p,'retained':'retained/'+name,'sha256':sha(b),'bytes':len(b)})
(HERE/'source.json').write_text(json.dumps({'method':'B isolated complete original code, controlled memory; no native/live process',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_path':reader.as_posix(),'reader_sha256':sha(reader.read_bytes()),
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),'unicorn_version':unicorn.__version__,'capstone_version':capstone.__version__,
 'bodies':bodies,'globals':{'write_length':hex(WL),'cycle_length':hex(CL),'tops':hex(TOPS)},'consumer_preimages':pins,
 'limits':'NUM3; WL=CL1/2/3, unsigned0/addTOPS0/ADDR0. Supplied state. No data-borne reachability, real initialization, drawing, scheduler or native effects.'},indent=2)+'\n')
print('12 bounded cases retained; deliberate guard fault is a separate controlled guest observation, not a game crash.',flush=True)
