"""Original array copy-count / counter-preservation / tail-init preconditions.

Static source-linked offsets and exact u32 arithmetic; no emulation or fixtures
claiming native effects. Accepted stride/layout T2 is corroboration, not recensus.
"""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('retained_normal','prove-title-queue-consumption.py');S=module('actual_annotations','validate-title-source-annotations.py')
def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(src,'texture-copy-construction-source-01.json',pins);agreement=S.validate(raw)
    spans={'0x61d100':('0x61d179','b941ad50789f7b4b2a35e3da877899801df0ca6c2ec646f204af368ea78fd617'),'0x613770':('0x6137f5','574f2205a5d275c169988b327b367574491ccf35eca0d1f115b65c507906e2ec'),'0x61c250':('0x61c2ad','557e57e1c34abeb4ed8ab4dcfa308660f9c8a4f5db145ed668ad2f3123e62d8e')}
    if len(raw['ranges'])!=3 or any(q['start'] not in spans or (q['end_exclusive'],q['sha256'])!=spans[q['start']] for q in raw['ranges']):raise ValueError('wrong/incomplete construction body')
    if raw.get('pdata_entries')!=[[0x61D100,0x61D179,0x1D7945C]] or raw.get('leaves')!=[dict(start='0x613770',end_exclusive='0x6137f5',padding='cc'*11),dict(start='0x61c250',end_exclusive='0x61c2ad',padding='cc'*3)]:raise ValueError('wrong construction root/leaf')
    cfgs=[P.closed(x,int(a,16),int(b,16)) for a,(b,h) in spans.items()]
    if cfgs[0]['calls']!=[dict(pc='0x61d136',target='0x17d260'),dict(pc='0x61d14c',target='0x613770'),dict(pc='0x61d15c',target='0x61c250')] or cfgs[1]['calls'] or cfgs[2]['calls']:raise ValueError('unclosed constructor call effects')
    for pc,m,a in [
      (0x61D114,'mov','esi, r9d'),(0x61D117,'mov','rbp, r8'),(0x61D11A,'mov','edi, edx'),(0x61D11C,'lea','rbx, [rcx + 8]'),(0x61D120,'test','edx, edx'),(0x61D122,'jne','0x61d128'),(0x61D124,'xor','eax, eax'),(0x61D128,'cmp','edi, 1'),(0x61D12B,'jbe','0x61d13e'),(0x61D12D,'imul','rcx, rdi, 0x58'),(0x61D131,'mov','edx, 8'),(0x61D13B,'mov','rbx, rax'),(0x61D13E,'test','rbx, rbx'),(0x61D141,'je','0x61d161'),(0x61D143,'mov','r8d, esi'),(0x61D146,'mov','rdx, rbp'),(0x61D149,'mov','rcx, rbx'),(0x61D151,'imul','rcx, rsi, 0x58'),(0x61D155,'sub','edi, esi'),(0x61D157,'add','rcx, rbx'),(0x61D15A,'mov','edx, edi'),
      (0x613770,'mov','r9, rcx'),(0x613773,'test','r8d, r8d'),(0x613776,'je','0x6137f4'),(0x613778,'add','rdx, 0x50'),(0x61377C,'mov','r8d, r8d'),(0x613790,'mov','rax, r9'),(0x613793,'add','r9, 0x58'),(0x613797,'test','rax, rax'),(0x61379A,'je','0x6137ee'),(0x6137D3,'mov','ecx, dword ptr [rdx - 0x18]'),(0x6137D6,'mov','dword ptr [rax + 0x38], ecx'),(0x6137E7,'add','rdx, 0x58'),(0x6137EE,'sub','r8, 1'),(0x6137F2,'jne','0x613790'),
      (0x61C250,'xor','r9d, r9d'),(0x61C258,'mov','r8d, r9d'),(0x61C25B,'test','edx, edx'),(0x61C25D,'je','0x61c2ac'),(0x61C25F,'lea','rax, [rcx + 0x10]'),(0x61C270,'lea','rcx, [rax - 0x10]'),(0x61C274,'test','rcx, rcx'),(0x61C277,'je','0x61c29b'),(0x61C293,'mov','dword ptr [rax + 0x28], r9d'),(0x61C29B,'inc','r8d'),(0x61C29E,'add','rax, 0x58'),(0x61C2A7,'cmp','r8d, edx'),(0x61C2AA,'jb','0x61c270')]:P.need(x,pc,m,a)
    if x[0x61377F]['memory'][0]['rip_target']!='0xd54348' or x[0x61C263]['memory'][0]['rip_target']!='0xd54348':raise ValueError('wrong async table constant')
    copies=[]
    # Literal first-iteration load/store pairs, including the accepted counter field.
    for load,store in [(0x61379C,0x6137A0),(0x6137A3,0x6137A7),(0x6137AB,0x6137AF),(0x6137B3,0x6137B7),(0x6137BB,0x6137BF),(0x6137C3,0x6137C7),(0x6137CB,0x6137CF),(0x6137D3,0x6137D6),(0x6137DD,0x6137E1),(0x6137E5,0x6137EB)]:
        li=x[load];si=x[store];a=li['memory'][0];b=si['memory'][0]
        if li['mnemonic']!='mov' or si['mnemonic']!='mov' or a['base']!='rdx' or b['base']!='rax' or a['role']!='r' or b['role']!='w' or a['size']!=b['size'] or li['args'].split(',')[0]!=si['args'].rsplit(', ',1)[1]:raise ValueError('copy dataflow changed')
        copies.append(dict(load=hex(load),store=hex(store),source_offset=0x50+a['displacement'],destination_offset=b['displacement'],bytes=a['size']))
    if [(q['source_offset'],q['destination_offset'],q['bytes']) for q in copies]!=[(k,k,8) for k in range(0,0x38,8)]+[(0x38,0x38,4),(0x48,0x48,8),(0x50,0x50,4)]:raise ValueError('wrong copied fields')
    zero=[]
    for pc in [0x61C279,0x61C27C,0x61C280,0x61C283,0x61C287,0x61C28B,0x61C28F,0x61C293]:
        i=x[pc];q=i['memory'][0];base={'rcx':0,'rax':0x10}.get(q['base'])
        if base is None or q['role']!='w' or not i['args'].endswith((', r9',', r9d')):raise ValueError('wrong initializer zero source')
        zero.append(dict(pc=hex(pc),offset=base+q['displacement'],bytes=q['size']))
    if [(q['offset'],q['bytes']) for q in zero]!=[(k,8) for k in range(0,0x38,8)]+[(0x38,4)]:raise ValueError('wrong initializer footprint')
    # Symbolic bound, not a reconstructed-code fixture: N,K are input low32.
    # For 0<=K<=N, K copied + (N-K) initialized = N; for K>N,
    # un-clamped copy exceeds N and SUB32 wraps the tail to 2^32+N-K.
    witness=dict(N=2,K=3,allocation_bytes=2*0x58,copy_records=3,tail_records=(2-3)&0xffffffff,first_excess_copy_offset=2*0x58,meaning='Conditional arithmetic counterexample to an unconstrained shrink-safe helper; not a natural caller witness or native run')
    r=dict(status='PRODUCER_CHECKED_COPY_COUNTER_AND_CAPACITY_PRECONDITIONS_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=agreement,normal_cfgs=cfgs,copy_dataflow=copies,initializer_zero_writes=zero,checker_sha256=P.sha(pathlib.Path(__file__)),question='Does61D100 clamp/reset old records or preserve copied counters and initialize only a bounded tail?',
      established=[
        '61D100 treats EDX low32 as new countN, R9D low32 as copy countK, and R8 as input pointer. N=0 returnsNULL without copy/init; N=1 chooses helper-record+8; N>1 calls17D260 with88*N bytes and alignment8. A NULL chosen destination skips copy/init. No owner type, allocator success or destruction of old storage is inferred.',
        'For a valid nonNULL destination, it calls613770 withK, not min(K,N), then61C250 at destination+88*K withu32(N-K). The checked normal branch closure contains no K<=N/clamp/drain call. Under the ordinary nonwrapping backed-storage premise, K<=N is needed for this helper to stay withinN records; K>N copies beyond that count and wraps the tail count. This is a required precondition, not proof a shipped caller violates it.',
        '613770 preserves each source DWORD+38 counter exactly, alongside the accepted data fields; it installsD54348 at+40 and copies async texture+48/index+50 without rebinding them to a different owner or index. It does not locally drain/reset the copied counters or invoke callbacks. General source/destination overlap and lifetime safety remain unproved.',
        '61C250 zeroes sevenQWORD fields0..30 and DWORD+38 in each valid tail record and installsD54348 at+40. It makes no local writes to+48/+50 or padding+3C/+54; those bytes are not certified zero/initialized by this helper. Successful parent allocation/base initialization may add effects outside this source.',
        'For0<=K<=N with valid storage, normal leaf loops and unchanged arguments, the firstK records are copied and remainingN-K records initialized. This bounded source formula preserves rather than creates a nonzero counter on the copied prefix; the complete writer closure and natural scheduler relationship remain OPEN.'
      ],conditional_arithmetic_witness=witness,assumptions=['ABI-correct normally returning allocator and correctly backed nonwrapping input/output/helper/stack storage','Stable N/K/source/destination, valid element records and no interfering writes','No arbitrary overlap, alias-to-stack, allocator/lifetime/ownership or natural shrink assumptions'],limitations=['Accepted OPUS T2 stride/layout reused; external tests/census not rerun or recounted','No complete caller/allocator/writer closure; copied nonzero values are possible input-domain facts, not observed natural counters','No actual resize, old-storage disposal, queue rescheduling or native/live observation; no universal malformed-input safety'],affected_claims=['OPUS element-array construction ABI and K<=N capacity precondition, wait-counter copy and uninitialized-tail members','FABLE Phyre async lifetime/move and complete counter-writer search'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='File reads/bounded static analysis only; no game/control/instrument/save/config/reference/peer process writes')
    out.open('x',encoding='utf-8').write(json.dumps(r,indent=2)+'\n');print('Counter copy, tail zero footprint and K<=N source precondition established; actual callers/lifetime OPEN')
if __name__=='__main__':main()
