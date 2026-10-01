"""B: bounded shipping post-resolve POPV stage then shipping store leaf.
Entry boundaries are injected; notification/resolver not executed or stubbed.
"""
import hashlib,json,struct,subprocess,sys,types
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-POPV-CONVERSION-ORDER');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();P=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained');files=[]
for n in ['original194.bin','original-table24.bin','shipping-reader.py','reg_tracking.py']:
 p=P/n;b=p.read_bytes();assert b==subprocess.check_output(['git','show','8db582868ae4a72bae3f9e76c1d709844e9d9d93:'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),sha256=sha(b),bytes=len(b),verified_at='8db582868ae4a72bae3f9e76c1d709844e9d9d93'))
rd=types.ModuleType('shipping_reader');exec(compile((R/'shipping-reader.py').read_bytes(),'retained certified reader source','exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
LO,END,ENTRY,STOP=0x267e60,0x267f60,0x267ef2,0x267f1e;code=rd.img_rd(image,ss,LO,END-LO);(R/'original-popv256.bin').write_bytes(code);store=(R/'original194.bin').read_bytes();table=(R/'original-table24.bin').read_bytes();assert store==rd.img_rd(image,ss,0x26d530,194) and table==rd.img_rd(image,ss,0x26d5f4,24)
policy=(R/'reg_tracking.py').read_bytes();roles=types.ModuleType('roles');exec(compile(policy,'retained shared reviewed adapter source','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;pi={i.address:i for i in cs.disasm(code,LO)};si={i.address:i for i in cs.disasm(store,0x26d530)};assert sum(i.size for i in pi.values())==256 and sum(i.size for i in si.values())==194
allowed={pc for pc in pi if ENTRY<=pc<STOP or 0x267f4c<=pc<END};assert pi[0x267f4c].bytes.hex()=='f30f2c849384010000' and pi[0x267f55].operands[0].imm==0x267f1a
def decode(ii):return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,memory=[dict(kind=roles.op_kind(i,o,j),size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,scale=o.mem.scale) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii.values()]
STACK,DEST,RSP,REC,SENT=0x40000100,0x40000900,0x60001800,0x60001830,0x60000200
def run(tag,bits,width,depth=1,mutated=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for a,n in [(LO&~4095,4096),(0x26d000,4096),(0x40000000,4096),(0x60000000,8192)]:u.mem_map(a,n)
 body=bytearray(code)
 if mutated:body[0x267f4c-LO+2]=0x2d # CVTTSS2SI -> CVTSS2SI, private nearest-rounding control
 u.mem_write(LO,bytes(body));u.mem_write(0x26d530,store);u.mem_write(0x26d5f4,table)
 ram=bytearray(b'\xa5'*4096);struct.pack_into('<i',ram,STACK-0x40000000,depth);ram[STACK-0x40000000+4]=tag;struct.pack_into('<I',ram,STACK-0x40000000+0x184,bits);u.mem_write(0x40000000,bytes(ram));u.mem_write(0x60001000,b'\xa7'*4096)
 rec=bytearray(b'\xa6'*48);struct.pack_into('<Q',rec,16,DEST);struct.pack_into('<I',rec,24,width<<28);struct.pack_into('<i',rec,28,0);u.mem_write(REC,bytes(rec));u.reg_write(UC_X86_REG_RBX,STACK);u.reg_write(UC_X86_REG_RSP,RSP);u.reg_write(UC_X86_REG_MXCSR,0x1f80);u.reg_write(UC_X86_REG_EFLAGS,2)
 visits=[];reads=[];writes=[];phase='conversion';actual={i.address:i for i in cs.disasm(body,LO)};store_rsp=RSP-8
 def visit(uc,pc,size,_):
  i=actual[pc] if phase=='conversion' else si[pc];assert i.size==size
  assert pc in allowed if phase=='conversion' else pc in si
  assert i.mnemonic!='call','Unexpected original call: never stub';visits.append(dict(phase=phase,pc=hex(pc),hex=i.bytes.hex()))
 def read(uc,typ,address,size,value,_):
  legal=((address==STACK and size==4) or (address==STACK+4 and size==1) or (address==STACK+0x184 and size==4)) if phase=='conversion' else ((REC<=address and address+size<=REC+48) or (0x26d5f4<=address and address+size<=0x26d60c) or (address==store_rsp and size==8))
  assert legal,('Unexpected read',phase,hex(address),size);reads.append(dict(phase=phase,pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(address),size=size,hex=bytes(uc.mem_read(address,size)).hex()))
 def write(uc,typ,address,size,value,_):
  legal=(address in [STACK,REC+32] and size==4) if phase=='conversion' else (address==DEST and size in [1,2,4]);assert legal,('Unexpected write',phase,hex(address),size);writes.append(dict(phase=phase,pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(address),size=size,hex=(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 u.hook_add(unicorn.UC_HOOK_CODE,visit);u.hook_add(unicorn.UC_HOOK_MEM_READ,read);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
 u.emu_start(ENTRY,STOP,count=32);assert u.reg_read(UC_X86_REG_RIP)==STOP and u.reg_read(UC_X86_REG_RSP)==RSP
 conversion=dict(pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),depth=struct.unpack('<i',u.mem_read(STACK,4))[0],value_bits=bytes(u.mem_read(REC+32,4)).hex(),record=bytes(u.mem_read(REC,48)).hex(),ram=bytes(u.mem_read(0x40000000,4096)).hex(),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)))
 # Explicit second-entry intervention: supply the resolved record ABI at the
 # alreadyverified leaf. The real notification gate is NOT executed/stubbed.
 phase='store';u.reg_write(UC_X86_REG_RCX,REC);u.reg_write(UC_X86_REG_RSP,store_rsp);u.mem_write(store_rsp,struct.pack('<Q',SENT));u.emu_start(0x26d530,SENT,count=64);assert u.reg_read(UC_X86_REG_RIP)==SENT and u.reg_read(UC_X86_REG_RSP)==RSP
 after=dict(pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),record=bytes(u.mem_read(REC,48)).hex(),ram=bytes(u.mem_read(0x40000000,4096)).hex(),running_popv=bytes(u.mem_read(LO,256)).hex(),store=bytes(u.mem_read(0x26d530,194)).hex(),table=bytes(u.mem_read(0x26d5f4,24)).hex(),return_sentinel=bytes(u.mem_read(store_rsp,8)).hex(),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)))
 return dict(tag=tag,input_bits=f'{bits:08x}',width=width,depth=depth,mutated=mutated,running_hex=bytes(body).hex(),initial=dict(ram=bytes(ram).hex(),record=bytes(rec).hex(),rsp=hex(RSP),store_rsp=hex(store_rsp),return_sentinel=hex(SENT),mxcsr='0x1f80',entry=hex(ENTRY),stop=hex(STOP)),conversion=conversion,after=after,visits=visits,reads=reads,writes=writes)
specs=[(2,0x3fe00000,0,1,False),(2,0x4effffff,0,1,False),(2,0x4f000000,0,1,False),(2,0x4effffff,3,1,False),(2,0x4f000000,3,1,False),(1,0x7fffffff,0,1,False),(2,0x3fe00000,0,0,False),(2,0x3fe00000,0,1,True)]
cases=[]
for spec in specs:cases.append(run(*spec));(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
consumer='Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md';b=Path(consumer).read_bytes();(R/'consumer-before.md').write_bytes(b)
raw=dict(method='B isolated original post-resolve integer-kind POPV stage, stop before notification; explicit second-entry ABI intervention invokes verified original store leaf. No stubs/nativeCPU/live/caller/resolver/callback execution',reference=dict(exe_sha256=sha(image),base=hex(rd.IMG_LO),popv_entry=hex(LO),bytes=256,popv_sha256=sha(code),stage_entry=hex(ENTRY),stage_stop=hex(STOP),stage_allowed_pcs=[hex(p) for p in sorted(allowed)],store_entry='0x26d530',store_sha256=sha(store),table='0x26d5f4',table_sha256=sha(table),retained67_files=files,access_adapter_sha256=sha(policy)),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,provider_files=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name]]),driver_sha256=sha(Path(__file__).read_bytes()),instructions=decode(pi),store_instructions=decode(si),cases=cases,consumer=dict(path=consumer,sha256=sha(b)),limits='Injected alreadyresolved integer-kind path/state/tag/record/MXCSR1F80. No normal reachability/notification/banks/actualassetvalidity/lifetime. Guest conversion/writes notnative MXCSR exception/status or unmasked parity. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE70 bounded original conversion/store; reducer required',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
