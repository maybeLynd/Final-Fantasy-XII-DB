"""bc4_hierarchy.py - control for BC-4 (FABLE, Claude Opus 5.5, 2026-09-26): the DynGeo instances' 21-slot base.

  H1 the RTTI class hierarchy descriptors: DynGeo3DInstance (vtable 009043D8) and DynGeoTextureInstance (00904328) list
     DynGeoUIInstance as a base; DynGeoUIInstance (00906FB0) lists only GeometryInstance.
  H2 of the 21 slots, 16 (0, 3, 4, 7-18, 20) are the same function in all three vtables: DynGeoUIInstance's methods,
     inherited unchanged. DynGeo3DInstance overrides 2, 5 and 6; DynGeoTextureInstance overrides 1, 2, 5, 6 and 19.
Planted negative: H2 asserts slot 2 differs in all three (a matcher that called everything shared would fail).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
def name(td): return d[off(td) + 16:off(td) + 120].split(b"\0")[0].decode("latin1")
def hierarchy(vt):
    col = q(vt - 8)
    me = name(BASE + u32(col + 12))
    chd = BASE + u32(col + 16)
    nb = u32(chd + 8); arr = BASE + u32(chd + 12)
    bases = [name(BASE + u32(BASE + u32(arr + 4 * i))) for i in range(nb)]
    return me, bases[1:]            # entry 0 is the class itself
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
UI, D3, TX = 0x906FB0, 0x9043D8, 0x904328
hu, h3, ht = hierarchy(UI), hierarchy(D3), hierarchy(TX)
check("H1 names", (hu[0], h3[0], ht[0]) == (".?AVDynGeoUIInstance@@", ".?AVDynGeo3DInstance@@", ".?AVDynGeoTextureInstance@@"))
check("H1 3D and Texture derive from DynGeoUIInstance; UI from GeometryInstance only",
      ".?AVDynGeoUIInstance@@" in h3[1] and ".?AVDynGeoUIInstance@@" in ht[1] and hu[1] == [".?AVGeometryInstance@@"],
      "%s | %s | %s" % (hu[1], h3[1], ht[1]))
same = [s for s in range(21) if q(UI + 8 * s) == q(D3 + 8 * s) == q(TX + 8 * s)]
o3 = [s for s in range(21) if q(D3 + 8 * s) != q(UI + 8 * s)]
ot = [s for s in range(21) if q(TX + 8 * s) != q(UI + 8 * s)]
check("H2 16 shared slots", same == [0, 3, 4] + list(range(7, 19)) + [20], str(same))
check("H2 3D overrides 2, 5, 6; Texture overrides 1, 2, 5, 6, 19", o3 == [2, 5, 6] and ot == [1, 2, 5, 6, 19], "%s %s" % (o3, ot))
check("H2 planted negative: slot 2 differs in all three", len({q(UI + 16), q(D3 + 16), q(TX + 16)}) == 3)
print("FAILS", fails)
sys.exit(1 if fails else 0)
