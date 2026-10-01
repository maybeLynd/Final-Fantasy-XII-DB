"""Known original mode0 caller: fixed Attack, conditional resource/ABI exclusion."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=importlib.util.spec_from_file_location('roles',P/'validate-title-source-annotations.py');V=importlib.util.module_from_spec(s);s.loader.exec_module(V)
if sha(P/'capture-index-path.py')!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497' or sha(P/'validate-title-source-annotations.py')!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('capture incomplete')
mp=P/'retained/c40-manifest.json';pin='56100abc27fc97e1fdcd85e7488dc1f712365a4296c3ad819f2622800caed1dd'
if sha(mp)!=pin:raise RuntimeError('parent manifest changed')
listed={m['path']:m for m in json.loads(mp.read_text())['members']};lineage=json.loads((P/'lineage.json').read_text())
if len(lineage)!=3:raise RuntimeError('required retained population changed')
for row in lineage:
 m=listed[row['member']];q=P/row['copy']
 if q.stat().st_size!=m['bytes'] or sha(q)!=m['sha256'] or row['sha256']!=m['sha256']:raise RuntimeError('retained member changed')
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('reference image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked source')
files=['source-01.json','retained/current-row-source-01.json','retained/current-row-source-02.json'];ix={};annotations=[]
for f in files:
 y=json.loads((P/f).read_text());annotations.append(V.validate(y))
 if y.get('exe_sha256')!=PIN:raise RuntimeError('source provenance changed')
 for r in y['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
  for i in r['instructions']:
   pc=int(i['pc'],16)
   if pc in ix and ix[pc]!=i:raise RuntimeError('source overlap disagreement')
   ix[pc]=i
required=[(0x313078,'mov','rcx, rbx'),(0x31307b,'call','0x30eff0'),(0x313080,'test','eax, eax'),(0x313082,'je','0x31310e'),(0x313096,'mov','r8d, 0x96'),(0x31309c,'mov','dword ptr [rsp + 0x20], 0'),(0x3130d9,'mov','rcx, rbx'),(0x3130dc,'call','0x30f760'),(0x30f76a,'push','rsi'),(0x30f76b,'push','rdi'),(0x30f76c,'push','r12'),(0x30f76e,'push','r13'),(0x30f770,'push','r15'),(0x30f772,'sub','rsp, 0x20'),(0x30f776,'cmp','dword ptr [rsp + 0x70], 0'),(0x30f77e,'movzx','edi, r8w'),(0x30f788,'je','0x30f78f'),(0x30f78a,'call','0x3105d0'),(0x30f798,'mov','r13d, 0x21e'),(0x30f7a1,'cmp','di, r13w'),(0x30f7a5,'ja','0x30f7d9'),(0x30f806,'mov','word ptr [rbx + 0x714], di'),(0x30f814,'mov','byte ptr [rbx + 0x6b4], sil'),(0x30488d,'movzx','r13d, word ptr [rsi + 0x64]'),(0x304f3d,'test','dword ptr [r15 + 0xc], 0x40000000'),(0x304f45,'je','0x304f54'),(0x304f4d,'call','0x306760'),(0x304f54,'mov','rdx, r15'),(0x304f5a,'call','0x30fe10')]
for pc,m,a in required:
 if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('operation changed '+hex(pc))
# Straightline after suspend result is nonzero; no intervening calls or R8 writes.
walk=[];pc=0x313088
while pc<0x3130dc:
 i=ix[pc];walk.append(i)
 if i['mnemonic'].startswith('j') or i['mnemonic'] in ['call','ret']:raise RuntimeError('unexpected commit leg boundary')
 pc+=len(bytes.fromhex(i['bytes']))
if pc!=0x3130dc:raise RuntimeError('unclosed commit leg')
r8dest=[i['pc'] for i in walk if i['args'].split(',')[0] in ['r8','r8d','r8w','r8b']];assert r8dest==['0x313096']
stackdest=[i for i in walk if any(m['base']=='rsp' and m['displacement']==32 and m['role'] in ['w','rw'] for m in i['memory'])];assert len(stackdest)==1 and stackdest[0]['pc']=='0x31309c'
# Windowsx64 fiftharg relation: callerRSP+20 -> entryRSP+28; prologue moves RSP by48hex.
abi={'push_bytes':5*8,'sub_bytes':32,'callee_prologue_delta':72,'caller_arg5_offset':32,'call_return_address_bytes':8,'callee_postprologue_arg5_offset':112}
assert abi['caller_arg5_offset']+abi['call_return_address_bytes']+abi['callee_prologue_delta']==abi['callee_postprologue_arg5_offset']
tb=(P/'retained/action_data_us.st2e').read_bytes();count,stride,off=struct.unpack_from('<III',tb,4);assert(count,stride)==(543,60) and off+count*stride<=len(tb)
flags=struct.unpack_from('<I',tb,off+150*stride+12)[0];assert flags&(1<<30)==0
result={'producer_complete':True,'method':'A STATIC_ONLY original directcaller/ABI/carrier andretainedUSrow bound','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':f,'sha256':sha(P/f)} for f in files],'annotation_prerequisites':annotations,'parent_manifest':pin,'instruction_assertions':len(required),'straightline_instructions':len(walk),'ABI':abi,'known_mode0_caller':{'site':'0x3130dc','action':150,'arg5':0,'required_preceding_call':'0x30eff0','required_nonzero_suspend_result':True,'scope':'One located directcaller leg, not all native callers'},'callee_carrier':'MOVZX EDI,R8W before modegate/callees; WindowsnonvolatileRDI, original150<=542 normalallowedpath writesDI currentunit714 andphase0','retained_table':{'path':'retained/action_data_us.st2e','sha256':sha(P/'retained/action_data_us.st2e'),'row':150,'flags':hex(flags),'bit30':False,'runtime_binding_observed':False},'excluded_path':'With currentactionstill150 and actionregistryboundto retainedUSrowbytes, 304F45 jumpsordinary304F54 ->30FE10, skipping306760. Thisactualdirectmode0caller cannot itself commit arbitraryrow275/Dismiss. Otherchanges/restore/registrybinding remainopen.','correction':'Earlier working delivery wording suggesting all known commit callers passmode1 is false:31309C passes0 after30EFF0. Publishedc40/8b localcarrier/cleanup proofs didnot dependon that wording; preserve originals and addcorrected consumer/handoff notes.','limitations':['No native/harness/game execution','Ordinary Windowsx64ABI/privateframe/normalcalls/noninterference, validinitializedsameunit andstableaction/registry premised','30EFF0 native effects/lifetime/fullrestore are not proven by calltag orstub','Only exactretainedUS table binding; no captured live table pointer','Other direct/indirect callers and forcedmode0 mayhave differentdomains','No universalrowidentity/globalstatstype/parity/wholeOVclosure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED knownmode0 fixedAttack andconditional specialpath exclusion; correctedallmode1 assumption, no native/game')
