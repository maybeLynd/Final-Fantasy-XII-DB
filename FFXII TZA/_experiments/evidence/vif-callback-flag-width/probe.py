import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('verified_image_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
prior=Path('Database/FFXII TZA/_experiments/evidence/vif-admission-progress/primary.json');ps=json.loads(prior.read_text())
decoder=next(b for b in ps['bodies'] if int(b['entry'],16)==0x22C970)
assert decoder['size']==533 and m.img_rd(raw,secs,0x22C970,533).hex()==decoder['raw_hex']
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+136)
ed=m.img_rd(raw,secs,m.IMG_LO+er,es);rf=[struct.unpack_from('<III',ed,i) for i in range(0,len(ed),12)]
bodies=[]
for a,n,extent in [(0x1DB550,172,'PE RuntimeFunction1DB550..1DB5FC, unwind1DE0B0C'),
 (0x22C940,43,'Complete straight-line wrapper through sole RET, fiveCC padding bytes follow'),
 (0x22C970,533,'Previously qualified complete chained decoder extent; exact original bytes reverified'),
 (0x22C930,11,'Complete two-instruction reset leaf through RET'),
 (0x1DB640,21,'No PE entry at1DB640; straight-line adapter through terminal JMP, elevenCC padding bytes follow'),
 (0x20F310,197,'PE RuntimeFunction20F310..20F3D5'),(0x1DB660,358,'PE RuntimeFunction1DB660..1DB7C6')]:
 b=m.img_rd(raw,secs,a,n);ii=list(cs.disasm(b,a));assert sum(i.size for i in ii)==n
 assert ii[-1].mnemonic==('jmp' if a==0x1DB640 else 'ret')
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),'extent':extent,
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]})
assert (0x1DB550-m.IMG_LO,0x1DB5FC-m.IMG_LO,0x1DE0B0C-m.IMG_LO) in rf
assert not any(r[0]+m.IMG_LO==0x1DB640 for r in rf)
assert m.img_rd(raw,secs,0x1DB655,11)==b'\xcc'*11 and m.img_rd(raw,secs,0x22C96B,5)==b'\xcc'*5
insmap={int(i['pc'],16):i for b in bodies for i in b['instructions']}
HEAP=0x50000000;OBJ=HEAP+0x100;DESC=HEAP+0x1000;PACKET=HEAP+0x2000;COPY=HEAP+0x3000
POINTERS=HEAP+0x4000;FLAGS=HEAP+0x5000;SP=0x61008808;RET=0x62000000;SLOT=SP-0x18
nonvols={UC_X86_REG_RBX:0x1122334455667788,UC_X86_REG_RBP:0x1020304050607080,
 UC_X86_REG_RSI:0x2122232425262728,UC_X86_REG_RDI:0x3132333435363738,
 UC_X86_REG_R12:0x4142434445464748,UC_X86_REG_R13:0x5152535455565758,
 UC_X86_REG_R14:0x6162636465666768,UC_X86_REG_R15:0x7172737475767778}
STUBS={0x1A1470:'packet allocator: return disposable COPY, record request; native allocator not executed',
 0x861EBA:'memcpy: copy requested bytes in guest and return destination; native CRT not executed',
 0x16D6A0:'registration: record pointer and return0; native ownership effects not executed'}
