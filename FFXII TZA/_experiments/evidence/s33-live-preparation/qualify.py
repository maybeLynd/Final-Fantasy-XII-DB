"""Original source/address preflight, never a live pickup measurement."""
import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent
def qualify(r):
 assert r['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);d={}
 for b in r['bodies']:
  raw=bytes.fromhex(b['hex']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
  ins=list(md.disasm(raw,int(b['address'],16)));assert sum(i.size for i in ins)==len(raw)
  assert [{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]==b['instructions']
  d.update({i.address:(i.mnemonic,i.op_str) for i in ins})
 expected={0x3fa193:('mov','rsi, rcx'),0x3fa387:('xor','edi, edi'),0x3fa39e:('lea','rbx, [rsi + 0x270]'),
  0x3fa3a5:('test','byte ptr [rbx + 0x272], 1'),0x3fa3ae:('inc','edi'),
  0x3fa3b0:('add','rbx, 0x2a0'),0x3fa3b7:('cmp','edi, 0xd'),
  0x3fa3ba:('jb','0x3fa3a5'),0x3fa3bc:('xor','eax, eax'),
  0x3fa730:('test','byte ptr [rdx + 0x272], 1'),
  0x3fa759:('mov','eax, dword ptr [rdx + 0x260]'),
  0x3fa7af:('xor','esi, esi'),0x3fa7b8:('cmp','dword ptr [rdx + 0x260], esi'),
  0x3fa7be:('jne','0x3fa7cf'),
  0x3fa7c3:('mov','word ptr [rdx + 0x272], si'),
  0x3fa7f3:('call','0x3fc510')}
 for a,v in expected.items():assert d[a]==v,hex(a)
 store=bytes.fromhex(r['handle_store_319E05']['hex']);i=next(md.disasm(store,0x319e05));assert (i.mnemonic,i.op_str)==('mov','dword ptr [rbx + 0x58], eax')
 return {'result':'PASS_ADDRESS_PREPARATION_ONLY','method':'A static original code; no B rerun or C capture',
  'relative_slot_map':[{'index':k,'record_from_subobject':0x270+k*0x2a0,'flag_from_subobject':0x270+k*0x2a0+0x272,'phase_from_subobject':0x270+k*0x2a0+0x260} for k in range(13)],
  'conclusion':'Requested flag formula is correct conditional on an actual validated manager/subobject. The two270/272 terms are record-base and member offsets, not accidental double counting.',
  'handle':'CREATE stores low32 pointer bits; lookup reads bit0 at handle+272 before linked-list membership test and returns phase+260 when matched.',
  'ordering':'This UPDATE body clears phase0 flags in its first traversal, before its second traversal calls3FC510. Effects of that callee and other writers not newly proven.',
  'live_unknowns':['actual initialized manager/slot identities and placement','real update/frame cadence','normal drop/retirement interleaving','ordinary exhaustion or observed consequence'],
  'limits':'Relative source/address qualification. No actual pointers, frames, timing, initialization, callbacks, native effects, input or crash observed.'}
def main():
 r=json.loads((HERE/'reference.json').read_text());o=qualify(r);tests=[]
 def reject(name,f):
  try:f()
  except AssertionError:tests.append({'name':name,'rejected':True})
  else:raise AssertionError('bad preflight accepted '+name)
 q=copy.deepcopy(r);q['exe_sha256']='0'*64;reject('wrong binary identity',lambda:qualify(q))
 q=copy.deepcopy(r);q['handle_store_319E05']['hex']='894b58';reject('wrong handle source register',lambda:qualify(q))
 q=copy.deepcopy(r);q['bodies'][0]['instructions'][0]['args']='fake';reject('decode not backed by bytes',lambda:qualify(q))
 assert o['relative_slot_map'][0]['flag_from_subobject']==0x4e2 and o['relative_slot_map'][-1]['flag_from_subobject']==0x2462
 (HERE/'observation.json').write_text(json.dumps(o,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'result':'PASS_PREPARATION_ONLY','cases':len(tests),'controls':tests,'live_semantic_closure':[]},indent=2)+'\n')
 print('PASS',len(tests),'rejecting controls; flag formula confirmed, no live placement/cadence/crash result')
if __name__=='__main__':main()
