"""Finite original copy-address proof. No machine-code execution or gameplay."""
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
required_ranges=[('0x30eda0','0x30ee9a'),('0x30eff0','0x30f121'),('0x30dfa0','0x30e010')]
if[(r['start'],r['end_exclusive']) for r in x['ranges']]!=required_ranges:raise RuntimeError('required source population changed')
ix={};graphs=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b)
 if set(local)!=g['visited']:raise RuntimeError('unaccounted source instructions')
 graphs.append({'entry':hex(a),'visited':len(g['visited']),'returns':[hex(t) for t in g['returns']],'calls':g['calls']})
req=[(0x30eda0,'mov','r8, qword ptr [rcx + 0xb88]'),(0x30eda7,'add','rcx, 0x6b0'),(0x30edae,'mov','rax, r8'),(0x30edb1,'mov','edx, 9'),(0x30edb6,'lea','rcx, [rcx + 0x80]'),(0x30edc7,'movups','xmmword ptr [rcx - 0x80], xmm0'),(0x30ee03,'sub','rdx, 1'),(0x30ee07,'jne','0x30edb6'),(0x30ee0c,'lea','r9, [rip + 0x1fb01ad]'),(0x30ee5d,'cmp','r8, rdx'),(0x30ee60,'je','0x30ee6f'),(0x30ee64,'cmp','eax, 8'),(0x30ee8f,'btr','ecx, eax'),(0x30ee97,'mov','byte ptr [rdx], cl'),
 (0x30f047,'mov','rcx, rdi'),(0x30f04a,'lea','rax, [rbx + 0x6b0]'),(0x30f051,'mov','edx, 9'),(0x30f056,'lea','rcx, [rcx + 0x80]'),(0x30f067,'movups','xmmword ptr [rcx - 0x80], xmm0'),(0x30f0a3,'sub','rdx, 1'),(0x30f0a7,'jne','0x30f056'),(0x30f0ac,'mov','r8d, 0x4f0'),(0x30f0e5,'lea','rcx, [rbx + 0x6b0]'),(0x30f0ec,'call','0x861ec0'),(0x30f0f1,'mov','qword ptr [rbx + 0xb88], rdi'),
 (0x30dfe3,'cmp','eax, 8'),(0x30dff3,'bts','ecx, r10d'),(0x30dff7,'mov','byte ptr [rdx + r11], cl'),(0x30dffe,'imul','rax, rcx, 0x4f0')]
for pc,m,a in req:
 if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required operation changed '+hex(pc))

# Addresses only: interpret the certified finite movups/lea copy forms, not
# native callees, injected memory, x86 state, or a reconstructed gameplay model.
import capstone
from capstone.x86_const import X86_OP_MEM,X86_OP_REG
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def footprint(loop,end,tail,last,src0,dst0):
 regs={'rax':src0,'rcx':dst0};xmm={};pairs=[];operations=[]
 def memaddr(ins,op):
  if op.type!=X86_OP_MEM or op.mem.index!=0:raise RuntimeError('unmodeled indexed copy')
  name=ins.reg_name(op.mem.base)
  if name not in regs:raise RuntimeError('unknown copy address')
  kind,k=regs[name];return kind,k+op.mem.disp
 def step(pc):
  rec=ix[pc];ins=next(cs.disasm(bytes.fromhex(rec['bytes']),pc));m=ins.mnemonic
  if m=='lea' and ins.reg_name(ins.operands[0].reg) in regs:
   regs[ins.reg_name(ins.operands[0].reg)]=memaddr(ins,ins.operands[1])
  elif m=='movups':
   a,b=ins.operands
   if a.type==X86_OP_REG and b.type==X86_OP_MEM:
    key=ins.reg_name(a.reg);xmm[key]=memaddr(ins,b);operations.append((hex(pc),'read',xmm[key]))
   elif a.type==X86_OP_MEM and b.type==X86_OP_REG:
    key=ins.reg_name(b.reg)
    if key not in xmm:raise RuntimeError('uninitialized vector carrier')
    dest=memaddr(ins,a);pairs.append({'read_origin':xmm[key][0],'read_offset':xmm[key][1],'write_origin':dest[0],'write_offset':dest[1],'bytes':16,'store':hex(pc)})
    operations.append((hex(pc),'write',dest))
   else:raise RuntimeError('unmodeled copy form')
  elif m in ['mov','xor','lea']:
   # Tail setup for R8/R9 or EAX after the final source load. None is
   # consulted as a copy address later; invalidate EAX's enclosing RAX.
   if ins.operands and ins.operands[0].type==X86_OP_REG and ins.reg_name(ins.operands[0].reg)=='eax':regs.pop('rax',None)
  else:raise RuntimeError('unmodeled copy instruction '+hex(pc))
 for _ in range(9):
  for pc in sorted(p for p in ix if loop<=p<end):step(pc)
 for pc in sorted(p for p in ix if tail<=p<=last):step(pc)
 offsets=[p['read_offset']-src0[1] for p in pairs]
 if offsets!=list(range(0,0x4f0,16)) or [p['write_offset']-dst0[1] for p in pairs]!=offsets:raise RuntimeError('copy coverage/order changed')
 if len(pairs)!=79 or any(p['read_origin']!=src0[0] or p['write_origin']!=dst0[0] for p in pairs):raise RuntimeError('copy population/origin changed')
 return {'source_start':src0,'destination_start':dst0,'bytes':0x4f0,'vector_pairs':len(pairs),'first':pairs[0],'last':pairs[-1],'pairs':pairs,'operation_count':len(operations)}
