"""Zero-return input-domain implication from existing original code, not samples."""
import hashlib,importlib.util,json,sys
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
  0x2ffd94:('mov','eax, 4'),0x2ffdad:('ret',''),0x2ffdbf:None,
  0x2ffd05:('mov','rdi, qword ptr [rdx + 0x698]'),0x2ffd02:('mov','rsi, rdx'),
  0x2ffe94:('xor','r8d, r8d'),0x2ffe97:('mov','rdx, rdi'),0x2ffe9a:('movzx','ecx, bx'),
  0x2ffe9d:('call','0x306480'),0x2ffebf:('mov','eax, 2'),0x2ffece:('ret','')}
 expected.pop(0x2ffdbf)  # No invented interior address is a witness.
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
 for pc in sorted(ix):
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access();written={i.reg_name(r) for r in wr}
  # Normal native ABI preserves these registers; local instructions must too.
  if 0x2ffd0c<pc<0x2ffd99 and written&{'rbx','ebx','bx','bl','bh'}:raise RuntimeError('action-word carrier changed')
  if 0x2ffd05<pc<=0x2ffe9d and written&{'rdi','edi','di','dil'}:raise RuntimeError('entry parsed-record carrier changed')
  if 0x2ffd94<pc<=0x2ffdad and written&{'rax','eax','ax','al','ah'}:raise RuntimeError('class-failure return4 overwritten')
  if 0x2ffebf<pc<=0x2ffece and written&{'rax','eax','ax','al','ah'}:raise RuntimeError('early return2 overwritten')
 return dict(complete_local_bytes=479,normal_returns=['0x2ffdad','0x2ffece'],
             implication='A normal EAX0 return requires class20 result nonzero for zero-extended low16(entryRCX); with the retained initialized count543 contract, id is0..542.',
             candidate_result='511..534 lie within0..542; this range gate cannot exclude them. This proves neither zero-result feasibility nor all-state admission.',
             later_category_arguments={'call':'0x2ffe9d','target':'0x306480','ECX':'zero-extended entryCX','RDX':'entry QWORD[incomingRDX+698] preserved inRDI','R8D':0},
             pointer_limit='Later RSI+698 reloads do not change the retained RDI argument. Native ABI/normal returns, pointer lifetime, state/alias stability remain premises; no scheduling or actual mutation observed.')

out=Path(sys.argv[1]) if len(sys.argv)>1 else P/'result-01.json'
if out.exists():raise RuntimeError('immutable result exists')
pins=json.loads((P/'input-identities-01.json').read_text())['inputs']
for x in pins:
 if sha(P/x['path'])!=x['sha256']:raise RuntimeError('retained prerequisite changed '+x['path'])
V=load('reviewed_role_validator','validate-title-source-annotations.py');G=load('existing_original_cfg','prove-title-queue-consumption.py')
src=P/'retained/action-selector-local-exclusions/action-availability-gates-raw-01.json'
raw=json.loads(src.read_text());agreement=V.validate(raw)
ix={int(i['pc'],16):i for r in raw['ranges'] if int(r['start'],16)==0x2ffcf0 for i in r['instructions']}
if not ix:raise RuntimeError('required complete availability body missing')
facts=derive(ix,G)
prior=json.loads((P/'retained/ov42-class20-action-admission/class20-admission-result-01.json').read_text())
if prior.get('method') is None:raise RuntimeError('retained class20 contract missing')
result=dict(producer_complete=True,method='A retained original code/control-flow implication; no new capture, table census or native/live execution',
 driver_sha256=sha(Path(__file__)),exe_sha256=raw['exe_sha256'],source_pins=[dict(path=src.relative_to(P).as_posix(),sha256=sha(src))],
 annotation_prerequisites=[agreement],input_pins=pins,facts=facts,
 limits='Valid readable unit/parsed records/private frame, initialized and stable original table count543, original class20 contract, normal nonvolatile ABI/returns/no interference. No caller/natural state/zero-result feasibility/all producer/override writer/loader/I/O/owner/lifetime closure.',
 affected_claims=['OV42 candidate input-domain premise for2FFCF0 and30DB70','FABLE availability actor-pointer explanation','OPUS low16 argument and source-order contract'])
with out.open('x') as f:json.dump(result,f,indent=2)
print('PROVED retained original zero-return/class20 implication; candidate511..534 still not excluded by range alone')
