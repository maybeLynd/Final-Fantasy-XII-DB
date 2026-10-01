# chse_se_index_check.py (FABLE, Claude Opus 5.5, 2026-09-25) - SB-2.
# Every SE block id the charseinfo_* tables author in slots 0-2, pushed through 002E60F0's index rule
#   index = (id < 500) ? id - 192 : id - 392        (seb-se-block-index.md, 002E60F0)
# into the kind-32 path array (pointer array at 01E7FCF0, 608 entries), and checked against the file it lands on:
# the landing path's basename must be se<id>. Also reports whether any authored id lies in 3-199 or 500-699.
# Inputs: the shipping EXE (.rdata array) and the full extract's in/common/charseinfo_*.bin.
# Control: the eight tables must parse as 16 + count x 16 bytes with the 'CHSE' magic.
import os, glob, struct, collections, sys
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
CHSE = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + 40 * i
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((0x120000 + va, min(vs, rs), ro))
def off(v):
    for a, s, r in secs:
        if a <= v < a + s:
            return r + v - a
    return None
def cstr(v):
    o = off(v)
    return d[o:d.index(b"\0", o)].decode("latin1") if o is not None else None
KIND32 = 0x01E7FCF0
paths = []
for i in range(608):
    p = struct.unpack_from("<Q", d, off(KIND32 + 8 * i))[0]
    paths.append(cstr(p) if p else None)
vals = collections.Counter()
for fn in sorted(glob.glob(os.path.join(CHSE, "charseinfo_*.bin"))):
    b = open(fn, "rb").read()
    count = struct.unpack_from("<I", b, 8)[0]
    if b[:4] != b"CHSE" or len(b) != 16 + 16 * count:
        sys.exit("REFUSE: %s is not a 16 + count x 16 CHSE table" % fn)
    for k in range(count):
        for s in range(3):
            v = struct.unpack_from("<H", b, 16 + 16 * k + 2 * s)[0]
            if v != 0xFFFF:
                vals[v] += 1
bad, low, mid = [], [], []
for v in sorted(vals):
    idx = v - 192 if v < 500 else v - 392
    landing = paths[idx] if 0 <= idx < len(paths) else None
    base = landing.rsplit("\\", 1)[-1].split(".")[0] if landing else None
    if base != "se%03d" % v:
        bad.append((v, idx, base))
    if 3 <= v <= 199:
        low.append(v)
    if 500 <= v <= 699:
        mid.append(v)
print("authored values:", sum(vals.values()), "distinct:", len(vals), "range %d..%d" % (min(vals), max(vals)))
print("in 3..199:", low)
print("in 500..699:", mid)
print("landing mismatches (value, index, landed on):", bad)
