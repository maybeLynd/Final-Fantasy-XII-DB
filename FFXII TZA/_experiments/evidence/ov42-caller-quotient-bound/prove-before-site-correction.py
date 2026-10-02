"""Compose original current-row and queue instructions with an integer invariant.

No new code capture, emulation or game observation. Equality of the construction
and queue table bindings is a premise to resolve, not a manufactured fixture.
"""
import copy,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def module(n,file):
 s=importlib.util.spec_from_file_location(n,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,targets,G):
 ops=[(0x30487f,'lea','rsi, [rcx + 0x6b0]'),(0x30488d,'movzx','r13d, word ptr [rsi + 0x64]'),(0x3048de,'cmp','r13w, bx'),(0x3048e2,'ja','0x305017'),(0x3048a8,'mov','ebx, 0x21e'),(0x30491a,'call','0x20e600'),(0x30491f,'mov','r15, rax'),(0x304929,'movzx','ecx, word ptr [rax + 8]'),(0x30492d,'movzx','eax, r13w'),(0x304931,'imul','ecx, eax'),(0x304934,'add','r15d, ecx'),(0x304939,'mov','r15, r14'),(0x304f47,'mov','rdx, r15'),(0x304f4d,'call','0x306760'),
 (0x306775,'mov','rdi, rdx'),(0x3067aa,'mov','eax, dword ptr [rip + 0x1fbb9ac]'),(0x3067b0,'dec','eax'),(0x3067b7,'cmp','eax, 5'),(0x3067ba,'ja','0x306a9a'),(0x3068a4,'call','0x20e600'),(0x3068a7,'sub','edi, eax'),(0x3068a9,'xor','edx, edx'),(0x3068b2,'movzx','ecx, word ptr [rax + 8]'),(0x3068b6,'mov','eax, edi'),(0x3068b8,'div','ecx'),(0x3068bd,'mov','edx, 0xffff'),(0x3068c2,'cmp','ax, dx'),(0x3068c5,'je','0x3068d1'),(0x3068c7,'movzx','eax, ax'),(0x3068ca,'sub','eax, 0xd0'),(0x3068d1,'or','eax, 0xffffffff'),(0x3068d4,'mov','dword ptr [rip + 0x1fb98fe], eax')]
 for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'composition operation changed '+hex(pc))
 a=copy.deepcopy(ix);a[0x30495a]['args']=hex(targets[9]);caller=G.graph(a,0x304850,0x305042)
 need(G.dominates(caller,0x3048de,0x304f4d) and G.dominates(caller,0x3048e2,0x304f4d),'current ID upper guard can be bypassed')
 arm=G.graph(ix,0x306848,0x306aef)
 need(all(G.dominates(arm,p,0x3068d4) for p in [0x3068a7,0x3068a9,0x3068b2,0x3068b8]),'quotient pipeline bypasses queue store')
 # Every positive16-bit divisor. The bound is checked once as an inequality,
 # not35,519,970 artificial execution samples. IMUL's low32 result is exact
 # here; low32 ADD/SUB cancellation holds for every possible base.
 maximum_id=int(ix[0x3048a8]['args'].split(',')[1],0);maximum_stride=(1<<16)-1
 maximum_product=maximum_id*maximum_stride;modulus=1<<32;bias=int(ix[0x3068ca]['args'].split(',')[1],0)
 need(maximum_id==542 and 0<maximum_product<modulus and maximum_id<0xffff,'product/narrowing bound invalid')
 domain=[[0,maximum_id-bias],[modulus-bias,modulus-1]]
 excluded=[511,534];need(all(b<excluded[0] or a>excluded[1] for a,b in domain),'disputed queue band intersects coherent domain')
 examples=[]
 for base,ident,stride in [(0xfffffff0,542,65535),(0xffffffff,208,60),(0x100000,0,1),(0x100000,207,65535)]:
  row=(base+ident*stride)&0xffffffff;difference=(row-base)&0xffffffff;q=difference//stride;value=(q-bias)&0xffffffff
  need(q==ident,'modular cancellation control failed');examples.append(dict(base=hex(base),id=ident,stride=stride,row=hex(row),quotient=q,queue=hex(value),class_='Mathematical boundary check, not native execution'))
 # Countermodels break exactly a named premise, and produce a disputed value.
 models=[]
 for label,ident,bc,sc,bq,sq in [('base-changed',208,0x100000,60,0x100000-(719-208)*60,60),('stride-changed',360,0x100000,60,0x100000,30),('ID-guard-removed',720,0x100000,60,0x100000,60)]:
  row=(bc+ident*sc)&0xffffffff;q=((row-bq)&0xffffffff)//sq;value=((q&0xffff)-bias)&0xffffffff
  need(511<=value<=534,'countermodel does not discriminate')
  models.append(dict(violated=label,id=ident,construction_base=hex(bc),construction_stride=sc,queue_base=hex(bq),queue_stride=sq,quotient=q,queue=value,executed=False))
 return dict(original_bound='Latched entryWORD unit+714 is unsigned<=542 before the terminal call. Valid non-NULL row construction and ordinary ABI carrier retention are premises.',equation='R=low32(Bc+i*Sc); D=(R-Bq) mod2^32; q=floor(D/Sq). If low32(Bc)==low32(Bq), Sc==Sq=S>0, i<=542, then i*S<=35,519,970<2^32, hence D=i*S and q=i. This holds for every low32 base, including wrapped ADD.',coverage='All543 admitted IDs and all65,535 positive unsigned16-bit strides by inequality/modular proof, not an executed state count.',maximum_product=maximum_product,queue_domain=domain,queue_sentinel='qFFFF cannot occur under this bound; i207 nevertheless produces DWORDFFFFFFFF by subtraction. Do not treat that collision as naturally admitted kind4.',excluded_queue_band=excluded,answer='The kind4 own queue store cannot emit DWORD511..534 under the stated caller construction/queue binding equality. Same owner, identical prior classifier row and kind4 classifier quotient208..225 are not needed for this weaker bound; kind4 dispatch is still required for the store.',weaker_required_binding=['Same construction and queue lookup base low32','Same positive unsigned16-bit construction multiplier and queue divisor','Caller R15 retained until306760 and queue RDI retained to quotient under actual ABI/noninterference'],unproved='Equality of actual descriptor/resolver bindings across original helper/callback calls, initialized resources, pointer validity, natural phase entry and later writers. Different owner alone does not explain the band under equal bindings, but ownership remains a separate lifetime/semantic obligation.',boundary_checks=examples,countermodels=models,limits='STATIC_ONLY mathematical composition of verified original instructions; no reconstructed fixture is promoted to original execution or natural reachability.')
