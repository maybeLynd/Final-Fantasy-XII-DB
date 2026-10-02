"""Zero-return input-domain implication from existing original code, not samples."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,f):
 s=importlib.util.spec_from_file_location(name,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 expected={0x2ffd0c:('movzx','ebx, cx'),0x2ffd75:('mov','r8d, 1'),
  0x2ffd80:('movzx','r14d, bx'),0x2ffd84:('mov','edx, r14d'),0x2ffd87:('lea','ecx, [r8 + 0x13]'),
  0x2ffd8b:('call','0x322c50'),0x2ffd90:('test','eax, eax'),0x2ffd92:('jne','0x2ffdae'),
  0x2ffd94:('mov','eax, 4'),0x2ffdad:('ret',''),
  0x2ffd05:('mov','rdi, qword ptr [rdx + 0x698]'),0x2ffd02:('mov','rsi, rdx'),
  0x2ffe94:('xor','r8d, r8d'),0x2ffe97:('mov','rdx, rdi'),0x2ffe9a:('movzx','ecx, bx'),
  0x2ffe9d:('call','0x306480'),0x2ffebf:('mov','eax, 2'),0x2ffece:('ret','')}
 for pc,op in expected.items():
  if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=op:raise RuntimeError('availability source witness changed '+hex(pc))
 whole=G.graph(ix,0x2ffcf0,0x2ffecf)
 if whole['visited']!=set(ix) or set(whole['returns'])!={0x2ffdad,0x2ffece}:raise RuntimeError('complete local availability CFG required')
 if not G.dominates(whole,0x2ffd8b,0x2ffdad):raise RuntimeError('class query bypass to normal reason exit')
 if not G.dominates(whole,0x2ffebf,0x2ffece):raise RuntimeError('early exit is not constant2')
 failed=G.graph(ix,0x2ffd92,0x2ffecf,fixed={0x2ffd92:False})
 if set(failed['returns'])!={0x2ffdad} or failed['calls'] or not G.dominates(failed,0x2ffd94,0x2ffdad):raise RuntimeError('failed class query must return4')
 if not G.dominates(whole,0x2ffd75,0x2ffd8b) or not G.dominates(whole,0x2ffd80,0x2ffd8b):raise RuntimeError('class20 argument path changed')
 if not G.dominates(whole,0x2ffd05,0x2ffe9d):raise RuntimeError('parsed-record carrier is not initialized')
 import capstone
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 def before(definition,target):
  if not G.dominates(whole,definition,target):raise RuntimeError('carrier definition does not dominate use')
  reverse={pc:set() for pc in ix}
  for pc,targets in whole['edges'].items():
   for t in targets:reverse[t].add(pc)
  todo=[target];seen=set()
  while todo:
   pc=todo.pop()
   if pc in seen or pc==definition:continue
   seen.add(pc);todo.extend(reverse[pc])
  return seen-{target}
 action_sites=before(0x2ffd0c,0x2ffd80)|before(0x2ffd0c,0x2ffe9a)
 record_sites=before(0x2ffd05,0x2ffe97)
 for pc in sorted(ix):
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access();written={i.reg_name(r) for r in wr}
  # Normal native ABI preserves these registers; local instructions must too.
  if pc in action_sites and written&{'rbx','ebx','bx','bl','bh'}:raise RuntimeError('action-word carrier changed')
  if pc in record_sites and written&{'rdi','edi','di','dil'}:raise RuntimeError('entry parsed-record carrier changed')
  if 0x2ffd94<pc<=0x2ffdad and written&{'rax','eax','ax','al','ah'}:raise RuntimeError('class-failure return4 overwritten')
  if 0x2ffebf<pc<=0x2ffece and written&{'rax','eax','ax','al','ah'}:raise RuntimeError('early return2 overwritten')
 return dict(complete_local_bytes=479,normal_returns=['0x2ffdad','0x2ffece'],
             implication='A normal EAX0 return requires class20 result nonzero for zero-extended low16(entryRCX); with the retained initialized count543 contract, id is0..542.',
             candidate_result='511..534 lie within0..542; this range gate cannot exclude them. This proves neither zero-result feasibility nor all-state admission.',
             later_category_arguments={'call':'0x2ffe9d','target':'0x306480','ECX':'zero-extended entryCX','RDX':'entry QWORD[incomingRDX+698] preserved inRDI','R8D':0},
             pointer_limit='Later RSI+698 reloads do not change the retained RDI argument. Native ABI/normal returns, pointer lifetime, state/alias stability remain premises; no scheduling or actual mutation observed.')

out=Path(sys.argv[1]) if len(sys.argv)>1 else P/'result-01.json'
if out.exists():raise RuntimeError('immutable result exists')
pins=json.loads((P/'input-identities-02.json').read_text())['inputs']
for x in pins:
 if sha(P/x['path'])!=x['sha256']:raise RuntimeError('retained prerequisite changed '+x['path'])
V=load('reviewed_role_validator','validate-title-source-annotations.py');G=load('existing_original_cfg','prove_owner_reload_order.py')
if not callable(getattr(G,'graph',None)) or not callable(getattr(G,'dominates',None)):raise RuntimeError('required actual CFG prerequisite unavailable')
src=P/'retained/action-selector-local-exclusions/action-availability-gates-raw-01.json'
raw=json.loads(src.read_text());agreement=V.validate(raw)
ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
image=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(image).hexdigest()!=raw['exe_sha256']:raise RuntimeError('shipping EXE changed')
pe=struct.unpack_from('<I',image,0x3c)[0];nsec=struct.unpack_from('<H',image,pe+6)[0];opt=struct.unpack_from('<H',image,pe+20)[0]
sections=[struct.unpack_from('<IIII',image,pe+24+opt+i*40+8) for i in range(nsec)]
def original(pc,n):
 for vs,va,rs,ro in sections:
  if 0x120000+va<=pc and pc+n<=0x120000+va+rs:return image[ro+pc-0x120000-va:ro+pc-0x120000-va+n]
 raise RuntimeError('original range is not file-backed')
for r in raw['ranges']:
 blob=bytes.fromhex(''.join(x['bytes'] for x in r['instructions']))
 if blob!=original(int(r['start'],16),len(blob)):raise RuntimeError('retained bytes differ from original image')
ix={int(i['pc'],16):i for r in raw['ranges'] if int(r['start'],16)==0x2ffcf0 for i in r['instructions']}
if not ix:raise RuntimeError('required complete availability body missing')
facts=derive(ix,G)
prior=json.loads((P/'retained/ov42-class20-action-admission/class20-admission-result-01.json').read_text())
classsrc=P/'retained/ov42-class20-action-admission/action-admission-guards-raw-01.json'
classraw=json.loads(classsrc.read_text());class_agreement=V.validate(classraw)
if (prior.get('initialized_count_premise')!=543 or prior.get('accepted_ids')!=[0,542] or prior.get('rejected_ids')!=[543,65535]
 or prior.get('raw_sha256')!=sha(classsrc) or prior.get('driver_sha256')!=sha(P/'retained/ov42-class20-action-admission/prove-class20-admission.py')):
 raise RuntimeError('retained original class20 contract/pins incomplete')
classix={int(i['pc'],16):i for r in classraw['ranges'] for i in r['instructions']}
# The supplied class20 arm and selected shared entry/return slices never read R8.
# Do not assume that of other classes. This avoids silently reusing an arm with
# a third-argument distinction when the present caller supplies R8D=1.
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
selected=[i for pc,i in classix.items() if 0x322c50<=pc<=0x322c7c or 0x322f72<=pc<=0x322f87 or 0x32302c<=pc<=0x323048 or 0x322c8d<=pc<=0x322c9e]
if not selected:raise RuntimeError('class20 selected source slices missing')
for rec in selected:
 pc=int(rec['pc'],16);b=bytes.fromhex(rec['bytes'])
 if b!=original(pc,len(b)):raise RuntimeError('class20 selected shipping bytes changed')
 i=next(cs.disasm(b,pc));rd,wr=i.regs_access()
 if {i.reg_name(q) for q in rd}&{'r8','r8d','r8w','r8b'}:raise RuntimeError('class20 selected arm depends on third argument')
result=dict(producer_complete=True,method='A retained original code/control-flow implication; no new capture, table census or native/live execution',
 driver_sha256=sha(Path(__file__)),exe_sha256=raw['exe_sha256'],source_pins=[dict(path=q.relative_to(P).as_posix(),sha256=sha(q)) for q in [src,classsrc]],
 annotation_prerequisites=[agreement,class_agreement],input_pins=pins,facts=facts,
 class20_argument_qualification='Current caller sets R8D1; selected original class20 entry/arm/shared return slices do not read R8. Other classes unproved.',
 limits='Valid readable unit/parsed records/private frame, initialized and stable original table count543, original class20 contract, normal nonvolatile ABI/returns/no interference. No caller/natural state/zero-result feasibility/all producer/override writer/loader/I/O/owner/lifetime closure.',
 affected_claims=['OV42 candidate input-domain premise for2FFCF0 and30DB70','FABLE availability actor-pointer explanation','OPUS low16 argument and source-order contract'])
with out.open('x') as f:json.dump(result,f,indent=2)
print('PROVED retained original zero-return/class20 implication; candidate511..534 still not excluded by range alone')