restore=footprint(0x30edb6,0x30ee03,0x30ee09,0x30ee44,('saved_slot',0),('unit',0x6b0))
snapshot=footprint(0x30f056,0x30f0a3,0x30f0a9,0x30f0e1,('unit',0x6b0),('saved_slot',0))
# The incoming source stays in nonvolatile-by-code R8 (this leaf does not call),
# even though the copy overwrites the unit's B88 pointer from source offset4D8.
after=[i for pc,i in ix.items() if 0x30eda0<pc<0x30ee5d]
for i in after:
 ins=next(cs.disasm(bytes.fromhex(i['bytes']),int(i['pc'],16)))
 _,writes=ins.regs_access()
 if any(ins.reg_name(r) in ['r8','r8d','r8w','r8b'] for r in writes):raise RuntimeError('incoming source pointer carrier overwritten')
assert 0x6b0+0x4f0==0xba0 and 0x714-0x6b0==0x64 and 0xb88-0x6b0==0x4d8
release=[{'slot':i,'pointer':'022BEFC0+'+hex(i*0x4f0),'bitmap_byte':'022BEFB0','bit':i} for i in range(8)]
result={'producer_complete':True,'method':'A STATIC_ONLY original finite copy-address proof',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],
 'annotation_prerequisites':[roles],'instruction_assertions':len(req),'graphs':graphs,
 'restore':restore,'snapshot':snapshot,
 'answer':'Both copies cover unit[6B0,BA0), not [730,C20). Restore includes phase6B4, current714 and B88; bitmap release compares original incoming source R8 despite overwritten B88.',
 'fields':[{'unit_offset':'0x6b4','saved_offset':'0x4','meaning':'phase'}, {'unit_offset':'0x714','saved_offset':'0x64','meaning':'current action'}, {'unit_offset':'0xb88','saved_offset':'0x4d8','meaning':'saved pointer field'}],
 'release_pointer':'R8 loaded at30EDA0 before any copy, not rewritten before30EE5D; fieldB88 contents may differ after the copy. Actual paired slot match clears its bitmap bit, no match still returns1.',
 'release_slots':release,
 'snapshot_order':'Allocate slot, copy current block, call memset(unit+6B0,0,4F0) with RDX decremented to0, then set B88 to allocated RDI. No slot 694/695/696 is in the copied range.',
 'limitations':['Address/order proof only, no native/emulated original-code execution or live observation',
  'Copy-source and unit destination must be mapped valid disjoint 4F0-byte buffers; arbitrary overlaps are not proven safe',
  'Snapshot allocator/native memset normal return and memory validity are assumptions, not stub-established effects',
  'Restored B88 is saved content, not automatically null; neither unique ownership, nesting, reuse safety nor scheduler ordering is established',
  'EXP091 prior85cases/mutations belong to ORACLE, not this package; known consumers require additive correction and a copy-origin producer regression']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED original restore/snapshot origin6B0, exact4F0 footprint and incoming release pointer; no native/game')
