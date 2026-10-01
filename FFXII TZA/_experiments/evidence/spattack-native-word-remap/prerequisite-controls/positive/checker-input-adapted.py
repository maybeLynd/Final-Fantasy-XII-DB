"""Conditional original-native word remap; not full interpreter or reachability.
Question: does the preload's minus/plus D0 arithmetic exclude ids511..534?
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\Tools\\work\\ASTRA\\runtime-residue-method-retriage\\spattack-prerequisite-controls-01\\positive');ROOT=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable result exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';b=exe.read_bytes()
pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if sha(exe)!=pin:raise ValueError('original image changed')
p=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,p+20)[0]
secs=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(va,n):
 for vs,sva,rs,ro in secs:
  if 0x120000+sva<=va and va+n<=0x120000+sva+rs:return b[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
 raise ValueError('unbacked original span')
pairs=[('effective-and-script-id-raw-01.json','capture-effective-and-script-id.py'),
 ('spattack-output-writers-raw-02.json','capture-spattack-output-writers.py'),
 ('spattack-queue-reader-raw-01.json','capture-spattack-queue-reader.py'),
 ('spattack-info-raw-01.json','capture-spattack-info.py'),
 ('spattack-leaves-and-guard-raw-01.json','capture-spattack-leaves-and-guard.py')]
records={};inputs=[]
for name,driver in pairs:
 path=W/name;r=json.loads(path.read_text())
 if r['exe_sha256']!=pin or r['driver_sha256']!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver):raise ValueError('capture invocation incomplete/changed')
 if name=='spattack-output-writers-raw-02.json' and r.get('wrapper_complete') is not True:raise ValueError('wrapper prerequisite incomplete')
 if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):raise ValueError('upstream controls failed')
 for span in r['ranges']:
  original=read(int(span['start'],16),int(span['end_exclusive'],16)-int(span['start'],16))
  if hashlib.sha256(original).hexdigest()!=span['sha256']:raise ValueError('original span differs')
  for i in span['instructions']:
   pc=int(i['pc'],16);cb=bytes.fromhex(i['bytes'])
   if cb!=read(pc,len(cb)):raise ValueError('instruction differs from image')
   if pc in records and records[pc]!=i:raise ValueError('overlapping source observations disagree')
   records[pc]=i
 inputs.append(dict(path=name,sha256=sha(path),driver=driver,driver_sha256=sha(W/driver)))
required={0x30db9d:('movzx','r8d, word ptr [rbx + 4]'),
 0x30dbc7:('movzx','ecx, word ptr [rbx + 4]'),0x30dbcb:('mov','eax, 0xffff'),
 0x30dbd2:('cmp','cx, ax'),0x30dbd5:('je','0x30dbea'),
 0x30dbd7:('movzx','eax, cx'),0x30dbda:('sub','eax, 0xd0'),
 0x30dbea:('or','eax, 0xffffffff'),0x30dc98:('mov','dword ptr [rip + 0x1fb44da], eax'),
 0x309c00:('mov','eax, dword ptr [rip + 0x1fb8572]'),
 0x309c06:('cmp','eax, -1'),0x309c09:('jne','0x309c0e'),
 0x309c0b:('xor','eax, eax'),0x309c13:('mov','dword ptr [rdx], eax'),
 0x30eea6:('mov','ebx, edx'),0x30eea8:('cmp','edx, -1'),
 0x30eeab:('je','0x30eeb7'),0x30eead:('mov','eax, 0xd0'),
 0x30eeb2:('add','bx, ax'),0x30eeb7:('mov','ebx, 0xffff'),
 0x30eef5:('movzx','r8d, bx'),0x30ef00:('call','0x30cfb0')}
def witnesses(rr):
 for pc,expected in required.items():
  i=rr.get(pc)
  if not i or (i['mnemonic'],i['args'])!=expected:raise ValueError('source remap witness changed')
witnesses(records)
if records[0x30dc98]['memory'][0]['rip_target']!=records[0x309c00]['memory'][0]['rip_target']:raise ValueError('different queue storage')
def encode(word):return -1 if word==0xffff else word-0xd0
def read_available(encoded):return encoded!=-1
def decode(encoded):return 0xffff if encoded==-1 else (encoded+0xd0)&0xffff
aliases=[w for w in range(65536) if decode(encode(w))!=w]
if aliases!=[0xcf]:raise ValueError('composed word domain differs')
candidate_results=[dict(action=w,queued=encode(w),reader_available=read_available(encode(w)),decoded=decode(encode(w))) for w in range(511,535)]
if any(not x['reader_available'] or x['decoded']!=x['action'] for x in candidate_results):raise ValueError('candidate exclusion found')
controls=dict(d0_encodes_zero=encode(0xd0)==0,cf_collides_with_sentinel=encode(0xcf)==-1,
 ffff_is_sentinel=encode(0xffff)==-1,cf_reader_reports_unavailable=not read_available(encode(0xcf)),
 high_word_fffe_preserved=decode(encode(0xfffe))==0xfffe)
bad={pc:dict(i) for pc,i in records.items()};bad[0x30eeb2]['mnemonic']='sub'
try:witnesses(bad)
except ValueError:controls['changed_addition_witness_refused']=True
else:raise ValueError('wrong remap accepted')
if not all(controls.values()):raise ValueError('boundary controls incomplete')
result=dict(question='Does the preload minus/plusD0 remap itself exclude candidate action ids511..534?',
 hypotheses=['only a bounded0..33 skill domain survives the remap','arithmetic preserves candidates under unchanged value-transfer premises'],
 method='A original source + exhaustive bounded word arithmetic, no machine-code execution',
 exe_sha256=pin,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,
 controls=controls,candidate_results=candidate_results,roundtrip_mismatch_words=aliases,
 reader_sentinel_words=[0xcf,0xffff],
 conclusion='Arithmetic-only exclusion REFUTED: ids511..534 encode303..326 and decode back unchanged. WordCF collides with -1 and the reader reports no output; FFFF also means unavailable.',
 limits='Conditional composed native arithmetic. Unchanged transfer through script storage/VM is a premise, not tested full interpreter execution. Producer guard admission, actual command/AI/authored selection, natural initialized queue/actor state, metadata/IO/owner submission remain OPEN. No all-writer/indirect-alias proof, no live observation. Exhaustive word calculations are not65536 native executions.')
out.write_text(json.dumps(result,indent=2)+'\n')
print('REFUTED arithmetic-only exclusion; candidate511..534 survive; CF/FFFF queue sentinel collision retained')
