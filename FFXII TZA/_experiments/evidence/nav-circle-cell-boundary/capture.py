"""Execute only verified shipping237B in fresh disposable guests; no live game."""
import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-CIRCLE-CELL-BOUNDARY');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not (W/'raw.json').exists() and not (W/'in-progress-cases.json').exists(),'Never replace an existing capture'
source=json.loads((W/'source.json').read_text());code=(R/'original237.bin').read_bytes();assert sha(code)==source['reference']['body_sha256'] and len(code)==237
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)==source['reference']['exe_sha256'] and code==rd.img_rd(image,ss,0x4690B0,237)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,0x4690B0));by_pc={i.address:i for i in seq};assert len(seq)==67 and not any(i.mnemonic=='call' for i in seq)
assert by_pc[0x469147].bytes[0]==0x77 and by_pc[0x469147].mnemonic=='ja' and by_pc[0x469147].operands[0].imm==0x4690EB
tools=dict(before_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name]])
(R/'capture-before-run.py').write_bytes(Path(__file__).read_bytes())
ENTRY,END,SENTINEL=0x4690B0,0x46919D,0x60000200
RECT,CIRCLE,STACK,RSP=0x40000100,0x40000200,0x60001000,0x60001808
bits=lambda f:struct.unpack('<I',struct.pack('<f',f))[0]
to_float=lambda b:struct.unpack('<f',struct.pack('<I',b))[0]
def run(name,x,z,r_bits,mutated=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in [ENTRY&~4095,0x40000000,STACK,0x60000000]:u.mem_map(page,4096)
 running=bytearray(code)
 if mutated:running[0x469147-ENTRY]=0x73 # JA -> JAE, explicitly private intervention.
 u.mem_write(ENTRY,bytes(running));rectangle=bytearray(b'\xa5'*32);circle=bytearray(b'\xa5'*24)
 for off,val in [(0,0.),(8,0.),(0x10,10.),(0x18,10.)]:struct.pack_into('<f',rectangle,off,val)
 for off,val in [(0,x),(8,z)]:struct.pack_into('<f',circle,off,val)
 struct.pack_into('<I',circle,0x10,r_bits)
 u.mem_write(RECT,bytes(rectangle));u.mem_write(CIRCLE,bytes(circle));stack=bytearray(b'\xa4'*80);struct.pack_into('<Q',stack,0,SENTINEL);u.mem_write(RSP,bytes(stack))
 regs=[(UC_X86_REG_RSP,RSP),(UC_X86_REG_RCX,RECT),(UC_X86_REG_RDX,CIRCLE),(UC_X86_REG_RAX,0xA5A5A5A5A5A5A5A5),(UC_X86_REG_EFLAGS,2),(UC_X86_REG_MXCSR,0x1F80)]
 for r,v in regs:u.reg_write(r,v)
 for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5]:u.reg_write(r,0xA5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5)
 initial=dict(rcx=hex(RECT),rdx=hex(CIRCLE),rsp=hex(RSP),sentinel=hex(SENTINEL),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),rax=hex(u.reg_read(UC_X86_REG_RAX)),rectangle=bytes(u.mem_read(RECT,32)).hex(),circle=bytes(u.mem_read(CIRCLE,24)).hex(),stack=bytes(u.mem_read(RSP,80)).hex(),xmm0_5=[hex(u.reg_read(r)) for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5]])
 visits=[];reads=[];writes=[];comparisons=[]
 compare_regs={'xmm0':UC_X86_REG_XMM0,'xmm1':UC_X86_REG_XMM1,'xmm2':UC_X86_REG_XMM2,'xmm3':UC_X86_REG_XMM3,'xmm4':UC_X86_REG_XMM4,'xmm5':UC_X86_REG_XMM5}
 def oncode(uc,pc,size,_):
  assert pc in by_pc and size==by_pc[pc].size,('Unexpected execution',hex(pc),size)
  visits.append(hex(pc));i=by_pc[pc]
  if i.mnemonic=='comiss':
   operands=[]
   for o in i.operands:
    if o.type==capstone.CS_OP_REG:operands.append(f'{uc.reg_read(compare_regs[i.reg_name(o.reg)])&0xFFFFFFFF:08x}')
    else:
     base=RECT if i.reg_name(o.mem.base)=='rcx' else CIRCLE if i.reg_name(o.mem.base)=='rdx' else None;assert base is not None
     operands.append(bytes(uc.mem_read(base+o.mem.disp,4)).hex())
   comparisons.append(dict(pc=hex(pc),args=i.op_str,operands=operands,eflags_before=hex(uc.reg_read(UC_X86_REG_EFLAGS))))
 def onread(uc,typ,a,size,value,_):
  assert (RECT<=a and a+size<=RECT+32) or (CIRCLE<=a and a+size<=CIRCLE+24) or (a==RSP and size==8),('Unexpected read',hex(a),size)
  reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=size,bytes=bytes(uc.mem_read(a,size)).hex()))
 def onwrite(uc,typ,a,size,value,_):writes.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=size,value=value));raise AssertionError('Predicate unexpectedly wrote memory')
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 failure=None
 try:u.emu_start(ENTRY,SENTINEL,count=128)
 except Exception as error:failure=repr(error)
 after=dict(stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),rax=hex(u.reg_read(UC_X86_REG_RAX)),eax=u.reg_read(UC_X86_REG_EAX),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),rectangle=bytes(u.mem_read(RECT,32)).hex(),circle=bytes(u.mem_read(CIRCLE,24)).hex(),stack=bytes(u.mem_read(RSP,80)).hex())
 return dict(name=name,method='B full original237B leaf in isolated disposable guest' if not mutated else 'B private JA->JAE detector intervention, not shipping code',mutated=mutated,x_bits=f'{bits(x):08x}',z_bits=f'{bits(z):08x}',radius_bits=f'{r_bits:08x}',running_hex=bytes(running).hex(),running_sha256=sha(running),initial=initial,visits=visits,reads=reads,writes=writes,comparisons=comparisons,after=after,failure=failure)
