"""Focused shipped test-zone index join. Source/data only; no game or census replay."""
import hashlib, importlib.util, json, pathlib, shutil, struct, sys

W = pathlib.Path(__file__).resolve().parent
def module(name, file):
    s = importlib.util.spec_from_file_location(name, W / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
C = module('bts_shared_capture', 'capture-index-path.py')
S = module('bts_annotations', 'validate-title-source-annotations.py')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = pathlib.Path(sys.argv[1])
    if out.exists(): raise ValueError('immutable capture exists')
    data = C.EXE.read_bytes()
    if hashlib.sha256(data).hexdigest() != C.SHA: raise ValueError('reference image changed')
    e = struct.unpack_from('<I', data, 60)[0]; o = struct.unpack_from('<H', data, e + 20)[0]
    sections = [struct.unpack_from('<IIII', data, e + 24 + o + k * 40 + 8)
                for k in range(struct.unpack_from('<H', data, e + 6)[0])]
    def read(a, n):
        for vs, va, rs, ro in sections:
            if C.BASE + va <= a and a + n <= C.BASE + va + rs:
                return data[ro + a - C.BASE - va:ro + a - C.BASE - va + n]
        raise ValueError('unbacked original bytes ' + hex(a))
    rva, n = struct.unpack_from('<II', data, e + 24 + 112 + 24)
    pd = [tuple(C.BASE + x for x in struct.unpack('<III', read(C.BASE + rva + k, 12)))
          for k in range(0, n, 12)]
    extents = [(0x3ea6e0, 0x3ea70b, 0x1d529d0), (0x2df9a0, 0x2e04dc, 0x1d7bc50)]
    if any(t not in pd for t in extents): raise ValueError('named normal extent changed')
    C.RANGES = [(0x264ed0, 0x264f01)] + [t[:2] for t in extents]
    C.main(); raw = json.loads(out.read_text())
    raw.update(wrapper_complete=True, pdata_entries=[list(t) for t in extents],
               leaf_boundary='264ED0..264F01 contains both RETs; following byte is CC; no pdata claimed',
               annotation_prerequisite=S.validate(raw), invocation_driver_sha256=sha(pathlib.Path(__file__)))
    # This exact old input is reused; no new full caller capture or historical experiment run.
    retained = W / 'index-path-raw-02.json'
    v = json.loads(retained.read_text()); S.validate(v)
    q = next(q for q in v['ranges'] if q['start'] == '0x32fca0')
    if (q['end_exclusive'], q['sha256']) != ('0x330048', '1d796bf176912574660eedaa1919235222d3a34b66f6492014cae31b3884f9f7'):
        raise ValueError('retained caller changed')
    if bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])) != read(0x32fca0, 0x330048 - 0x32fca0):
        raise ValueError('retained caller differs from image')
    raw['retained_caller'] = dict(path=retained.name, sha256=sha(retained), range=q,
                                  limits='Exact original retained range; no fresh native/caller-reachability run')
    # Preserve full primary file bytes and reused exact FST inputs, with all pins established first.
    primary = [(f'map-ref-{locale}.bin', pathlib.Path(f'D:/FFXII_TZA_extract/ps2data/image/ff12/{locale}/common/map_ref.bin'),
                '7c63552fd2c57438bea4eb1f27d6f52f4f6e7bd2430dbb5af0373a04e15b728b') for locale in ['ch', 'in']]
    pins = json.loads((W / 'index-domain-result-01.json').read_text())['results']
    if len(pins) != 12: raise ValueError('retained twelve language inputs missing')
    primary += [(p['name'], W / 'fst-inputs-01' / p['name'], p['sha256']) for p in pins]
    if any(sha(p) != h for name, p, h in primary): raise ValueError('required primary input changed')
    dst = W / 'bts-index-binding-inputs-01'
    if dst.exists(): raise ValueError('immutable inputs exist')
    dst.mkdir(); inputs = []
    for name, p, h in primary:
        shutil.copyfile(p, dst / name)
        inputs.append(dict(path=f'{dst.name}/{name}', sha256=h, bytes=p.stat().st_size,
                           source=str(p), evidence='primary authored data' if name.startswith('map-ref') else 'retained shipping FST input'))
    # Pointer arrays needed by this join, not an executable classification census.
    ix = [i for q in raw['ranges'] if q['start'] == '0x2df9a0' for i in q['instructions']]
    installs = []
    for k, i in enumerate(ix):
        if i['mnemonic'] != 'mov' or not i['memory']: continue
        dest = i['memory'][0].get('rip_target')
        if dest not in ['0x215f028', '0x215f0a8', '0x215f0d0']: continue
        reg = i['args'].split(', ')[-1]
        # Keep the actual local producer window. The checker must verify no intervening write to reg.
        producer = next((j for j in reversed(ix[:k]) if j['args'].split(',')[0] == reg), None)
        if not producer or producer['mnemonic'] != 'lea' or len(producer['memory']) != 1 or not producer['memory'][0]['rip_target']:
            raise ValueError('unprepared table producer')
        root = int(producer['memory'][0]['rip_target'], 16)
        installs.append(dict(store_pc=i['pc'], destination=dest, producer_pc=producer['pc'], root=hex(root)))
    nmb = [i for i in installs if i['destination'] == '0x215f0d0']
    if len(nmb) != 2: raise ValueError('NMB installation set changed')
    metadata = []
    for t in nmb:
        entries = []
        for a in range(321):
            p = struct.unpack('<Q', read(int(t['root'], 16) + 8 * a, 8))[0]
            # Full array raw words plus exact strings; a null is an observed qword, not absent evidence.
            s = None if p == 0 else read(p, 192).split(b'\0', 1)[0].decode('ascii')
            entries.append(dict(area=a, pointer=hex(p), name=s))
        metadata.append(dict(root=t['root'], raw_hex=read(int(t['root'], 16), 321 * 8).hex(), entries=entries))
    areas = sorted({x['area'] for t in metadata for x in t['entries'] if x['name'] and '\\bts_' in x['name']})
    fields = []
    m = (dst / 'map-ref-ch.bin').read_bytes(); off = struct.unpack_from('<I', m, 4)[0]
    for f in range(1315):
        if struct.unpack_from('<H', m, off + 8 * f + 4)[0] in areas: fields.append(f)
    focus = sorted(set(fields + [12, 129, 124]))  # title, populated asp_b, empty-table asp_a controls
    sparse = []
    for t in installs:
        if t['destination'] == '0x215f0d0': continue
        ids = [3 * f + k for f in focus for k in range(3)] if t['destination'] == '0x215f028' else [2 * a + k for a in sorted(set(areas + [12, 94, 95])) for k in range(2)]
        values = []
        for index in ids:
            p = struct.unpack('<Q', read(int(t['root'], 16) + 8 * index, 8))[0]
            values.append(dict(index=index, bytes=read(int(t['root'], 16) + 8 * index, 8).hex(),
                               name=None if p == 0 else read(p, 192).split(b'\0', 1)[0].decode('ascii')))
        sparse.append(dict(root=t['root'], destination=t['destination'], values=values))
    raw.update(inputs=inputs, installs=installs, nmb_metadata=metadata, focused_pointer_arrays=sparse,
               fields_examined=focus, limits='Original literal table installations and focused indices only; NMB name is authored metadata, not a script-load/live binding; all alias/other writers/overrides/timing remain separate')
    out.write_text(json.dumps(raw, indent=2)+'\n', encoding='utf-8')
    print('Captured focused original table/index binding and primary MRF; twelve FST inputs reused; no game')

if __name__ == '__main__': main()
