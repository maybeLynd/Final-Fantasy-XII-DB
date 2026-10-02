"""Conditional original render-slot index/cursor/publication proof, STATIC_ONLY."""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if (P/'inspect.py').exists():raise RuntimeError('local inspect.py would shadow required standard library')
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise RuntimeError('actual capture incomplete')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');roles=V.validate(x)
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=pin or x['exe_sha256']!=pin:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,offset in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
 raise RuntimeError('unbacked range')
required=[('0x41f730','0x41fbe8'),('0x420480','0x420851'),('0x4269a0','0x426c85'),('0x4279b0','0x427af9')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('source population changed')
rows=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for i in r['instructions']};g=G.graph(ix,a,b)
 if g['visited']!=set(ix):raise RuntimeError('unaccounted original CFG')
 selected=[i for i in ix.values() if any(m['role']!='addr' and m['base'] in ['rbx','rdi','rsi','rcx','r8'] and m['displacement'] in [0,0x284,0x48808,0x4880c] for m in i['memory'])]
 rows.append({'entry':hex(a),'bytes':b-a,'instructions':len(ix),'calls':g['calls'],'selected_accesses':selected})

inspection_status=json.loads((P/'inspect-02.status.json').read_text());inspection=json.loads((P/'inspection-02.json').read_text())
if inspection_status.get('terminal') is not True or inspection_status.get('exit')!=0 or inspection_status.get('exception') is not None or inspection_status['driver_sha256']!=sha(P/'inspect-slot-source.py') or inspection.get('inspection_complete') is not True or inspection['driver_sha256']!=sha(P/'inspect-slot-source.py') or inspection['source_sha256']!=sha(P/'source-01.json') or len(inspection['ranges'])!=4:raise RuntimeError('required actual inspection failed')
ix={int(i['pc'],16):i for r in x['ranges'] for i in r['instructions']}
gb={int(r['start'],16):G.graph({int(i['pc'],16):i for i in r['instructions']},int(r['start'],16),int(r['end_exclusive'],16)) for r in x['ranges']}
ops='''41f744|xor|edx, edx
41f74b|mov|r8d, 0x740
41f751|mov|rbx, rcx
41f754|call|0x861ec0
41f768|or|ebp, 0xffffffff
41f795|mov|word ptr [rbx], bp
42049a|or|dword ptr [rcx + 0x284], 0x2010f9
4204b8|mov|rsi, rcx
4204ef|or|dword ptr [rcx + 0x284], 0x4000
4269af|mov|rsi, qword ptr [rip + 0x1ea0572]
4269b6|mov|edi, 0xa0
4269bb|mov|rbx, rsi
4269c0|mov|rcx, rbx
4269c3|call|0x41f730
4269c8|add|rbx, 0x740
4269cf|sub|rdi, 1
4269d3|jne|0x4269c0
4269df|xor|ebx, ebx
4269ed|mov|qword ptr [rsi + 0x48808], rbx
4279c4|mov|rbx, qword ptr [rip + 0x1e9f55d]
4279d7|call|0x4278e0
4279dc|cmp|ax, -1
4279e0|je|0x4279e9
4279e2|xor|eax, eax
4279e9|cmp|dword ptr [rbx + 0x4880c], 0xa0
4279f3|jge|0x4279e2
4279fa|movsxd|rsi, dword ptr [rbx + 0x48808]
427a06|imul|rdi, rsi, 0x740
427a0d|add|rdi, rbx
427a10|mov|rcx, rdi
427a13|call|0x41f730
427a47|mov|dword ptr [rbx + 0x48814], esi
427a4d|mov|word ptr [rdi], si
427a6e|mov|rcx, rdi
427a71|call|0x420480
427a76|or|dword ptr [rdi + 0x290], 1
427a7d|xor|eax, eax
427a7f|inc|dword ptr [rbx + 0x4880c]
427a85|cmp|dword ptr [rbx + 0x4880c], 0xa0
427a94|jl|0x427a9e
427a96|mov|dword ptr [rbx + 0x48808], eax
427a9c|jmp|0x427adc
427a9e|mov|ecx, dword ptr [rbx + 0x48808]
427ab0|inc|ecx
427ab2|mov|dword ptr [rbx + 0x48808], ecx
427ab8|cmp|ecx, 0xa0
427abe|jl|0x427ac8
427ac0|mov|ecx, eax
427ac2|mov|dword ptr [rbx + 0x48808], eax
427ac8|movsxd|rdx, ecx
427acb|imul|r8, rdx, 0x740
427ad2|cmp|dword ptr [r8 + rbx + 0x284], eax
427ada|jne|0x427ab0
427adc|mov|rax, rdi'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required slot operation changed '+hex(pc))
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for regs,lo,hi in [({'rsi','esi','si','sil'},0x4279fa+7,0x427a4d),({'rdi','edi','di','dil'},0x427a10,0x427adc),({'rax','eax','ax','al','ah'},0x427a9e,0x427ada)]:
 for pc in sorted(q for q in ix if lo<=q<hi):
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
  if {i.reg_name(r) for r in wr}&regs:raise RuntimeError('slot/index/zero carrier changed '+hex(pc))
for a,b in [(0x4279e9,0x427a13),(0x427a13,0x427a4d),(0x427a4d,0x427a71),(0x427a71,0x427a7f),(0x427a7f,0x427adc)]:
 if not G.dominates(gb[0x4279b0],a,b):raise RuntimeError('publication order changed')
for pc,role,size in [(0x4279fa,'r',4),(0x427a4d,'w',2),(0x42049a,'rw',4),(0x427a7f,'rw',4),(0x4269ed,'w',8),(0x427ad2,'r',4)]:
 if (ix[pc]['memory'][0]['role'],ix[pc]['memory'][0]['size'])!=(role,size):raise RuntimeError('required slot memory width/role changed')
# No branch checks the starting cursor between its load and the first clear call.
if any(ix[pc]['mnemonic'].startswith('j') or ix[pc]['mnemonic'] in ['cmp','test'] for pc in ix if 0x4279fa<pc<0x427a13):raise RuntimeError('new cursor gate requires adjudication')
# Exact first init flag store precedes any original call; not a whole-call lifetime claim.
if any(i['mnemonic']=='call' for pc,i in ix.items() if 0x420480<=pc<0x42049a):raise RuntimeError('pre-flag callback changed')
local_metadata_writes=[{'pc':hex(pc),'args':i['args']} for pc,i in ix.items() if 0x420480<=pc<0x420851 and any(m['base'] in ['rcx','rsi'] and m['role'] in ['w','rw'] and m['displacement'] in [0,0x284] for m in i['memory'])]
if [(r['pc'],r['args']) for r in local_metadata_writes]!=[('0x42049a','dword ptr [rcx + 0x284], 0x2010f9'),('0x4204ef','dword ptr [rcx + 0x284], 0x4000')]:raise RuntimeError('metadata direct identity/active writes changed')
# A mathematical invariant of the supplied circular increment/wrap loop.
for c in range(160):
 visits=[(c+k)%160 for k in range(1,161)]
 if set(visits)!=set(range(160)) or len(set(visits))!=160 or visits[-1]!=c:raise RuntimeError('cursor cycle proof failed')
 if c!=(c&0xffff):raise RuntimeError('bounded self-index representation failed')
examples=[{'live_count':0,'starting_cursor':c,'passes_signed_count_cap':True,'in_declared_row_domain':0<=c<160,'relative_first_clear_address':c*0x740} for c in [-1,0,159,160]]
result={'producer_complete':True,'method':'A STATIC_ONLY conditional render-slot self-index/cursor/publication proof','driver_sha256':sha(Path(__file__)),
 'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],'annotation_prerequisites':[roles],
 'original_bytes':sum(r['bytes'] for r in rows),'instruction_assertions':len(ops.splitlines()),'graphs':rows,
 'clear_and_init':'41F730 requests zero-fill of740h bytes at its record pointer and directly stores WORD0=FFFF. System4269A0 calls it160 times at740h stride then storesQWORD0 to48808, jointly seeding DWORD cursor48808 and livecount4880C. Native fill and opaque callee preservation are separate premises; not captured live default state.',
 'allocation_identity':'After name-absence returnFFFF and signed livecount<160 gate,4279B0 loads starting cursor viaMOVSXD and forms record=base+cursor*740h before any independent cursor-domain check. Following normal clear return, it publishes pending tail and WORD[record]=low16(cursor), calls420480(record,...), then dirty290 OR1, increments livecount, chooses next cursor and returnsrecord. For cursor0..159 the storedWORD equals the physical row index; invalid cursor cannot be excluded by the count cap alone.',
 'active_publication':'420480 first ORs record284 with2010F9h before any call in that body. Thus the allocator self-index write precedes this active-flag boundary, which precedes the caller livecount increment under normal native returns. These source stages are not an atomic snapshot or observed scheduling window. Its supplied direct metadata writes do not clear0 or284; indirect effects/aliasing remain unproved.',
 'scan_invariant':'With starting cursor0..159, each scan iteration advances byone and wraps160 to0, keeping the domain0..159. One full cycle visits all160 indices once. Given stable readable row flags and at leastone zero284, the supplied scan stops within160 visits. A count<160 is not itself a proof that a zero284 exists; count/occupancy coherence must be established separately.',
 'countermodels':{'cursor_examples':examples,'no_free_row':{'live_count_before':0,'new_count':1,'all160_flags_nonzero_after_metadata':True,'source_count_enters_scan':True,'consequence':'Under stable flags, the mathematical supplied loop cycles with no terminating zero. Not an executed hang, naturally reachable state or game fault.'}},
 'rig_consumer_implication':'Fresh successful allocation under valid cursor/native preservation establishes the self-index source forwarded by the factory into rig68 and by4215A0 into6C. The active flag is published at a separate instruction phase. Caller validity across later opaque calls/release/scheduling still requires its own evidence; no universal healthy-owner guarantee.',
 'limits':['No original-code/native/emulator or live execution;160-cycle calculations and state countermodels are mathematical source analysis.',
 'Complete local original bodies, not complete all-writer/caller/alias/effect closure. Existing attributed +0 census only preparation.',
 'Valid unchanged global pool/private frames and native ABI, normal clear/metadata returns, no aliasing or interference, valid starting cursor and occupancy coherence are explicit premises.',
 'Native fill/library/resource callback effects, lifetime/reuse, actual cursor/active/list invariant at natural callers and observer scheduling/atomicity remain open.',
 'Name lookup4278E0 boundary is not re-proved; allocator path assumes its absence resultFFFF.',
 'Inspector01 and its output are invalid stdlib-shadow evidence; corrected inspector02/shadow control valid feasibility only, no prior semantic acceptance.',
 'Independent review and canonical incorporation pending; EXP127 invalid, K14 closed, menu spent/unapproved, no wholeOV closure or full database completion.']}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable result exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED conditional slot self-index/cursor invariant and publication order; STATIC_ONLY, native state unresolved')
