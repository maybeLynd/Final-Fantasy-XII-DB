"""Original mask output invariants; no game sample/forced native returns."""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def need(x,m):
 if not x:raise ValueError(m)
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 ops=[(0x30b785,'mov','dword ptr [rbp], 0'),(0x30b78c,'test','ecx, 0x3080'),(0x30b799,'mov','word ptr [rbp], ax'),(0x30b7ac,'or','ax, 2'),(0x30b7ba,'or','ax, 4'),(0x30b7c8,'or','ax, 8'),(0x30b7d6,'or','ax, 0x10'),(0x30b7de,'mov','eax, dword ptr [rbp]'),
 (0x30b7f6,'mov','dword ptr [rsp + 0x30], 0'),(0x30b804,'je','0x30b8c8'),(0x30b80d,'test','r8b, 0x10'),(0x30b811,'je','0x30b8c8'),(0x30b851,'jae','0x30b860'),(0x30b853,'test','edx, edx'),(0x30b855,'je','0x30b860'),(0x30b883,'call','0x17d470'),(0x30b888,'cmp','eax, 1'),(0x30b88b,'jne','0x30b8b1'),(0x30b88d,'mov','rax, qword ptr [rbx + 0x698]'),(0x30b897,'je','0x30b8b1'),(0x30b899,'movzx','eax, byte ptr [rax + 5]'),(0x30b89f,'jne','0x30b8b1'),(0x30b8a1,'movzx','ebx, word ptr [rsp + 0x32]'),(0x30b8a6,'or','bx, 1'),(0x30b8aa,'mov','word ptr [rsp + 0x32], bx'),(0x30b8b6,'call','0x17d470'),(0x30b8bb,'cmp','eax, 2'),(0x30b8be,'jne','0x30b8c8'),(0x30b8c0,'or','bx, ax'),(0x30b8c3,'mov','word ptr [rsp + 0x32], bx'),(0x30b8c8,'mov','eax, dword ptr [rsp + 0x30]'),(0x17d474,'call','0x1d50d0'),(0x17d479,'mov','eax, dword ptr [rax + 0xc20]')]
 for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'eligibility operation changed '+hex(pc))
 globalg=G.graph(ix,0x30b770,0x30b7e7);need(not globalg['calls'] and globalg['returns']==[0x30b7e6],'global query is not complete call-free leaf')
 stores=[(pc,m) for pc in sorted(globalg['visited']) for m in ix[pc]['memory'] if m['role'] in ['w','rw']]
 need(len(stores)==6 and all(m['base']=='rbp' and m['displacement']==0 and m['size']==(4 if pc==0x30b785 else 2) for pc,m in stores),'global query can write upperword differently')
 need(G.dominates(globalg,0x30b785,0x30b7de),'global zero initialization can be bypassed')
 unitg=G.graph(ix,0x30b7f0,0x30b8d2);need(unitg['calls']==[(0x30b883,'0x17d470'),(0x30b8b6,'0x17d470')],'unit query opaque boundaries changed')
 writes=[(pc,m) for pc in sorted(unitg['visited']) for m in ix[pc]['memory'] if m['role'] in ['w','rw']]
 need(len(writes)==7 and all(m['base']=='rsp' and (m['displacement'],m['size']) in [(0x30,4),(0x30,2),(0x32,2)] for pc,m in writes),'unit output store footprint differs')
 need([pc for pc,m in writes if m['displacement']==0x32]==[0x30b8aa,0x30b8c3],'other upperword write present')
 need(G.dominates(unitg,0x30b7f6,0x30b8c8),'unit output initialization bypass')
 # The second OR uses AX only after fullEAX==2, so it adds exactly bit2.
 # The first adds exactly bit1 only after mode1, nonNULLstats andstatsBYTE5==0.
 def high(eligible,first,second,stats0):return (1 if eligible and first==1 and stats0 else 0)|(2 if eligible and second==2 else 0)
 controls=[dict(eligible=True,first=1,second=1,stats0=True,upper=high(True,1,1,True)),dict(eligible=True,first=2,second=2,stats0=False,upper=high(True,2,2,False)),dict(eligible=True,first=1,second=2,stats0=True,upper=high(True,1,2,True)),dict(eligible=False,first=1,second=2,stats0=True,upper=high(False,1,2,True))]
 need([c['upper'] for c in controls]==[1,2,3,0],'mode predicate discrimination wrong')
 return dict(global_query='InitialDWORD0, only lowWORD stores and no calls: returned upperWORD is always0 with ordinary valid private frame. Low mask is confined tobits0..4 (0..31), whatever inputglobals; no initialization sample required.',unit_query='Normal return upperWORD = (eligible && first_mode==1 && currentstats_nonNULL && statsBYTE5==0 ? 1 : 0) OR (eligible && second_mode==2 ? 2 : 0). eligible requires nonNULLunit andunitDWORD bit4. Validstorage/ABI/privateframe and normalcallee returns required. Outputhigh is0..3 forarbitraryuint32 modevalues; same modevalue acrossreads restricts high to0..2.',input_zero='300CE0 passes queryEDX0, so unit-lowbit1 arm requiringEDXnonzero is absent. Lowword reasons remain separate from upperword protection.',mode_getter='17D470 obtainsRAX from1D50D0 thenreadsDWORDobject+C20. C20 is the existing canonical Invincible setting. Neither singleton initialization/default nor1D50D0 effects/lifetime are proved here; mode reads remain independent.',correction='Earlier mode17 first-global-upper-nonzero supplied CFG case is an instrument/callee-intervention countercontrol, not reachable with the shipping30B770/privateframe. Preserve its original evidence; remove that first-query uncertainty from native semantics. Negative primary own-write veto can onlycome from unitqueryupperword on valid normal original query calls, although callee effects/concurrency still matter.',formerly_runtime_reduction='One precise proposition (whether normal original globalqueryupperWORD couldbe nonzero) eliminated by invariant with no live game. Independent acceptance/canonical incorporation pending; accepted historical count remains4.',conditional_controls=controls,limits='Predicate models and source invariants, not original-code execution/livevalues or natural mode transitions. Upper3 is a two-read countermodel, not observed changing Invincible setting. No visible presentation or wholecall memory-effect claim.')
