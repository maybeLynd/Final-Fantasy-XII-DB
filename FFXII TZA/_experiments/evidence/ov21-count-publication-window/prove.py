"""Original count-publication order/callee-effect proof. No machine-code execution or gameplay."""


import hashlib,importlib.util,json,struct,sys


from pathlib import Path


sys.dont_write_bytecode=True


P=Path(__file__).resolve().parent


ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())


sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def load(n,f):


 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:


 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')


V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')


status=json.loads((P/'capture-01.status.json').read_text())


if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')


x=json.loads((P/'source-01.json').read_text())


if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture incomplete')


roles=V.validate(x)


raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()


PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'


if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image changed')


pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]


secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]


def read(a,n):


 for vs,rva,sz,off in secs:


  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]


 raise RuntimeError('unbacked source')



RETAINED_PINS={'ov21-bank-capacity-domain': 'c78420f604a4763f41074eec85b307eea39750b008623b4b28d38bc6e9cec70b', 'ov21-page-selection-invariant': '6fab4d403a4bdaf91b6054e2525e6efe9dc8537d66e7f7e911be428fa50c9a5b', 'namebinding-callback-inputs': '940c92959f59daf104c8047b76e71956e4671efe81e5f7b20e617ab244164b9a'}

retained=[];source_pins=[{'path':'source-01.json','sha256':sha(P/'source-01.json')}]
for group in json.loads((P/'lineage.json').read_text())['retained']:
 d=P/'retained'/group['slug']
 if group['manifest_sha256']!=RETAINED_PINS[group['slug']] or sha(d/'manifest.json')!=group['manifest_sha256']:raise RuntimeError('retained manifest changed')
 manifest=json.loads((d/'manifest.json').read_text())
 for row in group['files']:
  if sha(d/row['path'])!=row['sha256']:raise RuntimeError('retained input changed')
  if row['path']!='manifest.json' and not any(m['path']==row['path'] and m['sha256']==row['sha256'] for m in manifest['members']):raise RuntimeError('unbound retained input')
 s=json.loads((d/group['capture_status']).read_text())
 if s['exit']!=0 or s['driver_sha256']!=sha(d/group['capture_driver']):raise RuntimeError('required retained capture failed')
 if not group['legacy_receipt_schema']:
  if s.get('terminal') is not True or s.get('exception') is not None or not(d/'capture-01.stdout').read_bytes() or(d/'capture-01.stderr').read_bytes():raise RuntimeError('retained terminal capture failed')
 y=json.loads((d/group['source']).read_text());V.validate(y)
 if y.get('wrapper_complete') is not True or y['invocation_driver_sha256']!=sha(d/group['capture_driver']) or y['exe_sha256']!=PIN:raise RuntimeError('retained source identity failed')
 retained.append(y);source_pins.append({'path':(d/group['source']).relative_to(P).as_posix(),'sha256':sha(d/group['source'])})
