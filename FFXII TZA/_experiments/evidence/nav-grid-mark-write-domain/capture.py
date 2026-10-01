"""B: verified post-overlap writes in disposable guest memory, not live FF12."""
import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-GRID-MARK-WRITE-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists();R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');(R/'shipping-reader.py').write_bytes(rp.read_bytes());(R/'reg_tracking.py').write_bytes(Path(roles.__file__).read_bytes())
tools=dict(before_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name]])
sp=importlib.util.spec_from_file_location('rd',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
START,END=0x3923D6,0x39242E;body=rd.img_rd(d,ss,0x392200,679);code=body[START-0x392200:END-0x392200];assert len(code)==88
(R/'parent679.bin').write_bytes(body);(R/'write-window88.bin').write_bytes(code)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;parent=list(cs.disasm(body,0x392200));ii={i.address:i for i in parent};assert sum(i.size for i in parent)==679 and parent[-1].mnemonic=='ret'
ins=list(cs.disasm(code,START));assert sum(i.size for i in ins)==88 and not any(i.mnemonic.startswith('j') or i.mnemonic in ['call','ret'] for i in ins)
assert ii[0x392252].op_str=='r12d, ecx' and ii[0x3923CD].operands[0].imm==0x4690B0 and ii[0x3923D2].op_str=='eax, eax' and ii[0x3923D4].mnemonic=='je' and ii[0x3923D4].operands[0].imm==END
assert roles.op_kind(ii[0x392412],ii[0x392412].operands[0],0)=='w' and roles.op_kind(ii[0x39242B],ii[0x39242B].operands[0],0)=='rw' and ii[0x39242B].size==3
pe=struct.unpack_from('<I',d,0x3c)[0];pr,ps=struct.unpack_from('<II',d,pe+24+112+24);pd=rd.img_rd(d,ss,rd.IMG_LO+pr,ps);ext=[]
for j in range(0,ps-11,12):
 a,e,u=struct.unpack_from('<III',pd,j)
 if a+rd.IMG_LO<0x3924A7 and e+rd.IMG_LO>0x392200:
  head=rd.img_rd(d,ss,u+rd.IMG_LO,4);flags=head[0]>>3;off=4+((head[2]+1)//2)*4
  ub=rd.img_rd(d,ss,u+rd.IMG_LO,off+(12 if flags==4 else (4 if flags&3 else 0)))
  ext.append(dict(directory_rva=hex(pr),record_offset=j,record_hex=pd[j:j+12].hex(),entry=hex(a+rd.IMG_LO),end=hex(e+rd.IMG_LO),unwind=hex(u+rd.IMG_LO),flags=flags,unwind_hex=ub.hex(),chain=[hex(v+rd.IMG_LO) for v in struct.unpack_from('<III',ub,off)] if flags==4 else None))
last=0x392200;refs={(x['entry'],x['end'],x['unwind']):x for x in ext};root=(ext[0]['entry'],ext[0]['end'],ext[0]['unwind'])
for x in ext:
 assert int(x['entry'],16)==last;last=int(x['end'],16);cur=x;seen=set()
 while cur['flags']==4:
  k=(cur['entry'],cur['end'],cur['unwind']);assert k not in seen;seen.add(k);cur=refs[tuple(cur['chain'])]
 assert (cur['entry'],cur['end'],cur['unwind'])==root
assert last==0x3924A7 and len(ext)==3
source=dict(reference=dict(exe_sha256=sha(d),base=hex(rd.IMG_LO),parent_entry='0x392200',parent_bytes=679,parent_sha256=sha(body),entry=hex(START),end=hex(END),window_bytes=88,window_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),policy_sha256=sha(Path(roles.__file__).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),tools=tools,extents=ext,instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))) for i in ins])
(W/'source.json').write_text(json.dumps(source,indent=2)+'\n')
GLOB,HEAP,BASE,OCC=0x2AEE000,0x40000000,0x40000100,0x40000148
LO,N=BASE-16,16+110+16
def run(name,id_,col=0,occupancy=0,mutated=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in [START&~4095,GLOB,HEAP]:u.mem_map(page,4096)
 running=bytearray(code)
 if mutated:
  p=0x39242B-START;assert ii[0x39242B].mnemonic=='inc';running[p:p+3]=b'\x90'*3
 seq=list(cs.disasm(running,START));assert sum(i.size for i in seq)==88
 u.mem_write(START,bytes(running));u.mem_write(HEAP,b'\xa4'*4096);u.mem_write(BASE,b'\x00'*110);u.mem_write(OCC+col,bytes([occupancy]))
 for addr,val,fmt in [(0x2AEE060,2,'<I'),(0x2AEE0B8,36,'<I'),(0x2AEE0A0,BASE,'<Q'),(0x2AEE0A8,OCC,'<Q')]:u.mem_write(addr,struct.pack(fmt,val))
 regs=[(UC_X86_REG_R12D,id_&0xFFFFFFFF),(UC_X86_REG_EBX,col),(UC_X86_REG_EDI,0),(UC_X86_REG_RFLAGS,0x202)]
 for reg,val in regs:u.reg_write(reg,val)
 before=bytes(u.mem_read(LO,N));initial=dict(registers={str(reg):hex(u.reg_read(reg)) for reg,val in regs},globals=bytes(u.mem_read(GLOB,4096))[0x60:0xBC].hex(),focus_address=hex(LO),focus_bytes=before.hex(),id=id_,row=0,col=col,occupancy=occupancy,layout=dict(width=2,stride=36,records_base=hex(BASE),records_bytes=72,occupancy_base=hex(OCC),occupancy_bytes=2,scratch_bytes=36))
 visits=[];reads=[];raw_writes=[];writes=[];pending=[]
 def flush():
  for pc,a,n in pending:writes.append(dict(pc=hex(pc),address=hex(a),size=n,bytes=bytes(u.mem_read(a,n)).hex()))
  pending.clear()
 def oncode(uc,pc,n,_):flush();visits.append(hex(pc))
 def onread(uc,t,a,n,v,_):reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=n))
 def onwrite(uc,t,a,n,v,_):
  pc=uc.reg_read(UC_X86_REG_RIP);raw_writes.append(dict(pc=hex(pc),address=hex(a),size=n,provider_value=v));pending.append((pc,a,n))
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 failure=None
 try:u.emu_start(START,END,count=128);flush()
 except Exception as e:failure=repr(e)
 after=bytes(u.mem_read(LO,N));changed=[dict(address=hex(LO+j),before=f'{a:02x}',after=f'{b:02x}') for j,(a,b) in enumerate(zip(before,after)) if a!=b]
 return dict(name=name,intervention='Injected post-positive-overlap register/global/two-cell layout; '+('private NOP-INC data control' if mutated else 'shipping write fragment unchanged'),mutated=mutated,running_sha256=sha(running),running_hex=bytes(running).hex(),initial=initial,visits=visits,reads=reads,raw_writes=raw_writes,post_write_bytes=writes,after=dict(stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),focus_bytes=after.hex(),changed=changed,r12d=hex(u.reg_read(UC_X86_REG_R12D))),failure=failure)