def main():
 out=P/sys.argv[1];need(not out.exists(),'immutable output exists');C=module('capture_checks','capture_prerequisites.py');qualification=[C.check(P,'prepare-extents.py','capture.py','extents-01','capture-01','extents-01.json','source-01.json',['0x30b770','0x30b7f0']),C.check(P,'prepare-mode-extents.py','capture-mode.py','mode-extents-01','mode-capture-01','mode-extents-01.json','mode-source-01.json',['0x17d470'])]
 need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed dependencies changed')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed');pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');ix={};annotations=[];files=['source-01.json','mode-source-01.json','caller-mutators-source-01.json']
 for f in files:
  s=json.loads((P/f).read_text());need(s['exe_sha256']==PIN,'wrong source image');annotations.append(V.validate(s))
  for r in s['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original bytes');ix.update({int(i['pc'],16):i for i in r['instructions']})
 need(sha(P/'caller-mutators-source-01.json')=='d89a6e1a23f1c711b1b6717263973f83044c5a0a3cddf9e3cf82969ba955d593' and (ix[0x300de2]['mnemonic'],ix[0x300de2]['args'])==('xor','edx, edx') and (ix[0x300de8]['mnemonic'],ix[0x300de8]['args'])==('mov','rcx, r14') and (ix[0x300deb]['mnemonic'],ix[0x300deb]['args'])==('call','0x30b7f0'),'qualified caller query0 transfer differs')
 facts=derive(ix,G);controls=[]
 for label,pc,key,v in [('nonzero-output-init',0x30b785,'args','dword ptr [rbp], 0x10000'),('wrong-mode-selector',0x30b8bb,'args','eax, 3'),('wrong-mode-field-width',0x17d479,'args','rax, qword ptr [rax + 0xc20]')]:
  a=copy.deepcopy(ix);a[pc][key]=v
  try:derive(a,G)
  except ValueError as e:controls.append(dict(label=label,mutation={key:v},refused=str(e),method='Synthetic source assertion control, not original execution'))
  else:raise ValueError('source control accepted mutation')
 with out.open('x')as f:json.dump(dict(producer_complete=True,method='A STATIC_ONLY original output invariant and predicate/dataflow proof',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=f,sha256=sha(P/f)) for f in files],capture_prerequisites=qualification,annotation_prerequisites=annotations,facts=facts,source_controls=controls,limits=facts['limits'],acceptance='Producer valid; independent review/canonical consumption pending'),f,indent=2)
 print('PROVED global mask upperWORD always0; owner upperWORD0..3, stablemode0..2; nativefirst-veto need eliminated withoutlive')
if __name__=='__main__':main()
