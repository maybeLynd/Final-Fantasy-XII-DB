"""One original removal root; reuse the existing reviewed capture instrument."""
import hashlib, importlib.util, json, pathlib, struct, sys

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
out = W/'texture-async-removal-source-01.json'
if out.exists():
    raise ValueError('immutable source exists')
d = (ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
expected = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest() != expected:
    raise ValueError('wrong original image')
pe = struct.unpack_from('<I', d, 60)[0]
ns, opt = struct.unpack_from('<H', d, pe+6)[0], struct.unpack_from('<H', d, pe+20)[0]
sections = [struct.unpack_from('<IIII', d, pe+24+opt+40*k+8) for k in range(ns)]


def read(address, size):
    for vs, va, rs, ro in sections:
        if 0x120000+va <= address and address+size <= 0x120000+va+rs:
            return d[ro+address-0x120000-va:ro+address-0x120000-va+size]
    raise ValueError('whole range lacks raw backing')


rva, size = struct.unpack_from('<II', d, pe+24+112+3*8)
if not size or size % 12:
    raise ValueError('missing/incomplete exception directory')
pd = [tuple(v+0x120000 for v in struct.unpack('<III', read(0x120000+rva+12*k,12))) for k in range(size//12)]
roots = [entry for entry in pd if entry[0] == 0x62ec70]
if len(roots) != 1:
    raise ValueError('required normal removal root absent/ambiguous')
call = read(0x62bd75,5)
if call[0] != 0xe8 or 0x62bd7a+struct.unpack('<i',call[1:])[0] != 0x62ec70:
    raise ValueError('known original release/removal call changed')
for a,z,u in roots:
    read(a,z-a)
spec = importlib.util.spec_from_file_location('removal_shared_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [(a,z) for a,z,u in roots]
sys.argv = [sys.argv[0], str(out)]
C.main()
raw = json.loads(out.read_text())
spec = importlib.util.spec_from_file_location('removal_actual_roles', W/'validate-title-source-annotations.py')
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
raw.update(wrapper_complete=True, pdata_entries=[list(entry) for entry in roots],
           annotation_prerequisite=S.validate(raw),
           known_caller=dict(pc='0x62bd75',bytes=call.hex(),target='0x62ec70'),
           invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Physical original root and caller identity only; helper effects, normal CFG/dataflow, semantic acceptance and natural scheduler/lifetime remain unproved')
out.write_text(json.dumps(raw,indent=2)+'\n')
print('Retained original removal root', [(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']])