cases=[]
for args in [('positive-observer-id0',0,0,0,False),('last-in-record-id287',287,0,0,False),('next-record-id288',288,0,0,False),('last-cell-id288-occupancy-alias',288,1,0,False),('negative-one-no-low-byte-bit',-1,0,0,False),('negative-eight-prefix-write',-8,0,0,False),('occupancy255-wrap',0,0,255,False),('observer-NOP-INC-control',0,0,255,True)]:
 c=run(*args);cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert c['failure'] is None and c['after']['stop_pc']==hex(END) and c['visits']==[hex(i.address) for i in cs.disasm(bytes.fromhex(c['running_hex']),START)]
 assert c['reads'] and len(c['raw_writes'])==len(c['post_write_bytes'])==(1 if c['mutated'] else 2) and all(x['size']==1 for x in c['raw_writes'])
 if len(cases)==1:
  assert c['post_write_bytes']==[dict(pc='0x392412',address=hex(BASE),size=1,bytes='01'),dict(pc='0x39242b',address=hex(OCC),size=1,bytes='01')],'Stop immediately if positive observer control fails'
for x in tools['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256']
raw=dict(source=source,cases=cases,method='B shipping88B post-positive-overlap write fragment in disposable emulators; injected boundary/state; no native geometry/fullfunction/live behavior',limits='Only mapped injected memory/register/layout/IDs are observed. No geometry predicate/prologue/coordinate conversion/loop/cookie/native caller/initialized state/reentrancy/concurrent scheduling/actual invalid-ID reachability/crash/false-empty live cell or portable defaults. Private NOP-INC not original semantics. No source/native write-order atomicity claim.',cleanup='Fresh emulator per case, bounded128 instructions, no PC/game/process/save/config/reference/peer memory or file writes')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE_MARK_WRITE original88B boundary/ID/bytecounter controls retained; independent reducer/check needed, not normalgame proof')
