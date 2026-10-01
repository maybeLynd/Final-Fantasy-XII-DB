"""Original dispatch boolean versus forwarded accounting-index proof. No machine-code execution or gameplay."""


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
if lineage['parent_manifest_sha256']!='d4927fd135f97861ee64af294f75f898acf6c654da660d3b50d8324a16d8783c':raise RuntimeError('retained parent identity changed')
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

if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x3ab910','0x3ab93d'),('0x36c5d0','0x36c61f'),('0x36c620','0x36c659')]:raise RuntimeError('required dispatch/index source population changed')
ix={};graphs=[]
for r in x['ranges']+y['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 if a!=0x3ab910:
  g=G.graph(local,a,b)
  if set(local)!=g['visited']:raise RuntimeError('unaccounted original local source')
  graphs.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls']})
 else:
  # The reviewed local helper supports one external tail; this bounded body
  # has two. Check every original edge explicitly against the two verified
  # helper entries, without changing the shared tool or inventing execution.
  seen=set();todo=[a];edges={};tails={}
  while todo:
   pc=todo.pop()
   if pc in seen:continue
   if pc not in local:raise RuntimeError('unclosed dispatch body')
   seen.add(pc);i=local[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
   if m=='ret':succ=[]
   elif m=='jmp':
    dst=int(i['args'],16)
    if dst in [0x36c5d0,0x36c620]:tails[pc]=dst;succ=[]
    else:succ=[dst]
   elif m.startswith('j'):succ=[int(i['args'],16),n]
   else:succ=[n]
   edges[pc]=succ;todo.extend(succ)
  if seen!=set(local) or tails!={0x3ab932:0x36c5d0,0x3ab937:0x36c620}:raise RuntimeError('dispatch source/tails incomplete')
  graphs.append({'entry':hex(a),'instructions':len(local),'tails':{hex(k):hex(v) for k,v in tails.items()},'edges':{hex(k):[hex(q) for q in v] for k,v in edges.items()},'method':'Bounded original local CFG with two exact callee boundaries; no native execution'})
ops='''3ab910|test|rcx, rcx
3ab913|jne|0x3ab91a
3ab915|xor|r8d, r8d
3ab918|jmp|0x3ab927
3ab91a|test|cl, 3
3ab91d|mov|r8d, 0
3ab923|setne|r8b
3ab927|test|r8d, r8d
3ab92a|je|0x3ab937
3ab92c|cmp|r8d, 1
3ab930|jne|0x3ab93c
3ab932|jmp|0x36c5d0
3ab937|jmp|0x36c620
3ab93c|ret|
36c5d0|movsxd|r8, edx
36c5d3|test|ecx, ecx
36c5d7|test|cl, 3
36c5dc|cmp|ecx, 0x100000
36c5eb|and|rdx, rax
36c5f0|mov|rdx, qword ptr [rdx + 8]
36c5f9|movzx|eax, byte ptr [rdx + 0x17]
36c5fd|cmp|eax, r8d
36c602|mov|ecx, dword ptr [rdx + 0x18]
36c605|lea|r9, [rip + 0x1f6c804]
36c60c|sub|dword ptr [r9 + rax*4], ecx
36c610|add|dword ptr [r9 + r8*4], ecx
36c616|mov|byte ptr [rdx + 0x17], r8b
36c61a|mov|word ptr [rdx + 0x3e], ax
36c620|test|rcx, rcx
36c625|lea|r8, [rcx - 0x40]
36c62e|movzx|eax, byte ptr [r8 + 0x17]
36c633|cmp|eax, edx
36c637|mov|ecx, dword ptr [r8 + 0x18]
36c63b|lea|r9, [rip + 0x1f6c7ce]
36c642|sub|dword ptr [r9 + rax*4], ecx
36c646|movsxd|rax, edx
36c649|add|dword ptr [r9 + rax*4], ecx
36c64f|mov|byte ptr [r8 + 0x17], dl
36c653|mov|word ptr [r8 + 0x3e], ax
41f50e|mov|ecx, dword ptr [r14 + 0x2fc]
41f515|movsx|ebx, byte ptr [r14 + 0xc1]
41f51d|call|0x20e600
41f522|mov|rcx, rax
41f525|mov|edx, ebx
41f527|call|0x3ab910'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required dispatch/index operation changed '+hex(pc))
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for pc in sorted(q for q in ix if 0x3ab910<=q<0x3ab93d):
 ins=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=ins.regs_access()
 if {ins.reg_name(r) for r in wr}&{'rdx','edx','dx','dl','dh'}:raise RuntimeError('forwarded accounting argument changed')
ins=next(cs.disasm(bytes.fromhex(ix[0x36c5d0]['bytes']),0x36c5d0));_,wr=ins.regs_access()
if 'r8' not in {ins.reg_name(r) for r in wr}:raise RuntimeError('callee dispatch-temp replacement missing')
for pc,disp in [(0x36c605,0x1f6c804),(0x36c63b,0x1f6c7ce)]:
 i=ix[pc]
 if pc+len(bytes.fromhex(i['bytes']))+disp!=0x22d8e10 or i['memory'][0]['role']!='addr':raise RuntimeError('accounting base address/role mismatch')
for pc in [0x36c60c,0x36c610,0x36c642,0x36c649]:
 if ix[pc]['memory'][0]['role']!='rw' or ix[pc]['memory'][0]['size']!=4:raise RuntimeError('accounting read-modify-write classification failed')
base=0x22d8e10;examples=[]
for new in [-128,-1,0,1,2,127]:
 old=1;amount=32
 examples.append({'old_index_byte':old,'new_signed32':new,'debit_address':hex(base+old*4),'credit_address':hex(base+new*4),'new_record_index_byte':new&255,'amount':amount,'within_two_dword_addresses':new in [0,1]})
if examples[1]['credit_address']!='0x22d8e0c' or examples[4]['credit_address']!='0x22d8e18':raise RuntimeError('source counterexample calculation failed')
possible=[b if b<128 else b-256 for b in range(256)]
if len(possible)!=256 or len(set(possible))!=256 or sum(n in [0,1] for n in possible)!=2:raise RuntimeError('signed-byte representation calculation failed')
pre=json.loads((P/'consumer-preimage.json').read_text())
if sha(P/'consumer-preimage.txt')!=pre['excerpt_sha256'] or 'A boolean dispatch' not in (P/'consumer-preimage.txt').read_text():raise RuntimeError('consumer inference preimage changed')
result={'producer_complete':True,'method':'A STATIC_ONLY original tag-dispatch versus accounting argument dataflow',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':f,'sha256':sha(P/f)} for f in ['source-01.json','retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles],'instruction_assertions':len(ops.splitlines()),'graphs':graphs,
 'question':'Does3AB910 boolean dispatch restrict the forwarded accounting new index to0/1, as cited in the canonical range argument?',
 'dispatch':'RCX==0 orlow2bits0 producesR8D0 andtail36C620; otherwiseR8D1 andtail36C5D0. Thatboolean selectsrepresentation helper. EDX isnotchanged by3AB910.',
 'handle_index':'First36C5D0 instructionMOVSXDR8,EDX replacesdispatchboolean. Aftervalidhandle/recordguards, oldindex=zeroextendedBYTE17; comparewithR8D. Ifdifferent,debitDWORDbase+old*4,creditDWORDbase+signed32(new)*4; storelowBYTE(new)17 andclearWORD3E.',
 'raw_index':'36C620 replacesR8 withpayload-40h, comparesoldBYTE17 withEDX, andifdifferent MOVSXDRAX,EDX forcreditbase+signed32(new)*4. StoresDL17, clearsWORD3E. No newindex0/1 clamp/guard in either completebody.',
 'caller':'41F340 loadsbyteC1 viaMOVSXEBX thenEDX=EBX before3AB910. Representation provides possible -128..127, not0/1 bound. Actualinitialized/shipped domain ofC1 isnotprovedhere.',
 'implication':'Thecitedboolean dispatch isnot a boundonaccountingnewindex. A two-DWORD array/validcaller domain may haveindependentsupport, but thisreasoningdoesnotestablishit. Preserveprioraccepted result/history; OPUS/FABLE must audititsdependency andsupplyactualindex-domain/extent proof orqualifyclaim.',
 'mathematical_countermodels':examples,'signed_byte_representation':{'possible_values':256,'inside_0_or_1':2,'outside_0_or_1':254,'method':'Exhaustive representation calculation, notnativecalls orobservedcaller states'},
 'consumer_preimage':pre,
 'limits':['No originalnative/emulated/live execution; exactwrites are originalsource semantics undernormalvalidrecord/noninterference premises',
 'Non0/1 arguments andtheir calculatedaddresses are countermodels, notnaturalshippedreachability, observedcorruption orprovenlargerarrayextent',
 'Doesnotrefute a two-DWORDallocation provedbyindependentsource; refutes onlyboolean-dispatch implication forforwardedEDX',
 'OldindexreadBYTE17 doesnotestablishitsactualrange0/1 either; indexdomain/producers/allcallers/storageextent requireowneradjudication',
 'Factorycallersource retainedfrom1fccf591; no recapture/reexecutioncredit, no generalallocator/census redo',
 'Peerclaimedmemory/type pages untouched; independentreview andconsumeragreementpending; no menu/game/K14rerun orEXP127promotion']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED tag boolean does not bound forwarded accounting index; STATIC_ONLY source countermodels, no FF12 execution')

