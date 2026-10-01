"""One original FF12 square instruction: native status control, not the live game."""
import ctypes,datetime,hashlib,importlib.util,json,platform,struct,sys
from pathlib import Path
import _ctypes,capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-ORIGINAL-MULSS-STATUS-CONTROL');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert sys.platform=='win32' and ctypes.sizeof(ctypes.c_void_p)==8 and platform.machine().lower() in ['amd64','x86_64']
assert not (W/'raw.json').exists() and not (W/'native-preflight.json').exists(),'Inspect retained attempt rather than retrying unchanged'
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
P=Path('Database/FFXII TZA/_experiments/evidence/nav-circle-cell-boundary');manifest=json.loads((P/'manifest.json').read_text())
for x in manifest['members']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
parent=(P/'retained/original237.bin').read_bytes();op=parent[0x46912E-0x4690B0:0x469132-0x4690B0];assert op==bytes.fromhex('f30f59d2')
rp=P/'retained/shipping-reader.py';sp=importlib.util.spec_from_file_location('rd',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and op==rd.img_rd(image,ss,0x46912E,4)
prefix=bytes.fromhex('4883ec180fae1c24c7442404801f00000fae542404660f6ed1')
suffix=bytes.fromhex('660f7ed00fae1a448b0424448942040fae14240fae5a084883c418c3')
wrapper=prefix+op+suffix;cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(wrapper,0x1000));assert sum(i.size for i in seq)==len(wrapper) and seq[-1].mnemonic=='ret'
assert not any(i.mnemonic in ['call','jmp'] or i.mnemonic.startswith('j') for i in seq)
assert [(i.mnemonic,i.op_str) for i in seq]==[('sub','rsp, 0x18'),('stmxcsr','dword ptr [rsp]'),('mov','dword ptr [rsp + 4], 0x1f80'),('ldmxcsr','dword ptr [rsp + 4]'),('movd','xmm2, ecx'),('mulss','xmm2, xmm2'),('movd','eax, xmm2'),('stmxcsr','dword ptr [rdx]'),('mov','r8d, dword ptr [rsp]'),('mov','dword ptr [rdx + 4], r8d'),('ldmxcsr','dword ptr [rsp]'),('stmxcsr','dword ptr [rdx + 8]'),('add','rsp, 0x18'),('ret','')]
kernel=ctypes.WinDLL('kernel32',use_last_error=True)
kernel.VirtualAlloc.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.c_uint32];kernel.VirtualAlloc.restype=ctypes.c_void_p
kernel.VirtualProtect.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32)];kernel.VirtualProtect.restype=ctypes.c_int
kernel.VirtualFree.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32];kernel.VirtualFree.restype=ctypes.c_int
kernel.GetCurrentProcess.argtypes=[];kernel.GetCurrentProcess.restype=ctypes.c_void_p
kernel.FlushInstructionCache.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t];kernel.FlushInstructionCache.restype=ctypes.c_int
kernel.GetModuleFileNameW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_uint32];kernel.GetModuleFileNameW.restype=ctypes.c_uint32
buf=ctypes.create_unicode_buffer(1024);assert kernel.GetModuleFileNameW(ctypes.c_void_p(kernel._handle),buf,1024);kernel_path=Path(buf.value)
tools=dict(before_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),host_arch=platform.machine(),windows=list(sys.getwindowsversion()),capstone=capstone.__version__,unicorn=unicorn.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name,_ctypes.__file__,kernel_path]])
source=dict(reference=dict(exe_sha256=sha(image),parent237_sha256=sha(parent),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),original_entry='0x46912e',original_bytes=op.hex(),original_bytes_count=4),wrapper_hex=wrapper.hex(),wrapper_sha256=sha(wrapper),original_offset=len(prefix),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in seq],boundary='Only shipping4BMULSS executes; private MOVD input, MXCSR init/save/status/readback/restore and RET scaffolding. Native invocation is current Pythonhost process, never FF12 or another process.')
(W/'native-preflight.json').write_text(json.dumps(dict(source=source,tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),control='Exact5 baseline before inexact finite value and private NOP-MUL detector; no unmasked/NaN/live cases'),indent=2)+'\n')
for name,data in [('original4.bin',op),('wrapper.bin',wrapper),('parent237.bin',parent),('parent-raw.json',(P/'raw.json').read_bytes()),('parent-manifest.json',(P/'manifest.json').read_bytes()),('shipping-reader.py',rp.read_bytes())]:(R/name).write_bytes(data)
class MBI(ctypes.Structure):
 _fields_=[('BaseAddress',ctypes.c_void_p),('AllocationBase',ctypes.c_void_p),('AllocationProtect',ctypes.c_uint32),('RegionSize',ctypes.c_size_t),('State',ctypes.c_uint32),('Protect',ctypes.c_uint32),('Type',ctypes.c_uint32)]
