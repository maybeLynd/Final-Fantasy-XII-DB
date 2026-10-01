"""OV-42 bounded selector/FST discriminator. STATIC_ONLY, not natural reachability.
python prove-index-domain.py RAW_JSON TABLE_DIR OUTPUT_JSON
TABLE_DIR contains exact frozen FileSizeTable_*.fst bytes. No live process or game writes.
Domain 0..32767 is a declared bounded hypothesis, NOT an established bound on callers.
Rejects incomplete/mismatched primary evidence; mutations go through the same discriminator.
"""
import hashlib, json, pathlib, struct, sys

WITNESSES = {
    0x32f193: ('mov','dword ptr [r8], 8'),
    0x32f18c: ('lea','eax, [rdx*4]'),
    0x32f19e: ('lea','eax, [rdx + rdx*2]'),
    0x32f1a1: ('mov','dword ptr [r8], 5'),
    0x3dd610: ('movzx','eax, word ptr [rsp + 0x90]'),
    0x3dd618: ('inc','ax'),
    0x3dd61d: ('mov','word ptr [rbx + 0x12], ax'),
    0x3ddaa8: ('movsx','edx, word ptr [rbx + 0x12]'),
    0x3ddab9: ('call','0x32e620'),
    0x32e64a: ('test','edx, edx'),
    0x32e64c: ('jns','0x32e656'),
    0x2df963: ('imul','r8, rax, 0x1388'),
    0x2df96a: ('movsxd','rcx, edx'),
    0x2df974: ('add','r8, rcx'),
    0x2df977: ('mov','eax, dword ptr [rax + r8*4]'),
    0x32fed2: ('jl','0x32ff25'),
    0x32ff25: ('mov','rax, qword ptr [rbx + rcx + 0x21a6e70]'),
    0x32ff2d: ('mov','byte ptr [rax], 0'),
}

def signed16(x):
    x &= 0xffff
    return x-0x10000 if x&0x8000 else x

def evidence_gate(raw):
    if raw.get('method')!='A STATIC_ONLY' or raw.get('exe_sha256')!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':
        raise ValueError('wrong evidence identity')
    if not raw.get('ranges') or len(raw.get('controls',[]))!=3:
        raise ValueError('missing evidence, not valid empty result')
    if any(x['observed']!=x['expected'] for x in raw['controls']):
        raise ValueError('upstream observer failure')
    ins={int(x['pc'],16):x for r in raw['ranges'] for x in r['instructions']}
    for pc,(mn,args) in WITNESSES.items():
        if pc not in ins or (ins[pc]['mnemonic'],ins[pc]['args'])!=(mn,args):
            raise ValueError('original instruction witness mismatch at %x'%pc)
    # Require concrete corrected role classifications in the capture, not helper presence.
    for pc in [0x3dd61d,0x32ff2d]:
        if ins[pc]['memory'][0]['role']!='w': raise ValueError('capture did not classify store')

def analyze(raw, tables):
    evidence_gate(raw)
    if len(tables)!=12: raise ValueError('incomplete language input: require 12')
    results=[]
    for name,blob in sorted(tables.items()):
        if len(blob)!=41*5000*4: raise ValueError('wrong FST extent')
        words=struct.unpack('<205000I',blob)
        if words[0]!=57: raise ValueError('FST positive control failed')
        langs=[]
        for group,ns,stride in [(0,5,3),(1,8,4)]:
            negatives=0; first=None; positive_alias=[]; absent=0
            for selector in range(0x8000):
                full=stride*selector+1
                if signed16(full)>=0: continue
                negatives+=1
                if first is None: first=selector
                flat=ns*5000+full
                if flat>=len(words): raise ValueError('unobserved lookup extent')
                size=words[flat]
                if size==0xffffffff: absent+=1
                elif 0<size<0x80000000:
                    positive_alias.append(dict(selector=selector,full_index=full,narrowed=signed16(full),
                                               fst_flat_word=flat,aliased_kind=flat//5000,
                                               aliased_id=flat%5000,size=size))
            langs.append(dict(group=group,namespace=ns,stride=stride,selectors_examined=32768,
                              negative_count=negatives,first_negative_selector=first,
                              missing_size_count=absent,positive_aliased_sizes=len(positive_alias),
                              first_positive_alias=positive_alias[0] if positive_alias else None))
        results.append(dict(name=name,sha256=hashlib.sha256(blob).hexdigest(),groups=langs))
    return results

def main():
    rawpath,folder,out=map(pathlib.Path,sys.argv[1:])
    if out.exists(): raise ValueError('immutable result exists')
    raw=json.loads(rawpath.read_text()); tables={p.name:p.read_bytes() for p in folder.glob('FileSizeTable_*.fst')}
    results=analyze(raw,tables)
    # Same concrete checked path rejects lost prerequisites, missing inputs and altered store.
    controls=[]
    for tag,mut in [('missing_ranges',lambda r:r.update(ranges=[])),
                    ('observer_failed',lambda r:r['controls'][0].update(observed='r')),
                    ('wrong_narrowing',lambda r:next(x for z in r['ranges'] for x in z['instructions'] if x['pc']=='0x3dd618').update(args='eax'))]:
        clone=json.loads(json.dumps(raw)); mut(clone)
        try: analyze(clone,tables)
        except ValueError as e: controls.append(dict(case=tag,rejected=True,reason=str(e)))
        else: raise ValueError('required prerequisite mutation passed')
    try: analyze(raw,{})
    except ValueError as e: controls.append(dict(case='missing_tables',rejected=True,reason=str(e)))
    else: raise ValueError('empty inputs accepted')
    # Hand-calculated independent arithmetic boundary controls (not execution samples).
    boundary=[(3,10922,32767),(3,10923,-32766),(4,8191,32765),(4,8192,-32767),
              (4,16384,1),(4,24576,-32767)]
    if any(signed16(s*k+1)!=v for s,k,v in boundary): raise ValueError('arithmetic control failed')
    result=dict(method='A original-code analysis + exhaustive bounded-state/FST analysis',
                domain='nonnegative selectors 0..32767 only; caller domain still unproved',
                raw_sha256=hashlib.sha256(rawpath.read_bytes()).hexdigest(),
                driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                valid_controls=controls,boundary_controls=boundary,results=results,
                interpretation='FST extent/population alone cannot prove negative narrowed indices unreachable',
                natural_shipped_reachability='OPEN; need complete selector-producer/input bounds and load/owner scheduling')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print('VALID bounded analysis; languages=12; groups=2; prerequisite controls=4; natural reachability remains OPEN')

if __name__=='__main__': main()
