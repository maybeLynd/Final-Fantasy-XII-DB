"""Reuse reviewed capture path, complete original bodies and exact import identity."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
W = P.parent
out = P / 'source-01.json'
if out.exists(): raise RuntimeError('immutable source exists')
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
C = load('sd194_reviewed_capture', W / 'capture-index-path.py')
C.RANGES = [(0x377dc0, 0x37802a), (0x2df880, 0x2df8d9), (0x861eba, 0x861ec0)]
sys.argv = [sys.argv[0], str(out)]
C.main()
v = json.loads(out.read_text())
data = C.EXE.read_bytes()
if hashlib.sha256(data).hexdigest() != C.SHA: raise RuntimeError('reference identity moved')
pe = struct.unpack_from('<I', data, 60)[0]
opt = pe + 24
optional_size = struct.unpack_from('<H', data, pe + 20)[0]
secs = [struct.unpack_from('<IIII', data, pe + 24 + optional_size + 40*k + 8) for k in range(struct.unpack_from('<H', data, pe + 6)[0])]
def read(rva, n):
    for virtual_size, va, size, offset in secs:
        if va <= rva and rva+n <= va+size: return data[offset+rva-va:offset+rva-va+n]
    raise RuntimeError('unbacked original import')
def cstr(rva):
    b = bytearray()
    for k in range(512):
        x = read(rva+k, 1)
        if x == b'\0': return b.decode('ascii')
        b.extend(x)
    raise RuntimeError('import string bound')
idir, size = struct.unpack_from('<II', data, opt + 112 + 8)
found = []
for k in range(size//20):
    oft, ts, fwd, name, iat = struct.unpack('<IIIII', read(idir+20*k, 20))
    if not any([oft, ts, fwd, name, iat]): break
    for n in range(65536):
        q = struct.unpack('<Q', read((oft or iat)+8*n, 8))[0]
        if not q: break
        if C.BASE+iat+8*n == 0x8c2a68:
            if q>>63: raise RuntimeError('unexpected ordinal import')
            found.append({'iat_va': '0x8c2a68', 'dll': cstr(name), 'name': cstr(q+2), 'lookup_raw': q.to_bytes(8, 'little').hex()})
    else: raise RuntimeError('unterminated IAT table')
if len(found) != 1: raise RuntimeError('copy import missing/ambiguous')
v.update(wrapper_complete=True, wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         annotation_prerequisite=load('sd194_roles', W / 'validate-title-source-annotations.py').validate(v),
         static_copy_import=found[0], limits='STATIC_ONLY complete local bytes/declared import; no initialized stack/name, natural field entry or loaded copy effects')
out.write_text(json.dumps(v, indent=2) + '\n')
print(json.dumps({'ranges': [{'start': x['start'], 'end': x['end_exclusive'], 'sha256': x['sha256']} for x in v['ranges']], 'declared_copy': found[0]}))
