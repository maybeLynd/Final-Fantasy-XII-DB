"""OV42: does the slot's class20 validity gate exclude candidate ids511..534?

Verified original instructions plus exhaustive unsigned-word input predicate.
Not execution; descriptor count543 is an initialized-table premise, not a live read.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
OUT=pathlib.Path(sys.argv[1])
if OUT.exists():raise ValueError('immutable result exists')
rawpath=W/'action-admission-guards-raw-01.json';raw=json.loads(rawpath.read_text())
callerpath=W/'special-admission-callers-raw-01.json';caller=json.loads(callerpath.read_text())
receiptpath=W/'action-selectors-01/result.json';tables=json.loads(receiptpath.read_text())
exe=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
expected_sha='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if sha(exe)!=expected_sha or any(r['exe_sha256']!=expected_sha for r in (raw,caller)):
    raise ValueError('original-image prerequisite')
p=struct.unpack_from('<I',exe,0x3c)[0];optional=struct.unpack_from('<H',exe,p+20)[0]
sections=[struct.unpack_from('<IIII',exe,p+24+optional+i*40+8)
          for i in range(struct.unpack_from('<H',exe,p+6)[0])]
def read(va,n):
    for vs,sva,rs,ro in sections:
        if 0x120000+sva<=va and va+n<=0x120000+sva+rs:
            return exe[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
    raise ValueError('unbacked original bytes')
ins={int(i['pc'],16):i for r in (raw,caller) for s in r['ranges'] for i in s['instructions']}
def witnesses(records):
    required={0x30cc25:('movzx','edx, word ptr [rbx + 0x1c]'),0x30cc29:('mov','ecx, 0x14'),
      0x30cc32:('call','0x322c50'),0x322c5a:('lea','eax, [rcx - 1]'),
      0x322c5d:('mov','ebx, edx'),0x322c72:('mov','ecx, dword ptr [rdi + rax*4 + 0x203054]'),
      0x322c7c:('jmp','rcx'),0x322f72:('mov','rcx, qword ptr [rip + 0x2b9c1bf]'),
      0x322f79:('xor','eax, eax'),0x322f7b:('test','rcx, rcx'),0x322f7e:('je','0x32302a'),
      0x322f84:('mov','ecx, dword ptr [rcx + 4]'),0x322f87:('jmp','0x32302c'),
      0x32302c:('mov','edx, eax'),0x32302e:('cmp','ebx, edx'),0x323030:('jl','0x322c8d'),
      0x323036:('lea','eax, [rcx - 1]'),0x323039:('cmp','ebx, eax'),
      0x32303b:('jg','0x322c8d'),0x323041:('mov','eax, 1')}
    for pc,expected in required.items():
        rec=records.get(pc)
        if not rec or (rec['mnemonic'],rec['args'])!=expected:raise ValueError('source predicate witness changed')
        if bytes.fromhex(rec['bytes'])!=read(pc,len(bytes.fromhex(rec['bytes']))):raise ValueError('original witness bytes changed')
witnesses(ins)
for r in (raw,caller):
    if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):
        raise ValueError('required capture control failed')
jt=read(0x323054,32*4);target=0x120000+struct.unpack_from('<I',jt,19*4)[0]
if target!=0x322f72:raise ValueError('class20 dispatch not proved')
if int(ins[0x322f72]['memory'][0]['rip_target'],16)!=0x2ebf138:raise ValueError('wrong descriptor identity')
if len(tables['results'])!=9 or any(r['count']!=543 or r['stride']!=60 for r in tables['results']):
    raise ValueError('missing/changed authored-count premise')
for rec in tables['results']:
    lang=rec['path'].split('/test_battle/')[1].split('/')[0]
    b=(W/'action-selectors-01/tables'/('action_data_'+lang+'.st2e')).read_bytes()
    if sha(b)!=rec['table_sha256'] or struct.unpack_from('<I',b,4)[0]!=543:raise ValueError('table input changed')
def admissible(word,count):
    # This class arm's exact signed comparisons, on movzx u16 input and count<=INT_MAX.
    return word>=0 and word<=count-1
accepted=[i for i in range(65536) if admissible(i,543)]
if accepted!=list(range(543)):raise ValueError('bounded source predicate differs')
controls=dict(boundary542_accepted=admissible(542,543),boundary543_refused=not admissible(543,543),
              empty_count_refuses_all=not any(admissible(i,0) for i in range(65536)),
              private_count511_refuses_candidate511=not admissible(511,511))
if not all(controls.values()):raise ValueError('boundary control failed')
# Same-size private source-counterexample witness must be refused, not silently analyzed as original.
bad={pc:dict(rec) for pc,rec in ins.items()};bad[0x32303b]['mnemonic']='jl';bad[0x32303b]['bytes']='0f8c4cfcffff'
try:witnesses(bad)
except ValueError:controls['private_reversed_upper_branch_refused']=True
else:raise ValueError('changed original predicate was accepted')
result=dict(question='Does the class20 slot validity guard exclude ordinary action ids511..534?',
    method='A original source witnesses/jump-table resolution + exhaustive bounded u16 predicate; no code execution',
    exe_sha256=expected_sha,driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
    raw_sha256=sha(rawpath.read_bytes()),caller_raw_sha256=sha(callerpath.read_bytes()),
    table_receipt_sha256=sha(receiptpath.read_bytes()),class20_jump_table_bytes=jt.hex(),class20_target=hex(target),
    descriptor_global='02EBF138',initialized_count_premise=543,input_domain='slot+1C movzx unsigned16',
    accepted_ids=[0,542],rejected_ids=[543,65535],candidate_ids_accepted=list(range(511,535)),controls=controls,
    conclusion='REFUTED: class20 bounds exclude these candidates. Under initialized table premises they are valid ids.',
    limits='No slot allocation, command/AI/script selection, immutable initialized codec, readiness-helper progress or successful asset/owner admission is established. Exhaustive predicate evaluation is static reasoning, not original-code execution.')
OUT.write_text(json.dumps(result,indent=2)+'\n')
print('VALID source predicate: class20 admits0..542; candidate511..534 not excluded. Natural reachability OPEN.')
