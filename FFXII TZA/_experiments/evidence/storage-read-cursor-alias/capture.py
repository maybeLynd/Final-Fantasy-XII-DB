import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-STORAGE-READ-CURSOR-ALIAS');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists()
tools=dict(before_capture_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,binaries=[])
for name,p in [('capstone',Path(capstone._cs._name)),('unicorn',Path(backend.uclib._name))]:tools['binaries'].append(dict(name=name,path=str(p),bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader);image,ss=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ENTRY,STOP=0x866A00,0x70000000;code=reader.img_rd(image,ss,ENTRY,116);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins=list(cs.disasm(code,ENTRY));assert sum(i.size for i in ins)==116 and not any(i.mnemonic=='call' for i in ins)
ii={i.address:i for i in ins};assert ii[0x866A4D].bytes.hex()=='4188143a' and ii[0x866A54].bytes.hex()=='41ff01' and ii[0x866A3D].bytes.hex()=='418b09'
CUR,DEST,BASE,RSP=0x40002000,0x40003000,0x40004000,0x60001808
def run(name,count,alias):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in (ENTRY&~4095,0x1F44000,CUR,DEST,BASE,RSP&~4095,STOP):u.mem_map(page,4096)
 u.mem_write(ENTRY,code);u.mem_write(0x1F44D40,struct.pack('<QQ',BASE,BASE+4));u.mem_write(CUR,b'\0'*4);u.mem_write(DEST,b'\xa5'*8);u.mem_write(BASE,bytes.fromhex('0a14283c'));u.mem_write(RSP,struct.pack('<Q',STOP))
 target=CUR if alias else DEST;regs=[(UC_X86_REG_RCX,CUR),(UC_X86_REG_RDX,target),(UC_X86_REG_R8,count),(UC_X86_REG_RSP,RSP),(UC_X86_REG_RBX,0x1122334455667788),(UC_X86_REG_RSI,0x2233445566778899),(UC_X86_REG_RDI,0x33445566778899AA),(UC_X86_REG_MXCSR,0x1F80)]
 for reg,v in regs:u.reg_write(reg,v)
 initial=dict(registers={str(reg):hex(u.reg_read(reg)) for reg,v in regs},cursor=bytes(u.mem_read(CUR,4)).hex(),destination=bytes(u.mem_read(target,4)).hex(),disjoint_destination=bytes(u.mem_read(DEST,8)).hex(),source=bytes(u.mem_read(BASE,4)).hex(),global_vector=bytes(u.mem_read(0x1F44D40,16)).hex(),stack=bytes(u.mem_read(RSP-8,40)).hex())
 visited=[];reads=[];raw_writes=[];writes=[];pending=[]
 def flush():
  if not pending:return
  pc=pending[0][0];assert all(p==pc for p,a,n in pending);lo=min(a for p,a,n in pending);hi=max(a+n for p,a,n in pending);assert {j for p,a,n in pending for j in range(a,a+n)}==set(range(lo,hi));writes.append(dict(pc=hex(pc),address=hex(lo),bytes=bytes(u.mem_read(lo,hi-lo)).hex()));pending.clear()
 def oncode(uc,pc,n,_):flush();visited.append(hex(pc))
 def onread(uc,t,a,n,v,_):reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),bytes=bytes(uc.mem_read(a,n)).hex()))
 def onwrite(uc,t,a,n,v,_):
  pc=uc.reg_read(UC_X86_REG_RIP);pending.append((pc,a,n));raw_writes.append(dict(pc=hex(pc),address=hex(a),size=n,provider_value=v))
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 error=None
 try:u.emu_start(ENTRY,STOP,count=128);flush()
 except Exception as e:error=repr(e)
 after=dict(rip=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),eax=u.reg_read(UC_X86_REG_EAX),nonvolatile={str(reg):hex(u.reg_read(reg)) for reg,v in regs if reg in (UC_X86_REG_RBX,UC_X86_REG_RSI,UC_X86_REG_RDI)},cursor=bytes(u.mem_read(CUR,4)).hex(),destination=bytes(u.mem_read(target,4)).hex(),disjoint_destination=bytes(u.mem_read(DEST,8)).hex(),source=bytes(u.mem_read(BASE,4)).hex(),global_vector=bytes(u.mem_read(0x1F44D40,16)).hex(),stack=bytes(u.mem_read(RSP-8,40)).hex())
 return dict(name=name,count=count,alias=alias,intervention='Injected disposable cursor/vector/destination/ABI; shipping leaf unchanged',initial=initial,visited=visited,reads=reads,raw_writes=raw_writes,writes=writes,after=after,error=error)
cases=[]
for name,count,alias in [('one-byte-disjoint-control',1,False),('one-byte-cursor-alias',1,True),('two-byte-disjoint-control',2,False),('two-byte-cursor-alias-feedback',2,True),('zero-count-alias-no-copy-control',0,True)]:
 c=run(name,count,alias);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n');a=c['after']
 assert c['error'] is None and a['rip']==hex(STOP) and a['rsp']==hex(RSP+8) and a['source']==c['initial']['source'] and a['global_vector']==c['initial']['global_vector']
 assert a['nonvolatile']=={k:c['initial']['registers'][k] for k in a['nonvolatile']} and len(c['visited'])<128 and c['reads'] and c['writes']
 expect=11 if alias and count else count;assert a['cursor']==struct.pack('<I',expect).hex() and a['eax']==(0 if alias and count==2 else 1)
 data=[x for x in c['writes'] if x['pc']=='0x866a4d'];assert len(data)==(1 if alias and count else count)
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.bin').write_bytes(code);(R/'shipping-reader.py').write_bytes(rp.read_bytes())
for name,p in [('contract.md','Database/FFXII TZA/19-Save-Load-Settings/CONTRACT-storage-read-completion.md'),('differential.py','Reconstruction/Tests/Differential/diff_storage_read.py')]: (R/name).write_bytes(Path(p).read_bytes())
for x in tools['binaries']:assert sha(Path(x['path']).read_bytes())==x['sha256']
raw=dict(method='B verified original116B pure leaf, injected memory/entry ABI; no calls/stubs/wrapper/nativefile/save/live',reference=dict(exe_sha256=sha(image),entry=hex(ENTRY),bytes=len(code),body_sha256=sha(code),reader_sha256=sha(rp.read_bytes())),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),cases=cases,limits='Only destination=cursor lowbyte/count0,1,2 and disjoint controls, vector4bytes. Not all overlaps/general memory safety/nativeCPU/fullstorage/wrapper/caller/save corruption/reachability. Instrumented readbytes are instruction-boundary observations in single emulator; no concurrentstate or live atomicity claim.',cleanup='Disposable emulator instances, source unchanged; no actual game/process/control/save/config/reference/peerconsumer changes')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('Captured alias immediateincrement+next-read feedback, disjoint1/2 and zero no-copy controls; readonlycheck/independentreview required.',flush=True)
