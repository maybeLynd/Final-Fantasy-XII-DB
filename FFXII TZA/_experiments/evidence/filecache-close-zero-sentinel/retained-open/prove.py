"""Static exhaustive predicate partitions; no original-code execution."""
import hashlib,importlib.util,itertools,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';MASK=(1<<64)-1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def getter(ix,G):
 expected=[(0x59d920,'cmp','qword ptr [rcx + 0x28], -1'),(0x59d925,'jne','0x59d938'),(0x59d927,'cmp','qword ptr [rcx + 0x30], 0'),(0x59d92c,'jne','0x59d938'),(0x59d92e,'cmp','qword ptr [rcx + 0x40], -1'),(0x59d933,'jne','0x59d938'),(0x59d935,'xor','al, al'),(0x59d937,'ret',''),(0x59d938,'mov','al, 1'),(0x59d93a,'ret','')]
 if set(ix)!=set(pc for pc,m,a in expected):raise RuntimeError('getter population changed')
 for pc,m,a in expected:
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('getter predicate changed '+hex(pc))
 for pc,offset in [(0x59d920,0x28),(0x59d927,0x30),(0x59d92e,0x40)]:
  mem=ix[pc]['memory']
  if len(mem)!=1 or (mem[0]['base'],mem[0]['displacement'],mem[0]['size'],mem[0]['role'],mem[0]['index'] or None)!=('rcx',offset,8,'r',None):raise RuntimeError('getter predicate width/role changed')
 g=G.graph(ix,0x59d920,0x59d93b)
 if g['visited']!=set(ix) or g['calls'] or g['returns']!=[0x59d937,0x59d93a]:raise RuntimeError('getter CFG changed')
 checks=[(0x28,MASK),(0x30,0),(0x40,MASK)]
 rows=[]
 for eq in itertools.product([False,True],repeat=3):
  # Every64-bit field belongs to one equality class for its original immediate.
  fields={o:(imm if same else imm^1) for (o,imm),same in zip(checks,eq)}
  path=[];al=None;pc=0x59d920;zero=None
  for steps in range(10):
   path.append(hex(pc));i=ix[pc];m=i['mnemonic']
   if m=='cmp':
    mem=i['memory'][0];imm=int(i['args'].rsplit(', ',1)[1],0)&MASK;zero=fields[mem['displacement']]==imm;pc=g['edges'][pc][0]
   elif m=='jne':pc=g['edges'][pc][1 if zero else 0]
   elif m=='xor':al=0;pc=g['edges'][pc][0]
   elif m=='mov':al=1;pc=g['edges'][pc][0]
   elif m=='ret':break
   else:raise RuntimeError('unmodeled getter instruction')
  else:raise RuntimeError('static getter path did not terminate')
  want=0 if all(eq) else 1
  if al!=want:raise RuntimeError('getter equality partition disagrees')
  rows.append({'equal_to_sentinels':list(eq),'AL':al,'source_path':path})
 # The distinguishing zero state has cmp40,-1 false, regardless of the otherfields.
 zero_case=next(r for r in rows if r['equal_to_sentinels']==[True,True,False])
 if zero_case['AL']!=1 or '0x59d933' not in zero_case['source_path'] or '0x59d938' not in zero_case['source_path']:raise RuntimeError('zero-cache-view discriminator lost')
 return {'formula':'AL = !(QWORD28 == FFFFFFFFFFFFFFFF && QWORD30 == 0 && QWORD40 == FFFFFFFFFFFFFFFF)','logical_partitions':rows,'zero_view_witness':{'QWORD28':MASK,'QWORD30':0,'QWORD40':0,'AL':1,'source_path':zero_case['source_path']},'return_width':'OnlyAL is written on both return arms; no fullRAX clean0/1 claim','limits':'Eight exhaustive equality classes are static proof partitions, not eight native/game/harness runs. Valid readablefield bytes/private code/frame required; no actual caller or backing validity observed.'}
