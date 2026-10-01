"""Selected-bank lookup/removal closure; retained caller and actual shipping bytes.

Method A. Conditional empty-other-bank counterexample has no opaque calls.
No original code/native/game executes and no stub certifies native effects.
"""
import importlib.util, json, pathlib, sys

W=pathlib.Path(__file__).resolve().parent


def module(name,file):
    spec=importlib.util.spec_from_file_location(name,W/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


P=module('removal_original_cfg','prove-title-queue-consumption.py')
S=module('removal_reviewed_roles','validate-title-source-annotations.py')
SOURCES={
 'texture-async-removal-source-01.json': [('0x62ec70','0x62ecc2','f6f7c4fcacce01d97fbc0ed4fd35b18ded9b1128d8695f76d0c57ae2cb57ad17')],
 'texture-async-removal-tail-source-01.json': [('0x62ecc2','0x62ed36','3d5137ccbd4e8f9daf3c56e53b94d5cf354c3cc5ff5f60ed7d816e15249529ae'),('0x62ed36','0x62ed3c','ac829edc8d3d5ff13f0d67c2504827d5bc4a860f9e0462749c945b7728053f34')],
 'texture-async-removal-helpers-source-01.json': [('0x16d6d0','0x16d714','a0978695096493b0fe7886fe4e1facb0122606de8436fe80dfe2736ccfe34347'),('0x16da60','0x16ddc3','7ea8d0fa30a780a566012ea42129eecd946867ed4fde3591f07359c9e6e3e576')],
 'texture-async-removal-rotations-source-01.json': [('0x16d780','0x16d7dc','a5d522d7a583a6012623d13a2d368b17bf19dcbec7dd60473fe16a89b3dd3928'),('0x16d7e0','0x16d838','585b264dab378a6daaf29a6fd9114209dc91c8ca7023529aca04644b5e7ba9fd')],
}
CAPTURES=[('texture-async-removal-capture-01','capture-texture-async-removal.py'),
          ('texture-async-removal-tail-capture-01','capture-texture-async-removal-tail.py'),
          ('texture-async-removal-helpers-capture-02','capture-texture-async-removal-helpers.py'),
          ('texture-async-removal-rotations-capture-01','capture-texture-async-removal-rotations.py')]


def graph(ix,a,z):
    edges={}
    for p,i in ix.items():
        if not a<=p<z:continue
        m=i['mnemonic'];nextpc=p+len(bytes.fromhex(i['bytes']))
        edges[p]=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [nextpc]
        if m.startswith('j') and m!='jmp':edges[p].append(int(i['args'],16))
    dom={p:({a} if p==a else set(edges)) for p in edges}
    changed=True
    while changed:
        changed=False
        for p in edges:
            if p==a:continue
            parents=[q for q,targets in edges.items() if p in targets]
            if not parents:raise ValueError('normal graph has unreachable predecessor domain')
            new={p}|set.intersection(*(dom[q] for q in parents))
            if new!=dom[p]:dom[p]=new;changed=True
    return edges,dom


def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    receipts=[]
    for prefix,driver in CAPTURES:
        p=src/(prefix+'.status.json');status=json.loads(p.read_text())
        if status.get('exit')!=0 or status.get('driver_sha256')!=P.sha(src/driver):raise ValueError('required removal capture invocation failed or incomplete')
        stdout=src/(prefix+'.stdout');stderr=src/(prefix+'.stderr')
        if not stdout.read_bytes().strip() or stderr.read_bytes().strip():raise ValueError('required removal capture output missing/failed')
        receipts += [dict(path=q.name,sha256=P.sha(q)) for q in (p,stdout,stderr,src/driver)]
    pins=[];ix={};raws={};annotations=[]
    for name,wanted in SOURCES.items():
        raw,x=P.load(src,name,pins);annotations.append(S.validate(raw));raws[name]=raw
        if [(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']]!=wanted:raise ValueError('required original removal closure identity changed')
        if set(ix)&set(x):raise ValueError('overlapping original closure records')
        ix.update(x)
    root=[0x62ec70,0x62ecc2,0x1d8f380]
    if raws['texture-async-removal-source-01.json'].get('pdata_entries')!=[root]:raise ValueError('original removal root identity changed')
    tail=raws['texture-async-removal-tail-source-01.json']
    if tail.get('pdata_entries')!=[[0x62ecc2,0x62ed36,0x1daa2a8],[0x62ed36,0x62ed3c,0x1daa2c0]] or len(tail.get('chains',[]))!=2:
        raise ValueError('normal removal continuations missing')
    if any(t.get('parent')!=root or t.get('parent_raw')!='70ec5000c2ec500080f3c601' or int(t.get('header','00')[:2],16)>>3!=4 for t in tail['chains']):raise ValueError('normal removal parent triples changed')
    caller,c=P.load(src,'title-cleanup-callees-source-01.json',pins);annotations.append(S.validate(caller))
    q=next(q for q in caller['ranges'] if q['start']=='0x62bd04')
    if (q['end_exclusive'],q['sha256'])!=('0x62bf24','24450e2df1d737c74a52dd9d76ae2607cc490473f9b2e54388abdecd8a6a8fd5'):raise ValueError('retained release caller fragment changed')
    cfgs=[P.closed(ix,a,z) for a,z in [(0x62ec70,0x62ed3c),(0x16d6d0,0x16d714),(0x16da60,0x16ddc3),(0x16d780,0x16d7dc),(0x16d7e0,0x16d838)]]
    expected_calls=[[dict(pc='0x62ed08',target='0x16d6d0'),dict(pc='0x62ed13',target='0x16da60'),dict(pc='0x62ed29',target='qword ptr [rax + 0x18]')],[],
                    [dict(pc='0x16dc97',target='0x16d7e0'),dict(pc='0x16dcc3',target='0x16d780'),dict(pc='0x16dd7c',target='0x16d780'),dict(pc='0x16ddaa',target='0x16d7e0')],[],[]]
    if [g['calls'] for g in cfgs]!=expected_calls:raise ValueError('original removal call closure changed')
    operations=[(0x62ec76,'mov','eax, r8d'),(0x62ec79,'imul','rsi, rax, 0x38'),(0x62ec7d,'add','rsi, rcx'),
                (0x62ec80,'mov','rax, qword ptr [rsi + 0x18]'),(0x62ec84,'lea','r8, [rsi + 8]'),(0x62ec88,'mov','rcx, r8'),
                (0x62ec8b,'test','rax, rax'),(0x62ec8e,'je','0x62eca7'),(0x62ec90,'cmp','qword ptr [rax + 0x20], rdx'),
                (0x62ec94,'jb','0x62ec9f'),(0x62ec96,'mov','rcx, rax'),(0x62ec99,'mov','rax, qword ptr [rax + 8]'),
                (0x62ec9f,'mov','rax, qword ptr [rax]'),(0x62eca7,'lea','rax, [rsi + 8]'),
                (0x62ecab,'cmp','rcx, rax'),(0x62ecae,'je','0x62ecb6'),(0x62ecb0,'cmp','rdx, qword ptr [rcx + 0x20]'),
                (0x62ecb4,'jae','0x62ecb9'),(0x62ecb6,'mov','rcx, rax'),(0x62ecb9,'cmp','rcx, r8'),
                (0x62ecbc,'je','0x62ed36'),(0x62ecbe,'mov','rax, qword ptr [rsi + 0x18]'),
                (0x62eccc,'lea','rdi, [rsi + 8]'),(0x62ecd0,'mov','rbx, rdi'),
                (0x62ecd8,'cmp','qword ptr [rax + 0x20], rdx'),(0x62ecdc,'jb','0x62ece7'),
                (0x62ecde,'mov','rbx, rax'),(0x62ece1,'mov','rax, qword ptr [rax + 8]'),(0x62ece7,'mov','rax, qword ptr [rax]'),
                (0x62ecf4,'cmp','rdx, qword ptr [rbx + 0x20]'),(0x62ecf8,'jae','0x62ecfd'),
                (0x62ecfd,'cmp','rbx, rdi'),(0x62ed00,'je','0x62ed2c'),(0x62ed02,'dec','dword ptr [rsi + 0x28]'),
                (0x62ed05,'mov','rcx, rbx'),(0x62ed0d,'mov','rdx, rdi'),(0x62ed10,'mov','rcx, rbx'),
                (0x62ed18,'mov','rax, qword ptr [rsi + 0x30]'),(0x62ed1c,'lea','rcx, [rsi + 0x30]'),
                (0x62ed20,'mov','r8d, 0x28'),(0x62ed26,'mov','rdx, rbx')]
    for pc,m,a in operations:P.need(ix,pc,m,a)
    caller_pins=[(0x62bd5b,'mov','rcx, qword ptr [rip + 0x1953856]'),(0x62bd62,'test','rcx, rcx'),
                 (0x62bd65,'je','0x62bd7a'),(0x62bd67,'mov','r8d, dword ptr [rip + 0x1953822]'),
                 (0x62bd6e,'lea','rdx, [rax + 0x40]'),(0x62bd72,'add','rdx, rsi'),(0x62bd75,'call','0x62ec70')]
    for pc,m,a in caller_pins:P.need(c,pc,m,a)
    if c[0x62bd5b]['memory'][0]['rip_target']!='0x1f7f5b8' or c[0x62bd67]['memory'][0]['rip_target']!='0x1f7f590':raise ValueError('retained caller globals changed')
    edges,dom=graph(ix,0x62ec70,0x62ed3c)
    backward=[(p,t) for p,targets in edges.items() for t in targets if t<=p]
    if sorted(backward)!=[(0x62eca5,0x62ec90),(0x62eced,0x62ecd8)]:raise ValueError('unexpected normal removal repetition')
    for pc in (0x62ed08,0x62ed13,0x62ed29):
        if 0x62ed02 not in dom[pc]:raise ValueError('container count decrement does not dominate removal call')
    if not {0x62ed08,0x62ed13}<=dom[0x62ed29]:raise ValueError('node-helper before allocator order missing')
    helper_mem=[]
    for g in cfgs[1:]:
        a,z=int(g['entry'],16),int(g['end_exclusive'],16)
        data=[(p,m) for p,i in ix.items() if a<=p<z for m in i['memory'] if m['role']!='addr']
        if any(m.get('rip_target') or m.get('index') or m['displacement'] not in (0,8,16,24) for pc,m in data):raise ValueError('node-helper memory footprint exceeds verified header domain')
        helper_mem.append(dict(entry=g['entry'],header_displacements=sorted({m['displacement'] for pc,m in data}),instruction_accesses=len(data)))
    empty_path=[0x62ec70,0x62ec72,0x62ec76,0x62ec79,0x62ec7d,0x62ec80,0x62ec84,0x62ec88,0x62ec8b,0x62ec8e,
                0x62eca7,0x62ecab,0x62ecae,0x62ecb6,0x62ecb9,0x62ecbc,0x62ed36,0x62ed3a,0x62ed3b]
    if any(b not in edges[a] for a,b in zip(empty_path,empty_path[1:])) or any(ix[p]['mnemonic']=='call' for p in empty_path):raise ValueError('empty-bank counterexample path invalid')
    result=dict(status='PRODUCER_CHECKED_SELECTED_BANK_REMOVAL_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,
                source_pins=pins,required_invocation_receipts=receipts,annotation_prerequisites=annotations,normal_cfgs=cfgs,
                instruction_pins=[dict(pc=hex(pc),mnemonic=m,args=a) for pc,m,a in operations],normal_loop_edges=[dict(pc=hex(p),target=hex(t)) for p,t in backward],
                helper_header_footprints=helper_mem,bank_address='low64(context + 56*zeroextend32(incomingR8D))',
                caller_arguments=dict(context_global='0x1f7f5b8',bank_global='0x1f7f590',key='selected element address+40',null_context_skips_call=True),
                established=[
                    'The original wrapper selects exactly one56B bank from incomingR8D; it has no local bank-range check or bank-iteration loop. The retained62BD75 release caller supplies the current bank global, not a stored queue-time bank.',
                    'Two unsigned pointer-key lower-bound searches use node+20, right+0, left+8, root bank+18 and sentinel bank+8. Under a valid finite ordered unique-key tree their final >= comparisons admit equality only. A miss exits before decrement/helpers/allocator.',
                    'A found node causes one DEC32 of bank+28, then16D6D0(node),16DA60(node,sentinel), then allocator-record+30 vslot18(record,node,28h). The two only wrapper loops are pre-call searches; helper/free order is source-dominated. This is the container count, not an explicit texture element+38 write.',
                    'The verified four node helpers access only header offsets0/8/10/18, with no RIP/global reads or async key+20 dereference/callback target. Their only calls close to the two original call-free rotation leaves. The only remaining opaque call in this closure is the allocator interface slot18; its side effects are not certified.',
                    'An empty selected bank returns along a checked no-call path. Therefore a valid state with key queued in another distinct bank, current bank empty and caller bank changed is a conditional counterexample to universal all-bank cancellation. It requires no native stub or helper effects. Natural bank changes with a pending texture remain unproved.',
                ],counterexample=dict(kind='different-bank-empty-selection',queued_bank=0,release_bank=1,selected_root=0,other_bank_contains_key=True,
                                       normal_path=[hex(p) for p in empty_path],opaque_calls=0,
                                       conclusion='Wrapper returns without accessing the other bank or removing its key; conditional state, not natural gameplay/reachability'),
                assumptions=['Valid nonwrapping bank array/address, finite ordered unique-key tree and node-header link closure within the selected tree/sentinel',
                             'Stable bank/tree/key state and normal ABI-preserving helper/allocator returns for ordinary found-key order; allocator effects excluded',
                             'Distinct banks/texture object/async data for differentiating container+28 from element+38 and for the conditional other-bank witness'],
                limitations=['No actual scheduler/bank initialization, natural queue-time versus release-time bank changes, complete bank writers or caller set',
                             'No executing-job drain/cancellation, native allocator effects, asynchronous races, ownership/reuse or lifetime guarantee',
                             'Node header access closure is conditional on valid contained links; malformed/aliased pointers can target other state',
                             'Retained OPUS release/constructor semantics are reused; no producer or external review campaign credited as ours'],
                affected_claims=['OPUS texture ownedBlock release must state selected current bank and separate pendingCount ownership/drain',
                                 'FABLE keyed scheduler removal versus all-bank cancellation and running-work lifetime'],
                next_discriminator='Prove original bank-global writers/caller ordering or element+38 writer closure if unowned and still required; never infer natural wrong-bank cancellation from this conditional witness',
                checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
                cleanup='Original/retained file reads only; finite foreground scripts; no PC/game/input/instrument/save/config/reference/peer-process mutation')
    out.open('x').write(json.dumps(result,indent=2)+'\n')
    print('Selected current-bank/key removal closure proved; empty other-bank witness has no opaque calls; natural lifetime OPEN')


if __name__=='__main__':main()
