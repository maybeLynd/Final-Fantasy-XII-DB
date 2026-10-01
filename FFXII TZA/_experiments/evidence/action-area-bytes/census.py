"""The area bytes of the action row, tallied the way Battle_BuildActionTargetSet (0030D160) reads them.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), us battle_pack.bin,
action table at directory +0x3C. Names, where shown, come from the database's own
08-Combat-Formula/Recipe-System/recipe-users.tsv (set FF12_DB to the 'FFXII TZA' folder; optional).
What the code reads (0030D160, read whole 2026-09-19):
  +0x06 u8   area radius; 0 = single target                                  (0030D255, squared at 0030D2BD)
  +0x07 u8   cone half-angle in degrees (flag bit 24) / line half-width (flag bit 25)   (0030D2EC)
  +0x0C bit 21   the area is centred on the ACTOR, not on the primary target (0030D271)
  +0x0C bit 24   cone from the actor toward the primary target               (0030D3B1)
  +0x0C bit 25   line from the actor toward the primary target               (0030D3E3)
  +0x0C bit 1    add every standing party member                             (0030D461)
  +0x36 bit 3    no side filter; else bit 2: 0 = only units FRIENDLY to the primary target, 1 = only units HOSTILE to it
Predictions the reading makes, each of which the data could refute:
  P1  +0x07 is non-zero only on rows with bit 24 or bit 25, and those rows have a radius
  P2  bits 24 and 25 are never both set
  P3  rows with radius 0 do not carry bits 21, 24, 25 (they would never be read)
  P4  the -ga / -ja spells have a radius and their single-target forms do not
Control: 543 rows of 60 bytes (published).
FABLE, 2026-09-19.
"""
import os, re, struct, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
DB = os.environ.get("FF12_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
d = open(os.path.join(ROOT, "ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"), "rb").read()
o = struct.unpack_from("<I", d, 0x3C)[0]
n, stride, first = struct.unpack_from("<III", d, o + 4)
A = [d[o + first + i * stride: o + first + (i + 1) * stride] for i in range(n)]
print("control: action rows %d x %d (published 543 x 60)" % (n, stride))
names = {}
try:
    for line in open(os.path.join(DB, "08-Combat-Formula/Recipe-System/recipe-users.tsv"), encoding="utf-8").read().split("\n")[1:]:
        p = line.split("\t")
        if len(p) >= 4:
            ids = [int(x, 16) for x in p[2].split()]
            nm = [x.strip() for x in p[3].split(";")]
            if len(ids) == len(nm):
                names.update(zip(ids, nm))
except OSError:
    pass
print("names loaded:", len(names))
nm = lambda i: names.get(i, "#%d" % i)
fl = lambda r: struct.unpack_from("<I", r, 0xC)[0]
w36 = lambda r: struct.unpack_from("<H", r, 0x36)[0]
area = [i for i, r in enumerate(A) if r[6]]
print("rows with a radius (+0x06 != 0):", len(area), "; radius values:", sorted(collections.Counter(A[i][6] for i in area).items()))
for name, mask in (("bit 21 centre on actor", 1 << 21), ("bit 24 cone", 1 << 24), ("bit 25 line", 1 << 25), ("bit 1 whole party", 2)):
    rows = [i for i, r in enumerate(A) if fl(r) & mask]
    print("%-24s %3d rows; with a radius %3d; (+0x06, +0x07) -> rows: %s" % (name, len(rows), sum(1 for i in rows if A[i][6]),
          sorted(collections.Counter((A[i][6], A[i][7]) for i in rows).items())))
    print("      e.g.", ", ".join(nm(i) for i in rows[:14]))
p1 = [i for i, r in enumerate(A) if r[7] and not (fl(r) & (3 << 24))]
print("P1  rows with +0x07 != 0 but neither bit 24 nor 25:", len(p1), [(i, nm(i), A[i][6], A[i][7]) for i in p1[:12]])
print("    rows with bit 24/25 and no radius:", [i for i, r in enumerate(A) if fl(r) & (3 << 24) and not r[6]])
print("P2  rows with both bit 24 and bit 25:", [i for i, r in enumerate(A) if fl(r) & (3 << 24) == (3 << 24)])
print("P3  radius-0 rows carrying bit 21 / 24 / 25:", [(i, nm(i)) for i, r in enumerate(A) if not r[6] and fl(r) & ((1 << 21) | (3 << 24))][:20])
side = collections.Counter(("none(bit3)" if w36(A[i]) & 8 else ("hostile-to-primary(bit2)" if w36(A[i]) & 4 else "friendly-to-primary")) for i in area)
print("side filter of the rows with a radius:", sorted(side.items()))
for key in ("none(bit3)", "hostile-to-primary(bit2)"):
    rows = [i for i in area if ("none(bit3)" if w36(A[i]) & 8 else ("hostile-to-primary(bit2)" if w36(A[i]) & 4 else "friendly-to-primary")) == key]
    print("   ", key, ":", ", ".join(nm(i) for i in rows[:20]))
print("P4  named rows, radius by name:")
for pat in ("Cur", "Fir", "Blizza", "Thund", "Aero", "Protect", "Shell", "Haste", "Dispel", "Esuna", "Raise", "Scathe", "Flare", "Scourge", "Holy"):
    print("    %-8s %s" % (pat, ", ".join("%s=%d" % (names[i], A[i][6]) for i in sorted(names) if names[i].startswith(pat) and i < n)))
b12 = [i for i in area if fl(A[i]) & (1 << 12)]
print("rows with a radius AND +0x0C bit 12 (the shape descriptor 0031A990 reports these as having no area):", len(b12), "; radius values:",
      sorted(collections.Counter(A[i][6] for i in b12).items()), "; e.g.", ", ".join(nm(i) for i in b12[:16]))
shape = collections.Counter()
for i, r in enumerate(A):
    f = fl(r)
    if not r[6] or f & (1 << 12):
        s = 5 if f & 2 else 0
    elif f & (1 << 24):
        s = 3
    elif f & (1 << 25):
        s = 4
    else:
        s = 2 if f & (1 << 21) else 1
    shape[s] += 1
print("shape codes as 0031A990 would report them (0 single, 1 circle on target, 2 circle on actor, 3 cone, 4 line, 5 party):", sorted(shape.items()))