def main():
 for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864'),('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497')]:
  if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
 s=json.loads((P/'capture-01.status.json').read_text());x=json.loads((P/'source-01.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required getter capture failed')
 if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise RuntimeError('actual getter capture incomplete')
 parents=json.loads((P/'parent-identities.json').read_text());required={'filecache-source-key-initialization':'d5cc7655d068357ee5bd9496b5674f82d4e4679d30d12356ba5411d8b713350e','filecache-zero-handle-return':'93e2351f2132231d53da0597dbef418c7870e0a795e04e0090c4e5089c93c521'}
 if {p['slug']:p['manifest_sha256'] for p in parents}!=required or len(parents)!=2:raise RuntimeError('retained parent population changed')
 for p in parents:
  d=P/'parents'/p['slug'];result='result-02.json' if p['slug']=='filecache-source-key-initialization' else 'result-01.json'
  s=json.loads((d/'prove-02.status.json').read_text());v=json.loads((d/result).read_text())
  if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(d/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(d/'prove.py'):raise RuntimeError('required retained parent producer incomplete')
  if sha(d/'manifest.json')!=p['manifest_sha256']:raise RuntimeError('retained manifest changed')
  mf={m['path']:m for m in json.loads((d/'manifest.json').read_text())['members']}
  for r in p['files']:
   if sha(d/r['path'])!=r['sha256'] or(r['path']!='manifest.json' and r['sha256']!=mf[r['path']]['sha256']):raise RuntimeError('retained parent identity changed')
 names=['source-01.json','parents/filecache-source-key-initialization/source-01.json','parents/filecache-zero-handle-return/retained/source-01.json'];sources=[json.loads((P/n).read_text()) for n in names]
 V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');annotations=[V.validate(v) for v in sources]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise RuntimeError('unbacked original range')
 ix={};graphs={}
 for x in sources:
  if x.get('wrapper_complete') is not True or x['exe_sha256']!=PIN:raise RuntimeError('required original source incomplete')
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);local={int(i['pc'],16):i for i in r['instructions']}
   if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
   g=G.graph(local,a,b)
   if g['visited']!=set(local):raise RuntimeError('retained CFG incomplete')
   ix.update(local);graphs[a]=g
 facts=getter({pc:i for pc,i in ix.items() if 0x59d920<=pc<0x59d93b},G)
 def need(pc,m,a):
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('composed sentinel state operation changed '+hex(pc))
 for pc,m,a in [(0x597984,'xor','ebp, ebp'),(0x597986,'mov','qword ptr [rcx + 0x28], 0xffffffffffffffff'),(0x597994,'mov','qword ptr [rcx + 0x30], rbp'),(0x597998,'mov','rdi, rcx'),(0x59799b,'mov','qword ptr [rcx + 0x40], 0xffffffffffffffff'),(0x5979b2,'add','rcx, 0x20'),(0x5979b6,'call','0x59ee90'),(0x59eec4,'mov','r15, rcx'),(0x59efe5,'call','0x1d6d20'),(0x59efea,'mov','qword ptr [r15 + 0x20], rax'),(0x59efee,'test','rax, rax'),(0x59eff1,'js','0x59f000'),(0x59effb,'jmp','0x59f1d6'),(0x597a09,'mov','rax, rdi')]:need(pc,m,a)
 ctor=graphs[0x597970];resolver=graphs[0x59ee90]
 for a in [0x597984,0x597986,0x597994,0x59799b,0x5979b2]:
  if not G.dominates(ctor,a,0x5979b6):raise RuntimeError('constructor state order changed')
 # All later own constructor writes are disjoint the three getter fields.
 for pc,i in ix.items():
  if 0x5979bb<=pc<0x597a12:
   for m in i['memory']:
    if m['base']=='rdi' and m['role'] in ['w','rw'] and any(m['displacement']<b and a<m['displacement']+m['size'] for a,b in [(0x28,0x30),(0x30,0x38),(0x40,0x48)]):raise RuntimeError('later constructor overwrites backing fields')
 # Supplied prefix makes no own write to source+8/+10 before lookup.
 for pc,i in ix.items():
  if 0x59ee90<=pc<0x59efe5:
   for m in i['memory']:
    if m['base']=='r15' and m['role'] in ['w','rw'] and m['displacement']<0x18 and 8<m['displacement']+m['size']:raise RuntimeError('resolver prefix changes other backing fields')
 g=G.graph(ix,0x59ee90,0x59f1fc,fixed={0x59eff1:False})
 def reached(start):
  seen=set();todo=[start]
  while todo:
   pc=todo.pop()
   if pc in seen:continue
   seen.add(pc);todo.extend(g['edges'][pc])
  return seen
 post=reached(0x59efea)
 if any(ix[pc]['mnemonic']=='call' and pc!=0x59f1dd for pc in post):raise RuntimeError('new post-zero native boundary')
 for pc in post:
  for m in ix[pc]['memory']:
   if m['base']=='r15' and m['role'] in ['w','rw'] and m['displacement']<0x28 and 8<m['displacement']+m['size'] and pc!=0x59efea:raise RuntimeError('post-zero changes backing fields')
 facts['conditional_composition']={'constructor':'597970 receiver+20 ->59EE90 R15','cache_zero_source':'retained checked normalNULL path produceslookupRAX0;59EFEA stores source20=reader40 zero','other_fields':'constructor reader28=FFFFFFFFFFFFFFFF/30=0; own prefix/post/late-constructor backing-write checks preserve under ABI/noalias/noopaqueinterference','then_IsOpen':'On reached later getter with this preserved state AL1 despite zero cacheview','consumer_qualification':'Open means sentinel disjunction, not valid/nonnull cacheview certification; constructor returnsobjectRAX, resolverstatus0 distinct. No actual later getter trigger or naturalfailure proved.'}
 result={'producer_complete':True,'method':'A STATIC_ONLY original IsOpen sentinel invariant and conditional zero-view composition','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'source_pins':[{'path':n,'sha256':sha(P/n)} for n in names],'annotation_prerequisites':annotations,'parent_identities':parents,'new_original_bytes':27,'facts':facts,'limits':['Static equality partitions and composed conditional state, not native/original-code emulation/live execution.','Retained parents producer-valid at retention, independent acceptance/canonical consumption pending.','Validrecord/readableQWORDfields/nonalias/privateframes/nativeABI/normalreturns, reachedlookupcachepath and noopaqueinterference/successfulcookie prerequisites.','No naturalheapfailure/actuallatergetter/validview lifetime/readconsequence/allwriter/atomicity/scheduling proof. AL return only; upperRAX unassigned.'],'cleanup':'Own bounded offline tools only; no game/PC/instrument/save/config/reference/peer changes.'}
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise RuntimeError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED original IsOpen sentinel predicate accepts conditionalzero cacheview; STATIC_ONLY, no naturalfault claim')
if __name__=='__main__':main()
