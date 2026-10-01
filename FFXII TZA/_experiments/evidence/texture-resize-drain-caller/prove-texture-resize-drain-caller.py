"""Original normal call-order invariant; no inference from absence sampling.

Qualified full153-byte higher caller plus retained wait/resize/helper evidence.
The signed wait predicate is not proof of zero jobs or atomic lifetime safety.
Fresh result [disposable source directory]. No native/emulated/game execution.
"""
import importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def mod(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=mod('original_normal_cfg','prove-title-queue-consumption.py');S=mod('reviewed_annotations','validate-title-source-annotations.py')
DEPS={
 'texture-copy-capacity-caller-result-02.json':'e00a04d0ab2a6af9f9409e903a78fd2f242449a83e745578f5a4e295445dd866',
 'texture-copy-construction-result-01.json':'c05d8114657aeabacdcf7f453805ab477090284056f3dd1f515d96f38c368207',
 'title-cleanup-count-selector-result-01.json':'65c353fc508a3b745c09f4ea57dd6cb160ae31c5faf2f328b6bc7f7509d17d06',
}

def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(src,'texture-resize-drain-caller-source-01.json',pins);annotations=[S.validate(raw)]
    if len(raw['ranges'])!=1 or (raw['ranges'][0]['start'],raw['ranges'][0]['end_exclusive'],raw['ranges'][0]['sha256'])!=('0x628100','0x628199','e9d010397bd5ccb58575635e6f3d9962b2cf48c849a03f35b5382a213a522b7a'):raise ValueError('higher caller full body identity changed')
    entries=[[0x628100,0x628124,0x1de0c5c],[0x628124,0x62818e,0x1da85b8],[0x62818e,0x628199,0x1da85cc]]
    if raw.get('pdata_entries')!=entries or raw.get('padding')!='cc' or len(raw.get('unwind',[]))!=3:raise ValueError('missing normal higher caller fragments')
    for u,e,h in zip(raw['unwind'],entries,['010a0400','21050200','21000000']):
        z=bytes.fromhex(u['raw']);at=(4+2*z[2]+3)&~3;flags=z[0]>>3
        chain=[v+0x120000 for v in struct.unpack_from('<III',z,at)] if flags&4 else None
        if u['address']!=hex(e[2]) or z[:4].hex()!=h or u['header']!=h or u['flags']!=flags or u['chain']!=chain or (flags&4 and chain!=entries[0]):raise ValueError('higher caller root/unwind disagreement')
    prerequisite_pins=[]
    for name,digest in DEPS.items():
        p=src/name
        if P.sha(p)!=digest:raise ValueError('required retained dependency changed '+name)
        r=json.loads(p.read_text())
        if r.get('producer_complete') is not True or not r.get('source_pins'):raise ValueError('required upstream result incomplete '+name)
        prerequisite_pins.append(dict(path=name,sha256=digest))
        for pin in r['source_pins']:
            if P.sha(src/pin['path'])!=pin['sha256']:raise ValueError('required upstream source preimage changed')
    for name in ['title-cleanup-count-selector-source-01.json','texture-copy-capacity-caller-source-01.json','texture-copy-construction-source-01.json']:
        v,i=P.load(src,name,pins);annotations.append(S.validate(v))
        if name.startswith('title-'):wait=i
    cfg=P.closed(x,0x628100,0x628199)
    calls=[dict(pc=hex(p),target=t) for p,t in [(0x628118,'0x62bcb0'),(0x628129,'0x62b100'),(0x628134,'0x627da0'),(0x628176,'0x61fda0')]]
    if cfg['calls']!=calls:raise ValueError('higher caller native boundaries changed')
    for pc,m,a in [(0x62810a,'cmp','dword ptr [rcx + 0xbc], 0'),(0x628111,'mov','esi, edx'),(0x628113,'mov','rbx, rcx'),(0x628116,'je','0x628121'),(0x62811d,'test','eax, eax'),(0x62811f,'jne','0x62818e'),(0x628121,'mov','rcx, rbx'),(0x628129,'call','0x62b100'),(0x62812e,'mov','edx, esi'),(0x628130,'lea','rcx, [rbx + 0x30]'),(0x628134,'call','0x627da0'),(0x628139,'test','eax, eax'),(0x62813b,'jne','0x628189'),(0x62813d,'mov','ecx, dword ptr [rbx + 0x30]'),(0x628140,'xor','edx, edx'),(0x628142,'btr','ecx, 0x1f'),(0x628146,'cmp','ecx, 1'),(0x628149,'jbe','0x628151'),(0x62814b,'mov','rax, qword ptr [rbx + 0x38]'),(0x628151,'test','ecx, ecx'),(0x628153,'lea','rax, [rbx + 0x38]'),(0x628157,'cmove','rax, rdx'),(0x62815b,'cmp','qword ptr [rax], rdx'),(0x628176,'call','0x61fda0'),(0x62817b,'mov','edx, eax'),(0x62817d,'mov','dword ptr [rbx + 0xbc], 1'),(0x628187,'mov','eax, edx')]:P.need(x,pc,m,a)
    graph={};pred={p:set() for p in x}
    for pc,i in x.items():
        m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
        successors=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [n,int(i['args'],16)] if m.startswith('j') else [n]
        graph[pc]=successors
        for target in successors:pred[target].add(pc)
    dom={p:{p} if p==0x628100 else set(x) for p in x}
    changed=True
    while changed:
        changed=False
        for pc in x:
            if pc==0x628100:continue
            new={pc}|set.intersection(*(dom[p] for p in pred[pc]))
            if new!=dom[pc]:dom[pc]=new;changed=True
    required=[0x628111,0x628113,0x628121,0x628129,0x62812e,0x628130]
    if not set(required)<=dom[0x628134]:raise ValueError('drain/argument setup does not dominate resize')
    # Retained wait loop's bounds and branch predicate, not a new census/run.
    g_wait=P.closed(wait,0x62b100,0x62b170)
    for pc,m,a in [(0x62b10a,'mov','edx, dword ptr [rcx + 0x30]'),(0x62b10d,'xor','ebx, ebx'),(0x62b10f,'and','edx, 0x7fffffff'),(0x62b115,'mov','eax, 1'),(0x62b11d,'cmovne','eax, edx'),(0x62b124,'mov','edx, ebx'),(0x62b12e,'mov','ecx, dword ptr [rax]'),(0x62b130,'test','ecx, ecx'),(0x62b132,'jle','0x62b14e'),(0x62b14c,'jg','0x62b134'),(0x62b151,'inc','ebx'),(0x62b161,'cmp','ebx, eax'),(0x62b163,'jb','0x62b124')]:P.need(wait,pc,m,a)
    r=dict(status='PRODUCER_CHECKED_HIGHER_CALLER_DRAIN_BEFORE_RESIZE_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',
      question='Must the selected original texture caller return from62B100 before627DA0 can resize/copy/free the element storage, and what does that imply?',
      hypotheses=['Selected resize path can bypass the wait routine','Every normal resize call passes through the same-object wait; outstanding-work/lifetime safety still requires stronger premises'],
      evidence_choice='Complete original normal caller/retained callee dataflow and domination suffice for call order; no natural timing sample is needed.',
      exe_sha256=P.SHA,source_pins=pins,prerequisite_result_pins=prerequisite_pins,annotation_prerequisites=annotations,
      normal_cfgs=[cfg,g_wait],resize_dominators=[hex(p) for p in required],checker_sha256=P.sha(pathlib.Path(__file__)),
      established=[
       'Every normal path reaching628134->627DA0 has executed628129->62B100 and returned normally. RCX towait is original object; RCX toresize is object+30; EDXnewcount is preserved input low32 in ESI. The complete153B/three chained fragments and defining operations are covered, not only the root fragment.',
       'Object+BC nonzero first invokes62BCB0; nonzero returned status exits before wait/resize. Therefore not every invocation executes the wait, but every reached resize does. Resize failure returns its status before post-resize resource access; native callee effects remain opaque.',
       'Under stable valid masked oldcount n>=1/storage and normal terminating callees, the retained wait visits indices0..n-1 and observes a signed-nonpositive DWORD for each before moving on. Its observations are sequential, not a simultaneous all-zero/pending-job assertion. Negative signed counts also satisfy the predicate.',
       'The selected lower resize then enforcesK=min(newN,masked oldcount), reuses the copied-counter/helper contract and conditionally disposes old storage. No claim of resize-before-wait on this path remains. Higher normal caller reachability and actual scheduler/counter writers are separate.',
       'After successful resize, the higher caller selects NULL/inline/pointer for masked newcount0/1/>1 then reads QWORD[selected] without a local NULL guard. With oldcount>=1, requestednewN0, normal successful callees and no interfering/alias writes, this yields a conditional NULL read after the acceptedzero-count resize. This is a named positive-count/caller-domain obligation, not a claim shipped inputs reach0 or an observed crash.',
       'On post-resize success it calls61FDA0 only when selected resourceQWORD0 isNULL, then writes object+BC=1 and returns status. The local gate/order and argument bits are physical evidence; omitted resource binding/service effects remainOPEN.'
      ],
      limitations=['Normal original entry/ABI-preserving returns only; exceptions, asynchronous interruption and alias/interference excluded from order guarantee','No termination/progress guarantee or proof every counter encodes an outstanding job','No simultaneous zero condition; counters can rise after an individual check, queued keys may remain, and native allocator/free/callback effects are not certified','Full natural caller/count producers, initialized oldcount>=1/storage, actual scheduling, ownership/reuse and all wait-counter writers remainOPEN','No arbitrary high-bit/newcount sanitizer, cancellation, queue removal or lifetime safety claim; forced state would not establish natural reachability'],
      affected_claims=['OV29/Phyre selected texture resize wait/copy/free call order','OPUS texture+30 element-array/count/ABI and positive-count caller obligations','FABLE async wait versus ownership/lifetime interpretation'],
      next_discriminator='Validate upstream628100 callers and count producers for ordinary positive-count domain and interference policy; full counter/registration/removal sources before any automatic real-process collector',
      producer_acceptance='Pending independent primary-source/code-control review; retained producer/helper acceptance remains separately scoped',
      new_whole_runtime_rows_closed=0,native_runs=0,live_runs=0,
      cleanup='Offline retained/shipping reads and finite CFG proof only; no PC/game/input/instrument/save/config/reference/peer-process writes')
    out.open('x',encoding='utf-8').write(json.dumps(r,indent=2)+'\n');print('Original selected drain-before-resize domination proved; zero-count domain and lifetime remain conditional/open')
if __name__=='__main__':main()
