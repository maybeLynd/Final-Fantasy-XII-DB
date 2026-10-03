"""Conditional mode17 resource-write and notification order, original code only."""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def need(x,m):
 if not x:raise ValueError(m)
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 ops=[(0x300cf9,'mov','ebx, r8d'),(0x300cfc,'mov','r12d, edx'),(0x300cff,'mov','rsi, rcx'),(0x300d02,'call','0x31b860'),(0x300d0d,'shr','r13d, 4'),(0x300d13,'not','r13d'),(0x300d16,'and','eax, 1'),(0x300d19,'and','r13d, 1'),(0x300d37,'shr','r15d, 7'),(0x300d3b,'not','r15d'),(0x300d3e,'and','r15d, 1'),(0x300d44,'jne','0x300d69'),
 (0x300da4,'je','0x300dd8'),(0x300da9,'je','0x300dbf'),(0x300dba,'call','0x3283d0'),(0x300dc2,'je','0x300dd8'),(0x300dc4,'mov','ecx, dword ptr [r14 + 8]'),(0x300dce,'mov','r8d, edi'),(0x300dd1,'mov','edx, ebx'),(0x300dd3,'call','0x28f1f0'),(0x300ddb,'jns','0x300e00'),(0x300ddd,'call','0x30b770'),(0x300de4,'mov','dword ptr [rsp + 0x68], eax'),(0x300deb,'call','0x30b7f0'),(0x300df0,'cmp','word ptr [rsp + 0x6a], 0'),(0x300df6,'jne','0x300e2a'),(0x300df8,'shr','eax, 0x10'),(0x300dfe,'jne','0x300e2a'),(0x300e00,'mov','word ptr [rsi + 0x4c], di'),(0x300e07,'jle','0x300e19'),(0x300e14,'call','0x300bc0'),(0x300e20,'jge','0x300e2a'),(0x300e25,'call','0x2fa540'),
 (0x300be5,'test','r14b, 1'),(0x300be9,'jne','0x300c10'),(0x300c6a,'mov','word ptr [rdi + 6], cx'),(0x300c6e,'mov','edx, r14d'),(0x300c74,'call','0x30e060')]
 for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'mode17 operation changed '+hex(pc))
 mode=17;low=mode&1;suppress=(~(mode>>4))&1;notify=(~(mode>>7))&1
 need((low,suppress,notify)==(1,0,1),'mode17 flag derivation wrong')
 # Explicit supplied normal-return branch conditions; do not assign actual
 # query results or claim that every branch is reachable in natural gameplay.
 fixed={0x300d44:True,0x300da4:False,0x300da9:True,0x300dc2:False,0x300ddb:False,0x300e07:True}
 cases=[]
 for label,first_nonzero,second_nonzero in [('both-upper-words-zero',False,False),('first-upper-word-nonzero',True,False),('second-upper-word-nonzero',False,True)]:
  f=dict(fixed);f.update({0x300df6:first_nonzero,0x300dfe:second_nonzero});g=G.graph(ix,0x300ce0,0x300e3f,fixed=f)
  writes=0x300e00 in g['visited'];expected=not(first_nonzero or second_nonzero)
  need(writes==expected and (0x300dd3,'0x28f1f0') in g['calls'] and (0x300dba,'0x3283d0') not in g['calls'],'negative-delta source partition differs')
  need(all((pc,t) in g['calls'] for pc,t in [(0x300ddd,'0x30b770'),(0x300deb,'0x30b7f0')]),'negative post-query omitted')
  if writes:need(G.dominates(g,0x300dd3,0x300e00),'notification boundary does not precede own write')
  else:need(0x300e25 not in g['visited'],'own later decrease hook runs on veto path')
  cases.append(dict(label=label,own_word4c_store= writes,notification_attempt_before_post_queries=True,initial_3283d0_attempt=False,method='Conditional original local CFG, not machine-code execution',premises='Mode17, valid stats/storage/ABI, owner returned nonNULL, delta<0, normal callees and supplied upper-word query results; no natural reachability'))
 secondary=G.graph(ix,0x300bc0,0x300c8f,fixed={0x300be9:True})
 need(G.dominates(secondary,0x300c6a,0x300c74) and all(t not in ['0x30b770','0x30b7f0'] for _,t in secondary['calls']),'secondary initial-guard/store-order differs')
 return dict(flags='Mode17 bit0=1 bypasses initial eligibility checks; invertedbit4=0 suppresses3283D0; invertedbit7=1 enables28F1F0 when resolvedowner nonNULL. This is source argument composition, not observed game state.',primary_negative='The bit0 initial bypass does not bypass the later negative-delta checks.30B770 return upperWORD and30B7F0 return upperWORD are checked after28F1F0 attempt and before own statsWORD4C store. Any supplied nonzero upperWORD vetoes this own write and own later2FA540 decrease hook. Actual query output domains/effects remain unresolved here.',notification_limit='28F1F0 is a call attempt with ownerDWORD8/old signedWORD4C/clamped candidate/R9D1. No visible notification, callback effect or actual memory before/after observation is proved. Callees could have other writes; no whole-call no-write guarantee.',secondary='Mode17 bypasses300BC0 initial30B770/30B7F0 leg. Original ownWORD6 store precedes30E060 call carrying fullsaved flags17. Postcallee semantic effects remain open.',cases=cases,remaining='Resolve actual upper-word query domains/effects underthe same action state and30E060/28F1F0/2FA540 transitive effects when needed. No natural veto/reachability, resource-binding preservation, concurrent behavior or full command consequence closure.')
def main():
 out=P/sys.argv[1];need(not out.exists(),'immutable output exists');C=module('capture_checks','capture_prerequisites.py');qualified=C.check(P,'prepare-extents.py','capture.py','extents-01','capture-01','extents-01.json','source-01.json',['0x300ce0','0x300bc0'])
 need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed dependencies changed')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed');pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');s=json.loads((P/'source-01.json').read_text());need(s['exe_sha256']==PIN,'wrong source image');annotation=V.validate(s);ix={}
 for r in s['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original bytes');ix.update({int(i['pc'],16):i for i in r['instructions']})
 facts=derive(ix,G);controls=[]
 for label,pc,key,v in [('remove-negative-query-branch',0x300ddb,'mnemonic','jmp'),('unconditional-primary-store',0x300df6,'args','0x300e00'),('secondary-post-helper-identity',0x300c74,'args','0x30b770')]:
  a=copy.deepcopy(ix);a[pc][key]=v
  try:derive(a,G)
  except ValueError as e:controls.append(dict(label=label,pc=hex(pc),mutation={key:v},refused=str(e),method='Synthetic source-control, not original execution'))
  else:raise ValueError('source control accepted mutation')
 with out.open('x')as f:json.dump(dict(producer_complete=True,method='A STATIC_ONLY conditional original CFG/dataflow',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path='source-01.json',sha256=sha(P/'source-01.json'))],capture_prerequisites=qualified,annotation_prerequisites=[annotation],facts=facts,source_controls=controls,limits='Three supplied branch partitions/three focused source controls, not native/live observations. Actual query domains/callee effects and normal reachability OPEN.',acceptance='Producer-valid only; independent review/consumption pending.'),f,indent=2)
 print('PROVED mode17 initial bypass retains negative post-veto; notification attempt precedes own write; secondary ownwrite precedes callback boundary')
if __name__=='__main__':main()
