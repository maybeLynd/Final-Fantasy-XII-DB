"""Original BC predicate and cleanup bodies; Method A, no process execution.

Use the PE Exception DataDirectory, not section padding, for chain identities.
Capture complete linked normal fragments; opaque callee effects remain separate.
"""
import hashlib, importlib.util, json, pathlib, struct, sys

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
out = W / "title-cleanup-callees-source-01.json"
if out.exists():
    raise ValueError("immutable source already exists")
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    raise ValueError("wrong shipping image")
p = struct.unpack_from("<I", d, 60)[0]
ns = struct.unpack_from("<H", d, p + 6)[0]
opt = struct.unpack_from("<H", d, p + 20)[0]
sections = [struct.unpack_from("<IIII", d, p + 24 + opt + 40*k + 8) for k in range(ns)]


def read(a, n):
    for vs, va, rs, ro in sections:
        if 0x120000 + va <= a and a + n <= 0x120000 + va + rs:
            return d[ro + a - 0x120000 - va:ro + a - 0x120000 - va + n]
    raise ValueError("original address not file-backed")


rva, size = struct.unpack_from("<II", d, p + 24 + 112 + 3*8)
if size % 12:
    raise ValueError("incomplete Exception DataDirectory")
pd = [tuple(x + 0x120000 for x in struct.unpack("<III", read(0x120000+rva+12*k, 12))) for k in range(size//12)]
fragments = [
    (0x62BCB0, 0x62BCF1, 0x1DA8B68),
    (0x62BCF1, 0x62BD04, 0x1DA8510),
    (0x62BD04, 0x62BF24, 0x1DA8524),
    (0x62BF24, 0x62BF2B, 0x1DA853C),
    (0x62BF2B, 0x62BF37, 0x1DA854C),
]
common = (0x616C60, 0x616CBD, 0x1DA8590)
if not set(fragments + [common]) <= set(pd):
    raise ValueError("named original pdata identity changed")
chains = []
for entry in fragments[1:]:
    current, seen, steps = entry, set(), []
    while current != fragments[0]:
        if current in seen or current not in pd:
            raise ValueError("missing/cyclic original unwind chain")
        seen.add(current)
        h = read(current[2], 4)
        if not h[0] >> 3 & 4:
            raise ValueError("normal fragment missing chain")
        n = 4 + 2*((h[2] + 1) & ~1)
        raw = read(current[2], n+12)
        parent = tuple(x + 0x120000 for x in struct.unpack_from("<III", raw, n))
        steps.append(dict(entry=list(current), raw_unwind=raw.hex(), parent=list(parent)))
        current = parent
    chains.append(dict(fragment=list(entry), root=list(current), steps=steps))
if read(0x625F00, 11) != bytes.fromhex("83b9bc000000000f95c0c3"):
    raise ValueError("predicate leaf identity changed")
spec = importlib.util.spec_from_file_location("reviewed_capture", W / "capture-index-path.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [(0x625F00, 0x625F0B)] + [x[:2] for x in fragments] + [common[:2]]
sys.argv = [sys.argv[0], str(out)]
C.main()
r = json.loads(out.read_text())
r.update(
    wrapper_complete=True, pdata_entries=[list(x) for x in fragments + [common]],
    exception_directory=dict(rva=hex(rva), bytes=size),
    verified_unwind_chains=chains,
    invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits="Original physical predicate, linked cleanup fragments and common tail. Normal CFG/field effects require reduction; initialization, native delegate effects, ownership and lifetime remain separate.",
)
out.write_text(json.dumps(r, indent=2) + "\n")
print("Original predicate/linked cleanup/common-tail source available; semantic reduction required")
