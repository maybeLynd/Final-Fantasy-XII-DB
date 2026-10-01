import hashlib,json
from pathlib import Path
import capstone
from operand_direction import memory_role
W=Path(__file__).resolve().parent;s=json.loads((W/'source.json').read_text());raw=bytes.fromhex(s['raw_hex'])
assert len(raw)==418 and hashlib.sha256(raw).hexdigest()==s['sha256']=='32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a'
assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(raw,0x3D8E50));d={i.address:i for i in ii}
assert sum(i.size for i in ii)==418 and ii[-1].address==0x3D8FF1 and ii[-1].mnemonic=='ret'
assert d[0x3D8E5D].mnemonic=='ucomiss' and d[0x3D8E5D].op_str=='xmm0, xmm1'
assert d[0x3D8E60].mnemonic=='jp' and d[0x3D8E60].operands[0].imm==0x3D8E6C
assert d[0x3D8E62].mnemonic=='jne' and d[0x3D8E62].operands[0].imm==0x3D8E6C
assert d[0x3D8E6B].mnemonic=='ret'
assert [(i.address,i.operands[0].imm) for i in ii if i.mnemonic=='call']==[(0x3D8E78,0x36D930),(0x3D8FE2,0x36D8E0)]
for p in (0x3D8E8C,0x3D8F79):assert d[p].mnemonic=='test' and d[p].op_str=='r8d, r8d'
for p,target in ((0x3D8E8F,0x3D8F36),(0x3D8F7C,0x3D8FC6)):
 assert d[p].mnemonic=='je' and d[p].operands[0].imm==target
refs=[]
for i in ii:
 for k,o in enumerate(i.operands):
  if o.type==capstone.CS_OP_MEM and cs.reg_name(o.mem.base)=='rip':refs.append(dict(pc=hex(i.address),op=i.mnemonic,target=hex(i.address+i.size+o.mem.disp),width=o.size,capstone_access_flag=o.access,access=memory_role(i,k),operand=k))
assert refs==s['rip_references']
mode=[x for x in refs if x['target']=='0x22d9138'];assert len(mode)==1 and mode[0]['pc']=='0x3d8e7d' and mode[0]['access']=='read'
statewrites=[x for x in refs if x['target']=='0x1ef93e8' and x['access']=='write']
assert [x['pc'] for x in statewrites]==['0x3d8f26','0x3d8fb8']
assert all(0x3D8E8F<int(x['pc'],16)<0x3D8F36 or 0x3D8F7C<int(x['pc'],16)<0x3D8FC6 for x in statewrites)
assert not any(i.mnemonic=='call' for i in ii if 0x3D8E7D<i.address<0x3D8FE2)
# Original unrolled source blocks have five then two recurrence operations.
# Count the independently identifying mask/shift/bit-extract triples, not stores.
for lo,hi,n in ((0x3D8E95,0x3D8F26,5),(0x3D8F7E,0x3D8FB8,2)):
 block=[i for i in ii if lo<=i.address<hi]
 def imm_count(op,val):return sum(i.mnemonic==op and len(i.operands)==2 and i.operands[1].type==capstone.CS_OP_IMM and i.operands[1].imm==val for i in block)
 assert imm_count('shr',18)==n and imm_count('shr',4)==n
 assert imm_count('and',0x3FFFFF)==n and imm_count('or',0x1FC00000)==n and imm_count('and',1)==n
 assert not any(i.mnemonic.startswith('j') or i.mnemonic=='call' for i in block)
scratch=[x['pc'] for x in refs if x['access']=='write' and x['target']!='0x1ef93e8']
assert scratch==['0x3d8f44','0x3d8f56','0x3d8f65','0x3d8f71','0x3d8fcd','0x3d8fd5']
assert all(int(x,16)>=0x3D8F3F for x in scratch)
# Disabled gates join these own-body writes; zero amplitude returned before both
# native boundaries. No whole-invocation state safety inferred for native callees.
v=dict(status='PASS_STATIC_ONLY',zero_ordered_amplitude='Early return before calls/global state/scratch writes; unordered takes JP instead.',
 mode='Read once after first native call, latched R8D reused for both own recurrence gates. Zero skips5+2 blocks; any nonzero includes them.',
 direct_recurrence_steps=dict(zero_amplitude=0,mode_zero_nonzero_amplitude=0,mode_nonzero_nonzero_amplitude=7),
 direct_state_write_pcs=[x['pc'] for x in statewrites],scratch_write_pcs=scratch,
 calls=s['calls'],new_original_code_executions=0,live_cases=0,
 limits='A direct original-body proof. Native save/restore-call effects not executed/assumed inert; actual invocation state/caller ordering unobserved. 14/28-step composition needs enabled mode at each latch and separately justified callee/caller effects. Disabled nonzero is not no-op.',
 access_fix='Packed MOVUPS memory destination WRITE and LEA address-only, raw unreliable provider flags retained separately. Additive19 correction, not rewrite of published source. Byte-based19 copy/alias proof unaffected.')
if (W/'manifest.json').exists():assert json.loads((W/'validation.json').read_text())==v
else:(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS A: zero versus unordered amplitude, latched-mode0 skips direct5+2/state stores, scratch/calls retained. No native-call effect or live total guarantee.',flush=True)
