"""Original rig configured-index-list/core-link/rebase-guard proof. No machine-code execution or gameplay."""


import hashlib,importlib.util,json,struct,sys


from pathlib import Path


sys.dont_write_bytecode=True


P=Path(__file__).resolve().parent


ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())


sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def load(n,f):


 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:


 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')


V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')


status=json.loads((P/'capture-01.status.json').read_text())


if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')


x=json.loads((P/'source-01.json').read_text())


if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture incomplete')


roles=V.validate(x)


raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()


PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'


if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image changed')


pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]


secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]


def read(a,n):


 for vs,rva,sz,off in secs:


  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]


 raise RuntimeError('unbacked source')

lineage=json.loads((P/'lineage.json').read_text())
if lineage['parent_manifest_sha256']!='8cb0df4be7349c2523018eccfe053e409ce6898a07c7a6949644b6dfd1a4212e':raise RuntimeError('retained parent identity changed')
for row in lineage['retained_files']:
 if sha(P/'retained'/row['path'])!=row['sha256']:raise RuntimeError('retained input changed')
parent=json.loads((P/'retained/manifest.json').read_text())
if sha(P/'retained/manifest.json')!=lineage['parent_manifest_sha256']:raise RuntimeError('retained manifest changed')
for row in lineage['retained_files']:
 if row['path']!='manifest.json' and not any(q['path']==row['path'] and q['sha256']==row['sha256'] for q in parent['members']):raise RuntimeError('unbound retained member')
ps=json.loads((P/'retained/capture-01.status.json').read_text())
if ps.get('terminal') is not True or ps.get('exit')!=0 or ps.get('exception') is not None or ps['driver_sha256']!=sha(P/'retained/capture.py') or not(P/'retained/capture-01.stdout').read_bytes() or(P/'retained/capture-01.stderr').read_bytes():raise RuntimeError('required retained capture failed')
y=json.loads((P/'retained/source-01.json').read_text());parent_roles=V.validate(y)
if y.get('wrapper_complete') is not True or y['invocation_driver_sha256']!=sha(P/'retained/capture.py') or y['exe_sha256']!=PIN:raise RuntimeError('retained source identity failed')

codec_status=json.loads((P/'retained/retained/capture-01.status.json').read_text())
if codec_status.get('terminal') is not True or codec_status.get('exit')!=0 or codec_status.get('exception') is not None or codec_status['driver_sha256']!=sha(P/'retained/retained/capture.py') or not(P/'retained/retained/capture-01.stdout').read_bytes() or(P/'retained/retained/capture-01.stderr').read_bytes():raise RuntimeError('required retained codec capture failed')
z=json.loads((P/'retained/retained/source-01.json').read_text());codec_roles=V.validate(z)
if z.get('wrapper_complete') is not True or z['invocation_driver_sha256']!=sha(P/'retained/retained/capture.py') or z['exe_sha256']!=PIN:raise RuntimeError('retained codec identity failed')

