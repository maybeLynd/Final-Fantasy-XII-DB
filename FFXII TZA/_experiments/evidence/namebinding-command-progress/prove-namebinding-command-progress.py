"""Complete bounded original command dispatch; pending != file-success evidence."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('progress_proof','prove-title-queue-consumption.py');S=module('progress_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-namebinding-command-progress.py';st=json.loads((src/'namebinding-command-progress-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not (src/'namebinding-command-progress-capture-01.stdout').read_bytes().strip() or (src/'namebinding-command-progress-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'namebinding-command-progress-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    def raw(a,z):return next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
    ext=[(0x2e60f0,0x2e62db),(0x32e4d0,0x32e512),(0x3a1290,0x3a12ce)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=ext:raise ValueError('named boundaries changed')
    for q,(a,z) in zip(v['ranges'],ext):
        if raw(a,z)!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')
    table=json.loads((src/'namebinding-command-dispatch-table-01.json').read_text())
    tb=bytes.fromhex(table['bytes'])
    if len(tb)!=36 or table.get('start')!='0x2e62dc' or table.get('end_exclusive')!='0x2e6300' or table.get('exe_sha256')!=P.SHA or table.get('imagebase')!='0x120000' or table.get('invocation_driver_sha256')!=P.sha(d) or hashlib.sha256(tb).hexdigest()!=table['sha256'] or raw(0x2e62dc,0x2e6300)!=tb:raise ValueError('original dispatch table identity changed')
    targets=[0x120000+x for x in struct.unpack('<9I',tb)]
    if targets!=[0x2e614f,0x2e614f,0x2e628c,0x2e61d3,0x2e61e2,0x2e61fb,0x2e6213,0x2e6213,0x2e629e] or [int(t['target'],16) for t in table['entries']]!=targets:raise ValueError('nine-target mapping changed')
    ops=[
      (0x2e60fa,'mov','edi, dword ptr [rcx]'),(0x2e60fc,'mov','r15, rcx'),(0x2e60ff,'mov','rsi, qword ptr [rcx + 0x28]'),
      (0x2e6103,'movzx','ebx, di'),(0x2e6106,'sar','edi, 0x10'),(0x2e6109,'cmp','ebx, 8'),(0x2e610c,'ja','0x2e62c9'),
      (0x2e6129,'movsxd','rax, edi'),(0x2e6131,'lea','r13, [rax + rax]'),(0x2e6135,'lea','r14, [r14 + rax*4]'),
      (0x2e6139,'lea','rdx, [rip - 0x1c6140]'),(0x2e6140,'movsxd','rax, ebx'),(0x2e6143,'mov','ecx, dword ptr [rdx + rax*4 + 0x1c62dc]'),
      (0x2e614a,'add','rcx, rdx'),(0x2e614d,'jmp','rcx'),
      (0x2e614f,'mov','ecx, dword ptr [rsi + 0x14]'),(0x2e6152,'call','0x2ed950'),(0x2e6157,'movzx','ecx, word ptr [rax + r13]'),
      (0x2e615c,'test','cx, cx'),(0x2e615f,'js','0x2e61c2'),(0x2e61c2,'mov','dword ptr [r14], 0xffffffff'),
      (0x2e61c9,'mov','ebx, 7'),(0x2e61ce,'jmp','0x2e6139'),(0x2e61ad,'mov','r12d, eax'),
      (0x2e61b0,'test','eax, eax'),(0x2e61b2,'jg','0x2e623e'),(0x2e61b8,'mov','ebx, 7'),(0x2e61bd,'jmp','0x2e6139'),
      (0x2e61d6,'call','0x36d200'),(0x2e61e2,'mov','ecx, dword ptr [r14]'),(0x2e61e5,'test','ecx, ecx'),
      (0x2e61e7,'je','0x2e622d'),(0x2e61e9,'call','0x3a1650'),(0x2e61ee,'mov','dword ptr [r14], eax'),
      (0x2e61f1,'cmp','eax, -1'),(0x2e61f4,'je','0x2e61b8'),(0x2e61f6,'mov','ebx, 5'),(0x2e61fe,'call','0x3a1290'),
      (0x2e6203,'cmp','eax, 2'),(0x2e6206,'jne','0x2e62b5'),(0x2e6213,'inc','edi'),(0x2e6215,'add','r14, 4'),(0x2e6219,'add','r13, 2'),
      (0x2e621d,'cmp','r13, 6'),(0x2e6221,'jge','0x2e629e'),(0x2e6223,'mov','ebx, 1'),(0x2e6228,'jmp','0x2e6140'),
      (0x2e6234,'mov','ebx, 7'),(0x2e6239,'jmp','0x2e6140'),(0x2e6277,'call','0x32e620'),
      (0x2e627f,'mov','dword ptr [r15 + 0x30], eax'),(0x2e6283,'mov','dword ptr [rsi + rcx*4 + 0x30], ebx'),
      (0x2e6287,'mov','ebx, 2'),(0x2e628c,'mov','ecx, dword ptr [r15 + 0x30]'),(0x2e6290,'call','0x32e4d0'),
      (0x2e6295,'test','eax, eax'),(0x2e6297,'jne','0x2e62b5'),(0x2e6299,'lea','ebx, [rax + 3]'),(0x2e629c,'jmp','0x2e62b5'),
      (0x2e629e,'or','byte ptr [rsi + 0x18], 2'),(0x2e62a2,'test','byte ptr [rsi + 0x18], 4'),
      (0x2e62a6,'je','0x2e62b0'),(0x2e62a8,'mov','rcx, rsi'),(0x2e62ab,'call','0x2eaeb0'),(0x2e62b0,'mov','ebx, 9'),
      (0x2e62c9,'shl','edi, 0x10'),(0x2e62cc,'or','edi, ebx'),(0x2e62ce,'mov','dword ptr [r15], edi'),
      (0x32e4d4,'cmp','ecx, -1'),(0x32e4d7,'je','0x32e50b'),(0x32e4d9,'test','ecx, ecx'),(0x32e4db,'je','0x32e504'),
      (0x32e4df,'lea','rdx, [rip + 0x1f94cda]'),(0x32e4e6,'and','eax, 0x3f'),(0x32e4e9,'shl','rax, 7'),
      (0x32e4ed,'cmp','dword ptr [rax + rdx + 0x64], ecx'),(0x32e4f1,'jne','0x32e504'),
      (0x32e4f3,'cmp','byte ptr [rax + rdx + 0x20], 0'),(0x32e4f8,'je','0x32e504'),(0x32e4fa,'mov','eax, 1'),
      (0x32e504,'xor','ecx, ecx'),(0x32e506,'call','0x16d6a0'),(0x32e50b,'xor','eax, eax'),
      (0x3a1292,'cmp','ecx, -1'),(0x3a1297,'xor','r8d, r8d'),(0x3a12ae,'movzx','ecx, word ptr [r8 + 0xa]'),
      (0x3a12b3,'btr','edx, 0x1f'),(0x3a12c1,'cmp','ecx, edx'),(0x3a12c3,'jne','0x3a12cb'),
      (0x3a12c5,'movzx','eax, byte ptr [r8 + 0xc]'),(0x3a12cb,'xor','eax, eax')]
    for pc,m,args in ops:P.need(ix,pc,m,args)
    if ix[0x2e629e]['memory'][0]['role']!='rw' or ix[0x2e627f]['memory'][0]['role']!='w' or ix[0x2e6135]['memory'][0]['role']!='addr':raise ValueError('actual roles changed')
    # Local guarded dispatch only. All table entries original; no broad indirect-CFG policy.
    todo=[0x2e60f0];seen=set();calls=[];returns=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not 0x2e60f0<=pc<0x2e62db:raise ValueError('unclosed command CFG')
        seen.add(pc);i=ix[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if m=='ret':returns.append(hex(pc));continue
        if pc==0x2e614d:todo.extend(targets);continue
        if m=='jmp':todo.append(int(i['args'],16));continue
        if m.startswith('j'):todo.append(int(i['args'],16))
        if m=='call':calls.append(dict(pc=hex(pc),target=i['args']))
        todo.append(n)
    if seen!={p for p in ix if 0x2e60f0<=p<0x2e62db}:raise ValueError('unchecked command instructions')
    # Local EBX definitions before re-dispatch are fixed, within validated nine entries.
    defs=[dict(pc=i['pc'],mnemonic=i['mnemonic'],args=i['args']) for p,i in ix.items() if 0x2e60f0<=p<0x2e62db and i['args'].split(',')[0]=='ebx' and i['mnemonic'] in ['mov','movzx','lea']]
    if {x['pc'] for x in defs}!={'0x2e6103','0x2e61b8','0x2e61c9','0x2e61f6','0x2e6223','0x2e6234','0x2e6253','0x2e6287','0x2e6299','0x2e62b0'}:raise ValueError('state register writer set changed')
    # Allocation return inEBX at6253 is overridden by2 before any dispatch/return;
    # state3 after poll and9 after ready return, not redispatch.
    leafs=[P.closed(ix,a,z) for a,z in ext[1:]]
    witness=[dict(part=k,selector=k,word_offset=2*k,subresource_offset=0x30+4*k,source_class='signed WORD<0',dispatch_states=[1,7],next_selector=k+1,next_word_offset=2*(k+1)) for k in range(3)]
    if witness[-1]['next_word_offset']!=6:raise ValueError('three-part bound derivation failed')
    receipts=['capture-namebinding-command-progress.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','namebinding-command-dispatch-table-01.json','namebinding-command-progress-capture-01.status.json','namebinding-command-progress-capture-01.stdout','namebinding-command-progress-capture-01.stderr']
    result=dict(status='PRODUCER_VALID_COMMAND_PROGRESS_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,table_pin=dict(path='namebinding-command-dispatch-table-01.json',sha256=P.sha(src/'namebinding-command-dispatch-table-01.json')),dispatch_targets=[dict(state=k,target=hex(x)) for k,x in enumerate(targets)],command_cfg=dict(entry='0x2e60f0',end_exclusive='0x2e62db',instructions=len(seen),returns=returns,calls=sorted(calls,key=lambda x:int(x['pc'],16))),normal_leaf_cfgs=leafs,state_register_definitions=defs,negative_three_part_conditional_witness=witness,
      established=[
        'LowWORD command state is unsigned bounded0..8 byCMP8/JA. HighWORD is sign-extended selector used for metadata words and record subresource slots. The separate36B original table resolves all9 dispatch entries; code/table identities are distinct.',
        'State2 polls the saved32E620 request ID through32E4D0. Busy1 retains state2; zero advances to state3 and returns this invocation. The poll is not a direct byte/content/read-success check.',
        '32E4D0 busy1 requires id not0/-1, matching generation-tagged queue slot+64 and nonzero slot state+20. Sentinel-1, id0, mismatch or inactive slot return0 normally. This describes a busy predicate, not why the id ceased to be pending; ordinary16D6A0 callee effects are separate.',
        'State3 invokes36D200 on its subresource handle; state4 hands it to3A1650, maps return-1 to skip state7 or otherwise polls3A1290 at state5. Getter returns stamped resource byte+0C only for a matching valid record, else0; state5 advances only when return2. Opaque binding/read effects are not established.',
        'Signed-negative metadata WORD skips the local allocate/read/postprocess path, writes its subresource slotFFFFFFFF and dispatches state7. Nonpositive32E400 size likewise skips. State6/7 advance selector and offsets; after word offset reaches6 the command sets entry18mask02, conditionally calls removal under18mask04 and writes state9.',
        'With initial selector0/state0or1, valid stable three negative metadata WORDs and ordinary lookup returns, all3 parts skip, slots30/34/38 becomeFFFFFFFF and the command still sets18mask02/state9 without its direct32E620 call. Thus ready is local sequence completion including skipped parts, not universal proof all3 assets loaded successfully. This is an original branch/invariant witness, not a native or natural game observation.',
        'Incoming state8 directly selects the set-ready arm; state>8 exits dispatch. Arbitrary highWORD selectors are not bounds-sanitized by the low-state check; valid selector/caller preconditions remain.'],
      limitations=['No natural source metadata values/caller/init proof; valid backed command+28 entry, selector0..2, stable metadata, normal ABI and no interference assumed','The three-negative case is a conditional original-code witness; authored-resource reachability remains separate','Request admission/refusal/natural failure not demonstrated; constant kind20/positive-size path may constrain reachable refusals','No allocator/postprocessor implementation effects, asynchronous timing/cancel/drain, successful content load, initialized record ownership or whole OV closure','3A1290 is not an arbitrary-ID sanitizer: ECX=-1 sets R8=0 before field dereference; local caller guards the fresh postprocess-1 arm, valid subsequent state5 handle required','Producer checks, prerequisite refusals and retained canonical queue semantics are not independent acceptance or external-run credit'],
      affected_claims=['Existing FABLE name-binding ready/delayed-delete and optional subresource semantics','OPUS command-state, RequestID busy predicate, ready-state meaning and invalid-handle preconditions'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,next_discriminator='Independent source review and owner consumption; exact authored negative metadata/prepared caller proof only if a natural reachability claim requires it. Do not sample live ready flags to replace this local definition.',cleanup='Finite read-only original code/data and disposable refusal fixtures; no game/PC/native/emulated/instrument/save/config/reference/peer mutation')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Nine-state original command: not-busy then postprocess, skipped parts still ready; no live')
if __name__=='__main__':main()
