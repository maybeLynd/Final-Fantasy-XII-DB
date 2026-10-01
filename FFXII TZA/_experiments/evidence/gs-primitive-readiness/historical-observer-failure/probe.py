import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('verified_image_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
bodies=[]
for a,n,scope in [(0x20FE70,150,'Complete PRIM setter throughRET, calls actual20FBA0 then resets phase/vertex count'),
 (0x20FBA0,247,'Complete multi-return leaf through20FC96, nineCC pad bytes follow; no PE entry at this leaf assumed'),
 (0x210230,227,'Complete converter through bothRET paths; only postwriter suffix2102E8 executed'),
 (0x20F6B5,33,'XYZ2 phase prefix; controlled interior entry, stopbefore capacity test20F6D6'),
 (0x20F70D,20,'AL consumer/reset; controlled interior entry, stopbefore indexdispatch20F721 or sharedcontinuation20FA6F'),
 (0x20F721,7,'Unexecuted positive boundary instruction'),(0x20FA6F,8,'Unexecuted negative boundary context')]:
 b=m.img_rd(raw,secs,a,n);ii=list(cs.disasm(b,a))
 if a!=0x20FA6F:assert sum(i.size for i in ii)==n
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),'scope':scope,
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]})
assert m.img_rd(raw,secs,0x20FC97,9)==b'\xcc'*9
insmap={int(i['pc'],16):i for b in bodies for i in b['instructions']}
SP=0x61000808;RET=0x62000000;SRC=0x50000100
FIELDS={'primitive':0x1F83560,'fan':0x1F83561,'vertex_count':0x1F83568,'carry':0x1F8356C,
 'required':0x1F83570,'phase':0x1F83574,'aux78':0x1F83578}
saved_rbx=0x1122334455667788
def new_guest():
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);gm=m.GuestMem(u);pages=set()
 def page(a):
  p=a&~0xFFF
  if p not in pages:gm.map(p,0x1000);pages.add(p)
 for b in bodies:
  a=int(b['entry'],16)
  for p in range(a&~0xFFF,(a+b['size']+0xFFF)&~0xFFF,0x1000):page(p)
  gm.w(a,bytes.fromhex(b['raw_hex']))
 for a in [SP,SP-0x1000,RET,SRC,*FIELDS.values()]:page(a)
 for b in bodies:
  for i in cs.disasm(bytes.fromhex(b['raw_hex']),int(b['entry'],16)):
   for op in i.operands:
    if op.type==capstone.CS_OP_MEM and op.mem.base==capstone.x86_const.X86_REG_RIP:page(i.address+i.size+op.mem.disp)
 return u,gm
def snapshot(gm):return {k:int.from_bytes(gm.r(a,1 if k in ('primitive','fan') else 4),'little') for k,a in FIELDS.items()}
def stage(u,gm,name,entry,stops):
 before=snapshot(gm);steps=[];events=[];faults=[];failure=None
 def code(uc,a,n,x):
  if a in stops:uc.emu_stop();return
  assert a in insmap,'Unknown code '+hex(a)
  if name=='gate':assert 0x2102E8<=a<0x210313,'Executed omitted converter body'
  steps.append({'pc':hex(a),'op':insmap[a],
   'rax':hex(u.reg_read(UC_X86_REG_RAX)),'rcx':hex(u.reg_read(UC_X86_REG_RCX)),
   'rsp':hex(u.reg_read(UC_X86_REG_RSP)),'rbx':hex(u.reg_read(UC_X86_REG_RBX))})
 def mem(uc,access,a,n,v,x):
  if FIELDS['primitive']<=a<FIELDS['primitive']+0x20 or SRC<=a<SRC+16:
   events.append({'pc':hex(u.reg_read(UC_X86_REG_RIP)),'kind':'write' if access==unicorn.UC_MEM_WRITE else 'read',
    'address':hex(a),'size':n,'value_hex':(v&((1<<(8*n))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else gm.r(a,n).hex()})
 def bad(uc,access,a,n,v,x):faults.append({'access':access,'pc':hex(u.reg_read(UC_X86_REG_RIP)),'address':hex(a),'size':n});return False
 handles=[u.hook_add(unicorn.UC_HOOK_CODE,code),u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,mem),u.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,bad)]
 try:u.emu_start(entry,RET,timeout=1_000_000,count=2000)
 except (unicorn.UcError,AssertionError) as e:failure=type(e).__name__+': '+str(e)
 finally:
  for h in handles:u.hook_del(h)
 final=u.reg_read(UC_X86_REG_RIP)
 return {'stage':name,'entry':hex(entry),'accepted_boundary':final in stops,'final_pc':hex(final),
  'before':before,'after':snapshot(gm),'steps':steps,'events':events,'instruction_count':len(steps),
  'rax':hex(u.reg_read(UC_X86_REG_RAX)),'al':u.reg_read(UC_X86_REG_RAX)&255,
  'final_rsp':hex(u.reg_read(UC_X86_REG_RSP)),'final_rbx':hex(u.reg_read(UC_X86_REG_RBX)),
  'failure':failure,'faults':faults}
