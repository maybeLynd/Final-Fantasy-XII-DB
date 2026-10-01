"""Original local mask04 producer; original instruction order, no natural-state claim."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('account_proof','prove-title-queue-consumption.py');S=module('account_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    driver=src/'capture-handle-accounting-qualification.py'
    st=json.loads((src/'handle-accounting-qualification-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('capture failed/stale')
    if not (src/'handle-accounting-qualification-capture-01.stdout').read_bytes().strip() or (src/'handle-accounting-qualification-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'handle-accounting-qualification-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(driver):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    expected=[(0x36c5d0,0x36c61f),(0x369800,0x369855)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=expected:raise ValueError('named boundaries changed')
    for q,(a,z) in zip(v['ranges'],expected):
        raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if raw!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')

    cfg=P.closed(ix,0x36c5d0,0x36c61f)
    ops=[(0x36c5d0,'movsxd','r8, edx'),(0x36c5d3,'test','ecx, ecx'),(0x36c5d7,'test','cl, 3'),
      (0x36c5dc,'cmp','ecx, 0x100000'),(0x36c5e6,'mov','eax, 0xfffffffc'),(0x36c5eb,'and','rdx, rax'),
      (0x36c5f0,'mov','rdx, qword ptr [rdx + 8]'),(0x36c5f9,'movzx','eax, byte ptr [rdx + 0x17]'),
      (0x36c5fd,'cmp','eax, r8d'),(0x36c600,'je','0x36c614'),(0x36c602,'mov','ecx, dword ptr [rdx + 0x18]'),
      (0x36c605,'lea','r9, [rip + 0x1f6c804]'),(0x36c60c,'sub','dword ptr [r9 + rax*4], ecx'),
      (0x36c610,'add','dword ptr [r9 + r8*4], ecx'),(0x36c614,'xor','eax, eax'),
      (0x36c616,'mov','byte ptr [rdx + 0x17], r8b'),(0x36c61a,'mov','word ptr [rdx + 0x3e], ax'),
      (0x369815,'mov','eax, 0xfffffffc'),(0x36981a,'and','rcx, rax'),(0x369824,'mov','rbx, qword ptr [rcx + 8]'),
      (0x369828,'call','0x36a9c0'),(0x36982d,'test','rbx, rbx'),(0x369832,'lea','rcx, [rbx + 0x40]'),
      (0x36983b,'xor','edx, edx'),(0x369846,'jmp','0x369860')]
    for pc,m,args in ops:P.need(ix,pc,m,args)
    if cfg['calls'] or ix[0x36c605]['memory'][0]['rip_target']!='0x22d8e10':raise ValueError('accounting footprint identity changed')
    writes=[dict(pc=i['pc'],mnemonic=i['mnemonic'],args=i['args'],memory=m) for pc,i in ix.items() if 0x36c5d0<=pc<0x36c61f for m in i['memory'] if m['role'] in ['w','rw']]
    if [x['pc'] for x in writes]!=['0x36c60c','0x36c610','0x36c616','0x36c61a'] or [x['memory']['role'] for x in writes]!=['rw','rw','w','w']:raise ValueError('complete leaf write set changed')
    todo=[0x369800];seen=set();tails=[];calls=[];returns=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not 0x369800<=pc<0x369855:raise ValueError('unclosed free-entry CFG')
        seen.add(pc);i=ix[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if m=='ret':returns.append(hex(pc));continue
        if m=='jmp':
            if pc!=0x369846 or i['args']!='0x369860':raise ValueError('unknown free tail')
            tails.append(dict(pc=hex(pc),target=i['args']));continue
        if m.startswith('j'):todo.append(int(i['args'],16))
        if m=='call':calls.append(dict(pc=hex(pc),target=i['args']))
        todo.append(n)
    if seen!={pc for pc in ix if 0x369800<=pc<0x369855}:raise ValueError('unchecked free-entry bytes')
    if calls!=[dict(pc='0x369828',target='0x36a9c0')]:raise ValueError('free-entry opaque call changed')
    td=src/'capture-handle-access-release.py';ts=json.loads((src/'handle-access-release-capture-01.status.json').read_text())
    if ts.get('exit')!=0 or ts.get('driver_sha256')!=P.sha(td):raise ValueError('tree capture failed/stale')
    if not (src/'handle-access-release-capture-01.stdout').read_bytes().strip() or (src/'handle-access-release-capture-01.stderr').read_bytes().strip():raise ValueError('tree capture incomplete')
    tree,ti=P.load(src,'handle-access-release-source-01.json',pins);S.validate(tree)
    if tree.get('invocation_driver_sha256')!=P.sha(td) or [(q['start'],q['end_exclusive']) for q in tree['ranges']]!=[('0x36d170','0x36d1f5')]:raise ValueError('tree source identity changed')
    for q in tree['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        rb=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if rb!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('tree reference changed')
    tcfg=P.closed(ti,0x36d170,0x36d1f5)
    for pc,m,args in [(0x36d196,'mov','rbx, qword ptr [rdx + 8]'),(0x36d19a,'movzx','eax, word ptr [rbx + 0x1c]'),(0x36d19e,'cmp','word ptr [rdx + 6], ax'),(0x36d1a2,'jne','0x36d1eb'),(0x36d1a4,'test','byte ptr [rbx + 0x15], 2'),(0x36d1a8,'jne','0x36d1eb'),(0x36d1b3,'xor','edi, edi'),(0x36d1d9,'call','0x36b410'),(0x36d1de,'or','byte ptr [rbx + 0x15], 2'),(0x36d1e2,'mov','word ptr [rbx + 0x3e], di')]:P.need(ti,pc,m,args)
    if tcfg['calls']!=[dict(pc='0x36d1d9',target='0x36b410')]:raise ValueError('tree opaque insertion boundary changed')
    rp=src/'handle-accounting-retained-provenance-01.json';prov=json.loads(rp.read_text())
    for q in prov['members']:
        if P.sha(src/q['local_path'])!=q['sha256']:raise ValueError('retained member changed')
    retained,ri=P.load(src,'handle-accounting-retained-namebinding-deletion-source-01.json',pins);S.validate(retained)
    for q in retained['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        rb=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if rb!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('retained reference changed')
    callback=[i for p,i in sorted(ri.items()) if 0x2e4d20<=p<0x2e4dfe]
    P.need(ri,0x2e4d4b,'mov','esi, dword ptr [rdi + 0x10]')
    P.need(ri,0x2e4d87,'mov','ecx, esi')
    P.need(ri,0x2e4d89,'call','0x36d170')
    if any(i['mnemonic']=='call' and i['args']=='0x36c5d0' for i in callback):raise ValueError('unexpected accounting call in retained completion')
    prior=json.loads((src/'handle-accounting-retained-namebinding-deletion-result-01.json').read_text())
    affected=json.loads((src/'handle-accounting-affected-consumers-01.json').read_text())
    old=prior['established'][1]
    if old!=affected['original_affected_claim'] or 'unpins its backing' not in old:raise ValueError('affected semantic preimage changed')
    new=old.replace('unpins its backing','calls36D170(backingHandle), conditionally restoring relocation-tree membership under the slot/header stamp and header15mask02 guards')
    qualified=dict(prior)
    qualified.update(status='QUALIFIED_LOCAL_DELETION_RULES_INDEPENDENT_PENDING',established=[new if k==1 else x for k,x in enumerate(prior['established'])],original_result_sha256=P.sha(src/'handle-accounting-retained-namebinding-deletion-result-01.json'),semantic_addendum='Actual36D170 tree access release differs from36C5D0 accounting reclassification. Neither local proof establishes protective refcount lifetime or IO drain. Original bytes/order/flags/refusal controls unchanged; no re-execution credit. First erroneous accounting-callback assumption refused before output; preserved addendum02.',qualification_checker_sha256=P.sha(pathlib.Path(__file__)))
    normalized=out.with_name('namebinding-deletion-qualified-02.json')
    if normalized.exists():raise ValueError('immutable normalized result exists')
    rows=[dict(old=o,new=n,counter_delta='none' if o==n else 'subtract payload bytes fromold/add tonew modulo2^32',header17=n,header3E=0) for o in [0,1] for n in [0,1]]
    receipts=['capture-handle-accounting-qualification.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','handle-accounting-retained-provenance-01.json','handle-accounting-retained-namebinding-deletion-result-01.json','handle-accounting-affected-consumers-01.json','handle-accounting-method-addendum-01.json','handle-accounting-method-addendum-02.json','capture-handle-access-release.py','handle-access-release-capture-01.status.json','handle-access-release-capture-01.stdout','handle-access-release-capture-01.stderr','prove-handle-accounting-qualification.py','handle-accounting-qualification-positive-01.status.json','handle-accounting-qualification-positive-01.stdout','handle-accounting-qualification-positive-01.stderr','handle-accounting-qualification-capture-01.status.json','handle-accounting-qualification-capture-01.stdout','handle-accounting-qualification-capture-01.stderr']
    result=dict(status='PRODUCER_VALID_ACCOUNTING_QUALIFICATION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_accounting_cfg=cfg,normal_access_release_cfg=tcfg,accounting_memory_writes=writes,free_entry_cfg=dict(instructions=len(seen),calls=calls,tails=tails,returns=returns),category_bit_partition=rows,
      established=['36C5D0 takes a signed32 new accounting index inEDX, masks low32 handle to a slot and obtains its header through slot+8. With valid slot/header it compares oldBYTE+17 with new index, transfers DWORD payload-length accounting from022D8E10[old] to[new] when unequal, then stores header+17=new lowBYTE and clears WORD+3E even when index equal.',
        'Complete79B leaf has exactly counter SUB/ADD, header17 store and guard3E clear as memory writes, and no calls. It does not increment/decrement a protective reference count, cancel/drain IO or establish a lifetime retention policy. Arbitrary indices, invalid mapped handles and alias/interference safety are not established.',
        '369800 free entry masks its handle, saves slot+8 header, calls36A9C0 and conditionally tail-calls369860(header+40,0). It does not directly inspect accounting+17 to gate that tail. Opaque helper effects and full physical reclamation remain separate; no universal free-success claim.',
        'Retained full original2E4D20 calls36D170(backingHandle) at2E4D89, not36C5D0.36D170 checks slot+6/header+1C stamp and absent header15mask02, calls tree insertion36B410, sets mask02 and clears guard3E. Existing allocator semantics identify this as return-to-relocation-tree access release. Earlier own unpins wording is qualified to that operation; no protective lifetime/refcount/drain conclusion follows.',
        'Current canonical allocator accounting model already records this as category classification. No canonical index regression is asserted. Historical producer/result/README/method remain immutable; deterministic normalized02 applies the exact additive correction and pins its original preimage.'],
      affected_claims=['namebinding-deletion published result01 established[1], README, producer/freezer emitted unpins prose and method hypothesis','Existing FABLE/OPUS namebinding-deletion consumers and SPEC review must include normalized02','Runtime lifetime preparation must not use these calls as a protective pin/unpin barrier'],
      limitations=['Current canonical model is prior peer evidence, not new ASTRA census/tests or automatic acceptance of this application','Header slot+8 identity valid premise; this leaf has no stamp comparison and no generic pointer/ID safety','Accounting domain0/1 is scoped to these relevant calls; wider caller census not rerun','No full369860 reclamation, relocation, actual asynchronous lifetime, old request reuse or game observation proof','Producer/semantic correction remains pending independent review/consumer agreement'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],normalized_result=dict(path=normalized.name,sha256=hashlib.sha256((json.dumps(qualified,indent=2)+'\n').encode()).hexdigest()),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Finite original reads and scoped deterministic semantic overlay; published history/peer pages unchanged')
    with normalized.open('xb') as f:f.write((json.dumps(qualified,indent=2)+'\n').encode())
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Actual completion returns access to relocation tree; distinct accounting primitive and additive02')
if __name__=='__main__':main()