cases=[];r5=bits(5.)
specs=[('positive-inside',5.,5.,r5,False,1),('negative-distant',-6.,5.,r5,False,0),('edge-tangent',-5.,5.,r5,False,1),('corner-min-min-tangent',-3.,-4.,r5,False,0),('corner-min-max-tangent',-3.,14.,r5,False,0),('corner-max-min-tangent',13.,-4.,r5,False,0),('corner-max-max-tangent',13.,14.,r5,False,0),('corner-first-radius-next-up',-3.,-4.,r5+1,False,1),('corner-first-radius-next-down',-3.,-4.,r5-1,False,0),('corner-first-private-inclusive',-3.,-4.,r5,True,1)]
for name,x,z,rb,mutant,want in specs:
 c=run(name,x,z,rb,mutant);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert c['failure'] is None and c['after']['stop_pc']==hex(SENTINEL) and c['after']['rsp']==hex(RSP+8) and c['after']['eax']==want and c['reads'] and c['comparisons'] and 0<len(c['visits'])<128
 assert not c['writes'] and all(c['after'][k]==c['initial'][k] for k in ['rectangle','circle','stack']) and c['visits'][-1] in ['0x4690f0','0x46919c']
 assert (c['running_sha256']==source['reference']['body_sha256'])!=mutant
for p in tools['providers']:assert sha(Path(p['path']).read_bytes())==p['sha256'] and Path(p['path']).stat().st_size==p['bytes']
raw=dict(method='B verified original237B call-free leaf, initialized disposable ABI/argument state, MXCSR1F80; one private JA->JAE detector',driver_sha256=sha(Path(__file__).read_bytes()),source=source,tools=tools,cases=cases,limits='Only finite ordered0..10 rectangle/radius5 and adjacent binary32 values under injected MXCSR1F80. No native/live initialization/caller occurrence/radius distribution/actual MXCSR/NaN exceptions/timing/whole rasterizer or memory safety guarantee. Full source237B executes but actual gameplay/scheduling/ownership untouched.',cleanup='Fresh disposable guest per case, no callbacks/stubs/writes, complete RET to sentinel/stack advancement, original argument/stack bytes unchanged; standalone script completes. PC OFF/noFF12/game/save/config/reference/peer writes; S19 budget unchanged, fullL1+L2NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURED55 original edge/corner boundaries and adjacent radius; raw retained, reducer/review required',flush=True)
