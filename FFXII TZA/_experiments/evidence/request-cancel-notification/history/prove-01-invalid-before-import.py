"""Source proof: native mode4 cancellation need not wait for RET."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
PARENT='814b83ad013385518de8a269ee75b4ac949ba574ad8b998940231065edb0f7cd'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(source,parent,G):
 ix={int(i['pc'],16):i for r in source['ranges'] for i in r['instructions']}
 for r in source['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16)
  g=G.graph(ix,a,b,tail='0x3db6e0' if a in [0x352980,0x353660] else None)
  if g['visited']!={int(i['pc'],16) for i in r['instructions']}:raise ValueError('selected CFG not complete')
 def need(pc,m,a):
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('required cancel operation changed '+hex(pc))
 for op in [
  (0x352986,'mov','rcx, r9'),(0x352989,'mov','rbx, rdx'),(0x35298c,'call','0x267e10'),(0x352991,'mov','r8d, 4'),
  (0x352997,'mov','edx, eax'),(0x352999,'mov','rcx, rbx'),(0x35299c,'call','0x3db420'),(0x3529a1,'mov','rcx, rbx'),(0x3529a9,'jmp','0x3db6e0'),
  (0x35366a,'mov','rcx, r9'),(0x35366d,'mov','rbx, r9'),(0x353670,'call','0x267e10'),(0x353675,'mov','rcx, rbx'),
  (0x353678,'mov','edi, eax'),(0x35367a,'call','0x267e10'),(0x35367f,'mov','ecx, eax'),(0x353681,'call','0x264010'),
  (0x353686,'mov','r8d, 4'),(0x35368c,'lea','edx, [rdi + 1]'),(0x35368f,'mov','rcx, rax'),(0x353692,'mov','rbx, rax'),
  (0x353695,'call','0x3db420'),(0x35369a,'mov','rcx, rbx'),(0x3536a7,'jmp','0x3db6e0'),
  (0x3db426,'mov','rbx, rcx'),(0x3db429,'test','rcx, rcx'),(0x3db42c,'je','0x3db545'),
  (0x3db432,'movzx','r9d, byte ptr [rcx + 0x88]'),(0x3db43a,'xor','eax, eax'),(0x3db441,'test','edx, edx'),
  (0x3db448,'movzx','esi, byte ptr [rcx + 0x89]'),(0x3db44f,'cmovns','eax, edx'),(0x3db457,'movzx','r12d, word ptr [rcx + 6]'),
  (0x3db466,'cmp','r8d, 3'),(0x3db46a,'jne','0x3db473'),(0x3db46c,'lea','r9d, [rax + 1]'),(0x3db470,'xor','r8d, r8d'),
  (0x3db473,'xor','r14d, r14d'),(0x3db476,'movsxd','r15, eax'),(0x3db479,'cmp','r8d, 4'),
  (0x3db47d,'lea','ecx, [r9 - 1]'),(0x3db481,'movsxd','rbp, ecx'),(0x3db484,'cmovne','r14d, r8d'),
  (0x3db488,'cmp','rbp, r15'),(0x3db48b,'jl','0x3db53e'),(0x3db49b,'rol','edi, cl'),
  (0x3db4a0,'movzx','r8d, byte ptr [rbx + rbp + 0x94]'),(0x3db4a9,'test','r12d, edi'),(0x3db4ac,'je','0x3db50b'),
  (0x3db4ae,'xor','eax, eax'),(0x3db4b0,'cmp','r8d, 0xff'),(0x3db4b7,'je','0x3db50b'),
  (0x3db4b9,'mov','rcx, qword ptr [rbx + 0xa0]'),(0x3db4c0,'lea','rdx, [r8 + r8*4]'),
  (0x3db4c4,'movzx','r9d, byte ptr [rcx + rdx*4 + 0x11]'),(0x3db4ca,'test','r9d, r9d'),(0x3db4cd,'jne','0x3db4dc'),
  (0x3db4cf,'cmp','eax, esi'),(0x3db4d1,'jg','0x3db50b'),(0x3db4d3,'movzx','r8d, byte ptr [rcx + rdx*4]'),
  (0x3db4d8,'inc','eax'),(0x3db4da,'jmp','0x3db4b0'),(0x3db4dc,'mov','ecx, r14d'),(0x3db4df,'test','r14d, r14d'),
  (0x3db4e2,'je','0x3db500'),(0x3db500,'mov','edx, r8d'),(0x3db503,'mov','rcx, rbx'),(0x3db506,'call','0x3db2a0'),
  (0x3db50b,'ror','edi, 1'),(0x3db50d,'dec','rbp'),(0x3db510,'cmp','rbp, r15'),(0x3db513,'jge','0x3db4a0'),
  (0x3db51a,'mov','eax, 1'),(0x3db53e,'mov','eax, 1'),(0x3db545,'mov','eax, 1')
 ]:need(*op)
 graphs=[G.graph(ix,0x352980,0x3529ae,tail='0x3db6e0'),G.graph(ix,0x353660,0x3536ac,tail='0x3db6e0')]
 if graphs[0]['calls']!=[(0x35298c,'0x267e10'),(0x35299c,'0x3db420')] or graphs[1]['calls']!=[(0x353670,'0x267e10'),(0x35367a,'0x267e10'),(0x353681,'0x264010'),(0x353695,'0x3db420')]:raise ValueError('native caller boundary changed')
 for g in graphs:
  if g['tails']!=[0x3529a9 if g['entry']==0x352980 else 0x3536a7]:raise ValueError('postcancel scheduling tail changed')
 g=G.graph(ix,0x3db420,0x3db550)
 if g['calls']!=[(0x3db506,'0x3db2a0')]:raise ValueError('recycle gained another native boundary')
 fixed={0x3db42c:False,0x3db46a:True,0x3db48b:False,0x3db4ac:False,0x3db4b7:False,0x3db4cd:True,0x3db4e2:True}
 admitted=G.graph(ix,0x3db420,0x3db550,fixed=fixed)
 if not G.dominates(admitted,0x3db484,0x3db506) or (0x3db506,'0x3db2a0') not in admitted['calls']:raise ValueError('mode4 nonzero state no longer reaches removal')
 # Once this single selected entry is removed, every back edge to scan another
 # channel passes DEC RBP. There is no same-channel rescan after the call.
 todo=[0x3db50b];seen=set()
 while todo:
  pc=todo.pop()
  if pc==0x3db50d or pc in seen:continue
  if pc==0x3db4a0 or pc==0x3db506:raise ValueError('recycler removes another entry before changing channel')
  seen.add(pc);todo.extend(g['edges'][pc])
 for pc in g['returns']:
  value=0x3db545 if pc==0x3db54f else 0x3db51a
  # Nonnull empty range uses53E then51F instead of51A.
  if pc!=0x3db54f and not(G.dominates(g,0x3db51a,pc) or 0x3db53e in g['visited']):raise ValueError('return proof premise missing')
 # Exact complete source has only these writes to EAX after any removal call;
 # all normal paths set1, rather than forwarding remove/delivery status.
 after=[];todo=[0x3db50b];seen=set()
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  seen.add(pc)
  if ix[pc]['mnemonic']=='ret':after.append(hex(pc))
  todo.extend(g['edges'][pc])
 parentix={int(i['pc'],16):i for r in parent['ranges'] for i in r['instructions']}
 for pc,m,a in [(0x3db371,'cmp','byte ptr [rdi + 0x10], 3'),(0x3db375,'jne','0x3db382'),(0x3db37d,'call','0x3dc0d0'),(0x3dc122,'call','0x3dbcf0')]:
  if (parentix[pc]['mnemonic'],parentix[pc]['args'])!=(m,a):raise ValueError('retained notification composition changed')
 return dict(native_carriers={'352980':'one popped integer goes toEDX; receiverRBX;R8D4; then tail3DB6E0','353660':'first popped integer savedEDI; second goes through264010 actor resolution; EDX=EDI+1; R8D4; then tail3DB6E0'},
  range='Mode4: descending channels BYTEactor88-1 down to max(0,signedEDX); initial actorWORD6 active-bit snapshot gates each channel.',
  mode_state_gate='Mode4 leaves XORzeroR14D (CMOVNE not taken for4). First nonzero BYTEentry11 reaches3DB506 without a state3 test; states1 and2 qualify as well as3.',
  multiplicity='At most one selected nonzero entry per considered channel per invocation, then DEC RBP; not a loop removing every entry on each channel.',
  notification_composition='For valid head mode3 descriptor/non8000 requester ordinal, original3DB2A0 reaches3DC0D0 regardless of incoming entry11. Cancelling state1/2 can attempt endnotification without a target interpreter call in this scoped path.',
  return='3DB420 returnsEAX1 on all normal paths including NULLreceiver/empty channel range/no selected entry; removal/notification results are not propagated. Caller tails into3DB6E0; its effects are separate.',
  revised_claim='End-notification attempt is removal completion, not a certificate that target bytecode executed RET. Whether a receipt is admitted/delivered/consumed is a separate stage.',
  extent='3DB420 first runtime-function/unwind fragment is28B; complete local304B includes3DB506 call andNULLreturn3DB545. An entry-fragment decode is invalid for this semantic claim.',
  limits='No natural shipped cancel/interleaving, successful receipt, same-key reuse, actual function completion, lifetime or tail-scheduler effects proved. Normal valid linked head/descriptor, disjoint records/frame/nativeABI/returns/stable state and flags0/1 for retained noopaque-helper countermodel required.')
def main():
 for n,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/n)!=pin:raise ValueError('reviewed dependency changed')
 x=json.loads((P/'source-01.json').read_text());s=json.loads((P/'capture-01.status.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise ValueError('required actual capture failed')
 if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py') or x['exe_sha256']!=PIN:raise ValueError('capture invocation/reference mismatch')
 pin=json.loads((P/'parent-identities.json').read_text());m=json.loads((P/'retained/manifest.json').read_text());mf={q['path']:q for q in m['members']}
 if pin['manifest_sha256']!=PARENT or sha(P/'retained/manifest.json')!=PARENT:raise ValueError('retained parent manifest changed')
 for q in pin['files']:
  if sha(P/q['path'])!=q['sha256'] or(q['path']!='retained/manifest.json' and q['sha256']!=mf[q['path'].split('/',1)[1]]['sha256']):raise ValueError('retained selected member changed')
 z=json.loads((P/'retained/prove-02.status.json').read_text());r=json.loads((P/'retained/result-01.json').read_text())
 if z.get('terminal') is not True or z.get('exit')!=0 or z.get('exception') is not None or z['driver_sha256']!=sha(P/'retained/prove.py') or r.get('producer_complete') is not True or r['driver_sha256']!=sha(P/'retained/prove.py') or not(P/'retained/prove-02.stdout').read_bytes() or(P/'retained/prove-02.stderr').read_bytes():raise ValueError('retained producer prerequisite failed')
 parent=json.loads((P/'retained/source-01.json').read_text());V=load('roles','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py')
 annotations=[V.validate(q) for q in [x,parent]]
 expected=[(0x352980,0x3529ae,'4b411f5a5e6b4f7db9a82f3780785c8ed3b47fec39989ea2ccff4b194205437c'),(0x353660,0x3536ac,'8919bfe8eac51cd7ce02c79c7002d08116742586ffe480d7b872ace03a334a9b'),(0x3db420,0x3db550,'048cdf06a3daa0c0e82fe44a632936bd536bb0d94d445f91c61f7816bcf29a06')]
 if [(int(q['start'],16),int(q['end_exclusive'],16),q['sha256']) for q in x['ranges']]!=expected:raise ValueError('original extent/source population differs')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('wrong reference')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
 secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original span')
 for q in x['ranges']+parent['ranges']:
  a,b=int(q['start'],16),int(q['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,b-a):raise ValueError('original bytes differ')
 # Retained facts remain conditional producer evidence, not silently accepted.
 R=load('retained_producer','retained/prove.py')
 if json.loads(json.dumps(R.derive(parent,G)))!=r['facts']:raise ValueError('retained current original derive disagrees')
 facts=derive(x,parent,G)
 result=dict(producer_complete=True,method='A STATIC_ONLY native cancellation selection and end-notification gate',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,
  source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['source-01.json','retained/source-01.json']],annotation_prerequisites=annotations,new_original_bytes=426,facts=facts,limits=[facts['limits'],'Published parent producer-valid only; no independent acceptance inherited.','Source code/CFG proof, no native/emulator/live execution.'],cleanup='Finite offline tools only; no PC/game/save/config/reference/peer changes.')
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise ValueError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED cancellation mode4 reaches end-notification attempt without a RET requirement; delivery/natural interleaving OPEN')
if __name__=='__main__':main()
