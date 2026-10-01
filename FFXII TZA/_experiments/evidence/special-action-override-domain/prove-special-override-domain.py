"""Conditional override-domain induction grounded in the original constructor/control.
Not complete alias/writer closure or natural initialized-process evidence.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable result exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';b=exe.read_bytes()
if sha(exe)!=pin:raise ValueError('original image prerequisite')
pe=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,pe+20)[0]
secs=[struct.unpack_from('<IIII',b,pe+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,pe+6)[0])]
def read(a,n):
 for vs,va,rs,ro in secs:
  if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
 raise ValueError('unbacked image span')
records={};inputs=[];captures={}
for name,driver in [('special-override-control-raw-01.json','capture-special-override-control.py'),
                    ('special-override-constructor-raw-01.json','capture-special-override-constructor.py')]:
 r=json.loads((W/name).read_text());captures[name]=r
 if r['exe_sha256']!=pin or r['driver_sha256']!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver) or r.get('wrapper_complete') is not True:raise ValueError('capture invocation prerequisite')
 if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):raise ValueError('capture role prerequisite')
 for s in r['ranges']:
  orig=read(int(s['start'],16),int(s['end_exclusive'],16)-int(s['start'],16))
  if hashlib.sha256(orig).hexdigest()!=s['sha256']:raise ValueError('original span prerequisite')
  for i in s['instructions']:
   pc=int(i['pc'],16)
   if bytes.fromhex(i['bytes'])!=read(pc,len(bytes.fromhex(i['bytes']))):raise ValueError('instruction prerequisite')
   if pc in records and records[pc]!=i:raise ValueError('source disagreement')
   records[pc]=i
 inputs.append(dict(path=name,sha256=sha(W/name),driver=driver,driver_sha256=sha(W/driver)))
required={0x1ccb42:('mov','rdi, rcx'),0x1ccc06:('mov','qword ptr [rdi + 0xadc], 0x2710'),
 0x1d2dd3:('mov','eax, dword ptr [rdi + 0xae0]'),0x1d2dd9:('test','bl, bl'),
 0x1d2ddb:('je','0x1d2de5'),0x1d2ddd:('test','eax, eax'),0x1d2ddf:('jle','0x1d2df2'),
 0x1d2de1:('dec','eax'),0x1d2de3:('jmp','0x1d2dec'),0x1d2de5:('cmp','eax, 8'),
 0x1d2de8:('jge','0x1d2df2'),0x1d2dea:('inc','eax'),
 0x1d2dec:('mov','dword ptr [rdi + 0xae0], eax'),0x1d2df2:('mov','ecx, dword ptr [rdi + 0xae0]'),
 0x1d2df8:('dec','ecx'),0x1d2dfa:('call','0x2f7a00'),
 0x2f7a00:('mov','dword ptr [rip + 0x1bf40ea], ecx'),0x2f7a06:('ret',''),
 0x2f79e0:('movdqa','xmm0, xmmword ptr [rip + 0xa17ff8]'),
 0x2f79e8:('movdqu','xmmword ptr [rip + 0x1fc6f40], xmm0'),0x2f79f0:('ret','')}
def witnesses(rr):
 for pc,e in required.items():
  if pc not in rr or (rr[pc]['mnemonic'],rr[pc]['args'])!=e:raise ValueError('override-domain source witness changed')
witnesses(records)
store=records[0x1ccc06]['memory'][0]
if (store['displacement'],store['size'],store['role'])!=(0xadc,8,'w'):raise ValueError('constructor width coverage')
initial=(0x2710>>32)&0xffffffff
if initial!=0:raise ValueError('constructor AE0 high-dword effect')
rc=captures['special-override-control-raw-01.json'];constant=read(0xd0f9e0,16);words=list(struct.unpack('<8H',constant))
if rc['initializer_constant']['bytes']!=constant.hex() or rc['initializer_constant']['words']!=words or records[0x2f79e8]['memory'][0]['rip_target']!='0x22be930':raise ValueError('initializer original identity')
if records[0x2f7a00]['memory'][0]['rip_target']!='0x1eebaf0':raise ValueError('override-index identity')
def step(x,left):return x-1 if left and x>0 else x+1 if not left and x<8 else x
transitions=[dict(before=x,left=left,after=step(x,left),written_index=step(x,left)-1) for x in range(9) for left in [False,True]]
if any(not 0<=t['after']<=8 or not -1<=t['written_index']<=7 for t in transitions):raise ValueError('bounded induction fails')
if any(w in range(511,535) for w in words):raise ValueError('initialized override contains candidate')
controls=dict(constructor_high_dword_zero=initial==0,
              zero_left_saturates=step(0,True)==0,eight_right_saturates=step(8,False)==8,
              off_maps_to_negative_index=step(0,True)-1==-1,
              initial_domain_required=step(9,False)==9 and step(9,False)-1==8)
bad={pc:dict(i) for pc,i in records.items()};bad[0x1ccc06]['args']='dword ptr [rdi + 0xadc], 0x2710'
try:witnesses(bad)
except ValueError:controls['narrowed_constructor_store_refused']=True
else:raise ValueError('wrong constructor width accepted')
bad={pc:dict(i) for pc,i in records.items()};bad[0x1d2de5]['args']='eax, 9'
try:witnesses(bad)
except ValueError:controls['widened_control_bound_refused']=True
else:raise ValueError('wrong control bound accepted')
result=dict(question='What initialized values and control-state invariant does the original special-action override provide, and do they exclude candidate511..534?',
 hypotheses=['override control can normally choose an arbitrary u16 action','under its initialized state and unchanged eight-word table it selects OFF or one of eight fixed safe ids'],
 method='A original constructor width, initializer constant and finite transition induction; no code execution/live state',
 exe_sha256=pin,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,controls=controls,
 constructor_initial_ae0=initial,initializer_words=words,transitions=transitions,
 established='Constructor original qword store at+ADC gives high dword+AE0 zero at that instruction. Under no intervening overwrite, control arm preserves0..8 and writes override index-1..7. Eight initializer words241,231,234,237,229,228,227,226 cannot produce511..534.',
 unresolved='Complete no-overwrite/alias/lifetime proof for constructor completion and control field; global index indirect writers and eight-word array writes; non-debug caller/object provenance; other action-id producers. File-backed index-1 is separately only a file value.',
 limits='Conditional induction and immediate original store effects. Known direct first-section caller discovery is bounded, not all indirect caller/write closure. Initial corruption9 stays9 and sends index8, so the control is not a sanitizer for arbitrary state. No universal/natural OV42 exclusion inferred. External EXP190 replay corroboration is not an execution by ASTRA or proof of unstubbed initialization.')
if not all(controls.values()):raise ValueError('control failure')
out.write_text(json.dumps(result,indent=2)+'\n')
print('ESTABLISHED conditional override invariant: initialized0..8 -> index-1..7 and eight safe constants; full write closure OPEN')