if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x3e1c50','0x3e2800'),('0x3e3c30','0x3e3c9d'),('0x421d20','0x421d66')]:raise RuntimeError('required rig source population changed')
ix={};graphs=[];gb={}
for r in x['ranges']+y['ranges']+z['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b,tail='0x20e600' if a==0x421d20 else None)
 if set(local)!=g['visited']:raise RuntimeError('unaccounted original rig source')
 gb[a]=g;graphs.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls'],'tails':[hex(q) for q in g['tails']]})
ops='''3e1c50|test|rcx, rcx
3e1c53|je|0x3e27ff
3e1c5e|mov|rdi, rcx
3e1c66|mov|ecx, dword ptr [rcx + 0x70]
3e1c6e|call|0x20e600
3e1c73|xor|ebx, ebx
3e1c75|test|rax, rax
3e1c78|je|0x3e1cc6
3e1c7a|movzx|eax, word ptr [rdi + 0x68]
3e1c7e|cmp|ax, -1
3e1c88|movsx|rax, ax
3e1c8c|imul|rcx, rax, 0x740
3e1c93|add|rcx, qword ptr [rip + 0x1ee528e]
3e1c9a|cmp|dword ptr [rcx + 0x284], ebx
3e1ca0|cmove|rcx, rbx
3e1ca4|call|0x20e620
3e1cab|mov|dword ptr [rdi + 0x70], eax
3e1cae|call|0x20e600
3e1cb3|mov|rcx, rax
3e1cb6|call|0x421d20
3e1cbb|mov|rcx, rax
3e1cbe|call|0x20e620
3e1cc3|mov|dword ptr [rdi + 0x78], eax
3e1d49|mov|eax, dword ptr [rdi + 0x84]
3e1d4f|cmp|eax, edi
3e1d51|je|0x3e27f0
3e1d57|mov|ecx, dword ptr [rdi + 0x88]
3e1d62|test|eax, eax
3e1d64|jne|0x3e22b7
3e1d6a|and|byte ptr [rdi + 0x5f], 0xfd
3e1d6e|call|0x20e600
3e1d73|lea|ecx, [rdi + rax]
3e1d76|call|0x20e620
3e1d7d|mov|dword ptr [rdi + 0x88], eax
3e22b7|mov|esi, edi
3e22b9|sub|esi, eax
3e22bb|call|0x20e600
3e22c0|lea|ecx, [rsi + rax]
3e22c3|call|0x20e620
3e22ca|mov|dword ptr [rdi + 0x88], eax
3e27e5|mov|rsi, qword ptr [rsp + 0x38]
3e27ea|mov|dword ptr [rdi + 0x84], edi
421d26|mov|ebx, dword ptr [rcx + 0x18]
421d29|cmp|ebx, -1
421d2c|je|0x421d5e
421d2e|mov|ecx, dword ptr [rcx + 0x10]
421d31|call|0x20e600
421d3b|mov|rcx, qword ptr [rax + 0xd98]
421d42|mov|edx, ebx
421d44|call|0x2ed570
421d49|test|rax, rax
421d4c|je|0x421d5e
421d4e|mov|ecx, dword ptr [rax + 0x84]
421d59|jmp|0x20e600
421d5e|xor|eax, eax
3e3c3f|mov|rsi, rcx
3e3c42|mov|ecx, dword ptr [rcx + 0x88]
3e3c48|call|0x20e600
3e3c4d|xor|edi, edi
3e3c4f|mov|rbx, rax
3e3c52|cmp|dword ptr [rsi + 0x8c], edi
3e3c58|jbe|0x3e3c8d
3e3c60|mov|ecx, dword ptr [rsi + 0x78]
3e3c63|call|0x20e600
3e3c68|mov|ecx, dword ptr [rbx]
3e3c6a|add|rax, 0x230
3e3c70|imul|rcx, rcx, 0x290
3e3c77|add|rcx, rax
3e3c7a|call|0x203170
3e3c7f|inc|edi
3e3c81|lea|rbx, [rbx + 4]
3e3c85|cmp|edi, dword ptr [rsi + 0x8c]
3e3c8b|jb|0x3e3c60
20e600|mov|eax, ecx
20e602|add|rax, qword ptr [rip + 0x1d74f27]
20e620|sub|ecx, dword ptr [rip + 0x1d74f0a]
20e626|mov|eax, ecx'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required rig operation changed '+hex(pc))
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for regs,lo,hi in [({'rdi','edi','di','dil'},0x3e1c61,0x3e27ea),({'rax','eax','ax','al','ah'},0x3e1d4f,0x3e1d62),({'rsi','esi','si','sil'},0x3e22bb,0x3e22ca)]:
 for pc in sorted(q for q in ix if lo<=q<hi):
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
  if {i.reg_name(r) for r in wr}&regs:raise RuntimeError('rig carrier changed '+hex(pc))
for a,b in [(0x3e1d49,0x3e1d7d),(0x3e1d49,0x3e22ca),(0x3e1d7d,0x3e22b7)]:
 if a==0x3e1d7d:continue # Fresh path need not dominate relocation path.
 if not G.dominates(gb[0x3e1c50],a,b):raise RuntimeError('rig cache load doesnot dominate write')
# Exact local paths settle skip semantics independently of opaque effects.
if gb[0x3e1c50]['edges'][0x3e1d51]!=[0x3e27f0,0x3e1d57]:raise RuntimeError('same-self early exit changed')
direct={}
for pc,i in ix.items():
 if not 0x3e1c50<=pc<0x3e2800:continue
 for m in i['memory']:
  if m['base']=='rdi' and m['displacement'] in [0x78,0x84,0x88,0x8c] and m['role']!='addr':direct.setdefault(hex(m['displacement']),[]).append({'pc':hex(pc),'role':m['role'],'size':m['size'],'args':i['args']})
if sorted(int(r['pc'],16) for r in direct['0x88'] if r['role']=='w')!=[0x3e1d7d,0x3e22ca] or '0x8c' in direct:raise RuntimeError('rig supplied direct field census changed')
if direct['0x84'][-1]['args']!='dword ptr [rdi + 0x84], edi':raise RuntimeError('rawself store changed')
U=1<<32;MASK=U-1;M64=(1<<64)-1
def rebase(base,ref,delta):
 decoded=(base+ref)&M64
 ecx=(decoded+delta)&MASK
 return (ecx-(base&MASK))&MASK
examples=[]
for base,oldref,rig,oldself in [(0,0x100,0xcb006000,0),(0,0xcb006100,0xcb106000,0xcb006000),(0,0xcb006100,0xcb006000,0xcb006000),(0x1000,0x100,0xcb006000,0)]:
 cur=rig&MASK
 if oldself==cur:kind='same-lowself';new=oldref
 else:kind='fresh' if oldself==0 else 'relocated';delta=cur if oldself==0 else (cur-oldself)&MASK;new=rebase(base,oldref,delta)
 examples.append({'base':hex(base),'old88':hex(oldref),'rig':hex(rig),'old_rawself84':hex(oldself),'branch':kind,'new88':hex(new),'decoded_new88':hex((base+new)&M64)})
if examples[0]['new88']!='0xcb006100' or examples[1]['new88']!='0xcb106100' or examples[2]['branch']!='same-lowself':raise RuntimeError('source rebase calculation failed')
result={'producer_complete':True,'method':'A STATIC_ONLY rig index-list/core-link/selfcache source proof','driver_sha256':sha(Path(__file__)),
 'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','retained/source-01.json','retained/retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles,codec_roles],'instruction_assertions':len(ops.splitlines()),'graphs':graphs,'direct_rig_fields':direct,
 'rig78':'When initialDecode(rig70) isnonnull, 3E1C50 derivesCharacterRenderRecord fromsigned16rig68 andglobal022C6F28/stride740/active284 gate, encodes70, calls421D20 thenstoresEncode(result) in78. Ifinitialdecoded70==0, thisdirect78assignment is skipped (noimplicitclear).',
 'borrowed_core':'421D20 readsinputCharacterRenderRecord18 index; -1/missingrow returns0. OtherwiseDecode(record10)->rootD98 pool lookup2ED570(index)->row84 decoded. Distinctobjects: RenderStrideC0Element84 encodedresolvedworkspace fromretainedproducer, rig84 rawlowself cache.',
 'rig84':'LoadDWORD84 at3E1D49, comparewithEDI=low32(actualrigaddress). Equal jumps3E27F0 before88rebasing/controllerinit/self84store. Unequal: zero oldself selectsfresh path, nonzero selectsdelta path. Normalcompletedfullpath storesEDI directly84 at3E27EA, no encoder. Validnonalias/nativeABI/stablebase premises; not lifetimeidentityguarantee.',
 'rig88':'Fresh storeslow32(old88+low32(rig)) afterDecode/LEAECX/Encode; relocation storeslow32(old88+delta), delta=low32(currentrig-old_rawself84). Base stability required for cancellation. Same-lowself path skips88write butearlier70/78refresh stilloccurs conditionally.',
 'idempotence_limits':'Localsame-low32self guard prevents repeatedlistrebase, notfullnativecontroller-idempotence/healthy-session proof. Pointers differingby4GiB aliascache; nonzeroactualpointerwithlow32zero collidescoldcache0. Actualvalidallocator addressdomain unknownhere. Underarbitrarynonzerobase rawauthoredoffset isnot automatically a portablepointer; exactDecode outcome retained.',
 'rig8C':'No directRDI8C access in suppliedfixupbody. Resetreader consumesDWORD8C asunsignedloopcount. Rawblob/copy/default initialization andindirectcallee effects/allwriters remainseparate; no constructor-default claim.',
 'reset':'3E3C30 decodes88 first. Count0 skipslist dereference/native203170 calls. ForcountN>0, eachunsignedDWORD listindex i yieldsRCX=Decode(rig78)+230h+i*290h (64bit arithmetic), invokes203170, advanceslist4bytes andEDI unsigneduntilcount. No perindexbonecount/range check in thisbody; validstablelist/core extent andnativecallee effects notproved.',
 'mathematical_rebase_controls':examples,
 'limits':['No native/originalemulator/live execution orobservedrelocation/controller effects; examplesarefixed-widthsourcecalculations',
 'Complete suppliedlocalbodies andnamedlookup tail, notcompleteallwriters/callers/opaque effectgraph ornaturalinitialization/reachability',
 'Normalvalidobjects/privateframes/ABI andnoalias/interference required; opaque2ED570/nativecontrollerhelpers notprovedby stubs',
 'CopiedFCPsection2 source alreadycanonical UQ220; no recensus orclaimofnewauthored/physicalprocess samples',
 'Actuallistcount/data extent/indexvalidity/allocatedbelow4GiB/coreownership/lifetime/reuse/multithread scheduling remainOPEN',
 'Parentproducer/currentpositivefacts notindependentacceptance; count8C isnot assertedinitializeddefault orpreservedagainstopaquealiases',
 'EXP127INVALID_POST_TRACE unchanged; no parkedmenu/native/game/K14rerun or wholeOVclosure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED rig78 borrowed core,84 rawlowself cache,88 fresh/delta rebase andunsignedreset reader; STATIC_ONLY')
