"""Selected original upstream counts; no complete caller or natural-state claim.

Fresh result [optional disposable source directory]. Qualified lower result is
reused with exact input/tool receipts; no repeated lower census or code execution.
"""
import importlib.util,json,pathlib,struct,sys
import capstone
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('upstream_cfg','prove-title-queue-consumption.py')
S=module('upstream_annotation','validate-title-source-annotations.py')
EXPECTED={
 '0x180ec4':('0x180fd0','af8b7666c96220f661fa9d2daac5876a63521c6b4fd16107b000e94479f8f429'),
 '0x181054':('0x181167','92c2e3769858beadd8b4332678bfe860b824c7021d2ed324fff0cee4ce235f32'),
 '0x183760':('0x18377f','42a63b27b242f3bfbdbaa8e52c1153e1a9e494c7f731002342281eb9a299419e'),
 '0x183780':('0x183799','562c3e9c64d78143e483df0a07f36f68c36dfe3c9e46c61d9771a792ede4476b'),
 '0x1837a0':('0x1837bf','247fe1d37024d385acb5ddf6751344150b0dd8d77d77de8864944629a92f0134'),
 '0x1837c0':('0x1839fd','b29da13b34782a57528c2ad39276b23dff5f2dc23046c10257912cc1a0d90dcc'),
 '0x183eb0':('0x183ed4','6f608b90118467b937735eea2eb6ffac1319c19ccc09d2c3518232e8441cdc64'),
 '0x1baa30':('0x1bafe7','1200862630776d073831377824e2d301392e4588373611af518fae9d474fff8c'),
 '0x180e70':('0x180ec4','e9aaaf55537ace664f840a54326ba34002024df95fb5d2fae006831575b4456f'),
 '0x180fd0':('0x180ff1','c75d5d8509e2f18ac683be23f97a5e1b992aa2550824bb20a8349fca09bd0608'),
 '0x181000':('0x181054','6e784df58590729e8ec49e3a2e1ac58be501eba5fae089751359e09e37ed089d'),
 '0x181167':('0x181188','3815c20dcc198a17e23d1a865a5e7e5f25fda70a9158344484cf7f4cfbae2edd')}
REGIONS=[(0x180e70,0x180ff1),(0x181000,0x181188),(0x183760,0x18377f),(0x183780,0x183799),(0x1837a0,0x1837bf),(0x1837c0,0x1839fd),(0x183eb0,0x183ed4),(0x1baa30,0x1bafe7)]

