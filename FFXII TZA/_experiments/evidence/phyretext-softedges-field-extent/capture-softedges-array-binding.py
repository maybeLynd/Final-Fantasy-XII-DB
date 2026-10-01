"""Method A: bounded original array-fixup patcher, not a runtime observation.

Reuse the existing reviewed capture invocation, including store/LEA/RMW controls.
The exact pdata entry proves only this contiguous span's extent. No census.
"""
import hashlib, importlib.util, json, pathlib, struct, sys

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
OUT = W / 'softedges-resource-source-01' / 'array-binding-code-01.json'
if OUT.exists(): raise ValueError('immutable output already exists')
image = ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe'
data = image.read_bytes()
pin = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(data).hexdigest() != pin: raise ValueError('wrong image')
pe = struct.unpack_from('<I', data, 0x3c)[0]
count = struct.unpack_from('<H', data, pe+6)[0]
opt = struct.unpack_from('<H', data, pe+20)[0]
entries = []
for i in range(count):
    p = pe+24+opt+40*i
    if data[p:p+8].rstrip(b'\0') == b'.pdata':
        size, offset = struct.unpack_from('<II', data, p+16)
        for q in range(offset, offset+size-11, 12):
            a,b,u = struct.unpack_from('<III', data, q)
            if a+0x120000 == 0x59c250:
                entries.append((a+0x120000,b+0x120000,u+0x120000))
if len(entries) != 1 or entries[0][:2] != (0x59c250,0x59c6f8):
    raise ValueError('exact array-fixup patcher pdata identity failed')
spec = importlib.util.spec_from_file_location('reviewed_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
C.RANGES = [(0x59c250,0x59c6f8)]
sys.argv = [sys.argv[0],str(OUT)]
C.main()
raw = json.loads(OUT.read_text())
raw.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           pdata_entries=[list(e) for e in entries],
           limits='One original array-fixup patcher; file layout/name binding only. No live initialization, alias or natural caller execution.')
OUT.write_text(json.dumps(raw,indent=2)+'\n')
print('CAPTURED exact array-fixup source and actual shared-adapter controls')
