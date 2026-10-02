"""Original pre-keyed cache insertion ABI/unsigned key forwarding. STATIC_ONLY."""
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
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x.get('driver_sha256')!=sha(P/'capture-index-path.py'):raise RuntimeError('actual capture incomplete')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');roles=V.validate(x)
storage_status=json.loads((P/'capture-02.status.json').read_text())
if storage_status.get('terminal') is not True or storage_status.get('exit')!=0 or storage_status.get('exception') is not None or storage_status['driver_sha256']!=sha(P/'capture-storage.py') or not(P/'capture-02.stdout').read_bytes() or(P/'capture-02.stderr').read_bytes():raise RuntimeError('required storage capture failed')
z=json.loads((P/'source-02.json').read_text())
if z.get('wrapper_complete') is not True or z.get('invocation_driver_sha256')!=sha(P/'capture-storage.py') or z.get('driver_sha256')!=sha(P/'capture-index-path.py') or z['exe_sha256']!=PIN:raise RuntimeError('actual storage capture incomplete')
storage_roles=V.validate(z)
prior_status=json.loads((P/'prove-01.status.json').read_text());prior_result=json.loads((P/'result-01.json').read_text())
if prior_status.get('terminal') is not True or prior_status.get('exit')!=0 or prior_status.get('exception') is not None or prior_status['driver_sha256']!=sha(P/'prove-key-forwarding-01.py') or prior_result.get('producer_complete') is not True or prior_result['driver_sha256']!=sha(P/'prove-key-forwarding-01.py') or not(P/'prove-01.stdout').read_bytes() or(P/'prove-01.stderr').read_bytes():raise RuntimeError('required archived forwarding proof failed')
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
    for vs,rva,size,offset in secs:
        if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
    raise RuntimeError('unbacked original range')
