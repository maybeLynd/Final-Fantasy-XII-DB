import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
sp=importlib.util.spec_from_file_location('verified_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
pe=struct.unpack_from('<I',raw,0x3C)[0];er,es=struct.unpack_from('<II',raw,pe+24+112+24)
pdata=m.img_rd(raw,secs,m.IMG_LO+er,es)
rfs=[tuple(v+m.IMG_LO for v in struct.unpack_from('<III',pdata,i)) for i in range(0,len(pdata),12)]
bodies=[];instructions={}
for a,n in [(0x210230,227),(0x20EA50,266),(0x202B70,31),(0x217060,235)]:
 b=m.img_rd(raw,secs,a,n);ii=list(cs.disasm(b,a));assert sum(i.size for i in ii)==n
 rf=next(r for r in rfs if r[0]==a);assert rf[1]==a+n
 rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),'pe_function':[hex(v) for v in rf],'instructions':rows})
 instructions.update({i.address:i for i in ii})
def rip(pc):
 i=instructions[pc];ops=[o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP]
 assert len(ops)==1
 return i.address+i.size+ops[0].mem.disp
sites={'format':0x210236,'upper':0x21026C,'lower':0x2102C5,'scale':0x210285,'matrix':0x20EA6B,
 'colour0':0x20EA87,'colour1':0x20EA92,'colour2':0x20EAA0,'colour3':0x20EAAE,
 'uv_select':0x20EB11,'uv_false0':0x20EB42,'uv_false1':0x20EB3A,
 'uv_true0':0x20EB22,'uv_true1':0x20EB1A,'required':0x2102F5,'phase':0x2102FB}
bindings={k:rip(v) for k,v in sites.items()}
assert bindings['format']==0x1FD3611 and bindings['matrix']==0x1FD3620
assert bindings['scale']==0x8F30EC==rip(0x2102A7)
scale=m.img_rd(raw,secs,bindings['scale'],4);assert scale==struct.pack('<f',0.0625)
assert {i.operands[0].imm for i in instructions.values() if i.mnemonic=='call'}=={0x20EA50,0x202B70,0x217060}
SP=0x61000808;RET=0x62000000;SRC=0x50000100;DST=0x50000200
ident=[1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.]
transform=[2.,0.,0.,0.,0.,3.,0.,0.,0.,0.,4.,0.,10.,20.,30.,2.]
cancel=[16777216.,0.,0.,0.,-16777216.,1.,0.,0.,1.,0.,1.,0.,0.5,0.,0.,1.]
packed=lambda x,y,z:struct.pack('<QQ',x|(y<<32),z<<4)
floats=lambda x,y,z:struct.pack('<ffff',x,y,z,0.)
cases=[('packed-identity-control',0,packed(16,32,64),0.,1000.,ident,0),
 ('same-float-bytes-as-packed',0,floats(1,2,3),0.,1000.,ident,0),
 ('same-float-bytes-direct',1,floats(1,2,3),0.,1000.,ident,0),
 ('packed-upper-bound',0,packed(16,32,2000),10.,1000.,ident,0),
 ('packed-lower-bound',0,packed(16,32,0),10.,1000.,ident,0),
 ('direct-outside-packed-bound',1,floats(1,2,2000),10.,1000.,ident,0),
 ('matrix-and-homogeneous-divide',1,floats(1,2,3),0.,1000.,transform,1),
 ('single-precision-order',1,floats(1,1,1),0.,1000.,cancel,0)]
nonvolatile={'rbx':UC_X86_REG_RBX,'rbp':UC_X86_REG_RBP,'rsi':UC_X86_REG_RSI,'rdi':UC_X86_REG_RDI,
 'r12':UC_X86_REG_R12,'r13':UC_X86_REG_R13,'r14':UC_X86_REG_R14,'r15':UC_X86_REG_R15}
nonvolatile.update({'xmm'+str(i):globals()['UC_X86_REG_XMM'+str(i)] for i in range(6,16)})
seed={k:(0x1122334455660000+i if k[0]=='r' else 0x112233445566778899AABBCCDDEE0000+i) for i,k in enumerate(nonvolatile)}
retained=HERE/'retained';retained.mkdir(exist_ok=True)
page=Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md');pb=page.read_bytes()
(retained/page.name).write_bytes(pb);(retained/'image-reader.py').write_bytes(reader.read_bytes())
source={'method':'B complete isolated original-code composition, no effect stubs','exe_path':m.EXE,
 'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(reader.read_bytes()),
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'unicorn_version':unicorn.__version__,'capstone_version':capstone.__version__,'bodies':bodies,
 'bindings':{k:{'site':hex(sites[k]),'address':hex(v)} for k,v in bindings.items()},
 'shipping_scale_hex':scale.hex(),'fixture':{'stack':hex(SP),'return':hex(RET),'source':hex(SRC),'destination':hex(DST),
 'mxcsr':hex(0x1F80),'nonvolatile_seeds':{k:hex(v) for k,v in seed.items()},'output_before_hex':('A5'*48).lower()},
 'consumer':{'path':page.as_posix(),'retained':'retained/'+page.name,'sha256':sha(pb),'bytes':len(pb)},
 'stubs':[],'pe_metadata_role':'Physical body-range cross-check only; not evidence of semantics, ownership, registration, ordinary reachability or live execution. Those observations use original instruction bytes/control flow and actual isolated traces.',
 'limits':'Complete four functions, supplied finite globals/input, nonalias output and normal ABI. No original process initialization/ownership/native renderer/ordinary caller/presentation or exhaustive floating-point domain proof.'}