def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 # Status/exception/tool/input gates precede downstream calculation. A PASS
 # label is never a substitute for qualified original instructions.
 lower_path=src/'texture-resize-input-domain-result-01.json';lower=json.loads(lower_path.read_text())
 if lower.get('producer_complete') is not True or lower.get('exe_sha256')!=P.SHA or lower.get('status')!='PRODUCER_CHECKED_SELECTED_RAW_COUNT_FLOOR_WITH_HIGHBIT_RESIDUE_INDEPENDENT_PENDING':raise ValueError('required lower-floor result failed or incomplete')
 if P.sha(lower_path)!='603cb3a9d083860c022cfabd671215915ec6c5964033beb8f337afaf63670129' or lower['checker_sha256']!=P.sha(W/'prove-texture-resize-input-domain.py'):raise ValueError('required lower-floor result/tool identity changed')
 receipt_path=src/'texture-resize-input-domain-positive-01.status.json';receipt=json.loads(receipt_path.read_text())
 if receipt.get('exit')!=0 or receipt.get('driver')!='prove-texture-resize-input-domain.py':raise ValueError('required lower-floor invocation failed or incomplete')
 lower_sources=[]
 for q in lower['source_pins']:
  if P.sha(src/q['path'])!=q['sha256']:raise ValueError('required lower-floor source changed')
  v,_=P.load(src,q['path'],[]);lower_sources.append(S.validate(v))
 if len(lower_sources)!=3 or len(lower['selected_calls'])!=6:raise ValueError('missing lower-floor prerequisites')
 pins=[];raws=[];ix={};annotations=[]
 for name in ('texture-resize-dynamic-input-producers-source-01.json','texture-resize-forwarded-input-caller-source-01.json','texture-resize-palette-root-edges-source-01.json'):
  v,i=P.load(src,name,pins);annotations.append(S.validate(v));raws.append(v)
  if set(ix)&set(i):raise ValueError('overlapping original source spans')
  ix.update(i)
 ranges=[q for v in raws for q in v['ranges']]
 if len(ranges)!=12 or {q['start'] for q in ranges}!=set(EXPECTED):raise ValueError('missing/extra selected upstream range')
 if any((q['end_exclusive'],q['sha256'])!=EXPECTED[q['start']] for q in ranges):raise ValueError('selected upstream shipping identity changed')
 # Exact parent triples matter: both roots share an unwind address.
 expected_groups=[[[0x180e70,0x180ec4,0x1d539d0],[0x180ec4,0x180fd0,0x1d539a8],[0x180fd0,0x180ff1,0x1d539c0]],[[0x181000,0x181054,0x1d539d0],[0x181054,0x181167,0x1d539ec],[0x181167,0x181188,0x1d53a04]]]
 groups=raws[2].get('palette_roots',[])
 if [q['entries'] for q in groups]!=expected_groups:raise ValueError('missing original palette parent triples')
 for group in groups:
  if len(group['unwind'])!=3:raise ValueError('missing original palette unwind')
  for k,(e,u) in enumerate(zip(group['entries'],group['unwind'])):
   h=bytes.fromhex(u['raw']);flags=h[0]>>3;at=(4+2*h[2]+3)&~3
   if u['address']!=hex(e[2]) or u['header']!=h[:4].hex() or flags!=u['flags'] or u['chain']!=(group['entries'][0] if k else None):raise ValueError('palette root metadata inconsistent')
   if k and (flags!=4 or len(h)!=at+12 or [v+0x120000 for v in struct.unpack_from('<III',h,at)]!=group['entries'][0]):raise ValueError('palette original parent encoding changed')
   if not k and (flags!=3 or len(h)!=at+4 or u['handler']!=hex(struct.unpack_from('<I',h,at)[0]+0x120000)):raise ValueError('palette original handler boundary changed')
 # CALL identity is aligned original code, not arithmetic-only raw E8 matches.
 meta=raws[0]['callsite_metadata']+raws[1]['callsite_metadata']
 expected_sites={0x180f8e:0x17f3b0,0x181122:0x17f3b0,0x183775:0x17e8e0,0x18378f:0x17e8e0,0x1837b5:0x17e8e0,0x1839dd:0x17e8e0,0x183eca:0x17e8e0,0x1babb2:0x183780}
 if len(meta)!=8 or {int(q['site'],16) for q in meta}!=set(expected_sites):raise ValueError('missing original selected call metadata')
 for q in meta:
  pc=int(q['site'],16);P.need(ix,pc,'call',hex(expected_sites[pc]))
  if ix[pc]['bytes']!=q['expected_call_bytes'] or q['expected_target']!=hex(expected_sites[pc]):raise ValueError('original selected call metadata disagrees')
  a,z,u=q['fragment']
  if not a<=pc<z or (q['chain'] is None and (a,z) not in REGIONS):raise ValueError('selected call root identity missing')
  if q['chain'] is not None and not any(q['chain']==g[0] and q['fragment'] in g for g in expected_groups):raise ValueError('selected call wrong root parent')
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 decoded={i.address:i for q in ranges for i in cs.disasm(bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])),int(q['start'],16))}
 cfgs=[];graphs={};preds={};doms={}
 for a,z in REGIONS:
  cfgs.append(P.closed(ix,a,z));local={p for p in ix if a<=p<z};g={};pred={p:set() for p in local}
  for pc in local:
   i=ix[pc];m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
   targets=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [n,int(i['args'],16)] if m.startswith('j') else [n]
   g[pc]=targets
   for t in targets:pred[t].add(pc)
  d={p:{p} if p==a else set(local) for p in local};change=True
  while change:
   change=False
   for pc in sorted(local):
    if pc==a:continue
    new={pc}|set.intersection(*(d[t] for t in pred[pc]))
    if new!=d[pc]:d[pc]=new;change=True
  graphs[a]=g;preds[a]=pred;doms[a]=d
 def reach(g,start,stop):
  todo=[start];seen=set()
  while todo:
   pc=todo.pop()
   if pc in seen or pc==stop:continue
   seen.add(pc);todo.extend(g[pc])
  return seen
 def preserved(root,first,last,family):
  interval=(reach(graphs[root],first,last)&reach(preds[root],last,first))-{first,last}
  for pc in interval:
   i=decoded[pc]
   if i.mnemonic=='call' or {i.reg_name(r) for r in i.regs_access()[1]}&set(family):raise ValueError('volatile count source clobbered '+hex(pc))
 R9=('r9','r9d','r9w','r9b');R8=('r8','r8d','r8w','r8b');RCX=('rcx','ecx','cx','cl','ch')
 specs=[(0x180e70,0x180f8e,0x180f87,1),(0x181000,0x181122,0x18111f,1),(0x183760,0x183775,0x18376a,4),(0x1837a0,0x1837b5,0x1837aa,1),(0x1837c0,0x1839dd,0x1839cb,4),(0x183eb0,0x183eca,0x183ec4,1),(0x1baa30,0x1babb2,0x1babae,32)]
 for root,call,definition,n in specs:
  if definition not in doms[root][call]:raise ValueError('count definition does not dominate call')
  preserved(root,definition,call,R9)
  if n!=32 and root not in (0x180e70,0x181000):P.need(ix,definition,'mov','r9d, '+str(n))
 for root,origin,transfer,call in ((0x180e70,0x180f81,0x180f87,0x180f8e),(0x181000,0x181114,0x18111f,0x181122)):
  P.need(ix,origin,'mov','r8d, 1');P.need(ix,transfer,'mov','r9d, r8d')
  if origin not in doms[root][transfer] or origin not in doms[root][call]:raise ValueError('palette constant does not dominate')
  preserved(root,origin,transfer,R8)
 P.need(ix,0x1babac,'xor','ecx, ecx');P.need(ix,0x1babae,'lea','r9d, [rcx + 0x20]')
 if 0x1babac not in doms[0x1baa30][0x1babae]:raise ValueError('forwarded32 zero-base definition missing')
 preserved(0x1baa30,0x1babac,0x1babae,RCX)
 # Leaf forwards incoming R9 exactly; no intervening opaque call before17E8E0.
 preserved(0x183780,0x183780,0x18378f,R9)
 if {decoded[0x183780].reg_name(r) for r in decoded[0x183780].regs_access()[1]}&set(R9):raise ValueError('forwarder entry modifies R9')
 rows=[dict(root=hex(a),call=hex(c),definition=hex(d),incoming_floor_u32=n,after_floor=max(1,n),masked=max(1,n)&0x7fffffff) for a,c,d,n in specs]
 if any(q['after_floor']!=q['incoming_floor_u32'] or q['masked']==0 for q in rows):raise ValueError('selected safe-count constraint failed')
 result=dict(status='PRODUCER_CHECKED_SELECTED_UPSTREAM_COUNTS_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,
  question='Can these selected upstream original normal paths supply the80000000 masked-zero residue to the two lower count floors?',
  hypotheses=['Selected source count admits80000000','Dominating selected source definitions constrain counts to1/4/32'],
  result='REFUTED on selected paths: constants1/4/32 survive max(1,u32) unchanged and remain nonzero after AND7FFFFFFF. The arbitrary-input80000000 counterexample remains valid outside this selected coverage.',
  source_pins=pins,annotation_prerequisites=annotations,normal_cfgs=cfgs,selected_argument_paths=rows,
  forwarding_chain=dict(caller='0x1babb2',caller_count=32,leaf='0x183780',leaf_call='0x18378f',target='0x17e8e0',property='R9 unchanged before leaf call; later lower count-floor proof is retained/qualified'),
  required_result_pins=[dict(path=lower_path.name,sha256=P.sha(lower_path),checker_path='prove-texture-resize-input-domain.py',checker_sha256=lower['checker_sha256'],source_pins=lower['source_pins'],annotation_prerequisites=lower_sources,independent_acceptance='PENDING')],
  required_invocation_receipts=[dict(path=receipt_path.name,sha256=P.sha(receipt_path),checked_exit=receipt['exit'])],
  observations=['Two complete palette normal roots supply1 viaR8D->R9D; their source pixel-count EDX16/256 is a different argument, not texture element count',
  'Four other prepared wrappers overwriteR9D with1/4 immediately before their normal call',
  '183780 passes incomingR9 unchanged; its selected1BABB2 caller establishesRCX0 then LEA R9D[RCX+20], yielding32. Earlier1BAB52 load ofR9D fromresource+F8 is overwritten, not this call count',
  'Complete normal CFG/definition domination proves this bounded argument property; it does not prove any root naturally executes with valid initialized resources'],
  assumptions=['Original normal entry/return, ordinary ABI, valid private stack/objects, no interference or exceptional/interior entries','Qualified lower count-floor/private-slot prerequisites retained; opaque lower callees obey their stated premises'],
  limitations=['Seven prepared upstream sites plus one selected forwarder caller; reference search is not complete direct/indirect/RVA/virtual/registry closure',
  'No universal texturecount<=32, initialized allocation, native callback/scheduling/lifetime, save/resource success, naturally executed call or game-crash conclusion',
  '1837C0 buffer/conversion safety and exception-handler semantics are outside this count proof','No new original-code/harness/emulated/live runs; producer checks are not independent acceptance'],
  affected_claims=['OPUS selected renderer texture count-domain contract:1/4/32 excludes raw/masked zero on these paths','FABLE natural zero-count question: other callers/indirect binding or a violated premise needed; these selected paths need no game test'],
  next_discriminator='Bind remaining direct/indirect/registry callers only for a named universal producer claim, or move to independent pending-ticket lifetime/callback-dispatch obligation. Do not repeat these constants/samples.',
  learned_precondition='Containing palette child fragments alone were not whole normal roots; retained543B children were reused and only234B missing edges captured. Parent triples are distinct despite shared unwind address.',
  checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
  cleanup='Finite file reads/CFG/dataflow only; no PC/game/input/instrument/save/config/reference or peer-process writes')
 out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n');print('Selected original upstream counts1/4/32 exclude raw/maskedzero; full normal CFGs, no universal/natural-state closure')
if __name__=='__main__':main()