required=[('0x1d6a20','0x1d6a6d'),('0x20b680','0x20b83b'),('0x20b5f0','0x20b675')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('source population changed')
storage_required=[('0x1ae9b0','0x1aeafc'),('0x1ae850','0x1ae9a8'),('0x20ba70','0x20bb0c'),('0x16d840','0x16da54')]
if [(r['start'],r['end_exclusive']) for r in z['ranges']]!=storage_required:raise RuntimeError('storage source population changed')
ix={};gb={};graphs=[]
for r in x['ranges']+z['ranges']:
    a,b=int(r['start'],16),int(r['end_exclusive'],16)
    if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
    local={int(i['pc'],16):i for i in r['instructions']};ix.update(local);g=G.graph(local,a,b)
    if g['visited']!=set(local):raise RuntimeError('unaccounted original CFG')
    gb[a]=g;graphs.append({'entry':hex(a),'bytes':b-a,'instructions':len(local),'calls':g['calls'],'returns':[hex(z) for z in g['returns']]})
def need(pc,m,a):
    if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required insertion operation changed '+hex(pc))
ops='''1d6a34|mov|ebx, r9d
1d6a37|mov|edi, r8d
1d6a3a|mov|rsi, rdx
1d6a3d|mov|ebp, ecx
1d6a3f|call|0x20c700
1d6a44|mov|rcx, rax
1d6a47|mov|dword ptr [rsp + 0x20], ebx
1d6a4b|mov|r9d, edi
1d6a4e|mov|r8, rsi
1d6a51|mov|edx, ebp
1d6a53|call|0x20b680
20b680|mov|dword ptr [rsp + 0x10], edx
20b68f|sub|rsp, 0x40
20b6a4|mov|r14d, r9d
20b6a7|mov|r12, r8
20b6aa|mov|ebp, edx
20b6ac|mov|rsi, rcx
20b6af|add|rcx, 0x58
20b6b3|call|0x5cd4f0
20b6c8|cmp|dword ptr [rax + 0x20], ebp
20b6cb|jb|0x20b6d6
20b6e3|cmp|ebp, dword ptr [rbx + 0x20]
20b6e6|jae|0x20b6eb
20b6ef|cmp|rbx, rax
20b6f2|je|0x20b73f
20b721|mov|edx, ebp
20b726|call|0x20c300
20b73f|lea|rcx, [rsi + 0x98]
20b746|call|0x1ba860
20b758|test|rax, rax
20b75b|je|0x20b7e4
20b761|mov|edx, dword ptr [rsp + 0xa0]
20b768|cmp|edx, 5
20b788|cmp|edx, 3
20b7d0|lea|rdx, [rsp + 0x88]
20b7d8|lea|rcx, [rsi + 0x20]
20b7dc|call|0x20b5f0
20b7e1|mov|qword ptr [rax], rbx
20b5f0|sub|rsp, 0x48
20b607|mov|r9d, dword ptr [rdx]
20b610|cmp|dword ptr [r8 + 0x20], r9d
20b614|jb|0x20b61f
20b62f|cmp|dword ptr [rdx], ecx
20b631|jae|0x20b66c
20b633|mov|ecx, dword ptr [rdx]
20b635|lea|r9, [rsp + 0x30]
20b64e|mov|dword ptr [rsp + 0x30], ecx
20b652|mov|rcx, r10
20b659|mov|qword ptr [rsp + 0x38], 0
20b662|call|0x1ae9b0
20b66c|add|rax, 0x28'''
for line in ops.splitlines():
    pc,m,a=line.split('|');need(int(pc,16),m,a)
if gb[0x1d6a20]['calls']!=[(0x1d6a3f,'0x20c700'),(0x1d6a53,'0x20b680')]:raise RuntimeError('wrapper boundaries changed')
if gb[0x20b5f0]['calls']!=[(0x20b662,'0x1ae9b0')]:raise RuntimeError('map helper boundaries changed')
if [(ix[pc]['mnemonic'],ix[pc]['args']) for pc in sorted(ix) if 0x20b684<=pc<0x20b68f] != [('push','rbp'),('push','rsi'),('push','rdi'),('push','r12'),('push','r13'),('push','r14'),('push','r15')]:raise RuntimeError('insertion frame changed')
if 0x10+(7*8)+0x40!=0x88 or 0x28+(7*8)+0x40!=0xa0:raise RuntimeError('original frame calculation failed')
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def unchanged(regs,lo,hi,allow=()):
    for pc in sorted(q for q in ix if lo<=q<hi and q not in allow):
        i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
        if {i.reg_name(r) for r in wr}&set(regs):raise RuntimeError('key/carrier changed '+hex(pc))
unchanged({'rbp','ebp','bp','bpl'},0x1d6a3f,0x1d6a53)
unchanged({'rdx','edx','dx','dl','dh'},0x1d6a53,0x1d6a53)
unchanged({'rbp','ebp','bp','bpl'},0x20b6ac,0x20b839)
unchanged({'rsp','esp','sp','spl'},0x20b693,0x20b823,allow=tuple(pc for pc,target in gb[0x20b680]['calls']))
unchanged({'rdx','edx','dx','dl','dh'},0x20b7d8,0x20b7dc)
unchanged({'rdx','edx','dx','dl','dh'},0x20b5f0,0x20b633)
unchanged({'rcx','ecx','cx','cl','ch'},0x20b635,0x20b652)
unchanged({'r9','r9d','r9w','r9b'},0x20b63a,0x20b662)
for entry,a,b in [(0x1d6a20,0x1d6a3d,0x1d6a51),(0x1d6a20,0x1d6a51,0x1d6a53),(0x20b680,0x20b680,0x20b7dc),(0x20b680,0x20b6aa,0x20b726),(0x20b680,0x20b7d0,0x20b7dc),(0x20b5f0,0x20b633,0x20b662),(0x20b5f0,0x20b64e,0x20b662)]:
    if not G.dominates(gb[entry],a,b):raise RuntimeError('key forwarding dominance changed')
key_writes=[]
for pc,i in ix.items():
    if not 0x20b693<=pc<0x20b7dc:continue
    for m in i['memory']:
        if m['role'] not in ['w','rw'] or m['base']!='rsp':continue
        if m['index'] not in [None,'']:raise RuntimeError('unknown private-frame write')
        if m['displacement']<0x8c and 0x88<m['displacement']+m['size']:key_writes.append(i['pc'])
if key_writes:raise RuntimeError('original key home overwritten')
for pc,size,role in [(0x20b680,4,'w'),(0x20b64e,4,'w'),(0x20b607,4,'r'),(0x20b633,4,'r'),(0x20b659,8,'w')]:
    if (ix[pc]['memory'][0]['size'],ix[pc]['memory'][0]['role'])!=(size,role):raise RuntimeError('key/pair width-role changed')
helper_input_writes=[i['pc'] for pc,i in ix.items() if 0x20b5f0<=pc<0x20b675 and any(m['base']=='rdx' and m['role'] in ['w','rw'] for m in i['memory'])]
if helper_input_writes:raise RuntimeError('map helper input mutated')
named=[(hex(pc),target) for g in gb.values() for pc,target in g['calls']]
if any(target in ['0x20c440','0x20be50','0x20c1b0'] for pc,target in named):raise RuntimeError('new local normalizer boundary')
# Original native key creation: all five creation sites copy the entire16-byte
# pair. Valid fresh30h allocation/nonwrapping pointer is an explicit premise.
copy_sites=[(0x1ae9b0,0x1aea1c,0x1aea1f,'rbp',0x1aea28,0x1aea2c,'r14',0x1aea38,0x1aea3b),
            (0x1ae9b0,0x1aea98,0x1aea9b,'r13',0x1aeaa4,0x1aeaa8,'r14',0x1aeab4,0x1aeab7),
            (0x1ae850,0x1ae90e,0x1ae911,'r14',0x1ae91a,0x1ae91e,'r15',0x1ae92a,0x1ae92d),
            (0x1ae850,0x1ae94f,0x1ae952,'rbx',0x1ae95b,0x1ae95f,'r15',0x1ae96b,0x1ae96e),
            (0x20ba70,0x20bac5,0x20bac8,'r14',0x20bad1,0x20bad5,'rbp',0x20bae2,0x20bae5)]
for pc,m,a in [(0x1ae9cb,'mov','r14, r9'),(0x1aea4b,'mov','r9, r14'),(0x1aea59,'call','0x20ba70'),(0x1aead4,'mov','r8, r14'),(0x1aeada,'call','0x1ae850'),(0x1ae874,'mov','r15, r8'),(0x20ba8d,'mov','rbp, r9')]:need(pc,m,a)
unchanged({'r14','r14d','r14w','r14b'},0x1ae9ce,0x1aeaf4)
unchanged({'r15','r15d','r15w','r15b'},0x1ae877,0x1ae9a1)
unchanged({'rbp','ebp','bp','bpl'},0x20ba90,0x20baf5)
copies=[]
aliases={'rbp':{'rbp','ebp','bp','bpl'},'r13':{'r13','r13d','r13w','r13b'},'r14':{'r14','r14d','r14w','r14b'},'rbx':{'rbx','ebx','bx','bl','bh'}}
for entry,alloc,save,node,load_pc,store_pc,src,receiver,balance in copy_sites:
    need(alloc,'call','qword ptr [rax + 0x10]');need(save,'mov',node+', rax')
    add=save+len(bytes.fromhex(ix[save]['bytes']));need(add,'add','rax, 0x20')
    need(load_pc,'movups','xmm0, xmmword ptr ['+src+']');need(store_pc,'movups','xmmword ptr [rax], xmm0')
    need(receiver,'mov','rcx, '+node);need(balance,'call','0x16d840')
    unchanged(aliases[node],add,balance)
    if not G.dominates(gb[entry],alloc,store_pc) or not G.dominates(gb[entry],store_pc,balance):
        # The pointer+20==0 guard can bypass the copy. Do not turn this into an
        # unconditional dominance claim: valid nonwrapping30h pointer selects
        # the copy edge, proved below using the original guard identity.
        if not G.dominates(gb[entry],alloc,store_pc):raise RuntimeError('allocation does not dominate copy')
    guard=add+len(bytes.fromhex(ix[add]['bytes']));need(guard,'je',hex(store_pc+len(bytes.fromhex(ix[store_pc]['bytes']))))
    for pc in [load_pc,store_pc]:
        if len(ix[pc]['memory'])!=1 or ix[pc]['memory'][0]['size']!=16 or ix[pc]['memory'][0]['role']!=('r' if pc==load_pc else 'w'):raise RuntimeError('pair copy width/role changed')
    copies.append({'entry':hex(entry),'allocator_call':hex(alloc),'source_pair_register':src,'copy_load':hex(load_pc),'copy_store':hex(store_pc),'node_pair_interval':[0x20,0x30],'guard':'node+20h !=0 under valid fresh nonwrapping30h node','balance_call':hex(balance)})
if [(pc,target) for pc,target in gb[0x1ae9b0]['calls'] if target in ['0x20ba70','0x1ae850']]!=[(0x1aea59,'0x20ba70'),(0x1aeada,'0x1ae850')]:raise RuntimeError('native key-creation alternatives changed')
for entry,end in [(0x1ae9b0,0x1aeafc),(0x1ae850,0x1ae9a8),(0x20ba70,0x20bb0c)]:
    own=[pc for pc,i in ix.items() if entry<=pc<end and i['mnemonic']=='movups' and any(m['role']=='w' for m in i['memory'])]
    if own!=[store for e,alloc,save,node,load,store,src,receiver,balance in copy_sites if e==entry]:raise RuntimeError('pair copy population changed')
if gb[0x16d840]['calls'] or gb[0x16d840]['tails']:raise RuntimeError('new balancing callback/effect boundary')
header_writes=[]
for pc,i in ix.items():
    if not 0x16d840<=pc<0x16da54:continue
    for m in i['memory']:
        if m['role'] not in ['w','rw']:continue
        if m['index'] not in [None,''] or m['base'] not in ['rcx','rdx','r8','r9','rax'] or not 0<=m['displacement']<m['displacement']+m['size']<=0x19:raise RuntimeError('balancing write reaches value pair or unknown address')
        header_writes.append({'pc':hex(pc),'base':m['base'],'interval':[m['displacement'],m['displacement']+m['size']],'role':m['role']})
if not header_writes:raise RuntimeError('zero balancing footprint')
result={'producer_complete':True,'method':'A STATIC_ONLY pre-keyed insertion ABI and key forwarding','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,
 'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','source-02.json']],'annotation_prerequisites':[roles,storage_roles],'graphs':graphs,'original_bytes':2017,
 'entry_abi':{'1D6A20':{'ecx':'precomputed key32','rdx':'pointer forwarded as insertion r8','r8d':'forwarded insertion r9d','r9d':'forwarded insertion arg5 DWORD'},'20B680':{'rcx':'service/map receiver','edx':'key32','r8':'input data-pointer carrier','r9d':'size/value32 carrier','arg5_at_entry_rsp28':'numeric kind32'}},
 'key_stack':{'entry_saved_key_offset':0x10,'push_bytes':56,'sub_bytes':64,'current_saved_key_offset':0x88,'width':4,'overlapping_own_writes_before_map_call':key_writes,'kind_current_offset':0xa0},
 'map_helper':{'20B5F0_input':'RDX -> original DWORD key home at caller SP+88h','pair_key_current_offset':0x30,'pair_key_width':4,'pair_value_current_offset':0x38,'pair_value_seed':0,'native_insert_boundary':'1AE9B0 with R9 pointing to private key/value pair; no native effect executed','result_boundary':'returned node+28h value slot, caller stores its descriptor pointer there under normal helper contract'},
 'native_key_creation':{'copy_sites':copies,'balancing_header_writes':header_writes,'premises':'Valid fresh disjoint nonwrapping30h allocation, readable original pair/private stack, valid pointer-linked nodes/header, ABI/normal returns/no interference. Allocator callbacks and predecessor/successor helpers remain named native boundaries; no execution or initialized state observed.'},
 'established':['1D6A20 receives a precomputed DWORD key in ECX and forwards unchanged low32 through saved EBP to insertion EDX after obtaining the service receiver. Its data-pointer,size/value32 and numeric-kind32 arguments are distinct; no pathname or prefix processing occurs in this supplied wrapper.',
 '20B680 uses full DWORD key comparisons with unsigned JB/JAE and unchanged EBP. The existing-key arm forwards EDX=EBP to20C300; the new-descriptor arm passes the exact saved DWORD key home to20B5F0. No own full-width stack write overlaps that saved home before the map call.',
 '20B5F0 reads the full DWORD key and uses unsigned comparison. On insertion preparation it copies the full DWORD to private pair+0, seeds QWORD pair+8=0 and forwards the pair to named native tree boundary1AE9B0. No local BTR31/hash/prefix normalization or own input-key write on the supplied value path.',
 'All32 key bits are preserved to these boundaries, including bit31. Numeric ABI preservation is an invariant of the MOV widths/carriers, not a sampled native value. It does not prove that natural callers supply bit31-set keys.',
 'The path normalizer output domain alone therefore cannot establish the whole insertion entry input domain. Actual caller derivation and native map effects need their own evidence; absence/collision/eviction conclusions cannot come from lookup normalization alone.',
 'All supplied original native new-node creation alternatives in1AE9B0/1AE850/20BA70 copy16 bytes from the same input pair into node20..30 without key masking. Complete leaf16D840 balances only node/header pointer/color spans0..19 and has no calls; under valid node/header identities it leaves pair20..30 intact. Thus a successful valid new-node path preserves the full32 key in node20. Caller descriptor store through returned value slot28 changes the value pointer, not key20. Allocator/caller/natural-state premises remain, not merely assumed tree-copy semantics.'],
 'source_countermodel':{'key':0x80000000,'forwarded_key_at_existing_or_new_boundary':0x80000000,'would_be_31bit_masked_key':0,'method':'Fixed-width source representation calculation, not original/native execution or naturally inserted record'},
 'affected_claims':['FABLE path-resolution and OV33E2 insert-domain prerequisite','OPUS cache insertion key32/data/size/kind ABI and lookup-vs-insert domain contract'],
 'limits':['No FF12 instructions executed or emulated, no live process or natural cache contents captured.',
 'Complete seven supplied local bodies, not full transitive native library/helper or all-caller closure. Valid initialized service/map/data/private-frame, nonaliasing, standard ABI/normal returns and stable ordered tree are explicit premises.',
 'Original new-node pair copies and header-only balancing writes proved conditionally; allocator callbacks/predecessor-successor/20C300/20B0F0/lock/wrapper getter and actual replacement/lifetime effects remain named boundaries, not proved from stubs or names.',
 'Full32 entry domain does not prove naturally supplied high-bit/nonhash keys; original callers may constrain inputs. No collision/archive namespace/eviction or six-candidate acceptance claim.',
 'Prior accepted normalizer/prefix result not recaptured/retested. Its startup/native/import/locale limits remain.',
 'Independent review and canonical consumption pending; no wholeOV or fullL1L2 closure. K14 closed, EXP127 invalid, menu spent/unapproved.'],
 'cleanup':'Owned offline evidence writes only; no game/PC/native instrumentation/save/config/reference or peer consumer changes.'}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-02.json')
if out.exists():raise RuntimeError('immutable result exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('PROVED conditional pre-keyed full32 insertion forwarding; natural caller/native map effects OPEN')
