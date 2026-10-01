import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import unicorn
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.x86_const import *
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retained131',W/'retained/check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image()
maxx=32257.0 # -32768 + 255*255, exactly representable
bits=struct.unpack('<I',struct.pack('<f',maxx))[0]
f=lambda u:struct.unpack('<f',struct.pack('<I',u))[0]
NV=[UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15]
source=dict(method='B supplemental finite negative-origin rounding control only; parent14 cases NOT rerun',
 exe_sha256=hashlib.sha256(raw).hexdigest(),parent_source_sha256=hashlib.sha256((W/'source.json').read_bytes()).hexdigest(),
 helper_sha256=hashlib.sha256((W/'retained/check.py').read_bytes()).hexdigest(),
 driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python_version=sys.version,unicorn_version=unicorn.__version__,
 cell_width=255,cell_height=2,cols=255,rows=2,origin_x=-32768,origin_z=0,upper_x=maxx,
 declared_cells=510,table_bytes=1020,table_contents='All510 wordsFFFF (empty); table ends exactly at unmapped HEAP end.',
 intervention='Planted header and table placement, finite fdclass host stub; no original-game allocation/ordinary caller.',
 cleanup='Isolated Python exits; no native game/save/config/reference/control changes.')
(W/'supplement-source.json').write_text(json.dumps(source,indent=2)+'\n')
result=[]
for name,x in [('negative-origin-interior',0.0),('negative-origin-upper-minus-two-ulps',f(bits-2)),('negative-origin-upper-minus-one-ulp',f(bits-1))]:
 w=m.World(dict(ptx=x,pty=3.0,ghdr=dict(cw=255,ch=2,cols=255,rows=2,ox=-32768,oy=0)),raw,secs)
 uc=w.uc;table=m.HEAP+0x100000-1020
 w.gm.w(table,b'\xff\xff'*510)
 w.gm.w(m.BASEP+m.GHDR+8,m.dw(table-m.BASEP))
 pcs=[];reads=[];float_stages=[]
 def on_code(uc,pc,size,_):
  pcs.append(hex(pc))
  if pc in (0x38401C,0x384020):
   xb=uc.reg_read(UC_X86_REG_XMM1)&0xffffffff
   float_stages.append(dict(pc=hex(pc),xmm1_low_hex='%08x'%xb,xmm1_f32=f(xb)))
 def on_read(uc,access,address,size,value,_):
  if uc.reg_read(UC_X86_REG_RIP)==0x38402C:
   reads.append(dict(pc='0x38402c',address=hex(address),size=size,index=(address-table)//2,bytes=w.gm.r(address,size).hex()))
 uc.hook_add(UC_HOOK_CODE,on_code);uc.hook_add(UC_HOOK_MEM_READ,on_read)
 rsp=m.STACK+0x80008;w.gm.w(rsp,m.qw(m.RETQ))
 uc.reg_write(UC_X86_REG_RSP,rsp);uc.reg_write(UC_X86_REG_RCX,m.PT);uc.reg_write(UC_X86_REG_MXCSR,0x1F80)
 for j,reg in enumerate(NV):uc.reg_write(reg,0xABC000+j)
 before=[hex(uc.reg_read(reg)) for reg in NV]
 try:uc.emu_start(m.GGRID,m.RETQ,count=2000)
 except unicorn.UcError as e:
  if not w.faults:w.faults.append(('emuerr',str(e)))
 o=dict(name=name,x=x,z=3.0,x_strictly_below_upper=x<maxx,point_hex=w.gm.r(m.PT,8).hex(),
  header_hex=w.gm.r(m.BASEP+m.GHDR,16).hex(),table=hex(table),table_sha256=hashlib.sha256(w.gm.r(table,1020)).hexdigest(),
  pcs=pcs,instructions=len(pcs),float_stages=float_stages,cell_reads=reads,stub_trace=w.trace,
  faults=w.faults,end_pc=hex(uc.reg_read(UC_X86_REG_RIP)),rax=uc.reg_read(UC_X86_REG_RAX),
  starting_rsp=hex(rsp),ending_rsp=hex(uc.reg_read(UC_X86_REG_RSP)),starting_mxcsr='0x1f80',
  ending_mxcsr=hex(uc.reg_read(UC_X86_REG_MXCSR)),nonvolatile_before=before,
  nonvolatile_after=[hex(uc.reg_read(reg)) for reg in NV])
 result.append(o)
 print(name,'x',x,'subtract',float_stages,'read',reads,'fault',w.faults,'end',o['end_pc'],flush=True)
(W/'supplement-raw.json').write_text(json.dumps(result,indent=2)+'\n')