def main():
 out=Path(sys.argv[1]);out=out if out.is_absolute() else P/out;need(not out.exists(),'immutable result exists')
 origins=json.loads((P/'lineage.json').read_text());need(len(origins)==4,'retained source population differs')
 for row in origins:
  q=P/row['copy'];need(sha(q)==row['sha256'],'retained member changed')
  z=subprocess.run(['git','show',row['commit']+':'+row['member']],capture_output=True,timeout=15)
  need(z.returncode==0 and not z.stderr and z.stdout==q.read_bytes(),'retained Git identity unavailable/different')
 need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed dependencies changed')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed')
 pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');ix={};annotations=[];files=['caller-source-01.json','caller-source-02.json','queue-source-01.json']
 for f in files:
  x=json.loads((P/f).read_text());need(x['exe_sha256']==PIN,'wrong source image');annotations.append(V.validate(x))
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original instructions')
   for i in r['instructions']:
    pc=int(i['pc'],16);need(pc not in ix or ix[pc]==i,'overlapping source differs');ix[pc]=i
 carrier=json.loads((P/'carrier-result-01.json').read_text());z=bytes.fromhex(next(q for q in carrier['original_data'] if q['address']=='0x305044')['bytes']);need(z==read(0x305044,52),'retained phase table differs');targets=[0x120000+n for n in struct.unpack('<13I',z)]
 need(0x120000+struct.unpack('<6I',read(0x306af0,24))[3]==0x306848,'kind4 original dispatch target differs')
 facts=derive(ix,targets,G)
 with out.open('x') as f:json.dump(dict(producer_complete=True,method='A retained original-code/dataflow + modular invariant',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=f,sha256=sha(P/f)) for f in files],retained_lineage=origins,annotation_prerequisites=annotations,facts=facts,acceptance='Producer proof only; independent review/canonical incorporation pending.',cleanup='No PC/game/native/emulator/save/config/reference/peer changes. All finite child calls terminated.'),f,indent=2)
 print('PROVED conditional queue bound0..334 orFFFFFF30..FFFFFFFF;511..534 excluded without owner/classifier-row equality')
if __name__=='__main__':main()
