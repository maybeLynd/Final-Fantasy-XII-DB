"""Original skeleton workspace factory/size/failure proof. No machine-code execution or gameplay."""


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
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x41f340','0x41f72e'),('0x46e4d0','0x46e582'),('0x3712e0','0x371325'),('0x3ab8b0','0x3ab907')]:raise RuntimeError('required factory source population changed')
ix={};graphs=[];graph_by_entry={}
for r in x['ranges']+y['ranges']+z['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b)
 if set(local)!=g['visited']:raise RuntimeError('unaccounted original source')
 graph_by_entry[a]=g
 graphs.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls']})
ops='''3712e0|push|rbx
3712e2|sub|rsp, 0x20
3712e9|call|0x409f50
3712f1|mov|edx, 0x52544640
3712f9|call|0x409660
3712fe|imul|ecx, dword ptr [rax + 0xc], 0x149
371305|movzx|eax, word ptr [rax + 0x38]
371309|add|ecx, eax
37130b|lea|eax, [rcx*2 + 0xf]
371312|cdq|
371313|and|edx, 0xf
371316|add|eax, edx
371318|and|eax, 0xfffffff0
37131b|add|eax, dword ptr [rsp + 0x50]
372921|imul|eax, dword ptr [rbp + 0xc], 0x149
372928|movzx|ecx, word ptr [rbp + 0x38]
37292c|add|ecx, eax
37292e|lea|eax, [rcx*2 + 0xf]
37293a|cdq|
37293b|and|edx, 0xf
37293e|lea|ebx, [rdx + rax]
372941|and|ebx, 0xfffffff0
41f354|push|rdi
41f355|push|r12
41f357|push|r13
41f359|push|r14
41f35b|push|r15
41f35d|sub|rsp, 0x50
41f361|mov|r14, rcx
41f423|mov|ecx, dword ptr [rsp + 0xa8]
41f438|mov|dword ptr [rsp + 0x20], ecx
41f443|call|0x3712e0
41f44b|mov|ebp, eax
41f44d|call|0x3e6d10
41f452|imul|ecx, ebx, 0x108
41f458|add|eax, 0xf
41f45b|cdq|
41f45c|and|edx, 0xf
41f45f|add|ecx, 0x3a0
41f465|lea|r13d, [rdx + rax]
41f469|and|r13d, 0xfffffff0
41f470|lea|ebx, [rcx + 8]
41f473|cmove|ebx, ecx
41f497|mov|ecx, ebx
41f49c|je|0x41f4ce
41f4a2|je|0x41f4ce
41f4ab|lea|ecx, [rbx + rbx]
41f4ce|lea|ebx, [rcx + r13]
41f4d2|mov|edx, 1
41f4d7|add|ebx, ebp
41f4d9|mov|ecx, ebx
41f4db|call|0x3ab8b0
41f4e0|mov|rcx, rax
41f4e3|call|0x20e620
41f4ea|mov|dword ptr [r14 + 0x2fc], eax
41f4f1|movsxd|rbx, ebx
41f4f4|call|0x20e600
41f4fc|call|0x3ab7f0
41f504|mov|r8, rbx
41f507|xor|edx, edx
41f509|call|0x861ec0
41f52c|mov|ecx, dword ptr [r14 + 0x2fc]
41f533|call|0x20e600
41f53c|mov|rbx, rax
41f544|mov|ecx, dword ptr [rsp + 0xa8]
41f54e|mov|dword ptr [rsp + 0x38], ecx
41f556|mov|rcx, qword ptr [rsp + 0xa0]
41f565|mov|qword ptr [rsp + 0x30], rcx
41f56d|mov|dword ptr [rsp + 0x28], 0
41f575|mov|qword ptr [rsp + 0x20], rbx
41f57a|call|0x46e4d0
41f57f|cmp|eax, -1
41f582|jne|0x41f588
41f584|xor|esi, esi
41f586|jmp|0x41f595
41f595|mov|ecx, dword ptr [rsi + 4]
46e4da|push|rdi
46e4db|push|r14
46e4dd|push|r15
46e4df|sub|rsp, 0x40
46e4f0|call|0x51fbb0
46e4f5|mov|edi, eax
46e4f7|cmp|eax, -1
46e4fa|jne|0x46e500
46e4fc|or|eax, eax
46e4fe|jmp|0x46e56e
46e51a|mov|ecx, dword ptr [rsp + 0x98]
46e524|mov|dword ptr [rsp + 0x38], ecx
46e52c|mov|rcx, qword ptr [rsp + 0x90]
46e537|mov|qword ptr [rsp + 0x30], rcx
46e53c|mov|ecx, dword ptr [rsp + 0x88]
46e543|mov|dword ptr [rsp + 0x28], ecx
46e547|mov|rcx, qword ptr [rsp + 0x80]
46e54f|mov|qword ptr [rsp + 0x20], rcx
46e557|call|0x372820
46e56c|mov|eax, edi
3ab8bf|mov|ebx, edx
3ab8c1|mov|esi, ecx
3ab8d1|test|ebx, ebx
3ab8d3|je|0x3ab8e5
3ab8d5|cmp|ebx, 1
3ab8d8|jne|0x3ab8ef
3ab8da|mov|ecx, esi
3ab8dc|call|0x36b160
3ab8e1|mov|edi, eax
3ab8e3|jmp|0x3ab8ef
3ab8f9|mov|rax, rdi
20e600|mov|eax, ecx
20e602|add|rax, qword ptr [rip + 0x1d74f27]
20e620|sub|ecx, dword ptr [rip + 0x1d74f0a]
20e626|mov|eax, ecx'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required operation changed '+hex(pc))

# These are instruction/control-flow proofs over the captured shipping bytes,
# not executions. Full local graphs and exact operands are checked above.
for entry,a,b in [(0x41f340,0x41f443,0x41f4db),(0x41f340,0x41f4db,0x41f57a),(0x41f340,0x41f54e,0x41f57a),(0x46e4d0,0x46e4f0,0x46e557)]:
 if not G.dominates(graph_by_entry[entry],a,b):raise RuntimeError('required caller dominance changed')
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for regs,lo,hi in [({'rbp','ebp','bp','bpl'},0x41f44d,0x41f4db),({'r13','r13d','r13w','r13b'},0x41f46d,0x41f4db),({'rbx','ebx','bx','bl'},0x41f4e0,0x41f4f1),({'rbx','ebx','bx','bl'},0x41f53f,0x41f57a),({'rdi','edi','di','dil'},0x46e4f7,0x46e56c)]:
 for pc in sorted(q for q in ix if lo<=q<hi):
  ins=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=ins.regs_access()
  if {ins.reg_name(r) for r in wr}&regs:raise RuntimeError('nonvolatile carrier changed '+hex(pc))

wrapper_failure=[0x46e4f5,0x46e4f7,0x46e4fa,0x46e4fc,0x46e4fe,0x46e56e,0x46e573,0x46e578,0x46e57c,0x46e57e,0x46e580,0x46e581]
for pc in wrapper_failure:
 if pc in [0x46e4f5,0x46e4f7,0x46e4fa,0x46e4fc,0x46e4fe]:continue
 ins=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=ins.regs_access()
 if ix[pc]['mnemonic']=='call' or {ins.reg_name(r) for r in wr}&{'rax','eax','ax','al','ah'}:raise RuntimeError('failure result not preserved')
if ix[0x46e581]['mnemonic']!='ret':raise RuntimeError('failure exit changed')
caller_failure=[0x41f57f,0x41f582,0x41f584,0x41f586,0x41f595]
if ix[0x41f595]['memory'][0]['role']!='r' or ix[0x41f595]['memory'][0]['size']!=4:raise RuntimeError('failure read role changed')
if any(ix[pc]['mnemonic']=='call' for pc in caller_failure):raise RuntimeError('intervening failure call')

U=1<<32;MASK=U-1;MASK64=(1<<64)-1
def offset(h,w):
 # Every arithmetic stage is low32. CDQ consumes the sign of the actual LEA
 # result, before the correction/mask; this is not real-number algebra.
 t=((h*0x149+w)*2+15)&MASK
 correction=15 if t&(1<<31) else 0
 return ((t+correction)&MASK)&0xfffffff0
examples=[]
for h,w,length in [(0,0,0),(1,0,32),(0,65535,16),(0x7fffffff,65535,0),(0xffffffff,0,0x80000000)]:
 o=offset(h,w);e=(o+length)&MASK
 examples.append({'headerC':hex(h),'header38':hex(w),'length32':hex(length),'offset32':hex(o),'component32':hex(e)})
# Generic fit theorem: under stable equal header O, nonnegative L,S,Q and
# no32bit wrap, E=O+L and N=E+S+Q. Hence O<=O+L=E<=N. This is arithmetic
# on the explicitly constrained domain, NOT an allocator-size observation.
null_counter=[]
for base in [0,0x1000,0x1234567800001000]:
 encoded=(-base)&MASK;decoded=(base+encoded)&MASK64
 null_counter.append({'base':hex(base),'encoded_input0':hex(encoded),'decoded_encoded0':hex(decoded)})
if null_counter[1]['decoded_encoded0']!='0x100000000':raise RuntimeError('codec counterexample failed')
result={'producer_complete':True,'method':'A STATIC_ONLY original workspace factory/caller/size/failure source proof',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','retained/source-01.json','retained/retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles,codec_roles],'instruction_assertions':len(ops.splitlines()),'graphs':graphs,
 'abi':{'factory_frame_bytes':120,'factory_arg5_entry28_currentA0':'optional source blob','factory_arg6_entry30_currentA8':'DWORD length',
 'wrapper_frame_bytes':88,'wrapper_arg5_entry28_current80':'workspace representation','wrapper_arg6_entry30_current88':'DWORD value; factory supplies0',
 'wrapper_arg7_entry38_current90':'optional source blob','wrapper_arg8_entry40_current98':'DWORD length',
 'size_helper_frame_bytes':40,'helper_arg5_entry28_current50':'DWORD length'},
 'offset_correspondence':'3712E0 and372820 compute identical low32 O=((t+(15 if signbit(t) else0)) mod2^32)&FFFFFFF0, t=(2*(149h*DWORD_C+zeroextendedWORD_38)+15) mod2^32. ADDoperand ordering differs but ring addition commutes. Same unchanged header is a premise; opaque query calls do not prove it.',
 'requested_size':'3712E0 returns low32(O+L) savedEBP. Factory computes additional R13 side component S and one/two model-side component Q, then requestN=low32(E+S+Q) inECX at3AB8B0 flagEDX1. Flag1 calls36B160(ECX32), zeroextendsEAX intoRDI; no allocation result checked before encoding/storing2FC, zero fill, and binder call.',
 'conditional_extent':'For same unchanged header, O,L,S,Q nonnegative and each required arithmetic without wrap, E=O+L andN=E+S+Q, so [O,O+L) fits the first E component and requestedN. Actual allocator success/usable extent/reference roundtrip/native writes/lifetime remain independent premises.',
 'size_width_boundary':'Allocation adapter takes zeroextendedECX32 request. Factory zero-fill R8 is MOVSXD of total32; binder copyR8 is MOVSXD of length32. Highbit total/length becomes a huge unsigned64 call argument; no universal malformed-size safety or authored-domain acceptance.',
 'workspace_binding':'Allocation-adapter result ->Encode at41F4E3 ->instanceDWORD2FC. Decode stored2FC at41F533 ->RBX ->arg5 at41F575; wrapper forwards samearg5 to372820. Resolver/copy/native initialization effects and opaque aliasing are not executed or assumed.',
 'failure':{'premise':'51FBB0 returns EAX=FFFFFFFF; normal ABI and earlier calls complete',
 'wrapper_path':[hex(q) for q in wrapper_failure],'wrapper_result':'FFFFFFFF preserved; binder372820 skipped',
 'caller_path':[hex(q) for q in caller_failure],'result':'41F584 XOR ESI,ESI zeroextendsRSI=0;41F586 jumps41F595 DWORDread[RSI+4], address4, no intervening call. Natural bank failure and actual OS fault not established.'},
 'codec_qualification':'Encode(0)=low32(-B_low); Decode(Encode(0))=low64(B+low32(-B_low)). EncodedNULL label in parent denotes encoded input zero, not universal decodedNULL. Base0 retained ruling/samples not rerun; no EXP127 promotion.',
 'mathematical_controls':examples,'codec_mathematical_counterexamples':null_counter,
 'limits':['No game/native/isolated-machine-code execution or instrumented process; examples and fit theorem are source calculations',
 'Conditional field/header/resource stability, valid private ABI frames/objects and no aliasing/interference; caller queries not proved identical over time',
 'Native36B160/861EC0/861EBA/3AB910 effects, failure cleanup, actual allocator usable bytes, lifetime/reuse and internal78/88 target arrays remainOPEN',
 'No complete direct/indirect allcaller/allwriter proof; located cached caller chain is preparation evidence only',
 'Address4 consequence is conditional original effective-address proof; not natural reachability, observed crash or instruction fault execution',
 'Parent frozen evidence remains producer-valid pending publication/independent acceptance; additive qualification doesnot rewrite immutable inputs',
 'No wholeOV closure, new runtime count, menu attempt, K14 rerun or EXP127 semantic promotion']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED original workspace size/forwarding and conditional slot-failure address4 read; STATIC_ONLY, no game/native')

