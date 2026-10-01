"""Original local mask04 producer; original instruction order, no natural-state claim."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('pin_proof','prove-title-queue-consumption.py');S=module('pin_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    driver=src/'capture-namebinding-pin-exception.py'
    st=json.loads((src/'namebinding-pin-exception-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('capture failed/stale')
    if not (src/'namebinding-pin-exception-capture-01.stdout').read_bytes().strip() or (src/'namebinding-pin-exception-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'namebinding-pin-exception-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(driver):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    expected=[(0x2e6700,0x2e687d),(0x2ead50,0x2eae1e),(0x2e25e0,0x2e2651)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=expected:raise ValueError('named boundaries changed')
    for q,(a,z) in zip(v['ranges'],expected):
        raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
        if raw!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')
    cfgs=[P.closed(ix,a,z) for a,z in expected]
    ops=[
      (0x2e6708,'mov','rbx, qword ptr [rip + 0x1e79669]'),(0x2e670f,'xor','r14d, r14d'),
      (0x2e6730,'mov','r15, qword ptr [rbx + 8]'),(0x2e6739,'mov','edi, dword ptr [rbx + 0x14]'),
      (0x2e6753,'mov','ecx, edi'),(0x2e675a,'call','0x2ed6f0'),(0x2e6776,'call','0x32e400'),
      (0x2e677b,'or','byte ptr [rbx + 0x19], 4'),(0x2e677f,'lea','rsi, [rbx + 0x19]'),
      (0x2e6783,'mov','dword ptr [rbx + 0x10], r14d'),(0x2e6787,'mov','ebp, eax'),
      (0x2e6789,'test','eax, eax'),(0x2e678b,'jle','0x2e67ba'),(0x2e678d,'mov','ecx, eax'),
      (0x2e678f,'call','0x36b160'),(0x2e6794,'mov','dword ptr [rbx + 0x10], eax'),
      (0x2e6797,'test','eax, eax'),(0x2e6799,'je','0x2e67ba'),(0x2e679b,'and','byte ptr [rsi], 0xfb'),
      (0x2e679e,'mov','edx, edi'),(0x2e67a0,'mov','rcx, rbx'),(0x2e67a3,'call','0x2ead50'),
      (0x2e67dc,'mov','rax, qword ptr [rip + 0x1e79575]'),(0x2e67f2,'mov','qword ptr [rip + 0x1e7955f], rbx'),
      (0x2e684b,'and','byte ptr [rsi], 0xf7'),(0x2e684e,'mov','rbx, r15'),
      (0x2e686e,'mov','qword ptr [rip + 0x1e79503], r14'),
      (0x2e25e0,'mov','rdx, qword ptr [rip + 0x1e7d779]'),(0x2e25ef,'xor','r8d, r8d'),
      (0x2e25f2,'and','byte ptr [rdx + 0x19], 0xc8'),(0x2e2603,'mov','dword ptr [rdx + 0x14], ecx'),
      (0x2e2606,'mov','byte ptr [rdx + 0x18], r8b'),(0x2e264d,'mov','rax, rdx'),
      (0x2ead5d,'mov','rsi, rcx'),(0x2ead60,'mov','edi, edx'),(0x2ead62,'mov','ecx, dword ptr [rcx + 0x10]'),
      (0x2ead65,'call','0x36a000'),(0x2ead7c,'mov','r14, rax'),
      (0x2ead98,'xor','ecx, ecx'),(0x2ead9a,'mov','dword ptr [rsp + 0x38], esi'),
      (0x2ead9e,'mov','dword ptr [rsp + 0x30], ecx'),(0x2eada2,'lea','rax, [rip - 0x6089]'),
      (0x2eada9,'mov','qword ptr [rsp + 0x48], rcx'),(0x2eadb0,'mov','qword ptr [rsp + 0x40], rax'),
      (0x2eadcc,'call','0x2ed6f0'),(0x2eadea,'call','0x32e400'),(0x2eadef,'lea','rcx, [rsp + 0x30]'),
      (0x2eadf4,'mov','r9d, eax'),(0x2eadf7,'mov','qword ptr [rsp + 0x20], rcx'),
      (0x2eadfc,'mov','r8, r14'),(0x2eadff,'mov','ecx, dword ptr [rsp + 0x90]'),
      (0x2eae06,'mov','edx, ebx'),(0x2eae08,'call','0x32e620')]
    for pc,m,args in ops:P.need(ix,pc,m,args)
    mem=lambda pc:ix[pc]['memory'][0]
    if mem(0x2e677b)['role']!='rw' or mem(0x2e679b)['role']!='rw' or mem(0x2e677f)['role']!='addr' or mem(0x2ead9a)['role']!='w':raise ValueError('actual access roles changed')
    if mem(0x2e6708)['rip_target']!='0x215fd78' or mem(0x2e67f2)['rip_target']!='0x215fd58' or mem(0x2e25e0)['rip_target']!='0x215fd60' or mem(0x2eada2)['rip_target']!='0x2e4d20':raise ValueError('typed-list/descriptor identity changed')
    # Exact local branch segment has three outcomes; original callees are opaque.
    seq=[ix[p] for p in sorted(ix) if 0x2e677b<=p<=0x2e67a3]
    if [i['pc'] for i in seq if i['mnemonic'].startswith('j')]!=['0x2e678b','0x2e6799']:raise ValueError('allocation decision branches changed')
    if [i['pc'] for i in seq if i['mnemonic']=='call']!=['0x2e678f','0x2e67a3']:raise ValueError('allocation/submit sequence changed')
    alias19=[i for p,i in ix.items() if 0x2e677f<p<=0x2e684b and i['mnemonic']!='call' and 'rsi' in i['args'].split(',')[0].split() and i['mnemonic'] not in ['and','test']]
    if alias19:raise ValueError('flag address carrier overwritten')
    direct18=[dict(pc=i['pc'],memory=m) for p,i in ix.items() if 0x2e6700<=p<0x2e687d for m in i['memory'] if m['role'] in ['w','rw'] and m['base']=='rbx' and m['displacement']==0x18]
    if direct18:raise ValueError('worker directly changes record18')
    c=json.loads((src/'namebinding-pin-exception-consumer-01.json').read_text())
    if not c.get('sha256') or not any('128' in x['text'] and 'NameBindingEntry' in x['text'] for x in c['relevant']) or not any('0215FD78' in x['text'] for x in c['relevant']):raise ValueError('missing canonical typed-list premise')
    rows=[
      dict(size_result='signed <=0',allocation_call=False,submit_call=False,local_handle=0,mask04=1,point='arrival2E67BA under no interference'),
      dict(size_result='signed >0',allocation_result=0,allocation_call=True,submit_call=False,local_handle=0,mask04=1,point='arrival2E67BA under normal callee/no interference'),
      dict(size_result='signed >0',allocation_result='nonzero DWORD',allocation_call=True,submit_call=True,local_handle='returned DWORD',mask04=0,point='immediately before2E67A3; call may mutate state')]
    result=dict(status='PRODUCER_VALID_PIN_EXCEPTION_BRANCH_INDEPENDENT_PENDING',producer_complete=True,question='Does the original mask04 producer force ready18mask02 or mark allocation-unavailable branches?',method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfgs=cfgs,branch_partition=rows,descriptor=dict(callback='0x2e4d20',user_data='low32(record pointer), DWORD+8',flags=0,cancel_callback='NULL',read_destination='RAX of36A000(handle)',read_size='EAX of second32E400',metadata_queries=2),
      established=[
        'Validated worker starts from queued NameBindingEntry list0215FD78, uses boundID+14, moves records to live list0215FD58, and passes the same RBX record to2EAD50. Canonical table/list identity and valid list premises are explicit, not inferred from a displacement candidate alone.',
        'After signed size query32E400,2E677B sets19mask04 and zeroes+10. Size<=0 skips allocation and submission. Positive size with allocator36B160 returning0 also skips submission and retains04/zero handle. Nonzero allocation clears04 through the original RSI=record+19 alias BEFORE2EAD50 is called.',
        'The complete worker makes no direct record+18 write. A fresh constructor record has18=0 and04 cleared; given an ordinary preserved queued record, nonpositive size/no interfering callee writes leaves ready18mask02=0 with19mask04=1 and no read submitted by this invocation. This refutes ready-only as a local producer rule, not a natural pending-IO history.',
        'Submitter2EAD50 builds callback2E4D20, DWORD low32 record user data, flags0 and NULL cancellation function. It passes the36A000(handle) return as destination, metadata kind/index and a newly queried size to32E620. This is original descriptor and call dataflow, not proof the read is accepted or executed.',
        'The worker clears19mask08 locally at2E684B and clears queued headFD78 at normal exit. It does not locally clear04 on the unavailable arms. Other typed writers, aliased callees, current owner state and arbitrary callback effects are not excluded.'],
      assumptions=['Valid NameBindingEntry queued/live lists and backed record/stack','Normal ABI-preserving returns; nonvolatile carrier registers preserved','No relevant callee/alias/other-thread interference for retained bit/handle branch values and constructor composition','The original worker is reached with the constructed record when composing its rule; reachability/initialization not proven here'],
      limitations=['Not a complete mask04 writer census: module candidate scan has one incomplete jump-table body and excludes alias0 writes unless source-directed','mask04 is an unavailable/allocation-failure sentinel in this local producer, not a universal semantic enum or proof of no outstanding IO','No natural outstanding old callback plus mask04, callback reentrancy/timing, actual allocator success or full lifetime/safety proof','Metadata is queried twice; unchanged metadata needed to equate the first kind/index and second size mapping','Record low32 callback user data and prior MOVSXD require appropriate address representation; pointer portability/lifetime not certified','Producer controls are not independent review/canonical consumption; no whole OV21 or other runtime row closure'],
      affected_claims=['FABLE name-binding19mask04 exception/natural-pending preparation','OPUS NameBindingEntry pin/state flag distinctions, callback descriptor/type contracts','Existing ASTRA namebinding-deletion exception and lifetime preconditions'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-namebinding-pin-exception.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','namebinding-pin-exception-consumer-01.json','namebinding-pin-exception-capture-01.status.json','namebinding-pin-exception-capture-01.stdout','namebinding-pin-exception-capture-01.stderr']],
      native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,next_discriminator='Independent review/canonical consumption; only source-specific old outstanding request + mask04/reentrancy remains unresolved, not ready-only. Do not launch game just to retest this settled local branch.',cleanup='Finite file reads/private CLI controls only; no game/PC/native/emulated/instrument/save/config/reference/peer mutation')
    with out.open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Original mask04 producer distinguishes unavailable allocation from ready; callback descriptor bound')
if __name__=='__main__':main()
