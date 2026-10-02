"""Original control/dataflow proof; no reconstructed/native/game execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(source,G):
 ix={int(i['pc'],16):i for r in source['ranges'] for i in r['instructions']}
 graphs={int(r['start'],16):G.graph(ix,int(r['start'],16),int(r['end_exclusive'],16)) for r in source['ranges']}
 for r in source['ranges']:
  g=graphs[int(r['start'],16)]
  if g['visited']!={int(i['pc'],16) for i in r['instructions']}:raise ValueError('incomplete selected local CFG')
 def need(pc,m,a):
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('required operation changed '+hex(pc))
 for op in [
  (0x3db2aa,'movsxd','rsi, edx'),(0x3db2ad,'mov','rbx, rcx'),
  (0x3db2d7,'mov','rax, qword ptr [rbx + 0xa0]'),(0x3db2de,'lea','rcx, [rsi + rsi*4]'),(0x3db2e2,'lea','rdi, [rax + rcx*4]'),
  (0x3db2ea,'movzx','r14d, byte ptr [rdi + 0x12]'),(0x3db2ef,'and','r14d, 1'),
  (0x3db2f8,'cmp','byte ptr [rdi + 0x10], 4'),(0x3db2fe,'movsx','rbp, byte ptr [rdi + 2]'),
  (0x3db307,'movzx','ecx, byte ptr [rbp + rbx + 0x94]'),(0x3db32b,'cmp','esi, eax'),
  (0x3db346,'call','0x3dc1b0'),(0x3db366,'mov','eax, 0x8000'),(0x3db36b,'cmp','word ptr [rdi + 6], ax'),
  (0x3db371,'cmp','byte ptr [rdi + 0x10], 3'),(0x3db377,'mov','rdx, rdi'),(0x3db37a,'mov','rcx, rbx'),
  (0x3db37d,'call','0x3dc0d0'),(0x3db382,'movzx','eax, byte ptr [rdi + 0x12]'),
  (0x3db386,'cmp','al, 2'),(0x3db388,'jb','0x3db397'),(0x3db392,'call','0x263050'),
  (0x3db3e6,'movzx','edx, byte ptr [rbx + 0x60]'),(0x3db3ea,'mov','r8d, esi'),(0x3db3ed,'mov','rcx, rbx'),
  (0x3db3f0,'call','0x3db650'),(0x3db3f5,'or','byte ptr [rbx + 0x63], 2'),(0x3db3f9,'mov','byte ptr [rbx + 0x60], sil'),
  (0x3db402,'mov','eax, r14d'),
  (0x3dc0d6,'mov','rbx, rdx'),(0x3dc0d9,'movzx','edx, word ptr [rdx + 6]'),(0x3dc0dd,'mov','ecx, dword ptr [rbx + 8]'),
  (0x3dc0e0,'call','0x3587c0'),(0x3dc0e5,'test','rax, rax'),(0x3dc0e8,'je','0x3dc127'),
  (0x3dc10b,'mov','rcx, rax'),(0x3dc10e,'mov','word ptr [rsp + 0x20], 0x402'),
  (0x3dc115,'mov','dword ptr [rsp + 0x24], 0x80000000'),(0x3dc11d,'mov','byte ptr [rsp + 0x28], 1'),
  (0x3dc122,'call','0x3dbcf0'),(0x3dc127,'add','rsp, 0x40'),(0x3dc12b,'pop','rbx'),(0x3dc12c,'ret',''),
  (0x3dbcfa,'mov','rax, qword ptr [rcx + 0x48]'),(0x3dbd01,'movzx','r9d, word ptr [rdx + 4]'),
  (0x3dbd0c,'cmp','r9d, dword ptr [rax]'),(0x3dbd0f,'jb','0x3dbd21'),
  (0x3dbd11,'mov','eax, 3'),(0x3dbd26,'movzx','edi, byte ptr [rcx + 0x60]'),(0x3dbd2a,'cmp','edi, 0xff'),
  (0x3dbd30,'jne','0x3dbd47'),(0x3dbd32,'mov','eax, 2'),(0x3dbd46,'ret',''),
  (0x3dbd4e,'call','0x3dc130'),(0x3dbd5f,'call','0x3db7a0'),
  (0x3dc1ca,'mov','rax, qword ptr [rcx + 0xa0]'),(0x3dc1d1,'lea','r8, [rax + rax*4]'),
  (0x3dc220,'mov','byte ptr [rax + 1], r11b'),(0x3dc230,'mov','byte ptr [r10], cl'),(0x3dc233,'mov','byte ptr [r8 + 0x11], 0'),
  (0x263ff3,'lea','rcx, [rip + 0x1e34e16]'),(0x263ffa,'imul','rax, rax, 0x288'),
  (0x3587c9,'call','0x263ff0'),(0x3587df,'mov','rax, qword ptr [rcx + rbx*8 + 8]'),
  (0x3db6c3,'mov','byte ptr [r8 + 1], 0xff'),(0x3db6cd,'mov','byte ptr [r10 + 1], r11b'),(0x3db6d1,'mov','byte ptr [r8], dl')
 ]:need(*op)
 def ownwrites(entry):
  return [(hex(pc),m['base'],m['displacement'],m['size'],m['role']) for pc in sorted(graphs[entry]['visited']) for m in ix[pc]['memory'] if m['role'] in ('w','rw') and m['base']!='rsp']
 # The unhook writes entry/neighbour links and state, not actor+60. Those
 # pointer identities require the valid/disjoint pool premise; not every alias.
 want=[('0x3dc220','rax',1,1,'w'),('0x3dc230','r10',0,1,'w'),('0x3dc233','r8',0x11,1,'w')]
 if ownwrites(0x3dc1b0)!=want or graphs[0x3dc1b0]['calls']:raise ValueError('unlink effect boundary changed')
 for a in [0x3db550,0x263ff0,0x3587c0]:
  if ownwrites(a):raise ValueError('lookup/helper acquired nonstack write')
 if graphs[0x3587c0]['calls']!=[(0x3587c9,'0x263ff0')]:raise ValueError('requester resolver closure changed')
 if ix[0x263ff3]['memory'][0]['rip_target']!='0x2098e10':raise ValueError('manager root changed')
 remove=graphs[0x3db2a0]
 headwrites=[pc for pc in remove['visited'] for m in ix[pc]['memory'] if m['role'] in ('w','rw') and m['base']=='rbx' and m['displacement']<=0x60<m['displacement']+m['size']]
 if sorted(headwrites)!=[0x3db3f9]:raise ValueError('extra own free-head mutation')
 if not G.dominates(remove,0x3db3f0,0x3db3f9):raise ValueError('free link insertion lost before head publish')
 def closure(g,start):
  seen=set();todo=[start]
  while todo:
   pc=todo.pop()
   if pc in seen:continue
   seen.add(pc);todo.extend(g['edges'][pc])
  return seen
 after=closure(remove,0x3db382)
 if 0x3db3f9 not in after or 0x3db37d in after:raise ValueError('post/free order changed')
 # Every normal local path after posting passes this free-head store. A
 # hypothetical reference helper must return normally; its effects aren't proven.
 todo=[0x3db382];seen=set()
 while todo:
  pc=todo.pop()
  if pc==0x3db3f9 or pc in seen:continue
  if ix[pc]['mnemonic']=='ret':raise ValueError('post returns without later free publication')
  seen.add(pc);todo.extend(remove['edges'][pc])
 # Concrete conditional discriminator needs no opaque reference helper:
 # linked channel head, mode3, valid requester ordinal, flags0/1 skip 263050.
 fixed={0x3db2b6:True,0x3db2d5:False,0x3db2fc:False,0x3db305:False,
        0x3db320:False,0x3db32d:True,0x3db34d:True,0x3db36f:False,0x3db375:False,0x3db388:True}
 eligible=G.graph(ix,0x3db2a0,0x3db41a,fixed=fixed)
 if [c for c in eligible['calls'] if c[1]!='0x3db650']!=[(0x3db346,'0x3dc1b0'),(0x3db37d,'0x3dc0d0')]:raise ValueError('eligible before/free path gained unproved call')
 if not G.dominates(eligible,0x3db37d,0x3db3f9):raise ValueError('eligible removal can free before post')
 post=graphs[0x3dc0d0]
 if ownwrites(0x3dc0d0) or post['calls']!=[(0x3dc0e0,'0x3587c0'),(0x3dc122,'0x3dbcf0')]:raise ValueError('post boundary effects changed')
 if closure(post,0x3dc127)!={0x3dc127,0x3dc12b,0x3dc12c}:raise ValueError('post gained recovery/return rewrite')
 partitions=[]
 for function0_valid,free in [(False,None),(True,False),(True,True)]:
  fixed={0x3dbd0f:function0_valid}
  if free is not None:fixed[0x3dbd30]=free
  g=G.graph(ix,0x3dbcf0,0x3dbdb2,fixed=fixed)
  if not function0_valid or not free:
   if g['calls']:raise ValueError('reject path acquired calls')
   nonstack=[m for pc in g['visited'] for m in ix[pc]['memory'] if m['role'] in ('w','rw') and m['base']!='rsp']
   if nonstack:raise ValueError('rejection path mutates actor or entry')
   value=3 if not function0_valid else 2
   resultpc=0x3dbd11 if not function0_valid else 0x3dbd32
   if resultpc not in g['visited']:raise ValueError('wrong reject arm')
   outcome='EAX='+str(value)+', no own object writes/no calls'
  else:
   if (0x3dbd4e,'0x3dc130') not in g['calls'] or (0x3dbd5f,'0x3db7a0') not in g['calls']:raise ValueError('spare slot positive discriminator lost')
   outcome='reaches original unlink/insertion helpers; result/effects not established here'
  partitions.append(dict(function0_valid=function0_valid,has_free_slot=free,outcome=outcome,source_calls=[hex(pc) for pc,target in g['calls']]))
 return dict(order=['003DB346 unlink channel entry/clear entry+11','003DB37D ->003DC122 attempt end notification','003DB3F0 relink removed index onto current free list','003DB3F9 publish removed index as actor+60'],
   unlink_own_effects=want,allocation_partitions=partitions,
   descriptor_function_id='WORD0 at descriptor+4 from DWORD80000000; count>0 required before capacity rejection',
   conditional_self_full=('For a valid head mode3 entry whose requester resolves to the same actor, positive function count, '
     'free headFF, flags byte0/1, stable disjoint actor/pool/frame and normal ABI/returns: end-notification allocation returns2 '
     'before the removed entry becomes allocatable. This is a conditional original-code proof, not a naturally observed full pool.'),
   outer_return='EAX at003DB402 is entry+12 bit0 retained inR14D, independent of ignored notification allocation result. Flags1 gives return1 even in the conditional lost-notification path.',
   observer_implication='A free slot seen after removal cannot prove it existed at notification allocation. Capture requester identity/free head at003DBD26/32 and call origin003DC127, not only post-removal occupancy.',
   excluded='No natural full-pool/same-actor request/cancel-reentry occurrence, universal entry lifetime, concurrent mutation, all writer, native helper or imported effect proof. Flags>=2 additionally cross263050 and need its effect/noninterference proof.')
def main():
 for name,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/name)!=pin:raise ValueError('reviewed dependency changed')
 status=json.loads((P/'capture-01.status.json').read_text());source=json.loads((P/'source-01.json').read_text())
 if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status.get('driver_sha256')!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise ValueError('required capture failed/incomplete')
 if source.get('wrapper_complete') is not True or source.get('invocation_driver_sha256')!=sha(P/'capture.py') or source['driver_sha256']!=sha(P/'capture-index-path.py'):raise ValueError('actual capture invocation mismatch')
 receipt=json.loads((P/'retained-manifest.status.json').read_text())
 if receipt.get('terminal') is not True or receipt.get('exit')!=0 or receipt['stdout_sha256']!=sha(P/'retained-manifest.stdout') or receipt['stderr_sha256']!=sha(P/'retained-manifest.stderr'):raise ValueError('retained input receipt failed/stale')
 retained=json.loads((P/'retained-manifest.stdout').read_text());selected=json.loads((P/'retained-body-identities.json').read_text())
 entries=['00263FF0','003587C0','003DB2A0','003DB550','003DB650','003DBCF0','003DC0D0','003DC1B0']
 if selected['bodies']!=[next(b for b in retained['bodies'] if b['entry']==a) for a in entries] or selected['exe_sha256']!=PIN:raise ValueError('body identities changed')
 if len(source['ranges'])!=8 or source['exe_sha256']!=PIN:raise ValueError('missing original body population')
 data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('wrong reference image')
 pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
 secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked reference span')
 for b,r in zip(selected['bodies'],source['ranges']):
  a=int(b['entry'],16);blob=bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
  if (int(r['start'],16),int(r['end_exclusive'],16),r['sha256'])!=(a,a+b['length'],b['sha256']) or blob!=read(a,b['length']):raise ValueError('reference/retained code mismatch')
 V=load('reviewed_roles','validate-title-source-annotations.py');G=load('reviewed_cfg','prove_owner_reload_order.py')
 annotations=V.validate(source);facts=derive(source,G)
 result=dict(producer_complete=True,method='A STATIC_ONLY original notification-before-entry-reclaim proof',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,
  source_pins=[dict(path='source-01.json',sha256=sha(P/'source-01.json'))],annotation_prerequisites=[annotations],original_body_bytes=sum(b['length'] for b in selected['bodies']),facts=facts,
  limits=[facts['excluded'],'Normal initialized valid records/linked head/private frames/ABI and disjoint actor, entry pool and caller stack required. No native or game experiment performed.','Static graph partitions are proofs of control-flow boundaries, not calls with injected state or independent project acceptance.'],cleanup='Finite offline tools only; no PC/game/native/emulator/instrument/save/config/reference/peer writes.')
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise ValueError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
 print('PROVED post-before-reclaim and conditional full self-notification refusal; natural occurrence remains OPEN')
if __name__=='__main__':main()
