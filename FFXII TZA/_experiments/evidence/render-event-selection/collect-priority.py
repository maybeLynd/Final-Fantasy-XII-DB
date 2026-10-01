"""Offline capability-policy consumers; reuse exact-body PE and disassembly collector."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import capstone

raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
opt = pe + 24
ib = struct.unpack_from('<Q', raw, opt + 24)[0]
assert ib == 0x120000
st = opt + struct.unpack_from('<H', raw, pe + 20)[0]
sections = []
for i in range(struct.unpack_from('<H', raw, pe + 6)[0]):
    o = st + 40*i
    vs, va, rs, pr = struct.unpack_from('<IIII', raw, o+8)
    sections.append(dict(name=raw[o:o+8].rstrip(b'\0').decode(), va=ib+va, virtual_bytes=vs, raw_bytes=rs, disk_offset=pr))
def off(rva):
    for s in sections:
        d = ib+rva-s['va']
        if 0 <= d < s['raw_bytes']:
            return s['disk_offset'] + d
    raise ValueError(hex(rva))
def zstr(rva):
    start = off(rva)
    end = raw.index(b'\0', start)
    return raw[start:end].decode()
slots = {}
imp_rva, imp_bytes = struct.unpack_from('<II', raw, opt+112+8)
o = off(imp_rva)
while True:
    oft, _, _, name, ft = struct.unpack_from('<IIIII', raw, o)
    if not name: break
    dll = zstr(name)
    t = off(oft or ft)
    k = 0
    while True:
        v = struct.unpack_from('<Q', raw, t+8*k)[0]
        if not v: break
        sym = 'ordinal'+str(v&65535) if v>>63 else zstr(v+2)
        slots[ib+ft+8*k] = dll+'!'+sym
        k += 1
    o += 20
f = {}
for line in Path('Database/Tools/work/graph/functions.tsv').read_text(encoding='utf-8').splitlines()[1:]:
    p=line.split('\t')
    f[int(p[0],16)] = (p[1], int(p[2]))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
out = dict(exe_sha256=sha, image_base=hex(ib), dll_characteristics=hex(struct.unpack_from('<H', raw, opt+70)[0]), sections=sections, import_count=len(slots), dll_count=len(set(v.split('!')[0] for v in slots.values())), delay_import_directory=struct.unpack_from('<II', raw, opt+112+13*8), selected_imports={hex(k):slots[k] for k in (0x8C2F70,0x8C2B40)}, capstone_version=capstone.__version__, bodies=[])
out['upstream_sources'] = {p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('Database/Tools/work/graph/functions.tsv',)}
out['direct_VirtualAlloc_imports'] = [v for v in slots.values() if v.split('!')[-1].startswith('VirtualAlloc')]

a=0x1F00410
b=raw[off(a-ib):off(a-ib)+64]
x=dict(exe_sha256=sha,address=hex(a),bytes=64,sha256=hashlib.sha256(b).hexdigest(),hex=b.hex(),values=list(b),limit="Observed 64-byte window for known low event indices; not a declared table extent or proof all 12-bit indices are valid.")
Path('Database/Tools/work/ASTRA/render-event-priority.json').write_text(json.dumps(x,indent=2)+'\n')
print(json.dumps(x,indent=2))
