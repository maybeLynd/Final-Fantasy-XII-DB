"""rtti_bcd.py VTABLE: the class hierarchy descriptor behind a vtable, with each base class descriptor's
numContainedBases, mdisp/pdisp/vdisp and attributes - the nesting of the base list, not just its members."""
import struct, sys

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))


def v2o(v):
    for n, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


def td(rva):
    o = v2o(BASE + rva + 16)
    return d[o:o + 200].split(b"\0")[0].decode(errors="replace")


vt = int(sys.argv[1], 16)
col = struct.unpack_from("<Q", d, v2o(vt - 8))[0]
sig, off, cdo, td_rva, chd_rva, self_rva = struct.unpack_from("<IIIIII", d, v2o(col))
print("COL %08X sig %d offset %d class %s" % (col, sig, off, td(td_rva)))
chd = BASE + chd_rva
csig, attr, nbase, arr_rva = struct.unpack_from("<IIII", d, v2o(chd))
print("CHD %08X attributes 0x%X numBaseClasses %d" % (chd, attr, nbase))
for i in range(nbase):
    bcd_rva = struct.unpack_from("<I", d, v2o(BASE + arr_rva + 4 * i))[0]
    b_td, ncont, mdisp, pdisp, vdisp, battr = struct.unpack_from("<IIiiiI", d, v2o(BASE + bcd_rva))
    print("  [%d] %-45s contains %d  mdisp %d pdisp %d vdisp %d attr 0x%X" % (i, td(b_td), ncont, mdisp, pdisp, vdisp, battr))
