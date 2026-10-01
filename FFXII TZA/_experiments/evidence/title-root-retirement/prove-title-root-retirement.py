"""Conditional title/root retention and raw-owner notification, from original bytes.

No native fixture, process observation or transitive cancellation/lifetime proof.
Use fresh result [optional disposable source directory]. Retained TXT is decoded
and its memory operands classified with the actual shared reviewed adapter.
"""
import importlib.util,json,pathlib,re,struct,sys
import capstone
from capstone.x86_const import X86_OP_MEM
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('title_retention_dependencies','prove-title-queue-consumption.py')
S=module('title_retention_annotations','validate-title-source-annotations.py')
RETAINED={'title-watcher-lifetime-raw-02.json':'6f1592b32f094155884bfd4a78f285a773ed1c1cdd4a97d29eb8168551504759','title-watcher-attachment-raw-01.json':'4ed56c3c88151b514623482411340366e1d0cebc81ed4e2041df92e244884aac'}
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 status=src/'title-root-retirement-capture-02.status.json';st=json.loads(status.read_text());capture=src/'capture-title-root-retirement.py'
 if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(capture):raise ValueError('required root capture invocation failed or stale')
 if not (src/'title-root-retirement-capture-02.stdout').read_bytes().strip() or (src/'title-root-retirement-capture-02.stderr').read_bytes().strip():raise ValueError('required root capture output failed or missing')
 pins=[];allraw=[];ix={}
 for name in ['title-root-retirement-source-01.json',*RETAINED]:
  if name in RETAINED and P.sha(src/name)!=RETAINED[name]:raise ValueError('required retained source identity changed')
  raw,ops=P.load(src,name,pins);allraw.append(raw)
  for pc,i in ops.items():
   if pc in ix and ix[pc]!=i:raise ValueError('overlapping retained bytes disagree')
   ix[pc]=i
 if allraw[0].get('invocation_driver_sha256')!=P.sha(capture):raise ValueError('required root wrapper identity changed')
 expected=[('0x247ae0','0x248024','ac6a14bceedfa189f54f60fd4fab518c697349b86cc80e456cefd4137df5d095'),('0x2445d0','0x24460d','236801748843925eb089fc3dfbd34bfccae7e679d44891d1d02a696e88b92e90')]
 if [(q['start'],q['end_exclusive'],q['sha256']) for q in allraw[0]['ranges']]!=expected:raise ValueError('required original root identity changed')
 # Retained SECTION04 source, not its scripted native fixture verdicts.
 retained_pins=[]
 for name,h in [('original_body_manifest.json','2ae22b0b46bbb7a83cb545d5bc45bb62d350f03509a4e5d41b2725e26cbee5ef'),('original_disassembly.txt','ca93837847ed6efdc72a7ee26d8457324fc44ef06dddcfe60ffcf43c4aad1c57')]:
  p=src/'section04-title-member-source'/name
  if P.sha(p)!=h:raise ValueError('required original SECTION04 identity changed')
  retained_pins.append(dict(path=p.relative_to(src).as_posix(),sha256=h))
 manifest=json.loads((src/'section04-title-member-source/original_body_manifest.json').read_text())
 if manifest.get('exe_sha256')!=P.SHA:raise ValueError('retained image provenance changed')
 selected={0x393ff0,0x394070,0x394460,0x244f50,0x2465f0,0x244960,0x248220}
 bodies={int(q['entry'],16):q for q in manifest['bodies'] if int(q['entry'],16) in selected}
 if set(bodies)!=selected:raise ValueError('missing required retained body')
 text=(src/'section04-title-member-source/original_disassembly.txt').read_text();records={a:[] for a in selected}
 for line in text.splitlines():
  m=re.match(r'^([0-9A-F]{8})\s+([0-9a-f]+)\s+(\w+)\s*(.*?)\s*$',line)
  if not m:continue
  pc=int(m[1],16)
  for a,q in bodies.items():
   if a<=pc<int(q['end_exclusive'],16):records[a].append((pc,bytes.fromhex(m[2]),m[3],m[4].split(' ;')[0].rstrip()))
 # The adapter is checked by S before import and actually used in this path.
 annotations=[S.validate(raw) for raw in allraw]
 spec=importlib.util.spec_from_file_location('title_retained_actual_adapter',S.ADAPTER);roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 normalized=dict(adapter_sha256=P.ADAPTER,capstone=capstone.__version__,ranges=[])
 for a,q in sorted(bodies.items()):
  raw=records[a];blob=b''.join(t[1] for t in raw)
  if len(blob)!=q['bytes'] or P.sha(src/'section04-title-member-source/original_body_manifest.json')!=retained_pins[0]['sha256']:raise ValueError('incomplete required retained body')
  import hashlib
  if hashlib.sha256(blob).hexdigest()!=q['sha256']:raise ValueError('retained body bytes changed')
  decoded=list(cs.disasm(blob,a));nr=[]
  if len(decoded)!=len(raw):raise ValueError('retained decoder coverage differs')
  for ins,t in zip(decoded,raw):
   if (ins.address,ins.bytes,ins.mnemonic,ins.op_str)!=(t[0],t[1],t[2],t[3]):raise ValueError('retained text does not decode from bytes')
   memory=[]
   for k,op in enumerate(ins.operands):
    if op.type==X86_OP_MEM:
     m=op.mem;base=ins.reg_name(m.base);index=ins.reg_name(m.index)
     memory.append(dict(base=base,index=index,scale=m.scale,displacement=m.disp,size=op.size,role=roles.op_kind(ins,op,k),rip_target=hex(ins.address+ins.size+m.disp) if base=='rip' else None))
   rec=dict(pc=hex(ins.address),bytes=ins.bytes.hex(),mnemonic=ins.mnemonic,args=ins.op_str,memory=memory);nr.append(rec);ix[ins.address]=rec
  normalized['ranges'].append(dict(start=hex(a),end_exclusive=hex(a+len(blob)),sha256=q['sha256'],instructions=nr))
 annotations.append(S.validate(normalized))
 # Every normalized/retained code range is independently pinned to shipping bytes.
 data=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 import hashlib
 if hashlib.sha256(data).hexdigest()!=P.SHA:raise ValueError('original reference image changed')
 pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0];secs=[struct.unpack_from('<IIII',data,pe+24+opt+40*k+8) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
 def read(a,n):
  for vs,va,rs,ro in secs:
   if 0x120000+va<=a and a+n<=0x120000+va+rs:return data[ro+a-0x120000-va:ro+a-0x120000-va+n]
  raise ValueError('unbacked required original span')
 for raw in allraw+[normalized]:
  for q in raw['ranges']:
   if hashlib.sha256(read(int(q['start'],16),int(q['end_exclusive'],16)-int(q['start'],16))).hexdigest()!=q['sha256']:raise ValueError('retained original span disagrees with shipping image')
 ops=[(0x394495,'xor','r8d, r8d'),(0x394498,'lea','rdx, [rip - 0x42f]'),(0x39449f,'mov','ecx, 0xd8'),(0x3944a4,'call','0x244f50'),(0x244fc5,'mov','r9, rsi'),(0x244fc8,'mov','r8, rbp'),(0x244fcd,'call','0x2465f0'),(0x246641,'mov','qword ptr [rdi], rbx'),(0x246748,'call','rax'),
 (0x394106,'call','0x393ff0'),(0x394117,'mov','rcx, qword ptr [rip + 0x1cfa90a]'),(0x39411e,'mov','rdx, rbx'),(0x394121,'call','0x244960'),(0x244960,'cmp','qword ptr [rdx + 0x10], 0'),(0x244965,'je','0x248220'),
 (0x247cf2,'mov','ebp, 3'),(0x247d20,'lea','rdi, [rip + 0x1e46cf9]'),(0x247d40,'mov','qword ptr [rsp + 0x58], rsi'),(0x247d93,'lea','r8, [rip - 0x37ca]'),(0x247d9a,'call','0x2465f0'),(0x247d9f,'mov','qword ptr [rdi], rbx'),(0x247da2,'inc','rsi'),(0x247dac,'add','rdi, 8'),(0x247db0,'sub','rbp, 1'),(0x247db4,'jne','0x247d40'),(0x247fac,'inc','al'),(0x247fbc,'mov','rcx, rbx'),(0x247fbf,'jmp','0x247d89'),(0x2445d0,'cmp','dword ptr [rdx], 1'),(0x2445d8,'or','dword ptr [rcx + 0x40], 0x23'),
 (0x248267,'mov','qword ptr [rdx + 0x10], rbx'),(0x24826b,'test','byte ptr [rbx + 0x40], 0x20'),(0x24826f,'je','0x2482cc'),(0x248271,'or','dword ptr [rdx + 0x40], 0x20'),
 (0x245050,'lea','rdx, [rip + 0x6d0019]'),(0x24505a,'call','rax'),(0x245072,'test','byte ptr [rdi + 0x40], 0x20'),(0x24507e,'jne','0x24508a'),(0x245085,'jmp','0x2482e0'),(0x24508a,'xor','edx, edx'),(0x24508c,'call','0x2473f0'),(0x245094,'and','eax, 0xfffffffd'),(0x245097,'bts','eax, 0xa'),(0x24509b,'mov','dword ptr [rdi + 0x40], eax'),
 (0x24960b,'mov','rcx, qword ptr [rdi + 8]'),(0x249612,'mov','dword ptr [rsp + 0x20], 0x10'),(0x249620,'test','rcx, rcx'),(0x249623,'je','0x249634'),(0x249625,'mov','rax, qword ptr [rcx]'),(0x249628,'test','rax, rax'),(0x24962b,'je','0x249634'),(0x249632,'call','rax'),
 (0x3940e3,'or','dword ptr [rbx + 0xc0], 1'),(0x3940ea,'xor','eax, eax'),(0x3940ec,'add','rsp, 0x20'),(0x3940f0,'pop','rbx'),(0x3940f1,'ret',''),(0x2483ce,'mov','qword ptr [rdi], 0'),(0x2483d5,'bt','eax, 0xe'),(0x2483de,'call','0x3697f0'),(0x2483e9,'mov','byte ptr [rdi + 0xa2], 0')]
 for pc,m,a in ops:P.need(ix,pc,m,a)
 if ix[0x394117]['memory'][0]['rip_target']!='0x208ea28' or ix[0x247d20]['memory'][0]['rip_target']!='0x208ea20' or ix[0x247d93]['memory'][0]['rip_target']!='0x2445d0':raise ValueError('actual root target/handler binding changed')
 if read(0x915070,24)!=struct.pack('<I',18)+bytes(20):raise ValueError('original teardown message identity changed')
 # Exact owner-use window and complete message16 leaf arm, not a global absence claim.
 window=[i for pc,i in sorted(ix.items()) if 0x24960b<=pc<0x249634]
 owner_reads=[(i['pc'],m['displacement'],m['size'],m['role']) for i in window for m in i['memory'] if m['base']=='rcx']
 if owner_reads!=[('0x249625',0,8,'r')]:raise ValueError('unexpected local owner-field dependency')
 arm=[i for pc,i in sorted(ix.items()) if 0x3940e3<=pc<=0x3940f1]
 if [i['pc'] for i in arm]!=['0x3940e3','0x3940ea','0x3940ec','0x3940f0','0x3940f1']:raise ValueError('message16 arm incomplete')
 receipts=['title-root-retirement-capture-02'+s for s in ('.status.json','.stdout','.stderr')]+['capture-title-root-retirement.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py']
 r=dict(status='PRODUCER_VALID_CONDITIONAL_TITLE_RETENTION_INDEPENDENT_PENDING',producer_complete=True,method='A RETAINED/STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,retained_source_pins=retained_pins,annotation_prerequisite=annotations,required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],instruction_pins=[dict(pc=hex(pc),mnemonic=m,args=a) for pc,m,a in ops],local_owner_reads=owner_reads,
 established=['Title394460 selects handler394070/extentD8 via244F50. Original constructor clears requested bytes, installs handler and invokes message1. Titlemessage1 starts393FF0 requests BEFORE loading root0208EA28 and calling244960(this). Parentless gate tail248220 sets self+10 and propagates root bit5 directly into title flags40. This is the actual title path, not an unrelated rooted widget.',
 'Original247AE0 loop publishes three constructed roots into0208EA20/28/30. It selects2445D0, whose message1 ORs23 into flags40. Under successful valid unchanged root construction/attachment, the title inherits bit5. This proves conditional deferral applicability, not a captured initialized root.',
 '245020 broadcastsmessage18 then REREADS self flags40 bit5. If still set, it calls2473F0(self,0), clears bit1/sets bit10 and does not locally release through2482E0. If clear, it tailcalls2482E0. Handler/children/opaque helper mutation can change that branch; initial root bit5 alone is not unconditional lifetime proof.',
 'After existing ticket sealed/equal/custom-zero gates, ordinary2495C0 loads RAW owner ticket+8, rejectsNULL, loads current owner handler and rejectsNULL, then calls it withmessage16. The owner-use window reads only owner+0; it does not locally read owner flags40, a generation, or title publication02AEE4C0. Ticket flags/counters are not owner flags.',
 'Title394070 message16 directly ORs readybit0 at+C0; that arm has no closing/publication/parent test. At a valid retained post-teardown boundary with handler unchanged and ordinary ticket gates satisfied, this local composition permits readybit mutation despite bit10 and cleared publication. This is a conditional source counterexample to inherent local notification revocation, not a natural late-delivery witness.',
 'Physical2482E0 release nulls handler BEFORE its pool/heap disposition. A still-backed, unreused pool slot with thatNULL suppresses ordinary notification.244F50 can select released pool slots and2465F0 installs a new handler, so the NULL is not a perpetual identity token. Retained ticket raw owner+8 has no local generation resolution. Natural surviving tickets/reuse, safety and cross-system cancellation remain unproved.'],
 assumptions=['Normal ABI-correct calls with valid backing/root/tree; successful allocator/memset/constructor and unchanged handler/global/parent until attachment', 'Root flag5 still set on attach; no opaque or message handler clears it before post-broadcast branch', 'Conditional late boundary has valid retained owner/ticket/member and satisfied ordinary completion gates; pointer/context roundtrip assumptions unchanged', 'No assertion opaque focus, enable, resource, allocator/free or message callbacks leave all storage unchanged; only explicit local operations/order proved'],
 limitations=['No live/native/emulated run or observed IO/callback/thread/frame; no full natural caller/reachability or actual pending teardown', 'Root initialized successfully in source is conditional, not actual process initial-state proof; message18/pre-release/physical-release and pool reuse are distinct', 'No transitive no-cancellation/drain, arbitrary double teardown, heap dereference validity, ABA occurrence or scheduler lifetime guarantee', 'Earlier accepted sender/retirement guards reused, not reviewed again; independent acceptance/canonical incorporation of this additive composition still pending'],
 conditional_witness=dict(boundary='after245020 retained branch returns normally',flags40='bit5 andbit10 set/bit1 clear',publication02AEE4C0=0,owner_handler='394070 unchanged',c0_before=0,c0_after_local_message16=1,natural_reachability=False),
 affected_claims=['FABLE title OV31: actual parent/root and deferral applicability conditional source gap','FABLE/OPUS OV29: closing/publication is not local ordinary-notification revocation; raw current-handler lookup distinct from identity/lifetime guarantee'],next_discriminator='Determine whether original request/retirement/callback scheduling prevents a surviving ordinary ticket across handler null/reuse; use retained queue/cancellation source before automated observation. Actual overlap/timing remains open.',checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Finite read-only original/retained reduction; no game/PC/input/instrument/native/save/config/reference/peer process mutation')
 out.open('x',encoding='utf-8').write(json.dumps(r,indent=2)+'\n');print('Conditional title root retention and raw-owner notification proved; natural timing/reuse OPEN')
if __name__=='__main__':main()
