"""Original positive CharacterRenderRecord C1 upper-nibble store proof. No machine-code execution or gameplay."""


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

if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x2e28e0','0x2e30ca'),('0x2e3110','0x2e34f5')]:raise RuntimeError('required C1 source population changed')
ix={};graphs={};summaries=[];writes=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b)
 if set(local)!=g['visited']:raise RuntimeError('incomplete C1 source graph')
 graphs[a]=g;summaries.append({'entry':hex(a),'instructions':len(local),'returns':[hex(q) for q in g['returns']],'calls':g['calls']})
 for pc,i in local.items():
  for m in i['memory']:
   if m['displacement']==0xc1 and m['role'] in ['w','rw']:writes.append(pc)
if sorted(writes)!=[0x2e29e9,0x2e33b3]:raise RuntimeError('required positive stores missing/extra within supplied bodies')
ops='''2e28f1|mov|rdi, rcx
2e2906|mov|rsi, qword ptr [rcx + 0xc0]
2e29a4|movzx|edx, byte ptr [rsi + 0x10]
2e29af|mov|rax, qword ptr [rdi + 0xc0]
2e29b6|shr|edx, 4
2e29b9|test|rax, rax
2e29bc|je|0x2e29ef
2e29be|cmp|dword ptr [rax], -1
2e29c1|je|0x2e29ef
2e29c3|movzx|ecx, word ptr [rax]
2e29c6|cmp|cx, -1
2e29ca|je|0x2e29ef
2e29cc|movsx|rax, cx
2e29d0|imul|rcx, rax, 0x740
2e29d7|add|rcx, qword ptr [rip + 0x1fe454a]
2e29de|je|0x2e29ef
2e29e0|cmp|dword ptr [rcx + 0x284], r12d
2e29e7|je|0x2e29ef
2e29e9|mov|byte ptr [rcx + 0xc1], dl
2e312a|mov|rsi, qword ptr [rcx + 0xc0]
2e3134|mov|rdi, rcx
2e3367|movzx|edx, byte ptr [rbx + 0x10]
2e3379|mov|rax, qword ptr [rdi + 0xc0]
2e3380|shr|edx, 4
2e3383|test|rax, rax
2e3386|je|0x2e33b9
2e3388|cmp|dword ptr [rax], -1
2e338b|je|0x2e33b9
2e338d|movzx|eax, word ptr [rax]
2e3390|cmp|ax, -1
2e3394|je|0x2e33b9
2e3396|movsx|rax, ax
2e339a|imul|rcx, rax, 0x740
2e33a1|add|rcx, qword ptr [rip + 0x1fe3b80]
2e33a8|je|0x2e33b9
2e33aa|cmp|dword ptr [rcx + 0x284], r12d
2e33b1|je|0x2e33b9
2e33b3|mov|byte ptr [rcx + 0xc1], dl'''
for line in ops.splitlines():
 pc,m,args=line.split('|');pc=int(pc,16)
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required C1 operation changed '+hex(pc))
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
flow=[]
for entry,load,shift,store,table in [(0x2e28e0,0x2e29a4,0x2e29b6,0x2e29e9,0x2e29d7),(0x2e3110,0x2e3367,0x2e3380,0x2e33b3,0x2e33a1)]:
 for q in [load,shift]:
  if not G.dominates(graphs[entry],q,store):raise RuntimeError('C1 value source does not dominate store')
 for pc in sorted(q for q in ix if load<q<store and q!=shift):
  ins=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=ins.regs_access()
  if ins.mnemonic=='call' or {ins.reg_name(r) for r in wr}&{'rdx','edx','dx','dl','dh'}:raise RuntimeError('source-to-store EDX carrier changed')
 for pc,role,size in [(load,'r',1),(store,'w',1)]:
  if len(ix[pc]['memory'])!=1 or ix[pc]['memory'][0]['role']!=role or ix[pc]['memory'][0]['size']!=size:raise RuntimeError('positive source/store width or role changed')
 i=ix[table];mem=i['memory'][0]
 if pc==table:raise RuntimeError('unexpected loop residue')
 if mem['base']!='rip' or table+len(bytes.fromhex(i['bytes']))+mem['displacement']!=0x22c6f28:raise RuntimeError('CharacterRenderRecord table identity changed')
 flow.append({'entry':hex(entry),'load':hex(load),'shift':hex(shift),'store':hex(store),'table_global':'0x22c6f28','record_stride':'0x740'})
