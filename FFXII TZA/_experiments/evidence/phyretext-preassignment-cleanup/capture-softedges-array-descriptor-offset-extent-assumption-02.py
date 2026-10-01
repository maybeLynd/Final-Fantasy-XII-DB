"""Named F4 prerequisite for the already selected CD14/NULL-cleanup question.

Method A: constructor, root getter and F4 recomputation distinguish the normal
registered descriptor from an arbitrary/rebound one. Capture compiler physical
spans only; normal coverage/callee effects must still be established in reduction.
No game, new fixture platform, class census or repeat of earlier captures.
"""
import hashlib,importlib.util,json,pathlib,struct,sys,capstone
from capstone.x86_const import X86_OP_IMM
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-array-descriptor-offset-code-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0]
targets={0x6373d0,0x632d80,0x63e410};rows=[];sections=[]
for i in range(n):
 q=p+24+o+40*i
 sections.append(struct.unpack_from('<IIII',d,q+8))
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000 in targets:rows.append((a+0x120000,b+0x120000,u+0x120000))
if len(rows)!=1 or rows[0][:2]!=(0x6373d0,0x637432):raise ValueError('exact normal root getter physical identity')
def read(a,z):
 for vs,va,rs,ro in sections:
  if 0x120000+va<=a and a+z<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+z]
 raise ValueError('unbacked exact source')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
leaves=[]
for start in (0x632d80,0x63e410):
 # A bounded diagnostic window supplies candidate instructions, but only the
 # complete normal reachable CFG defines the captured leaf. No first-RET or
 # first-padding heuristic receives semantic function credit.
 ix={}
 for ins in cs.disasm(read(start,512),start):
  if ins.mnemonic=='int3':break
  ix[ins.address]=ins
 todo=[start];seen=set();exits=[]
 while todo:
  a=todo.pop()
  if a in seen:continue
  if a not in ix:raise ValueError('leaf CFG leaves validated candidate instructions')
  seen.add(a);ins=ix[a]
  if ins.mnemonic=='ret':exits.append(a);continue
  if ins.mnemonic=='call':raise ValueError('claimed leaf calls another routine; revise boundary/method')
  if ins.mnemonic.startswith('j'):
   if len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM:raise ValueError('unresolved leaf tail target')
   todo.append(ins.operands[0].imm)
   if ins.mnemonic!='jmp':todo.append(a+ins.size)
  else:todo.append(a+ins.size)
 if not exits:raise ValueError('zero-return leaf is incomplete')
 end=max(a+ix[a].size for a in seen)
 if any(a not in seen and ix[a].mnemonic!='nop' for a in ix if start<=a<end):raise ValueError('unresolved internal leaf code')
 leaves.append(dict(start=start,end=end,normal_returns=exits,reachable_instructions=len(seen)))
if [(x['start'],x['end']) for x in leaves]!=[(0x632d80,0x632e77),(0x63e410,0x63e487)]:
 raise ValueError('derived exact leaf extent differs; preserve diagnostic and revise before capture')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[r[:2] for r in rows]+[(x['start'],x['end']) for x in leaves];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 verified_leaf_cfgs=leaves,
 question='Which normal root/constructor/F4 conditions justify CD14 clearing the same array+8 slot60EFE0 reads?',
 limits='Physical original prerequisite spans, not live registration state, arbitrary descriptor invariance, caller reachability or lazy-init side effects.')
out.write_text(json.dumps(r,indent=2)+'\n')
print('Captured named original descriptor-offset prerequisites; arrayF4/null-cleanup composition not yet accepted')
