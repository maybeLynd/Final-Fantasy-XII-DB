"""Conditional original caller/out-key dataflow; no FF12 instructions executed."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable result exists')
if (P/'inspect.py').exists():raise RuntimeError('stdlib inspect shadow refused')
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or (P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('exe_sha256')!=PIN:raise RuntimeError('actual capture incomplete')
ids=json.loads((P/'retained-identities.json').read_text())
if len(ids.get('files',[]))!=14:raise RuntimeError('missing retained identity population')
for row in ids['files']:
 if sha(P/'retained'/row['snapshot'])!=row['sha256']:raise RuntimeError('retained snapshot changed')
M=json.loads((P/'retained/manifest.json').read_text());mm={m['path']:m for m in M['members']}
for row in ids['files'][:10]:
 if row['snapshot']!='manifest.json' and mm.get(row['snapshot'],{}).get('sha256')!=row['sha256']:raise RuntimeError('retained published member changed')
t=json.loads((P/'retained/filecache-key-preprocessing-positive-02.status.json').read_text())
v=json.loads((P/'retained/filecache-key-preprocessing-result-02.json').read_text())
if t.get('terminal') is not True or t.get('exit')!=0 or t.get('exception') is not None or t['driver_sha256']!=sha(P/'retained/prove-filecache-key-preprocessing.py') or v.get('producer_complete') is not True:raise RuntimeError('required retained producer failed')
retained=[]
for name,tag,driver in [('filecache-key-boundaries-source-02.json','filecache-key-boundaries-capture-02.status.json','capture-filecache-key-boundaries.py'),('filecache-hash-loop-source-01.json','filecache-hash-loop-capture-01.status.json','capture-filecache-hash-loop.py')]:
 t=json.loads((P/'retained'/tag).read_text())
 if name=='filecache-hash-loop-source-01.json':
  if t!={'exit':0,'driver':'capture-filecache-hash-loop.py'}:raise RuntimeError('legacy hash receipt changed or failed')
  # The legacy record does NOT establish a completed, driver-bound invocation.
  # The needed shipping hash bytes are independently qualified below against EXE.
 else:
  if t.get('terminal') is not True or t.get('exit')!=0 or t.get('exception') is not None or t['driver_sha256']!=sha(P/'retained'/driver):raise RuntimeError('required retained capture failed')
 retained.append(json.loads((P/'retained'/name).read_text()))
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked original range')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')
annotations=[V.validate(z) for z in [x,*retained]]
required=[('0x59ee90','0x59f1fc'),('0x59a9b0','0x59aad5'),('0x20c1b0','0x20c2f2')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('source population changed')
ranges=x['ranges']+[r for z in retained for r in z['ranges'] if r['start'] in ['0x1d6d20','0x674a00']]
if len(ranges)!=5:raise RuntimeError('missing retained wrapper/hash body')
ix={};gb={};graphs=[]
for r in ranges:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local);g=G.graph(local,a,b)
 if g['visited']!=set(local):raise RuntimeError('unaccounted local CFG')
 gb[a]=g;graphs.append({'entry':hex(a),'bytes':b-a,'instructions':len(local),'calls':g['calls'],'returns':[hex(q) for q in g['returns']]})
def need(pc,m,a):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('key provenance operation changed '+hex(pc))
for line in '''59eed6|xor|r12b, r12b
59eec4|mov|r15, rcx
59efc4|mov|r12b, 1
59efce|setne|r12b
59efd7|lea|r9, [r15 + 0x28]
59efe5|call|0x1d6d20
59eff1|js|0x59f000
59f1ab|test|r12b, r12b
59f1ae|je|0x59f1bc
59f1b0|mov|edx, dword ptr [r15 + 0x28]
59f1b4|mov|rcx, r15
59f1b7|call|0x59a9b0
59a9c3|mov|esi, edx
59a9c5|mov|edi, dword ptr [rcx]
59a9cd|mov|ecx, edi
59a9cf|call|0x1d6bb0
59a9d4|mov|qword ptr [rsp + 0x50], rax
59aa93|movsx|r9d, byte ptr [rbx + 0x18]
59aa98|lea|rdx, [rsp + 0x50]
59aa9d|mov|r8d, edi
59aaa2|mov|ecx, esi
59aaa4|call|0x1d6a20
1d6d34|mov|rbx, r9
1d6d47|mov|qword ptr [rsp + 0x20], rbx
1d6d55|call|0x20c1b0
20c1ee|mov|r14, qword ptr [rsp + 0x1a0]
20c218|cmp|byte ptr [rsp + 0x40], 0
20c21d|je|0x20c2c7
20c228|call|0x674a00
20c22d|mov|dword ptr [r14], eax
20c2c7|or|rax, 0xffffffffffffffff
674a23|btr|eax, 0x1f
674a27|ret|'''.splitlines():
 pc,m,a=line.split('|');need(int(pc,16),m,a)
if 5*8+0x150+0x28!=0x1a0:raise RuntimeError('fifth out-key argument frame failed')
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def writes(pc,regs):
 i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,w=i.regs_access();return bool({i.reg_name(q) for q in w}&set(regs))
def ancestors(g,target):
 todo=[target];seen=set()
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  seen.add(pc);todo.extend(a for a,bs in g['edges'].items() if pc in bs)
 return seen
cg=gb[0x59a9b0];cone=ancestors(cg,0x59aaa4)
if [q for q in sorted(cone) if writes(q,['rsi','esi','si','sil'])]!=[0x59a9c3]:raise RuntimeError('incoming key carrier changed')
if [q for q in sorted(cone) if writes(q,['rdi','edi','di','dil'])]!=[0x59a9c5]:raise RuntimeError('size carrier changed')
if [q for q in sorted(cone) if writes(q,['rsp','esp','sp','spl']) and ix[q]['mnemonic']!='call']!=[0x59a9ba,0x59a9bb]:raise RuntimeError('commit private frame changed')
pair_writes=[]
for pc in sorted(cone):
 if pc<=0x59a9d4:continue
 for m in ix[pc]['memory']:
  if m['role'] in ['w','rw'] and m['base']=='rsp':
   if m['index'] not in ['',None]:raise RuntimeError('unknown private-frame alias')
   pair_writes.append({'pc':hex(pc),'start':m['displacement'],'end':m['displacement']+m['size']})
   if m['displacement']<0x58 and 0x50<m['displacement']+m['size']:raise RuntimeError('saved base pointer overwritten')
for entry,a,b in [(0x59ee90,0x59efd7,0x59efe5),(0x59ee90,0x59f1b0,0x59f1b7),(0x59a9b0,0x59a9c3,0x59aaa4),(0x59a9b0,0x59a9d4,0x59aaa4),(0x59a9b0,0x59aaa2,0x59aaa4),(0x1d6d20,0x1d6d34,0x1d6d55),(0x1d6d20,0x1d6d47,0x1d6d55),(0x20c1b0,0x20c228,0x20c22d),(0x674a00,0x674a23,0x674a27)]:
 if not G.dominates(gb[entry],a,b):raise RuntimeError('required carrier dominance failed')
for lo,hi,regs in [(0x59f1b0+4,0x59f1b7,['rdx','edx','dx','dl','dh']),(0x59aa98+5,0x59aaa4,['rdx','edx','dx','dl','dh']),(0x59aa93+5,0x59aaa4,['r9','r9d','r9w','r9b']),(0x20c1ee+8,0x20c22d,['r14','r14d','r14w','r14b']),(0x20c228+5,0x20c22d,['rax','eax','ax','al','ah']),(0x674a23+4,0x674a27,['rax','eax','ax','al','ah'])]:
 if any(writes(q,regs) for q in ix if lo<=q<hi):raise RuntimeError('call argument/result carrier changed')
rg=gb[0x59ee90]
if [q for q in sorted(rg['visited']) if writes(q,['r12','r12d','r12w','r12b'])]!=[0x59eed6,0x59efc4,0x59efce,0x59f1f8]:raise RuntimeError('unmodelled arm flag writer')
if [q for q in sorted(ancestors(rg,0x59f1b7)) if writes(q,['r15','r15d','r15w','r15b'])]!=[0x59eec4]:raise RuntimeError('source record carrier changed')
# Finite original-CFG abstract interpretation of the one nonvolatile arm byte.
# Every other branch is nondeterministic; opaque calls obey normal Win64 ABI.
todo=[(rg['entry'],None,False)];seen=set();commits=[]
while todo:
 pc,flag,looked=todo.pop();state=(pc,flag,looked)
 if state in seen:continue
 seen.add(state)
 if pc==0x59eed6:flags=[0]
 elif pc==0x59efc4:flags=[1]
 elif pc==0x59efce:flags=[0,1]
 elif pc==0x59f1f8:flags=[None]
 else:flags=[flag]
 if pc==0x59efe5:looked=True
 if pc==0x59f1b7:
  commits.append({'flag':flag,'lookup_seen':looked})
  if flag!=1 or not looked:raise RuntimeError('armed commit without prior lookup')
 for f in flags:
  edges=rg['edges'][pc]
  if pc==0x59f1ae:
   if f not in [0,1]:raise RuntimeError('unknown arm flag at commit branch')
   edges=[0x59f1bc] if f==0 else [0x59f1b0]
  todo.extend((n,f,looked) for n in edges)
if not commits or len(seen)>6*len(rg['visited']):raise RuntimeError('zero/unbounded flag proof')
empty=G.graph({q:ix[q] for q in gb[0x20c1b0]['visited']},0x20c1b0,0x20c2f2,fixed={0x20c21d:True})
outwrites=[hex(q) for q in empty['visited'] for m in ix[q]['memory'] if m['role'] in ['w','rw'] and m['base']=='r14']
if outwrites or 0x20c228 in empty['visited'] or 0x20c22d in empty['visited'] or 0x20c2c7 not in empty['visited']:raise RuntimeError('empty lookup out-key path changed')
nonempty=G.graph({q:ix[q] for q in gb[0x20c1b0]['visited']},0x20c1b0,0x20c2f2,fixed={0x20c21d:False})
if not all(G.dominates(nonempty,0x20c22d,q) for q in nonempty['returns']):raise RuntimeError('nonempty return without out-key store')
own28writes=[hex(q) for q in rg['visited'] for m in ix[q]['memory'] if m['role'] in ['w','rw'] and m['base']=='r15' and m['displacement']<0x2c and 0x28<m['displacement']+m['size']]
if own28writes:raise RuntimeError('resolver direct out-key writes changed')
result={'producer_complete':True,'method':'A STATIC_ONLY original-byte CFG/carrier/finite flag proof','exe_sha256':PIN,'driver_sha256':sha(Path(__file__)),'sources':[{'source_file':'source-01.json','sha256':sha(P/'source-01.json')},*({'source_file':'retained/'+name,'sha256':sha(P/'retained'/name)} for name in ['filecache-key-boundaries-source-02.json','filecache-hash-loop-source-01.json'])],'annotations':annotations,'graphs':graphs,
 'established':['The supplied resolver reads key DWORD record+28 into EDX at59F1B0.59A9B0 preserves that incoming full32 value in ESI and supplies ECX=ESI to1D6A20; no local archive-path rehash at this boundary.','A bounded finite original-CFG proof of r12b shows every locally armed59F1B7 commit passed59EFE5 cache lookup, under normal nonvolatile-register ABI. Other predicates are nondeterministic; this is not natural-state execution.','1D6D20 maps R9 out-key address into the fifth20C1B0 argument; its5push/SUB150 frame reads that address atcurrentSP1A0 intoR14.','Nonempty normalized lookup calls674A00 then stores fullDWORD returned key at20C22D before every local normal return, including miss. All hash exits passBTR EAX31, so this fresh output lies0..7FFFFFFF.','Empty normalized lookup branches straight to return-1 without hash or direct out-key store. The resolver itself has no direct record+28 write. Under valid nonaliasing state and no opaque callee interference, subsequent armed archive-hit commit forwards the prior field, rather than a newly initialized hash. This conditional boundary does not establish that such an archive hit or high-bit key occurs naturally.'],
 'retained_hash_invocation':'LEGACY_INCOMPLETE_INVOCATION_RECEIPT; no terminal/driver-bound capture credit. Needed hash bytes independently verified against pinned shipping EXE and reviewed decoder in this producer.',
 'arm_flag_proof':{'states':len(seen),'commit_states':commits,'bound':6*len(rg['visited']),'limits':'One byte plus lookup visitation only; no concrete path length, native execution, archive feasibility or all-caller proof'},
 'empty_lookup':{'returns':[hex(q) for q in empty['returns']],'direct_out_key_writes':outwrites,'hash_called':False,'return_value':'FFFFFFFFFFFFFFFF'},'direct_record28_writes':own28writes,'private_pointer_nonoverlap_writes':pair_writes,
 'interpretation':'Keep pre-keyed insertion interface distinct from a qualified caller. Fresh31bit key follows nonempty lookup, not a universal insert-domain claim. Empty normalization has a retained-out-field precondition. FABLE/OPUS must preserve stable-state/nonalias/callback limits and natural reachability as separate obligations.',
 'limits':['Static original bytes only. No shipping instruction, harness, real process or game input executed.','Valid record and distinct out-fields, private frame, readable terminated input/output buffers and successful normalization premises where used; no memory stability inferred from pointer carriers.','Normal Win64 ABI/returns and opaque callees do not interfere with record28 before its key read; allocator/native callback/lifetime/actual bindings and concurrent scheduling unproved.','Supplied local caller path only, no all-indirect/external caller closure; empty normalization plus successful archive hit or a natural high-bit key is unproved.','Retained accepted wrapper/hash evidence reused; no repeat prefix samples or selector/filter/archive census. Producer controls, independent verdict and canonical consumption are separate.'],
 'affected_claims':['FABLE path page §5/§8 RAM cache backfill key provenance; OV33E2 insertion-domain prerequisite, not whole row closure','OPUS source-record+28 output/pre-keyed1D6A20 ABI and empty-normalizer contract'],
 'cleanup':'No game/PC/native instruments, saves/configuration/reference/peer writes; bounded offline child only.'}
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS qualified caller key/out-field and finite arm-byte proof; no FF12 execution')
