"""Bound selected original caller count sources; no all-caller/natural census.

Reuse four retained bodies plus missing prefix/tail; all normal CFGs closed.
Flooring rawu32 atone does not exclude encoded zero after bit31 masking.
"""
import importlib.util,json,pathlib,sys
import capstone
W=pathlib.Path(__file__).resolve().parent
def mod(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=mod('normal_cfg','prove-title-queue-consumption.py');S=mod('actual_annotation','validate-title-source-annotations.py')
EXPECTED={
 '0x17e8e0':('0x17ebca','12f0954c83902638b8c609c490e13291d86fb11871c3fdb15ceb2bc338b1bdd9'),
 '0x17f3b0':('0x17f5b0','a1635218f9dae062a4b928df96f2292dc5dceb76c89aa34d6cf46a40bb754f60'),
 '0x1946e0':('0x1949b6','02297d5efd51139eb5862aa0c83db31de9120286799f3598e6f611def2048a60'),
 '0x1b7941':('0x1b7c93','120e3eb8f0eff4e5deb565482e8d670fb6521c86ee84861485036dce15a45fa1'),
 '0x1b7850':('0x1b7941','7d9126734144388d158992ef00ce312530fa90bece9c4a8ee6145a0bce10941a'),
 '0x1b7c93':('0x1b7cde','9407d2a8acf6ddf963d8c117d9cfa591224e04d43ef7cada44c50842374fa15e')}

def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 pins=[];raws=[];ix={};annotations=[]
 for name in ['texture-resize-input-callers-source-01.json','texture-resize-input-root-prefix-source-01.json','texture-resize-input-tail-source-01.json']:
  v,i=P.load(src,name,pins);annotations.append(S.validate(v));raws.append(v)
  if set(ix)&set(i):raise ValueError('overlapping raw source spans')
  ix.update(i)
 ranges=[q for v in raws for q in v['ranges']]
 if len(ranges)!=6 or {q['start'] for q in ranges}!=set(EXPECTED):raise ValueError('missing/extra selected original body')
 if any((q['end_exclusive'],q['sha256'])!=EXPECTED[q['start']] for q in ranges):raise ValueError('selected original body identity changed')
 tail=raws[2]
 if len(tail.get('pdata_entries',[]))!=6 or len(tail.get('unwind',[]))!=6 or raws[1]['pdata_entries']!=tail['pdata_entries'][:3]:raise ValueError('missing complete chained root metadata')
 for a,b,c in zip(tail['pdata_entries'],tail['pdata_entries'][1:],tail['unwind'][1:]):
  if a[1]!=b[0] or c['chain']!=tail['pdata_entries'][0]:raise ValueError('chained-root gap or wrong parent')
 regions=[(0x17e8e0,0x17ebca),(0x17f3b0,0x17f5b0),(0x1946e0,0x1949b6),(0x1b7850,0x1b7cde)]
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 decoded={i.address:i for q in ranges for i in cs.disasm(bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])),int(q['start'],16))}
 cfgs=[];graphs={};doms={};preds={}
 for a,z in regions:
  cfgs.append(P.closed(ix,a,z));local={p for p in ix if a<=p<z};g={};pred={p:set() for p in local}
  for p in local:
   i=ix[p];m=i['mnemonic'];n=p+len(bytes.fromhex(i['bytes']))
   targets=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [n,int(i['args'],16)] if m.startswith('j') else [n]
   g[p]=targets
   for t in targets:pred[t].add(p)
  d={p:{p} if p==a else set(local) for p in local};changed=True
  while changed:
   changed=False
   for p in local:
    if p==a:continue
    new={p}|set.intersection(*(d[t] for t in pred[p]))
    if new!=d[p]:d[p]=new;changed=True
  graphs[a]=g;doms[a]=d;preds[a]=pred
 def reaches(g,start,stop):
  todo=[start];seen=set()
  while todo:
   p=todo.pop()
   if p in seen or p==stop:continue
   seen.add(p);todo.extend(g[p])
  return seen
 def interval(root,first,last):
  g=graphs[root];rev={p:list(v) for p,v in preds[root].items()}
  return (reaches(g,first,last)&reaches(rev,last,first))-{first,last}
 def unchanged(root,first,last,family):
  for pc in interval(root,first,last):
   i=decoded[pc]
   if i.mnemonic=='call':continue # specified ordinary nonvolatile ABI only
   if {i.reg_name(r) for r in i.regs_access()[1]}&set(family):raise ValueError('count source overwritten '+hex(pc))
 def private(root,first,last,offset):
  for pc in interval(root,first,last):
   i=decoded[pc]
   if i.mnemonic!='call' and 'rsp' in {i.reg_name(r) for r in i.regs_access()[1]}:raise ValueError('private-slot frame changed')
   for m in ix[pc]['memory']:
    if m['base']=='rsp' and m['role'] in ('w','rw') and m['displacement']<offset+4 and offset<m['displacement']+m['size']:raise ValueError('private count slot overwritten '+hex(pc))
 specs=[(0x17e8e0,0x17ea2a,[0x17e90f,0x17e9df,0x17e9e5,0x17e9e8,0x17e9ec,0x17e9f1,0x17ea23]),(0x17f3b0,0x17f477,[0x17f3e9,0x17f43b,0x17f440,0x17f443,0x17f447,0x17f472]),(0x1946e0,0x1947a0,[0x19472d,0x19479b]),(0x1b7850,0x1b79e2,[0x1b79da]),(0x1b7850,0x1b7a65,[0x1b7a5d]),(0x1b7850,0x1b7ae7,[0x1b7adf])]
 for root,call,defs in specs:
  if not set(defs)<=doms[root][call]:raise ValueError('count definitions do not dominate selected call')
  P.need(ix,call,'call','0x628100')
 for p,m,a in [(0x17e90f,'mov','dword ptr [rsp + 0x30], r9d'),(0x17e9df,'mov','r15d, 1'),(0x17e9e5,'mov','edx, r15d'),(0x17e9e8,'cmp','dword ptr [rsp + 0x30], edx'),(0x17e9ec,'cmova','edx, dword ptr [rsp + 0x30]'),(0x17e9f1,'mov','dword ptr [rsp + 0x38], edx'),(0x17ea23,'mov','edx, dword ptr [rsp + 0x38]'),(0x17f3e9,'mov','r15d, r9d'),(0x17f43b,'mov','esi, 1'),(0x17f440,'cmp','r15d, esi'),(0x17f443,'mov','edi, esi'),(0x17f447,'cmova','edi, r15d'),(0x17f472,'mov','edx, edi'),(0x19472d,'mov','esi, 1'),(0x19479b,'mov','edx, esi'),(0x1b79da,'mov','edx, 4'),(0x1b7a5d,'mov','edx, 4'),(0x1b7adf,'mov','edx, 4')]:P.need(ix,p,m,a)
 private(0x17e8e0,0x17e90f,0x17e9ec,0x30);private(0x17e8e0,0x17e9f1,0x17ea23,0x38)
 unchanged(0x17f3b0,0x17f3e9,0x17f447,['r15','r15d','r15w','r15b'])
 unchanged(0x17f3b0,0x17f43b,0x17f447,['rsi','esi','si','sil'])
 unchanged(0x17f3b0,0x17f447,0x17f472,['rdi','edi','di','dil'])
 unchanged(0x1946e0,0x19472d,0x19479b,['rsi','esi','si','sil'])
 for root,call,defs in specs[3:]:unchanged(root,defs[0],call,['rdx','edx','dx','dl','dh'])
 # Native instruction witnesses bind the unsigned operation; this integer
 # constraint proof is not a synthetic/native execution or natural input.
 witnesses=[dict(incoming_u32=n,emitted=max(1,n),masked=max(1,n)&0x7fffffff) for n in (0,1,0x7fffffff,0x80000000,0xffffffff)]
 if witnesses[3]['masked']!=0:raise ValueError('masked-zero counterexample calculation failed')
 r=dict(status='PRODUCER_CHECKED_SELECTED_RAW_COUNT_FLOOR_WITH_HIGHBIT_RESIDUE_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisites=annotations,normal_cfgs=cfgs,
  question='Do the six validated direct628100 call sites admit raw zero, and does their count floor prove nonzero masked element count?',
  hypotheses=['A selected normal caller supplies rawzero','All six exclude rawzero, but dynamic highbit input can defeat a stronger masked-nonzero inference'],
  result='Selected rawzero excluded under explicit normal ABI/private-slot/no-interference premises. Masked nonzero universal claim REFUTED for arbitrary dynamicR9D: max(1,80000000)&7FFFFFFF=0. Natural occurrence and all other callers OPEN.',
  selected_calls=[dict(call=hex(c),root=hex(a),definitions=[hex(p) for p in d],count='max(1,u32 incomingR9D)' if a in (0x17e8e0,0x17f3b0) else '1' if a==0x1946e0 else '4') for a,c,d in specs],
  algebraic_witnesses=witnesses,mask_proof='N&7FFFFFFF=0 iff N is0 or80000000. All selected N>=1 excludes0. The two unsigned floors do not exclude80000000; fixed1/4 exclude both.',
  assumptions=['Original normal entries/returns and ordinary nonvolatile ABI','Valid objects/storage; private stack30/38 not aliased or modified by opaque callees/interference','No exception/unwind/async entry or arbitrary interior call bypassing defining instructions'],
  limitations=['Only six verified direct sites; raw-reference scan is not a complete direct/indirect/RVA/virtual caller census','No natural incomingR9D bounds, shipping highbit occurrence, allocation success or actual zero-count crash','Rawzero helper counterexample remains valid conditionally but cannot be routed through these sites under these premises','Encoded ownership/highbit count semantics, lower allocator/resource effects and full lifecycle remain separately open'],
  learned_precondition='A containing pdata fragment is not a whole root. Initial normal closure refused1B7C93. Retained241/850 bytes were reused, only75B missing tail added; six actual fragments and all normal branches now covered.',
  affected_claims=['OPUS selected texture count ABI/domain contract','FABLE natural zero-count resize discriminator should target dynamic input producers/highbit or other callers, not replay these six rawzero paths'],
  next_discriminator='Trace ordinary R9D producers feeding17E8E0/17F3B0 and establish nonzero masked-count bounds, or legal counterexample. Prove caller completeness separately; no game session justified.',
  checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Original/retained reads and finite CFG/dataflow only; no PC/game/input/instrument/save/config/reference/peer-process writes')
 out.open('x',encoding='utf-8').write(json.dumps(r,indent=2)+'\n');print('Six selected rawzero paths excluded; two unsigned floors retain exact80000000 masked-zero residue; no natural/all-caller claim')
if __name__=='__main__':main()
