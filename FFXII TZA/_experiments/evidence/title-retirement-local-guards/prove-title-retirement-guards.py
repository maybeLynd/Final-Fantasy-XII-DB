"""Retained-source proof of the local24A680 membership/release guards.

Does NOT settle the original transitive cancellation/lifetime question. Fresh
output [optional retained-input directory] for actual prerequisite controls.
"""
import hashlib,json,pathlib,re,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else ROOT/'Database/FFXII TZA/_experiments/evidence/title-member-notification-routing/section04-title-member-source'
if len(sys.argv) not in (2,3) or out.exists():raise ValueError('fresh result required')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=source/'original_body_manifest.json';dp=source/'original_disassembly.txt'
if sha(mp)!='2ae22b0b46bbb7a83cb545d5bc45bb62d350f03509a4e5d41b2725e26cbee5ef' or sha(dp)!='ca93837847ed6efdc72a7ee26d8457324fc44ef06dddcfe60ffcf43c4aad1c57':raise ValueError('retained input generation changed')
m=json.loads(mp.read_text())
if m['exe_sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong original build')
ix={}
for line in dp.read_text().splitlines():
 match=re.match(r'^([0-9A-F]{8})\s+([0-9a-f]+)\s+(\S+)\s*(.*)$',line)
 if match:
  pc,blob,mne,args=match.groups();a=int(pc,16)
  if a in ix:raise ValueError('duplicate original instruction')
  ix[a]=dict(bytes=blob,mnemonic=mne,args=args.split(';')[0].strip())
for entry in ['0024A680','00394070','00181610','003697F0','00249580']:
 b=next(x for x in m['bodies'] if x['entry']==entry);start=int(entry,16);end=int(b['end_exclusive'],16);at=start;raw=b''
 while at<end:
  z=bytes.fromhex(ix[at]['bytes']);raw+=z;at+=len(z)
 if at!=end or len(raw)!=b['bytes'] or hashlib.sha256(raw).hexdigest()!=b['sha256']:raise ValueError('retained body incomplete/mixed '+entry)
def need(pc,mne,args):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(mne,args):raise ValueError('required original operation changed '+hex(pc))
need(0x39409e,'mov','edx, 1');need(0x3940a3,'call','0x24a680')
need(0x24a680,'test','rcx, rcx');need(0x24a683,'je','0x24a70c')
need(0x24a69f,'xor','r8d, r8d');need(0x24a6a2,'cmp','rax, rbx')
need(0x24a6a7,'add','rax, 0x48');need(0x24a6ab,'cmp','rax, rbx');need(0x24a6ae,'je','0x24a6c0')
need(0x24a6b0,'add','rax, 0x48');need(0x24a6b4,'add','r8d, 2');need(0x24a6b8,'cmp','r8d, 0x40');need(0x24a6bc,'jl','0x24a6a2')
need(0x24a6c0,'inc','r8d');need(0x24a6c3,'cmp','r8d, 0x40');need(0x24a6c7,'je','0x24a702')
need(0x24a6c9,'call','0x181610');need(0x24a6ce,'mov','eax, dword ptr [rbx + 0x38]')
need(0x24a6d1,'and','eax, 0x3f00');need(0x24a6d6,'cmp','eax, 0x1400')
need(0x24a6dd,'mov','rcx, qword ptr [rbx + 0x10]');need(0x24a6e6,'call','0x3697f0')
need(0x24a6eb,'test','edi, edi');need(0x24a6ed,'je','0x24a6f8');need(0x24a6ef,'mov','rcx, qword ptr [rbx + 0x18]');need(0x24a6f3,'call','0x3697f0')
need(0x24a6f8,'and','dword ptr [rbx + 0x38], 0xffffffdf');need(0x24a6fc,'dec','dword ptr [rip + 0x1e4607e]')
# Bind the RIP addresses from encoded bytes, not the disassembler's comment.
def rip(pc):
 z=bytes.fromhex(ix[pc]['bytes']);return pc+len(z)+int.from_bytes(z[-4:],'little',signed=True)
