"""Ordered native writes/null partitions; no injected or naturally observed state."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 ops=[(0x309c00,'mov','eax, dword ptr [rip + 0x1fb8572]'),(0x309c06,'cmp','eax, -1'),
 (0x309c09,'jne','0x309c0e'),(0x309c0b,'xor','eax, eax'),(0x309c0e,'test','rdx, rdx'),
 (0x309c11,'je','0x309c15'),(0x309c13,'mov','dword ptr [rdx], eax'),
 (0x309c15,'test','rcx, rcx'),(0x309c18,'je','0x309c22'),
 (0x309c1a,'mov','eax, dword ptr [rip + 0x1fb856c]'),(0x309c20,'mov','dword ptr [rcx], eax'),
 (0x309c22,'mov','dword ptr [rip + 0x1fb854c], 0xffffffff'),(0x309c2c,'mov','eax, 1'),
 (0x34836b,'mov','rsi, rax'),(0x34837c,'call','0x2650b0'),(0x348381,'mov','rdx, rsi'),
 (0x348384,'mov','rcx, rax'),(0x348387,'mov','rbx, rax'),(0x34838a,'call','0x309c00'),
 (0x3483a9,'mov','ecx, dword ptr [rbx]'),(0x3483b1,'mov','ecx, dword ptr [rsi]')]
 for pc,m,a in ops:
  if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('native output witness changed '+hex(pc))
 if [ix[pc]['memory'][0]['rip_target'] for pc in [0x309c00,0x309c1a,0x309c22]]!=['0x22c2178','0x22c218c','0x22c2178']:raise RuntimeError('queue/unit source identities changed')
 whole=G.graph(ix,0x309c00,0x309c32)
 if whole['calls'] or whole['visited']!={pc for pc in ix if 0x309c00<=pc<0x309c32}:raise RuntimeError('primitive full local CFG missing')
 partitions=[]
 for available in [False,True]:
  for action_out in [False,True]:
   for unit_out in [False,True]:
    g=G.graph(ix,0x309c00,0x309c32,fixed={0x309c09:available,0x309c11:not action_out,0x309c18:not unit_out})
    writes=[pc for pc in sorted(g['visited']) if any(m['role'] in ['w','rw'] for m in ix[pc]['memory'])]
    wanted=([0x309c13] if action_out else [])+([0x309c20] if unit_out else [])+[0x309c22] if available else []
    if writes!=wanted or g['returns']!=([0x309c31] if available else [0x309c0d]):raise RuntimeError('nullable-output partition changed')
    if available and action_out and unit_out and not (G.dominates(g,0x309c13,0x309c1a) and G.dominates(g,0x309c20,0x309c22)):raise RuntimeError('native write/read/reset order changed')
    partitions.append(dict(queue_available=available,action_pointer_nonnull=action_out,unit_pointer_nonnull=unit_out,writes=[hex(p) for p in writes],return_DWORD=int(available)))
 bridge=G.graph(ix,0x348330,0x3483d5,tail='0x26b4e0')
 if bridge['tails']!=[0x3483d0] or not all(G.dominates(bridge,0x34838a,pc) for pc in [0x3483a9,0x3483b1]):raise RuntimeError('bridge postcall reads not unconditional')
 # Formula implements the established two DWORD store order, not a native run.
 a=(303).to_bytes(4,'little');u=(0x89abcdef).to_bytes(4,'little');rows=[]
 for delta in range(-4,5):
  final=bytes(u[j-delta] if 0<=j-delta<4 else a[j] for j in range(4))
  rows.append(dict(unit_pointer_minus_action_pointer=delta,initial_action_hex=a.hex(),unit_hex=u.hex(),final_action_bytes=final.hex(),final_action_DWORD=int.from_bytes(final,'little'),overlap_bytes=max(0,4-abs(delta))))
 if next(x for x in rows if x['unit_pointer_minus_action_pointer']==0)['final_action_DWORD']!=0x89abcdef:raise RuntimeError('same-output countermodel missing')
 return dict(native_partitions=partitions,source_order=['queue DWORD read22C2178','conditional action DWORD store RDX','conditional unit DWORD read22C218C/store RCX','queue DWORD reset22C2178=FFFFFFFF','DWORD return1'],
 both_null='Available queue with both output pointersNULL: no output dereference/write, queue still reset, DWORD return1. Unavailable queue returnsDWORD0, leaves queue and outputs unchanged.',
 overlap_formula='For nonNULL source-global-disjoint outputs, delta=RCX-RDX. Final action byte[j] is unit byte[j-delta] when0<=j-delta<4, otherwise original action byte[j]. Samebuffer leaves unit DWORD in both views. Only byte-range-disjoint outputs guarantee preservation of both values independent of their contents.',
 arithmetic_countermodels=rows,
 source_alias_limit='Unit global22C218C is read after the first output store. If an output aliases source/reset globals, the unchanged-unit/overlap formula premises fail. Such aliases are not included in this proof.',
 bridge_limit='348330 unconditionally reads DWORD[*RBX] and DWORD[*RSI] after309C00 normal return, even when its queue result is0. Primitive null guards therefore do not certify a safe whole bridge call; valid destinations still required. No actual null pointer, exception/fault or authored alias observed.')
def main(out):
 if out.exists():raise RuntimeError('immutable result exists')
 pins=json.loads((P/'input-identities-01.json').read_text())['inputs']
 for x in pins:
  if sha(P/x['path'])!=x['sha256']:raise RuntimeError('required retained input changed')
 V=load('shared_roles','validate-title-source-annotations.py');G=load('actual_CFG','prove_owner_reload_order.py')
 if not callable(getattr(G,'graph',None)) or not callable(getattr(G,'dominates',None)):raise RuntimeError('required CFG interface missing')
 ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());im=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 if hashlib.sha256(im).hexdigest()!=pin:raise RuntimeError('shipping EXE changed')
 pe=struct.unpack_from('<I',im,60)[0];op=struct.unpack_from('<H',im,pe+20)[0];secs=[struct.unpack_from('<IIII',im,pe+24+op+k*40+8) for k in range(struct.unpack_from('<H',im,pe+6)[0])]
 def rd(a,n):
  for vs,v,rs,r in secs:
   if 0x120000+v<=a and a+n<=0x120000+v+rs:return im[r+a-0x120000-v:r+a-0x120000-v+n]
  raise RuntimeError('unbacked original range')
 ix={};sourcepins=[];checks=[]
 for n in ['spattack-queue-reader-raw-01.json','spattack-info-raw-01.json']:
  r=json.loads((P/n).read_text());checks.append(V.validate(r));sourcepins.append(dict(path=n,sha256=sha(P/n)))
  if r['exe_sha256']!=pin:raise RuntimeError('retained source image identity differs')
  for q in r['ranges']:
   blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
   if blob!=rd(int(q['start'],16),len(blob)):raise RuntimeError('shipping source bytes differ')
   ix.update({int(i['pc'],16):i for i in q['instructions']})
 result=dict(producer_complete=True,method='A retained original shipping bytes/local CFG and write-range algebra; no new capture/native/emulator/game execution',
 exe_sha256=pin,driver_sha256=sha(Path(__file__)),source_pins=sourcepins,annotation_prerequisites=checks,input_pins=pins,facts=derive(ix,G),
 limits='Valid stable readable source globals, nonwrapping readable/writable output ranges if nonNULL; overlap algebra requires output ranges disjoint from both source/reset globals. Private frame, normal ABI/returns/no interference. No actual authored pointer alias, allocation size, fault, owner/lifetime, concurrent state, interpreter or natural command reachability.',
 affected_claims=['OV42 two-field native output representation and unchanged transfer premise','FABLE script-to-native queue reader versus full bridge safety','OPUS nullable primitive and disjoint out-range ABI preconditions'])
 with out.open('x') as f:json.dump(result,f,indent=2)
 print('PROVED ordered overlapping outputs/all-null consumption; whole bridge still requires valid destinations')
if __name__=='__main__':main(Path(sys.argv[1]))
