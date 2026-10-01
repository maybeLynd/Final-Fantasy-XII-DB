"""Named original tracker cleanup and its183720 registration boundary, Method A.

Read METHODS.md. Validate the three normal188B fragments by actual unwind chains
and a closed entry CFG; do not call the87B root a whole function. Callee effects
are separate. No general observer/classifier, process or native execution.
"""
import hashlib,importlib.util,json,pathlib,struct,sys,capstone
from capstone.x86_const import X86_OP_IMM
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'title-tracker-cleanup-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong reference image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];secs=[];pd=[]
for k in range(n):
 q=p+24+o+40*k;secs.append(struct.unpack_from('<IIII',d,q+8))
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):pd.append(tuple(x+0x120000 for x in struct.unpack_from('<III',d,j)))
def read(a,z):
 for vs,va,rs,ro in secs:
  if 0x120000+va<=a and a+z<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+z]
 raise ValueError('unbacked original source')
frags=[x for x in pd if 0x1fb660<=x[0]<0x1fb71c];chains=[]
if [(x[0],x[1]) for x in frags]!=[(0x1fb660,0x1fb6b7),(0x1fb6b7,0x1fb6f1),(0x1fb6f1,0x1fb71c)]:raise ValueError('normal fragment extents changed')
for entry in frags[1:]:
 h=read(entry[2],4)
 if not h[0]>>3&4:raise ValueError('normal continuation has no unwind chain')
 size=4+2*((h[2]+1)&~1);raw=read(entry[2],size+12)
 target=tuple(x+0x120000 for x in struct.unpack_from('<III',raw,size))
 if target!=frags[0]:raise ValueError('continuation does not bind exact original root')
 chains.append(dict(fragment=list(entry),raw_unwind=raw.hex(),root=list(target)))
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ix={i.address:i for i in cs.disasm(read(0x1fb660,188),0x1fb660)}
if sum(i.size for i in ix.values())!=188:raise ValueError('incomplete normal decoder')
todo=[0x1fb660];seen=set();returns=[];calls=[]
while todo:
 a=todo.pop()
 if a in seen:continue
 if a not in ix:raise ValueError('entry-normal CFG leaves verified fragments')
 seen.add(a);i=ix[a]
 if i.mnemonic=='ret':returns.append(a);continue
 if i.mnemonic=='call':calls.append(dict(pc=hex(a),target=i.op_str))
 if i.mnemonic.startswith('j'):
  if len(i.operands)!=1 or i.operands[0].type!=X86_OP_IMM:raise ValueError('unresolved branch/tail boundary')
  todo.append(i.operands[0].imm)
  if i.mnemonic!='jmp':todo.append(a+i.size)
 else:todo.append(a+i.size)
if returns!=[0x1fb71b] or seen!=set(ix):raise ValueError('incomplete/zero normal coverage')
helper=[x for x in pd if x[0]==0x183720]
if len(helper)!=1 or helper[0][:2]!=(0x183720,0x183754):raise ValueError('named registration helper physical identity changed')
method=dict(question='Does tracker1FB660 directly free its value fields or invoke registered/delegated operations, and what remains unresolved for title callback cancellation?',
 hypotheses=['local nulling/draining establishes all native release/cancellation effects','original boundary calls register/delegate effects whose target/scheduling require separate evidence'],
 method='A original code: exact normal CFG and call/argument dataflow discriminate local effects; no isolated/live samples needed for this boundary.',
 existing='Retained24A680/181610/1B1960 and published title routing/local guards; new source captures only missing188Bvalue-cleanup and52Bhelper.',
 controls='Exact EXE hash/unwind chain roots/full normal CFG; actual shared-adapter store/LEA/RMW; checked producer exit/fresh output before dependent reads.',
 limits='Normal-return ABI; invalid list/allocator state, opaque callee effects, initialized object binding, native callback scheduling/cancellation/lifetime not established.',
 consumer='FABLE OV29/title lifetime; OPUS-owned exact contracts after independent review',cleanup='No game/process/input/native call/save/config/reference mutation')
with (W/'title-tracker-cleanup-method-01.json').open('x') as f:json.dump(method,f,indent=2)
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[x[:2] for x in frags]+[helper[0][:2]];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in frags+helper],verified_unwind_chains=chains,
 normal_cfg=dict(entry=hex(0x1fb660),end_exclusive=hex(0x1fb71c),reachable_instructions=len(seen),returns=[hex(x) for x in returns],opaque_calls=calls),
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits=method['limits'])
out.write_text(json.dumps(r,indent=2)+'\n');print('Captured complete normal tracker boundary and named registration helper; callee/scheduling effects still separate')