base=rip(0x24a695);counter=rip(0x24a6fc)
if (base,counter)!=(0x208f580,0x2090780):raise ValueError('pool/counter identity changed')
need(0x249590,'test','byte ptr [rax], 1');need(0x249597,'add','rax, 0x20');need(0x24959b,'cmp','edx, 0xc');need(0x24959e,'jl','0x249590')
if rip(0x249580)!=0x2090790:raise ValueError('ticket pool identity changed')
record_rows=[dict(index=k,address=hex(base+0x48*k)) for k in range(64)]
if base+64*0x48!=counter or len({x['address'] for x in record_rows})!=64:raise ValueError('bounded pool calculation incomplete')
r=dict(status='PRODUCER_CHECKED_LOCAL_GUARDS_INDEPENDENT_PENDING',producer_complete=True,method='A RETAINED_SOURCE',
 question='Does original24A680(mode1) check ticket pending/already-retired state before its local resource-record release stores?',
 hypotheses=['ticket/pending/active release guard','exact resource-pool address membership only, followed by local release effects'],
 method_choice='Complete retained original body plus exact bounded loop/dataflow suffices for LOCAL guards; no live/isolated execution or unchanged body recapture.',
 reference=dict(exe_sha256=m['exe_sha256'],manifest_sha256=sha(mp),disassembly_sha256=sha(dp),source_commit='0fcf9349e',original_body_sha256='d9acb85e3fd2e73d0e88365cc0a39d604086e67b706516b442412a1a6432a78d'),
 observations=['Titlemessage18 passes+C8/mode1 at394097/9E/A3; that handler does not clear+C8.',
  '24A680 accepts onlyNULL or exact64 resource-record addresses0208F580+k*48,k0..63. NULL/other addresses return before local release calls/stores; membership loop progresses by two with both parity slots tested.',
  'These64 records end at02090780, the locally decremented DWORD counter; completion ticket pool02090790(12x20) is distinct. No local ticket counter/pending/readiness test occurs in24A680.',
  'Recognized address calls181610 first. It then conditionally frees+10 when flags38&3F00==1400 and pointer nonnull; nonzero mode unconditionally passes+18 to3697F0 (which separately handlesNULL).',
  'On normal continuation, it clears flags38 bit20 and decrementsDWORD02090780. It has no local flag20/already-retired guard; its only read of flags38 before clearing masks3F00, excluding20. It performs no local pointer10/18 clear.',
  'Thus a retained recognized address is eligible again after bit20 was cleared, and a normal repeated call can reach the same localDEC again. This is an exact local guard/effects statement, not a full idempotence/free/side-effect proof.',
  'Neither this source nor a pending ticket alone establishes that cancellation/drain ran.181610 ->manager getter1B1C00 ->1B1960 has separate tracking-tree effects; free/tracker services and scheduler/parent lifetimes require their own bounds.'],
 bounded_arithmetic=record_rows,
 conditional_local_counter_effect='Each recognized-address normal continuation performs one DEC DWORD; arithmetic wraps modulo2^32. Nested/reentrant service effects on overall counter are NOT assumed absent.',
 limitations=['Original transitive2495C0 cancellation/drain and natural pending teardown remainOPEN','Intermediate helper/free effects not substituted as proof or fully certified','Distinct static pools are not observed initialized pointers/ownership or reuse/lifetime guarantees','No safe arbitrary double teardown, overall idempotence or full absence claim','Prior title routing review/consumption remains separate; no duplicate sender review'],
 semantic_implication='Reconstruct membership/flags/pointer releases exactly; do not implement a fictitious pending-ticket/active-bit guard or equate mode1 with proven cancellation.',
 consumer='FABLE title/OV29 and OPUS-owned handle contract/type changes after scoped independent review',
 checker_sha256=sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
 cleanup='Retained reads only; no process/input/game/instrument/save/config/reference writes')
out.write_text(json.dumps(r,indent=2)+'\n');print('Retained-source local membership/release guards proved; transitive cancellation/lifetime remainsOPEN')
