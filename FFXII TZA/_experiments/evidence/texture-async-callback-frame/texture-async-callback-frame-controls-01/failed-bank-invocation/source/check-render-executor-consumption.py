"""Source confirmation of returned BG11; not a live hit or new broad census."""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable output exists')
rp=W/'render-executor-consumption-raw-01.json';r=json.loads(rp.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';b=exe.read_bytes()
if sha(exe)!=r['exe_sha256'] or r['exe_sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('original identity')
if r['driver_sha256']!=sha(W/'capture-index-path.py') or r['invocation_driver_sha256']!=sha(W/'capture-render-executor-consumption.py'):raise ValueError('actual capture invocation')
if len(r['controls'])!=3 or any(c['observed']!=c['expected'] for c in r['controls']):raise ValueError('capture controls')
p=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,p+20)[0]
secs=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(va,n):
 for vs,sva,rs,ro in secs:
  if 0x120000+sva<=va and va+n<=0x120000+sva+rs:return b[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
 raise ValueError('unbacked original bytes')
ins={int(i['pc'],16):i for s in r['ranges'] for i in s['instructions']}
required={0x610753:('call','0x60a410'),0x60a46a:('call','0x624670'),
 0x60a46f:('mov','r14, rax'),0x624670:('jmp','0x5fd050'),
 0x60a5b3:('lea','rbx, [rsi + 0x70]'),0x60a5c0:('mov','ecx, dword ptr [rsi]'),
 0x60a5c2:('dec','ecx'),0x60a5d0:('movzx','eax, byte ptr [r12 + rax + 0x4eaad8]'),
 0x60a5d9:('mov','ecx, dword ptr [r12 + rax*4 + 0x4eaab8]'),
 0x60a8bd:('mov','qword ptr [rbp - 0x50], r14'),0x60a8ca:('mov','rax, qword ptr [rbx - 0x60]'),
 0x60a8ce:('mov','qword ptr [rbp - 0x40], rax'),0x60a8d2:('lea','rcx, [rbp - 0x50]'),
 0x60a8d6:('call','qword ptr [rbx - 0x68]'),0x1f4a19:('mov','rcx, qword ptr [rcx]'),
 0x1f4a1c:('call','0x624660'),0x624660:('lea','rax, [rcx + 0x18c0]')}
def witnesses(records):
 for pc,expected in required.items():
  rec=records.get(pc)
  if not rec or (rec['mnemonic'],rec['args'])!=expected:raise ValueError('required source witness changed')
  cb=bytes.fromhex(rec['bytes'])
  if cb!=read(pc,len(cb)):raise ValueError('original witness bytes changed')
witnesses(ins)
singleton=[]
for pc in (0x5fd097,0x5fd0c4):
 rec=ins[pc];m=rec['memory'][0]
 if rec['mnemonic']!='lea' or int(m['rip_target'],16)!=0x2cc0410:raise ValueError('getter singleton differs')
 singleton.append(dict(pc=hex(pc),bytes=rec['bytes'],target=m['rip_target']))
# Original two-level dispatch, not a guessed switch shape.
labels=read(0x60aad8,47);dest=read(0x60aab8,8*4)
arm=labels[0x2f-1];target=0x120000+struct.unpack_from('<I',dest,arm*4)[0]
if target!=0x60a899:raise ValueError('opcode2F dispatch mismatch')
bad={pc:dict(i) for pc,i in ins.items()};bad[0x60a8d2]['args']='lea rcx, [rbx]'
try:witnesses(bad)
except ValueError:changed_context_refused=True
else:raise ValueError('changed source accepted')
page=ROOT/'Database/FFXII TZA/17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md'
result=dict(method='A retained canonical answer + focused certified-original source confirmation',
 question='Who executes callback001F4A10 and what is callback context field0?',
 canonical_answer_commit='7e4af33d5',requester_return='fable-astra-live-facts-0930 README',
 exe_sha256=r['exe_sha256'],driver_sha256=sha(pathlib.Path(__file__)),capture_sha256=sha(rp),
 canonical_page_sha256=sha(page),getter_sites=singleton,
 dispatch=dict(labels_hex=labels.hex(),targets_hex=dest.hex(),opcode=47,arm=arm,target=hex(target)),
 controls=dict(actual_capture_roles=3,changed_callback_context_source_refused=changed_context_refused),
 normalized=dict(render_thread_call='00610753 ->0060A410',callback_call='0060A8D6 indirect block+8',
 callback_return_address='0060A8D9',callback_context='synthesized stack record',
 context_field0='02CC0410',device='02CC1CD0',block_low_dword='0x2F; block is not callback context'),
 result='Returned static answer satisfies executor/context question; old live breakpoint request superseded without gameplay.',
 limits='Not an actual callback hit, numeric runtime sample, thread id or universal reachability proof. Normal initialized-object/native-ABI assumptions. Block upper DWORD is not assigned by its opcode store and not needed by this callback. Existing canonical answer reused, not a new broad census or independent acceptance of every Gi contract.')
out.write_text(json.dumps(result,indent=2)+'\n')
print('CONFIRMED returned executor/context answer from original source; live request unnecessary')
