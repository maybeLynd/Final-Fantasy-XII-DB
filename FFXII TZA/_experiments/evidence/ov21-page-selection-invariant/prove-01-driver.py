"""Conditional original bank-page search/link proof. No machine-code execution or gameplay."""


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
if lineage['parent_manifest_sha256']!='c78420f604a4763f41074eec85b307eea39750b008623b4b28d38bc6e9cec70b':raise RuntimeError('retained parent identity changed')
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
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x51f6b0','0x51f79c'),('0x51f880','0x51f9e5')]:raise RuntimeError('required source population changed')
ix={};graphs=[]
for r in x['ranges']+y['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 if a in [0x51f6b0,0x51f880,0x51f7a0]:
  g=G.graph(local,a,b)
  if set(local)!=g['visited']:raise RuntimeError('unaccounted local source')
  graphs.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls']})
ops='''51fa19|mov|qword ptr [rcx + 0x18], 0xffffffffffffffff
51f6bf|movzx|eax, word ptr [rcx + 0x24]
51f6c3|xor|ebp, ebp
51f6c8|mov|edi, ebp
51f6ca|cmp|word ptr [rcx + 0x22], ax
51f6ce|jl|0x51f6e3
51f6d0|or|eax, 0xffffffff
51f6e2|ret|
51f6e8|mov|esi, ebp
51f6f4|movzx|edi, word ptr [rbx + 0x20]
51f706|movsx|rdi, di
51f70a|shl|rdi, 5
51f70e|add|rdi, qword ptr [rbx + 0x10]
51f712|cmp|dword ptr [rdi], -1
51f715|je|0x51f730
51f717|inc|word ptr [rbx + 0x20]
51f71b|inc|esi
51f71d|movzx|eax, word ptr [rbx + 0x24]
51f721|cmp|word ptr [rbx + 0x20], ax
51f725|jl|0x51f72b
51f727|mov|word ptr [rbx + 0x20], bp
51f72b|cwde|
51f72c|cmp|esi, eax
51f72e|jl|0x51f6f0
51f730|movsx|eax, word ptr [rbx + 0x24]
51f734|cmp|esi, eax
51f736|jne|0x51f73d
51f738|or|eax, 0xffffffff
51f73d|movsx|eax, word ptr [rbx + 0x20]
51f741|mov|dword ptr [rdi], eax
51f743|cmp|dword ptr [rbx + 0x18], -1
51f747|jne|0x51f74c
51f749|mov|dword ptr [rbx + 0x18], eax
51f74c|movsxd|rsi, dword ptr [rbx + 0x1c]
51f750|cmp|esi, -1
51f753|je|0x51f77c
51f767|mov|ecx, dword ptr [rdi]
51f76c|shl|rdx, 5
51f770|add|rdx, qword ptr [rbx + 0x10]
51f774|mov|dword ptr [rdx + 8], ecx
51f777|mov|ecx, dword ptr [rdx]
51f779|mov|dword ptr [rdi + 4], ecx
51f77e|inc|word ptr [rbx + 0x22]
51f782|mov|dword ptr [rbx + 0x1c], ecx
51f7aa|cmp|word ptr [rcx + 0x22], 0
51f7b2|jle|0x51f825
51f7bc|test|rcx, rcx
51f7bf|je|0x51f7ca
51f7ca|mov|ecx, dword ptr [rbx + 0x4c]
51f7de|shl|edx, cl
51f7e0|cmp|dword ptr [rax + 0x14], edx
51f7e3|jl|0x51f86d
51f7e9|mov|edi, dword ptr [rbx + 0x18]
51f7ef|je|0x51f825
51f818|cmp|dword ptr [rdx + 0x14], eax
51f81b|jl|0x51f842
51f81d|mov|edi, dword ptr [rdx + 8]
51f823|jne|0x51f7f1
51f825|mov|rcx, rbx
51f828|call|0x51f6b0
51f830|cmp|edi, -1
51f833|jne|0x51f850
51f835|xor|eax, eax
51f841|ret|
51f8d1|movsxd|rbp, dword ptr [rdi + 4]
51f8f3|mov|eax, dword ptr [rdi + 8]
51f8fa|mov|dword ptr [rdx + rcx + 8], eax
51f8fe|movsxd|rbp, dword ptr [rdi + 8]
51f920|mov|eax, dword ptr [rdi + 4]
51f927|mov|dword ptr [rdx + rcx + 4], eax
51f930|cmp|esi, dword ptr [rbx + 0x18]
51f935|mov|eax, dword ptr [rdi + 8]
51f938|mov|dword ptr [rbx + 0x18], eax
51f93b|cmp|esi, dword ptr [rbx + 0x1c]
51f940|mov|eax, dword ptr [rdi + 4]
51f943|mov|dword ptr [rbx + 0x1c], eax
51f949|xor|eax, eax
51f94b|mov|qword ptr [rdi + 0x14], rax
51f94f|mov|qword ptr [rdi], 0xffffffffffffffff
51f956|mov|dword ptr [rdi + 8], 0xffffffff
51f95d|dec|word ptr [rbx + 0x22]'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required operation changed '+hex(pc))
head_tail=[]
for pc,off,role in [(0x51f743,0x18,'r'),(0x51f749,0x18,'w'),(0x51f74c,0x1c,'r'),(0x51f782,0x1c,'w'),(0x51f7e9,0x18,'r'),(0x51f938,0x18,'w'),(0x51f943,0x1c,'w')]:
 mem=ix[pc]['memory'][0]
 if mem['displacement']!=off or mem['size']!=4 or mem['role']!=role:raise RuntimeError('field width/role changed')
 head_tail.append({'pc':hex(pc),'offset':hex(off),'bytes':4,'role':role})
sel={pc:i for pc,i in ix.items() if 0x51f7a0<=pc<0x51f878}
zero=G.graph(sel,0x51f7a0,0x51f878,fixed={0x51f7b2:True,0x51f833:False})
if not G.dominates(zero,0x51f828,0x51f841) or zero['calls']!=[(0x51f828,'0x51f6b0')]:raise RuntimeError('zero-count acquisition path changed')
# Mathematical certificate tied to the original increment/wrap/sentinel sites.
# These are source calculations, not original instruction executions.
cert=[]
for start in range(10):
 seq=[];cur=start
 for step in range(10):
  seq.append(cur);cur+=1
  if cur>=10:cur=0
 if sorted(seq)!=list(range(10)):raise RuntimeError('circular bound incomplete')
 cert.append({'start':start,'visit_order':seq})
states=0
for mask in range(1<<10):
 n=mask.bit_count()
 for row in cert:
  free=next((i for i in row['visit_order'] if not(mask>>i&1)),None)
  if n<10 and free is None or n==10 and free is not None:raise RuntimeError('sentinel occupancy certificate failed')
  states+=1
if states!=10240:raise RuntimeError('incomplete mathematical domain')
# If all n allocated pages are full, used=sum(counts)=32*n. Therefore used<320
# forces n<10, where a free sentinel exists. Otherwise a complete acyclic list
# visits a partial page and original JL returns it. These premises are NOT a
# proven all-writer inductive invariant or a running-game state observation.
broken=G.graph(sel,0x51f7a0,0x51f878,fixed={0x51f7b2:False,0x51f7bf:True,0x51f7e3:False,0x51f7ef:True,0x51f833:False})
acq={pc:i for pc,i in ix.items() if 0x51f6b0<=pc<0x51f79c}
full=G.graph(acq,0x51f6b0,0x51f79c,fixed={0x51f6ce:False})
if broken['returns']!=[0x51f841] or broken['calls']!=[(0x51f828,'0x51f6b0')] or full['returns']!=[0x51f6e2] or full['calls']:raise RuntimeError('countermodel source path changed')
pre=json.loads((P/'consumer-preimage.json').read_text())
if len(pre['rows'])!=2 or 'read on no path read' not in pre['rows'][0] or 'returns at once when it is <= 0' not in pre['rows'][1]:raise RuntimeError('consumer defect absent from exact preimage')
result={'producer_complete':True,'method':'A STATIC_ONLY source proof and conditional finite invariant; no machine execution','driver_sha256':sha(Path(__file__)),
 'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles],'instruction_assertions':len(ops.splitlines()),'graphs':graphs,'head_tail_accesses':head_tail,
 'page_links':'page DWORD0=id, DWORD4=previous, DWORD8=next; descriptor DWORD18=head/DWORD1C=tail; acquisition appends, removal rewires neighbors/endpoints',
 'zero_live_count':'Branch51F7B2 reaches51F828call51F6B0, not immediate return; acquisition can succeed or fail. Negative signed count natural admissibility not proved.',
 'finite_search_certificate':cert,'mathematical_sentinel_states':states,
 'conditional_invariant':'Valid stable10x32 metadata, globalused=sum(pageused), complete acyclic active list, free sentinels for inactive pages, valid cursor, stable nonNULL table and no interference imply: used<320 finds a partial page or acquires a free page. A full current page alone cannot explain helperNULL.',
 'countermodel':{'method':'composed static branch certificate, not execution or natural reachability','pageused':[32]*9+[31],'globalused':319,'banksLive':10,'cursor':0,'head':-1,'dropped_premise':'complete active-list coherence','selector_return_pc':'51F841','helper_return_pc':'51F6E2','result':'NULL despite319<320'},
 'consumer_corrections':{'path':pre['path'],'preimage_file_sha256':pre['file_sha256'],'rows':'018 unread u8[8] contradicted by independent DWORDhead/tail accesses; 022 immediate-return claim contradicted by original acquisition call'},
 'limits':['No original machine/native/live execution; cursor orders and10240 sentinel categories are mathematical source-linked calculations',
 'Complete-list/count/sentinel/occupancy consistency, valid cursor, initialized lifetime, no interference and stable nonNULL table identity are preconditions, not proved universal original invariants',
 'Nonzero relocatable handle3AB7F0/native effects not proved; handle0 or valid stable resolver/table identity required',
 'Removal link updates do not establish physical backing free or scheduling',
 'Allwriters/concurrency/realstartup, authored ownercardinality, samekeyreuse, naturalexhaustion and wholeOV21 remainOPEN',
 'Exact peer-owned consumer preimage preserved; independent acceptance/incorporation pending']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED original head/tail DWORDs, zero-count acquisition and conditional occupancy lemma; no native/game')


