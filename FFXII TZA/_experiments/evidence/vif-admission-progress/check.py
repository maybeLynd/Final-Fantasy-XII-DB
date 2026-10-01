import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['method'].startswith('A exact') and s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert len(s['bodies'])==3
 assert {b['entry']:b['sha256'] for b in s['bodies']}=={
  '0x22c940':'1bffe5bb8147ab9ba75bc635bc24ce81496c1b4b4652815fa972f99e3956a472',
  '0x22c970':'6f08de7d67b7ead7557bb05c85f0a2fbe8b244a46514a37f151c19e3e19d41dd',
  '0x22bff0':'c88b16447482201c1627caf6e2ae1f61dbdcba1bb8f1ac9e2fd1f6f0252890ce'}
 x={int(i['pc'],16):i for b in s['bodies'] for i in b['instructions']}
 for b in s['bodies']:
  data=bytes.fromhex(b['raw_hex']);assert sha(data)==b['sha256'] and len(data)==b['size']
  at=int(b['entry'],16)
  for i in b['instructions']:
   ib=bytes.fromhex(i['bytes']);assert int(i['pc'],16)==at
   assert data[at-int(b['entry'],16):at-int(b['entry'],16)+len(ib)]==ib;at+=len(ib)
  assert at==int(b['entry'],16)+b['size'] and b['instructions'][-1]['op']=='ret'
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 # Wrapper forwards supplied edx as decoder byte length; no content admission in this call-free prefix.
 ins(0x22C954,'mov','r8d, edx');ins(0x22C957,'mov','rdx, rcx');ins(0x22C961,'call','0x22c970')
 prefix=[i for a,i in x.items() if 0x22C940<=a<0x22C961]
 assert not any(i['op'].startswith('j') or i['op']=='call' for i in prefix)
 # At positive entry the index is zero; first payload/header load is before the only loop budget compare.
 ins(0x22C981,'xor','edi, edi');ins(0x22C986,'mov','r12d, r8d')
 ins(0x22C98C,'test','r8d, r8d');ins(0x22C98F,'jle','0x22cb78')
 path=[i for a,i in x.items() if 0x22C995<=a<0x22C9D6]
 assert not any(i['op'].startswith('j') or i['op']=='call' for i in path)
 ins(0x22C9D0,'movsxd','rax, edi');ins(0x22C9D3,'add','edi, 4')
 ins(0x22C9D6,'mov','ebx, dword ptr [rax + rbp]')
 ins(0x22CB55,'cmp','edi, r12d');ins(0x22CB58,'jl','0x22c9d0')
 ins(0x22CAC7,'call','0x22bff0');ins(0x22CACC,'add','edi, eax')
 # Positive NUM, V4-32 path; WL0 is admitted because WL>CL is the only initial compare.
 ins(0x22C00A,'cmp','r11d, edi');ins(0x22C00D,'jg','0x22c8c2')
 ins(0x22C01C,'xor','ebx, ebx');ins(0x22C608,'test','r13d, r13d');ins(0x22C60B,'jle','0x22c89e')
 ins(0x22C611,'shl','edi, 4');ins(0x22C614,'mov','ecx, r11d');ins(0x22C617,'shl','ecx, 4')
 ins(0x22C61A,'mov','esi, r11d');ins(0x22C61D,'movsxd','rbp, edi');ins(0x22C620,'neg','esi')
 ins(0x22C622,'movsxd','r14, ecx');ins(0x22C625,'mov','edi, r13d')
 ins(0x22C630,'cmp','edi, r11d');ins(0x22C633,'mov','ecx, edi');ins(0x22C635,'cmovg','ecx, r11d')
 ins(0x22C639,'movsxd','r9, ecx');ins(0x22C63C,'test','ecx, ecx');ins(0x22C63E,'jle','0x22c678')
 ins(0x22C678,'add','r10, rbp');ins(0x22C67B,'add','rax, r14')
 ins(0x22C67E,'add','ebx, r11d');ins(0x22C681,'add','edi, esi')
 ins(0x22C683,'cmp','ebx, r13d');ins(0x22C686,'jl','0x22c630')
 skipped=[i for a,i in x.items() if 0x22C640<=a<0x22C678]
 assert sum(i['op']=='mov' and i['args'].startswith('dword ptr') for i in skipped)==4
 chosen=[i for a,i in x.items() if 0x22C630<=a<=0x22C63E or 0x22C678<=a<=0x22C686]
 assert not any(i['op']=='call' or ('ptr [' in i['args']) for i in chosen)
 assert sha((HERE/'retained'/'existing-reader.py').read_bytes())==s['reader_sha256']
 assert sha((HERE/'retained'/'consumer-preimage.md').read_bytes())==s['consumer']['sha256']
 return {'evidence_class':'STATIC ORIGINAL-CODE DERIVATION, not execution',
  'packet_length':'signed byte count gates entry and continuation, not first four-byte header access or UNPACK payload admission',
  'positive_short_length':'1,2,3 all reach first four-byte header read under the same positive-entry path',
  'unpack_length':'decoder does not pass remaining byte budget to UNPACK; returned EAX advances index',
  'zero_write_cycle':'For V4-32/NUM>0, WL=CL0 passes initial comparison, chooses inner count0, skips all source/destination traffic, increments counters/pointers by0 and returns to same loop; no normal return on that path.',
  'progress_control':'WL=CL1 makes the admitted inner count1 and increments processed EBX by1; this is a static counterfactual against the zero-progress derivation, not a new execution.',
  'limits':'Selected V4-32 zero-cycle proof only. Supplied state, no live/default initialization, authored reachability, crash, negative-length payload use or all-format universal.'}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s);controls=[]
 def reject(name,mut):
  q=copy.deepcopy(s);mut(q)
  try:derive(q)
  except (AssertionError,KeyError,ValueError):controls.append({'name':name,'rejected':True});return
  raise AssertionError('INVALID_CONTROL '+name)
 def change(q,pc,op,args):
  for b in q['bodies']:
   for i in b['instructions']:
    if i['pc']==hex(pc):i['op']=op;i['args']=args;return
 reject('counter-update-now-progresses',lambda q:change(q,0x22C67E,'add','ebx, 1'))
 reject('before-header-admission-inserted',lambda q:change(q,0x22C9D3,'cmp','r12d, 4'))
 reject('remaining-budget-now-passed',lambda q:change(q,0x22CACC,'sub','r12d, eax'))
 reject('zero-cycle-branch-now-exits',lambda q:change(q,0x22C63E,'jle','0x22c89e'))
 reject('zero-body-qualification',lambda q:q.update(bodies=[]))
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','class':'Static byte/flow qualification with five corrupted-analysis controls; no native test count','controls':controls},indent=2)+'\n')
 print('PASS static original-flow derivation and five counterfactual rejection controls; no code execution.')
if __name__=='__main__':main()
