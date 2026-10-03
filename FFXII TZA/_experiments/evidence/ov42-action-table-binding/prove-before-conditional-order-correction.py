"""Original binder dataflow and exact limits of pointer/stride stability.

Method A only. Arithmetic countermodels are not native executions or shipped
reachability. Full call-window stability is deliberately not inferred.
"""
import copy,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def receipt(tag,driver):
 s=json.loads((P/(tag+'.status.json')).read_text())
 need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==sha(P/driver),'required successful current '+tag)
 need((P/(tag+'.stdout')).read_bytes() and not(P/(tag+'.stderr')).read_bytes(),'required nonempty clean '+tag)
 return dict(path=tag+'.status.json',sha256=sha(P/(tag+'.status.json')))
def derive(ix,G):
 ops=[(0x236d7b,'mov','rax, qword ptr [rip + 0x1e578fe]'),(0x236d82,'mov','ecx, dword ptr [rax + 0x3c]'),(0x236d85,'call','0x237fc0'),
 (0x237fcf,'movsxd','rdx, ecx'),(0x237fd5,'lea','rcx, [rip + 0x2c8715c]'),(0x237fde,'call','0x3845f0'),
 (0x3845f4,'mov','qword ptr [rcx], rdx'),(0x3845f7,'test','rdx, rdx'),(0x3845fa,'je','0x3846e7'),
 (0x384600,'mov','eax, dword ptr [rdx + 0xc]'),(0x384608,'test','eax, eax'),(0x38460a,'je','0x384611'),(0x38460c,'add','eax, edx'),(0x38460e,'mov','dword ptr [rdx + 0xc], eax'),
 (0x384647,'mov','eax, dword ptr [rdi + 0x14]'),(0x38464a,'test','eax, eax'),(0x38464c,'je','0x3846e2'),(0x384652,'add','eax, edx'),(0x384659,'mov','ecx, eax'),(0x38465b,'mov','ebp, eax'),(0x38465d,'call','0x20e620'),(0x384662,'mov','dword ptr [rdi + 0x14], eax'),
 (0x384665,'test','rbp, rbp'),(0x384668,'je','0x3846dd'),(0x384680,'call','0x20e600'),(0x384688,'movzx','r14d, word ptr [rax]'),(0x38468c,'call','0x20e600'),(0x384698,'cmp','rsi, r14'),(0x38469b,'lea','rbx, [rax + 4]'),(0x38469f,'je','0x3846b9'),(0x3846a3,'xor','r8d, r8d'),(0x3846a9,'add','edx, ebp'),(0x3846b2,'call','0x3846f0'),(0x3846b9,'add','dword ptr [rbx], ebp'),
 (0x384701,'mov','rcx, rdx'),(0x384704,'call','0x20e620'),(0x384709,'mov','dword ptr [rdi], eax'),(0x384720,'call','0x20e600'),(0x38472a,'call','0x20e600'),(0x384750,'test','ecx, ecx'),(0x384752,'je','0x384780'),(0x384780,'add','dword ptr [rbx], ebp'),
 (0x20e600,'mov','eax, ecx'),(0x20e602,'add','rax, qword ptr [rip + 0x1d74f27]'),(0x20e609,'ret',''),(0x20e620,'sub','ecx, dword ptr [rip + 0x1d74f0a]'),(0x20e626,'mov','eax, ecx'),(0x20e628,'ret','')]
 for pc,m,a in ops:need(pc in ix and (ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'binding operation changed '+hex(pc))
 need(ix[0x237fd5]['memory'][0]['rip_target']=='0x2ebf138' and ix[0x237fd5]['memory'][0]['role']=='addr','wrong action slot/address role')
 need(ix[0x236d7b]['memory'][0]['rip_target']=='0x208e680','wrong delivered directory')
 need(ix[0x20e602]['memory'][0]['size']==8 and ix[0x20e620]['memory'][0]['size']==4 and all(ix[p]['memory'][0]['rip_target']=='0x1f83530' for p in [0x20e602,0x20e620]),'arena read width/identity changed')
 binder=G.graph(ix,0x3845f0,0x3846ec)
 need(G.dominates(binder,0x3845f4,0x38460e),'row rewrite precedes slot publication')
 need(G.dominates(binder,0x38460e,0x38465d),'nested encoder can precede row rewrite')
 need(G.dominates(G.graph(ix,0x237fc0,0x238154),0x237fde,0x238059),'action wrapper bypasses binder')
 fields=[]
 for load,test,branch,add,store,base,offset in [(0x384600,0x384608,0x38460a,0x38460c,0x38460e,'rdx',12),(0x384614,0x384618,0x38461a,0x38461c,0x38461e,'r8',16),(0x384625,0x384629,0x38462b,0x38462d,0x38462f,'r8',24),(0x384636,0x38463a,0x38463c,0x38463e,0x384640,'r8',28)]:
  need(ix[load]['args']==f'eax, dword ptr [{base} + {hex(offset)}]' and ix[test]['args']=='eax, eax' and ix[branch]['mnemonic']=='je' and ix[add]['args']=='eax, edx' and ix[store]['args']==f'dword ptr [{base} + {hex(offset)}], eax','nonzero scalar rebase differs')
  fields.append(dict(offset=hex(offset),load=hex(load),store=hex(store),effect='x==0 ? 0 : low32(x+low32(D))'))
 # Complete decoder/encoder leaves, not omitted callback stubs.
 need([i for pc,i in sorted(ix.items()) if 0x20e600<=pc<0x20e60a]==[ix[p] for p in [0x20e600,0x20e602,0x20e609]],'decoder leaf not complete')
 need([i for pc,i in sorted(ix.items()) if 0x20e620<=pc<0x20e629]==[ix[p] for p in [0x20e620,0x20e626,0x20e628]],'encoder leaf not complete')
 # Supplied arithmetic checks tied to the verified instructions, not executions.
 u32=lambda n:n&0xffffffff;u64=lambda n:n&0xffffffffffffffff
 decode=lambda a,e:u64(a+u32(e));encode=lambda a,m:u32(m-u32(a))
 D=0x100000;before=0x20;first=u32(D+before);second=u32(D+first)
 need(first!=second,'same-pointer rebind countermodel does not discriminate')
 rebind=dict(descriptor_pointer=hex(D),arena=0,input_row_offset=hex(before),first_stored_rows=hex(first),second_stored_rows=hex(second),first_decoded_low32=hex(u32(decode(0,first))),second_decoded_low32=hex(u32(decode(0,second))),same_slot_pointer=True,other_relocated_fields_zero=True,executed=False,limits='Valid supplied descriptor storage and disjoint slot; no claim that the game naturally binds the same prepared descriptor twice.')
 arena=0x100001000;subdir=u32(D+0x100);encoded=encode(arena,subdir);decoded=decode(arena,encoded)
 need(u32(decoded)==subdir and decoded!=subdir,'encoder/decoder projection control does not discriminate')
 inverse=dict(arena=hex(arena),rebased_subdir_low32=hex(subdir),stored_encoded=hex(encoded),decoded_full64=hex(decoded),low32_roundtrip=True,full64_pointer_equality=False,executed=False)
 # Count-zero directory at D+4: its last entry is D+8. This names the exact
 # original store that invalidates an unqualified whole-call stride claim.
 stride=60;subdir=D+4;last_entry=subdir+4;after=u32(stride+subdir)
 need(last_entry==D+8 and (after&65535)!=stride,'directory alias control fails')
 alias=dict(arena=0,descriptor=hex(D),input_subdirectory_field=4,directory_word_count=0,directory=hex(subdir),last_entry_address=hex(last_entry),original_store='0x3846b9',before_stride=60,after_stride=after&65535,after_dword=hex(after),executed=False,limits='Constructed overlapping generic descriptor, not a stock action-table sample or natural malformed-resource reachability. Whole-call preservation needs a disjointness/valid-layout premise.')
 return dict(action_binding={'directory':'QWORD[0208E680], field DWORD+3C at236D82','wrapper':'237FC0 signextends ECX intoRDX and passes address02EBF138 to3845F0','slot_publication':'QWORD store3845F4 occurs before nonnull validation/field rebase; not atomic initialization proof'},scalar_fields=fields,
 rows='For a nonzero +C, binder writes low32(+C+low32(D)) without calling20E620; zero stays zero. Decoder consumes that stored DWORD and reads the fullQWORD arena. Same descriptor pointer therefore does not imply the same decoded rows-base after another bind.',
 subdirectory='For initial +14!=0: M=low32(+14+low32(D)); store E=low32(M-low32(A)) through20E620. If M!=0, decode E through20E600 and visit nested directory; +14 stores an encodedDWORD, not a resolved pointer. Decoder=low64(A64+zeroextend32(E)); only low32 roundtrip is universal under unchanged arena.',
 fixed_header_writes='No direct fixed-displacement stores to descriptor+4/+8 in3845F0. Nested directory/child entry writes can alias that storage unless validated resource layout/disjointness rules it out; do not promote direct-field footprint to unconditional whole-call preservation.',
 child='Outer first count entries call3846F0 withR8D=0. Child stores encoder result to the entry slot, decodes child directory, and its zero-depth branch adds child base to each count+1 entry without recursive calls. Callee interpretation assumes valid nonoverlapping storage/ordinary ABI and unchanged arena between paired encode/decode reads.',
 resolver='Complete20E600 and20E620 leaves have no calls and no memory stores. They cannot themselves mutate table or arena; scheduling/concurrent writers and omitted callers remain separate.',countermodels=[rebind,inverse,alias],
 remaining='No complete writer/alias/callback/concurrency closure across304934 ->304F4D ->3068A7/3068B2 is established. Registrar completion, resource reuse/free, arena reassignment and normal command reachability remain OPEN. Existing quotient bound remains conditional on equal low32 rows-base/equal positiveWORD stride.',
 consumer_changes=['RegistryAG12: replace resolved20E620/pointer wording with encoder then actual20E600 decode; qualify +4/+8 preservation by direct writes versus nested aliases.','OV42: do not substitute pointer equality for row-base equality; retain binder/reload/arena/disjointness premises until original call-window writers are excluded.','OPUS: preserve DWORD encoder/QWORD decoder widths, signextended descriptor wrapper and slot-store-before-rebase ordering.'])
def main():
 out=P/sys.argv[1];need(not out.exists(),'immutable output exists')
 receipts=[receipt('binding-extents-01','prepare-binding-extents.py'),receipt('binding-capture-01','capture-binding.py'),receipt('binding-helper-extents-01','prepare-binding-helper-extents.py'),receipt('binding-helper-capture-01','capture-binding-helpers.py')]
 origins=[]
 for file in ['resolver-lineage-01.json','encoder-lineage-01.json']:
  x=json.loads((P/file).read_text());b=(P/x['copy']).read_bytes();need(hashlib.sha256(b).hexdigest()==x['sha256'],'retained source changed')
  t=subprocess.run(['git','ls-tree','-z',x['commit'],'--',x['member']],capture_output=True,timeout=15);need(t.returncode==0 and not t.stderr and t.stdout,'retained Git tree unavailable');oid=t.stdout.split(b'\t')[0].split()[-1].decode()
  t=subprocess.run(['git','cat-file','blob',oid],capture_output=True,timeout=15);need(t.returncode==0 and not t.stderr and t.stdout==b,'retained Git bytes differ');origins.append(x)
 need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed dependencies changed')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'wrong executable')
 pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');ix={};annotations=[]
 files=['binding-source-01.json','binding-helper-source-01.json','retained-resolver-source-01.json','retained-encoder-source-01.json']
 for f in files:
  x=json.loads((P/f).read_text());need(x.get('exe_sha256')==PIN,'wrong source image');annotations.append(V.validate(x))
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original bytes')
   for i in r['instructions']:
    pc=int(i['pc'],16);need(pc not in ix or ix[pc]==i,'overlapping annotation differs');ix[pc]=i
 # Restrict leaves to exact original extents, while retaining immutable full
 # maps/lineage above. Other retained functions are not new scientific samples.
 facts=derive(ix,G)
 with out.open('x') as f:json.dump(dict(producer_complete=True,method='A original shipping bytes/static dataflow and arithmetic countermodels',exe_sha256=PIN,driver_sha256=sha(Path(__file__)),source_pins=[dict(path=f,sha256=sha(P/f)) for f in files],annotation_prerequisites=annotations,prerequisite_receipts=receipts,retained_lineage=origins,facts=facts,acceptance='Producer evidence only; independent review and canonical incorporation pending',cleanup='No FF12 process, native/emulated execution, PC control, instrumentation, save/config/reference or peer changes.'),f,indent=2)
 print('PROVED slot38 binder dataflow; same-pointer rebind is not rows-base invariance;20E620 encodes; stride preservation needs alias bounds')
if __name__=='__main__':main()
