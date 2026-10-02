"""Additive, executable returned-review contracts from retained shipping bytes.

Pure derive() is the actual invocation's semantic path and focused-control target.
Parents retain their original results; this does not replay their sample campaigns.
"""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 def need(pc,m,a):
  if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required reviewed phase operation changed '+hex(pc))
 def mem(pc,base,offset,size,role,index=None):
  rows=ix[pc]['memory']
  if len(rows)!=1 or (rows[0]['base'],rows[0]['displacement'],rows[0]['size'],rows[0]['role'],rows[0]['index'] or None)!=(base,offset,size,role,index):raise RuntimeError('reviewed phase width/role changed '+hex(pc))
 def order(g,a,b):
  if not G.dominates(g,a,b):raise RuntimeError('reviewed phase order changed '+hex(a)+'->'+hex(b))
 ops='''427a18|cmp|dword ptr [rbx + 0x48810], -1
427a1f|jne|0x427a29
427a21|mov|dword ptr [rbx + 0x48810], esi
427a29|movsxd|rax, dword ptr [rbx + 0x48814]
427a30|imul|rcx, rax, 0x740
427a37|mov|word ptr [rcx + rbx + 4], si
427a3c|movzx|eax, word ptr [rbx + 0x48814]
427a43|mov|word ptr [rdi + 2], ax
427a47|mov|dword ptr [rbx + 0x48814], esi
427a4d|mov|word ptr [rdi], si
427a71|call|0x420480
427a7f|inc|dword ptr [rbx + 0x4880c]
42919f|call|0x422d50
4291a4|test|rax, rax
4291a7|je|0x4291ad
4291a9|and|dword ptr [rax + 0xc], 0xfffffffd
4291d3|call|0x2ed570
4291d8|mov|rbx, rax
4291db|test|rax, rax
4291de|je|0x429296
4291e4|and|dword ptr [rax], 0xfffffffb
4291e9|call|0x20e620
4291ee|mov|rdi, qword ptr [rsp + 0x30]
4291f3|mov|dword ptr [rbx + 0xa0], eax
427d18|dec|dword ptr [rdi + 0x4880c]
42924d|dec|dword ptr [rdx + 0x4880c]
427dae|call|0x4200a0
427db3|or|dword ptr [rdi + 0x48818], 0x20
427dba|cmp|esi, -1
427dbd|jne|0x427cc0'''
 for line in ops.splitlines():
  pc,m,a=line.split('|');need(int(pc,16),m,a)
 for q in [(0x427a21,'rbx',0x48810,4,'w'),(0x427a43,'rdi',2,2,'w'),(0x427a47,'rbx',0x48814,4,'w'),(0x427a4d,'rdi',0,2,'w'),(0x4291a9,'rax',12,4,'rw'),(0x4291e4,'rax',0,4,'rw'),(0x4291f3,'rbx',0xa0,4,'w'),(0x427db3,'rdi',0x48818,4,'rw'),(0x427d18,'rdi',0x4880c,4,'rw'),(0x42924d,'rdx',0x4880c,4,'rw')]:mem(*q)
 mem(0x427a37,'rcx',4,2,'w','rbx')
 alloc=G.graph(ix,0x4279b0,0x427af9)
 slot=[]
 for nonempty,sites in [(False,[0x427a21]),(True,[0x427a37,0x427a43])]:
  g=G.graph(ix,0x4279b0,0x427af9,fixed={0x427a1f:nonempty})
  for pc in sites:order(g,pc,0x427a47)
  wrong={0x427a21,0x427a37,0x427a43}-set(sites)
  if wrong&g['visited']:raise RuntimeError('pending list partition changed')
  slot.append({'pending_list_nonempty':nonempty,'before_tail_sites':[hex(v) for v in sites]})
 order(alloc,0x427a47,0x427a4d);order(alloc,0x427a4d,0x427a71);order(alloc,0x427a71,0x427a7f)
 # Derive scalar width from actual memory operations, not an English byte label.
 scalar=[]
 for pc in sorted(q for q in ix if 0x6c0520<=q<0x6c053a):
  for m in ix[pc]['memory']:
   if m['role'] in ['w','rw']:
    if ix[pc]['mnemonic']!='movss' or (m['base'],m['index'] or None,m['size'],m['role'])!=('rcx',None,4,'w'):raise RuntimeError('scalar store width/class changed')
    scalar.append({'pc':hex(pc),'offset':m['displacement'],'store_bytes':m['size']})
 if len(scalar)!=4 or sorted(r['offset'] for r in scalar)!=[0,4,8,12]:raise RuntimeError('scalar store population changed')
 marked=G.graph(ix,0x429140,0x4292a6,fixed={0x429153:True,0x429169:False})
 for pc in [0x4291a9,0x4291e4,0x4291f3]:
  if pc not in marked['visited']:raise RuntimeError('helper-object write not on mark arm')
 order(marked,0x42919f,0x4291a9);order(marked,0x4291d3,0x4291e4);order(marked,0x4291d8,0x4291f3);order(marked,0x4291e9,0x4291f3)
 # Check original carriers in the limited straight-line return-to-write slices.
 import capstone
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 for regs,lo,hi in [({'rax','eax','ax','al','ah'},0x4291a4,0x4291a9),({'rax','eax','ax','al','ah'},0x4291d8,0x4291e4),({'rbx','ebx','bx','bl','bh'},0x4291db,0x4291f3),({'rax','eax','ax','al','ah'},0x4291ee,0x4291f3)]:
  for pc in sorted(q for q in ix if lo<=q<hi):
   i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
   if {i.reg_name(r) for r in wr}&regs:raise RuntimeError('helper object/value carrier changed')
 for branch,target,write in [(0x4291a7,0x4291ad,0x4291a9),(0x4291de,0x429296,0x4291e4)]:
  if marked['edges'][branch][0]!=target:raise RuntimeError('helper null guard changed')
  g=G.graph(ix,0x429140,0x4292a6,fixed={0x429153:True,0x429169:False,branch:True})
  if write in g['visited']:raise RuntimeError('helper null arm still writes returned object')
 sweep=G.graph(ix,0x427c90,0x427dd8)
 order(sweep,0x427d18,0x427dae);order(sweep,0x427dae,0x427db3)
 if sweep['edges'][0x427dae]!=[0x427db3] or sweep['edges'][0x427db3]!=[0x427dba]:raise RuntimeError('postcleanup poolflag continuation changed')
 # Pool identities are source RIP targets, not observed runtime pointer values.
 for pc in [0x4279c4,0x429146,0x427c9a]:
  if ix[pc]['memory'][0]['rip_target']!='0x22c6f28':raise RuntimeError('shared pool root changed')
 def fields(lo,hi,base):
  return sorted({m['displacement'] for pc,i in ix.items() if lo<=pc<hi for m in i['memory'] if m['base']==base and m['role']!='addr' and 0x48800<=m['displacement']<=0x48818})
 pending_fields=fields(0x429204,0x429296,'rdx');active_fields=fields(0x427c90,0x427dd8,'rdi')
 if pending_fields!=[0x48808,0x4880c,0x48810,0x48814] or active_fields!=[0x48800,0x48804,0x48808,0x4880c,0x48818]:raise RuntimeError('shared list bookkeeping field population changed')
 return {'slot_publication':{'partitions':slot,'normal_return_source_order':['clear41F730','pending head-or-neighbor links','pending tail48814','selfWORD ID0','metadata420480 active284','dirty290','shared count4880C'], 'qualification':'ID precedes active flag and count, but list links and tail precedeID. Reset calls include sentinel/default writes; not all-zero returned rows.'},
 'scalar_reset':{'writes':scalar,'store_bytes':4,'stores_per_call':4,'bytes_per_call':sum(r['store_bytes'] for r in scalar),'calls':[{'pc':'0x41f95f','span':[0x210,0x220]},{'pc':'0x41f97a','span':[0x220,0x230]}],'qualification':'four4-byte MOVSS stores percall,16B total percall; not four16B scalarstores.'},
 'mark_external_writes':[{'pc':'0x4291a9','object':'422D50 normalreturnRAX ifnonnull','offset':12,'bytes':4,'operation':'AND~2'},{'pc':'0x4291e4','object':'2ED570 normalreturnRAX ifnonnull on reached binding branch','offset':0,'bytes':4,'operation':'AND~4'},{'pc':'0x4291f3','object':'2ED570 result preservedRBX on reached nonnull branch','offset':0xa0,'bytes':4,'operation':'store20E620 EAX onnormalreturn'}],
 'post_active_cleanup':{'pc':'0x427db3','object':'pool loadedfrom022C6F28','offset':0x48818,'bytes':4,'operation':'OR20h','normal_return_order':['DEC sharedcount','cleanup4200A0->clear41F730','ORpool48818,20h','cached-next comparison/continuation']},
 'shared_bookkeeping':{'root_global':'0x22c6f28','pending_endpoints':[0x48810,0x48814],'active_endpoints':[0x48800,0x48804],'count':0x4880c,'cursor':0x48808,'count_and_cursor_bytes':4,'qualification':'one shared source count/cursor, separate pending/active endpoints; not two independent counts or sampled pointer identity.'}}
