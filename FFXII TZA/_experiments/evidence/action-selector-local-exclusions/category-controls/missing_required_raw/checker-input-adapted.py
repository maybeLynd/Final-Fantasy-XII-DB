"""Candidate-row category exclusion: verified source and retained tables, not a live run.
The normal raw+5==0 category path rejects; nonzero raw+5 bypasses it.
Run from the repo root with one FRESH result path. Never overwrite receipts.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\Tools\\work\\ASTRA\\runtime-residue-method-retriage\\category-prerequisite-controls-01\\missing_required_raw');ROOT=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable result exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';b=exe.read_bytes()
if sha(exe)!=pin:raise ValueError('original image prerequisite')
p=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,p+20)[0]
secs=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(va,n):
 for vs,sva,rs,ro in secs:
  if 0x120000+sva<=va and va+n<=0x120000+sva+rs:return b[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
 raise ValueError('unbacked source span')
records={};inputs=[]
for name,driver in [('action-availability-gates-raw-01.json','capture-action-availability-gates.py'),
                    ('spattack-leaves-and-guard-raw-01.json','capture-spattack-leaves-and-guard.py')]:
 r=json.loads((W/name).read_text())
 if r['exe_sha256']!=pin or r['driver_sha256']!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver):raise ValueError('capture invocation prerequisite')
 if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):raise ValueError('capture role prerequisite')
 for s in r['ranges']:
  original=read(int(s['start'],16),int(s['end_exclusive'],16)-int(s['start'],16))
  if hashlib.sha256(original).hexdigest()!=s['sha256']:raise ValueError('source span prerequisite')
  for i in s['instructions']:
   pc=int(i['pc'],16)
   if read(pc,len(bytes.fromhex(i['bytes'])))!=bytes.fromhex(i['bytes']):raise ValueError('instruction prerequisite')
   if pc in records and records[pc]!=i:raise ValueError('source disagreement')
   records[pc]=i
 inputs.append(dict(path=name,sha256=sha(W/name),driver=driver,driver_sha256=sha(W/driver)))
required={
 0x30610d:('call','0x322c50'),0x306114:('jne','0x306120'),
 0x306116:('mov','eax, 4'),0x306120:('test','rdi, rdi'),
 0x306123:('je','0x30632c'),0x306129:('movzx','eax, byte ptr [rdi + 5]'),
 0x30612d:('test','eax, eax'),0x30612f:('jne','0x30632c'),
 0x30616b:('movzx','ecx, word ptr [rdx + 8]'),0x30616f:('imul','ecx, r14d'),
 0x306173:('add','ecx, eax'),0x306175:('jmp','0x306181'),
 0x306181:('movzx','eax, byte ptr [rcx + 0x1e]'),0x306185:('cmp','eax, 6'),
 0x306188:('ja','0x3062f4'),0x3062f4:('cmp','eax, 9'),
 0x3062f7:('je','0x306311'),0x3062f9:('cmp','eax, 0xff'),
 0x3062fe:('je','0x30630a'),0x306300:('mov','eax, 5'),
 0x306305:('jmp','0x3061d3'),0x3061d3:('mov','rbx, qword ptr [rsp + 0x30]'),
 0x3061d8:('mov','rbp, qword ptr [rsp + 0x38]'),0x3061dd:('mov','rsi, qword ptr [rsp + 0x40]'),
 0x3061e2:('mov','rdi, qword ptr [rsp + 0x48]'),0x3061e7:('add','rsp, 0x20'),
 0x3061eb:('pop','r14'),0x3061ed:('ret',''),
 0x30632c:('xor','eax, eax'),0x30632e:('jmp','0x3061d8'),
 0x3064a6:('call','0x3060e0'),0x3064ab:('test','eax, eax'),
 0x3064ad:('je','0x3064bf'),0x3064af:('mov','eax, 0xf'),
 0x3064bf:('movzx','edx, di'),0x3064c5:('call','0x323ec0'),
 0x2ffe9d:('call','0x306480'),0x2ffea2:('test','eax, eax'),
 0x2ffea4:('jne','0x2ffd99'),0x2ffd99:('mov','r14, qword ptr [rsp + 0x38]'),
 0x2ffd9e:('mov','rbx, qword ptr [rsp + 0x40]'),0x2ffda3:('mov','rsi, qword ptr [rsp + 0x48]'),
 0x2ffda8:('add','rsp, 0x20'),0x2ffdac:('pop','rdi'),0x2ffdad:('ret',''),
 0x30dbbe:('call','0x2ffcf0'),0x30dbc3:('test','eax, eax'),
 0x30dbc5:('jne','0x30dc24'),0x30dc24:('mov','eax, 1'),
 0x30dc29:('movaps','xmm6, xmmword ptr [rsp + 0x20]'),
 0x30dc2e:('add','rsp, 0x30'),0x30dc32:('pop','rbx'),0x30dc33:('ret','')}
def witnesses(rr):
 for pc,expected in required.items():
  if pc not in rr or (rr[pc]['mnemonic'],rr[pc]['args'])!=expected:raise ValueError('category path witness changed')
witnesses(records)
if records[0x306135]['memory'][0]['rip_target']!='0x2ebf138':raise ValueError('action descriptor identity')
packet=W/'special-action-frozen-ready';manifest=json.loads((packet/'manifest.json').read_text())
listed={m['path']:m for m in manifest['members']}
def frozen(rel):
 m=listed[rel];p=packet/rel
 if p.stat().st_size!=m['bytes'] or sha(p)!=m['sha256']:raise ValueError('immutable table prerequisite')
 return p.read_bytes()
receipt=json.loads(frozen('action-selectors-01/result.json'))
if len(receipt['results'])!=9:raise ValueError('missing table corpus')
rows=[]
for r in receipt['results']:
 lang=r['path'].split('/test_battle/')[1].split('/')[0]
 rel='action-selectors-01/tables/action_data_'+lang+'.st2e';tb=frozen(rel)
 n,s,o=struct.unpack_from('<III',tb,4)
 if not r['retained_equals_archive'] or r['table_sha256']!=hashlib.sha256(tb).hexdigest() or (n,s)!=(543,60) or o+n*s>len(tb):raise ValueError('authored table premise')
 rowfacts=[dict(id=i,category=tb[o+i*s+0x1e],selector=struct.unpack_from('<H',tb,o+i*s+0x24)[0]) for i in range(511,535)]
 if any(x['category']!=7 or x['selector']!=0xffff for x in rowfacts):raise ValueError('candidate category counterexample')
 rows.append(dict(language=lang,table_sha256=r['table_sha256'],rows=rowfacts))
# These are exact local branch outcomes, conditional on valid id/initialized row.
# They are NOT a reconstructed full availability function or native executions.
def category7_result(raw_present,raw5):return 0 if not raw_present or raw5!=0 else 5
raw5_domain=[dict(raw5=v,category_result=category7_result(True,v)) for v in range(256)]
if raw5_domain[0]['category_result']!=5 or any(x['category_result']!=0 for x in raw5_domain[1:]):raise ValueError('finite branch outcome differs')
controls=dict(raw5_zero_rejected=category7_result(True,0)==5,
              nonzero_raw5_bypasses=all(category7_result(True,v)==0 for v in range(1,256)),
              null_raw_category_bypasses=category7_result(False,0)==0,
              category_ff_uses_zero_arm=records[0x3062fe]['args']=='0x30630a')
bad={pc:dict(i) for pc,i in records.items()};bad[0x306188]['mnemonic']='jbe'
try:witnesses(bad)
except ValueError:controls['reversed_category_branch_refused']=True
else:raise ValueError('wrong branch accepted')
result=dict(question='Does the original category availability guard exclude ordinary candidate action ids511..534, and under which raw actor premise?',
 hypotheses=['all actor kinds unconditionally exclude these candidates','raw+5==0 excludes category7, while nonzero raw+5 bypasses this local guard'],
 method='A verified complete guard source and immutable archive-matched row data; finite byte-domain reasoning; no native execution',
 exe_sha256=pin,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,
 table_manifest_sha256=sha(packet/'manifest.json'),table_receipt_sha256=sha(packet/'action-selectors-01/result.json'),
 rows=rows,raw5_domain=raw5_domain,controls=controls,
 established=['All nine retained archive-matched tables give rows511..534 category7 and selectorFFFF.',
 'Under valid class20 id, initialized row identity and nonnull raw+5==0,3060E0 returns5 independent of raw+4 and the remaining row fields.',
 '306480 translates this nonzero category result into0F without entering its licence leg.',
 'If2FFCF0 reaches this leg with that raw state, its nonzero result returns to30DB70, whose ordinary branch rejects before its pending-action/actor stores.',
 'Nonzero raw+5 bypasses the category check and returns0; no universal actor exclusion follows.'],
 unresolved=['Stable raw+5/row codec through preceding calls; natural actor and action selection; other queue producers including null-record arm; successful loader/IO/owner reachability; OV42 as a whole.'],
 limits='Conditional source path, not full availability execution or complete caller/alias proof. Class20/initialized table binding is a premise already separately documented. Null raw bypasses this category helper but the outer helper has other null handling. No live state, timing, normal reachability or all-producer exclusion inferred.')
if not all(controls.values()):raise ValueError('control failure')
out.write_text(json.dumps(result,indent=2)+'\n')
print('ESTABLISHED category7 exclusion for raw+5==0; universal actor exclusion REFUTED; candidate natural reachability OPEN')
