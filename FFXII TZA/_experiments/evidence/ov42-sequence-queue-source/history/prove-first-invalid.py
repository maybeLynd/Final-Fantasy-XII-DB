"""Bounded original kind-4 queue source, without inventing kind/row coherence."""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(ok,msg):
 if not ok:raise ValueError(msg)
def receipt(tag,driver):
 s=json.loads((P/(tag+'.status.json')).read_text());need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==sha(P/driver) and bool((P/(tag+'.stdout')).read_bytes()) and not(P/(tag+'.stderr')).read_bytes(),'required successful current invocation '+tag)
def derive(ix,d,G):
 expected=[(0x30676d,'mov','rbx, rcx'),(0x306775,'mov','rdi, rdx'),(0x3067aa,'mov','eax, dword ptr [rip + 0x1fbb9ac]'),(0x3067b0,'dec','eax'),(0x3067b7,'cmp','eax, 5'),(0x3067ba,'ja','0x306a9a'),(0x3067c0,'cdqe',''),(0x3067c7,'lea','r14, [rip - 0x1e67ce]'),(0x3067ce,'mov','eax, dword ptr [r14 + rax*4 + 0x1e6af0]'),(0x3067d6,'add','rax, r14'),(0x3067d9,'jmp','rax'),(0x306898,'mov','rax, qword ptr [rip + 0x2bb8899]'),(0x30689f,'mov','ecx, dword ptr [rax + 0xc]'),(0x3068a2,'call','0x20e600'),(0x3068a7,'sub','edi, eax'),(0x3068a9,'xor','edx, edx'),(0x3068ab,'mov','rax, qword ptr [rip + 0x2bb8886]'),(0x3068b2,'movzx','ecx, word ptr [rax + 8]'),(0x3068b6,'mov','eax, edi'),(0x3068b8,'div','ecx'),(0x3068bd,'mov','edx, 0xffff'),(0x3068c2,'cmp','ax, dx'),(0x3068c5,'je','0x3068d1'),(0x3068c7,'movzx','eax, ax'),(0x3068ca,'sub','eax, 0xd0'),(0x3068cf,'jmp','0x3068d4'),(0x3068d1,'or','eax, 0xffffffff'),(0x3068d4,'mov','dword ptr [rip + 0x1fbb89e], eax')]
 for pc,m,a in expected:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'sequence operation changed '+hex(pc))
 need(d['relative_dwords']==[0x1e6931,0x1e6a3d,0x1e67db,0x1e6848,0x1e69f8,0x1e6a8e],'dispatch table changed')
 targets=[0x120000+v for v in d['relative_dwords']];need(all(t in ix for t in targets),'missing dispatch targets')
 # The one indirect instruction is analytically resolved for each actual kind,
 # after verifying the original table, DEC/unsigned bound/CDQE/base/index chain.
 reach=[]
 for k,t in enumerate(targets,1):
  v=copy.deepcopy(ix);v[0x3067d9]['args']=hex(t)
  g=G.graph(v,0x306760,0x306aef,fixed={0x3067ba:False})
  reach.append(dict(kind=k,target=hex(t),queue_store_reachable=0x3068d4 in g['visited']))
 need([q['kind'] for q in reach if q['queue_store_reachable']]==[4],'queue not exclusive to kind4 dispatch')
 g=G.graph(ix,0x306848,0x306aef)
 need(G.dominates(g,0x3068d4,0x306898) and G.dominates(g,0x3068d4,0x3068b8),'queue source arithmetic not mandatory')
 # No native call after the DIV before the two-arm queue store; these are exact
 # straight-line partitions, not native executions or live row observations.
 sites=[i for a,i in sorted(ix.items()) if 0x306898<=a<=0x3068d4]
 need([i['args'] for i in sites if i['mnemonic']=='call']==['0x20e600'],'extra arithmetic call')
 writes=[(hex(a),i['mnemonic'],i['args']) for a,i in sorted(ix.items()) if 0x306848<=a<0x3068a7 and i['args'].split(',')[0] in ['rdi','edi','di','dil'] and i['mnemonic'] not in ['cmp','test']]
 need(not writes,'incoming row carrier overwritten before pointer subtraction')
 examples=[dict(supplied_row_id=i,assumed_stride=60,assumed_low32_difference=i*60,quotient=i,queue_dword=i-208) for i in [511,534]]
 return dict(dispatch=reach,input='Entry RDX -> nonvolatile RDI; earlier helper effects and valid ABI/stability explicitly conditional.',formula='D = (low32(incoming row pointer) - low32(20E600(context+C) return)) mod 2^32. S = u16(second context load+8). With S>0, q=floor(D/S), w=q&0xFFFF. w==FFFF -> queue DWORDFFFFFFFF; otherwise queue DWORD=w-208 mod2^32.',context='Two independent loads of QWORD2EBF138 at306898/3068AB; first supplies lookup key DWORD+C, second supplies divisor WORD+8. Do not assume identical contexts or immutable descriptor/lookup.',divisor='No zero-divisor guard between WORD load and DIV ECX; S>0 is a precondition, not an observed initialized invariant or fault.',candidate_examples=examples,scope='Examples are arithmetic consequences under coherent row/base/stride premises, not original-code executions. Kind4 alone does not locally check row ID; any exclusion requires the relationship between global kind and this call\'s row pointer.',limits='No natural kind4/candidate pair, caller/owner coherence, setter/dispatch scheduling, initialized descriptors, native helper effects, lifetime/reuse or whole OV42 closure. Normal Win64 ABI, readable disjoint state and no interference required. Entry earlier helper calls can affect state; no side-effect-free whole-function claim.')
