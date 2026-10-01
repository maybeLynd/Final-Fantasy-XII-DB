"""Original skeletonRef binding/copy dataflow proof. No machine-code execution or gameplay."""


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
if lineage['parent_manifest_sha256']!='57ff5303f24bd3451904cccf600210613ce097d295173f840a70fc30f0f70923':raise RuntimeError('retained parent identity changed')
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

if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x3713c0','0x371497'),('0x372820','0x372f54'),('0x20e600','0x20e60a')]:raise RuntimeError('required source population changed')
ix={};graphs=[]
for r in x['ranges']+y['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b)
 if set(local)!=g['visited']:raise RuntimeError('unaccounted original source')
 graphs.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls']})
ops='''3713ca|mov|rbx, rcx
3713cd|mov|ecx, dword ptr [rcx + 0x80]
3713d3|call|0x20e600
3713db|call|0x3ab7f0
3713e0|mov|rcx, rax
3713e3|call|0x20e620
3713ec|mov|dword ptr [rbx + 0x84], eax
3713f2|cmp|di, -1
3713f6|je|0x37148c
371422|xor|ecx, ecx
37142a|call|0x20e620
371435|mov|dword ptr [rbx + 0x94], eax
371443|je|0x37148c
371445|cmp|dword ptr [rbx + 0x90], 0
37144c|jle|0x37148c
37144e|mov|ecx, dword ptr [rbx + 0x84]
371454|call|0x20e600
371459|add|eax, dword ptr [rbx + 0x90]
37145f|movsxd|rcx, eax
371462|call|0x20e620
371469|mov|dword ptr [rbx + 0x94], eax
371477|je|0x37148c
371487|call|0x3e1c50
372825|push|rbx
372826|push|rsi
372827|push|r12
372829|sub|rsp, 0x30
372832|mov|rsi, rcx
37290d|xor|ecx, ecx
37290f|call|0x20e620
372914|mov|dword ptr [rsi + 0x94], eax
37291a|mov|dword ptr [rsi + 0x90], r12d
372921|imul|eax, dword ptr [rbp + 0xc], 0x149
372928|movzx|ecx, word ptr [rbp + 0x38]
37292c|add|ecx, eax
37292e|lea|eax, [rcx*2 + 0xf]
372935|mov|rcx, qword ptr [rsp + 0x70]
37293a|cdq|
37293b|and|edx, 0xf
37293e|lea|ebx, [rdx + rax]
372941|and|ebx, 0xfffffff0
372944|call|0x20e620
372949|mov|rdi, qword ptr [rsp + 0x80]
372951|mov|dword ptr [rsi + 0x80], eax
372962|test|rdi, rdi
372965|je|0x3729c2
372969|mov|dword ptr [rsi + 0x90], ebx
37296f|call|0x20e600
372977|call|0x3ab7f0
37297c|mov|rcx, rax
37297f|call|0x20e620
372986|mov|dword ptr [rsi + 0x84], eax
37298c|call|0x20e600
372991|add|eax, dword ptr [rsi + 0x90]
372997|movsxd|rcx, eax
37299a|call|0x20e620
37299f|movsxd|rbx, dword ptr [rsp + 0x88]
3729a9|mov|dword ptr [rsi + 0x94], eax
3729af|call|0x20e600
3729b4|mov|rcx, rax
3729b7|mov|r8, rbx
3729ba|mov|rdx, rdi
3729bd|call|0x861eba
3729c2|mov|rcx, rsi
3729ca|call|0x3713c0
20e600|mov|eax, ecx
20e602|add|rax, qword ptr [rip + 0x1d74f27]
20e609|ret|
20e620|sub|ecx, dword ptr [rip + 0x1d74f0a]
20e626|mov|eax, ecx
20e628|ret|'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required operation changed '+hex(pc))
writers=[]
for pc in [0x371435,0x371469,0x372914,0x3729a9]:
 mem=ix[pc]['memory'][0]
 if mem['displacement']!=0x94 or mem['size']!=4 or mem['role']!='w':raise RuntimeError('positive writer width/role changed')
 writers.append({'pc':hex(pc),'bytes':ix[pc]['bytes'],'args':ix[pc]['args']})
import csv,capstone
rows=list(csv.DictReader((P/'retained-accesses.tsv').read_text().splitlines(),delimiter='\t'))
for row in writers:
 matches=[r for r in rows if int(r['site'],16)==int(row['pc'],16)]
 if len(matches)!=1 or matches[0]['kind']!='w' or matches[0]['instruction']!='mov '+row['args']:raise RuntimeError('retained table writer correspondence failed')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
# Actual register-access decoding: preserve owner/workspace offset/copy source
# and signed32 length carriers across their defined segments. Opaque calls
# respect nonvolatile Windows x64 registers; aliased side effects are excluded.
for regs,lo,hi in [({'rbx','ebx','bx','bl'},0x3713cd,0x37148c),({'rsi','esi','si','sil'},0x372835,0x3729bd),({'rbx','ebx','bx','bl'},0x372944,0x37299f),({'rdi','edi','di','dil'},0x372951,0x3729bd),({'rbx','ebx','bx','bl'},0x3729a6,0x3729bd)]:
 for pc in sorted(q for q in ix if lo<=q<hi):
  ins=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,w=ins.regs_access()
  if {ins.reg_name(r) for r in w}&regs:raise RuntimeError('nonvolatile carrier changed '+hex(pc))
g=G.graph({pc:i for pc,i in ix.items() if 0x372820<=pc<0x372f54},0x372820,0x372f54)
if not G.dominates(g,0x372914,0x3729bd) or not G.dominates(g,0x3729a9,0x3729bd):raise RuntimeError('write not before optional copy')
# Fixed-code modular identity: decoder low32=B_low+ref; ADD EAX truncates;
# MOVSXD preserves the low32; encoder reads onlyECX and subtractsB_low. Hence
# newref=low32(ref+offset) if base stable. Signextension is discarded by encoder.
U=1<<32;examples=[]
for base,ref,offset in [(0,0xcb000000,0x6000),(0,0xfffffff0,0x20),(0x1234567800001000,0x40,0x20)]:
 decoded=(base+ref)&((1<<64)-1);summed=(decoded+offset)%U
 signed=summed if summed<1<<31 else summed-U
 encoded=((signed%U)-(base%U))%U
 if encoded!=(ref+offset)%U:raise RuntimeError('modular identity failed')
 examples.append({'base':hex(base),'ref':hex(ref),'offset':hex(offset),'signed_temporary':signed,'encoded':hex(encoded),'decoded_final':hex((base+encoded)&((1<<64)-1))})
pre=json.loads((P/'consumer-preimage.json').read_text())
if sha(P/'retained-accesses.tsv')!=pre['access_table_sha256'] or 'no writer' not in pre['row']:raise RuntimeError('consumer/table preimage changed')
result={'producer_complete':True,'method':'A STATIC_ONLY original skeletonRef producer/copy call dataflow','driver_sha256':sha(Path(__file__)),
 'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles],'instruction_assertions':len(ops.splitlines()),'graphs':graphs,'positive_writers':writers,
 'binding':'372820 storesEncode(callerarg5) into80. Ifcallerarg7sourceblobnonnull, storescomputedworkspaceoffset in90, resolvesworkspacevia3AB7F0 into84, then94=low32(84+90). It passesDecode94 asRCX destination, callerarg7 asRDX source, signed32 callerarg8 extendedto64 asR8 to861EBA, then calls3713C0 torefreshbinding.',
 'refresh':'3713C0 group16FFFF skips before clearing94. Otherwise writesencodedNULL; onlyA0decodednonnull and90signedpositive admit new94=low32(84+90), thennonnull decode permits3E1C50. Opaque section-query/native effects not proved.',
 'abi':{'prologue_frame_bytes':72,'arg5_entry28_current70':'workspace representation','arg7_entry38_current80':'optional sourceblob','arg8_entry40_current88':'onlyDWORDread/MOVSXD; negative length unsafe/unproved'},
 'workspace_offset':'Original32bit IMUL149*headerDWORD_C, pluszeroextendedWORD_38, LEA(2*x+15),CDQ/AND15 correction andANDFFFFFFF0. No unrestricted safe-size or author-domain proof.',
 'modular_binding_identity':'newref=low32(ref84+offset90) understablebase. MOVSXD doesnotleavea negative64 destination becauseencoder readsECX only; finaldecodeaddsfull64base.',
 'mathematical_controls':examples,'consumer_preimage':pre,
 'limits':['No original native/harness/live execution; modular examples are source calculations, general equality follows fixed-width ring operations',
 'Positive four suppliedwriters verified; not a complete allwriter/bulk-copy/alias or temporal lifetime closure',
 'Validprivateframe/row/table/nonaliasing, normalABI/nativecallee return andstablebase/noninterference required',
 '861EBA callarguments established, not effects under any stub or realexecution; copying callerbytes doesnotbyitself identifytheir authored source',
 'Callerarg5 allocation/extent/ownership, arg7blob origin/length domain, targetinternal78/88arrays andnaturalskeletonresetentry remainOPEN',
 'Oldno-writer census note preservedas historical; currentpositiveproducer explanation and independentOPUS/FABLE consumption pending',
 'EXP127 remainsINVALID_POST_TRACE; no semanticpromotion, retry/menu/game or wholeOV closure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED four original skeletonRef writes, callerworkspace binding and signed32copy-length carrier; no native/game')
