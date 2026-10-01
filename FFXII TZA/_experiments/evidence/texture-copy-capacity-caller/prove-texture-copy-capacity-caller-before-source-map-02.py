"""Source invariant: the selected normal caller supplies K=min(N,old count).

All three normal unwind fragments and all branches, not entry-fragment output.
Upstream helper evidence is required and requalified. No normal caller/lifetime
closure is inferred from raw-reference absence or from a forced invocation.
"""
import importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('retained_normal','prove-title-queue-consumption.py');S=module('actual_annotations','validate-title-source-annotations.py')
def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(src,'texture-copy-capacity-caller-source-01.json',pins);agreement=S.validate(raw)
    if len(raw['ranges'])!=1 or (raw['ranges'][0]['start'],raw['ranges'][0]['end_exclusive'],raw['ranges'][0]['sha256'])!=('0x627da0','0x627e4f','95493508b9d494abfe83909a3efc4798719e3e43a2a21d0b1251ac9b0fbac2c5'):raise ValueError('wrong/incomplete capacity caller body')
    entries=[[0x627DA0,0x627DFE,0x1DA8448],[0x627DFE,0x627E38,0x1DA845C],[0x627E38,0x627E4F,0x1DA8470]]
    if raw.get('pdata_entries')!=entries or raw.get('padding')!='cc' or len(raw.get('unwind',[]))!=3:raise ValueError('missing normal caller fragments')
    for q,e,header in zip(raw['unwind'],entries,['01140800','21050200','21000000']):
        z=bytes.fromhex(q['raw']);at=(4+z[2]*2+3)&~3;flags=z[0]>>3
        chain=[v+0x120000 for v in struct.unpack_from('<III',z,at)] if flags&4 else None
        if q['address']!=hex(e[2]) or z[:4].hex()!=header or q['header']!=header or q['flags']!=flags or q['chain']!=chain or (flags&4 and chain!=entries[0]):raise ValueError('unwind chain/root disagreement')
    helper,h=P.load(src,'texture-copy-construction-source-01.json',pins);helper_agreement=S.validate(helper)
    dep=src/'texture-copy-construction-result-01.json';r=json.loads(dep.read_text());pins.append(dict(path=dep.name,sha256=P.sha(dep)))
    if r.get('producer_complete') is not True or r.get('status')!='PRODUCER_CHECKED_COPY_COUNTER_AND_CAPACITY_PRECONDITIONS_INDEPENDENT_PENDING' or r.get('source_pins')!=[dict(path='texture-copy-construction-source-01.json',sha256=P.sha(src/'texture-copy-construction-source-01.json'))]:raise ValueError('missing/failed helper prerequisite')
    expected_helper={'0x61d100':'b941ad50789f7b4b2a35e3da877899801df0ca6c2ec646f204af368ea78fd617','0x613770':'574f2205a5d275c169988b327b367574491ccf35eca0d1f115b65c507906e2ec','0x61c250':'557e57e1c34abeb4ed8ab4dcfa308660f9c8a4f5db145ed668ad2f3123e62d8e'}
    if len(helper['ranges'])!=3 or any(q['start'] not in expected_helper or q['sha256']!=expected_helper[q['start']] for q in helper['ranges']):raise ValueError('helper original bytes changed')
    cfg=P.closed(x,0x627DA0,0x627E4F)
    if cfg['calls']!=[dict(pc='0x627de8',target='0x61d100'),dict(pc='0x627e24',target='0x584730')]:raise ValueError('caller native boundary changed')
    for pc,m,a in [(0x627DB4,'mov','r9d, dword ptr [rcx]'),(0x627DB7,'mov','esi, edx'),(0x627DB9,'btr','r9d, 0x1f'),(0x627DBE,'mov','rdi, rcx'),(0x627DC1,'cmp','edx, dword ptr [rcx]'),(0x627DC3,'je','0x627e38'),(0x627DC5,'cmp','r9d, 1'),(0x627DC9,'jbe','0x627dd1'),(0x627DCB,'mov','rbx, qword ptr [rcx + 8]'),(0x627DD1,'test','r9d, r9d'),(0x627DD6,'lea','rbx, [rcx + 8]'),(0x627DDC,'xor','ebx, ebx'),(0x627DDE,'cmp','esi, r9d'),(0x627DE1,'mov','r8, rbx'),(0x627DE4,'cmovb','r9d, esi'),(0x627DE8,'call','0x61d100'),(0x627DED,'mov','rbp, rax'),(0x627DF0,'test','rax, rax'),(0x627DF3,'jne','0x627dfe'),(0x627DF5,'test','esi, esi'),(0x627DF7,'je','0x627dfe'),(0x627DF9,'lea','eax, [rbp + 0xd]'),(0x627DFE,'mov','qword ptr [rsp + 0x30], r14'),(0x627E03,'lea','r14, [rdi + 8]'),(0x627E07,'cmp','rbx, rbp'),(0x627E0A,'je','0x627e29'),(0x627E0C,'cmp','rbx, r14'),(0x627E0F,'je','0x627e29'),(0x627E11,'mov','eax, dword ptr [rdi]'),(0x627E13,'shr','eax, 0x1f'),(0x627E16,'not','al'),(0x627E18,'test','al, 1'),(0x627E1A,'je','0x627e29'),(0x627E1C,'test','rbx, rbx'),(0x627E21,'mov','rcx, rbx'),(0x627E29,'cmp','rbp, r14'),(0x627E2E,'mov','qword ptr [r14], rbp'),(0x627E36,'mov','dword ptr [rdi], esi'),(0x627E38,'xor','eax, eax')]:P.need(x,pc,m,a)
    P.need(h,0x61D114,'mov','esi, r9d');P.need(h,0x61D11A,'mov','edi, edx');P.need(h,0x61D143,'mov','r8d, esi')
    # Domination over actual original normal instruction edges; no synthetic success.
    graph={};pred={p:set() for p in x}
    for pc,i in x.items():
        n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        edges=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [n,int(i['args'],16)] if m.startswith('j') else [n]
        graph[pc]=edges
        for nxt in edges:pred[nxt].add(pc)
    root=0x627DA0;dom={p:({root} if p==root else set(x)) for p in x}
    changed=True
    while changed:
        changed=False
        for pc in x:
            if pc==root:continue
            v={pc}|set.intersection(*(dom[q] for q in pred[pc]))
            if v!=dom[pc]:dom[pc]=v;changed=True
    required={0x627DB4,0x627DB7,0x627DB9,0x627DDE,0x627DE4}
    if not required<=dom[0x627DE8] or pred[0x627DE8]!={0x627DE4}:raise ValueError('capacity clamp does not dominate helper call')
    result=dict(status='PRODUCER_CHECKED_SELECTED_CALLER_CAPACITY_INVARIANT_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=agreement,helper_annotation_prerequisite=helper_agreement,normal_cfg=cfg,call_dominators=[hex(p) for p in sorted(required)],checker_sha256=P.sha(pathlib.Path(__file__)),question='Does the selected original627DA0 caller enforce the helper copy-capacity precondition?',
      established=[
        'On every normal path reaching627DE8, oldcount=qword-record DWORD&7FFFFFFF and newN=EDX low32. CMP newN,oldcount / unsigned CMOVB sets R9D=min(newN,oldcount), with no call or intervening write before61D100. The clamp dominates that call across all175B/three unwind fragments. Thus this caller suppliesK<=N for all u32N/oldWORD bitpatterns, excluding the helper-only N2/K3 counterexample on this path.',
        'Old source isNULL for masked0, record+8 for1, and pointer[record+8] for>1. If input newN equals the full unmasked oldDWORD, the caller returns0 without allocating/copying/freeing. Comparing the unmasked word is distinct from the masked copy count.',
        'NULL helper output with nonzero newN returns0xD before changing the record or reaching old-storage free; newN0 withNULL output is an accepted success path. Success conditionally calls584730 on old storage only when old!=new, old!=record+8, oldnonNULL and old bit31clear; it then stores the returned pointer when different frominline and writes the newN DWORD, returning0. Nativefree effects, external record ownership and high-bit newN validity remain open.',
        'This local caller/helper closure preserves copied wait-counter and userdata fields and performs no local wait, queue-key removal, copied-member rebinding or async invocation. That does not establish natural pending resize or transitive allocator/free behavior; higher callers may enforce the missing lifetime premise.'
      ],assumptions=['Correct normally returning ABI/callees, valid nonwrapping record/source/output/stack storage','Interfering/transitive allocator/free effects excluded from local guard/write-order conclusions','N must additionally satisfy the encoded count-domain/storage interpretation for ordinary reconstructed use; this proof does not sanitize arbitrary new high-bit values'],limitations=['Only this selected caller, not a complete direct/indirect/RVA/indexed caller census','No game/resize/timing observation or universal allocator, cancellation, lifetime or malformed-state guarantee','Helper producer and original bytes requalified, independent acceptance still pending; no external tests/census credit'],affected_claims=['OPUS bounded resize caller ABI, capacity clamp and failure/record-publication contract','FABLE counter-copy versus pending async object/lifetime preconditions'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Original bytes/static proof only; no game/PC/instrument/save/config/reference/peer mutation')
    out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n');print('Selected original caller proves K<=N; pending-resize/lifetime/high-bit domain remain OPEN')
if __name__=='__main__':main()
