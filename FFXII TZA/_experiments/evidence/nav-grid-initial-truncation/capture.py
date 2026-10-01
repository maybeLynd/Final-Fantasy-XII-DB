import datetime,hashlib,importlib.util,json,math,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-NAV-GRID-INITIAL-TRUNCATION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists(),'Do not replace a retained capture'
tools=dict(before_capture_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,binaries=[])
for name,p in [('capstone',Path(capstone._cs._name)),('unicorn',Path(backend.uclib._name))]:tools['binaries'].append(dict(name=name,path=str(p),bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
P=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-quantization');m=json.loads((P/'manifest.json').read_text());assert m['members']
for x in m['members']:
 data=(P/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
source=(P/'source.json').read_bytes();s=json.loads(source);builder=next(x for x in s['bodies'] if x['entry']=='0x3924b0');body=bytes.fromhex(builder['raw_hex']);assert len(body)==607 and sha(body)=='0a7ec1000ef3d48a471ff9200675b11ef90717fedcb53b50afa84a4281e236f5'
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader)
image,ss=reader.load_image();assert sha(image)==s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and reader.img_rd(image,ss,0x3924B0,607)==body
ENTRY,END=0x39258C,0x392607;code=body[ENTRY-0x3924B0:END-0x3924B0];assert len(code)==123
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins=list(cs.disasm(code,ENTRY));assert sum(i.size for i in ins)==123
ii={i.address:i for i in ins};assert [(ii[p].mnemonic,ii[p].bytes.hex()) for p in (0x3925A9,0x3925CE)]==[('cvttss2si','f30f2cc1'),('cvttss2si','f30f2cc1')]
assert not any(i.mnemonic.startswith('j') or i.mnemonic in ('call','ret') for i in ins)
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0];bits=lambda x:struct.unpack('<I',struct.pack('<f',x))[0]
def preparation(w,h):
 # Host prediction supplying a disclosed boundary, NOT original sqrtf execution.
 return bits(f32(math.sqrt(f32(f32(w*h)/f32(275)))))
assert 1<struct.unpack('<f',struct.pack('<I',preparation(1,400)))[0]<2
GLOB,STACK,RSP=0x2AEE000,0x60001000,0x60001800
def run(name,w,h,mutated=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in (ENTRY&~4095,GLOB,STACK):u.mem_map(page,4096)
 running=bytearray(code)
 if mutated:
  off=0x3925A9-ENTRY;assert running[off:off+4].hex()=='f30f2cc1';running[off+2]=0x2D
 u.mem_write(ENTRY,bytes(running));u.mem_write(0x2AEE070,b'\xa5'*28);u.mem_write(RSP,b'\x00'*0x40)
 for off in (0x24,0x34):u.mem_write(RSP+off,bytes.fromhex('a5a5a5a5'))
 c0=preparation(w,h)
 regs=[(UC_X86_REG_RSP,RSP),(UC_X86_REG_RAX,0),(UC_X86_REG_MXCSR,0x1F80),(UC_X86_REG_XMM0,c0),(UC_X86_REG_XMM1,0),(UC_X86_REG_XMM2,0),(UC_X86_REG_XMM3,0),(UC_X86_REG_XMM4,0),(UC_X86_REG_XMM6,0),(UC_X86_REG_XMM7,0),(UC_X86_REG_XMM8,bits(w)),(UC_X86_REG_XMM9,bits(h)),(UC_X86_REG_XMM10,bits(w)),(UC_X86_REG_XMM11,bits(h))]
 for reg,v in regs:u.reg_write(reg,v)
 initial=dict(rsp=hex(u.reg_read(UC_X86_REG_RSP)),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),registers={str(reg):hex(u.reg_read(reg)) for reg,v in regs},sqrt_return_bits=f'{c0:08X}',width_bits=f'{bits(w):08X}',height_bits=f'{bits(h):08X}',globals=bytes(u.mem_read(0x2AEE070,28)).hex(),stack=bytes(u.mem_read(RSP,64)).hex())
 visited=[];reads=[];raw_writes=[];writes=[];pending=[];states=[]
 def flush():
  if not pending:return
  pc=pending[0][0];assert all(p==pc for p,a,n in pending)
  lo=min(a for p,a,n in pending);hi=max(a+n for p,a,n in pending);assert {j for p,a,n in pending for j in range(a,a+n)}==set(range(lo,hi))
  writes.append(dict(pc=hex(pc),address=hex(lo),bytes=bytes(u.mem_read(lo,hi-lo)).hex()));pending.clear()
 def oncode(uc,pc,n,_):
  flush();visited.append(hex(pc))
  if pc in (0x3925AD,0x3925D2,0x3925ED,0x392600):states.append(dict(pc=hex(pc),eax=f'{uc.reg_read(UC_X86_REG_EAX):08X}',xmm4=f'{uc.reg_read(UC_X86_REG_XMM4)&0xFFFFFFFF:08X}',xmm3=f'{uc.reg_read(UC_X86_REG_XMM3)&0xFFFFFFFF:08X}'))
 def onread(uc,t,a,n,v,_):reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=n))
 def onwrite(uc,t,a,n,v,_):
  pc=uc.reg_read(UC_X86_REG_RIP);pending.append((pc,a,n));raw_writes.append(dict(pc=hex(pc),address=hex(a),size=n,provider_value=v))
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 failure=None
 try:u.emu_start(ENTRY,END,count=128);flush()
 except Exception as e:failure=repr(e)
 after=dict(stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),floor_argument_bits=f'{u.reg_read(UC_X86_REG_XMM0)&0xFFFFFFFF:08X}',globals=bytes(u.mem_read(0x2AEE070,28)).hex(),stack=bytes(u.mem_read(RSP,64)).hex())
 return dict(name=name,intervention='Private CVTTSS2SI->CVTSS2SI first conversion' if mutated else 'Injected sqrt-return boundary/rectangle/stack/MXCSR; shipping arithmetic unchanged',mutated=mutated,running_code_sha256=sha(bytes(running)),initial=initial,visited=visited,reads=reads,raw_writes=raw_writes,writes=writes,states=states,after=after,failure=failure)
