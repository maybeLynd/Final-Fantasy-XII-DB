"""Composed normal NULL-return contract, exact original code; no game execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable output exists')
if (P/'inspect.py').exists():raise RuntimeError('stdlib shadow refused')
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
sources=[]
for n,d in [('01','capture.py'),('02','capture-cookie.py')]:
 s=json.loads((P/f'capture-{n}.status.json').read_text());x=json.loads((P/f'source-{n}.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/d) or not(P/f'capture-{n}.stdout').read_bytes() or(P/f'capture-{n}.stderr').read_bytes():raise RuntimeError('required capture failed '+n)
 if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/d) or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('exe_sha256')!=PIN:raise RuntimeError('actual capture incomplete')
 sources.append(x)
s=json.loads((P/'source-qualification-01.status.json').read_text());f=json.loads((P/'source-feasibility-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'qualify-source.py') or f['driver_sha256']!=sha(P/'qualify-source.py') or f.get('stage')!='SOURCE_CFG_QUALIFIED_NOT_SEMANTIC_CLOSURE' or f.get('producer_complete') is not False:raise RuntimeError('required source feasibility failed or mislabelled')
ids=json.loads((P/'retained-identities.json').read_text())
if len(ids.get('files',[]))!=10:raise RuntimeError('missing retained inputs')
for r in ids['files']:
 if sha(P/'retained'/r['snapshot'])!=r['sha256']:raise RuntimeError('retained preimage changed')
t=json.loads((P/'retained/prove-03.status.json').read_text());v=json.loads((P/'retained/result-02.json').read_text())
if t.get('terminal') is not True or t.get('exit')!=0 or t.get('exception') is not None or t['driver_sha256']!=sha(P/'retained/prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'retained/prove.py'):raise RuntimeError('retained producer incomplete')
for n,d in [('capture-01.status.json','capture.py'),('filecache-key-boundaries-capture-02.status.json','capture-filecache-key-boundaries.py')]:
 t=json.loads((P/'retained'/n).read_text())
 if t.get('terminal') is not True or t.get('exit')!=0 or t.get('exception') is not None or t['driver_sha256']!=sha(P/'retained'/d):raise RuntimeError('retained capture incomplete')
sources.extend(json.loads((P/'retained'/n).read_text()) for n in ['source-01.json','filecache-key-boundaries-source-02.json'])
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');annotations=[V.validate(x) for x in sources]
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked original range')
ranges=[r for x in sources for r in x['ranges'] if r['start'] in ['0x20c300','0x210ec0','0x85e730','0x808c40','0x20c1b0','0x59ee90','0x1d6d20']]
if len(ranges)!=7:raise RuntimeError('zero/ambiguous required bodies')
ix={};gb={};views={};graphs=[]
for r in ranges:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local);view={p:dict(i,mnemonic=i['mnemonic'].removeprefix('bnd ')) for p,i in local.items()} if a==0x808c40 else local
 g=G.graph(view,a,b,tail='0x85e730' if a==0x210ec0 else 'qword ptr [rip + 0x64409]' if a==0x85e730 else '0x809654' if a==0x808c40 else None)
 if g['visited']!=set(local):raise RuntimeError('unclosed/unaccounted local CFG')
 gb[a]=g;views[a]=view;graphs.append({'entry':hex(a),'bytes':b-a,'calls':g['calls'],'returns':[hex(q) for q in g['returns']],'tails':[hex(q) for q in g['tails']]})
def need(pc,m,a):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required failure operation changed '+hex(pc))
for line in '''20c328|inc|dword ptr [rcx + 0x88]
20c354|inc|byte ptr [rdx + 0x10]
20c38b|inc|byte ptr [rcx + 0x10]
20c3f8|inc|byte ptr [rcx + 0x10]
20c3fb|mov|ecx, 0x10
20c400|call|0x210ec0
20c40a|test|rax, rax
20c40d|je|0x20c423
20c41b|call|0x217a60
20c423|xor|eax, eax
210ec6|jmp|0x85e730
85e730|jmp|qword ptr [rip + 0x64409]
20c2a8|call|0x20c300
20c2ad|mov|rbx, rax
20c2b3|call|0x5cd820
20c2b9|mov|rax, rbx
20c2bc|jmp|0x20c2cb
20c2d6|call|0x808c40
1d6d55|call|0x20c1b0
59efe5|call|0x1d6d20
59efea|mov|qword ptr [r15 + 0x20], rax
59efee|test|rax, rax
59eff1|js|0x59f000
59eff9|xor|eax, eax
59effb|jmp|0x59f1d6
59f1dd|call|0x808c40
808c56|bnd ret|'''.splitlines():
 pc,m,a=line.split('|');need(int(pc,16),m,a)
decl=sources[0]['import_declaration']
if decl['name']!='malloc' or decl['iat_va']!='0x8c2b40' or bytes.fromhex(decl['iat_file_bytes'])!=read(0x8c2b40,8) or read(int(decl['hint_name_va'],16)+2,7)!=b'malloc\0':raise RuntimeError('shipping malloc declaration mismatch')
# Exact event count on the supplied normal local CFG, not native executions.
g=gb[0x20c300];todo=[(g['entry'],0)];seen=set();alloc=[];incs={0x20c354,0x20c38b,0x20c3f8}
while todo:
 pc,n=todo.pop()
 if (pc,n) in seen:continue
 seen.add((pc,n));n+=pc in incs
 if n>1:raise RuntimeError('multiple direct descriptor increments')
 if pc==0x20c400:
  alloc.append(n)
  if n!=1:raise RuntimeError('allocation without one descriptor increment')
 todo.extend((q,n) for q in g['edges'][pc])
if not alloc or not G.dominates(g,0x20c328,0x20c400):raise RuntimeError('manager increment not before allocation')
post=G.graph({q:ix[q] for q in g['visited']},0x20c40a,0x20c438,fixed={0x20c40d:True})
if post['calls'] or 0x20c41b in post['visited'] or 0x20c423 not in post['visited']:raise RuntimeError('NULL path invokes constructor/callback')
for pc in post['visited']:
 for m in ix[pc]['memory']:
  if m['role'] in ['w','rw'] and m['base']!='rsp':raise RuntimeError('post-NULL object write/rollback')
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def writes(pc,regs):
 d=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,w=d.regs_access();return bool({d.reg_name(q) for q in w}&set(regs))
rax={'rax','eax','ax','al','ah'}
if any(writes(q,rax) for q in gb[0x808c40]['visited']) or gb[0x808c40]['calls'] or gb[0x808c40]['returns']!=[0x808c56]:raise RuntimeError('successful cookie return modifies RAX')
if any(writes(q,rax) for q in post['visited'] if q>0x20c423):raise RuntimeError('NULL return value changed')
if any(writes(q,{'rbx','ebx','bx','bl','bh'}) for q in ix if 0x20c2b0<=q<0x20c2b9):raise RuntimeError('saved lookup return carrier changed')
if any(writes(q,rax) for q in ix if 0x20c2bc<=q<=0x20c2f1):raise RuntimeError('lookup epilogue return changed')
if any(writes(q,rax) for q in ix if 0x1d6d5a<=q<=0x1d6d6e):raise RuntimeError('lookup wrapper return changed')
rp=G.graph(views[0x59ee90],0x59efea,0x59f1fc,fixed={0x59eff1:False})
if rp['calls']!=[(0x59f1dd,'0x808c40')] or 0x59f000 in rp['visited'] or 0x59f1b7 in rp['visited'] or 0x59eff9 not in rp['visited']:raise RuntimeError('zero cache return selects archive/fill')
if any(writes(q,rax) for q in rp['visited'] if q>0x59eff9):raise RuntimeError('resolver zero status changed')
result={'producer_complete':True,'method':'A STATIC_ONLY original composed normal-NULL return rules','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'source_pins':[{'path':n,'sha256':sha(P/n)} for n in ['source-01.json','source-02.json','retained/source-01.json','retained/filecache-key-boundaries-source-02.json']],'annotations':annotations,'graphs':graphs,'malloc_declaration':decl,
 'allocation_prephase':{'abstract_states':len(seen),'descriptor_increments_per_allocation':alloc,'manager_increment_before_allocation':True,'limits':'Own original-CFG event counts, not runs/actual live values'},
 'established':['20C300 increments manager DWORD88 before its16B handle allocation, and every local allocation path has exactly one direct selected-record BYTE10 increment.','If that allocation returnsNULL normally, the function skips217A60 construction, returns0 and has no own subsequent object-write rollback or other call. Earlier selected kind/word changes can remain too; opaque/native interference excluded by premise.','210EC0 forwards through85E730 to the static PE malloc import at8C2B40. Named declaration is not live binding or observed heap failure.','On the demonstrated found-record lookup path,20C1B0 saves a zero20C300 result inRBX, unlocks then returns it. Successful in-body808C40 cookieRET preservesRAX by original instructions; generic Win64 ABI alone would not prove this.1D6D20 epilogue also preservesRAX.','Resolver59EE90 stores zero in record20 and tests only the sign ofRAX for the miss branch. Zero follows the cache path, copies the size out-field and returns status0; it does not enter the archive fallback or cache-fill call on this path.'],
 'interpretation':'Allocation-NULL zero and lookup-miss -1 are distinct at these supplied interfaces. A status0 or the preceding local counters alone cannot certify a successfully constructed cache-view handle. This is a conditional failure contract, not an observed leak or natural exhaustion claim.',
 'limits':['No shipping instructions/native harness/game execution. Actual malloc target/DLL, occurrence ofNULL or exhaustion unobserved.','Valid existing map/record/private frames and distinct fields; selected helpers return valid records normally and do not alter the counted fields outside stated effects. Normal Win64 nonvolatile ABI and successful in-bodycookieRET; native exception/failure tail effects unproved.','All own local increments only; no universal successful-handle cardinality, allcounterwriter closure, natural bytewrap, heap leak, lifetime/reuse/scheduling or later reader consequence proof.','Retained99 producer source revalidated against originalEXE but remains pending independent acceptance; its verdict/consumption not assumed. Parent wrapper bytes reused, no selector/filter/prefix/archive census.','Normal allocator-NULL path only; exceptional native unwinding and imported allocator hooks are distinct.'],
 'affected_claims':['FABLE cache lookup/fallback success and failure semantics, OV33 prerequisite only','OPUS cache handle acquire/accounting/return-value contract'],'cleanup':'Only bounded own offline children. No PC/game/nativeinstrument/save/config/reference/peer writes.'}
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS conditional allocation-zero accounting and cache-versus-miss propagation; no FF12 execution')
