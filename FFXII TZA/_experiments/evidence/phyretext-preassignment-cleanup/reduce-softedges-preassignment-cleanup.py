"""Static conditional proof of the reached shader-array preclear/cleanup path.

Fresh result [optional disposable source dir]. No emulator/native/game execution.
The getter argument attribution is derived from stores, not its old driver label.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
if len(sys.argv) not in (2,3) or out.exists():raise ValueError('fresh-output [disposable-source-dir] required')
pins=[];SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(z):return hashlib.sha256(z).hexdigest()
def load(name):
 p=source/name;z=p.read_bytes();r=json.loads(z);pins.append(dict(path=name,sha256=sha(z)))
 if r.get('exe_sha256')!=SHA or r.get('wrapper_complete') is not True:raise ValueError('incomplete original prerequisite '+name)
 if [(c['bytes'],c['observed']) for c in r['controls']]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('observer control missing')
 for q in r['ranges']:
  b=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
  if len(b)!=int(q['end_exclusive'],16)-int(q['start'],16) or sha(b)!=q['sha256']:raise ValueError('original extent/hash mismatch')
 return {int(i['pc'],16):i for q in r['ranges'] for i in q['instructions']}
def need(ix,pc,m,args):
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('required normalized operation changed '+hex(pc))
def rip(ix,pc):
 targets=[int(x['rip_target'],16) for x in ix[pc]['memory'] if x.get('rip_target')]
 if len(targets)!=1:raise ValueError('missing exact RIP identity')
 return targets[0]
reg=load('softedges-member-resolution-code-01.json')
ctor=load('softedges-array-descriptor-offset-code-01.json')
parent=load('softedges-array-parent-getter-code-01.json')
patch=load('softedges-header-membership-code-01.json')
call=load('softedges-elements-callback-source-01/original-code.json')
setter=load('softedges-member-assignment-code-01.json')
cleanup=load('softedges-preassignment-cleanup-code-01.json')
need(reg,0x5eeb5e,'xor','r15d, r15d');need(reg,0x5eeb90,'call','0x6372a0')
need(reg,0x5eeb95,'mov','rbx, rax');need(reg,0x5eeb9f,'call','0x6373d0')
need(reg,0x5eeba4,'mov','rdx, rax');need(reg,0x5eeba7,'mov','dword ptr [rsp + 0x30], r15d')
need(reg,0x5eebac,'mov','qword ptr [rsp + 0x28], rbx');need(reg,0x5eebc3,'call','0x632d80')
if rip(reg,0x5eeb61)!=0x2cea460:raise ValueError('registered array descriptor identity changed')
need(parent,0x6372a7,'ret','')
if rip(parent,0x6372a0)!=0x2cf8270 or rip(ctor,0x6373f7)!=0x1f2e330:raise ValueError('parent/sub-object getter identities changed')
need(ctor,0x632dd1,'mov','rax, qword ptr [rsp + 0x30]');need(ctor,0x632dd6,'mov','qword ptr [rcx + 0x70], rdx')
need(ctor,0x632dda,'mov','qword ptr [rcx + 0x78], rax');need(ctor,0x632e4b,'mov','eax, dword ptr [rsp + 0x38]')
need(ctor,0x632e4f,'mov','dword ptr [rcx + 0xf0], eax');need(ctor,0x632d80,'xor','r10d, r10d')
need(ctor,0x632e62,'mov','qword ptr [rcx + 0xf4], r10')
need(ctor,0x63e416,'mov','dword ptr [rcx + 0xf4], r8d');need(ctor,0x63e410,'xor','r8d, r8d')
if rip(ctor,0x63e425)!=0x2cf8270:raise ValueError('recompute root sentinel changed')
need(ctor,0x63e430,'cmp','rax, r9');need(ctor,0x63e433,'je','0x63e44a')
need(ctor,0x63e435,'mov','ecx, dword ptr [rax + 0xf0]');need(ctor,0x63e43b,'add','dword ptr [rdx + 0xf4], ecx')
need(ctor,0x63e441,'mov','rax, qword ptr [rax + 0x78]');need(ctor,0x63e448,'jne','0x63e430')
need(patch,0x59cc38,'xor','r13d, r13d');need(patch,0x59cc76,'mov','ecx, dword ptr [r14 + 0x48]')
need(patch,0x59cc7a,'mov','rax, qword ptr [r14 + 0x18]');need(patch,0x59cc7e,'sub','ecx, dword ptr [rax + 0xf4]')
need(patch,0x59cc84,'movsxd','rdx, ecx');need(patch,0x59cc8c,'add','rdx, qword ptr [rsp + 0x38]')
need(patch,0x59cc6a,'shr','r8d, 1');need(patch,0x59cc6d,'and','r8b, 1')
need(patch,0x59cc91,'cmp','r9d, 2');need(patch,0x59cc9b,'test','r8b, r8b');need(patch,0x59cc9e,'je','0x59ccfc')
need(patch,0x59ccfc,'shr','ebx, 6');need(patch,0x59ccff,'and','bl, 1');need(patch,0x59cd07,'mov','r9d, dword ptr [r12 + 0x14]')
need(patch,0x59cd0c,'je','0x59cd14');need(patch,0x59cd14,'mov','qword ptr [rdx], r13')
need(patch,0x59cd1d,'mov','rdx, qword ptr [rsp + 0x38]');need(patch,0x59cd25,'call','qword ptr [rax + 0x40]')
need(call,0x60f3df,'mov','r8d, r9d');need(call,0x60f3e2,'mov','rdx, r10');need(call,0x60f3e5,'mov','rcx, r11')
need(call,0x60f3e8,'jmp','rax');need(call,0x60f284,'call','0x60efe0');need(call,0x60f289,'xor','eax, eax')
need(setter,0x60effb,'jns','0x60f012');need(setter,0x60effd,'mov','eax, 5')
need(setter,0x60f012,'mov','rcx, qword ptr [rcx + 8]');need(setter,0x60f016,'cmp','rcx, rsi');need(setter,0x60f019,'je','0x60f031')
need(setter,0x60f01b,'mov','edx, dword ptr [rdi]');need(setter,0x60f01d,'mov','eax, edx');need(setter,0x60f01f,'shr','eax, 0x1f')
need(setter,0x60f022,'not','al');need(setter,0x60f024,'test','al, 1');need(setter,0x60f028,'btr','edx, 0x1f')
need(setter,0x60f026,'je','0x60f031');need(setter,0x60f02c,'call','0x5f03a0')
need(setter,0x60f031,'bts','ebx, 0x1f');need(setter,0x60f035,'mov','qword ptr [rdi + 8], rsi')
need(setter,0x60f040,'mov','dword ptr [rdi], ebx')
need(cleanup,0x5f03a0,'test','rcx, rcx');need(cleanup,0x5f03a3,'je','0x5f0407');need(cleanup,0x5f0407,'ret','')
facts=json.loads((source/'softedges-elements-callback-source-01/facts.json').read_text())
if facts['assignment']!='0x60f3d0' or facts['callback']!='0x60f280' or facts['vtable']!='0xd4bd30':raise ValueError('conditional callback identity changed')
pins.append(dict(path='softedges-elements-callback-source-01/facts.json',sha256=sha((source/'softedges-elements-callback-source-01/facts.json').read_bytes())))
results=[]
for negative in (False,True):
 for null_source in (False,True):
  for borrowed_old in (False,True):
   results.append(dict(negative_count=negative,source_is_null=null_source,old_count_borrowed=borrowed_old,
    cleanup_called=not negative and not null_source and not borrowed_old,
    cleanup_argument='NULL' if not negative and not null_source and not borrowed_old else 'not called',
    pointer_after='NULL (preclear retained)' if negative else 'new source',
    count_after='unchanged old count' if negative else 'new count | 0x80000000',
    callback_normal_return=0))
result=dict(status='PRODUCER_CHECKED_CONDITIONAL_PROOF_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',
 question='When does reached59CD14 clear the same array+8 slot60EFE0 reads, and can its cleanup release old array storage?',
 hypotheses=['matching currentF4/slot: preclear makes observed old pointerNULL','different/rebound ownerF4 or supplied-object identity: no same-slot proof'],
 choice='Original ABI, branch and DWORD address arithmetic settle this conditional claim without sampling/game; natural state and no-rebind history remain separate.',
 exe_sha256=SHA,source_pins=pins,
 observations=[
  '6372A0 normal leaf returns02CF8270. Registrar5EEB90/95/AC sends it as arg6;632DD1/DA store it at descriptor+78.',
  '6373D0 normal return is01F2E330, sent through RDX/arg2 to descriptor+70 at632DD6; its lazy-init effects are unproved. Old private capture/root-getter wording was wrong; original bytes/results retained unchanged.',
  'Named descriptor02CEA460 constructor arg7=0 -> F0=0; constructor zerosF4/F8. Recompute63E410 for current ownF0=0,parent02CF8270 adds only own0, then excludes the root before reading itsF0. This provesF4=0 under those CURRENT metadata conditions, not arbitrary later invariance.',
  'Reached kind2, bit1clear/bit6clear path writesNULL at suppliedObject+sext32((memberOffset-ownerF4)mod2^32) at59CD14 before passing suppliedObject directly to registered callback.',
  'For memberOffset8, equality with suppliedObject+8 holds iff current ownerF4DWORD=0: signed result8 iff DWORD result8 iff8-F4=8 modulo2^32. No finite sample or general overlap-safety claim is needed.',
  'Under same-slot/no-intervening-writer/readable-state premises, nonnegative setter readsNULL. NewsourceNULL skips cleanup; newsource nonnull with borrowed old count skips cleanup; owned old count calls5F03A0(NULL,maskedCount), which branches directly toRET and accesses no object memory/callee.',
  'RET still consumes the stack return address. No RAX value assertion for cleanup. Nonnegative setter then writes new pointer and borrowed count; it cannot free the preclear-overwritten old pointer through this cleanup path.',
  'Negative count still sees the prior preclear, but60EFE0 returns5 before array read/count store;60F280 suppresses status to0. Thus composed pointer patcher may clear the pointer despite callback0 and unchanged count. Standalone setter no-write proof remains valid.'
 ],address_identity_proof='F4DWORD==0 iff sext32((8-F4)mod2^32)==8; pointer additions modulo64 do not change this equality.',
 exhaustive_path_partition=results,
 assumptions=['Matching native m_els member currently has offset8,kind2,flags bit1/6clear,owner02CEA460; getter16D680/slot40 and registered callback identities unchanged',
              'Normal reached branch includes59CC38; Windows x64 nonvolatile-register preservation; supplied object remains the same; no write/alias interferes between preclear and setter read',
              'CURRENT ownerF4=0, justified by fresh normal constructor or ownF0=0,parent02CF8270 recomputation plus no later metadata change; not assumed universally',
              'Valid readable/writable array and ABI/stack; callback/cleanup return normally'],
 affected_claims=['PhyreText pointer keys22/27 conditional assignment effects','Shader-array callback ownership/negative-count boundary','Original class-descriptor parent/sub-object andF4 prerequisite attribution'],
 limitations=['Not live state, shipping load success, initialized pointer identity/lifetime or natural reachability','Constructor/recompute are analyzed, not executed; external/lazy-init effects and all later F4 writers not closed','No full function effects inventory, alias safety, generalnonnull cleanup or universal allocation-leak assertion','Prior field/member/key independent reviews and canonical consumption remain separate'],
 native_runs=0,live_runs=0,checker_sha256=sha(pathlib.Path(__file__).read_bytes()))
out.write_text(json.dumps(result,indent=2)+'\n');print('Conditional same-slot/NULL-cleanup proof; parent attribution corrected; negative count retains preclear. Independent pending.')
