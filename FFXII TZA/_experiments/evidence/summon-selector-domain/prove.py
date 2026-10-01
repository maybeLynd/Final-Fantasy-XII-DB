"""Local selector-domain proof; initialized actor identity remains separate."""
import argparse,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
 if out.exists():raise RuntimeError('immutable result exists')
 st=json.loads((src/'capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
 v=json.loads((src/'source-01.json').read_text())
 if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('mixed/incomplete source wrapper')
 V=load('summon_selector_roles',T/'validate-title-source-annotations.py');annotation=V.validate(v)
 if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph dependency changed')
 G=load('summon_selector_graph',T/'prove_owner_reload_order.py');raw=(G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise RuntimeError('wrong original image')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,o in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[o+a-0x120000-rva:o+a-0x120000-rva+n]
  raise RuntimeError('unbacked source')
 ranges=v['ranges']
 if [(r['start'],r['end_exclusive']) for r in ranges]!=[('0x50ffb0','0x50ffeb'),('0x3139c0','0x3139ce'),('0x3137e0','0x3137ef'),('0x3266c0','0x326ba5')]:raise RuntimeError('required source population changed')
 for r in ranges:
  lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for r in ranges for i in r['instructions']}
 pins=[(0x50ffba,'mov','rcx, r9'),(0x50ffbd,'mov','rbx, r9'),(0x50ffc0,'call','0x267e10'),(0x50ffc5,'mov','rcx, rbx'),(0x50ffc8,'mov','edi, eax'),(0x50ffca,'call','0x267e10'),(0x50ffcf,'movzx','ecx, dil'),(0x50ffd3,'mov','ebx, eax'),(0x50ffd5,'call','0x3139c0'),(0x50ffda,'mov','ecx, ebx'),(0x50ffe6,'jmp','0x313550'),
 (0x3139c0,'mov','rax, qword ptr [rip + 0x2bab7c9]'),(0x3139c7,'mov','byte ptr [rax + 0x5ad4], cl'),(0x3139cd,'ret',''),(0x3137e0,'mov','rax, qword ptr [rip + 0x2bab9a9]'),(0x3137e7,'movzx','eax, byte ptr [rax + 0x5ad4]'),(0x3137ee,'ret',''),
 (0x3266c8,'mov','rdi, qword ptr [rip + 0x2b98ac1]'),(0x3266d4,'add','rdi, 0x5a48'),(0x32670e,'mov','r13d, 0xffff'),(0x32674f,'call','0x30d9a0'),(0x326754,'xor','ebp, ebp'),(0x326756,'sub','eax, 1'),(0x326759,'je','0x3269d2'),(0x3269d2,'call','0x313800'),(0x3269d7,'movsxd','rbx, eax'),(0x3269da,'call','0x3137e0'),(0x3269df,'mov','rcx, rbp'),(0x3269e2,'cmp','rcx, 3'),(0x3269e6,'jne','0x326a14'),
 (0x3269e8,'movzx','edx, al'),(0x3269eb,'cmp','al, 0xff'),(0x3269ed,'jne','0x3269f2'),(0x3269ef,'mov','edx, r13d'),(0x3269f2,'mov','word ptr [rdi + 0x18], dx'),(0x3269f6,'movzx','edx, al'),(0x3269f9,'cmp','al, 0xff'),(0x3269fb,'jne','0x326a00'),(0x3269fd,'mov','edx, r13d'),(0x326a00,'mov','word ptr [rdi + 0x2a], dx'),(0x326a04,'movzx','edx, al'),(0x326a07,'cmp','al, 0xff'),(0x326a09,'jne','0x326a0e'),(0x326a0b,'mov','edx, r13d'),(0x326a0e,'mov','word ptr [rdi + 0x4e], dx'),(0x326a12,'jmp','0x326a2b'),
 (0x326a14,'cmp','rcx, rbx'),(0x326a17,'je','0x326a2b'),(0x326a19,'mov','word ptr [rdi + rcx*2 + 0x12], r13w'),(0x326a1f,'mov','word ptr [rdi + rcx*2 + 0x24], r13w'),(0x326a25,'mov','word ptr [rdi + rcx*2 + 0x48], r13w'),(0x326a2b,'inc','rcx'),(0x326a2e,'cmp','rcx, 4'),(0x326a32,'jl','0x3269e2')]
 for pc,m,a in pins:
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('producer/map operation changed '+hex(pc))
 graphs=[]
 for n,r in enumerate(ranges):
  local={int(i['pc'],16):i for i in r['instructions']};g=G.graph(local,int(r['start'],16),int(r['end_exclusive'],16),tail='0x313550' if n==0 else None)
  graphs.append({'entry':r['start'],'visited':len(g['visited']),'returns':[hex(i) for i in g['returns']],'tails':[hex(i) for i in g['tails']],'calls':[[hex(pc),t] for pc,t in g['calls']]})
 if graphs[0]['calls']!=[['0x50ffc0','0x267e10'],['0x50ffca','0x267e10'],['0x50ffd5','0x3139c0']] or graphs[0]['returns'] or graphs[0]['tails']!=['0x50ffe6']:raise RuntimeError('bridge boundary changed')
 if any(i['mnemonic'].startswith('j') and i['mnemonic']!='jmp' for i in ranges[0]['instructions']) or any(i['mnemonic'].startswith('j') or i['mnemonic']=='call' for r in ranges[1:3] for i in r['instructions']):raise RuntimeError('unexpected local selector guard')
 arm=[i for i in ranges[3]['instructions'] if 0x3269df<=int(i['pc'],16)<0x326a34]
 if any(i['mnemonic']=='call' for i in arm):raise RuntimeError('new intervening arm call')
 stores=[]
 for pc,off in [(0x3269f2,0x5a60),(0x326a00,0x5a72),(0x326a0e,0x5a96)]:
  m=ix[pc]['memory'][0]
  if m['role']!='w' or m['base']!='rdi' or m['index'] or m['size']!=2 or m['displacement']+0x5a48!=off:raise RuntimeError('slot3 store identity changed')
  stores.append({'pc':hex(pc),'state_offset':hex(off),'map':{0x5a60:1,0x5a72:2,0x5a96:4}[off],'slot':3,'size':2})
 byte_cases=[{'selector_byte':s,'slot3_word':s if s!=255 else 65535,'in_esper_band':27<=s<=39} for s in range(256)]
 if len(byte_cases)!=256 or sum(r['in_esper_band'] for r in byte_cases)!=13:raise RuntimeError('invalid finite byte partition')
 examples=[{'first_pop':x,'stored_byte':x&255,'slot3_word':(x&255) if(x&255)!=255 else 65535} for x in [-1,0,26,27,39,40,254,255,256,283]]
 result={'producer_complete':True,'method':'A STATIC_ONLY original producer/dataflow proof; zero machine-code/game execution','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(src/'source-01.json')}],'annotation_prerequisites':[annotation],'instruction_assertions':len(pins),'graphs':graphs,'slot3_stores':stores,'byte_partition':byte_cases,'algebraic_examples':examples,
 'established':['Bridge stores first PopInt32 return low8 bits in5AD4, then forwards second return fullECX32 to313550; no local selector band validation','3137E0 reads5AD4 aszeroextendedbyte; mode1 arm copies thatbyte into slot3 ofmaps1/2/4, exceptFF becomesFFFF','The four-iteration arm has no type27..39 check; other slots preserve summonerindex or clearFFFF','Byte-domain behavior is source-determined; the thirteen-member authored summon rows do not bound this separate API input'],
 'map_arm_boundary':'326A34 before shared actor/application tail, same-block/noninterference premises required',
 'unresolved':['Reachable authored values at50FFB0 and full PopInt32 behavior/VM stack argument meaning','Actual actor/stats type after23A570 or async party-read completion, aliasing/lifetime/scheduling','Natural row275 Dismiss command acceptance->execution and loaded-resource identity','Other writers including saved-state restore and full source/type domain invariant'],
 'limits':'Local API and mapping domain only. Mathematical unconstrained input examples do not prove authored/gameplay reachability or a malformed-type native fault. Map selector is not captured/live stats type. Whole3266C0 CFG records callee boundaries, not transitive effects; no return-time map stability claim. Existing13table/constants/catalog names not recounted or independently accepted.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'pins':len(pins),'source_byte_cases':256,'slot3_stores':3,'natural_type_guarantee':False}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args()
 # A package-relative filename must not silently create a repository-root
 # result when the actual CLI is launched from the repository root.
 output=a.output if a.output.is_absolute() else P/a.output
 main(a.src,output)
