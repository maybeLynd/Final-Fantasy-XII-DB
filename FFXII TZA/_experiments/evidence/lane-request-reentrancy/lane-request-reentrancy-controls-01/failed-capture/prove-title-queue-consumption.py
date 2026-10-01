"""Local original queue growth and four-bank callback consumption proof.

Fresh result [optional disposable source directory]. Method A source dataflow.
No harness/native/emulated/game execution; algebraic witnesses are conditional.
"""
import hashlib,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ADAPTER='5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(source,name,pins):
 p=source/name;v=json.loads(p.read_text());pins.append(dict(path=name,sha256=sha(p)))
 if v.get('exe_sha256')!=SHA or v.get('wrapper_complete') is not True or v.get('adapter_sha256')!=ADAPTER:raise ValueError('missing original/adapter prerequisite')
 if [(x['bytes'],x['observed']) for x in v['controls']]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('actual observer controls missing')
 for q in v['ranges']:
  z=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
  if len(z)!=int(q['end_exclusive'],16)-int(q['start'],16) or hashlib.sha256(z).hexdigest()!=q['sha256']:raise ValueError('mixed original bytes')
 return v,{int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
def need(ix,pc,m,a):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('source operation mismatch '+hex(pc))
def closed(ix,a,z):
 todo=[a];seen=set();returns=[];calls=[]
 while todo:
  p=todo.pop()
  if p in seen:continue
  if p not in ix or not a<=p<z:raise ValueError('unclosed normal CFG '+hex(p))
  seen.add(p);i=ix[p];nextpc=p+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
  if m=='ret':returns.append(hex(p));continue
  if m=='jmp':todo.append(int(i['args'],16));continue
  if m.startswith('j'):todo.append(int(i['args'],16))
  if m=='call':calls.append(dict(pc=hex(p),target=i['args']))
  todo.append(nextpc)
 local={p for p in ix if a<=p<z}
 if local!=seen:raise ValueError('normal body has unchecked instructions')
 return dict(entry=hex(a),end_exclusive=hex(z),instructions=len(seen),returns=sorted(returns),calls=sorted(calls,key=lambda x:int(x['pc'],16)))
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source dir]')
 out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result already exists')
 pins=[];slow,s=load(source,'title-queue-slow-consumer-source-01.json',pins);consumer,c=load(source,'title-queue-consumer-source-01.json',pins);enqueue,e=load(source,'title-cleanup-callback-queue-source-01.json',pins)
 expected={0x1858a0:('0x185a0f','7de7c1c81408da54d8f0a088342bb25faa686fe7bddfd02bf3d9caa3cfae249c'),0x186230:('0x1862ad','95811f0a1707bdb0e0832193d6e5b907001c0af68a70b17d67ecf1b3c7ca1581')}
 for raw in [slow,consumer]:
  for q in raw['ranges']:
   a=int(q['start'],16)
   if a in expected and (q['end_exclusive'],q['sha256'])!=expected[a]:raise ValueError('named body identity changed')
 g1=closed(s,0x1858a0,0x185a0f);g2=closed(c,0x186230,0x1862ad)
 if g1['calls']!=[{'pc':'0x185956','target':'qword ptr [rax + 0x10]'},{'pc':'0x1859dd','target':'qword ptr [r9 + 0x18]'}] or g2['calls']!=[{'pc':'0x186277','target':'qword ptr [rbx]'}]:raise ValueError('call boundaries changed')
 for pc,m,a in [(0x185a94,'movsxd','rax, dword ptr [rcx + 0xcb8]'),(0x185a9b,'add','rcx, 0xc38'),(0x185aa2,'shl','rax, 5'),(0x185ab3,'mov','rdx, qword ptr [rcx + 8]'),(0x185abb,'jae','0x185ad7'),(0x185adc,'call','0x1858a0')]:need(e,pc,m,a)
 for pc,m,a in [(0x1858af,'mov','rax, qword ptr [rcx + 8]'),(0x1858b3,'mov','rbx, r8'),(0x1858b6,'mov','rdi, rdx'),(0x1858b9,'mov','rsi, rcx'),(0x1858bc,'cmp','rax, qword ptr [rcx + 0x10]'),(0x1858c0,'je','0x18591f'),(0x18591f,'sub','rax, qword ptr [rcx]'),(0x185922,'sar','rax, 4'),(0x185930,'test','eax, eax'),(0x185932,'je','0x185940'),(0x185934,'lea','ebp, [rax + rax]'),(0x185937,'test','ebp, ebp'),(0x185939,'jne','0x185945'),(0x18593b,'xor','r14d, r14d'),(0x185940,'mov','ebp, 1'),(0x185945,'mov','rax, qword ptr [rcx + 0x18]'),(0x185949,'add','rcx, 0x18'),(0x18594d,'mov','edx, ebp'),(0x185952,'shl','rdx, 4'),(0x185959,'mov','r14, rax'),(0x18595c,'mov','rdx, qword ptr [rsi]'),(0x18595f,'mov','rcx, r14'),(0x185962,'cmp','rdx, rdi'),(0x185965,'je','0x18597f'),(0x18596c,'movups','xmm0, xmmword ptr [rdx]'),(0x18596f,'movups','xmmword ptr [rcx], xmm0'),(0x185972,'add','rdx, 0x10'),(0x185976,'add','rcx, 0x10'),(0x18597a,'cmp','rdx, rdi'),(0x18597d,'jne','0x185967'),(0x18597f,'test','rcx, rcx'),(0x185984,'movups','xmm0, xmmword ptr [rbx]'),(0x185987,'movups','xmmword ptr [rcx], xmm0'),(0x18598a,'mov','rax, qword ptr [rsi + 8]'),(0x18598e,'lea','rbx, [rcx + 0x10]'),(0x185992,'cmp','rdi, rax'),(0x185995,'je','0x1859bc'),(0x1859bc,'mov','rdx, qword ptr [rsi]'),(0x1859bf,'test','rdx, rdx'),(0x1859c2,'je','0x1859e1'),(0x1859c4,'mov','r8, qword ptr [rsi + 0x10]'),(0x1859c8,'lea','rcx, [rsi + 0x18]'),(0x1859cc,'mov','r9, qword ptr [rcx]'),(0x1859cf,'sub','r8, rdx'),(0x1859d2,'sar','r8, 4'),(0x1859d6,'mov','r8d, r8d'),(0x1859d9,'shl','r8, 4'),(0x1859e1,'mov','eax, ebp'),(0x1859e8,'mov','qword ptr [rsi], r14'),(0x1859eb,'mov','qword ptr [rsi + 8], rbx'),(0x1859f4,'shl','rax, 4'),(0x1859f8,'add','rax, r14'),(0x185a00,'mov','qword ptr [rsi + 0x10], rax')]:need(s,pc,m,a)
 for pc,m,a in [(0x18623f,'mov','eax, dword ptr [rcx + 0xcb8]'),(0x186245,'mov','rsi, rcx'),(0x186248,'inc','eax'),(0x18624a,'and','eax, 3'),(0x18624d,'mov','dword ptr [rcx + 0xcb8], eax'),(0x186253,'movsxd','rbx, eax'),(0x186256,'lea','rax, [rbx + 0x62]'),(0x18625a,'shl','rbx, 5'),(0x18625e,'shl','rax, 5'),(0x186262,'mov','rbx, qword ptr [rbx + rcx + 0xc38]'),(0x18626a,'mov','rdi, qword ptr [rax + rcx]'),(0x18626e,'cmp','rbx, rdi'),(0x186271,'je','0x186282'),(0x186273,'mov','rcx, qword ptr [rbx + 8]'),(0x186277,'call','qword ptr [rbx]'),(0x186279,'add','rbx, 0x10'),(0x18627d,'cmp','rbx, rdi'),(0x186280,'jne','0x186273'),(0x186282,'movsxd','rcx, dword ptr [rsi + 0xcb8]'),(0x18628e,'shl','rcx, 5'),(0x186292,'mov','rax, qword ptr [rcx + rsi + 0xc38]'),(0x18629a,'mov','qword ptr [rcx + rsi + 0xc40], rax')]:need(c,pc,m,a)
 if s[0x185987]['memory'][0]['role']!='w' or c[0x18629a]['memory'][0]['role']!='w' or c[0x186256]['memory'][0]['role']!='addr':raise ValueError('actual store/address roles changed')
 cycles=[dict(initial_low2=i,consumed_banks=[(i+k)&3 for k in range(1,5)]) for i in range(4)]
 if any(x['consumed_banks'][-1]!=x['initial_low2'] or len(set(x['consumed_banks']))!=4 for x in cycles):raise ValueError('bounded low-bit cycle derivation failed')
 r=dict(status='PRODUCER_CHECKED_CONDITIONAL_QUEUE_DATAFLOW_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=SHA,source_pins=pins,normal_cfgs=[g1,g2],question='How does the full queue append store its pair, and how is that pair consumed through the same four-bank context?',established=[
 'With valid stable begin<=write<=capacity and position=write supplied by185A90, its write>=capacity condition implies write==capacity. Original1858A0 takes the full-growth arm; the spare-capacity insertion arm is not reached under these premises.',
 'At valid full size n=(write-begin)/16, n=0 chooses new capacity1; 1<=n<=7FFFFFFF chooses2*n. Native arithmetic tests low32(EAX), doubles in32-bit EBP and zero-extends allocation bytes; it is not an arbitrary-size sanitizer. Growth uses queue+18 interface slot10, copies the old prefix and staged16B pair, optionally calls interface slot18 on old storage, then publishes begin/write/capacity in that order. Relevant slot effects and success/freshness remain premises.',
 '1858A0 has only the two interface call sites, with allocator-record/byte-count/storage arguments. It never directly calls the staged function pointer as its target. This is local source dataflow, not proof that opaque allocation callbacks cannot perform arbitrary transitive effects.',
 '186230 writes new bank ((old DWORD+1) modulo2^32)&3 BEFORE loading queue begin/write for that bank. Queue bases are context+C38+32*bank; write offset C40. It snapshots the write cursor, then invokes each16B pair function at+0 with RCX=data at+8 and increments the iterator by16. This establishes the previously omitted stored-data callback ABI, conditional on that consumer executing.',
 'Under unchanged index/storage/callback inputs and normal ABI-preserving returns, it visits only the pre-call [begin,write) snapshot and resets current selected write to its begin. It does not free the queue allocation or zero callback/data bytes locally. Initial empty queue skips callbacks and still resets its cursor.',
 'Four uninterrupted consumer invocations rotate through all four banks and return to the original low-two-bit bank. A pair appended to the current bank is not visited on the next invocation; its bank is selected on the fourth invocation under unchanged relevant state. Invocations are not frames, and actual initial index/pump caller/thread/timing are not established.',
 'The final reset re-reads context+CB8 after callbacks instead of using the captured bank. Same-bank callback append without reallocation lies beyond the captured end and its cursor can be discarded by that reset; a callback that changes CB8 can redirect which bank is reset. These are conditional source counterexamples to unrestricted mutation/reentry safety, not observations that17ECC0 or ordinary gameplay performs those mutations.'
 ],bounded_algebraic_cycle=cycles,cycle_basis='INC32 then AND3 depends only on two low bits; all4 residues enumerated as algebraic controls, not4 original-code executions',conditional_witnesses=[dict(kind='append_without_reallocation',bank=1,begin='0x1000',captured_write='0x1010',capacity='0x1030',callback_appends_at='0x1010',new_write='0x1020',loop_end_unchanged='0x1010',reset_write='0x1000',interpretation='New appended pair is not invoked in this loop and is outside the reset logical range; requires callback append and no reallocation/index interference'),dict(kind='index_mutation',captured_bank=1,callback_leaves_index=2,reset_bank=2,interpretation='Final reset uses bank2 while loop iterated bank1; conditional state write, no natural reachability assertion')],assumptions=['ABI-correct stack and normally returning original callees; callbacks preserve nonvolatile iterator/end/context registers','Valid contiguous backed16B queue records; stable input pair and context; growth returns fresh sufficiently large nonNULL storage with no conflicting aliases or overflow','0<=full count<=7FFFFFFF for ordinary capacity formula; opaque allocation/free side effects not independently established','Unchanged queue/index/storage through callbacks for the ordinary loop/cycle; mutation witnesses explicitly replace that premise'],limitations=['No actual initialized game state, consumer caller/thread/frame, natural reentry, callback mutation or lifetime observation','Named pump source spans are retained preparation only; no automatic same-context consumer caller proof','No cancellation/drain of title resource tickets, full lifetime guarantee, allocation-interface implementation or5DE250/19C590 release effects','Direct-call-only candidate search with zero hits lacks negative detection control and does not establish no caller; identified E9 at185C20 remains a candidate until a separate original leaf/caller proof'],next_discriminators=['Validate185C20 tail entry and its callers/binding before asserting normal consumer reachability','Bind allocation interfaces and callback5DE250/19C590 effects if needed for cancellation/lifetime proposition'],affected_claims=['OPUS renderer four-bank callback queue ABI/order and mutation preconditions','FABLE title tracker deferred-release scheduling boundary'],checker_sha256=sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Only original file reads and synchronous checked scripts; no PC/game/process/instrument/save/config/reference writes')
 with out.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
 print('Original full-append and four-bank local callback ABI/order proved; natural timing/lifetime remains OPEN')
if __name__=='__main__':main()
