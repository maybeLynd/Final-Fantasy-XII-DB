import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail
b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-POSTMULTIPLY-FLOAT-ORDER');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists(),'Do not replace an original-code capture'
tools=dict(before_capture_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,binaries=[])
for name,p in [('capstone',Path(capstone._cs._name)),('unicorn',Path(backend.uclib._name))]:tools['binaries'].append(dict(name=name,path=str(p),bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
P=Path('Database/FFXII TZA/_experiments/evidence/postmultiply-order-alias');m=json.loads((P/'manifest.json').read_text());assert m['members']
for x in m['members']:
 data=(P/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
source=(P/'source.json').read_bytes();s=json.loads(source);body=bytes.fromhex(s['raw_hex']);assert len(body)==349 and sha(body)=='69b03e9207174ab6f16e5d56817186ec446e5348ab0025255fc8a585d064b726'
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader)
image,ss=reader.load_image();assert sha(image)==s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and reader.img_rd(image,ss,0x3977B0,349)==body
ENTRY,END=0x3977CD,0x397863;code=body[ENTRY-0x3977B0:END-0x3977B0];assert len(code)==150
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins=list(cs.disasm(code,ENTRY));assert sum(i.size for i in ins)==150
assert [(i.address,i.bytes.hex()) for i in ins if i.mnemonic=='addss']==[(0x397844,'f30f58d0'),(0x397850,'f30f58d1'),(0x397857,'f30f58d0')]
assert ins[-1].address==0x39785E and ins[-1].mnemonic=='movss' and not any(i.mnemonic in ('call','ret','jmp') for i in ins)
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
bits=lambda x:struct.unpack('<I',struct.pack('<f',x))[0]
def predictions(row):
 p=[f32(x) for x in row]
 return dict(ordered=bits(f32(f32(f32(p[1]+p[0])+p[2])+p[3])),balanced=bits(f32(f32(p[0]+p[1])+f32(p[2]+p[3]))),real_number_sum=bits(sum(p)))
assert predictions([2**24,1,1,-2**24])==dict(ordered=0,balanced=0x3F800000,real_number_sum=0x40000000)
# Same bounded observer approach as scaled-random-float-order: read/write hooks,
# instruction boundary flush of provider write fragments into committed bytes.
OUT,BMAT,STACK=0x40000000,0x40001000,0x60001000;RSP=STACK+0x800
def run(name,row,mutated=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in (ENTRY&~4095,OUT,BMAT,STACK):u.mem_map(page,4096)
 running=bytearray(code)
 if mutated:
  off=0x397850-ENTRY;assert running[off:off+4].hex()=='f30f58d1';running[off+2]=0x5C
 u.mem_write(ENTRY,bytes(running));av=struct.pack('<16f',*([1.0]*16));bv=struct.pack('<16f',*(row+[0.0]*12))
 u.mem_write(OUT,av);u.mem_write(BMAT,bv);u.mem_write(RSP,b'\xa5'*64)
 for reg,v in [(UC_X86_REG_RCX,OUT),(UC_X86_REG_RDX,BMAT),(UC_X86_REG_RSP,RSP),(UC_X86_REG_RAX,0),(UC_X86_REG_R8,0),(UC_X86_REG_R9,0),(UC_X86_REG_R10,0),(UC_X86_REG_XMM6,0),(UC_X86_REG_XMM7,0),(UC_X86_REG_MXCSR,0x1F80)]:u.reg_write(reg,v)
 initial=dict(rcx=hex(u.reg_read(UC_X86_REG_RCX)),rdx=hex(u.reg_read(UC_X86_REG_RDX)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),xmm6=hex(u.reg_read(UC_X86_REG_XMM6)),xmm7=hex(u.reg_read(UC_X86_REG_XMM7)),A=bytes(u.mem_read(OUT,64)).hex(),B=bytes(u.mem_read(BMAT,64)).hex(),snapshot=bytes(u.mem_read(RSP,64)).hex())
 visited=[];reads=[];raw_writes=[];writes=[];pending=[]
 def flush():
  if not pending:return
  pc=pending[0][0];assert all(p==pc for p,a,n in pending)
  lo=min(a for p,a,n in pending);hi=max(a+n for p,a,n in pending);assert {j for p,a,n in pending for j in range(a,a+n)}==set(range(lo,hi))
  writes.append(dict(pc=hex(pc),address=hex(lo),bytes=bytes(u.mem_read(lo,hi-lo)).hex()));pending.clear()
 def oncode(uc,pc,n,_):flush();visited.append(hex(pc))
 def onread(uc,t,a,n,v,_):reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=n))
 def onwrite(uc,t,a,n,v,_):
  pc=uc.reg_read(UC_X86_REG_RIP);pending.append((pc,a,n));raw_writes.append(dict(pc=hex(pc),address=hex(a),size=n,provider_value=v))
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 failure=None
 try:u.emu_start(ENTRY,END,count=128);flush()
 except Exception as e:failure=repr(e)
 after=dict(A=bytes(u.mem_read(OUT,64)).hex(),B=bytes(u.mem_read(BMAT,64)).hex(),snapshot=bytes(u.mem_read(RSP,64)).hex(),rsp=hex(u.reg_read(UC_X86_REG_RSP)),rax=hex(u.reg_read(UC_X86_REG_RAX)),stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)))
 return dict(name=name,intervention='Private ADDSS->SUBSS at397850' if mutated else 'Injected disjoint A/B, aligned stack and entry state; shipping instructions unchanged',mutated=mutated,running_code_sha256=sha(bytes(running)),initial=initial,visited=visited,reads=reads,raw_writes=raw_writes,writes=writes,after=after,output_bits=bytes(u.mem_read(OUT,4)).hex(),host_prediction=predictions(row),failure=failure)
