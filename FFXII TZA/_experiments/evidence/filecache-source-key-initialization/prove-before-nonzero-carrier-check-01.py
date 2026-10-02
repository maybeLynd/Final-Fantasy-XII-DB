"""Exact key-field initialization/local retention, STATIC_ONLY."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable result exists')
if (P/'inspect.py').exists():raise RuntimeError('stdlib shadow refused')
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('exe_sha256')!=PIN:raise RuntimeError('actual capture incomplete')
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');annotations=V.validate(x)
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('wrong original image')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked original span')
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x597930','0x59796b'),('0x597970','0x597a12'),('0x59ed70','0x59ee0c')]:raise RuntimeError('source population changed')
ix={};gb={};graphs=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local);g=G.graph(local,a,b)
 if g['visited']!=set(local):raise RuntimeError('unaccounted local CFG')
 gb[a]=g;graphs.append({'entry':hex(a),'bytes':b-a,'instructions':len(local),'calls':g['calls'],'returns':[hex(q) for q in g['returns']]})
def need(pc,m,a):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('key initializer/carrier changed '+hex(pc))
for line in '''597936|xor|eax, eax
597951|mov|dword ptr [rcx + 0x28], eax
59795d|call|0x59ee90
597984|xor|ebp, ebp
5979a3|mov|dword ptr [rcx + 0x48], ebp
5979b2|add|rcx, 0x20
5979b6|call|0x59ee90
59ed8a|mov|rdi, rcx
59ed90|add|rcx, 0x20
59ed97|call|0x59ee90'''.splitlines():
 pc,m,a=line.split('|');need(int(pc,16),m,a)
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def unchanged(lo,hi,regs):
 for pc in sorted(q for q in ix if lo<=q<hi):
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
  if {i.reg_name(q) for q in wr}&set(regs):raise RuntimeError('zero/receiver carrier changed '+hex(pc))
unchanged(0x597938,0x597951,['rax','eax','ax','al','ah']);unchanged(0x597951,0x59795d,['rcx','ecx','cx','cl','ch'])
unchanged(0x597986,0x5979a3,['rbp','ebp','bp','bpl']);unchanged(0x597970,0x5979b2,['rcx','ecx','cx','cl','ch']);unchanged(0x5979b6,0x5979b6,['rcx'])
unchanged(0x59ed70,0x59ed90,['rcx','ecx','cx','cl','ch']);unchanged(0x59ed94,0x59ed97,['rcx','ecx','cx','cl','ch'])
for entry,a,b in [(0x597930,0x597936,0x597951),(0x597930,0x597951,0x59795d),(0x597970,0x597984,0x5979a3),(0x597970,0x5979a3,0x5979b6),(0x597970,0x5979b2,0x5979b6),(0x59ed70,0x59ed90,0x59ed97)]:
 if not G.dominates(gb[entry],a,b):raise RuntimeError('initialization/receiver dominance changed')
spans=[]
for pc in sorted(gb[0x59ed70]['visited']):
 for m in ix[pc]['memory']:
  if m['role'] not in ['w','rw']:continue
  if m['base']=='rsp':continue
  if m['base']!='rdi' or m['index'] not in ['',None]:raise RuntimeError('unmodelled rebind direct-write alias')
  span={'pc':hex(pc),'start':m['displacement'],'end':m['displacement']+m['size'],'role':m['role']};spans.append(span)
  if span['start']<0x4c and 0x48<span['end']:raise RuntimeError('rebind writes cache key directly')
if len(spans)!=5:raise RuntimeError('zero/incomplete rebind write census')
for entry,store,call,target in [(0x597930,0x597951,0x59795d,0x28),(0x597970,0x5979a3,0x5979b6,0x48)]:
 for pc in sorted(gb[entry]['visited']):
  if not store<pc<call:continue
  for m in ix[pc]['memory']:
   if m['role'] in ['w','rw'] and m['base']=='rcx' and m['displacement']<target+4 and target<m['displacement']+m['size']:raise RuntimeError('constructor key overwritten before resolver')
result={'producer_complete':True,'method':'A STATIC_ONLY original initializer/rebind local rules','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],'annotation_prerequisite':annotations,'graphs':graphs,'rebind_direct_object_writes':spans,
 'established':['597930 zeroes standalone source-record DWORD28 before every local59EE90 call.','597970 zeroes full reader object DWORD48 before every local59EE90 call and passes receiver+20, so this is source-record28.','59ED70 passes receiver+20 into59EE90 before its path-copy/update work, with no own direct write overlapping reader48..4C anywhere in its complete body. It therefore does not locally reset the prior cache-key field before re-resolving.','Compose only under valid disjoint state and no opaque interference: the prior field of an empty-normalized first constructor resolve is zero; a rebind may retain the earlier field. This narrows the prior arbitrary-field boundary for these demonstrated producers, not every caller or state.'],
 'limits':['No shipping instructions, native harness or game execution; initialized-state rule is static, not a live initialization capture.','Valid record/frame/distinct fields, normal ABI/returns and no opaque/concurrent key interference. Rebind callees receive object/source pointers; their native effects and all-writer closure remain unproved.','Key zero only at the demonstrated constructor boundary; no allocator freshness/portable snapshot-default/universal lifetime guarantee.','A natural empty-name archive hit, actual key values and collision/eviction/reuse scheduling are unproved. Existing accepted RTTI/base identity and caller census not redone.','This supplement does not independently accept the prior99-member backfill package or close wholeOV33.'],
 'affected_claims':['FABLE cache-backfill retained-field initial-state qualification','OPUS source-record28/reader48 zero initialization versus rebind contracts'],'cleanup':'Only bounded own offline children; no PC/game/instrument/save/config/reference/peer writes.'}
out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS exact constructor-zero and rebind-local retention rules; no FF12 execution')
