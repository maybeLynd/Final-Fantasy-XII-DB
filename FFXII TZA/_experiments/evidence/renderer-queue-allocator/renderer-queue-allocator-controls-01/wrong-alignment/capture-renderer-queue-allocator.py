"""Selected shipping allocator wrappers/import metadata; Method A only.

Reuses the reviewed capture path. A named PE import is not a loaded CRT module.
Read both exact normal roots; do not stub, execute or modify the reference.
"""
import hashlib, importlib.util, json, pathlib, struct, sys

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'

def module(name, file):
    s = importlib.util.spec_from_file_location(name, W / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

def main():
    out = pathlib.Path(sys.argv[1])
    if out.exists(): raise ValueError('immutable output exists')
    d = (ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(d).hexdigest() != SHA: raise ValueError('wrong original EXE')
    p = struct.unpack_from('<I', d, 60)[0]; opt = p + 24
    if d[p:p+4] != b'PE\0\0' or struct.unpack_from('<H', d, opt)[0] != 0x20b:
        raise ValueError('wrong PE64 header')
    base = struct.unpack_from('<Q', d, opt + 24)[0]
    if base != 0x120000: raise ValueError('wrong image base')
    ns = struct.unpack_from('<H', d, p + 6)[0]
    osize = struct.unpack_from('<H', d, p + 20)[0]
    sections = [struct.unpack_from('<IIII', d, opt + osize + 40*k + 8) for k in range(ns)]
    def read(rva, n):
        for vs, va, rs, ro in sections:
            if va <= rva and rva + n <= va + rs:
                return d[ro+rva-va:ro+rva-va+n]
        raise ValueError('unbacked original RVA')
    def cstr(rva):
        z = bytearray()
        for k in range(256):
            b = read(rva+k, 1)
            if b == b'\0': return z.decode('ascii')
            z.extend(b)
        raise ValueError('unterminated bounded import name')
    rva, size = struct.unpack_from('<II', d, opt + 112 + 3*8)
    if not size or size % 12: raise ValueError('incomplete exception directory')
    pd = [tuple(v+base for v in struct.unpack('<III', read(rva+12*k, 12))) for k in range(size//12)]
    roots = [(0x1edf80, 0x1edfda), (0x1edfe0, 0x1ee040)]
    expected = [(0x1edf80, 0x1edfda, 0x1d529d0), (0x1edfe0, 0x1ee040, 0x1d529d0)]
    rows = [e for e in pd if any(e[:2] == r for r in roots)]
    if rows != expected: raise ValueError('selected normal root changed')
    unwind = read(0x1d529d0-base, 8)
    if unwind.hex() != '0106020006320230': raise ValueError('selected unwind changed')
    table = read(0x902720-base, 32)
    if table.hex() != '80d616000000000010df1e000000000080df1e0000000000e0df1e0000000000':
        raise ValueError('physical allocator table changed')
    # Reuse the bounded original import reader method from the cleanup packet.
    targets = {0x8c2b40:'malloc', 0x8c2b48:'free', 0x8c2b60:'_aligned_malloc', 0x8c2b70:'_aligned_free'}
    rva, size = struct.unpack_from('<II', d, opt + 112 + 8)
    entries = []; terminated = False
    for k in range(size//20):
        blob = read(rva+20*k, 20)
        ilt, time, chain, name, iat = struct.unpack('<IIIII', blob)
        if blob == b'\0'*20: terminated = True; break
        if not ilt: raise ValueError('missing original lookup table')
        for target, label in targets.items():
            delta = target-base-iat
            if delta < 0 or delta % 8: continue
            idx = delta//8
            for j in range(idx+1):
                thunk = struct.unpack('<Q', read(ilt+8*j, 8))[0]
                if not thunk: break
            else:
                if thunk >> 63: raise ValueError('unnamed ordinal import')
                symbol = cstr(thunk+2)
                lookup = read(ilt+8*idx, 8); original_iat = read(target-base, 8)
                if original_iat != lookup: raise ValueError('original IAT/ILT mismatch')
                entries.append(dict(dll=cstr(name), name=symbol,
                    hint=struct.unpack('<H', read(thunk, 2))[0], descriptor_rva=hex(rva+20*k),
                    lookup_table_rva=hex(ilt), slot=idx, iat=hex(target), descriptor_bytes=blob.hex(),
                    lookup_bytes=lookup.hex(), original_iat_bytes=original_iat.hex(),
                    name_bytes=read(thunk, 2+len(symbol)+1).hex()))
    if not terminated or len(entries) != 4 or {int(e['iat'],16):e['name'] for e in entries} != targets:
        raise ValueError('incomplete/ambiguous import binding')
    if any(e['dll'] != 'api-ms-win-crt-heap-l1-1-0.dll' for e in entries):
        raise ValueError('wrong original import DLL')
    C = module('reviewed_capture', 'capture-index-path.py')
    C.RANGES = roots; sys.argv = [sys.argv[0], str(out)]; C.main()
    raw = json.loads(out.read_text())
    S = module('source_annotations', 'validate-title-source-annotations.py')
    raw.update(wrapper_complete=True, pdata_entries=rows,
        unwind_bytes=unwind.hex(), physical_table=dict(address='0x902720', bytes=table.hex(),
            sha256=hashlib.sha256(table).hexdigest(), slots=[hex(x) for x in struct.unpack('<QQQQ',table)]),
        import_boundaries=entries, annotation_prerequisite=S.validate(raw),
        invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        reused_import_reader='capture-title-cleanup-import-boundary-02.py bounded RVA/descriptor/ILT/name algorithm',
        limits='Original bytes/PE metadata/local normal ABI only. No loaded IAT/DLL identity, native heap effect, successful allocation, natural failure/reachability, concurrency or lifetime.')
    out.write_text(json.dumps(raw, indent=2)+'\n')
    print('CAPTURED two complete shipping wrappers and four original import bindings; no execution')

if __name__ == '__main__': main()
