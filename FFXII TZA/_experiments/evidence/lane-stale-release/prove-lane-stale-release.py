"""Static local release retry proof, derived from verified shipping instructions.

Fresh result [disposable source]. Boolean partitions are symbolic instruction
branch consequences; they are not native executions or natural stale histories.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('lane_proof','prove-title-queue-consumption.py');S=module('lane_roles','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-lane-stale-release.py';st=json.loads((src/'lane-stale-release-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not (src/'lane-stale-release-capture-01.stdout').read_bytes().strip() or (src/'lane-stale-release-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'lane-stale-release-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    def read(a,n):
        for _,va,rs,ro in sec:
            if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise ValueError('original range unbacked')
    for q in v['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,z-a):raise ValueError('reference byte identity changed')
    cfgs=[P.closed(ix,a,z) for a,z in [(0x2e4e50,0x2e4f34),(0x2eafa0,0x2eb027),(0x2eb890,0x2eb923),(0x2e6a80,0x2e6b0d),(0x2e2660,0x2e26e8)]]
    ops=[
      (0x2e4e5a,'movzx','esi, cx'),(0x2e4e5d,'sar','ecx, 0x10'),(0x2e4e60,'movzx','eax, cx'),
      (0x2e4e63,'lea','rbx, [rax + rax*8]'),(0x2e4e67,'shl','rbx, 5'),
      (0x2e4e7b,'movsx','rax, word ptr [rbx + 0x22]'),(0x2e4e8a,'xor','edi, edi'),(0x2e4e93,'js','0x2e4eb0'),
      (0x2e4ea6,'mov','eax, dword ptr [rbx + 0x5c]'),(0x2e4ea9,'cmp','dword ptr [rcx + 0x24], eax'),(0x2e4eac,'cmove','rdi, rcx'),
      (0x2e4eb5,'mov','ecx, esi'),(0x2e4eb7,'mov','ebp, 1'),(0x2e4ebc,'shl','ebp, cl'),(0x2e4ebe,'or','dword ptr [rbx + 0x24], ebp'),
      (0x2e4ec1,'mov','eax, ebp'),(0x2e4ec3,'not','eax'),(0x2e4ec5,'and','dword ptr [rbx + 0x34], eax'),(0x2e4ec8,'test','rdi, rdi'),
      (0x2e4ecb,'je','0x2e4f10'),(0x2e4eFA,'call','0x41e580'),(0x2e4eff,'test','dword ptr [rbx + 0x2c], ebp'),
      (0x2e4f02,'je','0x2e4f1a'),(0x2e4f04,'mov','ecx, dword ptr [rdi + 0x14]'),(0x2e4f07,'mov','edx, esi'),(0x2e4f09,'call','0x2eb890'),
      (0x2e4f10,'mov','edx, esi'),(0x2e4f12,'mov','rcx, rbx'),(0x2e4f15,'call','0x2eafa0'),
      (0x2eafa0,'mov','r8, rcx'),(0x2eafa3,'mov','ecx, edx'),(0x2eafa5,'mov','edx, 1'),(0x2eafaa,'shl','edx, cl'),
      (0x2eafac,'mov','ecx, dword ptr [r8 + 0x2c]'),(0x2eafb0,'test','edx, ecx'),(0x2eafb2,'jne','0x2eb026'),
      (0x2eafb4,'mov','eax, dword ptr [r8 + 0x34]'),(0x2eafb8,'or','eax, dword ptr [r8 + 0x28]'),(0x2eafbc,'mov','r9d, dword ptr [r8 + 0x24]'),
      (0x2eafc0,'or','eax, r9d'),(0x2eafc3,'test','edx, eax'),(0x2eafc5,'je','0x2eb026'),(0x2eafc7,'or','ecx, edx'),
      (0x2eafc9,'mov','dword ptr [r8 + 0x2c], ecx'),(0x2eafcd,'test','edx, r9d'),(0x2eafd0,'je','0x2eb026'),
      (0x2eafd2,'mov','rcx, qword ptr [rip + 0x1e74db7]'),(0x2eb01f,'mov','qword ptr [rip + 0x1e74d6a], rax'),(0x2eb026,'ret',''),
      (0x2eb890,'movsxd','r8, edx'),(0x2eb895,'js','0x2eb922'),(0x2eb8f3,'cmp','dword ptr [rdx + 0x5c], ecx'),(0x2eb8f6,'jne','0x2eb922'),
      (0x2eb8f8,'lea','rcx, [rdx + r8*2]'),(0x2eb8fc,'dec','word ptr [rcx + 0xe0]'),(0x2eb903,'cmp','word ptr [rcx + 0xe0], 0'),
      (0x2eb90b,'jg','0x2eb922'),(0x2eb90d,'mov','eax, dword ptr [rdx + 0x3c]'),(0x2eb910,'or','eax, dword ptr [rdx + 0x38]'),
      (0x2eb913,'bt','eax, r8d'),(0x2eb917,'jae','0x2eb922'),(0x2eb919,'xor','eax, eax'),(0x2eb91b,'mov','word ptr [rcx + 0xe0], ax'),
      (0x2e6aa0,'test','dword ptr [rdi + 0x2c], ebx'),(0x2e6aa3,'je','0x2e6ab4'),(0x2e6aa5,'test','dword ptr [rdi + 0x24], ebx'),
      (0x2e6aa8,'je','0x2e6ab4'),(0x2e6aaf,'call','0x2e6e30'),(0x2e6ab8,'cmp','esi, 0x20'),(0x2e6abb,'jl','0x2e6aa0'),
      (0x2e6abd,'lea','rax, [rdi + 0x10]'),(0x2e6ade,'mov','qword ptr [rax + 8], 0'),(0x2e6ae6,'mov','qword ptr [rax], 0'),
      (0x2e6aed,'mov','eax, dword ptr [rdi + 0x28]'),(0x2e6af0,'or','eax, dword ptr [rdi + 0x24]'),(0x2e6af3,'jne','0x2e6afd'),
      (0x2e2660,'mov','rdx, qword ptr [rip + 0x1e7d709]'),(0x2e26c6,'mov','dword ptr [rdx + 0x5c], ecx'),
      (0x2e26d1,'mov','qword ptr [rdx + 0x28], r11'),(0x2e26d5,'mov','dword ptr [rdx + 0x24], r11d'),(0x2e26d9,'mov','qword ptr [rdx + 0x30], r11')]
    for pc,m,a in ops:P.need(ix,pc,m,a)
    # Exact requested-already-set path before the branch and terminal RET.
    early=[ix[a] for a in sorted(ix) if 0x2eafa0<=a<=0x2eafb2]+[ix[0x2eb026]]
    if any(i['mnemonic']=='call' or any(m['role'] in ['w','rw'] for m in i['memory']) for i in early):raise ValueError('request retry early footprint changed')
    helper=[i for a,i in ix.items() if 0x2eb890<=a<0x2eb923]
    hw=[(i['pc'],m['base'],m['displacement'],m['size']) for i in helper for m in i['memory'] if m['role'] in ['w','rw']]
    if hw!=[('0x2eb8fc','rcx',0xe0,2),('0x2eb91b','rcx',0xe0,2)] or any(i['mnemonic']=='call' for i in helper):raise ValueError('count helper has other writes/calls')
    if ix[0x2eb01f]['memory'][0]['rip_target']!='0x215fd90':raise ValueError('queue head identity changed')
    partitions=[]
    for requested in [False,True]:
        for loaded in [False,True]:
            for pending_or28 in [False,True]:
                # Each arm is pinned to TEST/JNE, TEST/JE, MOV2C, TEST/JE and headstore above.
                decision='already_requested_early' if requested else 'inactive_early' if not loaded and not pending_or28 else 'mark_pending_no_enqueue' if not loaded else 'mark_and_enqueue'
                branches=['0x2eafb2->0x2eb026'] if requested else ['0x2eafb2 fallthrough','0x2eafc5->0x2eb026'] if decision=='inactive_early' else ['0x2eafb2 fallthrough','0x2eafc5 fallthrough','0x2eafd0->0x2eb026'] if not loaded else ['0x2eafb2 fallthrough','0x2eafc5 fallthrough','0x2eafd0 fallthrough','0x2eb01f headstore']
                partitions.append(dict(requested=requested,loaded=loaded,pending_or28=pending_or28,decision=decision,branches=branches))
    result=dict(status='PRODUCER_VALID_CONDITIONAL_STALE_LANE_NO_ENQUEUE_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfgs=cfgs,request_partition=partitions,early_retry_pcs=[i['pc'] for i in early],early_retry_calls_or_memory_writes=0,helper_memory_writes=hw,
      established=[
      '2E4E50 resolves a nullable owner from node index/generation, sets loaded+24 and clears pending+34 BEFORE testing owner. Stale/null-owner arm passes same sub-record RBX and lane ESI to2EAFA0, skipping registration/unpin and2EB890 locally.',
      '2EAFA0 computes the lane mask and tests requested+2C FIRST. If already set, it returns with no call or memory write, regardless of newly loaded+24. Therefore under unchanged requested bit this stale completion does not enqueue, and cannot create sweep membership if it was absent before the callback. It also does not unlink existing membership.',
      'Positive distinguishing arm: requested0 and loaded1 sets requested and links sub-record+10 to sweep head0215FD90. Requested0/pending-or28 but unloaded marks requested without enqueue; inactive lane is unchanged. These exact branch cases differ from an idempotent request-that-always-requeues.',
      '2EB890 is not a repair enqueue: it searches owner by boundId, requires nonnegative index and matching generation, then decrements lane signed-WORD count+E0. Only with resulting signed count<=0 and selected bit in+38|+3C does it clamp to0. It has no call, no global or queue-node write. It is called on valid-owner/nonzero-handle/requested branch, not stale-owner completion.',
      'Reached2E6A80 calls lane release only for requested AND loaded across32 lanes, then locally unlinks its sweep node irrespective of remaining pending+34. This can leave a conditional later-completion relink requirement; external callee effects, queue head walker and actual interleaving are not assumed.',
      '2E2660 pops free head0215FD70, binds node/generation and clears loaded/requested/pending masks. It has no call or direct sweephead0215FD90 store. This is a local allocator fact, not proof that every subsequent pending request remains outside the sweep.'],
      refuted=['Direct stale completion always enqueues a previously requested lane once loaded becomes1','2EB890 is itself the deferred-release sweep enqueue helper'],
      unresolved=['Natural reachability of requested-pending then stale-node combination','Other enqueue producers/queue scheduling and eventual release/lifetime progress','Actual handle pin/free effects on stale arm and all wholeOV21/OV25 claims'],
      limitations=['Valid sub-record/node/metadata and lane0..31; callback low16 lane and16-bit record index have no universal malformed-input upper-bound proof','Normal ABI/returns and no interfering writes; static paths/Boolean partitions are not native executions or live observations','Prior queue membership variable; no unconditional leak or impossibility claim and no reuse/lifetime guarantee','Only named local bodies; opaque callee effects, external aliases, relinks and natural sequencing unproved','Producer evidence, independent acceptance and canonical incorporation remain separate; prior peer censuses are not tests run here'],
      affected_claims=['OV25 carried stale-node release-request completion/list obligation','FABLE lane ownership semantics','OPUS direct-release retry/precondition contracts','FRONTIER OV21 source lifetime preparation'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-lane-stale-release.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','lane-stale-release-capture-01.status.json','lane-stale-release-capture-01.stdout','lane-stale-release-capture-01.stderr']],
      next_discriminator='If consumer needs natural eventual-release closure, trace actual listhead/node relink producers and lifetime/callback invariant; do not launch gameplay to sample absence',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Finite read-only capture/proof and private controls, no game/PC/native/instrument/save/config/reference/peer changes')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Conditional requested-before-stale completion cannot directly enqueue; lane count helper is not list repair')
if __name__=='__main__':main()