def main():
 for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
 parents=json.loads((P/'parent-identities.json').read_text());sources=[]
 expected={'render-slot-identity-publication':'a2bcea12693de55748686a2cef48402c0189666974a8af9a8c0720b2717c73ee','render-clear-callee-footprints':'c3e8141dc7fafc01b3fc7651abc3f5be49cf623f66e12c72b8a6615ef08439fc','render-removal-phase-contracts':'fc26ae31f8ddb389fff58deeb7616680334f0e93723e35f4556159e32b47bc5c'}
 if {q['slug']:q['manifest_sha256'] for q in parents}!=expected or len(parents)!=3:raise RuntimeError('parent population changed')
 for q in parents:
  d=P/'parents'/q['slug'];manifest=json.loads((d/'manifest.json').read_text());members={r['path']:r for r in manifest['members']}
  if sha(d/'manifest.json')!=q['manifest_sha256']:raise RuntimeError('parent manifest changed')
  # Status validation before membership/hash validation supplies specific failure evidence.
  for tag,driver in [('capture-01','capture.py'),('prove-01','prove.py')]:
   s=json.loads((d/(tag+'.status.json')).read_text())
   if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(d/driver) or not(d/(tag+'.stdout')).read_bytes() or(d/(tag+'.stderr')).read_bytes():raise RuntimeError('required parent invocation failed '+q['slug']+'/'+tag)
  v=json.loads((d/'result-01.json').read_text())
  if v.get('producer_complete') is not True or v['driver_sha256']!=sha(d/'prove.py'):raise RuntimeError('required parent semantic result incomplete')
  for r in q['retained_files']:
   if sha(d/r['path'])!=r['sha256'] or (r['path']!='manifest.json' and r['sha256']!=members[r['path']]['sha256']):raise RuntimeError('retained parent identity changed')
  name=q['slug']+'-source-01.json'
  if sha(P/name)!=sha(d/'source-01.json'):raise RuntimeError('source alias not original parent')
  sources.append((name,json.loads((P/name).read_text())))
 reviews=json.loads((P/'review-identities.json').read_text())
 if len(reviews)!=6 or {r['reviewer'] for r in reviews}!={'fable','auditspec'}:raise RuntimeError('review population missing')
 for r in reviews:
  if sha(P/r['retained_path'])!=r['sha256']:raise RuntimeError('returned review identity changed')
 V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
 secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,offset in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
  raise RuntimeError('unbacked original range')
 ix={};annotations=[]
 for name,x in sources:
  if x.get('wrapper_complete') is not True or x['exe_sha256']!=PIN:raise RuntimeError('retained source incomplete')
  annotations.append(V.validate(x))
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16)
   if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
   local={int(i['pc'],16):i for i in r['instructions']};tail={0x46d110:'0x202c70',0x3e37e0:'0x861ec0',0x4200a0:'0x41f730'}.get(a)
   g=G.graph(local,a,b,tail=tail)
   if g['visited']!=set(local):raise RuntimeError('incomplete retained original CFG')
   ix.update(local)
 facts=derive(ix,G)
 result={'producer_complete':True,'method':'A STATIC_ONLY retained shipping-byte returned-review qualification','exe_sha256':PIN,'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':name,'sha256':sha(P/name)} for name,x in sources],'annotation_prerequisites':annotations,'parent_identities':parents,'review_identities':reviews,'facts':facts,'limits':['No new capture, native/emulated/live execution. Review executions are external corroboration, not ASTRA tests.','Original normal-return source phases require valid pool/rows/privateframes/indices, nativeABI/normalreturns, reached validhelperobjects and noalias/nointerference.','Source root and instruction order do not establish runtime pointers, atomicity, scheduling, allwriter coherence, naturalreachability or lifetime.','Existing originals/acceptance history immutable; supplemental producer validity still requires independent review and actual canonical consumption.'],'cleanup':'Only owned offline evidence files; no game/PC/control/instrument/save/config/reference/peer mutations.'}
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise RuntimeError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED returned render phase/width/effect qualifications from retained shipping bytes; STATIC_ONLY')
if __name__=='__main__':main()