def main():
 out=Path(sys.argv[1]);need(not out.exists(),'immutable output already exists')
 for tag,driver in [('extent-01','extent.py'),('capture-02','capture.py'),('data-01','capture-data.py')]:receipt(tag,driver)
 e=json.loads((P/'extent-01.json').read_text());d=json.loads((P/'data-01.json').read_text());x=json.loads((P/'source-02.json').read_text())
 need(e.get('complete') is True and e['bytes']==936 and len(e['records'])==5 and d.get('complete') is True,'physical metadata/data incomplete')
 need(x.get('wrapper_complete') is True and x['invocation_driver_sha256']==sha(P/'capture.py') and x['driver_sha256']==sha(P/'capture-index-path.py'),'source capture identity incomplete')
 need(sha(P/'capture-index-path.py')=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497' and sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed dependency changed')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');annotation=V.validate(x)
 PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN and x['exe_sha256']==PIN and d['exe_sha256']==PIN and e['exe_sha256']==PIN,'reference identity changed')
 blob=bytes.fromhex(d['physical_body_hex']);need(len(blob)==936 and hashlib.sha256(blob).hexdigest()==e['body_sha256']==d['physical_body_sha256'],'physical bytes/hash disagreement')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];matched=False
 for k in range(struct.unpack_from('<H',raw,pe+6)[0]):
  vs,rva,sz,off=struct.unpack_from('<IIII',raw,pe+32+opt+40*k)
  if 0x120000+rva<=0x306760 and 0x306b08<=0x120000+rva+sz:
   start=off+0x306760-0x120000-rva;need(raw[start:start+936]==blob,'not original physical bytes');matched=True
 need(matched and len(x['ranges'])==1,'missing original range')
 r=x['ranges'][0];code=bytes.fromhex(''.join(i['bytes'] for i in r['instructions']));need((r['start'],r['end_exclusive'])==('0x306760','0x306aef') and code==blob[:911] and blob[911:912]==b'\x90' and blob[912:]==bytes.fromhex(d['table_hex']) and list(struct.unpack('<6I',blob[912:]))==d['relative_dwords'],'code/padding/table separation differs')
 ix={int(i['pc'],16):i for i in r['instructions']};facts=derive(ix,d,G)
 result=dict(producer_complete=True,method='A STATIC_ONLY original dispatch table and queue arithmetic',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path='source-02.json',sha256=sha(P/'source-02.json'))],data_pin=dict(path='data-01.json',sha256=sha(P/'data-01.json')),metadata_pin=dict(path='extent-01.json',sha256=sha(P/'extent-01.json')),annotation_prerequisites=[annotation],facts=facts,limits=facts['limits'],cleanup='All tools offline and bounded; no FF12/native/emulator/PC control or save/config/reference/process intervention.')
 with out.open('x') as f:json.dump(result,f,indent=2)
 print('PROVED kind4-only local queue writer and exact quotient/remap; kind-to-row coherence OPEN')
if __name__=='__main__':main()
