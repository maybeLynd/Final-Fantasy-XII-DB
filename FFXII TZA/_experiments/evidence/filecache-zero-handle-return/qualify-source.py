"""Actual source feasibility only; composed failure claim remains open."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=P/'source-feasibility-01.json'
if out.exists():raise RuntimeError('immutable feasibility exists')
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');sources=[];checks=[]
for n,d in [('01','capture.py'),('02','capture-cookie.py')]:
 s=json.loads((P/f'capture-{n}.status.json').read_text());x=json.loads((P/f'source-{n}.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/d) or x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/d) or x.get('exe_sha256')!=PIN:raise RuntimeError('failed/incomplete actual capture')
 sources.append(x);checks.append(V.validate(x))
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original identity changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked original range')
graphs=[];cookie=[]
for x in sources:
 for r in x['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16);blob=bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
  if blob!=read(a,b-a):raise RuntimeError('original byte mismatch')
  ix={int(i['pc'],16):i for i in r['instructions']}
  if a==0x808c40:
   cookie=list(ix.values());view={p:dict(i,mnemonic=i['mnemonic'].removeprefix('bnd ')) for p,i in ix.items()};g=G.graph(view,a,b,tail='0x809654')
  else:g=G.graph(ix,a,b,tail='0x85e730' if a==0x210ec0 else 'qword ptr [rip + 0x64409]' if a==0x85e730 else None)
  if g['visited']!=set(ix):raise RuntimeError('unaccounted local body')
  graphs.append({'entry':hex(a),'bytes':b-a,'calls':g['calls'],'returns':[hex(q) for q in g['returns']],'tails':[hex(q) for q in g['tails']]})
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for i in cookie:
 d=next(cs.disasm(bytes.fromhex(i['bytes']),int(i['pc'],16)));_,w=d.regs_access()
 if {d.reg_name(q) for q in w}&{'rax','eax','ax','al','ah'}:raise RuntimeError('cookie own return-value write needs investigation')
decl=sources[0]['import_declaration']
if decl['name']!='malloc' or decl['iat_va']!='0x8c2b40' or bytes.fromhex(decl['iat_file_bytes'])!=read(0x8c2b40,8):raise RuntimeError('allocation declaration mismatch')
result={'stage':'SOURCE_CFG_QUALIFIED_NOT_SEMANTIC_CLOSURE','producer_complete':False,'driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'graphs':graphs,'annotation_checks':checks,'malloc_static_declaration':decl,'cookie_observation':'Supplied complete33B has no own RAX-family writes, no calls, in-body successful return808C56 and failure tail809654. BND prefix removed only in temporary control-edge view; raw bytes/annotations preserved. External failure tail effects not proved.','next':'Build composed allocation-zero/own-count-phase/lookup-return propagation proof with exact retained source/status and controls; do not promote capture/CFG feasibility alone.','limits':'Original bytes read, not executed. Import declaration is not live binding. Successful cookie in-body RET is a distinct native precondition, not a generic Win64 volatile-RAX promise. No natural allocation failure/collision/leak/game session claim.'}
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('QUALIFIED 363 original bytes/four local bodies; composed semantic obligation remains open')
