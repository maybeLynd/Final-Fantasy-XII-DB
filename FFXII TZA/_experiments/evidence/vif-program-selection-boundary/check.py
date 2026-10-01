import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);x={}
 for k,n in [('decoder',533),('reset',11),('flush',85)]:
  b=s[k];raw=bytes.fromhex(b['raw_hex']);assert b['size']==n and len(raw)==n and sha(raw)==b['sha256']
  ii=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(raw,int(b['entry'],16))]
  assert ii==b['instructions'] and sum(len(bytes.fromhex(i['bytes'])) for i in ii)==n
  x.update({int(i['pc'],16):i for i in ii})
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 ins(0x22C930,'mov','dword ptr [rip + 0x1e5c50a], 0');assert 0x22C93A+0x1E5C50A==0x2088E44
 ins(0x22C93A,'ret','');assert len(s['reset']['instructions'])==2
 flush=s['flush']['instructions'];assert sum(i['op']=='ret' for i in flush)==2
 ins(0x22C8E8,'je','0x22c904');assert not any(i['op']=='call' or 'esi' in i['args'] or 'rsi' in i['args'] for i in flush)
 # Flush only has these five store sites, all16-bit state words; no installed count/list/program-table store.
 stores=[i for i in flush if i['op']=='mov' and i['args'].startswith('word ptr')]
 assert {i['pc'] for i in stores}=={'0x22c8de','0x22c8f5','0x22c8fc','0x22c916','0x22c91d'}
 for pc,args,target in [(0x22C8DE,'word ptr [rip + 0x1e38537], ax',0x2064E1C),(0x22C8F5,'word ptr [rip + 0x1e5c53c], cx',0x2088E38),
  (0x22C8FC,'word ptr [rip + 0x1e38525], ax',0x2064E28),(0x22C916,'word ptr [rip + 0x1e3850b], ax',0x2064E28),(0x22C91D,'word ptr [rip + 0x1e5c514], cx',0x2088E38)]:
  ins(pc,'mov',args);disp=int(args.split('0x')[1].split(']')[0],16)
  assert pc+len(bytes.fromhex(x[pc]['bytes']))+disp==target
 ins(0x22C9AB,'mov','esi, dword ptr [rip + 0x1e5c493]');assert 0x22C9B1+0x1E5C493==0x2088E44
 ins(0x22C9D6,'mov','ebx, dword ptr [rax + rbp]')
 ins(0x22CA45,'movzx','ecx, bx');ins(0x22CA4F,'mov','qword ptr [r9 + rcx*8], rax');ins(0x22CA60,'mov','dword ptr [rdx + rax*4], ecx')
 ins(0x22CAD8,'call','0x22c8d0');ins(0x22CADD,'xor','eax, eax');ins(0x22CADF,'movzx','r8d, bx')
 ins(0x22CAE3,'test','esi, esi');ins(0x22CAE5,'je','0x22cb0e')
 ins(0x22CAF1,'mov','ecx, dword ptr [rdx]');ins(0x22CAF3,'cmp','r8d, ecx');ins(0x22CAF6,'jb','0x22cafd')
 ins(0x22CAF8,'cmp','ecx, eax');ins(0x22CAFA,'cmovae','eax, ecx');ins(0x22CB05,'jne','0x22caf1')
 ins(0x22CB07,'cmp','eax, 0x10000');ins(0x22CB0C,'je','0x22cb41');ins(0x22CB0E,'mov','r9d, eax')
 ins(0x22CB17,'lea','rax, [rip + 0x1e3c312]');assert 0x22CB1E+0x1E3C312==0x2068E30
 ins(0x22CB1E,'call','qword ptr [rax + r9*8]')
 for p in s['refs']:
  data=(HERE/p['retained']).read_bytes();assert len(data)==p['bytes'] and sha(data)==p['sha256']
 assert sha((HERE/'retained'/'type-rows.tsv').read_bytes())==s['type_source']['selected_rows_sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 # Bounded symbolic witnesses of these actual branches, not executions of a reconstructed implementation.
 witnesses=[{'incoming_list':[],'request':4,'selected_slot':0,'path':'ESI0 jumps directly to22CB0E'},
 {'incoming_list':[5,7],'request':4,'selected_slot':0,'path':'Both unsigned JB paths leave initialEAX0'},
 {'incoming_list':[5,7],'request':6,'selected_slot':5,'path':'5 qualifies,7 skipped'},
 {'incoming_list':[7,5],'request':8,'selected_slot':7,'path':'7 qualifies,5 cannot lower best'}]
 return {'local_behavior':'Empty/noeligible list selects slot0; no empty-list/no-match rejection or table-pointer validity test on this path.',
  'reset_behavior':'22C930 clears only installedCount, not pointer-table bytes. Fresh decoder entry subsequently imports ESI0 and MSCAL selects retained slot0 after flush.',
  'sentinel_limit':'Under only valid MPG-produced u16 list entries, best0/u16 never reaches10000; sentinel comparison does not reject absence of a candidate. Arbitrary corrupted list contents unqualified.',
  'witnesses':witnesses,'consumer_qualification':'Largest eligible address if one exists; otherwise slot0. Count reset removes eligibility list count but does not erase pointer table. Slot0 must be valid if dispatch is allowed.',
  'not_claimed':'No actual invalid shipped command, null/stale function invocation, callback/drawing effects, normal reset frequency, universal capacity/lifetime or full family census.',
  'limits':s['limits'],'propagation':'PENDING FABLE/OPUS/independent review'}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s);controls=[]
 for name,pc,args in [('empty-list-rejection-invented',0x22CAE5,'0x22cb41'),('no-match-sentinel-invented',0x22CADD,'eax, 0x10000')]:
  q=copy.deepcopy(s)
  for i in q['decoder']['instructions']:
   if i['pc']==hex(pc):i['args']=args
  try:derive(q)
  except AssertionError:controls.append({'name':name,'rejected':True});continue
  raise AssertionError('INVALID_CONTROL '+name)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','controls':controls,'class':'Original static flow and symbolic path witnesses; no original/native/guest/live execution or mutation campaign'},indent=2)+'\n')
 print('PASS original slot0 fallback/count-only reset, positive eligible paths and two artifact-integrity controls.')
if __name__=='__main__':main()
