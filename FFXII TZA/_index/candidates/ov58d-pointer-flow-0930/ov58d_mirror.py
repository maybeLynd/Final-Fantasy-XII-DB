"""ov58d_mirror.py - who writes the image head's copy of region A (OPUS, 2026-09-30). Reads ov58d_flow.tsv.

002EF4A0 copies 0x6000 bytes from the mirror 02166480 into the state 021B290C on every post-load (00233C10 -> 00235AF0),
so region A is also written from mirror + 0x4748 .. + 0x4F0F. This lists every census store whose state-relative
address can land in that window (state-relative [-0x47D44, -0x4757C)), and every store into the controller-backed image
head [02164280, 02164280 + 0xE240) that 00583CB0 backs up and 00583C00 restores.
"""
import collections, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = 0x021B290C
MIRROR_A = (0x02166480 + 0x4748 - STATE, 0x02166480 + 0x4F10 - STATE)
HEAD = (0x02164280 - STATE, 0x02164280 + 0xE240 - STATE)
OFF = re.compile(r"\bA([+-]0x[0-9a-f]+)\b")
LO = re.compile(r"lo=(-?0x[0-9a-f]+)")
rows = [l.rstrip("\n").split("\t") for l in io.open(os.path.join(HERE, "ov58d_flow.tsv"), encoding="utf-8")][1:]
hit_m, hit_h, ind = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
for cls, fn, addr, text, size, base in rows:
    size = int(size)
    for m in OFF.finditer(base):
        o = int(m.group(1), 16)
        if o < MIRROR_A[1] and o + size > MIRROR_A[0]:
            hit_m[fn].add((addr, text))
        if o < HEAD[1] and o + size > HEAD[0]:
            hit_h[fn].add((addr, text))
    m = LO.search(base)
    if m and cls.startswith("INDEXED") and int(m.group(1), 16) < MIRROR_A[1] and int(m.group(1), 16) >= HEAD[0]:
        ind[fn].add((addr, text))
print("known-offset stores into the mirror's copy of region A: %d functions" % len(hit_m))
for f, s in sorted(hit_m.items()):
    print("  %s  %s" % (f, "; ".join("%s %s" % x for x in sorted(s)[:3])))
print("known-offset stores anywhere in the backed-up image head: %d functions" % len(hit_h))
for f, s in sorted(hit_h.items()):
    print("  %s  %d stores  e.g. %s" % (f, len(s), "; ".join("%s %s" % x for x in sorted(s)[:2])))
print("indexed stores whose lower bound lies in the image head: %d functions" % len(ind))
for f, s in sorted(ind.items()):
    print("  %s  %d stores" % (f, len(s)))
