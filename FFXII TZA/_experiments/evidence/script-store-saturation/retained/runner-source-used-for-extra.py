"""B: complete call-free original store leaf/table in bounded disposable guests."""
import hashlib,importlib.util,json,struct,subprocess,sys,types
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-STORE-SATURATION');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding/retained');reader=(P/'shipping-reader.py').read_bytes();policy=(P/'reg_tracking.py').read_bytes();(R/'shipping-reader.py').write_bytes(reader);(R/'reg_tracking.py').write_bytes(policy)
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';roles=types.ModuleType('roles');exec(compile(policy,'retained reviewed adapter source','exec'),roles.__dict__)
ENTRY,END,TABLE=0x26d530,0x26d5f2,0x26d5f4;code=rd.img_rd(image,ss,ENTRY,END-ENTRY);tab=rd.img_rd(image,ss,TABLE,24);targets=[rd.IMG_LO+v for v in struct.unpack('<6I',tab)];cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,ENTRY)};assert sum(i.size for i in ii.values())==len(code) and ii[END-1].mnemonic=='ret' and all(a in ii for a in targets) and not any(i.mnemonic=='call' for i in ii.values())
assert ii[0x26d545].mnemonic=='ja' and ii[0x26d545].operands[0].imm==END-1 and ii[0x26d577].bytes.hex()=='0f4fc1'
# Validate full intraprocedural control closure including the exact six targets.
todo=[ENTRY];seen=set();rets=[]
while todo:
 pc=todo.pop()
 if pc in seen:continue
 assert pc in ii,('Control exits original verified leaf',hex(pc));seen.add(pc);i=ii[pc]
 if i.mnemonic=='ret':rets.append(pc);continue
 if i.mnemonic=='jmp':todo.extend(targets if i.operands[0].type==capstone.CS_OP_REG else [i.operands[0].imm]);continue
 if i.mnemonic.startswith('j'):assert i.operands[0].type==capstone.CS_OP_IMM;todo.append(i.operands[0].imm)
 todo.append(pc+i.size)
assert len(targets)==6 and len(rets)>=6 and max(rets)==END-1
(R/'original194.bin').write_bytes(code);(R/'original-table24.bin').write_bytes(tab)
records=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,memory=[dict(kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp,size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii.values()]
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,provider_files=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name]],limits='Provider file identities; no native CPU/game execution or MXCSR flag parity proof')
DEST,REC,RSP,SENT=0x40000100,0x40000200,0x60001808,0x60000200
def run(width,value,index=0,mutated=False,lowbits=0):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(ENTRY&~4095,4096);u.mem_map(0x40000000,4096);u.mem_map(0x60000000,8192);body=bytearray(code)
 if mutated:body[0x26d577-ENTRY+1]=0x4c # CMOVG -> CMOVL, labelled private detector.
 running={i.address:i for i in cs.disasm(body,ENTRY)};u.mem_write(ENTRY,bytes(body));u.mem_write(TABLE,tab);memory=b'\xa5'*96;u.mem_write(DEST-32,memory);rec=bytearray(b'\xa6'*48);struct.pack_into('<Q',rec,16,DEST);struct.pack_into('<I',rec,24,(width<<28)|lowbits);struct.pack_into('<i',rec,28,index);struct.pack_into('<I',rec,32,value&0xffffffff);u.mem_write(REC,bytes(rec));u.mem_write(RSP,struct.pack('<Q',SENT));u.reg_write(UC_X86_REG_RCX,REC);u.reg_write(UC_X86_REG_RSP,RSP);u.reg_write(UC_X86_REG_MXCSR,0x1f80);u.reg_write(UC_X86_REG_EFLAGS,2)
 visits=[];reads=[];writes=[]
 def visit(uc,pc,size,_):assert pc in seen and running[pc].size==size;visits.append(hex(pc))
 def read(uc,typ,address,size,value,_):
  assert (REC<=address and address+size<=REC+48) or (TABLE<=address and address+size<=TABLE+24) or (address==RSP and size==8),('Unexpected read',hex(address),size)
  reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(address),size=size,hex=bytes(uc.mem_read(address,size)).hex()))
 def write(uc,typ,address,size,value,_):
  assert DEST-32<=address and address+size<=DEST+64,('Unexpected write',hex(address),size);writes.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(address),size=size,value=value,hex=value.to_bytes(size,'little').hex()))
 u.hook_add(unicorn.UC_HOOK_CODE,visit);u.hook_add(unicorn.UC_HOOK_MEM_READ,read);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write);error=None
 try:u.emu_start(ENTRY,SENT,count=64)
 except Exception as ex:error=repr(ex)
 after=dict(pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),guard_memory=bytes(u.mem_read(DEST-32,96)).hex(),record=bytes(u.mem_read(REC,48)).hex(),code=bytes(u.mem_read(ENTRY,len(body))).hex(),table=bytes(u.mem_read(TABLE,24)).hex(),stack=bytes(u.mem_read(RSP,8)).hex())
 return dict(width=width,input_bits=f'{value&0xffffffff:08x}',signed_input=struct.unpack('<i',struct.pack('<I',value&0xffffffff))[0],index=index,lowbits=hex(lowbits),mutated=mutated,running_hex=bytes(body).hex(),initial=dict(record=bytes(rec).hex(),guard_memory=memory.hex(),rsp=hex(RSP),return_sentinel=hex(SENT),mxcsr='0x1f80'),visits=visits,reads=reads,writes=writes,after=after,error=error)
specs=[(0,-1,0),(0,0,0),(0,255,0),(0,256,0),(1,-129,0),(1,-128,0),(1,127,0),(1,128,0),(2,-1,0),(2,65535,0),(2,65536,0),(3,-32769,0),(3,-32768,0),(3,32767,0),(3,32768,0),(4,-2147483648,0),(4,2147483647,0),(5,0x7fc00000,0),(6,123,0),(3,42,-1)]
cases=[]
for width,value,index in specs:
 c=run(width,value,index);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n');assert c['error'] is None and c['after']['pc']==hex(SENT) and c['after']['rsp']==hex(RSP+8) and c['reads'] and c['visits'][-1] in [hex(r) for r in rets]
cases.append(run(0,256,mutated=True));cases.append(run(0,256,lowbits=0x0800007f));assert all(c['error'] is None for c in cases)
consumers=[]
for n,p in [('variables-primary-before.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md'),('verbs-primary-before.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md')]:
 b=Path(p).read_bytes();(R/n).write_bytes(b);consumers.append(dict(path=p,sha256=sha(b),retained=n))
raw=dict(method='B full original call-free194B leaf+original24B dispatch table in initialized disposable guests; one private clamp-opcode detector and injected ABI/state; no game/native CPU/caller execution',reference=dict(exe_sha256=sha(image),base=hex(rd.IMG_LO),reader_sha256=sha(reader),access_policy_sha256=sha(policy),entry=hex(ENTRY),end=hex(END),source_bound='Closed original entry/branch/six-table-target/RET graph, not .pdata: no leaf unwind entry found in preparation',body_sha256=sha(code),table_address=hex(TABLE),table_sha256=sha(tab),targets=[hex(x) for x in targets],reachable_pcs=[hex(x) for x in sorted(seen)],returns=[hex(x) for x in sorted(rets)]),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),instructions=records,cases=cases,consumers=consumers,limits='Supplied already-resolved record/value, no POPV conversion/callback/normal caller/native bank state/lifetime/reachability or malformed/global alias safety. Integer cases and raw width5 store under emulator; no native MXCSR status claim. PC OFF/S19 unchanged/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE67 original closed leaf memory writes; reducer required',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
