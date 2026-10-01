"""Original bank-capacity source/ABI proof. No machine-code execution or gameplay."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')
status=json.loads((P/'capture-01.status.json').read_text())
if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture incomplete')
roles=V.validate(x)
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked source')
required_ranges=[('0x3325d0','0x33265b'),('0x41e3a0','0x41e489'),('0x409f10','0x409f42'),('0x51f9f0','0x51fb6c'),('0x51fb70','0x51fba7'),('0x51fbb0','0x51fce3'),('0x51f7a0','0x51f878'),('0x41e580','0x41e58c')]
if[(r['start'],r['end_exclusive']) for r in x['ranges']]!=required_ranges:raise RuntimeError('required source population changed')
ix={};graphs=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b,tail={0x3325d0:"0x426480",0x41e3a0:"0x5211f0",0x41e580:"0x409fe0"}.get(a))
 if set(local)!=g['visited']:raise RuntimeError('unaccounted source instructions')
 graphs.append({'entry':hex(a),'visited':len(g['visited']),'returns':[hex(t) for t in g['returns']],'calls':g['calls']})
req=[(0x332610,'mov','edx, 0xa'),(0x33263c,'call','0x41e3a0'),
 (0x41e3bb,'mov','ebx, edx'),(0x41e3de,'mov','qword ptr [rsi + 0xd90], rsi'),
 (0x41e439,'mov','rcx, qword ptr [rsi + 0xd90]'),(0x41e440,'mov','edx, ebx'),(0x41e442,'call','0x409f10'),
 (0x409f14,'mov','r9d, edx'),(0x409f23,'mov','edx, 0x50'),(0x409f34,'lea','r8d, [rdx - 0x4b]'),(0x409f38,'call','0x51f9f0'),
 (0x51fa11,'mov','r14d, r9d'),(0x51fa14,'mov','rbx, rcx'),(0x51fa38,'mov','qword ptr [rcx + 0x50], rdi'),
 (0x51fa47,'mov','word ptr [rcx + 0x24], r14w'),(0x51fa81,'mov','ecx, r8d'),
 (0x51fa89,'mov','edx, 1'),(0x51fa92,'shl','edx, cl'),(0x51fa9f,'imul','edx, r14d'),(0x51faa6,'mov','dword ptr [rbx + 0x54], edx'),
 (0x51fb70,'xor','eax, eax'),(0x51fb97,'mov','qword ptr [rcx + 0x50], rax'),(0x51fb9b,'mov','dword ptr [rcx + 0x58], eax'),
 (0x41e580,'mov','rcx, qword ptr [rcx + 0xd90]'),(0x41e587,'jmp','0x409fe0'),
 (0x51fbb9,'mov','eax, dword ptr [rcx + 0x54]'),(0x51fbc5,'cmp','dword ptr [rcx + 0x58], eax'),
 (0x51fbc8,'jl','0x51fbd6'),(0x51fbca,'or','eax, 0xffffffff'),(0x51fbd5,'ret',''),
 (0x51fbdb,'call','0x51f7a0'),(0x51fbe3,'test','rax, rax'),(0x51fbe6,'jne','0x51fbf9'),
 (0x51fbe8,'or','eax, 0xffffffff'),(0x51fbf8,'ret',''),
 (0x51f828,'call','0x51f6b0'),(0x51f830,'cmp','edi, -1'),(0x51f833,'jne','0x51f850'),(0x51f835,'xor','eax, eax'),(0x51f841,'ret','')]
for pc,m,a in req:
 if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required operation changed '+hex(pc))

# Check actual definition paths and register writes rather than a hand-made
# list of addresses being mistaken for an ABI argument proof.
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def written(pc):
 i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,w=i.regs_access()
 names={i.reg_name(r) for r in w}
 return names
def region(lo,hi):return sorted(pc for pc in ix if lo<=pc<hi)
def no_write(regs,lo,hi,permitted=()):
 bad=[hex(pc) for pc in region(lo,hi) if pc not in permitted and written(pc)&set(regs)]
 if bad:raise RuntimeError('argument carrier changed '+str(bad))
no_write(['edx','dx','dl','rdx'],0x332610+5,0x33263c)
no_write(['ebx','bx','bl','rbx'],0x41e3bb+2,0x41e440)
no_write(['r9d','r9w','r9b','r9'],0x409f14+3,0x409f38)
no_write(['r8d','r8w','r8b','r8'],0x51f9f0,0x51fa81)
no_write(['r14d','r14w','r14b','r14'],0x51fa11+3,0x51fa9f)
no_write(['edx','dx','dl','rdx'],0x51fa89+5,0x51faa6,[0x51fa92,0x51fa9f])
assert (1 << (5 & 31))*10==320 and (320*0x50)==0x6400
# Root group argument EBX is nonvolatile across ordinary Windows-x64 calls.
# Initializer's vector loop before capacity publication has no calls; table
# stores are assumed disjoint from its private frame and bank header.
g=G.graph({pc:i for pc,i in ix.items() if 0x51f9f0<=pc<0x51fb6c},0x51f9f0,0x51fb6c)
if not G.dominates(g,0x51faa6,0x51fb6b):raise RuntimeError('capacity write does not dominate normal return')
clears=[]
for pc,origin in [(0x51fa38,'constructor early clear'),(0x51fb97,'reset')]:
 m=ix[pc]['memory'][0]
 if m['role']!='w' or m['displacement']!=0x50 or m['size']!=8:raise RuntimeError('overlapping store changed')
 clears.append({'pc':hex(pc),'operation':origin,'interval':[0x50,0x58],'covers_capacity_54':0x50<=0x54 and 0x54+4<=0x58})

# Complete distinct immediate failure paths; do not infer their natural
# feasibility or explain a NULL helper return by a stubbed implementation.
alloc={pc:i for pc,i in ix.items() if 0x51fbb0<=pc<0x51fce3}
failures=[]
for name,fix,terminal,call in [('used-ge-capacity',{0x51fbc8:False},0x51fbd5,None),
                             ('backing-page-null',{0x51fbc8:True,0x51fbe6:False},0x51fbf8,'0x51f7a0')]:
 g=G.graph(alloc,0x51fbb0,0x51fce3,fixed=fix)
 if g['returns']!=[terminal] or (call is None and g['calls']) or(call is not None and [t for pc,t in g['calls']]!=[call]):raise RuntimeError('failure path changed')
 failures.append({'name':name,'return':hex(terminal),'calls':[{'pc':hex(pc),'target':t} for pc,t in g['calls']],'return_value':'FFFFFFFF (low16 FFFF)'})
result={'producer_complete':True,'method':'A STATIC_ONLY original boot-argument/capacity/reset/failure proof',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],
 'annotation_prerequisites':[roles],'instruction_assertions':len(req),'graphs':graphs,
 'identified_boot':{'root_call':'33263C ->41E3A0','groups':10,'wrapper':'409F10 ->51F9F0','entry_stride':0x50,'shift':5,'local_capacity_store':320,'backing_bytes_arithmetic':0x6400,'runtime_value_observed':False},
 'root_binding':'41E3A0 sets D90=root; later409F10 readsD90 and41E580 registration readsD90. Noninterference and valid ordinary ABI assumed; no universal all-root/write-set closure.',
 'overlapping_capacity_clears':clears,'failure_paths':failures,
 'answer':'This identified completed initializer publishes local capacity320. Constructor/reset qword+50 also clears capacity+54; starts-only offset54 census misses them. Allocator-1/registration40A1CC alone cannot distinguish immediate used>=capacity from backing-page-null underused<capacity.',
 'required_observation_discriminator':'If a later runtime proof is needed, record bank identity, initialization/teardown phase, capacity54 andused58, then distinguish51FBCA versus51FBE8 path before attributing40A1CC. Validate known positive registration and observer state; an undifferentiated -1 is not a full-bank witness.',
 'limitations':['Original instruction/ABI/local-write proof only, no native/harness/live execution',
  'Boot caller ordinary Windowsx64 nonvolatile EBX and valid root/frame/table nonaliasing/noninterference assumed',
  'Local constructor capacity320 does not establish real startup completed, all later writers, allocator backing success or consistent page metadata',
  'Backing-page NULL path is statically present; feasibility of that combined state under initialized metadata remains open',
  'Reset/preinit capacity0 is not simultaneously evidence for ordinary completed boot; actual callback timing/lifetime still needed if not statically closed',
  'External root final tail5211F0 is a named boundary, not analyzed/executed; its effects remain open',
  'Other roots/boot routes, authored simultaneous keys/owners and real bank exhaustion/competing-owner/rejection remain open; no wholeOV21 closure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED located boot capacity320, overlapping reset clear and distinct allocator-failure paths; no game/native')
