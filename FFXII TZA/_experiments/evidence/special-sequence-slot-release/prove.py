"""Original cleanup branch/order proof, no native effects or gameplay samples."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')
if sha(P/'capture-index-path.py')!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497' or sha(P/'validate-title-source-annotations.py')!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' or sha(P/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('reviewed dependency identity changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture incomplete')
roles=V.validate(x);raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image identity changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked source')
if[(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x30c970','0x30ca50'),('0x306570','0x3065c7'),('0x31b7e0','0x31b80a')]:raise RuntimeError('required source population changed')
ix={}
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 ix.update({int(i['pc'],16):i for i in r['instructions']})
required=[(0x30c97a,'xor','edi, edi'),(0x30c983,'cmp','cl, 0x1f'),(0x30c988,'movsx','rax, cl'),(0x30c98c,'lea','rbx, [rax + rax*2]'),(0x30c990,'shl','rbx, 4'),(0x30c9f7,'call','0x325a00'),(0x30c9ff,'call','0x317ec0'),(0x30ca04,'cmp','dword ptr [rbx + 0x18], edi'),(0x30ca07,'je','0x30ca19'),(0x30ca09,'mov','ecx, dword ptr [rbx + 0x20]'),(0x30ca0c,'call','0x31b7e0'),(0x30ca11,'mov','rcx, rax'),(0x30ca14,'call','0x306570'),(0x30ca19,'and','dword ptr [rbx + 0x2c], 0xffffffe0'),(0x30ca22,'mov','word ptr [rbx + 0x1c], ax'),(0x30ca3b,'mov','qword ptr [rbx + 0x14], rdi'),(0x30ca3f,'mov','dword ptr [rbx + 0x10], edi'),(0x30ca42,'mov','dword ptr [rbx + 0x20], edi'),(0x30ca4f,'ret',''),
(0x31b7e4,'test','byte ptr [rip + 0x1d6db55], 0x10'),(0x31b7eb,'je','0x31b803'),(0x31b7ed,'call','0x3588b0'),(0x31b7f2,'test','rax, rax'),(0x31b7f5,'je','0x31b803'),(0x31b803,'xor','eax, eax'),(0x31b809,'ret',''),(0x31b7fe,'jmp','0x263e30'),
(0x306574,'test','rcx, rcx'),(0x306577,'je','0x30658a'),(0x306579,'mov','rax, qword ptr [rip + 0x1fbbbe8]'),(0x306580,'test','rax, rax'),(0x306583,'je','0x30658a'),(0x306585,'cmp','rcx, rax'),(0x306588,'jne','0x3065c2'),(0x30658a,'mov','ecx, 3'),(0x30658f,'call','0x2671f0'),(0x306594,'test','eax, eax'),(0x306596,'jne','0x3065c2'),(0x306598,'and','dword ptr [rip + 0x1fbbbb9], 0xfffffffc'),(0x30659f,'xor','eax, eax'),(0x3065a1,'mov','qword ptr [rip + 0x1fbbbb4], rax'),(0x3065a8,'mov','qword ptr [rip + 0x1fbbbb9], rax'),(0x3065af,'call','0x238a60'),(0x3065bd,'jmp','0x332190'),(0x3065c6,'ret','')]
for pc,m,a in required:
 if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('operation changed '+hex(pc))
graphs=[]
for a,b,tail in [(0x30c970,0x30ca50,None),(0x306570,0x3065c7,'0x332190'),(0x31b7e0,0x31b80a,'0x263e30')]:
 local={pc:i for pc,i in ix.items() if a<=pc<b};g=G.graph(local,a,b,tail=tail)
 if set(local)!=g['visited']:raise RuntimeError('incomplete/unreachable source accounting')
 graphs.append({'entry':hex(a),'visited':len(g['visited']),'returns':[hex(pc) for pc in g['returns']],'tails':[hex(pc) for pc in g['tails']],'calls':[{'pc':hex(pc),'target':t} for pc,t in g['calls']]})
# Caller call normal-return successor is exactly slotclear, with no success test.
assert 0x30ca14+len(bytes.fromhex(ix[0x30ca14]['bytes']))==0x30ca19
# Branch-partition labels only. No harness, stubs, isolated machine execution or live observation.
cases=[]
for arg in [0,0x1000,0x2000]:
 for owner in [0,0x1000]:
  for predicate in [0,1]:
   admitted=arg==0 or owner==0 or arg==owner;clear=admitted and predicate==0
   cases.append({'release_arg':arg,'global_owner':owner,'resource_predicate':predicate,'queries_resource':admitted,'local_global_clear_path':clear,'slot_reset_after_normal_return':True})
assert len(cases)==12 and any(c['release_arg']==0 and c['global_owner']==0x1000 and c['local_global_clear_path'] for c in cases)
resets=[{'pc':hex(pc),'base':m['base'],'offset':m['displacement'],'bytes':m['size'],'role':m['role']} for pc in [0x30ca22,0x30ca26,0x30ca29,0x30ca2d,0x30ca34,0x30ca3b,0x30ca3f,0x30ca42] for m in ix[pc]['memory']]
clears=[{'pc':hex(pc),'address':m['rip_target'],'bytes':m['size'],'role':m['role']} for pc in [0x306598,0x3065a1,0x3065a8] for m in ix[pc]['memory']]
assert clears[1]['address']=='0x22c215c' and clears[1]['bytes']==8
result={'producer_complete':True,'method':'A STATIC_ONLY original branch/caller-order proof','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],'annotation_prerequisites':[roles],'instruction_assertions':len(required),'graphs':graphs,'resolver_zero_path':'02089340bit4 clear or3588B0 NULL -> EAX0; no false-handle/native effects assumed','caller_transfer':'slot+18 !=0 ->31B7E0(slot+20) -> RCX=RAX unconditionally ->306570; no NULL/result check','global_release_admission':'argNULL OR globalownerNULL OR equal pointers; then predicate2671F0(3) must returnzero to execute localglobalclear','postreturn':'Caller always executes local slotreset after306570 normalreturn, including mismatchedowner/resourcepredicate-nonzero return; no local success channel','slot_resets':resets,'global_local_clears':clears,'branch_partition_countermodels':cases,'answer':'A failed owner resolution can be forwarded asNULL wildcard, conditional on valid slot+18/noninterference/normalcallee returns. A skipped globalclear is not a skipped slotreset. No naturalinvalidowner/reuse bug was observed; the cross-call ownership contract must state these conditional paths.','limitations':['No native/game/emulator/forced calls or actual resourcepredicate effects','Valid poolslot0..31, validlinks/privateframe, x64ABI and slot/global noninterference across normal external returns assumed','31B7E0 target263E30 and othercallees native effects not established by their call tags','Resourcepredicate nonzero prevents LOCAL clear; does not prove predicate/transitivecalls neverwrite sameglobals','Natural lostowner/alias/reuse/abort reachability and scheduling remainopen','QWORDclear022C215C covers kindDWORD and adjacentstateDWORD; observed write footprint is not atomicity/timing/parity guarantee']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED qualified NULL wildcard transfer and unconditional postreturn slotreset; no native/game')