cases=[]
for name,row,mutated,expected in [('finite-cancellation-grouping-discriminator',[2**24,1,1,-2**24],False,0),('ordinary-integer-agreement-control',[1.0,2.0,3.0,4.0],False,0x41200000),('ordinary-add-to-subtract-write-detector',[1.0,2.0,3.0,4.0],True,0x40800000)]:
 c=run(name,row,mutated);cases.append(c)
 # Stop before the next case if the feasibility/detection control is invalid.
 (W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert c['failure'] is None and c['after']['stop_pc']==hex(END) and c['visited']==[hex(i.address) for i in ins],name
 assert c['after']['rsp']==hex(RSP) and c['after']['B']==c['initial']['B'] and c['after']['snapshot']==c['initial']['A'],name
 assert len(c['writes'])==5 and c['writes'][-1]==dict(pc='0x39785e',address=hex(OUT),bytes=expected.to_bytes(4,'little').hex()),name
 assert c['output_bits']==expected.to_bytes(4,'little').hex() and c['after']['A'][8:]==c['initial']['A'][8:],name
R=W/'retained';R.mkdir(exist_ok=False)
for n,data in [('source.json',source),('parent-manifest.json',(P/'manifest.json').read_bytes()),('window.bin',code),('shipping-reader.py',rp.read_bytes()),('primitives.md',Path('Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md').read_bytes())]: (R/n).write_bytes(data)
for x in tools['binaries']:assert sha(Path(x['path']).read_bytes())==x['sha256'],'Tool changed during capture'
receipt=dict(method='B original150B snapshot/first-output prefix, controlled disjoint memory and MXCSR1F80; not live/nativeCPU/full invocation',reference=dict(exe_sha256=sha(image),parent_source_sha256=sha(source),parent_body_sha256=sha(body),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),window_sha256=sha(code),entry=hex(ENTRY),end=hex(END),reader_sha256=sha(rp.read_bytes())),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],cases=cases,limits='Snapshot/first output only, injected disjoint A/B, aligned stack, MXCSR1F80; skipped cookie/prologue/nonvolatile saves; stops before other outputs/loop/cookie-check/return. No general domain/NaN/subnormal/rounding-mode/alias law or normalcaller/rendering proof.',cleanup='Disposable emulators only; no game/PC/process/save/config/reference or peer-file writes; acceptance pending checker and independent review')
(W/'raw.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Retained original first-output rounding discriminator, ordinary control and labelled write detector; not accepted until check.',flush=True)
