"""Bound local allocation/release/import effects and empty-bank null path.

Method A. Abstract native returns are explicit premises, not stubs/executions.
Requires the actual capture's successful exit and exact source/driver hashes.
"""
import hashlib, importlib.util, json, pathlib, sys
W = pathlib.Path(__file__).resolve().parent
def module(name, file):
    s = importlib.util.spec_from_file_location(name, W/file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
P = module('source_proof', 'prove-title-queue-consumption.py')
S = module('annotations', 'validate-title-source-annotations.py')

def normal_boundary(ix, a, b, tail_pc, tail_target):
    todo=[a];seen=set();calls=[];exits=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not a<=pc<b:raise ValueError('unclosed selected normal CFG')
        seen.add(pc);i=ix[pc];m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
        if m=='jmp':
            if pc!=tail_pc or i['memory']!=[dict(base='rip',index=None,scale=1,
                displacement=tail_target-n,size=8,role='r',rip_target=hex(tail_target))]:
                raise ValueError('unbound external tail')
            exits.append(dict(pc=hex(pc),kind='named_import_tail',iat=hex(tail_target)));continue
        if m=='ret':exits.append(dict(pc=hex(pc),kind='local_return'));continue
        if m.startswith('j'):todo.append(int(i['args'],16))
        if m=='call':calls.append(hex(pc))
        todo.append(n)
    if seen!={pc for pc in ix if a<=pc<b}:raise ValueError('unchecked selected normal instructions')
    return dict(entry=hex(a),end_exclusive=hex(b),instructions=len(seen),calls=sorted(calls),exits=exits)

def main():
    if len(sys.argv)!=4:raise ValueError('source_directory capture_status fresh_result')
    source,status,out=map(pathlib.Path,sys.argv[1:])
    if out.exists():raise ValueError('immutable result exists')
    receipt=json.loads(status.read_text());name='renderer-queue-allocator-source-01.json'
    if receipt.get('exit')!=0:raise ValueError('upstream capture failed or missing exit')
    if receipt.get('source_name')!=name or receipt.get('source_sha256')!=P.sha(source/name):
        raise ValueError('capture receipt source moved')
    if receipt.get('driver_sha256')!=P.sha(source/'capture-renderer-queue-allocator.py'):
        raise ValueError('capture driver prerequisite moved')
    pins=[];raw,ix=P.load(source,name,pins);ann=S.validate(raw)
    if raw.get('invocation_driver_sha256')!=receipt['driver_sha256']:
        raise ValueError('source invocation identity moved')
    if raw.get('pdata_entries')!=[[0x1edf80,0x1edfda,0x1d529d0],[0x1edfe0,0x1ee040,0x1d529d0]] or raw.get('unwind_bytes')!='0106020006320230':
        raise ValueError('normal wrapper extent prerequisite')
    for pc,m,a in [
        (0x1edf86,'cmp','qword ptr [rip + 0x1d94eba], 0'),(0x1edf8e,'mov','rbx, rdx'),
        (0x1edf91,'jne','0x1edfc6'),(0x1edf93,'mov','ecx, 0x20'),
        (0x1edf98,'call','qword ptr [rip + 0x6d4ba2]'),(0x1edf9e,'test','rax, rax'),
        (0x1edfa1,'je','0x1edfbf'),(0x1edfa3,'mov','dword ptr [rax], 0x2000000'),
        (0x1edfa9,'mov','dword ptr [rax + 4], 0x200000'),(0x1edfb0,'mov','qword ptr [rax + 0x10], 0'),
        (0x1edfb8,'mov','dword ptr [rax + 0x18], 0'),(0x1edfbf,'mov','qword ptr [rip + 0x1d94e82], rax'),
        (0x1edfc6,'mov','edx, 0x10'),(0x1edfcb,'mov','rcx, rbx'),
        (0x1edfe6,'cmp','qword ptr [rip + 0x1d94e5a], 0'),(0x1edfee,'mov','rbx, rdx'),
        (0x1edff1,'jne','0x1ee026'),(0x1edff3,'mov','ecx, 0x20'),
        (0x1edff8,'call','qword ptr [rip + 0x6d4b42]'),(0x1edffe,'test','rax, rax'),
        (0x1ee001,'je','0x1ee01f'),(0x1ee003,'mov','dword ptr [rax], 0x2000000'),
        (0x1ee009,'mov','dword ptr [rax + 4], 0x200000'),(0x1ee010,'mov','qword ptr [rax + 0x10], 0'),
        (0x1ee018,'mov','dword ptr [rax + 0x18], 0'),(0x1ee01f,'mov','qword ptr [rip + 0x1d94e22], rax'),
        (0x1ee026,'test','rbx, rbx'),(0x1ee029,'je','0x1ee03a'),(0x1ee02b,'mov','rcx, rbx')]:
        P.need(ix,pc,m,a)
    expected={'0x1edf80':('0x1edfda','68b3991103d547ae55dd08ee258bd731666450870d2f516f5a55f92ba5fa0f48'),
              '0x1edfe0':('0x1ee040','57cc3066baf02d405eb3d1c748ca8a72f16accb806199e989265b4ba4051f977')}
    if len(raw['ranges'])!=2 or any((q['end_exclusive'],q['sha256'])!=expected.get(q['start']) for q in raw['ranges']):
        raise ValueError('shipping complete wrapper bytes changed')
    table=raw.get('physical_table',{})
    if table!=dict(address='0x902720',bytes='80d616000000000010df1e000000000080df1e0000000000e0df1e0000000000',
        sha256='a7740d5af6d40501aae47062771ea9ca7f9d216f8143538f42df0e8b1cd5ac3c',
        slots=['0x16d680','0x1edf10','0x1edf80','0x1edfe0']):raise ValueError('physical table prerequisite')
    expected_imports=[(0x8c2b40,'malloc',25,0,'88eecc0100000000','19006d616c6c6f6300'),
        (0x8c2b48,'free',24,1,'80eecc0100000000','18006672656500'),
        (0x8c2b60,'_aligned_malloc',1,4,'b6eecc0100000000','01005f616c69676e65645f6d616c6c6f6300'),
        (0x8c2b70,'_aligned_free',0,6,'a6eecc0100000000','00005f616c69676e65645f6672656500')]
    entries=[dict(dll='api-ms-win-crt-heap-l1-1-0.dll',name=n,hint=h,descriptor_rva='0x1ccad08',
        lookup_table_rva='0x1ccb8b0',slot=s,iat=hex(a),descriptor_bytes='b0b8cc010000000000000000e6f5cc01402b7a00',
        lookup_bytes=l,original_iat_bytes=l,name_bytes=b) for a,n,h,s,l,b in expected_imports]
    if raw.get('import_boundaries')!=entries:raise ValueError('named import binding changed')
    for pc,target in [(0x1edf86,0x1f82e48),(0x1edfbf,0x1f82e48),(0x1edfe6,0x1f82e48),(0x1ee01f,0x1f82e48),
                      (0x1edf98,0x8c2b40),(0x1edff8,0x8c2b40)]:
        if ix[pc]['memory'][0]['rip_target']!=hex(target):raise ValueError('header/import pointer binding changed')
    cfg=[normal_boundary(ix,0x1edf80,0x1edfda,0x1edfd3,0x8c2b60),
         normal_boundary(ix,0x1edfe0,0x1ee040,0x1ee033,0x8c2b70)]
    if cfg[0]['calls']!=['0x1edf98'] or cfg[1]['calls']!=['0x1edff8']:
        raise ValueError('unchecked external wrapper call')
    prior,pi=P.load(source,'renderer-queue-initialization-source-02.json',pins)
    prior_ann=S.validate(prior)
    ranges={q['start']:q for q in prior['ranges']}
    for a,z,h in [('0x184cb0','0x184cdf','17aa2b33ec08c888dafd3db09498053f558da4b4dac61a63abb907041f48b45d'),
                  ('0x1edf00','0x1edf0e','b1dc13f72a07d6ebcb83fc9363a2b4036d1506c41c3aa2967c07bd27b517518f'),
                  ('0x188640','0x188721','b4edaadcf104b43087948c2e8c14854758bec0f95ca80d2b454e5f6c9611d9f6')]:
        if a not in ranges or (ranges[a]['end_exclusive'],ranges[a]['sha256'])!=(z,h):
            raise ValueError('retained bank/reserve prerequisite incomplete')
    reserve_cfg=P.closed(pi,0x188640,0x188721)
    for pc,m,a in [(0x184ccd,'add','rcx, 0x18'),(0x184cd1,'call','0x1edf00'),
                  (0x1edf07,'mov','qword ptr [rcx], rax'),(0x188664,'cmp','edx, eax'),
                  (0x188666,'jbe','0x188710'),(0x18867a,'test','edx, edx'),(0x18867c,'je','0x188698'),
                  (0x188682,'add','rcx, 0x18'),(0x188686,'mov','edx, r14d'),(0x188689,'xor','r8d, r8d'),
                  (0x18868c,'shl','rdx, 4'),(0x188690,'call','qword ptr [rax + 0x10]'),
                  (0x188693,'mov','rbp, rax'),(0x18869a,'mov','rax, rbp'),
                  (0x18869d,'cmp','rbx, rsi'),(0x1886a0,'je','0x1886be'),
                  (0x1886c6,'test','rdx, rdx'),(0x1886c9,'je','0x1886e8'),
                  (0x1886ef,'and','rax, 0xfffffffffffffff0'),(0x1886f3,'mov','qword ptr [rdi], rbp'),
                  (0x1886f6,'add','rax, rbp'),(0x1886f9,'mov','qword ptr [rdi + 8], rax'),
                  (0x1886fd,'mov','rax, r14'),(0x188700,'shl','rax, 4'),
                  (0x188704,'add','rax, rbp'),(0x18870c,'mov','qword ptr [rdi + 0x10], rax')]:P.need(pi,pc,m,a)
    if pi[0x1edf00]['memory'][0]['rip_target']!='0x902720':raise ValueError('constructor table binding')
    # General empty-bank proof, not a sampled native return or reconstructed fixture.
    # For every unsigned desired D in [1,2^32-1], initial capacity/current/begin=0:
    # D>capacity selects allocation, D!=0 calls it, begin==current skips copy,
    # original begin==0 skips release. No branch then depends on returned pointer A.
    contract=source/'renderer-queue-allocator-external-contract-01.json'
    docs=json.loads(contract.read_text())
    if [d['title'] for d in docs.get('sources',[])]!=['Microsoft Learn: _aligned_malloc','Microsoft Learn: _aligned_free']:
        raise ValueError('missing separate external contract')
    result=dict(status='PRODUCER_PROVED_LOCAL_ALLOCATOR_NULL_BOUNDARY_INDEPENDENT_PENDING',producer_complete=True,
        method='A shipping bytes/normal CFG/dataflow plus separately labelled external API contract; no execution',
        question='Does allocator902720 guarantee nonnull normal return, and what does empty-bank reserve publish under a normally returned null?',
        exe_sha256=P.SHA,source_pins=pins,annotation_prerequisites=[ann,prior_ann],normal_cfgs=cfg,
        retained_reserve_cfg=reserve_cfg,checker_sha256=P.sha(pathlib.Path(__file__)),
        capture_receipt=dict(path=status.name,sha256=P.sha(status),exit=receipt['exit']),
        external_contract=dict(path=contract.name,sha256=P.sha(contract),limits=docs['method']),
        established=[
            'Physical902720 slots10/18 bind1EDF80/1EDFE0; original184CB0->1EDF00 writes that table at bank+18. Not a live pointer sample.',
            '1EDF80 preserves incomingRDX inRBX across optional header malloc(32), restores it toRCX and tails original8C2B60 _aligned_malloc withEDX16. Incoming allocator recordRCX andR8 are not used locally. No local return-side nonnull test, retry or throwing adapter exists: a normally returning import supplies the wrapper result.',
            'Both wrappers test global01F82E48. If zero, malloc(32) is attempted; nonnull initializes only DWORD0/4, QWORD10, DWORD18, then stores returnedRAX to the global. Null skips those field writes, storesnull and continues to the allocation tail or release pointer test. Local header failure does not select an abort/retry branch.',
            '1EDFE0 tests saved incomingRDX. Null takes the localRET without aligned_free; nonnull moves it toRCX then tails original8C2B70 _aligned_free. IncomingR8 size is not consumed locally. Null still may perform the separate header allocation before that test. No meaningful void-release return value or actual free/ownership effect is proved.',
            'Under the separately documented _aligned_malloc API contract, nonzero80000/alignment16 does not guarantee nonnull on normal return. Therefore the local wrapper cannot justify an unconditional successful-backed allocation claim. This is not an observed shipped-process failure or loaded-DLL proof.',
            'For an unchanged backed initially empty bank and every unsigned desiredD in1..FFFFFFFF, reserve selects allocation, skips copy because oldbegin==oldcurrent, and skips old release because oldbegin==0. Given a normally returned pointerA, it locally writes(begin,current,end)=(A,A,(A+16*D) mod2^64), with no nonnull gate. A=0,D5000 conditionally yields(0,0,80000); this is an abstract conditional source consequence, not a native failure observation or valid storage.'],
        normalized=dict(allocation_request=dict(size='incoming RDX',alignment=16,iat='0x8c2b60'),
            release=dict(pointer='incoming RDX',null_skips_release=True,header_work_can_precede_skip=True,iat='0x8c2b70'),
            empty_bank_formula=dict(domain='unsignedD1..FFFFFFFF; initialbegin=current=end0; no interference; normal ABI/return',
                stores=['A','A','(A+16*D) mod2^64'],conditional_null_5000=[0,0,80000])),
        refuted=['Unconditional nonnull guarantee from this wrapper/its documented API',
                 'Null release pointer means the whole wrapper makes no call',
                 'R8 byte/count argument is consumed by the bound slot18 local wrapper'],
        unresolved=['Actual loaded CRT/IAT/invalid-parameter handler behavior and process allocation success/placement',
                    'Natural failure/reachability, caller ownership, alias/reuse, synchronization and lifetime',
                    'Nonempty-bank failure safety and effects of opaque later renderer calls; no crash/safety inference'],
        acceptance='Two exact normal wrapper CFGs and named import boundaries; actual source/driver/exit prerequisites; scoped original reserve path. Independent review and canonical consumption remain pending.',
        affected_claims=['FABLE title/renderer initialization and deferred cleanup preconditions',
                         'OPUS allocator callback ABI, null-return/reserve and aligned release contracts'],
        cheaper_method_result='Fresh runtime unnecessary for local no-guarantee/import/conditional empty-bank proposition; actual allocator placement remains separate.',
        native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
        scoped_allocation_obligations_answered_without_game=1,
        previously_reported_historical_runtime_eliminations=4,
        cleanup='Read-only original reference; synchronous bounded scripts only; no game/PC/save/config/instrument/native/peer mutation')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('PROVED local allocator/import/null publication boundary; native state and lifetime remain OPEN')

if __name__=='__main__':main()
