"""Original local carrier proof; all countermodels are mathematical, never gameplay."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('roles','validate-title-source-annotations.py')
if sha(P/'capture-index-path.py')!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':raise RuntimeError('shared capture identity changed')
if sha(P/'validate-title-source-annotations.py')!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':raise RuntimeError('reviewed validator identity changed')
manifest_pins={'action-selector-local-exclusions': '8221834782de76d5d53743a53d436240d9e3fd89adb8460e11f1017bdd82c81a', 'ov42-class20-action-admission': '67e7df297497326a5b98d9d21355923750442981e8121cfb4d4e7840de5e4d92', 'row113-equality': '12e3323d7635333a1368db1d49a51fbf4e2bb69845a86ddd5c65f2e3cd25aa29', 'presentation-index-domain': '499a3e53e678069ec4c7424c2f2efbed3236d504c899fe93555cb85596a756eb'}
lineage=json.loads((P/'lineage.json').read_text());assert len(lineage)==10
for packet,h in manifest_pins.items():
 if sha(P/'retained'/(packet+'-manifest.json'))!=h:raise RuntimeError('parent manifest changed')
for row in lineage:
 members={x['path']:x for x in json.loads((P/'retained'/(row['packet']+'-manifest.json')).read_text())['members']};x=members[row['member']];q=P/row['copy']
 if q.stat().st_size!=x['bytes'] or sha(q)!=x['sha256'] or x['sha256']!=row['sha256']:raise RuntimeError('retained member changed')
def checked(tag,driver):
 x=json.loads((P/(tag+'.status.json')).read_text())
 if x.get('exit')!=0 or x.get('terminal') is not True or x.get('exception') is not None or x.get('driver_sha256')!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('required capture status failed '+tag)
checked('capture-01','capture.py');checked('capture-02','capture-completion.py')
for tag,driver in [('source-01.json','capture.py'),('source-02.json','capture-completion.py')]:
 x=json.loads((P/tag).read_text())
 if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/driver):raise RuntimeError('capture invocation incomplete')
sources=['source-01.json','source-02.json','retained/action-selector-local-exclusions-special-selection-dispatch-raw-02.json','retained/ov42-class20-action-admission-special-admission-callers-raw-01.json','retained/row113-equality-source-01.json','retained/presentation-index-domain-source-01.json']
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('wrong original image')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked original bytes')
ix={};annotations=[]
for f in sources:
 x=json.loads((P/f).read_text());annotations.append(V.validate(x))
 if x.get('exe_sha256')!=PIN:raise RuntimeError('wrong source identity')
 for r in x['ranges']:
  lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise RuntimeError('original byte mismatch')
  for i in r['instructions']:
   pc=int(i['pc'],16)
   if pc in ix and ix[pc]!=i:raise RuntimeError('retained source disagreement')
   ix[pc]=i
# Complete caller code boundary: catalog2088 contains2034code +52switchdata +2padding.
# Explicit data extents are derived from actual CMP guards, not guessed function length.
required=[(0x30487f,'lea','rsi, [rcx + 0x6b0]'),(0x30488d,'movzx','r13d, word ptr [rsi + 0x64]'),(0x304895,'mov','qword ptr [rbp - 0x59], r14'),(0x30491f,'mov','r15, rax'),(0x304929,'movzx','ecx, word ptr [rax + 8]'),(0x30492d,'movzx','eax, r13w'),(0x304931,'imul','ecx, eax'),(0x304934,'add','r15d, ecx'),(0x304939,'mov','r15, r14'),(0x304940,'cmp','eax, 0xc'),(0x304943,'ja','0x305006'),(0x304950,'mov','ecx, dword ptr [rdx + rax*4 + 0x1e5044]'),(0x30495a,'jmp','rcx'),(0x304f3d,'test','dword ptr [r15 + 0xc], 0x40000000'),(0x304f47,'mov','rdx, r15'),(0x304f4a,'mov','rcx, rdi'),(0x304f4d,'call','0x306760'),(0x305041,'ret',''),
(0x30cc7a,'movzx','ecx, word ptr [rbx + 0x1c]'),(0x30cc7e,'imul','esi, ecx'),(0x30cc81,'add','esi, eax'),(0x30cd93,'mov','rdx, rsi'),(0x30cd99,'call','0x30ce10'),(0x30cf07,'mov','rdx, rbp'),(0x30cf0d,'call','0x306bd0'),(0x306be0,'mov','rsi, rdx'),(0x306bfc,'cmp','rdi, qword ptr [rip + 0x1fbb565]'),(0x306c71,'sub','esi, eax'),(0x306c7c,'movzx','ecx, word ptr [rax + 8]'),(0x306c82,'div','ecx'),(0x306c84,'add','eax, 0xffffff6c'),(0x306c89,'cmp','eax, 0x7f'),(0x306c95,'movzx','eax, byte ptr [rdx + rax + 0x1e6d08]'),(0x306ca9,'mov','ebx, 1'),(0x306cdb,'mov','dword ptr [rip + 0x1fbb47b], ebx'),
(0x306775,'mov','rdi, rdx'),(0x3067aa,'mov','eax, dword ptr [rip + 0x1fbb9ac]'),(0x3067b0,'dec','eax'),(0x3067b7,'cmp','eax, 5'),(0x3067ba,'ja','0x306a9a'),(0x3067ce,'mov','eax, dword ptr [r14 + rax*4 + 0x1e6af0]'),(0x3067d9,'jmp','rax'),(0x306974,'movzx','ecx, byte ptr [rdi + 0x26]'),(0x30697f,'mov','byte ptr [rax + 0x5ad4], cl')]
for pc,m,a in required:
 if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('operation changed '+hex(pc))
caller_table=read(0x305044,13*4);caller_targets=[0x120000+x for x in struct.unpack('<13I',caller_table)]
kind_table=read(0x306d08,128);kind_jumps=read(0x306cec,7*4);kind_targets=[0x120000+x for x in struct.unpack('<7I',kind_jumps)]
if kind_targets!=[0x306cbe,0x306cc5,0x306cd1,0x306cb7,0x306ca9,0x306cb0,0x306ccc]:raise RuntimeError('kind switch source changed')
kind1_ids=[148+k for k,x in enumerate(kind_table) if kind_targets[x]==0x306ca9]
if kind1_ids!=list(range(262,275)):raise RuntimeError('known kind1 source domain changed')
dispatch=read(0x306af0,24);assert struct.unpack('<I',dispatch[:4])[0]+0x120000==0x306931
# Complete caller local CFG, with explicit bounded indirect-switch destinations.
lo,hi=0x304850,0x305042;local={pc:i for pc,i in ix.items() if lo<=pc<hi};todo=[lo];seen=set();edges={}
while todo:
 pc=todo.pop()
 if pc in seen:continue
 if pc not in local:raise RuntimeError('unclosed caller CFG '+hex(pc))
 seen.add(pc);i=local[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
 if m=='ret':succ=[]
 elif pc==0x30495a:succ=caller_targets
 elif m=='jmp':succ=[int(i['args'],16)]
 elif m.startswith('j'):succ=[n,int(i['args'],16)]
 elif m=='int3':raise RuntimeError('unexpected caller trap')
 else:succ=[n]
 edges[pc]=succ;todo+=succ
assert set(local)==seen,'unreachable source code must be accounted'
anc={0x304f4d}
while True:
 new=anc|{p for p,ds in edges.items() if any(d in anc for d in ds)}
 if new==anc:break
 anc=new
r15defs=[pc for pc,i in local.items() if i['mnemonic'] in ['mov','add'] and i['args'].split(',')[0] in ['r15','r15d']]
if set(r15defs)&anc!={0x30491f,0x304934,0x304939}:raise RuntimeError('R15 caller definitions changed')
owner_kind_refs=[i['pc'] for i in local.values() for r in i['memory'] if r['rip_target'] in ['0x22c215c','0x22c2168']]
if owner_kind_refs:raise RuntimeError('local owner/kind reference counterexample')
# A source-level countermodel, not executed FF12 instructions or natural reachability.
table=P/'retained/action-selector-local-exclusions-special-action-frozen-ready--action-selectors-01--tables--action_data_us.st2e';tb=table.read_bytes();count,stride,off=struct.unpack_from('<III',tb,4);assert(count,stride)==(543,60)
rows=[]
for row in [262,275]:rows.append({'row':row,'flags':hex(struct.unpack_from('<I',tb,off+stride*row+12)[0]),'selector':tb[off+stride*row+38]})
assert [r['selector'] for r in rows]==[27,0] and all(int(r['flags'],16)&(1<<30) for r in rows)
base=0x100000;counter={'kind_source_row':262,'current_action_row':275,'stable_base':base,'stride':60,'kind_source_pointer':base+262*60,'current_action_pointer':base+275*60,'classified_kind':1,'writer_selector':0,'current_flags_bit30':True,'interpretation':'Different valid source rows satisfy local value/bit30 guards; omitted action scheduling/ownership invariant may exclude this state in natural gameplay','executed':False}
result={'producer_complete':True,'method':'A STATIC_ONLY original complete caller and bounded carrier proof','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':f,'sha256':sha(P/f)} for f in sources],'annotation_prerequisites':annotations,'parent_manifest_pins':manifest_pins,'instruction_assertions':len(required),'caller_cfg':{'entry':hex(lo),'code_end':hex(hi),'visited':len(seen),'returns':[hex(pc) for pc in seen if local[pc]['mnemonic']=='ret'],'indirect_targets':[hex(x) for x in caller_targets],'callsite':hex(0x304f4d),'R15_definitions_reaching_call':[hex(x) for x in sorted(set(r15defs)&anc)],'explicit_owner_kind_refs':owner_kind_refs},'original_data':[{'address':hex(a),'bytes':z.hex(),'sha256':hashlib.sha256(z).hexdigest()} for a,z in [(0x305044,caller_table),(0x306d08,kind_table),(0x306cec,kind_jumps),(0x306af0,dispatch)]],'existing_kind1_ids_corrob':kind1_ids,'row_values_used':rows,'countermodel':counter,'answer':'Queued+1C classifier and currentunit+714 updater are separate row carriers. Local current-action code has no explicit kind/owner row binding; owner-only initializer does not store original row identity. Thus kind1 alone does not establish selector27..39 for an arbitrary later incoming action row. Stable same-row/ownership/scheduling is an upstream proof obligation; sourcecountermodel is not naturally reached behavior.','limitations':['No native/game/forced-call execution','Normal external calls, x64ABI, validframe and stable initialized registry/row data assumed','Original tables/resource identities are not captured live pointers or lifetime guarantees','Current code no explicit RIP owner/kind read does not prove transitive callees cannot enforce invariants','No allwriters/globalunreachability/actualbattle-statstype or wholeOV42 closure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED separate original carriers, complete local caller and qualified countermodel; no native/live')