def run(name,seed,command):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);gm=m.GuestMem(u);pages=set()
 def page(a):
  p=a&~0xFFF
  if p not in pages:gm.map(p,0x1000);pages.add(p)
 for b in bodies:
  a=int(b['entry'],16);n=b['size']
  for p in range(a&~0xFFF,(a+n+0xFFF)&~0xFFF,0x1000):page(p)
  u.mem_write(a,bytes.fromhex(b['raw_hex']))
 for a in [*STUBS,0x2EC3ED0,0x2088E44,0x2088E50,0x2064E30,0x1E027C0,0x1F82D00,0x1F7F400,SP,SP-0x1000,RET]:page(a)
 # Caller/helper/collector RIP-relative global reads are mapped, their external manager values stay supplied zero.
 for i in insmap.values():
  if '[rip + 0x' in i['args']:
   disp=int(i['args'].split('[rip + 0x')[1].split(']')[0],16);page(int(i['pc'],16)+len(bytes.fromhex(i['bytes']))+disp)
 for p in range(HEAP,HEAP+0x6000,0x1000):page(p)
 w=lambda a,v,n:gm.w(a,v.to_bytes(n,'little'))
 r=lambda a,n:int.from_bytes(gm.r(a,n),'little')
 for reg,v in nonvols.items():u.reg_write(reg,v)
 w(SP,RET,8);w(SLOT,seed,4);w(OBJ+0x18,1,4);w(OBJ+0x1C,1,4);w(OBJ+0x20,DESC,8)
 w(DESC,PACKET,8);w(DESC+8,20,4)
 packet=struct.pack('<I',command<<24|1)+struct.pack('<QQ',0x8000,0)
 gm.w(PACKET,packet);gm.w(COPY,b'\xA5'*32)
 w(OBJ+0x220,4,4);w(OBJ+0x224,7,4);w(OBJ+0x228,POINTERS,8)
 w(OBJ+0x428,4,4);w(OBJ+0x42C,7,4);w(OBJ+0x430,FLAGS,8);gm.w(FLAGS,b'\xA5'*4)
 w(0x1E027C0,1,1);w(0x2088E44,9,4)
 u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_RCX,OBJ)
 before={'slot_dword':r(SLOT,4),'packet_hex':gm.r(PACKET,20).hex(),'flags_hex':gm.r(FLAGS,4).hex(),
  'copy_hex':gm.r(COPY,32).hex(),'initial_object_counts':[r(OBJ+0x224,4),r(OBJ+0x42C,4)],'gate':r(0x1E027C0,1)}
 steps=[];trace=[];events=[];stubs=[];faults=[]
 watched={0x1DB5B9,0x1DB5BE,0x22C944,0x22C948,0x22C9BB,0x22C9C3,0x22CB27,0x22CB30,
  0x1DB640,0x1DB643,0x1DB64C,0x1DB650,0x1DB67D,0x1DB729}
 def reg(k):return u.reg_read(k)
 def ret(value):
  stack=reg(UC_X86_REG_RSP);dest=r(stack,8);u.reg_write(UC_X86_REG_RAX,value)
  u.reg_write(UC_X86_REG_RSP,stack+8);u.reg_write(UC_X86_REG_RIP,dest)
 def code(uc,a,n,x):
  steps.append(hex(a))
  if a in STUBS:
   rcx,rdx,r8=reg(UC_X86_REG_RCX),reg(UC_X86_REG_RDX),reg(UC_X86_REG_R8)
   stubs.append({'pc':hex(a),'description':STUBS[a],'rcx':hex(rcx),'rdx':hex(rdx),'r8':hex(r8)})
   if a==0x1A1470:assert rdx==16;ret(COPY)
   elif a==0x861EBA:assert (rcx,rdx,r8)==(COPY,PACKET+4,16);gm.w(rcx,gm.r(rdx,r8));ret(rcx)
   else:assert rdx==COPY;ret(0)
   return
  assert a in insmap,'Unknown original execution '+hex(a)
  if a in watched:trace.append({'pc':hex(a),'instruction':insmap[a],
   'rsp':hex(reg(UC_X86_REG_RSP)),'rax':hex(reg(UC_X86_REG_RAX)),'rcx':hex(reg(UC_X86_REG_RCX)),
   'rdx':hex(reg(UC_X86_REG_RDX)),'r8':hex(reg(UC_X86_REG_R8)),'r13':hex(reg(UC_X86_REG_R13)),
   'r14':hex(reg(UC_X86_REG_R14)),'slot_dword':r(SLOT,4),'flag_byte':r(FLAGS,1)})
 def memory(uc,access,a,n,v,x):
  if a<=SLOT<a+n or SLOT<=a<SLOT+4 or FLAGS<=a<FLAGS+4:
   events.append({'kind':'write' if access==unicorn.UC_MEM_WRITE else 'read','pc':hex(reg(UC_X86_REG_RIP)),
    'address':hex(a),'size':n,'value_hex':(v&((1<<(n*8))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else gm.r(a,n).hex()})
 def bad(uc,access,a,n,v,x):faults.append({'access':access,'pc':hex(reg(UC_X86_REG_RIP)),'address':hex(a),'size':n});return False
 u.hook_add(unicorn.UC_HOOK_CODE,code);u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
 u.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,bad);failure=None
 try:u.emu_start(0x1DB550,RET,timeout=2_000_000,count=5000)
 except (unicorn.UcError,AssertionError) as e:failure=type(e).__name__+': '+str(e)
 unchanged=all(gm.r(int(b['entry'],16),b['size']).hex()==b['raw_hex'] for b in bodies)
 after={'slot_dword':r(SLOT,4),'packet_hex':gm.r(PACKET,20).hex(),'flags_hex':gm.r(FLAGS,4).hex(),
  'copy_hex':gm.r(COPY,32).hex(),'object_counts':[r(OBJ+0x224,4),r(OBJ+0x42C,4)],
  'stored_copy_pointer':hex(r(POINTERS,8)),'reset_installed_count':r(0x2088E44,4)}
 result={'name':name,'seed_dword':seed,'command':hex(command),'entry':hex(0x1DB550),'entry_rsp':hex(SP),'flag_slot':hex(SLOT),
  'before':before,'after':after,'trace':trace,'watched_memory_events':events,'steps':steps,'stub_calls':stubs,
  'instruction_count':len(steps),'returned':reg(UC_X86_REG_RIP)==RET,'final_rsp':hex(reg(UC_X86_REG_RSP)),
  'nonvolatile_preserved':all(reg(k)==v for k,v in nonvols.items()),'original_code_unchanged':unchanged,
  'failure':failure,'faults':faults,'limits':'Controlled guest stack/object/packet; three disclosed native-effect stubs. Not normal gameplay or live initialization.'}
 return result

retained=HERE/'retained';retained.mkdir(exist_ok=True);refs=[]
for p in [prior,Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md')]:
 b=p.read_bytes();name=p.name;(retained/name).write_bytes(b);refs.append({'path':p.as_posix(),'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
(retained/'image-reader.py').write_bytes(rb)
(HERE/'source.json').write_text(json.dumps({'method':'B isolated verified original composition','exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),
 'reader_sha256':sha(rb),'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'capstone_version':capstone.__version__,'unicorn_version':unicorn.__version__,'bodies':bodies,
 'exception_directory':{'rva':hex(er),'bytes':es,'sha256':sha(ed)},'refs':refs,'stubs':{hex(a):v for a,v in STUBS.items()},
 'fixture':{'object':hex(OBJ),'chunk_descriptor':hex(DESC),'packet':hex(PACKET),'copy':hex(COPY),
  'pointer_array':hex(POINTERS),'flag_array':hex(FLAGS),'flag_slot':hex(SLOT),'stack':hex(SP),'return':hex(RET)},
 'limits':'Seven original bodies execute from caller entry with controlled memory and three native-effect stubs. No FF12/native process, actual stack contents, scheduling, allocator/lifetime or visual effect established.'},indent=2)+'\n')
results=[]
for name,seed,command in [('DIRECT-clean-control',0,0x50),('DIRECT-upper-byte',0x100,0x50),
 ('DIRECT-low-byte-overwritten',1,0x50),('DIRECT-high-bit',0x80000000,0x50),
 ('DIRECTHL-clean-control',0,0x51),('DIRECTHL-upper-byte',0x100,0x51)]:
 try:result=run(name,seed,command)
 except BaseException as e:
  (HERE/'failure.json').write_text(json.dumps({'case':name,'error':repr(e),'accepted':False},indent=2)+'\n');raise
 results.append(result);(HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
 assert result['returned'] and int(result['final_rsp'],16)==SP+8 and result['nonvolatile_preserved'] and result['original_code_unchanged']
 assert not result['failure'] and not result['faults'] and 0<result['instruction_count']<5000
 assert result['after']['packet_hex']==result['before']['packet_hex']
 # Baseline/control must actually observe the original width chain and collector result before proceeding.
 assert [x['pc'] for x in result['stub_calls']]==['0x1a1470','0x861eba','0x16d6a0']
 assert result['after']['object_counts']==[1,1]
 if name=='DIRECT-clean-control':assert result['after']['flags_hex']=='00a5a5a5'
 print(name,'slot',hex(result['after']['slot_dword']),'flag',result['after']['flags_hex'][:2],'instructions',result['instruction_count'],flush=True)
