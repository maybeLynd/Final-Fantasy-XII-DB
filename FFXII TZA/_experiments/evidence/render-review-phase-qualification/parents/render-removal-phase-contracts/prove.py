"""Original branch-dependent render removal/cleanup contracts, STATIC_ONLY."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if (P/'inspect.py').exists():raise RuntimeError('local inspect.py would shadow required standard library')
def load(n,f):
    s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
    if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not (P/'capture-01.stdout').read_bytes() or (P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x.get('driver_sha256')!=sha(P/'capture-index-path.py'):raise RuntimeError('actual capture incomplete')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');roles=V.validate(x)
lineage=json.loads((P/'lineage.json').read_text());r=P/'retained-clear';mpin='c3e8141dc7fafc01b3fc7651abc3f5be49cf623f66e12c72b8a6615ef08439fc'
if lineage['manifest_sha256']!=mpin or sha(r/'manifest.json')!=mpin:raise RuntimeError('retained clear manifest changed')
members=json.loads((r/'manifest.json').read_text())['members']
for row in lineage['files']:
    q=r/row['path']
    if sha(q)!=row['sha256'] or q.stat().st_size!=row['bytes']:raise RuntimeError('retained clear input changed')
    if row['path']!='manifest.json' and not any(m['path']==row['path'] and m['sha256']==row['sha256'] for m in members):raise RuntimeError('unbound retained clear input')
ps=json.loads((r/'prove-01.status.json').read_text());pv=json.loads((r/'result-01.json').read_text())
if ps.get('terminal') is not True or ps.get('exit')!=0 or ps.get('exception') is not None or ps['driver_sha256']!=sha(r/'prove.py') or pv.get('producer_complete') is not True or pv['driver_sha256']!=sha(r/'prove.py') or not(r/'prove-01.stdout').read_bytes() or(r/'prove-01.stderr').read_bytes():raise RuntimeError('required retained clear producer failed')
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN or pv['exe_sha256']!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
    for vs,rva,size,offset in secs:
        if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
    raise RuntimeError('unbacked original range')
required=[('0x429140','0x4292a6'),('0x427c90','0x427dd8'),('0x4200a0','0x4201eb')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('source population changed')
ix={};gb={};graphs=[]
for row in x['ranges']:
    a,b=int(row['start'],16),int(row['end_exclusive'],16)
    if bytes.fromhex(''.join(i['bytes'] for i in row['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
    local={int(i['pc'],16):i for i in row['instructions']};ix.update(local)
    g=G.graph(local,a,b,tail='0x41f730' if a==0x4200a0 else None)
    if g['visited']!=set(local):raise RuntimeError('unaccounted original CFG')
    gb[a]=g;graphs.append({'entry':hex(a),'bytes':b-a,'instructions':len(local),'calls':g['calls'],'tails':[hex(v) for v in g['tails']]})
def need(pc,m,args):
    if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required removal operation changed '+hex(pc))
ops='''429146|mov|rdx, qword ptr [rip + 0x1e9dddb]
42914d|mov|rbx, rcx
429150|test|rcx, rcx
429153|jne|0x42915d
429155|xor|eax, eax
42915c|ret|
42915d|test|byte ptr [rcx + 0x284], 4
429169|je|0x429204
42916f|or|dword ptr [rcx + 0x290], 2
429178|or|byte ptr [rcx + 0x2ae], 1
42917f|mov|qword ptr [rcx + 0x108], rax
429186|mov|dword ptr [rcx + 0x110], eax
42918c|mov|eax, dword ptr [rcx + 0x284]
429192|and|eax, 0xfffffffb
429195|bts|eax, 0x1e
429199|mov|dword ptr [rcx + 0x284], eax
42919f|call|0x422d50
4291b0|cmp|edi, -1
4291b3|je|0x429296
4291f9|mov|eax, 1
429204|test|byte ptr [rcx + 0x290], 1
42920b|je|0x429296
42924d|dec|dword ptr [rdx + 0x4880c]
429253|movsx|eax, word ptr [rbx]
42927d|cmp|dword ptr [rdx + 0x4880c], 0
429288|mov|dword ptr [rdx + 0x48808], eax
42928e|mov|rcx, rbx
429291|call|0x41f730
429296|mov|eax, 1
427c9a|mov|rdi, qword ptr [rip + 0x1e9f287]
427ca1|mov|esi, dword ptr [rdi + 0x48800]
427caa|je|0x427dcd
427cc0|movsxd|rax, esi
427cc3|imul|rbx, rax, 0x740
427cca|add|rbx, rdi
427ccd|test|byte ptr [rbx + 0x290], 2
427cd4|movsx|edx, word ptr [rbx + 4]
427cd8|mov|esi, edx
427cda|je|0x427dba
427d18|dec|dword ptr [rdi + 0x4880c]
427d48|cmp|dword ptr [rdi + 0x4880c], ebp
427d50|mov|dword ptr [rdi + 0x48808], ebp
427d56|mov|rcx, rbx
427d59|call|0x42f4c0
427d7e|call|0x426ec0
427d97|call|0x3b6000
427da6|call|0x3afbe0
427dab|mov|rcx, rbx
427dae|call|0x4200a0
427db3|or|dword ptr [rdi + 0x48818], 0x20
427dbd|jne|0x427cc0
4200aa|mov|rbx, rcx
4200e7|xor|edi, edi
4201d2|mov|rcx, rbx
4201e6|jmp|0x41f730'''
for line in ops.splitlines():
    pc,m,a=line.split('|');need(int(pc,16),m,a)
if ix[0x429146]['memory'][0]['rip_target']!='0x22c6f28' or ix[0x427c9a]['memory'][0]['rip_target']!='0x22c6f28':raise RuntimeError('global pool identity changed')
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def unchanged(regs,lo,hi):
    for pc in sorted(q for q in ix if lo<=q<hi):
        i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
        if {i.reg_name(r) for r in wr}&set(regs):raise RuntimeError('carrier changed '+hex(pc))
unchanged({'rbx','ebx','bx','bl','bh'},0x429204,0x429291)
unchanged({'rdx','edx','dx','dl','dh'},0x429204,0x429291)
unchanged({'rcx','ecx','cx','cl','ch'},0x42914d,0x429169)
unchanged({'rdi','edi','di','dil'},0x427ca1,0x427dd6)
unchanged({'rbx','ebx','bx','bl','bh'},0x427ccd,0x427db3)
unchanged({'rsi','esi','si','sil'},0x427cda,0x427dc3)
unchanged({'rbx','ebx','bx','bl','bh'},0x4200ad,0x4201dc)
unchanged({'rcx','ecx','cx','cl','ch'},0x4201d5,0x4201e6)

# Native helpers are named opaque boundaries. Fixed branch graphs classify
# input predicates, not reachable game states or executed test cases.
cases=[]
for name,non_null,bound,pending,expected_calls,expected_returns in [
 ('null',False,None,None,[],[0x42915c]),
 ('bound-mark',True,True,None,[0x42919f,0x4291bc,0x4291d3,0x4291e9],[0x429203,0x4292a5]),
 ('unbound-unmarked-no-op',True,False,False,[],[0x4292a5]),
 ('unbound-pending-unlink-clear',True,False,True,[0x429291],[0x4292a5])]:
    fixed={0x429153:non_null}
    if non_null:fixed[0x429169]=not bound
    if non_null and not bound:fixed[0x42920b]=not pending
    g=G.graph(ix,0x429140,0x4292a6,fixed=fixed)
    if [pc for pc,target in g['calls']]!=expected_calls or g['returns']!=expected_returns:raise RuntimeError('removal partition changed '+name)
    dec=0x42924d in g['visited'];clear=0x429291 in g['visited']
    if dec!=clear or dec!=(name=='unbound-pending-unlink-clear'):raise RuntimeError('decrement/clear partition changed')
    writes=[{'pc':hex(pc),'mnemonic':ix[pc]['mnemonic'],'args':ix[pc]['args'],'memory':[m for m in ix[pc]['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']} for pc in sorted(g['visited']) if any(m['role'] in ['w','rw'] and m['base']!='rsp' for m in ix[pc]['memory'])]
    if name in ['null','unbound-unmarked-no-op'] and writes:raise RuntimeError('new no-op object writes')
    cases.append({'name':name,'input_nonnull':non_null,'record284_mask04':bound,'record290_mask01':pending,'calls':g['calls'],'returns':[hex(q) for q in g['returns']],'direct_count_decrement':dec,'direct_clear':clear,'nonstack_writes':writes})
for a,b in [(0x42924d,0x429291),(0x427d18,0x427d59),(0x427d18,0x427d7e),(0x427d18,0x427dae),(0x4200aa,0x4201e6),(0x4201d2,0x4201e6)]:
    entry=0x429140 if a==0x42924d else 0x427c90 if a==0x427d18 else 0x4200a0
    if not G.dominates(gb[entry],a,b):raise RuntimeError('cleanup publication order changed')
if any(i['mnemonic']=='call' for pc,i in ix.items() if 0x427cc0<=pc<0x427d18):raise RuntimeError('new pre-decrement callback')
if any(i['mnemonic']=='call' for pc,i in ix.items() if 0x429204<=pc<0x429291):raise RuntimeError('new pending unlink callback')
for entry,base,expected in [(0x429140,'rdx',[0x42924d,0x42927d]),(0x427c90,'rdi',[0x427d18,0x427d48])]:
    hi=0x4292a6 if entry==0x429140 else 0x427dd8
    refs=[pc for pc,i in ix.items() if entry<=pc<hi and any(m['base']==base and m['displacement']<0x48810 and 0x4880c<m['displacement']+m['size'] and m['role']!='addr' for m in i['memory'])]
    if refs!=expected:raise RuntimeError('count guard/access population changed')
if not G.dominates(gb[0x427c90],0x427cd8,0x427d59):raise RuntimeError('next-link capture no longer precedes cleanup')
# First active-record read is dirty290; source does not test its ID0 before it.
if any(m['base']=='rbx' and m['displacement']<2 and 0<m['displacement']+m['size'] and m['role']!='addr' for pc,i in ix.items() if 0x427cc0<=pc<0x427d18 for m in i['memory']):raise RuntimeError('new pre-decrement ID access requires interpretation')
result={'producer_complete':True,'method':'A STATIC_ONLY removal branches and phase boundaries','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,
 'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],'annotation_prerequisites':[roles],
 'graphs':graphs,'original_bytes':1017,'partitions':cases,
 'retained_clear':{'manifest_sha256':mpin,'producer_sha256':sha(r/'prove.py'),'result_sha256':sha(r/'result-01.json'),'state_at_read':lineage['state_at_read'],'use':'Conditional clear ID0FFFF/active284zero, no reexecution or independent acceptance'},
 'established':['429140 NULL input returns0. Non-NULL input returns1 on every local normal-return branch, so return1 is not itself an immediate-release certificate.',
 'record284 mask04 set takes marking path: OR290 mask02, OR2AE mask01, clear108/110, clear284 mask04 and set bit30, then named binding/model helpers. It does not directly decrement count or call41F730. Opaque helper effects remain separate.',
 'mask04 clear and record290 mask01 clear takes a no-op success path with no nonstack writes or helper calls. Thus a source return1 can leave the supplied record unchanged; natural reachability of a particular state is unproved.',
 'mask04 clear and290 mask01 set unlinks pending neighbors/endpoints, decrements count, optionally resets cursor at new count0, then calls41F730 directly. It does not call4200A0 resource cleanup. Retained clear result applies only with its explicit valid/library/ABI premises.',
 '427C90 walks active-list head48800 and caches signed next WORD4 in ESI before any selected-record callback. record290 mask02 selects unlink/decrement/cleanup. Count decrement427D18 precedes42F4C0, optional child/owner cleanup,4200A0 and its final tail41F730. New count0 resets cursor before cleanup.',
 '4200A0 names embedded/resource cleanup calls before its final41F730 tail. Standard ABI preserves record in RBX until restoring it after RCX=record. Native helpers/resource releases, failures and child-loop termination are not inferred from names.',
 'Neither removal body has a count-positive guard before its selected DEC; new-count0 comparison occurs afterward. A coherent count/list/row premise is required. Active sweep does not test ID0 before dirty290/action; universal every-consumer-tests-ID-first wording needs qualification.'],
 'source_countermodels':{'return_success_without_free':{'input_nonnull':True,'record284':0x2010f9,'record290':0,'id':3,'return':1,'own_nonstack_writes':0,'own_calls':0,'limits':'Mathematical supplied source-state model, not naturally reached game state'},'selected_remove_with_count0':{'new_signed32_count':-1,'zero_reset_taken':False,'limits':'Fixed-width DEC calculation, not executed underflow/natural corruption'}},
 'affected_claims':['FABLE dual-list remover branch/return semantics and deferred marking versus immediate clear','OPUS render removal return/count/initialization contracts','Render-slot occupancy/lifetime evidence requirements and observer phase attribution'],
 'limits':['No FF12 instruction execution/emulation or live process; branch partitions and countermodels are source calculations.',
 'Complete local supplied CFGs only; named helper/library effects, standard ABI, valid pool/record/neighbor indices, nonaliasing and interference premises remain.',
 'Count-before-cleanup is source order, not atomic state or proof of reentrant/async observation. Stable coherent count/list/flags at operation boundaries and caller reachability remain open.',
 'Active/child loops require finite valid chains and helper progress; no general termination or malformed-input safety established.',
 'No new all-writer/caller/list census; existing canonical counts/history preserved. Conditional retained clear producer not independently accepted at read.',
 'Independent review/canonical incorporation pending; no whole OV or full database closure. K14 closed, EXP127 invalid, menu spent/unapproved.'],
 'cleanup':'Only owned offline evidence writes; all bounded children terminal, no game/PC/instrument/save/config/reference or peer consumer edits.'}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable result exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('PROVED original mark/no-op/unlink-clear contracts and count-before-cleanup order; STATIC_ONLY')