cases=[]
for name,w,h,mutant in [('positive-square-count-control',16.0,16.0,False),('positive-skinny-zero-count',1.0,400.0,False),('skinny-rounded-conversion-detector',1.0,400.0,True)]:
 c=run(name,w,h,mutant);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert c['failure'] is None and c['after']['stop_pc']==hex(END) and c['visited']==[hex(i.address) for i in ins] and c['after']['rsp']==hex(RSP) and c['after']['stack']==c['initial']['stack']
 assert len(c['writes'])==6 and len(c['states'])==4 and c['reads'] and c['raw_writes']
 if w==16:assert c['states'][0]['eax']==c['states'][1]['eax']=='00000010' and c['after']['floor_argument_bits']=='3F800000'
 elif not mutant:assert c['states'][0]['eax']=='00000000' and c['states'][2]['xmm4']=='7F800000' and c['after']['floor_argument_bits']=='7F800000'
 else:assert c['states'][0]['eax']=='00000001' and c['after']['floor_argument_bits']!='7F800000'
R=W/'retained';R.mkdir(exist_ok=False)
for n,data in [('source.json',source),('parent-manifest.json',(P/'manifest.json').read_bytes()),('window.bin',code),('shipping-reader.py',rp.read_bytes()),('corridor-contract.md',Path('Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-corridor-query-family.md').read_bytes())]:(R/n).write_bytes(data)
for x in tools['binaries']:assert sha(Path(x['path']).read_bytes())==x['sha256']
receipt=dict(method='B original123B post-sqrt/pre-floor arithmetic, disclosed host-prepared sqrt return, not library/fullbuilder/live proof',reference=dict(exe_sha256=sha(image),parent_source_sha256=sha(source),parent_body_sha256=sha(body),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),window_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),entry=hex(ENTRY),end=hex(END)),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],cases=cases,preparation=dict(method='Host source/IEEE prediction only; injected boundary, no native sqrtf call',formula='f32(sqrt(f32(f32(w*h)/f32(275))))',skinny_header_hex='0114011400000000',header_scope='u8 cellW1/cellH20/cols1/rows20, s16 origins0; source representation calculation, not authored occurrence/getter execution'),limits='Injected returned sqrt bits and width/height/minmax/registers/stackpadding/MXCSR1F80. No native sqrtf/floorf/allocator/cookie/getter/caller/fullbuilder/actualstate/librarybinding/scene/normaloccurrence/nativeCPUexception guarantee. Observed count and floor-call argument only, not finalcellsize/dimensions/allocation/fault.',cleanup='Disposable emulators only; no PC/game/process/save/config/reference/peer writes; originalprefix controls and downstream agreement pending independent review')
(W/'raw.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Retained positive-square control, skinny nx0/refinedInf original-prefix and labelled conversion detector; check required before acceptance.',flush=True)
