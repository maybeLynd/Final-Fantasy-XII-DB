"""B full shipping comparator on valid disposable stack; A six consumers."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,subprocess,types,inspect
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=W
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-COMPARISON-UNORDERED');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();assert b==subprocess.check_output(['git','show','8db582868ae4a72bae3f9e76c1d709844e9d9d93:'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),bytes=len(b),sha256=sha(b),verified_at='8db582868ae4a72bae3f9e76c1d709844e9d9d93'))
prior=json.loads(Path('Database/FFXII TZA/_experiments/evidence/script-popv-negative-rounding/raw.json').read_text());tools=prior['tools'];assert sha(Path(sys.executable).read_bytes())==tools['python_sha256'] and unicorn.__version__==tools['unicorn'] and capstone.__version__==tools['capstone']
for p in tools['provider_files']:assert sha(Path(p['path']).read_bytes())==p['sha256']
rd=types.ModuleType('shipping_reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile((R/'shipping-reader.py').read_bytes(),'retained certified reader','exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
LO=0x25d740;code=rd.img_rd(image,ss,LO,413);(R/'compare413.bin').write_bytes(code);table=rd.img_rd(image,ss,0x261df8+40,24);(R/'consumer-table24.bin').write_bytes(table)
roles=types.ModuleType('roles');policy=(R/'reg_tracking.py').read_bytes();exec(compile(policy,'shared reviewed adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def rows(b,pc):return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,memory=[dict(kind=roles.op_kind(i,o,j),size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in cs.disasm(b,pc)]
source=rows(code,LO);assert sum(len(bytes.fromhex(x['hex'])) for x in source)==413
consumers=[]
for j,n in enumerate(struct.unpack('<6I',table)):
 pc=0x120000+n;b=rd.img_rd(image,ss,pc,24);(R/f'consumer-{j+10:02x}.bin').write_bytes(b);consumers.append(dict(opcode=j+10,entry=hex(pc),bytes=24,sha256=sha(b),instructions=rows(b,pc)))
STACK=0x40000100;RSP=0x60001808;SENT=0x60000200
NV={UC_X86_REG_RBX:0x1234123412341234,UC_X86_REG_RDI:0x2345234523452345,UC_X86_REG_RBP:0x3456345634563456,UC_X86_REG_RSI:0x4567456745674567,UC_X86_REG_XMM6:0x123456789abcdef0123456789abcdef,UC_X86_REG_XMM7:0x23456789abcdef0123456789abcdef0}
def run(name,left,right,expected,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);maps=[(0x25d000,4096),(0x40000000,4096),(0x60000000,8192)]
 for a,n in maps:u.mem_map(a,n)
 body=bytearray(code)
 if mutant:body[0x25d8b5-LO:0x25d8b7-LO]=b'\x90\x90'
 u.mem_write(LO,bytes(body));actual={i.address:i for i in cs.disasm(body,LO)}
 ram=bytearray(b'\xa5'*4096);struct.pack_into('<i',ram,0x100,2);ram[0x104:0x106]=b'\x02\x02';struct.pack_into('<II',ram,0x284,left,right);u.mem_write(0x40000000,bytes(ram));u.mem_write(0x60001000,b'\xa7'*4096);u.mem_write(RSP,struct.pack('<Q',SENT))
 for reg,value in NV.items():u.reg_write(reg,value)
 u.reg_write(UC_X86_REG_RCX,STACK);u.reg_write(UC_X86_REG_RSP,RSP);u.reg_write(UC_X86_REG_MXCSR,0x1f80);u.reg_write(UC_X86_REG_EFLAGS,2)
 initial=dict(rcx=hex(u.reg_read(UC_X86_REG_RCX)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),nonvolatile={str(k):hex(u.reg_read(k)) for k in NV},ram=bytes(u.mem_read(0x40000000,4096)).hex(),frame=bytes(u.mem_read(RSP-0x48,0x68)).hex(),code_sha256=sha(bytes(u.mem_read(LO,413))))
 visits=[];reads=[];writes=[]
 def visit(uc,pc,size,_):
  assert pc in actual;ins=actual[pc];assert ins.size==size and ins.mnemonic!='call','Unexpected call: no fault stubs';visits.append(dict(pc=hex(pc),hex=ins.bytes.hex(),eflags=hex(uc.reg_read(UC_X86_REG_EFLAGS))))
 def read(uc,typ,addr,size,value,_):
  legal=((addr==STACK and size==4) or (addr in [STACK+4,STACK+5] and size==1) or (addr in [STACK+0x184,STACK+0x188] and size==4) or RSP-0x48<=addr and addr+size<=RSP+0x20);assert legal,('unexpected read',hex(addr),size);reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(addr),size=size,hex=bytes(uc.mem_read(addr,size)).hex()))
 def write(uc,typ,addr,size,value,_):
  assert (addr==STACK and size==4) or RSP-0x48<=addr and addr+size<=RSP+0x20,('unexpected write',hex(addr),size);writes.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(addr),size=size,hex=(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 u.hook_add(unicorn.UC_HOOK_CODE,visit);u.hook_add(unicorn.UC_HOOK_MEM_READ,read);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
 u.emu_start(LO,SENT,count=128)
 final=dict(pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),eax=f'{u.reg_read(UC_X86_REG_EAX):08X}',mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),nonvolatile={str(k):hex(u.reg_read(k)) for k in NV},ram=bytes(u.mem_read(0x40000000,4096)).hex(),frame=bytes(u.mem_read(RSP-0x48,0x68)).hex(),code_sha256=sha(bytes(u.mem_read(LO,413))))
 want=bytearray(ram);struct.pack_into('<i',want,0x100,0);got=u.reg_read(UC_X86_REG_EAX);signed=got-0x100000000 if got&0x80000000 else got
 assert final['pc']==hex(SENT) and final['rsp']==hex(RSP+8) and final['nonvolatile']==initial['nonvolatile'] and bytes.fromhex(final['ram'])==bytes(want) and signed==expected and final['code_sha256']==initial['code_sha256']
 for a,n in maps:u.mem_unmap(a,n)
 return dict(name=name,left_bits=f'{left:08X}',right_bits=f'{right:08X}',intervention='Private JP25D8B5->twoNOPs' if mutant else 'Original shipping code with injected valid float operands/ABI',initial=initial,final=final,result_signed=signed,visits=visits,reads=reads,writes=writes,cleanup='All three disposable guest mappings unmapped; no host game process/native allocation/save changes')
cases=[]
for args in [('ordered-less',0x3f800000,0x40000000,-1),('ordered-equal',0x3f800000,0x3f800000,0),('ordered-greater',0x40000000,0x3f800000,1),('nan-left',0x7fc12345,0x3f800000,1),('nan-right',0x3f800000,0x7fc12345,1),('nan-self',0x7fc12345,0x7fc12345,1),('private-jp-nop',0x7fc12345,0x3f800000,0,True)]:
 cases.append(run(*args));(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
raw=dict(method='B full413B original comparator in disposable guest, valid depth2/tag2/maskedMXCSR; A original six24B consumers, privateJP-NOP labelled. No full interpreter/nativeCPU/live',reference=dict(exe_sha256=sha(image),source_sha256=sha(code),table_sha256=sha(table),adapter_sha256=sha(policy),files=files),tools=tools,instructions=source,consumers=consumers,cases=cases,driver_sha256=sha(Path(__file__).read_bytes()),limits='Guest masked comparison/return/pop and source boolean consumers only; not native exception/status/unmasked behavior/gameRC/actual authored NaN reachability/full caller/interpreter/live. Bad-tag/underflow/fault-call behavior not executed or stubbed. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE77 original comparator ordered/unordered effects',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
