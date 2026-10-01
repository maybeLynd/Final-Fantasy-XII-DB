"""Original local mask04 producer; original instruction order, no natural-state claim."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('reentry_proof','prove-title-queue-consumption.py');S=module('reentry_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    driver=src/'capture-lane-request-reentrancy.py'
    st=json.loads((src/'lane-request-reentrancy-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('capture failed/stale')
    if not (src/'lane-request-reentrancy-capture-01.stdout').read_bytes().strip() or (src/'lane-request-reentrancy-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'lane-request-reentrancy-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(driver):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    expected=[(0x32e620,0x32e774),(0x32e870,0x32e98d),(0x32e070,0x32e149),(0x32e330,0x32e36b)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=expected:raise ValueError('named boundaries changed')
    for q,(a,z) in zip(v['ranges'],expected):
        raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if raw!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')

    cfgs=[P.closed(ix,a,z) for a,z in expected[:2]]
    t=json.loads((src/'lane-request-pump-dispatch-table-01.json').read_text())
    tb=bytes.fromhex(t['bytes']);a,z=0x32e2d0,0x32e2e8
    rb=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
    if len(tb)!=24 or rb!=tb or hashlib.sha256(tb).hexdigest()!=t['sha256'] or t.get('exe_sha256')!=P.SHA or t.get('invocation_driver_sha256')!=P.sha(driver) or t.get('start')!=hex(a) or t.get('end_exclusive')!=hex(z):raise ValueError('original pump table identity changed')
    targets=[0x120000+x for x in struct.unpack('<6I',tb)]
    if targets[0]!=0x32e0bd or [int(x['target'],16) for x in t['entries']]!=targets:raise ValueError('conditional pump state1 target changed')
    ops=[
      (0x32e656,'call','0x3eb0d0'),(0x32e65b,'test','eax, eax'),(0x32e65d,'mov','rax, qword ptr [rsp + 0x90]'),
      (0x32e665,'je','0x32e742'),(0x32e678,'movups','xmm0, xmmword ptr [rax]'),(0x32e67b,'movups','xmm1, xmmword ptr [rax + 0x10]'),
      (0x32e67f,'movups','xmmword ptr [rsp + 0x30], xmm0'),(0x32e684,'movsd','xmm0, qword ptr [rax + 0x20]'),
      (0x32e689,'movsd','qword ptr [rsp + 0x50], xmm0'),(0x32e68f,'movups','xmmword ptr [rsp + 0x40], xmm1'),
      (0x32e6b4,'lea','rax, [rsp + 0x30]'),(0x32e6c4,'mov','qword ptr [rsp + 0x20], rax'),
      (0x32e6cc,'mov','dword ptr [rsp + 0x34], 0x80000'),(0x32e6d6,'mov','qword ptr [rsp + 0x50], r14'),(0x32e6dd,'call','0x32e870'),
      (0x32e750,'mov','qword ptr [rsp + 0x20], rax'),(0x32e759,'call','0x32e870'),
      (0x32e888,'xor','ebx, ebx'),(0x32e88d,'cmp','qword ptr [rip + 0x1f9693c], rbx'),
      (0x32e8a0,'jne','0x32e8c5'),(0x32e8a8,'xor','ecx, ecx'),(0x32e8aa,'call','0x32e070'),
      (0x32e8af,'call','0x46dfe0'),(0x32e8b4,'xor','ecx, ecx'),(0x32e8b6,'call','0x35ea30'),
      (0x32e8bb,'cmp','qword ptr [rip + 0x1f9690d], 0'),(0x32e8c3,'je','0x32e8a2'),
      (0x32e8c9,'call','0x32e990'),(0x32e8ce,'mov','rcx, qword ptr [rsp + 0x60]'),
      (0x32e8db,'mov','eax, dword ptr [rcx]'),(0x32e8dd,'mov','r8, qword ptr [rcx + 0x10]'),
      (0x32e8e1,'mov','r9, qword ptr [rcx + 0x18]'),(0x32e8e5,'mov','r11d, dword ptr [rcx + 8]'),
      (0x32e951,'mov','qword ptr [r10 + 0x40], r8'),(0x32e955,'mov','qword ptr [r10 + 0x48], r9'),(0x32e961,'mov','dword ptr [r10 + 0x60], r11d'),
      (0x32e090,'mov','rbx, qword ptr [rip + 0x1f97129]'),(0x32e097,'test','rbx, rbx'),
      (0x32e0a0,'movzx','eax, byte ptr [rbx + 0x20]'),(0x32e0a4,'dec','eax'),(0x32e0a6,'cmp','eax, 5'),
      (0x32e0b1,'mov','ecx, dword ptr [rdi + rax*4 + 0x20e2d0]'),(0x32e0bb,'jmp','rcx'),
      (0x32e0bd,'call','0x3eadd0'),(0x32e0c2,'test','eax, eax'),(0x32e0c4,'jne','0x32e2a0'),
      (0x32e0ca,'mov','r8d, dword ptr [rbx + 0x28]'),(0x32e0ce,'test','r8d, r8d'),(0x32e0d1,'je','0x32e130'),
      (0x32e130,'mov','rcx, rbx'),(0x32e133,'call','0x32e330'),(0x32e13b,'mov','byte ptr [rbx + 0x20], 0'),
      (0x32e13f,'call','0x32ec40'),
      (0x32e336,'mov','rax, qword ptr [rcx + 0x40]'),(0x32e33a,'mov','rbx, rcx'),(0x32e33d,'test','rax, rax'),
      (0x32e340,'je','0x32e351'),(0x32e342,'mov','rdx, qword ptr [rcx + 0x70]'),
      (0x32e346,'mov','r8d, 1'),(0x32e34c,'mov','ecx, dword ptr [rcx + 0x60]'),(0x32e34f,'call','rax')]
    for pc,m,args in ops:P.need(ix,pc,m,args)
    if ix[0x32e88d]['memory'][0]['rip_target']!='0x22c51d0' or ix[0x32e090]['memory'][0]['rip_target']!='0x22c51c0':raise ValueError('queue object identity changed')
    if ix[0x32e67f]['memory'][0]['role']!='w' or ix[0x32e961]['memory'][0]['role']!='w':raise ValueError('actual descriptor-store roles changed')
    # Explicit closed helper including one named external tail, no global CFG relaxation.
    todo=[0x32e330];seen=set();tails=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not 0x32e330<=pc<0x32e36b:raise ValueError('unclosed done-helper CFG')
        seen.add(pc);i=ix[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if m=='ret':continue
        if m=='jmp':
            if pc!=0x32e360 or i['args']!='0x3697f0':raise ValueError('unknown done-helper tail')
            tails.append(dict(pc=hex(pc),target=i['args']));continue
        if m.startswith('j'):todo.append(int(i['args'],16))
        todo.append(n)
    if seen!={p for p in ix if 0x32e330<=p<0x32e36b}:raise ValueError('unchecked done-helper instructions')
    lv,li=P.load(src,'lane-request-retained-source-01.json',pins);S.validate(lv)
    prov=json.loads((src/'lane-request-retained-provenance-01.json').read_text())
    if P.sha(src/'lane-request-retained-source-01.json')!=prov['member_sha256']:raise ValueError('retained lane source identity changed')
    for q in lv['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        rb=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if rb!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('retained reference changed')
    for pc,m,args in [(0x2e6f0d,'mov','eax, dword ptr [rbx + 0x5c]'),(0x2e6f17,'cmp','dword ptr [rcx + 0x24], eax'),(0x2e6f1a,'cmove','r14, rcx'),(0x2e700c,'call','0x32e620'),(0x2e7011,'mov','ebp, 1'),(0x2e7016,'call','0x36c140'),(0x2e701b,'call','0x36c110'),(0x2e7039,'test','ebp, ebp'),(0x2e703b,'je','0x2e7040'),(0x2e703d,'or','dword ptr [rbx + 0x34], edi')]:P.need(li,pc,m,args)
    rereads=[dict(pc=i['pc'],memory=m) for p,i in li.items() if 0x2e700c<p<=0x2e703d for m in i['memory'] if m['base']=='rbx' and m['displacement'] in [0x22,0x5c]]
    if rereads:raise ValueError('caller direct owner revalidation changed')
    receipts=['capture-lane-request-reentrancy.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','lane-request-pump-dispatch-table-01.json','lane-request-retained-provenance-01.json','lane-request-method-addendum-01.json','lane-request-reentrancy-capture-01.status.json','lane-request-reentrancy-capture-01.stdout','lane-request-reentrancy-capture-01.stderr']
    r=dict(status='PRODUCER_VALID_CONDITIONAL_OLD_CALLBACK_WINDOW_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_request_cfgs=cfgs,done_helper_cfg=dict(instructions=len(seen),external_tails=tails),pump_extent='PREFIX_ONLY217B; conditional queuedstate1/zero-byte/gate0 path, not full pump',conditional_order=['lanecurrentownercheck2E6F17','32E620 builder','32E870 freehead0 ->32E070(0)','oldheadstate1/bytes0/gate0 ->32E330 -> callback(arg32,dest64,1)','remainingfullpoolservice/pacing/positivefreehead','32E990 newslot and descriptorfield reads/copy','builderreturn','2E703D pendingstore'],
      established=['Full32E870 calls32E070(0),46DFE0 and35EA30(0) while freehead022C51D0 is0; initial nonzero freehead bypasses that wait. Only after wait does it call32E990 and read the descriptor pointer/fields. This order is original, not a simulated-input or live observation.',
        'Under a valid nonempty oldqueue head in state1,bytes0 and3EADD0 returning0, original pump prefix selects target0 from its guarded6-entry table and calls32E330 before clearing/recycling the oldslot. NonNULL+40 callback receives ECX=userDWORD+60, RDX=destination+70, R8D=1. Thus an old queued callback can run inside fullpool retry before new descriptor adoption under these explicit conditions.',
        '32E620 ordinary gate0 path forwards the original descriptor pointer. Gate nonzero/descriptor nonNULL copies40B to stack BEFORE32E870, then overrides cap+4=80000 and partcallback+20=NULL. Original-pointer reads after the wait and pre-wait staged-copy reads are different boundaries; neither snapshot atomicity nor arbitrary alias mutation is certified.',
        'Retained lane issuer checks current owner stamp before the submission path and publishes pending+34 after32E620 returns, with36C140/36C110 calls between. Its segment contains no direct owner-index22/stamp5C reread before the pending store. ABI register preservation is not an object-lifetime revalidation.',
        'The conditional retry callback belongs to an old queued request: the new slot checkout occurs afterward. This does not prove the newlysubmitted request callbacks inline during its own wait, or that an old callback naturally mutates/recycles the same lane record.'],
      limitations=['Valid stable queue/descriptor/record storage and normal ABI-return premises; other-thread/interfering writes and aliases may invalidate sequential snapshot assumptions','Conditional old-head/gate/control state is not a shipped natural fullpool history, owner recycling witness, timing measurement or unconditional reentrancy bug','Full pump otherstates/footer, builder modegetter, allocator bookkeeping/checkout/recycler and callback bodies opaque outside selected original boundaries','Same-record latecallback/reuse and service cancellation/drain guarantee remain OPEN; no safety/leak/crash/natural reachability proof','Copied40B staging is three original load/store groups, not atomic; fullpool may loop forever if no progress, including existing BGM reentry caveat','Retained/prior queue producer runs not ASTRA test credit or independent acceptance of this application'],
      affected_claims=['Existing FABLE/OPUS lane ownership/reuse/currentowner-check semantics','Resource descriptor staging and request-call callback/revalidation preconditions'],checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,next_discriminator='Independent review/canonical call-boundary qualification; specific original oldcallback mutation/lifetime guarantee needed for natural same-record reuse, not a new game setup.',cleanup='Finite original byte/data reads and retained source composition, no game/PC/native/emulated/instrument/save/config/reference/peer mutation')
    with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print('Original fullpool oldcallback window precedes descriptor adoption and lane pending store')
if __name__=='__main__':main()