# Bounded invariant over every possible source-byte representation, rather
# than collecting samples. All values are calculations, not actual records.
groups={k:[] for k in range(16)}
for b in range(256):
 n=b>>4
 if not 0<=n<=15 or ((n in [0,1])!=(b&0xe0==0)):raise RuntimeError('upper-nibble domain theorem failed')
 groups[n].append(b)
if any(len(v)!=16 for v in groups.values()):raise RuntimeError('incomplete representation calculation')
examples=[{'source_byte':hex(b),'C1':b>>4,'factory_MOVSX_byte':b>>4,'two_value_condition':b&0xe0==0} for b in [0,15,16,31,32,127,128,255]]
result={'producer_complete':True,'method':'A STATIC_ONLY original positive C1 stores and upper-nibble invariant',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],
 'annotation_prerequisites':[roles],'instruction_assertions':len(ops.splitlines()),'graphs':summaries,'positive_store_flow':flow,
 'result':'Both supplied positiveC1 stores takezeroextendedsourceBYTE+10, logicalSHREDX4, thenstoreDL intoCharacterRenderRecordC1. Conditionalstorevalue=sourcebyte>>4 in0..15. No opaque call/EDXwrite occursbetweenread/shift/store; bothload/shift dominate respectivewrite.',
 'identity':'Guarded record derivesfromwordindex inobjectC0 state, signextends16 andusesglobal022C6F28/stride740; target284 nonzero guard. Thisdoesnotprovenonnegative/inrange index orproperobjectinitialization.',
 'source_scope':'2E28E0 loads source fromRSI assignedentryobjectC0;2E3110 source isRBX selectedslot, notnecessarilyrootstate. No universalargumentDL provenance orallselectedslot initialization proof.',
 'domain':'Undertheseconditionalwrites, laterfactorysigned-byte read cannotbenegative. Values2..15 remainpossibleinrepresentation; 0/1 iff sourcebyte& E0h==0, equivalentlysourcebyte<=1Fh. Actualsource-byte domain/shippeddomain needseparateproof.',
 'affected_claims':['CharacterRenderRecordparamByteC1 hasprovedproducer arithmetic anddownstreamaccountinguse beyond neutralcopy census; ownerqualifiedmeaning/range updatepending',
 'Accounting-dispatch-index arbitrarynegative countermodels remainmathematical butareexcludedbythese suppliedwriter outputs; no completeallwriter/alias closure',
 'Two-DWORDaccountingextent stillnotprovedbytagdispatch or upper-nibblebound; needactualsourcebit5..7 exclusion/allcaller+storageevidence'],
 'representation_calculation':{'inputs':256,'outputs':16,'inputs_per_output':16,'method':'Exhaustivebyte representation calculations, notnativecalls/live observations'},'mathematical_boundaries':examples,
 'limits':['Originalsource only; no native/harness/live game execution or naturalbadstate observation',
 'Two positivewrites within complete suppliedbodies, notallpossiblewriters/bulkcopy/alias/constructor orlifetime invariant',
 'Normalvalidobject/frame/table/header execution andnointerference required; originalsigned16indexguards arenotuniversalboundschecks',
 'No sourceinputbit5..7 naturalzero proof, actualaccountingstorageextent or arraygeometry adjudication; consumers independentlypending',
 'No nativecallee side effects/reachability/resource lifecycle certification; EXP127invalid, menuspent/unapproved K14closed']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED two positive C1 stores yield upper nibble0..15; STATIC_ONLY, no native/game')

