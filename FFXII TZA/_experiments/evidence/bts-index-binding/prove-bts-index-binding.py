"""Focused original table/data join; no inference from directory names to live execution."""
import hashlib, importlib.util, json, pathlib, struct, sys
W = pathlib.Path(__file__).resolve().parent
def module(name, file):
    s = importlib.util.spec_from_file_location(name, W / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
P = module('bts_proof', 'prove-title-queue-consumption.py')
S = module('bts_actual_roles', 'validate-title-source-annotations.py')
MRF_SHA='7c63552fd2c57438bea4eb1f27d6f52f4f6e7bd2430dbb5af0373a04e15b728b'
FST_SHA={
 'FileSizeTable_ASIA.fst':'0f9c202078c753b70749b1149998eb747f4dd57067e3cf8538ee77d33b44e4d3',
 'FileSizeTable_CH.fst':'1f7e4ca1ea1a003d2ade2a6338be3513f659ab986efb3dc734db12c36498075b',
 'FileSizeTable_CN.fst':'e33cb21a6ae3ac84aaf7500d724e20aefdf6cbc6e7ff9e97ee2faa8448f41258',
 'FileSizeTable_DE.fst':'d80b86be6f53166701abf5c15356c449421fbb41f2e82e105044a406e90e350c',
 'FileSizeTable_ES.fst':'4aec6d0e32f56dbe95fd9c76aef4685c42e2eb043e1ffffa2059c2ba5c2af5a9',
 'FileSizeTable_FR.fst':'d8f6211d36a6207a2a20ecbfe0e8b53f12b6ba5c473f4693fec4730e30293213',
 'FileSizeTable_IN.fst':'0f9c202078c753b70749b1149998eb747f4dd57067e3cf8538ee77d33b44e4d3',
 'FileSizeTable_IT.fst':'948c7aee093a63b210972227e68172d79303f7a1e2a9a2d44b4012b589e7fdc1',
 'FileSizeTable_JP.fst':'0f9c202078c753b70749b1149998eb747f4dd57067e3cf8538ee77d33b44e4d3',
 'FileSizeTable_KR.fst':'83a4dda471c8b9744375227389730097ba8502984e66c88dc5de0738549976ca',
 'FileSizeTable_UK.fst':'2451762db99591c4b8417d1278d6120f20226f338f4da36aa2ff544d713bb40f',
 'FileSizeTable_US.fst':'3a03ea77c689d1f48428c440a272b7dbfd77b121758bfd2c5ac0697ceeeb2b3e'}

def main():
    if len(sys.argv) not in (2, 3): raise ValueError('fresh result [disposable source]')
    out = pathlib.Path(sys.argv[1]); src = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists(): raise ValueError('immutable result exists')
    driver = src / 'capture-bts-index-binding.py'
    st = json.loads((src / 'bts-index-binding-capture-02.status.json').read_text())
    if st.get('exit') != 0 or st.get('driver_sha256') != P.sha(driver):
        raise ValueError('required capture failed or stale')
    if not (src / 'bts-index-binding-capture-02.stdout').read_bytes().strip() or (src / 'bts-index-binding-capture-02.stderr').read_bytes().strip():
        raise ValueError('required capture output incomplete')
    pins = []; raw, ix = P.load(src, 'bts-index-binding-source-02.json', pins)
    if raw.get('invocation_driver_sha256') != P.sha(driver): raise ValueError('capture driver changed')
    annotations = S.validate(raw)
    data = (S.ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest() != P.SHA: raise ValueError('reference image changed')
    e = struct.unpack_from('<I', data, 60)[0]; o = struct.unpack_from('<H', data, e+20)[0]
    secs = [struct.unpack_from('<IIII', data, e+24+o+k*40+8) for k in range(struct.unpack_from('<H', data, e+6)[0])]
    def read(a, n):
        for vs, va, rs, ro in secs:
            if 0x120000+va <= a and a+n <= 0x120000+va+rs:
                return data[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise ValueError('unbacked image span')
    for q in raw['ranges'] + [raw['retained_caller']['range']]:
        a = int(q['start'], 16); n = int(q['end_exclusive'], 16)-a
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])) != read(a, n):
            raise ValueError('original instruction identity mismatch')
    inline = raw['installer_inline_data']
    if (inline['start'], inline['end_exclusive'], bytes.fromhex(inline['bytes'])) != ('0x2e04af', '0x2e04dc', read(0x2e04af,45)):
        raise ValueError('original inline data mismatch')
    ops = [(0x264ee6,'movsxd','rdx, ecx'),(0x264ee9,'movsxd','rcx, dword ptr [r8 + 4]'),
           (0x264ef0,'lea','rax, [rcx + rdx*8]'),(0x264ef9,'movzx','eax, word ptr [rax + 4]'),
           (0x3ea6e8,'call','0x264ed0'),(0x3ea6f9,'mov','ecx, eax'),(0x3ea700,'jmp','0x3ea820'),
           (0x2dfbb3,'cmp','eax, 0xa'),(0x2dfbb6,'ja','0x2dff32'),
           (0x2dfbbe,'mov','ecx, dword ptr [r10 + rax*4 + 0x1c04b0]'),(0x2dfbc6,'add','rcx, r10'),(0x2dfbc9,'jmp','rcx')]
    for pc,m,a in ops: P.need(ix,pc,m,a)
    # Finite switch targets are data, and must all land on decoded code boundaries.
    switch = [0x120000+x for x in struct.unpack('<11I',read(0x2e04b0,44))]
    if any(x not in ix or not 0x2df9a0 <= x < 0x2e04af for x in switch):
        raise ValueError('switch target is not original code boundary')
    installer = [i for q in raw['ranges'] if q['start']=='0x2df9a0' for i in q['instructions']]
    # Recompute all literal installations into these three globals in this function.
    actual=[]
    for k,i in enumerate(installer):
        if i['mnemonic']!='mov' or not i['memory']: continue
        dest=i['memory'][0].get('rip_target')
        if dest not in ['0x215f028','0x215f0a8','0x215f0d0']: continue
        reg=i['args'].split(', ')[-1]
        j=next((j for j in reversed(installer[:k]) if j['args'].split(',')[0]==reg),None)
        if not j or j['mnemonic']!='lea' or not j['memory'][0]['rip_target']: raise ValueError('unknown table producer')
        actual.append(dict(store_pc=i['pc'],destination=dest,producer_pc=j['pc'],root=j['memory'][0]['rip_target']))
    if actual != raw['installs']: raise ValueError('table installation attribution changed')
    roots={key:[i['root'] for i in actual if i['destination']==key] for key in ['0x215f028','0x215f0a8','0x215f0d0']}
    if [len(roots[k]) for k in roots] != [10,2,2]: raise ValueError('literal table alternatives incomplete')
    expected={'bts-index-binding-inputs-01/'+n:h for n,h in FST_SHA.items()}
    expected.update({'bts-index-binding-inputs-01/map-ref-'+locale+'.bin':MRF_SHA for locale in ['ch','in']})
    if len(raw['inputs'])!=14 or {p['path']:p['sha256'] for p in raw['inputs']}!=expected:
        raise ValueError('required primary identity set changed')
    for p in raw['inputs']:
        q=src/p['path']
        if not q.is_file() or P.sha(q)!=p['sha256'] or q.stat().st_size!=p['bytes']:
            raise ValueError('required primary input changed')
        pins.append(dict(path=p['path'],sha256=p['sha256']))
    mrf=[]
    for name in ['map-ref-ch.bin','map-ref-in.bin']:
        d=(src/'bts-index-binding-inputs-01'/name).read_bytes()
        if len(d)!=12288 or d[:4]!=b'MRF\x02': raise ValueError('wrong MRF layout')
        a,z=struct.unpack_from('<II',d,4)
        if a!=48 or (z-a)%8 or (z-a)//8!=1315: raise ValueError('wrong MRF field boundary')
        mrf.append([struct.unpack_from('<4H',d,a+8*f) for f in range(1315)])
    if mrf[0]!=mrf[1]: raise ValueError('MRF locale contradiction')
    meta=[]
    for t in raw['nmb_metadata']:
        root=int(t['root'],16)
        if t['root'] not in roots['0x215f0d0'] or bytes.fromhex(t['raw_hex'])!=read(root,321*8):
            raise ValueError('NMB metadata identity changed')
        if len(t['entries'])!=321: raise ValueError('NMB metadata incomplete')
        found={}
        for x in t['entries']:
            p=struct.unpack('<Q',read(root+8*x['area'],8))[0]
            name=None if not p else read(p,192).split(b'\0',1)[0].decode('ascii')
            if (x['pointer'],x['name'])!=(hex(p),name): raise ValueError('NMB name pointer identity changed')
            if name and '\\bts_' in name:
                zone=name.split('\\')[-1].removesuffix('.nmb')
                found[zone]=x['area']
        meta.append(found)
    if len(meta)!=2 or meta[0]!=meta[1] or len(meta[0])!=31:
        raise ValueError('test-zone metadata identities incomplete')
    rows=[]
    for zone,a in sorted(meta[0].items()):
        fs=[f for f,row in enumerate(mrf[0]) if row[2]==a]
        rows.append(dict(zone=zone,area=a,fields=fs,field_record_words=[list(mrf[0][f]) for f in fs]))
    fields=sorted({f for row in rows for f in row['fields']}); areas=sorted(meta[0].values())
    if len(fields)!=31 or any(len(row['fields'])!=1 for row in rows): raise ValueError('test-zone MRF relation changed')
    if set(areas)&{94,187,217,280}: raise ValueError('test-zone maps to a known empty-table area')
    arrays=raw['focused_pointer_arrays']
    if {t['root'] for t in arrays}!=set(roots['0x215f028']+roots['0x215f0a8']):
        raise ValueError('focused table alternatives missing')
    for t in arrays:
        root=int(t['root'],16); by={x['index']:x for x in t['values']}
        ids=[3*f+k for f in fields for k in range(3)] if t['destination']=='0x215f028' else [2*a+k for a in areas for k in range(2)]
        for index in ids:
            if index not in by: raise ValueError('required focused index missing')
            x=by[index]; b=read(root+8*index,8)
            if bytes.fromhex(x['bytes'])!=b or b!=bytes(8) or x['name'] is not None:
                raise ValueError('test-zone missing-path proposition refuted')
        # Positive path control: same table, same actual pointer decode, title slot.
        index=36 if t['destination']=='0x215f028' else 24
        x=by[index]; p=struct.unpack('<Q',read(root+8*index,8))[0]
        if not p or x['bytes']!=struct.pack('<Q',p).hex() or x['name']!=read(p,192).split(b'\0',1)[0].decode('ascii') or '\\ttl_a\\' not in x['name']:
            raise ValueError('positive path control failed')
    fsts=[]
    for p in raw['inputs']:
        if not p['path'].endswith('.fst'): continue
        d=(src/p['path']).read_bytes()
        if len(d)!=41*5000*4: raise ValueError('FST extent mismatch')
        entries=[]
        for kind,ids in [(5,[3*f+k for f in fields for k in range(3)]),(21,[2*a+k for a in areas for k in range(2)])]:
            vals=[struct.unpack_from('<i',d,4*(kind*5000+i))[0] for i in ids]
            if set(vals)!={-1}: raise ValueError('test-zone missing-size proposition refuted')
            entries.append(dict(kind=kind,indices=ids,values=vals))
        script_control=struct.unpack_from('<i',d,4*(5*5000+36))[0]
        ard_control=struct.unpack_from('<i',d,4*(21*5000+188))[0]
        # UK's literal title size is -1. Do not fabricate a title positive for it.
        # Every same-file ARD row has a positive asp_a entry; eleven title positives
        # and one UK missing entry are kept as separate measured facts.
        if ard_control!=224 or (p['path'].endswith('_UK.fst') and script_control!=-1) or (not p['path'].endswith('_UK.fst') and script_control<=0):
            raise ValueError('literal FST detection controls failed')
        fsts.append(dict(path=p['path'],entries=entries,title_ebp_size=script_control,asp_a_ard_positive_size=ard_control))
    if len(fsts)!=12: raise ValueError('FST alternatives incomplete')
    caller={int(i['pc'],16):i for i in raw['retained_caller']['range']['instructions']}
    for pc,m,a in [(0x32fcb0,'mov','r15d, edx'),(0x32fcbf,'movsxd','rdi, ecx'),(0x32fd19,'test','edi, edi'),(0x32fd1b,'jle','0x32fd3f'),(0x32fd3f,'mov','esi, 5'),(0x32fd44,'lea','ebp, [r15 + r15*2]'),(0x32fd4d,'call','0x32e400'),(0x32fd54,'jle','0x32fd69'),(0x32fd5a,'call','0x2df980'),(0x330014,'mov','r9d, ebp'),(0x33001f,'mov','r8d, esi'),(0x330022,'mov','edx, r15d'),(0x330025,'mov','ecx, edi'),(0x330029,'call','0x3306e0'),(0x330030,'call','0x330310')]:
        P.need(caller,pc,m,a)
    receipts=['capture-bts-index-binding.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py']+[f'bts-index-binding-capture-02{s}' for s in ['.status.json','.stdout','.stderr']]
    result=dict(status='PRODUCER_VALID_BTS_INDEX_BINDING_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,
        required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],annotation_prerequisite=annotations,
        rows=rows,focused_null_path_words=dict(script=31*3*10,ard_and_fpk=31*2*2),fst_alternatives=fsts,
        switch_targets=[hex(x) for x in switch],literal_installations=actual,
        established=['Both original namespace26 NMB arrays name the same31 bts zones at the same area indices. NMB naming is authored metadata; no NMB reader or live zone execution is established.',
        'In both unchanged primary MRF images these area indices select31 distinct field rows. The original getter reads unsignedWORD row+4, not persistence group+6. The refresh passes that value to3EA820 when changed/forced.',
        'For these31 area indices, both literal namespace21 arrays have NULL at2*area and2*area+1. They do not name any of the four shipped empty-table ARDs. All twelve retained shipping FSTs have-1 for those62indices.',
        'For the31 corresponding field IDs, all ten literal namespace5 alternatives have NULL at3*field+0,+1,+2; all twelve FSTs have-1 at the93 corresponding entries. Manager0 at the observed32FCA0 branch computes namespace5/base3*selector; arbitrary other manager/selector paths are not covered.',
        'Each array passes a real nonnull ttl_a pointer/string control. Each FST has positive asp_a ARD size224; eleven have positive ttl_a script size, while UK has-1 at that slot. These are separate literal observations, not a promised universal title positive. NULL/-1 observations are actual bounded entries, not a missing-output or no-hit result.',
        'This eliminates the numeric authored-index ambiguity under the unchanged normal MRF/literal-table premises. It does not prove a bts script executes with those IDs or is globally unreachable. No successfully loaded bts ARD or script is observed.'],
        limitations=['No new original-code/native/emulated/live execution, script census or external review run',
        'No universal bts unreachability: direct injection, aliases, embedded/copied script bodies, alternate selectors/managers, modified tables, runtime size overrides, other writers and stale/pending callbacks remain separate',
        'NMB directory labels are metadata, not a live script-storage pointer or lifetime guarantee',
        'Full primary-payload carrier330310/3306E0 and size override prerequisites are not newly proved; negative size alone is not a whole request-machine/lifetime proof',
        'No full GR18 E1 or OV/AQ closure; independent review and canonical consumption pending'],
        affected_claims=['FABLE GR18 bts numeric binding residual: authored MRF/literal paths can be resolved offline; leave actual natural script reachability explicit','OPUS GR18 adjudication must distinguish missing resource slots from a bound zero-count reward table'],
        next_discriminator='Inspect original330310/3306E0 primary request admission under manager0/selector field/no-size-override; does missing FST size prevent primary payload admission, and can ordinary field startup substitute another existing carrier? No menu/native setup.',
        learned_failure='Capture01 attempted to decode whole .pdata extent as code; NOP and11 RVA switch words followRET. Actualexit1/no result retained; capture02 separates data. Positive01 refused because UK title-size control is-1; preserve that literal missing value, use same-file positive asp_a ARD224 and11 separate title positives. No result from either failed invocation. Never decode inline data as access-role evidence or invent universal title availability.',
        checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
        cleanup='Finite original/data reads and private input copies only; no game/PC/input/instrument/save/config/reference/peer-process mutation')
    out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n')
    print('31 authored test-zone index mappings resolved;930 script/124 ARD path words NULL and12 FST alternatives checked; natural script reachability OPEN')
if __name__=='__main__': main()