if[(r['start'],r['end_exclusive']) for r in x['ranges']]!=[('0x51fcf0','0x51fe24'),('0x3ab7f0','0x3ab853'),('0x20e620','0x20e629')]:raise RuntimeError('required source population changed')
ix={};local={}
need_ranges={0x51fbb0:0x51fce3,0x51fcf0:0x51fe24,0x51f880:0x51f9e5,0x3ab7f0:0x3ab853,0x36b130:0x36b159,0x20e620:0x20e629}
for src in [x]+retained:
 for r in src['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
  if a in need_ranges:
   if b!=need_ranges[a] or a in local:raise RuntimeError('duplicate or wrong required body')
   local[a]={int(i['pc'],16):i for i in r['instructions']};ix.update(local[a])
if set(local)!=set(need_ranges):raise RuntimeError('missing required original body')
graphs={a:G.graph(v,a,need_ranges[a]) for a,v in local.items()}
for a,g in graphs.items():
 if g['visited']!=set(local[a]):raise RuntimeError('unclosed body population')
required=[(0x51fc71,'inc','dword ptr [r14 + 0x14]'),(0x51fcb2,'inc','dword ptr [rbx + 0x58]'),
 (0x51fc92,'call','0x3ab7f0'),(0x51fd4b,'cmp','dword ptr [rdi + 0x58], 0'),
 (0x51fd4f,'jne','0x51fd59'),(0x51fd59,'mov','ecx, dword ptr [rax + 0x14]'),
 (0x51fd5c,'dec','ecx'),(0x51fd5e,'mov','dword ptr [rax + 0x14], ecx'),
 (0x51fd7c,'call','0x51f880'),(0x51fe02,'call','0x20e620'),(0x51fe0c,'dec','dword ptr [rdi + 0x58]'),
 (0x3ab82c,'call','0x36b130'),(0x36b14d,'mov','rax, qword ptr [rax + 8]'),
 (0x36b151,'add','rax, 0x40'),(0x20e620,'sub','ecx, dword ptr [rip + 0x1d74f0a]'),(0x20e626,'mov','eax, ecx'),(0x20e628,'ret','')]
for pc,m,args in required:
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise RuntimeError('required operation changed '+hex(pc))
for a,allowed in [(0x51fcf0,{'0x3ab7f0','0x51f880','0x20e620'}),(0x51f880,{'0x3ab7f0'}),(0x3ab7f0,{'0x36b130'}),(0x36b130,set()),(0x20e620,set())]:
 if {target for pc,target in graphs[a]['calls']}!=allowed:raise RuntimeError('unexpected direct callee')
# Every reachable helper is closed. No callback dispatch, indirect call or
# nonstack store exists in these readers; private frames must not alias banks.
readers=[]
for a in [0x3ab7f0,0x36b130,0x20e620]:
 writes=[]
 for pc,i in local[a].items():
  for mem in i['memory']:
   if mem['role'] in ['w','rw']:
    if mem['base']!='rsp' or mem['index'] is not None:raise RuntimeError('reader nonstack write')
    writes.append({'pc':hex(pc),'memory':mem})
 readers.append({'entry':hex(a),'private_stack_writes':writes,'calls':graphs[a]['calls']})
acquire=graphs[0x51fbb0]
release=G.graph(local[0x51fcf0],0x51fcf0,0x51fe24,fixed={0x51fd4f:True})
for g,page,total,ret in [(acquire,0x51fc71,0x51fcb2,0x51fce2),(release,0x51fd5e,0x51fe0c,0x51fe23)]:
 if not G.dominates(g,page,total) or not G.dominates(g,total,ret):raise RuntimeError('count order does not dominate successful normal return')
window_calls={name:[{'pc':hex(pc),'target':target} for pc,target in g['calls'] if lo<pc<hi]
 for name,g,lo,hi in [('acquire',acquire,0x51fc71,0x51fcb2),('release',release,0x51fd5e,0x51fe0c)]}
if {r['target'] for r in window_calls['acquire']}!={'0x3ab7f0'} or {r['target'] for r in window_calls['release']}!={'0x51f880','0x3ab7f0','0x20e620'}:raise RuntimeError('window call set changed')
# Page unlink in the release window is reached only after zero count tests.
# Its QWORD+14 clear re-clears already-zero page count and also cursor+18.
for pc in [0x51fd66,0x51fd73]:
 if(ix[pc]['mnemonic'],ix[pc]['args'])!=('test','ecx, ecx'):raise RuntimeError('empty-page predicate changed')
if (ix[0x51f94b]['mnemonic'],ix[0x51f94b]['args'])!=('mov','qword ptr [rdi + 0x14], rax'):raise RuntimeError('page reset changed')
mem=ix[0x51f94b]['memory'][0]
if mem['role']!='w' or mem['size']!=8 or mem['displacement']!=0x14:raise RuntimeError('page count/cursor overlap changed')
transitions=[{'operation':'acquire lastfree','entry':{'global':319,'page_sum':319},'after_page':{'global':319,'page_sum':320,'difference':-1},'after_total':{'global':320,'page_sum':320,'difference':0}},
 {'operation':'release full','entry':{'global':320,'page_sum':320},'after_page':{'global':320,'page_sum':319,'difference':1},'after_total':{'global':319,'page_sum':319,'difference':0}}]
for t in transitions:
 for phase in ['after_page','after_total']:
  d=t[phase]
  if d['global']-d['page_sum']!=d['difference']:raise RuntimeError('count arithmetic inconsistent')
result={'producer_complete':True,'method':'A STATIC_ONLY original count order and closed direct callee graph','driver_sha256':sha(Path(__file__)),
 'source_pins':source_pins,'annotation_prerequisites':[roles],'instruction_assertions':len(required),
 'graphs':[{'entry':hex(a),'instructions':len(g['visited']),'returns':[hex(q) for q in g['returns']],'calls':g['calls']} for a,g in graphs.items()],
 'window_calls':window_calls,'reader_effects':readers,'count_transition_calculations':transitions,
 'answer':'Page count is published before total count on acquire and release. Their equality is not maintained at every instruction. The complete intervening direct-call graph contains page unlink and reader-only pointer/base helpers, no callback/indirect dispatch. It does not establish absence of other-thread/asynchronous interference.',
 'observation_requirement':'Bind bank identity, acquisition/release phase and coherent entry/return or stopped transition. Asynchronous separate count reads are not atomic; a one-count mismatch at an interior point is not sufficient evidence of persistent corruption.',
 'arena_helper':'20E620 subtracts DWORD arena base01F83530 fromECX andreturnsEAX, no RNG or nativeallocation; statichelper doesnot prove runtimearena value.',
 'limitations':['No original machine/native/live execution; transitions are source arithmetic, not captured events',
 'Valid live slot/page, initialized bank, no underflow/overflow, stable table/handle identity, private stack disjointness and no interfering writes required',
 'Direct callee graph cannot itself establish thread ownership, scheduling, asynchronous reentry, natural caller reachability or atomicity',
 'Release original used!=0 gate is not positivity/valid-index checking; malformed negative/duplicate/free inputs are not asserted safe',
 'Legacy namebinding capture receipt lacks terminal/exception fields; retained originalbytes are revalidated directly here, no new execution/live credit',
 'Allwriter/list invariance, actual startup/arena binding, authored keys, naturalexhaustion/samekey ownership andwholeOV21 remainOPEN']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED page-before-total count stores and closed intervening callback-free direct graph; no native/game')
