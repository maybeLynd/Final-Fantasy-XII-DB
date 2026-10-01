"""Conditional original-code bridge for two retained pointer-fixup keys.
Requires complete captured source and the already published retained table receipt.
No constructed runtime state, original execution or successful-load assertion.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable result exists')
pins=[]
def load(name):
 p=W/name;z=p.read_bytes();r=json.loads(z);pins.append(dict(path=name,sha256=hashlib.sha256(z).hexdigest()))
 if r.get('exe_sha256')!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' or r.get('wrapper_complete') is not True:raise ValueError('original prerequisite incomplete')
 if [(c['bytes'],c['observed']) for c in r['controls']]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('capture observer controls missing')
 for q in r['ranges']:
  z=bytes.fromhex(''.join(x['bytes'] for x in q['instructions']))
  if len(z)!=int(q['end_exclusive'],16)-int(q['start'],16) or hashlib.sha256(z).hexdigest()!=q['sha256']:raise ValueError('source byte extent/hash changed')
 return {int(x['pc'],16):x for q in r['ranges'] for x in q['instructions']}
def need(ix,pc,m,a):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('required operation changed '+hex(pc))
outer=load('softedges-effectvariant-registration-code-01.json');inner=load('softedges-member-resolution-code-01.json')
kind=load('softedges-array-terminal-guard-source-01/original-code.json');mapped=load('softedges-mapping-builders-code-01.json')
resolve=inner|load('softedges-member-resolution-continuation-code-01.json')
bridge=load('softedges-resource-source-01/member-bridge-code-01.json')
patch=load('softedges-header-membership-code-01.json')
need(outer,0x5e48c6,'mov','dword ptr [rsp + 0x30], 3');need(outer,0x5e4951,'mov','dword ptr [rsp + 0x30], 3')
need(outer,0x5e48d2,'mov','dword ptr [rsp + 0x20], 0x40');need(outer,0x5e495d,'mov','dword ptr [rsp + 0x20], 0x50')
need(inner,0x5eed9a,'mov','dword ptr [rsp + 0x30], 2');need(kind,0x632a21,'mov','ebx, dword ptr [rsp + 0x80]')
need(kind,0x632a4d,'mov','dword ptr [rdi + 0x5c], ebx');need(kind,0x16d680,'mov','rax, rcx')
need(mapped,0x59b8f7,'sub','esi, eax');need(mapped,0x59b8f9,'dec','esi')
need(mapped,0x59b903,'add','rdx, qword ptr [r9 + 0x30]');need(mapped,0x59b93c,'mov','qword ptr [rdi + 0x28], rdx')
need(resolve,0x59eca2,'mov','ebp, dword ptr [rax + 0x5c]');need(resolve,0x59ecca,'je','0x59ece6')
need(resolve,0x59ece6,'xor','al, al');need(resolve,0x59ecf2,'cmp','ebp, 2');need(resolve,0x59ecf5,'jne','0x59ecfb')
need(resolve,0x59ecf9,'je','0x59ecff');need(resolve,0x59ecfb,'xor','al, al');need(resolve,0x59ecff,'mov','al, 1')
need(resolve,0x59ed0d,'jne','0x59ed52');need(resolve,0x59ed52,'xor','eax, eax')
need(bridge,0x59bfed,'je','0x59c0db');need(bridge,0x59c0db,'mov','rax, rbx')
need(bridge,0x59bfaf,'cmp','qword ptr [rcx + 0x30], rax')
need(patch,0x59cd07,'mov','r9d, dword ptr [r12 + 0x14]');need(patch,0x59cd25,'call','qword ptr [rax + 0x40]')
need(patch,0x59cd14,'mov','qword ptr [rdx], r13')
fp=W/'softedges-array-terminal-guard-source-01/facts.json';facts=json.loads(fp.read_text());pins.append(dict(path=str(fp.relative_to(W)),sha256=hashlib.sha256(fp.read_bytes()).hexdigest()))
if any(v['target']!='0x16d680' for v in facts['slots'].values()):raise ValueError('native getter-slot generation mismatch')
cp=ROOT/'Database/FFXII TZA/_experiments/evidence/phyretext-softedges-field-extent';mf=json.loads((cp/'manifest.json').read_text())
name='softedges-resource-source-01/field-extent-result-02.json';field=(cp/name).read_bytes()
if hashlib.sha256(field).hexdigest()!=next(x['sha256'] for x in mf['members'] if x['path']==name):raise ValueError('published retained-table receipt changed')
f=json.loads(field)
if f.get('producer_complete') is not True or f.get('asset_sha256')!='f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf':raise ValueError('retained-table prerequisite missing')
fixups=[e for e in f['fixup_tables']['pointer']['entries_by_list'][2] if e[0] in (0x80000016,0x8000001b)]
if fixups!=[[0x80000016,0,0,12,0,11,-1],[0x8000001b,0,11,12,0,1,-1]]:raise ValueError('two exact source keys/counts changed')
asset=(W/'softedges-resource-source-01/phyretext.fx.phyre').read_bytes()
if hashlib.sha256(asset).hexdigest()!=f['asset_sha256']:raise ValueError('retained file mismatch')
h=struct.unpack_from('<21I',asset);b=asset[h[1]:h[1]+h[2]];nt,nc,nm,pooln=struct.unpack_from('<4I',b,8);ms=32+4*nt+36*nc;pool=b[ms+24*nm:]
def text(a):return pool[a:pool.index(b'\0',a)].decode('ascii')
classes=[];cur=0
for i in range(nc):
 c=struct.unpack_from('<9I',b,32+4*nt+36*i);members=[struct.unpack_from('<6I',b,ms+24*j) for j in range(cur,cur+c[3])];cur+=c[3]
 classes.append((c,{text(m[0]):m for m in members}))
vr,vm=classes[12];ar,am=classes[16]
if nt!=13 or text(vr[2])!='PEffectVariant' or text(ar[2])!='PArray<PShaderParameterDefinition>':raise ValueError('file class identity')
route=[]
for key,native,name in [(22,0x40,'m_tweakableShaderParameterDefinitions'),(27,0x50,'m_untweakableShaderParameterDefinitions')]:
 m=vm[name];els=am['m_els']
 if m[1]!=nt+17 or m[3]!=5 or key-m[2]!=4 or m[4]&0x42 or els[1]!=nt+43 or els[2:4]!=(4,1) or els[4]&0x42:raise ValueError('file range/kind-guard precondition changed')
 if vr[5]!=0 or ar[5]!=0:raise ValueError('parent file offset changed; revise composition')
 route.append(dict(key=key,outer_member=name,outer_kind=3,inner_member='m_els',inner_kind=2,residual=4,
  file_child_class_id=43,native_array_address='object+zext32(0x%x+arrayF4-effectVariantF4)'%native,
  source_list=12,source_object_index=0 if key==22 else 11,count=11 if key==22 else 1))
out.write_text(json.dumps(dict(status='PRODUCER_CHECKED_CONDITIONAL_BRIDGE_INDEPENDENT_PENDING',method='A STATIC_ONLY',
 question='Under unchanged matching native mappings, which terminal member and pointer/count association do these two packed keys request?',
 result='Both keys conditionally resolve outer kind3 array then terminal kind2 m_els; no null child/getter assumption. The source association is first11 definition objects and singleton object11. Existing pointer/count setter proof supplies only normal continuation behavior.',
 source_pins=pins,table_dependency=dict(path=str((cp/name).relative_to(ROOT)),sha256=hashlib.sha256(field).hexdigest(),commit='5bbbe5528076e0d2c82a9b05e0dfc4c3232bfaa1',acceptance='Producer valid, independent review pending'),routes=route,
 guard_correction='Kind2 with bit6 clear stops recursion. With bit6 set and nonnull self getter, optional query result==1 ALLOWS recursion; other results stop. Current canonical prose result==1 fails has reversed polarity. Bit1 always stops. No claim about opaque query effects or natural values.',
 assumptions=['Class/member name/type mapping matches these native registered objects;59BFaf type equality holds','Registrations returned normally and metadata/kinds/getters remain unchanged','The pointer-fixup assignment site is reached with correctly bound list12 native objects','Normal source-association continuation after any unproved owned-storage cleanup'],
 limitations=['Actual successful live/resource initialization is unobserved','F4 values retained symbolically; no universal zero or destination-address assumption','Pointer patcher can write a destination slot at59CD14 before the callback; this is not a complete effects inventory or a claim of unchanged pre-call array storage','Native source pointer/lifetime/aliases and opaque cleanup not proved','Not whole constructor/OV42 closure, gameplay or natural reachability'],
 checker_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),producer_complete=True,live_runs=0,isolated_native_runs=0),indent=2)+'\n')
print('Checked conditional two-key/m_els bridge and exact guard polarity; actual load/lifetime remain OPEN')
