"""Named original cleanup count loop and selector; Method A only.

No process execution or initialization/ownership inference. The selector's two
normal returns, not its first RET alone, delimit the bounded leaf input.
"""
import hashlib
import importlib.util
import json
import pathlib
import struct
import sys

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
out = W / "title-cleanup-count-selector-source-01.json"
if out.exists():
    raise ValueError("immutable source exists")
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
if hashlib.sha256(d).hexdigest() != SHA:
    raise ValueError("wrong shipping image")
p = struct.unpack_from("<I", d, 60)[0]
ns = struct.unpack_from("<H", d, p+6)[0]
opt = struct.unpack_from("<H", d, p+20)[0]
sections = [struct.unpack_from("<IIII", d, p+24+opt+40*k+8) for k in range(ns)]


def read(a, n):
    for vs, va, rs, ro in sections:
        if 0x120000+va <= a and a+n <= 0x120000+va+rs:
            return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError("original address not file-backed")


rva, size = struct.unpack_from("<II", d, p+24+112+3*8)
if size % 12:
    raise ValueError("incomplete exception directory")
pd = [tuple(x+0x120000 for x in struct.unpack("<III", read(0x120000+rva+12*k, 12)))
      for k in range(size//12)]
entry = (0x62B100, 0x62B170, 0x1D6B7C8)
if entry not in pd or any(a <= 0x623DF0 < b for a, b, u in pd):
    raise ValueError("named span/leaf metadata changed")
if read(0x623E28, 8) != bytes([0xCC])*8:
    raise ValueError("selector trailing padding identity changed")
spec = importlib.util.spec_from_file_location("reviewed_capture", W / "capture-index-path.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [(0x62B100, 0x62B170), (0x623DF0, 0x623E28)]
sys.argv = [sys.argv[0], str(out)]
C.main()
result = json.loads(out.read_text())
spec = importlib.util.spec_from_file_location("actual_annotations", W / "validate-title-source-annotations.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
qualification = S.validate(result)
result.update(
    wrapper_complete=True, pdata_entry=list(entry), exception_directory=dict(rva=hex(rva), bytes=size),
    selector_leaf=dict(start="0x623df0", end_exclusive="0x623e28", metadata_entry=False,
                       trailing_bytes="cc"*8, normal_extent_requires_cfg=True),
    annotation_prerequisite=qualification,
    invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits="Physical source/annotation consistency; normal control/dataflow needs reduction. No initialized count/storage, native service effects, field purpose, lifetime or natural reachability proof",
)
out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf8")
print("Original count loop and two-return selector captured; normal reduction/state proof still required")
