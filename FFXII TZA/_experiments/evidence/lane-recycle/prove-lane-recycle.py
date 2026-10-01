"""Conditional callback-ticket/recycler rules from verified original code.

Fresh result [disposable source]. No outstanding-IO inference from pending bits.
No natural stale callback, allocator effect or scheduling claim from this proof.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('recycle_proof','prove-title-queue-consumption.py');S=module('recycle_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-lane-recycle.py';st=json.loads((src/'lane-recycle-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not (src/'lane-recycle-capture-01.stdout').read_bytes().strip() or (src/'lane-recycle-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    provenance=json.loads((src/'lane-recycle-retained-provenance-01.json').read_text())
    if provenance.get('retained_sha256')!=P.sha(src/'lane-recycle-retained-source-01.json') or provenance.get('status')!='IMMUTABLE_QUALIFIED_SOURCE_REUSED':raise ValueError('retained source changed/missing')
    pins=[];v,ix=P.load(src,'lane-recycle-source-01.json',pins);S.validate(v)
    old,oi=P.load(src,'lane-recycle-retained-source-01.json',pins);S.validate(old)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture provenance changed')
    if set(ix).intersection(oi):raise ValueError('mixed overlapping source')
    ix.update(oi)
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    def read(a,n):
        for _,va,rs,ro in sec:
            if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise ValueError('original range unbacked')
    for q in v['ranges']+old['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,z-a):raise ValueError('reference byte identity changed')
    cfgs=[P.closed(ix,a,z) for a,z in [(0x2e6eb0,0x2e7072),(0x2e9470,0x2e9552),(0x2e4000,0x2e4145),(0x2e4e50,0x2e4f34),(0x2e2660,0x2e26e8),(0x2e6a80,0x2e6b0d)]]
    ops=[
      (0x2e6ede,'mov','rbx, rcx'),(0x2e6fc3,'movzx','ecx, word ptr [rbx + 0x20]'),(0x2e6fc7,'shl','ecx, 0x10'),(0x2e6fca,'or','ecx, esi'),
      (0x2e6fb3,'lea','rdx, [rip - 0x216a]'),(0x2e6fcc,'mov','qword ptr [rsp + 0x40], rdx'),(0x2e6fd6,'mov','dword ptr [rsp + 0x38], ecx'),
      (0x2e700c,'call','0x32e620'),(0x2e6ee1,'rol','edi, 0'),(0x2e6ef1,'mov','ebp, 1'),(0x2e6ef6,'jne','0x2e7032'),
      (0x2e7036,'and','dword ptr [rbx + 0x28], eax'),(0x2e703d,'or','dword ptr [rbx + 0x34], edi'),(0x2e7048,'cmp','esi, 0x20'),
      (0x2e4e5a,'movzx','esi, cx'),(0x2e4e5d,'sar','ecx, 0x10'),(0x2e4e60,'movzx','eax, cx'),
      (0x2e4e63,'lea','rbx, [rax + rax*8]'),(0x2e4e67,'shl','rbx, 5'),(0x2e4e7b,'movsx','rax, word ptr [rbx + 0x22]'),
      (0x2e4ea6,'mov','eax, dword ptr [rbx + 0x5c]'),(0x2e4ea9,'cmp','dword ptr [rcx + 0x24], eax'),(0x2e4eac,'cmove','rdi, rcx'),
      (0x2e4ebe,'or','dword ptr [rbx + 0x24], ebp'),(0x2e4ec5,'and','dword ptr [rbx + 0x34], eax'),
      (0x2e6aed,'mov','eax, dword ptr [rdi + 0x28]'),(0x2e6af0,'or','eax, dword ptr [rdi + 0x24]'),(0x2e6af3,'jne','0x2e6afd'),
      (0x2e6af5,'mov','rcx, rdi'),(0x2e6af8,'call','0x2e9470'),
      (0x2e9470,'test','rcx, rcx'),(0x2e9479,'movsx','rax, word ptr [rcx + 0x22]'),(0x2e949a,'cmp','dword ptr [rdx + 0x24], eax'),
      (0x2e949f,'mov','word ptr [rdx + 0x1e], r8w'),(0x2e94a7,'mov','word ptr [rcx + 0x22], r8w'),
      (0x2e954a,'mov','qword ptr [rip + 0x1e7681f], rcx'),(0x2e9551,'ret',''),
      (0x2e2673,'lea','r8, [rdx + 0x60]'),(0x2e2690,'mov','dword ptr [r8], r11d'),(0x2e267e,'mov','r9d, 0x20'),
      (0x2e26c6,'mov','dword ptr [rdx + 0x5c], ecx'),(0x2e26d9,'mov','qword ptr [rdx + 0x30], r11'),
      (0x2e40a0,'mov','edx, dword ptr [rax + 0x2c]'),(0x2e40a3,'test','r8d, edx'),(0x2e40a6,'jne','0x2e4112'),
      (0x2e410b,'mov','qword ptr [rip + 0x1e7bc7e], rcx')]
    for pc,m,a in ops:P.need(ix,pc,m,a)
    if ix[0x2e6fb3]['memory'][0]['rip_target']!='0x2e4e50' or ix[0x2e954a]['memory'][0]['rip_target']!='0x215fd70':raise ValueError('callback/free head identity changed')
    recycler=[i for a,i in ix.items() if 0x2e9470<=a<0x2e9552]
    if any(i['mnemonic']=='call' for i in recycler):raise ValueError('unexpected recycler callee')
    # The complete, byte-validated recycler has no [record+34] pending access.
    pending=[i['pc'] for i in recycler for m in i['memory'] if m['base']=='rcx' and m['displacement']==0x34]
    if pending:raise ValueError('recycler pending guard/access changed')
    body=[i for a,i in ix.items() if 0x2e9470<=a<0x2e9552]
    rcx_writes=[i['pc'] for i in body if i['args'].split(',')[0] in ['rcx','ecx','cx','cl','ch'] and i['mnemonic'] not in ['cmp','test']]
    if rcx_writes:raise ValueError('recycler record carrier changed')
    rdi=[i for a,i in ix.items() if 0x2e6aa0<=a<=0x2e6af8 and i['args'].split(',')[0] in ['rdi','edi','di','dil'] and i['mnemonic'] not in ['cmp','test']]
    if rdi!=[]:raise ValueError('sweep carrier changed')
    result=dict(status='PRODUCER_VALID_CURRENT_METADATA_TICKET_AND_LOCAL_RECYCLE_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfgs=cfgs,recycler_pending_accesses=pending,recycler_calls=0,ticket_formula='(u16(subrecord+20)<<16)|lane; receiver high16=slot,low16=lane; no submitting-generation operand',
      established=[
      '2E6EB0 constructs descriptor callback2E4E50 and DWORDargument=(u16 record+20<<16)|lane from lane0..31. No submitting-generation value is encoded in this DWORD. Receiver decodes exactly high16 sub-record index/low16 lane.',
      'Completion compares CURRENT sub-record+5C against CURRENT node+24 after reading CURRENT sub-record+22. It does not compare either against a generation carried by this ticket. This local metadata consistency check alone cannot distinguish an old ticket targeting a recycled slot whose new metadata is coherent.',
      'Reached2E6A80 tests loaded+24|mask28 before calling2E9470, not pending+34. Complete2E9470 has no call, no pending+34 access and no record-carrier change; for nonnull valid record it invalidates current node index, unlinks both nodes and pushes the same storage to free head0215FD70. Local nonzero pending alone does not prevent this push.',
      '2E2660 pops free storage, rebinds node/generation, zeroes32 lane handle slots and clears pending+34 as part of QWORD+30. It makes no release call for old lane handles. These are local allocation rules, not proof that the slot naturally recycles with outstanding IO.',
      '2E4000 is another named direct sweephead writer. For each lane it tests requested+2C and skips marking/enqueue if already set. Therefore its examined local iteration does not by itself repair the already-requested lane. Another lane or other producer may link the same shared node.',
      'Pending-mask+34 does not itself prove a newly accepted asynchronous read:2E6EB0 can set it on the nonzero existing-handle arm without a32E620 call, and its actual request-call arm sets pending AFTER32E620 returns. Queue acceptance/callback timing cannot be inferred from this field alone.'],
      refuted=['This DWORDcallback ticket explicitly contains the submitting owner generation','Examined local recycler refuses any nonzero pending mask before pushing the slot free'],
      limitations=['Normal ABI/returns, valid record/list/lane/node and no interfering writes; no malformed-state safety or pointer-placement guarantee','No natural late callback, overlapping generations, leak, crash or universal safety/unsafety claim','Current metadata consistency is distinct from original-request identity; other queue/service contracts could prevent late delivery','Composed conditional static paths are not native/live executions, accepted IO observations or full scheduler reachability','Only named local direct writer/body rules; other lanes, relinks/aliases and callers remain outside proof','Producer review and canonical consumption pending; retained source is reused without recapture and prior controls are not new runs'],
      affected_claims=['NameBindingSubRecord generation defence scope and actual recycle site','OV25 carried lane lifetime/requeue interpretation','OPUS callback-ticket/recycler/precondition contract','FRONTIER future real scheduling discriminator'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-lane-recycle.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','lane-recycle-retained-provenance-01.json','lane-recycle-capture-01.status.json','lane-recycle-capture-01.stdout','lane-recycle-capture-01.stderr']],
      next_discriminator='Original callers and accepted IO/service cancellation/drain guarantee preventing late delivery across actual slot recycle; not a pending-bit sample or forced callback',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Finite read-only reference/capture and private source controls; no game/PC/native/instrument/save/config/reference/peer changes')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Ticket is slot/lane, current generation check is not old-request identity; no local pending guard in recycler')
if __name__=='__main__':main()
