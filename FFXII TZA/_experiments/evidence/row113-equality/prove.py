"""Bounded-width original arithmetic invariant, not a replacement engine/sample proof."""
import argparse,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
 if out.exists():raise RuntimeError('immutable output exists')
 st=json.loads((src/'capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
 v=json.loads((src/'source-01.json').read_text())
 if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('capture wrapper incomplete/mixed')
 V=load('row113_roles',T/'validate-title-source-annotations.py');G=load('row113_cfg',T/'prove_owner_reload_order.py')
 if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph identity changed')
 roles=V.validate(v);parents={}
 pins={'presentation-index-domain':'499a3e53e678069ec4c7424c2f2efbed3236d504c899fe93555cb85596a756eb','ov42-class20-action-admission':'67e7df297497326a5b98d9d21355923750442981e8121cfb4d4e7840de5e4d92'}
 files={'presentation-index-domain':['source-01.json','result-01.json','prove.py','proof-01.status.json','proof-01.stdout','proof-01.stderr'],'ov42-class20-action-admission':['special-admission-callers-raw-01.json']}
 for name,pin in pins.items():
  manifest=src/'retained'/(name+'-manifest.json')
  if sha(manifest)!=pin:raise RuntimeError('parent manifest changed')
  members={m['path']:m for m in json.loads(manifest.read_text())['members']}
  for name2 in files[name]:
   p=src/'retained'/(name+'-'+name2);m=members[name2]
   if sha(p)!=m['sha256'] or p.stat().st_size!=m['bytes']:raise RuntimeError('parent member changed')
   if p.suffix=='.json':parents[name+'/'+name2]=json.loads(p.read_text())
 ps=parents['presentation-index-domain/proof-01.status.json'];pr=parents['presentation-index-domain/result-01.json'];pd=src/'retained/presentation-index-domain-prove.py'
 if ps.get('exit')!=0 or ps.get('terminal') is not True or ps.get('exception') is not None or ps['driver_sha256']!=sha(pd) or pr['driver_sha256']!=sha(pd) or pr.get('producer_complete') is not True or not(src/'retained/presentation-index-domain-proof-01.stdout').read_bytes() or(src/'retained/presentation-index-domain-proof-01.stderr').read_bytes():raise RuntimeError('required original parent proof failed/incomplete')
 sel=parents['presentation-index-domain/source-01.json'];caller=parents['ov42-class20-action-admission/special-admission-callers-raw-01.json']
 parent_roles=[V.validate(sel),V.validate(caller)]
 raw=(G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise RuntimeError('wrong original image')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise RuntimeError('unbacked source')
 if[(r['start'],r['end_exclusive']) for r in v['ranges']]!=[('0x30ce10','0x30cf3f')]:raise RuntimeError('required range population changed')
 for r in v['ranges']+sel['ranges']+caller['ranges']:
  lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for data in [v,sel,caller] for r in data['ranges'] for i in r['instructions']}
 assertions=[(0x30cc6a,'call','0x20e600'),(0x30cc6f,'mov','rcx, qword ptr [rip + 0x2bb24c2]'),(0x30cc76,'movzx','esi, word ptr [rcx + 8]'),(0x30cc7a,'movzx','ecx, word ptr [rbx + 0x1c]'),(0x30cc7e,'imul','esi, ecx'),(0x30cc81,'add','esi, eax'),(0x30cc83,'je','0x30cde6'),(0x30cd93,'mov','rdx, rsi'),(0x30cd96,'mov','rcx, rdi'),(0x30cd99,'call','0x30ce10'),
 (0x30ce1a,'mov','rsi, rcx'),(0x30ce1d,'mov','rbp, rdx'),(0x30ce4d,'call','0x20e600'),(0x30ce59,'mov','edi, ebp'),(0x30ce5b,'sub','edi, eax'),(0x30ce5d,'movzx','ebx, word ptr [rcx + 8]'),(0x30ce64,'call','0x20e600'),(0x30ce69,'mov','rcx, rax'),(0x30ce6c,'xor','edx, edx'),(0x30ce6e,'mov','eax, edi'),(0x30ce75,'div','ebx'),(0x30ce77,'imul','eax, ebx'),(0x30ce7f,'add','eax, ecx'),(0x30ce93,'test','dword ptr [rax + 0xc], 0x40000000'),
 (0x30cf07,'mov','rdx, rbp'),(0x30cf0a,'mov','rcx, rsi'),(0x30cf0d,'call','0x306bd0'),(0x306be0,'mov','rsi, rdx'),(0x306be3,'mov','rdi, rcx'),(0x306c3d,'mov','rdx, rsi'),(0x306c4a,'mov','rcx, rdi'),(0x306c4d,'call','0x309230'),
 (0x309251,'mov','rbx, rdx'),(0x3092a4,'call','0x20e600'),(0x3092b0,'movzx','edx, word ptr [rcx + 8]'),(0x3092b4,'imul','ecx, edx, 0x113'),(0x3092ba,'add','ecx, eax'),(0x3092c0,'cmp','rbx, rcx'),(0x3092c3,'je','0x3092cb')]
 for pc,m,a in assertions:
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('operation changed '+hex(pc))
 body=v['ranges'][0];local={int(i['pc'],16):i for i in body['instructions']};g=G.graph(local,0x30ce10,0x30cf3f)
 if len(g['returns'])!=2 or {t for pc,t in g['calls']}!={'0x20e600','0x306bd0'}:raise RuntimeError('unexpected normalization control boundary')
 M=1<<32;U=(1<<16)-1;k=0x113
 products={'maximum_row_product':U*U,'difference_min':-k*U,'difference_max':(U-k)*U,'modulus':M,'row_domain':[0,U],'nonzero_stride_domain':[1,U]}
 if not(0<=products['maximum_row_product']<M and -M<products['difference_min']<=0<=products['difference_max']<M):raise RuntimeError('integer bound proof failed')
 # For fixed nonzero s, equality moduloM requires(i-k)*s to be a multiple
 # ofM. The original domain bounds it strictly between -M andM, so it must
 # be zero and therefore i=k. Arbitrary B cancels even when B+product wraps.
 # Because i*s<M, ((B+i*s)modM-B)modM ==i*s; DIV32 by s returns exacti
 # and remainder0. Normalization recomposesP, without needing no-add-wrap.
 witnesses=[]
 for B in [0,M-1]:
  for s in [1,32768,U]:
   for i in [0,k,511,U]:
    p=(B+i*s)%M;d=(p-B)%M;q,rem=divmod(d,s);n=(q*s+B)%M;c=(B+k*s)%M
    if d!=i*s or q!=i or rem or n!=p or(p==c)!=(i==k):raise RuntimeError('boundary witness contradicted theorem')
    witnesses.append({'base_low32':B,'row':i,'stride':s,'pointer':p,'recovered_row':q,'remainder':rem,'normalization_preserves_pointer':n==p,'special_comparison_equal':p==c})
 countermodels=[{'case':'zero-stride','row':511,'special_row':k,'stride':0,'equal':True,'limit':'Outside nonzero premise; original DIV by0 not executed'},
 {'case':'broader-row-width','row':k+(1<<17),'special_row':k,'stride':1<<15,'equal':((k+(1<<17))*(1<<15))%M==(k*(1<<15))%M,'limit':'Row exceeds u16; no shipping-width alias'},
 {'case':'broader-stride-width','row':k+(1<<15),'special_row':k,'stride':1<<17,'equal':((k+(1<<15))*(1<<17))%M==(k*(1<<17))%M,'limit':'Stride exceedsu16'},
 {'case':'changed-base','row':511,'producer_base':0,'selector_base':511-k,'stride':1,'equal':True,'limit':'Violates stable low32 resolver base'},
 {'case':'changed-stride','row':511,'producer_stride':k,'selector_stride':511,'base':0,'equal':511*k==k*511,'limit':'Violates stable context stride'}]
 if not all(c['equal'] for c in countermodels):raise RuntimeError('countermodel control failed')
 source_names=['source-01.json','retained/presentation-index-domain-source-01.json','retained/ov42-class20-action-admission-special-admission-callers-raw-01.json']
 result={'producer_complete':True,'method':'A STATIC_ONLY original bounded-width invariant, no native/game execution','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':n,'sha256':sha(src/n)} for n in source_names],'annotation_prerequisites':[roles]+parent_roles,'parent_manifests':pins,'instruction_assertions':len(assertions),'graphs':[{'entry':'0x30ce10','visited':len(g['visited']),'returns':[hex(i) for i in g['returns']],'calls':[{'pc':hex(pc),'target':t} for pc,t in g['calls']]}],
 'bounds':products,'theorem':'With fixed B=u32 low resolver return, s=u16 in1..65535, i=u16 in0..65535 and ordinaryABI/noninterference, P=(B+i*s)mod2^32 is injective in i; P equals specialC=(B+275*s)mod2^32 iff i275. Original DIV normalization recoversi exactly and recomposesP even if addition wraps.',
 'reason':'i*s<2^32; -2^32<(i-275)*s<2^32. The only multiple of2^32 in that latter open interval is0; s>0 impliesi275. B cancels in modular equality/subtraction. DIV32 has EDX0 and numeratori*s, quotienti/remainder0.',
 'boundary_witnesses':witnesses,'countermodels':countermodels,'caller_limits':'Retained30CBFC..30CD9E prefix and306BD0 prefix, not full caller/interpreter closure. Normal-return calls preserve nonvolatile RSI/RBP/entrypoint arguments by ABI; actual helper effects and pointer availability not proved.',
 'established':['No other u16 row can select309230 equal-table branch through this source producer under stable nonzero u16 stride/base premises','30CE10 record normalization preserves produced row pointer under those premises; no no-add-wrap premise needed','Row275 is the precise remaining equal-branch type-admission question; other row u16 selectors stay under their separate authored bounds'],
 'unresolved':['Natural base/stride/context stability/initialization and externalcall effects','Natural row275 actor type27..39 admission and actual metadata/loaded pointers','Other caller/value producers, allocations/lifetime/interference, wholeOV42/21 rejection/consequences'],
 'limits':'24 algebraic boundary witnesses/five broadened-domain countermodels are not executions or substitute for the interval proof. No shipped header/9-table census repeated. Parent producer proof valid but independent acceptance pending, not assumed.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'theorem':'equal branch iff row275 under stated premises','row_product_max':U*U,'difference_interval':[products['difference_min'],products['difference_max']],'pins':len(assertions),'native_game_runs':0}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output)
