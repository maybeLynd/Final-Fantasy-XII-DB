import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import UC_X86_REG_RIP,UC_X86_REG_RSP,UC_X86_REG_RCX
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd();sha=lambda b:hashlib.sha256(b).hexdigest()
reader=ROOT/'Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py'
spec=importlib.util.spec_from_file_location('retained_reader_and_guest_memory',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image();md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies=[]
for a,n in [(0x633390,500),(0x6B6700,71)]:
 b=m.img_rd(raw,secs,a,n);ins=list(md.disasm(b,a));assert sum(i.size for i in ins)==len(b)
 bodies.append({'entry':hex(a),'bytes':n,'sha256':sha(b),'raw_hex':b.hex(),'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
assert bodies[0]['sha256']=='2e9ba08fb90cf456170fc7042ce1be4bc571c8d88557d8fb46a31cb58211c501'
assert bodies[1]['sha256']=='4f773d1e8a86fdc0679db27c2f585fcfce9413659797da17a635a510c0f684b9'
# Local observer control: record member-node spans omitted by EXP097's obs map.
head=0x50000080;nodes=[0x52000100,0x1002000100];links=[n+8 for n in nodes];ret=0x62000000;stack=0x61000808
results=[]
for variant in ['original','node-prev-selflink-NOP-control']:
 uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);gm=m.GuestMem(uc)
 code=bytearray.fromhex(bodies[1]['raw_hex'])
 if variant!='original':
  assert code[0x40:0x44].hex()=='48895208';code[0x40:0x44]=b'\x90'*4
 for page in [0x6B6000,head&~0xFFF,*[n&~0xFFF for n in nodes],stack&~0xFFF,ret]:gm.map(page,0x1000)
 gm.w(0x6B6700,code);gm.w(stack,struct.pack('<Q',ret));gm.w(head,struct.pack('<QQ',links[0],links[-1]))
 before={}
 for i,n in enumerate(nodes):
  blob=bytearray(bytes([0xA5 if i==0 else 0x5A])*56)
  blob[8:24]=struct.pack('<QQ',links[i+1] if i+1<len(nodes) else head,links[i-1] if i else head)
  gm.w(n,blob);before[hex(n)]=blob.hex()
 events=[];steps=[]
 uc.hook_add(unicorn.UC_HOOK_CODE,lambda u,a,n,x:steps.append(a))
 def write(u,access,a,n,value,x):events.append({'pc':hex(u.reg_read(UC_X86_REG_RIP)),'address':hex(a),'bytes':n,'value':hex(value&((1<<(8*n))-1))})
 uc.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
 uc.reg_write(UC_X86_REG_RSP,stack);uc.reg_write(UC_X86_REG_RCX,head)
 uc.emu_start(0x6B6700,ret,timeout=2_000_000,count=1000)
 assert uc.reg_read(UC_X86_REG_RIP)==ret and uc.reg_read(UC_X86_REG_RSP)==stack+8 and 0<len(steps)<1000
 after={hex(n):gm.r(n,56).hex() for n in nodes};head_after=list(struct.unpack('<QQ',gm.r(head,16)))
 assert head_after==[head,head]
 results.append({'variant':variant,'fixture':'supplied guest head and two nodes, one above4GiB; no live allocation provenance',
 'code_sha256':sha(code),'entry_rsp':hex(stack),'end':hex(ret),'final_rsp':hex(stack+8),'instruction_count':len(steps),
 'head':hex(head),'head_after':[hex(x) for x in head_after],'nodes':[hex(n) for n in nodes],
 'before':before,'after':after,'write_events':events,'sequence':[hex(x) for x in steps],
 'calls_or_stubs':0,'normal_native_return':True})
(HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
refs=[
 'Database/FFXII TZA/_experiments/evidence/class-descriptor-dtor-exec/check.py',
 'Database/FFXII TZA/_experiments/evidence/class-descriptor-dtor-exec/result.json',
 'Database/FFXII TZA/_experiments/evidence/class-descriptor-dtor-exec/bodies.json',
 'Database/FFXII TZA/_experiments/EXP-097-class-descriptor-dtor-exec.md',
 'Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md']
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,f in enumerate(refs):
 b=Path(f).read_bytes();n=f'{i:02d}-'+Path(f).name;(HERE/'retained'/n).write_bytes(b);pins.append({'path':f,'retained':'retained/'+n,'bytes':len(b),'sha256':sha(b)})
(HERE/'source.json').write_text(json.dumps({'method':'A complete original teardown + retained EXP097; B focused no-call drain / one mutation observer control',
 'exe_sha256':sha(raw),'reader_sha256':sha(reader.read_bytes()),'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'capstone_version':capstone.__version__,'unicorn_version':unicorn.__version__,'bodies':bodies,'refs':pins,
 'limits':'Supplied guest node provenance. Unmodified71-byte routine only in original arm. Mutation arm is observer falsification, not shipping behavior. No allocator/callback bridge or live process.'},indent=2)+'\n')
print('ORIGINAL drain and labeled single mutation complete; both heads self-linked. Raw node bytes now retained. No EXP097 campaign replay.',flush=True)