(HERE/'source.json').write_text(json.dumps(source,indent=2)+'\n')
results=[]
for name,flag,inp,lower,upper,matrix,uv_select in cases:
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);gm=m.GuestMem(u);pages=set()
 def map_page(a):
  p=a&~0xFFF
  if p not in pages:gm.map(p,0x1000);pages.add(p)
 for b in bodies:
  a=int(b['entry'],16)
  for p in range(a&~0xFFF,(a+b['size']+0xFFF)&~0xFFF,0x1000):map_page(p)
  gm.w(a,bytes.fromhex(b['raw_hex']))
 for a in [SP,RET,SRC,DST,*bindings.values()]:map_page(a)
 fixtures={k:struct.pack('<f',v) for k,v in {'lower':lower,'upper':upper,
  'uv_false0':0.25,'uv_false1':0.5,'uv_true0':0.75,'uv_true1':1.}.items()}
 fixtures.update({'format':bytes([flag]),'scale':scale,'matrix':struct.pack('<16f',*matrix),
  'uv_select':bytes([uv_select]),'required':struct.pack('<I',3),'phase':struct.pack('<I',3)})
 fixtures.update({'colour'+str(i):bytes([v]) for i,v in enumerate([8,64,128,255])})
 for k,b in fixtures.items():gm.w(bindings[k],b)
 gm.w(SRC,inp);gm.w(DST,b'\xA5'*48);gm.w(SP,struct.pack('<Q',RET))
 u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_RCX,DST);u.reg_write(UC_X86_REG_RDX,SRC)
 u.reg_write(UC_X86_REG_MXCSR,0x1F80);u.reg_write(UC_X86_REG_EFLAGS,2)
 for k,v in seed.items():u.reg_write(nonvolatile[k],v)
 r={'name':name,'input_hex':inp.hex(),'coordinate_flag':flag,'lower':lower,'upper':upper,'matrix':matrix,
  'uv_select':uv_select,'starting_bindings':{k:gm.r(bindings[k],len(v)).hex() for k,v in fixtures.items()},
  'steps':[],'events':[],'boundaries':[],'faults':[],'failure':None}
 results.append(r)
 watch=[(SRC,16),(DST,48)]+[(bindings[k],len(v)) for k,v in fixtures.items()]
 def code(uc,a,n,x):
  if a==RET:uc.emu_stop();return
  assert a in instructions,'Unknown executed code '+hex(a)
  i=instructions[a];r['steps'].append({'pc':hex(a),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str,
   'rsp':hex(u.reg_read(UC_X86_REG_RSP)),'rcx':hex(u.reg_read(UC_X86_REG_RCX)),
   'rdx':hex(u.reg_read(UC_X86_REG_RDX)),'r8':hex(u.reg_read(UC_X86_REG_R8))})
  if a in (0x20EA50,0x202B70,0x217060,0x20EAD8):
   z={'pc':hex(a),'destination_hex':gm.r(DST,48).hex()}
   if a==0x20EA50:z['temporary_coordinate_hex']=gm.r(u.reg_read(UC_X86_REG_RDX),16).hex()
   r['boundaries'].append(z)
 def mem(uc,access,a,n,v,x):
  if any(a<start+size and a+n>start for start,size in watch):
   r['events'].append({'pc':hex(u.reg_read(UC_X86_REG_RIP)),'kind':'write' if access==unicorn.UC_MEM_WRITE else 'read',
    'address':hex(a),'size':n,'value_hex':(v&((1<<(8*n))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else gm.r(a,n).hex()})
 def bad(uc,access,a,n,v,x):r['faults'].append({'access':access,'pc':hex(u.reg_read(UC_X86_REG_RIP)),'address':hex(a),'size':n});return False
 handles=[u.hook_add(unicorn.UC_HOOK_CODE,code),u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,mem),u.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,bad)]
 try:u.emu_start(0x210230,RET,timeout=2_000_000,count=5000)
 except (unicorn.UcError,AssertionError) as e:r['failure']=type(e).__name__+': '+str(e)
 finally:
  for h in handles:u.hook_del(h)
 r.update(final_pc=hex(u.reg_read(UC_X86_REG_RIP)),final_rsp=hex(u.reg_read(UC_X86_REG_RSP)),
  return_rax=hex(u.reg_read(UC_X86_REG_RAX)),return_al=u.reg_read(UC_X86_REG_RAX)&255,
  final_mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),output_hex=gm.r(DST,48).hex(),
  output_first_ten_floats=list(struct.unpack('<10f',gm.r(DST,40))),input_unchanged=gm.r(SRC,16)==inp,
  bindings_unchanged=all(gm.r(bindings[k],len(v))==v for k,v in fixtures.items()),
  code_unchanged=all(gm.r(int(b['entry'],16),b['size']).hex()==b['raw_hex'] for b in bodies),
  final_nonvolatile={k:hex(u.reg_read(v)) for k,v in nonvolatile.items()},instruction_count=len(r['steps']))
 (HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
 assert r['final_pc']==hex(RET) and r['final_rsp']==hex(SP+8) and not r['faults'] and not r['failure'],r
 assert r['input_unchanged'] and r['bindings_unchanged'] and r['code_unchanged']
 assert r['final_nonvolatile']=={k:hex(v) for k,v in seed.items()}
 if name=='packed-identity-control':assert r['output_first_ten_floats'][:4]==[1.,2.,64.,1.];print('Feasibility/control retained: original full chain returns (1,2,64,1).',flush=True)
 print(name,r['output_first_ten_floats'][:4],r['instruction_count'],flush=True)