assert ctypes.sizeof(MBI)==48
kernel.VirtualQuery.argtypes=[ctypes.c_void_p,ctypes.POINTER(MBI),ctypes.c_size_t];kernel.VirtualQuery.restype=ctypes.c_size_t
prototype=ctypes.WINFUNCTYPE(ctypes.c_uint32,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32))
def native(running,input_bits):
 address=kernel.VirtualAlloc(None,4096,0x3000,4);assert address,ctypes.get_last_error()
 result=dict(input_bits=f'{input_bits:08x}',allocation='Ownprocess4096B private RW then RX; no external/game memory')
 try:
  ctypes.memmove(address,running,len(running));assert ctypes.string_at(address,len(running))==running
  old=ctypes.c_uint32();assert kernel.VirtualProtect(address,4096,0x20,ctypes.byref(old)) and old.value==4
  assert kernel.FlushInstructionCache(kernel.GetCurrentProcess(),address,len(running))
  output=(ctypes.c_uint32*4)(*[0xA5A5A5A5]*4);result['before_output_words']=[f'{x:08x}' for x in output]
  f=prototype(address);result['result_bits']=f'{f(input_bits,output):08x}';result['after_output_words']=[f'{x:08x}' for x in output]
  result['running_sha256']=sha(ctypes.string_at(address,len(running)))
 finally:
  result['freed']=bool(kernel.VirtualFree(address,0,0x8000));assert result['freed'],ctypes.get_last_error()
  mbi=MBI();assert kernel.VirtualQuery(address,ctypes.byref(mbi),ctypes.sizeof(mbi))==48;result['after_free_state']=hex(mbi.State);assert mbi.State==0x10000
 return result
def guest(running,input_bits):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);rsp,out,ret=0x60001808,0x40000100,0x10000
 for page in [0x1000,0x10000,0x60001000,0x40000000]:u.mem_map(page,4096)
 u.mem_write(0x1000,running);u.mem_write(rsp,struct.pack('<Q',ret));u.mem_write(out,b'\xa5'*16)
 for r,v in [(UC_X86_REG_RSP,rsp),(UC_X86_REG_RCX,input_bits),(UC_X86_REG_RDX,out),(UC_X86_REG_RAX,0xA5A5A5A5),(UC_X86_REG_MXCSR,0x1FA0)]:u.reg_write(r,v)
 visits=[];writes=[]
 def hook(uc,pc,size,_):visits.append(hex(pc))
 def write(uc,typ,a,n,v,_):writes.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=n,value=v))
 u.hook_add(unicorn.UC_HOOK_CODE,hook);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write);failure=None
 try:u.emu_start(0x1000,ret,count=64)
 except Exception as error:failure=repr(error)
 return dict(input_bits=f'{input_bits:08x}',initial_mxcsr='0x1fa0',before_output_words=['a5a5a5a5']*4,result_bits=f'{u.reg_read(UC_X86_REG_EAX):08x}',after_output_words=[f'{x:08x}' for x in struct.unpack('<IIII',bytes(u.mem_read(out,16)))],after_mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),visits=visits,writes=writes,failure=failure,running_sha256=sha(running))
cases=[]
for name,input_bits,mutant,want in [('exact-five',0x40A00000,False,'41c80000'),('next-above-five',0x40A00001,False,'41c80003'),('private-omit-mul',0x40A00001,True,'40a00001')]:
 running=bytearray(wrapper)
 if mutant:running[len(prefix):len(prefix)+4]=b'\x90'*4
 n=native(bytes(running),input_bits);g=guest(bytes(running),input_bits);c=dict(name=name,mutated=mutant,running_hex=bytes(running).hex(),native=n,guest=g);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert n['result_bits']==g['result_bits']==want and n['running_sha256']==g['running_sha256']==sha(running) and g['failure'] is None and g['stop_pc']=='0x10000' and g['rsp']=='0x60001810'
 assert n['after_output_words'][1]==n['after_output_words'][2] and n['after_output_words'][3]=='a5a5a5a5' and g['after_output_words'][1:]==['00001fa0','00001fa0','a5a5a5a5'] and g['after_mxcsr']=='0x1fa0'
 assert g['visits']==[hex(i.address) for i in cs.disasm(running,0x1000)] and 0<len(g['visits'])<64
 assert (running[len(prefix):len(prefix)+4]==op)!=mutant
for p in tools['providers']:assert sha(Path(p['path']).read_bytes())==p['sha256']
assert sha(image)==source['reference']['exe_sha256'] and image==rd.load_image()[0]
raw=dict(method='B one verified original4B MULSS in native current-host Win64 state wrapper versus same wrapper in Unicorn; not live game',driver_sha256=sha(Path(__file__).read_bytes()),source=source,tools=tools,cases=cases,limits='Only exact5/next-binary32 finite positive square and private omit-MUL control, masked round-nearest1F80. Native4B boundaries omit full4690B0/caller/init/gameMXCSR/library/scheduling. NativeABI wrapper injected; emulator status not automatically nativeCPU flags. No unmasked/NaN/subnormal/overflow exception proof. No broad reruns or general runtime platform.',cleanup='Native MXCSR saved/restored in wrapper with equality receipt, own private4096B code allocation freed/VirtualQuery MEM_FREE, output sentinel beyond12B preserved; fresh guests return/restore status. Standalone Python completes responsive, no external/game attach or process/control/save/config/reference/peer writes. PC OFF/S19 allowance unchanged/fullL1+L2NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('RETAINED57 native andguest result/status/control/cleanup, reducer required',flush=True)
print([(c['name'],c['native']['result_bits'],c['native']['after_output_words'][0],c['guest']['after_output_words'][0]) for c in cases],flush=True)
