"""B verified original CDQ/IDIV/MOV slice, disposable guest; not full OPDIV."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess,types,inspect
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=W
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-INTEGER-DIVIDE-OVERFLOW');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
parent=Path('Database/FFXII TZA/_experiments/evidence/script-division-unordered-guard');parent_commit=subprocess.check_output(['git','log','-1','--format=%H','--',(parent/'raw.json').as_posix()],text=True).strip() or None
parent_manifest=json.loads((parent/'manifest.json').read_text());assert len(parent_manifest['members'])==31
for m in parent_manifest['members']:
 b=(parent/m['path']).read_bytes();assert len(b)==m['bytes'] and sha(b)==m['sha256']
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,sha256=sha(b),copy=n))
p=Path('Database/FFXII TZA/_experiments/evidence/script-comparison-unordered/raw.json');b=p.read_bytes();c='b956f1086e0523ecc8813fea66b60257eaeba816';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);tools=json.loads(b)['tools'];assert sha(Path(sys.executable).read_bytes())==tools['python_sha256'] and unicorn.__version__==tools['unicorn'] and capstone.__version__==tools['capstone']
for p in tools['provider_files']:assert sha(Path(p['path']).read_bytes())==p['sha256']
reader=(R/'shipping-reader.py').read_bytes();assert sha(reader)=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32';rd=types.ModuleType('shipping_reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile(reader,'certified original reader','exec'),rd.__dict__)
image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=rd.img_rd(image,ss,0x25f0d9,5);guard=rd.img_rd(image,ss,0x25f0d1,8);(R/'original5.bin').write_bytes(code);(R/'guard8.bin').write_bytes(guard)
parent_files=[]
for name in ['raw.json','manifest.json','retained/opdiv298.bin','retained/dispatch4.bin','retained/descriptor24.bin','retained/name32.bin']:
 p=parent/name;b=p.read_bytes()
 if parent_commit:assert b==subprocess.check_output(['git','show',parent_commit+':'+p.as_posix()])
 out='parent79-'+Path(name).name;(R/out).write_bytes(b);parent_files.append(dict(path=name,copy=out,sha256=sha(b)))
parent_raw=json.loads((R/'parent79-raw.json').read_text());assert parent_raw['reference']['exe_sha256']==sha(image) and parent_raw['reference']['opcode']=='0x15' and parent_raw['reference']['name']=='OPDIV'
full=(R/'parent79-opdiv298.bin').read_bytes();assert full==rd.img_rd(image,ss,0x25f0ac,298) and full[45:50]==code and full[37:45]==guard
assert (R/'parent79-dispatch4.bin').read_bytes()==rd.img_rd(image,ss,0x261df8+0x15*4,4)
descriptor=rd.img_rd(image,ss,0x1efea60+0x14*24,24);assert descriptor==(R/'parent79-descriptor24.bin').read_bytes()
namepc=int.from_bytes(descriptor[8:16],'little');assert rd.img_rd(image,ss,namepc,32)==(R/'parent79-name32.bin').read_bytes()
roles=types.ModuleType('roles');policy=(R/'reg_tracking.py').read_bytes();exec(compile(policy,'actual shared reviewed adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def rows(b,pc):
 ii=list(cs.disasm(b,pc));assert sum(i.size for i in ii)==len(b)
 return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
source=rows(code,0x25f0d9);source_guard=rows(guard,0x25f0d1);assert code.hex()=='99f7fb8bc8'
NV={UC_X86_REG_RDI:0x123456789abcdef,UC_X86_REG_RBP:0x23456789abcdef0,UC_X86_REG_RSI:0x3456789abcdef01,UC_X86_REG_R12:0x456789abcdef012,UC_X86_REG_R13:0x56789abcdef0123};LO=0x25f0d9;STOP=0x25f0de
def snapshot(u):return dict(pc=hex(u.reg_read(UC_X86_REG_RIP)),eax=f'{u.reg_read(UC_X86_REG_EAX):08X}',ebx=f'{u.reg_read(UC_X86_REG_EBX):08X}',edx=f'{u.reg_read(UC_X86_REG_EDX):08X}',ecx=f'{u.reg_read(UC_X86_REG_ECX):08X}',eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),nv={str(k):hex(u.reg_read(k)) for k in NV},code_hex=bytes(u.mem_read(0x25f0d9,5)).hex(),page_sha256=sha(bytes(u.mem_read(0x25f000,4096))))
def run(name,dividend,divisor,want,private=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(0x25f000,4096);page=bytearray(b'\xcc'*4096);body=code if not private else b'\x99\x90\x90\x8b\xc8';page[LO-0x25f000:STOP-0x25f000]=body;u.mem_write(0x25f000,bytes(page));actual={i.address:i for i in cs.disasm(body,LO)}
 visits=[];memory=[]
 def visit(uc,pc,size,_):
  assert pc in actual and actual[pc].size==size;observed=bytes(uc.mem_read(pc,size));assert observed==actual[pc].bytes;visits.append(dict(pc=hex(pc),hex=observed.hex(),before=snapshot(uc)))
 def mem(uc,kind,addr,size,value,_):memory.append(dict(kind=kind,address=hex(addr),size=size));raise AssertionError('Register slice must not access memory')
 u.hook_add(unicorn.UC_HOOK_CODE,visit);u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,mem)
 u.reg_write(UC_X86_REG_EAX,dividend&0xffffffff);u.reg_write(UC_X86_REG_EBX,divisor&0xffffffff);u.reg_write(UC_X86_REG_EDX,0xa5a5a5a5);u.reg_write(UC_X86_REG_ECX,0x12345678);u.reg_write(UC_X86_REG_EFLAGS,2);u.reg_write(UC_X86_REG_RIP,LO)
 for reg,value in NV.items():u.reg_write(reg,value)
 initial=snapshot(u);error=None
 try:
  try:u.emu_start(LO,STOP,count=8)
  except unicorn.UcError as e:error=dict(errno=e.errno,text=str(e))
  final=snapshot(u);assert not memory and final['nv']==initial['nv'] and final['ebx']==initial['ebx'] and final['page_sha256']==initial['page_sha256']
  if want=='exception':assert error and error['errno']==unicorn.UC_ERR_EXCEPTION and final['pc']=='0x25f0da' and [v['pc'] for v in visits]==['0x25f0d9','0x25f0da'] and final['ecx']==initial['ecx']
  else:
   quotient,remainder=want;assert error is None and final['pc']==hex(STOP) and (int(final['eax'],16),int(final['edx'],16),int(final['ecx'],16))==(quotient&0xffffffff,remainder&0xffffffff,quotient&0xffffffff)
 finally:
  u.mem_unmap(0x25f000,4096);assert list(u.mem_regions())==[]
 return dict(name=name,dividend=dividend,divisor=divisor,intervention='PRIVATE IDIV->twoNOP, supplied register entry' if private else 'Original5B slice, supplied register entry after OPDIV zero guard; zero case explicitly bypasses that guard',initial=initial,final=final,error=error,visits=visits,memory=memory,cleanup='Disposable sole guest mapping unmapped; no native host/game/save changes')
cases=[]
for args in [('positive',20,3,(6,2)),('negative',-20,3,(-6,-2)),('min-valid',-2147483648,1,(-2147483648,0)),('quotient-overflow',-2147483648,-1,'exception'),('zero-bypass-detection',1,0,'exception'),('private-idiv-nop',-2147483648,-1,(-2147483648,-1),True)]:
 cases.append(run(*args));(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
raw=dict(method='B verified original5B CDQ/IDIV/MOV in disposable guest with supplied register entry; A source nonzero guard; no full OPDIV/native OS/live',reference=dict(exe_sha256=sha(image),entry=hex(LO),stop=hex(STOP),code_sha256=sha(code),guard_sha256=sha(guard),adapter_sha256=sha(policy),files=files,parent_commit=parent_commit,parent_view='Committed primary verified against Git' if parent_commit else 'Own immutable frozen31 manifest verified; independently matched original handler/table/descriptor/name bytes, publication pending, not acceptance',parent_files=parent_files),instructions=source,guard=source_guard,tools=tools,cases=cases,driver_sha256=sha(Path(__file__).read_bytes()),limits='Guest register slice outcome/error only, not native OS exception vector/handler/game crash/fullOPDIV/pops/pushes/normal caller/authored values. Zero case intentionally bypasses original guard, detector only; privateNOP intervention not original behavior. No fault callback/stubs/memory; no live/native game/save/config/reference change. PC OFF/S19 unapproved/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE80 original quotient-overflow guest discriminator',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
