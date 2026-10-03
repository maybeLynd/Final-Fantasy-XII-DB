"""New conditional Dismiss ordering proof over immutable retained shipping inputs."""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
W=ROOT/'Database/Tools/work/ASTRA/runtime-residue-method-retriage'
E=ROOT/'Database/FFXII TZA/_experiments/evidence'
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def need(x,m):
 if not x:raise ValueError(m)
def load(slug,name,pin):
 p=E/slug/name;z=p.read_bytes();need(hashlib.sha256(z).hexdigest()==pin,'retained dependency changed '+name);return json.loads(z)
def ix(s):return {int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
def instruction(i,pc,m,a):need(pc in i and (i[pc]['mnemonic'],i[pc]['args'])==(m,a),'instruction/selected path changed '+hex(pc))
def memory(i,pc,**k):
 z=i[pc]['memory'];need(len(z)==1 and all(z[0].get(a)==b for a,b in k.items()),'selected memory identity changed '+hex(pc))
def derive(q,pre,suffix,qd,kd):
 a=ix(q);c=ix(pre)|ix(suffix)
 for pc,m,s in [(0x306c71,'sub','esi, eax'),(0x306c7c,'movzx','ecx, word ptr [rax + 8]'),(0x306c80,'mov','eax, esi'),(0x306c82,'div','ecx'),(0x306c84,'add','eax, 0xffffff6c'),(0x306c89,'cmp','eax, 0x7f'),(0x306c8c,'ja','0x306ccc'),(0x306c95,'movzx','eax, byte ptr [rdx + rax + 0x1e6d08]'),(0x306c9d,'mov','ecx, dword ptr [rdx + rax*4 + 0x1e6cec]'),(0x306ca4,'add','rcx, rdx'),(0x306ca7,'jmp','rcx'),(0x306cb0,'mov','ebx, 2'),(0x306cb5,'jmp','0x306cd1')]:instruction(c,pc,m,s)
 mapping=bytes.fromhex(kd['mapping_hex']);jumps=struct.unpack('<7I',bytes.fromhex(kd['jump_hex']))
 need(len(mapping)==128 and mapping[0x113-0x94]<7,'classifier table malformed')
 target=0x120000+jumps[mapping[127]]
 need(target==0x306cb0,'full quotient275 no longer publishes kind2')
 memory(c,0x306cdb,role='w',rip_target='0x22c215c',size=4)
 for pc,m,s in [(0x3067aa,'mov','eax, dword ptr [rip + 0x1fbb9ac]'),(0x3067b0,'dec','eax'),(0x3067b7,'cmp','eax, 5'),(0x3067ba,'ja','0x306a9a'),(0x3067c0,'cdqe',''),(0x3067ce,'mov','eax, dword ptr [r14 + rax*4 + 0x1e6af0]'),(0x3067d6,'add','rax, r14'),(0x3067d9,'jmp','rax')]:instruction(a,pc,m,s)
 memory(a,0x3067aa,role='r',rip_target='0x22c215c',size=4)
 jt=struct.unpack('<6I',bytes.fromhex(qd['table_hex']))
 need(0x120000+jt[1]==0x306a3d,'kind2 dispatch is not the Dismiss arm')
 need(0x120000+jt[0]==0x306931,'positive kind1 dispatch changed')
 for pc,m,s in [(0x306a44,'test','byte ptr [rax + 0x5ad0], 1'),(0x306a4b,'je','0x306a5b'),(0x306a4f,'call','0x35dae0'),(0x306a68,'call','0x306d90'),(0x306a74,'mov','eax, dword ptr [rcx + 0x5b04]'),(0x306a7a,'test','al, 1'),(0x306a7c,'je','0x306a95'),(0x306a7e,'and','eax, 0xfffffffe'),(0x306a81,'mov','dword ptr [rcx + 0x5b04], eax'),(0x306a87,'call','0x35c620'),(0x306a8c,'jmp','0x306a95'),(0x306ab2,'test','ebx, ebx'),(0x306ab4,'jle','0x306ad3'),(0x306acd,'sub','rcx, 1'),(0x306ad1,'jne','0x306ac0'),(0x306ad3,'mov','ecx, 3'),(0x306ad8,'call','0x332130'),(0x306adf,'mov','dword ptr [rip + 0x1fbb677], 5')]:instruction(a,pc,m,s)
 for pc in [0x306a3d,0x306a54,0x306a6d]:memory(a,pc,role='r',rip_target='0x2ebf190',size=8)
 for pc,role in [(0x306a74,'r'),(0x306a81,'w')]:memory(a,pc,role=role,base='rcx',displacement=0x5b04,size=4)
 memory(a,0x306adf,role='w',rip_target='0x22c2160',size=4)
 instruction(a,0x306946,'or','ecx, 1');memory(a,0x306949,role='w',base='rdx',displacement=0x5b04,size=4)
 # Validate all normal successors in the connected arm/common suffix. Calls
 # are deliberately opaque; normal returns and finite valid roster loop required.
 lo,hi=0x306a3d,0x306ae9
 for pc,i in a.items():
  if not lo<=pc<hi or 0x306a8e<=pc<0x306a95:continue # other kind's dismount arm
  if i['mnemonic'].startswith('j'):need(i['args'].startswith('0x') and lo<=int(i['args'],16)<hi,'selected path escapes before state5')
 return dict(classifier='Under full unsigned row/base/positive-stride quotient275, original selector byte127 and jump entry5 reach306CB0 EBX2 ->022C215C. Quotient275 is a premise, not a naturally observed action.',
  dispatch='306760 reads currentkind separately. Kind2 uses original six-entry table element1 ->306A3D. Kind1 element0 ->306931 ORs modebit1, a distinct positive arm. Same-kind/owner/current-row persistence is not established here.',
  order='On normal kind2 path, optional35DAE0 and306D90 run first. It then re-reads battle pointer/mode; if bit0set, AND~1 and directDWORDstore at306A81 precede35C620, common rosterflag loop,332130(3) and this routine\'s direct022C2160=5 at306ADF. If bit0alreadyclear, localmode store is skipped and common state5 path remains. The literal state5 write belongs to this common preparation path; no finishing-state6/7 guard surrounds this localclear.',
  implication='The canonical phrase "clears bit0 when the sequence ends" needs qualification against this local preparation ordering. This is not proof of actual onscreen timing or eventual cleanup, and not proof of naturally initialized summonerKO reachability.',
  limits='Exact original code/tables/readable objects, Win64 ABI/valid private stack, normal returning opaque helpers, bounded valid roster traversal and no interference. Helpers can change objects or global state; no lastingmodeclear, firsteverstate5, resource success, atomic snapshot, lifetime/reuse/natural scheduling or wholeUQ147 closure.')
def main():
 out=P/sys.argv[1];need(not out.exists(),'fresh output required')
 Q='ov42-sequence-queue-source';K='ov42-kind-row-coherence'
 deps=[(Q,'source-02.json','c7177768e00b6b98a33d464a4714837af414a9df1a8ed3bce72e5992b70a2db1'),(K,'retained-prefix-01.json','33276301865c4c6aca31720248a0afe6c6832924b97bd40e754abdc2b45c307a'),(K,'source-01.json','75e86a31138d7e4242101e5315741837b8f8c7eabf95f52de19e050ec0b1cf59'),(Q,'data-01.json','19e148fb2cd82900f6a23f91282c34ffeca83bf7bdddb533a0effc4c02b407eb'),(K,'data-01.json','d2ee2256cfda1d4f77c4ebf944b054d0e4b228b9e63eacaf4bc16d54358eea2c')]
 q,pre,suffix,qd,kd=[load(*d) for d in deps]
 for slug,n,pin in [(Q,'capture-02.status.json','5cf973a0584bdaf72bb8db73e49f78c27ac3d867c7c4f381d895ea931fe89a4a'),(Q,'data-01.status.json','94e05fb9356f602d14df3666261d424e87b50b4ec3a8ef066418eaec0eba1431'),(K,'capture-02.status.json','6deff0b68cd752d0965e3919c5b59b5b5266e716435191d0f947472c30f7630e'),(K,'data-01.status.json','32472aa6c25172dc0e69da438905fbe757664bbf50003fc3afc33d5198885477')]:
  s=load(slug,n,pin);need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None,'retained upstream failed/incomplete')
 vfile=W/'validate-title-source-annotations.py';need(hashlib.sha256(vfile.read_bytes()).hexdigest()=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
 spec=importlib.util.spec_from_file_location('reviewed_roles',vfile);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 annotations=[v.validate(x) for x in [q,pre,suffix]]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'original image changed')
 pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0]
 def original(a,n):
  for j in range(struct.unpack_from('<H',raw,pe+6)[0]):
   _,rva,sz,off=struct.unpack_from('<IIII',raw,pe+32+os+40*j)
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('physical data unbacked')
 for d,a,n in [(qd,0x306760,936),(kd,0x306bd0,440)]:
  z=bytes.fromhex(d['physical_body_hex']);need(d.get('complete') is True and len(z)==n and z==original(a,n),'retained physical body/table mismatch')
 need(bytes.fromhex(qd['table_hex'])==original(0x306af0,24) and bytes.fromhex(kd['jump_hex'])==original(0x306cec,28) and bytes.fromhex(kd['mapping_hex'])==original(0x306d08,128),'table/code boundary mismatch')
 facts=derive(q,pre,suffix,qd,kd);controls=[]
 for id,kind in [('dismiss-selector-byte-changed','map'),('kind2-table-target-changed','jump'),('mode-store-offset-changed','offset'),('state5-target-changed','state')]:
  z=copy.deepcopy([q,pre,suffix,qd,kd])
  if kind=='map':b=bytearray.fromhex(z[4]['mapping_hex']);b[127]=4;z[4]['mapping_hex']=b.hex();want='no longer publishes kind2'
  elif kind=='jump':b=bytearray.fromhex(z[3]['table_hex']);struct.pack_into('<I',b,4,0x306931-0x120000);z[3]['table_hex']=b.hex();want='dispatch is not the Dismiss arm'
  elif kind=='offset':ix(z[0])[0x306a81]['memory'][0]['displacement']=0x5ad0;want='selected memory identity changed'
  else:ix(z[0])[0x306adf]['memory'][0]['rip_target']='0x22c215c';want='selected memory identity changed'
  try:derive(*z)
  except ValueError as e:need(want in str(e),'wrong control detector');controls.append(dict(id=id,diagnostic=str(e),method='Labelled synthetic source/table-record semantic control, not an EXE patch or machine-code execution'))
  else:raise ValueError('semantic detector missed '+id)
 with out.open('x') as f:json.dump(dict(producer_complete=True,method='A retained original bytes/branch tables and conditional order proof; no new code capture or native execution',driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exe_sha256=PIN,canonical_dependencies=[dict(slug=s,path=n,sha256=h) for s,n,h in deps],annotation_prerequisites=annotations,facts=facts,controls=controls,acceptance='Producer-valid only; independent review/canonical consumption pending. WholeUQ147 remains open.'),f,indent=2)
 print('Retained original tables bind Dismiss kind2; conditional local mode clear precedes same routine state5 write. Natural timing/KO remains OPEN.')
if __name__=='__main__':main()