def validate_stage(r):
 assert r['accepted_boundary'] and not r['failure'] and not r['faults'] and 0<r['instruction_count']<2000
def save(groups):
 (HERE/'raw-results.json').write_text(json.dumps(groups,indent=2)+'\n')
retained=HERE/'retained';retained.mkdir(exist_ok=True)
p=Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md');pb=p.read_bytes()
(retained/p.name).write_bytes(pb);(retained/'image-reader.py').write_bytes(rb)
(HERE/'source.json').write_text(json.dumps({'method':'B isolated original integer controller with controlled interior boundaries',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,'unicorn_version':unicorn.__version__,
 'bodies':bodies,'fields':{k:hex(v) for k,v in FIELDS.items()},'fixture':{'stack':hex(SP),'return':hex(RET),'source':hex(SRC),'saved_rbx':hex(saved_rbx)},
 'consumer':{'path':p.as_posix(),'retained':'retained/'+p.name,'bytes':len(pb),'sha256':sha(pb)},
 'stubs':[],'entry_limits':'PRIM setter is complete; phase prefix stops before capacity/geometry. Gate enters2102E8 AFTER omitted writer call with matching controlled frame. ALconsumer stops before indexdispatch/sharedcontinuation. No vertexwriter/transform/indexgenerator/nativeGPU effects, complete PACKED invocation or live state proven.'},indent=2)+'\n')
groups=[]
for name,mode,adcs in [('triangle-list-control',3,[0]*6),('line-list',1,[0]*6),('line-strip',2,[0]*6),
 ('triangle-strip',4,[0]*6),('point',0,[0]*6),('triangle-fan',5,[0]*6),('sprite',6,[0]*6),
 ('triangle-list-ADC-control',3,[0,0,1,0,0,0])]:
 u,gm=new_guest();gm.w(FIELDS['primitive'],b'\x07\xA5');gm.w(FIELDS['vertex_count'],b'\x11'*20)
 gm.w(SP,struct.pack('<Q',RET));u.reg_write(UC_X86_REG_RSP,SP);u.reg_write(UC_X86_REG_RCX,mode)
 g={'name':name,'mode':mode,'adcs':adcs,'starting_fields':snapshot(gm),'init':None,'vertices':[],
  'limits':'Candidate controller transitions only; actual vertexconversion/index effects omitted and counters held unchanged across that boundary.'}
 groups.append(g);g['init']=stage(u,gm,'PRIM-init',0x20FE70,{RET});save(groups);validate_stage(g['init'])
 assert g['init']['after']['phase']==0 and g['init']['after']['vertex_count']==0
 for i,adc in enumerate(adcs):
  v={'candidate':i+1,'adc':adc};g['vertices'].append(v)
  v['phase']=stage(u,gm,'phase',0x20F6B5,{0x20F6D6});save(groups);validate_stage(v['phase'])
  gm.w(SRC,struct.pack('<QQ',0,adc<<47));gm.w(SP,struct.pack('<Q',RET));gm.w(SP-8,struct.pack('<Q',saved_rbx))
  u.reg_write(UC_X86_REG_RSP,SP-0x38);u.reg_write(UC_X86_REG_RBX,SRC)
  v['gate']=stage(u,gm,'gate',0x2102E8,{RET});save(groups);validate_stage(v['gate'])
  assert v['gate']['final_rsp']==hex(SP+8) and v['gate']['final_rbx']==hex(saved_rbx)
  v['consumer']=stage(u,gm,'ALconsumer',0x20F70D,{0x20F721,0x20FA6F});save(groups);validate_stage(v['consumer'])
  if name=='triangle-list-control' and i==2:
   assert [x['gate']['al'] for x in g['vertices']]==[0,0,1]
   print('First three original triangle-list candidates passed; same retained group continues.',flush=True)
 g['original_code_unchanged']=all(gm.r(int(b['entry'],16),b['size']).hex()==b['raw_hex'] for b in bodies)
 assert g['original_code_unchanged'];save(groups)
 print(name,'AL',[v['gate']['al'] for v in g['vertices']],
  'required',g['init']['after']['required'],'carry',g['init']['after']['carry'],flush=True)
