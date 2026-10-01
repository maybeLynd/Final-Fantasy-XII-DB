"""Original-source getter/queue correction and conditional tracker effects.

Fresh result [optional disposable source dir]. No native/emulated/live runs.
Normal CFGs and call boundaries do not establish omitted initialization/callees.
"""
import hashlib,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
if len(sys.argv) not in (2,3) or out.exists():raise ValueError('fresh result [disposable source dir]')
pins=[];SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name):
 p=source/name;v=json.loads(p.read_text());pins.append(dict(path=name,sha256=sha(p)))
 if v.get('exe_sha256')!=SHA or v.get('wrapper_complete') is not True:raise ValueError('incomplete original dependency '+name)
 if [(x['bytes'],x['observed']) for x in v['controls']]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('actual observer controls missing')
 for q in v['ranges']:
  z=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
  if len(z)!=int(q['end_exclusive'],16)-int(q['start'],16) or hashlib.sha256(z).hexdigest()!=q['sha256']:raise ValueError('mixed/changed original bytes')
 return v,{int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
raw,tracker=load('title-tracker-cleanup-source-01.json');queue_raw,queue=load('title-cleanup-callback-queue-source-01.json')
def need(ix,pc,m,args):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('required source operation changed '+hex(pc))
def rip(ix,pc):
 z=[int(m['rip_target'],16) for m in ix[pc]['memory'] if m.get('rip_target')]
 if len(z)!=1:raise ValueError('missing/ambiguous original RIP identity')
 return z[0]
cfg=raw.get('normal_cfg',{})
if (cfg.get('entry'),cfg.get('end_exclusive'),cfg.get('reachable_instructions'),cfg.get('returns'))!=('0x1fb660','0x1fb71c',52,['0x1fb71b']) or len(raw.get('verified_unwind_chains',[]))!=2:raise ValueError('normal tracker source incomplete')
for chain in raw['verified_unwind_chains']:
 if chain['root']!=[0x1fb660,0x1fb6b7,0x1da8448]:raise ValueError('wrong normal root generation')
need(tracker,0x1fb677,'mov','rcx, qword ptr [rcx]');need(tracker,0x1fb67a,'call','0x183720')
need(tracker,0x1fb689,'mov','qword ptr [rdi], rbp');need(tracker,0x1fb687,'xor','ebp, ebp')
need(tracker,0x1fb691,'mov','rcx, qword ptr [rbx + 0x28]');need(tracker,0x1fb695,'call','0x183720')
need(tracker,0x1fb69d,'mov','qword ptr [rbx + 0x28], rbp');need(tracker,0x1fb6a1,'call','0x16d6d0')
need(tracker,0x1fb6c0,'mov','rdx, qword ptr [rsi]');need(tracker,0x1fb6c3,'lea','rcx, [rdi + 8]')
need(tracker,0x1fb6c7,'call','0x1af2b0');need(tracker,0x1fb6d4,'mov','rbx, qword ptr [rsi + 8]')
need(tracker,0x1fb6d8,'mov','r8d, 0x30');need(tracker,0x1fb6de,'mov','rdx, rsi')
need(tracker,0x1fb6d0,'lea','rcx, [rdi + 0x38]');need(tracker,0x1fb6e1,'call','qword ptr [rax + 0x18]')
need(tracker,0x1fb6ff,'mov','qword ptr [rdi + 0x20], rbp');need(tracker,0x1fb703,'mov','byte ptr [rdi + 0x28], bpl')
need(tracker,0x1fb707,'mov','dword ptr [rdi + 0x30], ebp');need(tracker,0x1fb70f,'mov','qword ptr [rax], rax')
need(tracker,0x1fb712,'mov','qword ptr [rdi + 0x18], rax')
need(queue,0x189127,'ret','')
if queue[0x189120]['bytes']!='488b057164df01' or rip(queue,0x189120)!=0x1f7f598:raise ValueError('global getter identity changed')
need(tracker,0x183720,'test','rcx, rcx');need(tracker,0x183723,'je','0x183753')
need(tracker,0x18372a,'mov','rbx, rcx');need(tracker,0x18372d,'call','0x189120')
need(tracker,0x183732,'test','rax, rax');need(tracker,0x183735,'je','0x18374e');need(tracker,0x183737,'call','0x189120')
need(tracker,0x18373c,'mov','rcx, rax');need(tracker,0x183746,'mov','r8, rbx');need(tracker,0x183749,'call','0x185a90')
if rip(tracker,0x18373f)!=0x17ecc0:raise ValueError('wrong supplied callback')
need(queue,0x185a94,'movsxd','rax, dword ptr [rcx + 0xcb8]');need(queue,0x185a9b,'add','rcx, 0xc38')
need(queue,0x185aa2,'shl','rax, 5');need(queue,0x185aa6,'add','rcx, rax')
need(queue,0x185aa9,'mov','qword ptr [rsp + 0x20], rdx');need(queue,0x185aae,'mov','qword ptr [rsp + 0x28], r8')
need(queue,0x185ab3,'mov','rdx, qword ptr [rcx + 8]');need(queue,0x185ab7,'cmp','rdx, qword ptr [rcx + 0x10]')
need(queue,0x185abb,'jae','0x185ad7');need(queue,0x185abd,'lea','rax, [rdx + 0x10]')
need(queue,0x185ac1,'mov','qword ptr [rcx + 8], rax');need(queue,0x185ac5,'test','rdx, rdx')
need(queue,0x185ac8,'je','0x185ae1');need(queue,0x185aca,'movups','xmm0, xmmword ptr [rsp + 0x20]')
need(queue,0x185acf,'movups','xmmword ptr [rdx], xmm0');need(queue,0x185adc,'call','0x1858a0')
if queue[0x185acf]['memory'][0]['role']!='w' or queue[0x185abd]['memory'][0]['role']!='addr':raise ValueError('actual shared memory/address roles changed')
need(queue,0x17ecc6,'mov','rbx, rcx');need(queue,0x17ecc9,'call','0x5de250')
need(queue,0x17ecce,'mov','rcx, rbx');need(queue,0x17ecd6,'jmp','0x19c590')
result=dict(status='PRODUCER_CHECKED_CONDITIONAL_BOUNDARY_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',
 question='Does tracker183720 resolve each supplied object and synchronously release it, or use a shared context to queue a callback/data pair?',
 hypotheses=['argument-dependent object resolver and immediate complete release','global context getter plus conditional callback-pair enqueue; omitted scheduling/release effects separate'],
 evidence_choice='Complete original getter/caller/writer/control flow distinguishes these hypotheses without original-code execution or live state.',
 exe_sha256=SHA,source_pins=pins,
 established=[
  '189120 is exactly MOV RAX,[01F7F598];RET. It ignores RCX and does not resolve the supplied object. The canonical transform paragraph resolving the object twice is incorrect.',
  '183720 with supplied argumentNULL returns before context reads. Otherwise it reads the shared global twice, tests only the first forNULL, and passes the second as RCX with callback17ECC0/data=original argument to185A90. Stable/nonNULL context across reads is a condition, not a lifetime invariant.',
  '185A90 chooses queue=secondContext+C38+32*signextend32(DWORD[secondContext+CB8]); it has no local index bounds check. It stages16B [callback,data] on stack.',
  'If old writecursor<end(unsigned) and old cursornonnull, fast path stores cursor+16 at queue+8 BEFORE copying16B pair to oldcursor. It makes no nested call or callback execution on that branch. There is no local full16B remaining-capacity check; valid vector/index/allocation/ABI and alias premises are required.',
  'If cursorNULL while unsigned cursor<end, it still advances cursor by16 and skips the copy. This is a conditional malformed-state branch, not observed initialization or a normal null-queue claim. Otherwise write>=end delegates1858A0(queue,write,&pair), effects unproved here.',
  '1FB660 invokes183720 for value+0, then nulls+0; circular-list payload+28 similarly invokes183720 then nulls+28. Another linked list delegates1AF2B0(value+8,[link]) and allocator-like vcall18(value+38,link,30). Normal return resets+20/+28byte/+30 and circular+10/+18. Invoking these helpers is not itself complete release/cancellation evidence.',
  'Supplied callback17ECC0, IF actually invoked with incoming RCX, preserves that input for5DE250 then tail19C590. This proves that callback entry boundary, not that queue consumption supplies stored data or invokes it at a specific frame/thread.'
 ],correction=dict(page='00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md',clause='183720:189120 resolves the object twice',supported_replacement='189120 reads shared global01F7F598;183720 stages17ECC0/original-argument through185A90 after first nonNULL context test'),
 assumptions=['Normally returning original callees and ABI-valid stack/register state','Stable valid context for any fast-path association; signed index yields backed queue, 16B storage readable/writable; no interfering aliases/writes','Valid terminating circular/linked lists for tracker normal return; callback/link helper effects not assumed safe/absent'],
 limitations=['Actual initialized context/index/capacity/global lifetime and natural tracker branches remain unobserved','Queue slow path1858A0, consumer ABI/thread/frame/drain and5DE250/19C590 effects remainOPEN','No atomic16B-copy/order guarantee to concurrent observers or observed race','Not whole title ticket cancellation/lifetime, successful load, arbitrary malformed-input safety, direct native free or initialized pointer proof'],
 next_discriminators=['Original1858A0 insertion and context queue consumer identify whether/how callback pair executes','Bound5DE250/19C590 callback effects and tracker1AF2B0/vcall identity from original metadata before live escalation'],
 affected_claims=['Canonical global-getter/183720 description','OV29 title tracker and deferred resource-release boundary','OPUS context queue/callback ABI contracts where owned'],
 native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,checker_sha256=sha(pathlib.Path(__file__)),
 cleanup='Offline original reads only; no game/process/control/instrument/save/config/reference writes')
out.write_text(json.dumps(result,indent=2)+'\n');print('Global getter/callback queue correction and conditional tracker boundary proved; scheduling/cancellation remainsOPEN')
