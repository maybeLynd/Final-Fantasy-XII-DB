import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()

def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);x={}
 for b,(entry,end) in zip(s['bodies'],[(0x20F310,0x20F3D5),(0x1DB660,0x1DB7C6)],strict=True):
  raw=bytes.fromhex(b['raw_hex']);assert int(b['entry'],16)==entry and int(b['end'],16)==end
  assert len(raw)==b['size']==end-entry and sha(raw)==b['sha256']
  ii=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(raw,entry)]
  assert ii==b['instructions'] and sum(len(bytes.fromhex(i['bytes'])) for i in ii)==len(raw)
  x.update({int(i['pc'],16):i for i in ii})
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 ins(0x20F316,'cmp','byte ptr [rip + 0x1bf34a3], 0');assert 0x20F31D+0x1BF34A3==0x1E027C0
 ins(0x20F320,'jne','0x20f32d');ins(0x20F322,'mov','eax, 0x10');ins(0x20F32C,'ret','')
 ins(0x20F339,'xor','r10d, r10d');ins(0x20F33E,'lea','edi, [rax + 0x10]')
 ins(0x20F350,'mov','rax, qword ptr [r9]')
 for pc,op,args in [(0x20F35C,'shr','rbx, 0xf'),(0x20F360,'shr','rax, 0x3a'),(0x20F364,'and','ebx, 1'),
  (0x20F367,'shr','rcx, 0x3c'),(0x20F36B,'and','r8d, 0x7fff'),(0x20F372,'and','eax, 3'),
  (0x20F375,'movzx','r11d, cl'),(0x20F379,'test','cl, cl'),(0x20F37B,'cmove','r11d, edi'),
  (0x20F37F,'test','al, al'),(0x20F381,'jne','0x20f38f'),(0x20F383,'movzx','edx, r11b'),
  (0x20F387,'imul','edx, r8d'),(0x20F38B,'inc','edx'),(0x20F38D,'jmp','0x20f3b5'),
  (0x20F38F,'cmp','al, 1'),(0x20F391,'jne','0x20f3ab'),(0x20F393,'movzx','ecx, r11b'),
  (0x20F397,'imul','ecx, r8d'),(0x20F39B,'mov','eax, ecx'),(0x20F39D,'and','eax, 1'),
  (0x20F3A0,'add','eax, ecx'),(0x20F3A2,'lea','edx, [rax*8 + 0x10]'),(0x20F3A9,'jmp','0x20f3b8'),
  (0x20F3AB,'sub','al, 2'),(0x20F3AD,'cmp','al, 1'),(0x20F3AF,'ja','0x20f3b8'),
  (0x20F3B1,'lea','edx, [r8 + 1]'),(0x20F3B5,'shl','edx, 4'),(0x20F3B8,'add','r10d, edx'),
  (0x20F3BB,'cmp','bl, 1'),(0x20F3BE,'je','0x20f3c7'),(0x20F3C0,'mov','eax, edx'),
  (0x20F3C2,'add','r9, rax'),(0x20F3C5,'jmp','0x20f350'),(0x20F3C7,'mov','eax, r10d')]:ins(pc,op,args)
 h=s['bodies'][0]['instructions'];assert not any(i['op']=='call' for i in h)
 assert [i['pc'] for i in h if '[r9]' in i['args']]==['0x20f350']
 # No buffer end/length import or overflow conditional exists in the complete helper.
 branches={i['pc']:i['args'] for i in h if i['op'].startswith('j')}
 assert set(branches)=={'0x20f320','0x20f381','0x20f38d','0x20f391','0x20f3a9','0x20f3af','0x20f3be','0x20f3c5'}
 # Inspect all instructions between measurement and first copy, not just two isolated MOVs.
 expected=[('call','0x20f310'),('mov','rcx, qword ptr [rip + 0x1da766d]'),('mov','edx, eax'),
  ('mov','ebx, eax'),('call','0x1a1470'),('mov','r8d, ebx'),('mov','rdx, rdi'),
  ('mov','rcx, rax'),('mov','rsi, rax'),('call','0x861eba')]
 assert [(i['op'],i['args']) for i in s['bodies'][1]['instructions'] if 0x1DB687<=int(i['pc'],16)<=0x1DB6A8]==expected
 ins(0x1DB681,'mov','rcx, rdx');ins(0x1DB684,'mov','rdi, rdx')
 p=s['consumer'];b=(HERE/p['retained']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 # Arithmetic witnesses derived from the instructions above; not emulator/native cases.
 def declared_step(flg,nloop,nreg):
  nreg=16 if nreg==0 else nreg
  if flg==0:return (nreg*nloop+1)*16
  if flg==1:return (nreg*nloop+(nreg*nloop&1))*8+16
  return (nloop+1)*16
 small=[{'flg':f,'nloop':n,'nreg':r,'step':declared_step(f,n,r)} for f,n,r in [(0,0,0),(0,1,0),(1,3,1),(2,0,0),(3,32767,15)]]
 assert [a['step'] for a in small]==[16,272,48,16,524288]
 maximum=declared_step(0,32767,0);assert maximum==8388368 and maximum<2**32
 witnesses=[]
 for count in [256,257,512,513]:
  total=count*maximum;witnesses.append({'maximum_packed_tags':count,'declared_total':total,'returned_u32':total&0xFFFFFFFF,
   'last_header_offset':(count-1)*maximum,'final_tag_eop':1,'class':'symbolic declared layout only; not allocated, read or executed'})
 tail=declared_step(2,7679,0);exact=512*maximum+tail
 assert exact==2**32 and tail==122880
 zero={'maximum_packed_nonfinal_tags':512,'final_image_nloop':7679,'final_image_step':tail,
  'declared_total':exact,'returned_u32':0,'last_header_offset':512*maximum,'final_tag_eop':1,
  'class':'symbolic declared layout only; helper reads headers, not all payload bytes'}
 return {'method':'A — static original instructions and mathematical boundary witnesses',
  'established':['Gate zero returns16 before any packet header read. Enabled helper reads one8-byte header at each computed position.',
   'NREG0 maps16, FLG is masked0..3; each individual step is positive, <=8388368 and fitsu32.',
   'R10D accumulation is modulo2^32. Nonfinal pointer advance uses zeroextended individual EDX then ADD R9,RAX; it is not advanced by the wrapped total.',
   'EOP includes final tag size in total then returns; no final pointer advance or final payload read occurs.',
   'No caller-supplied length/end or total-overflow rejection exists in this complete helper.',
   'Collector passes zeroextended return via EDX to001A1470 and savedEBX via R8D to00861EBA; no intervening size/overflow guard before these calls.'],
  'small_positive_arithmetic_witnesses':small,'max_single_step':maximum,'accumulation_witnesses':witnesses,'exact_zero_witness':zero,
  'semantic_implication':'To use the enabled return as the full declared copied extent, the reachable sequence must terminate at EOP, have readable computed headers and backing source extent, and a declared total <2^32 (plus valid pointer arithmetic). Otherwise the local result alone does not establish those properties.',
  'consumer_changes_enabled':'Qualify helper return asu32 modulo total and no length guard; collector uses its zeroextended value. Existing documented GIF formulas remain correct. Route actual producer/caller constraints separately if claimed.',
  'unresolved':['Actual authored packet bounds and proof that normal producers meet them.','Allocator/memcpy semantics, zero-size allocation result, subsequent replay and any actual failure.','Normal call reachability, initialization of01E027C0, lifetime and rendered consequences.'],
  'not_claimed':'No shipped oversized packet, infinite live loop, allocation/null fault, complete payload read, game crash, or universal unsafe caller.',
  'propagation':'PENDING independent review and FABLE/OPUS canonical incorporation','limits':s['limits']}

def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s)
 # Source/interpretation sensitivity checks; not runtime fault injection or mutation-campaign pass.
 controls=[]
 for name,pc,args in [('widened-accumulator-description',0x20F3B8,'r10, rdx'),('signed-copy-length-description',0x1DB69C,'r8, ebx')]:
  q=copy.deepcopy(s)
  for b in q['bodies']:
   for i in b['instructions']:
    if i['pc']==hex(pc):i['args']=args
  try:derive(q)
  except AssertionError:controls.append({'name':name,'rejected':True});continue
  raise AssertionError('INVALID_CONTROL '+name)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_STATIC_ONLY','source_bodies':2,'symbolic_only':True,
  'native_or_live_cases':0,'controls':controls,'limits':'Byte/flow qualification and arithmetic witnesses, no native/guest/live or full campaign acceptance.'},indent=2)+'\n')
 print('PASS_STATIC_ONLY: originalu32 accumulation/u64 pointer step/zeroextended caller length; no native or live cases accepted.')
if __name__=='__main__':main()
