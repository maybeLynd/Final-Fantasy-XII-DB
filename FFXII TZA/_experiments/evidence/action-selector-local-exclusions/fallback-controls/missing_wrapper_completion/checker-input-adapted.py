"""OV42: bound the actual original matcher's fallback result by load width.
The separate nonnegative override path is deliberately left unresolved.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\Tools\\work\\ASTRA\\runtime-residue-method-retriage\\fallback-prerequisite-controls-01\\missing_wrapper_completion');ROOT=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline')
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
records={};inputs=[]
for name,driver in [('special-selection-dispatch-raw-02.json','capture-special-selection-dispatch.py'),
                    ('spattack-leaves-and-guard-raw-01.json','capture-spattack-leaves-and-guard.py')]:
 r=json.loads((W/name).read_text())
 if r['exe_sha256']!=pin or r['driver_sha256']!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver):raise ValueError('capture invocation prerequisite')
 if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):raise ValueError('capture role prerequisite')
 if name.endswith('raw-02.json'):
  if r.get('wrapper_complete') is not True or r['jump_table'].get('entries')!=6:raise ValueError('dispatch wrapper prerequisite')
  jt=r['jump_table'];actual=read(0x306af0,24)
  if actual.hex()!=jt['bytes'] or jt['targets']!=[hex(0x120000+x) for x in struct.unpack('<6I',actual)]:raise ValueError('dispatch table prerequisite')
 for s in r['ranges']:
  source=read(int(s['start'],16),int(s['end_exclusive'],16)-int(s['start'],16))
  if hashlib.sha256(source).hexdigest()!=s['sha256']:raise ValueError('source span prerequisite')
  for i in s['instructions']:
   pc=int(i['pc'],16)
   if bytes.fromhex(i['bytes'])!=read(pc,len(bytes.fromhex(i['bytes']))):raise ValueError('instruction prerequisite')
   if pc in records and records[pc]!=i:raise ValueError('overlapping evidence disagrees')
   records[pc]=i
 inputs.append(dict(path=name,sha256=sha(W/name),driver=driver,driver_sha256=sha(W/driver)))
required={0x2f8d66:('movsxd','rax, dword ptr [rip + 0x1bf2d83]'),
 0x2f8d70:('test','eax, eax'),0x2f8d72:('js','0x2f8d85'),
 0x2f8d7b:('movzx','eax, word ptr [rcx + rax*2]'),0x2f8d84:('ret',''),
 0x2f8da6:('js','0x2f8e23'),0x2f8e08:('jb','0x2f8e19'),
 0x2f8e19:('cmp','edx, 3'),0x2f8e1c:('je','0x2f8e36'),
 0x2f8e21:('jns','0x2f8db0'),0x2f8e28:('or','eax, 0xffffffff'),
 0x2f8e35:('ret',''),0x2f8e36:('movzx','eax, byte ptr [r10]'),
 0x2f8e3a:('mov','rbx, qword ptr [rsp + 0x30]'),0x2f8e3f:('mov','rdi, qword ptr [rsp + 0x38]'),
 0x2f8e44:('add','rsp, 0x20'),0x2f8e48:('pop','rsi'),0x2f8e49:('ret',''),
 0x30dc55:('call','0x2f8d60'),0x30dc5a:('movzx','edi, ax'),
 0x30dc68:('call','0x322c50'),0x30dc6f:('je','0x30dc83'),
 0x30dc71:('mov','eax, 0xffff'),0x30dc76:('cmp','di, ax'),
 0x30dc79:('je','0x30dc83'),0x30dc7b:('lea','eax, [rbx - 0xd0]'),
 0x3067aa:('mov','eax, dword ptr [rip + 0x1fbb9ac]'),
 0x3067b0:('dec','eax'),0x3067b7:('cmp','eax, 5'),0x3067ba:('ja','0x306a9a')}
def witnesses(rr):
 for pc,e in required.items():
  if pc not in rr or (rr[pc]['mnemonic'],rr[pc]['args'])!=e:raise ValueError('fallback source witness changed')
witnesses(records)
if records[0x2f8d66]['memory'][0]['rip_target']!='0x1eebaf0' or records[0x2f8d74]['memory'][0]['rip_target']!='0x22be930' or records[0x2f8d85]['memory'][0]['rip_target']!='0x2ebf0a0':raise ValueError('matcher object identity')
# A complete original matcher capture is required for its three RET exits.
r=json.loads((W/'special-selection-dispatch-raw-02.json').read_text())
s=next(s for s in r['ranges'] if s['start']=='0x2f8d60')
if s['end_exclusive']!='0x2f8e4a' or [i['pc'] for i in s['instructions'] if i['mnemonic']=='ret']!=['0x2f8d84','0x2f8e35','0x2f8e49']:raise ValueError('matcher return coverage')
controls=dict(fallback_byte_upper_bound=0xff<511,
              fallback_miss_narrows_to_ffff_and_is_rejected=(-1&0xffff)==0xffff,
              override_word_can_represent_candidate=511<=0xffff,
              dispatch_mode_is_not_row_category=records[0x3067aa]['memory'][0]['rip_target']=='0x22c215c')
bad={pc:dict(i) for pc,i in records.items()};bad[0x2f8e36]['args']='eax, word ptr [r10]'
try:witnesses(bad)
except ValueError:controls['widened_result_load_refused']=True
else:raise ValueError('wrong result width accepted')
if not all(controls.values()):raise ValueError('boundary controls incomplete')
result=dict(question='Can30DB70 null-record selection obtain candidate511..534 from2F8D60 authored-threshold fallback when signed override index01EEBAF0 is negative?',
 hypotheses=['fallback returns a full action word capable of511..534','fallback match returns only one unsigned byte; miss is the rejectedFFFF sentinel'],
 method='A original return-width/dataflow invariant; no samples/native execution/authored corpus census',
 exe_sha256=pin,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,controls=controls,
 conclusion='EXCLUDED on the negative-override fallback path: matching return range0..255; no match becomesFFFF and is rejected before queue value creation. No new authored threshold capture is required for this result-width invariant.',
 unresolved='Nonnegative override reads a u16 from022BE930; its index/value writer domain is not proved here. Other queue producers, direct script inputs, initialized row/actor premises, natural loader/rejection reachability remain OPEN.',
 corrections='306760 dispatch selects by separate mode dword022C215C in1..6, not row category. Invalid raw01 inferred10 edges from6 entries plus padding/code; raw02 derives extent from original guard and keeps only6. No prior semantic claim depended on raw01.',
 limits='Complete local matcher source and caller leg, not full natural reachability. No forced calls, emulator, real FF12, timing, save or config access. Producer controls and independent acceptance remain distinct.')
out.write_text(json.dumps(result,indent=2)+'\n')
print('EXCLUDED candidate511..534 from negative-override byte-return fallback; u16 override remains OPEN')
