# tally.py - per-offset value tallies for one st2e table of the us battle_pack.bin.
# usage: tally.py NAME [--w 1|2|4] [--rows]   (default prints u8 and aligned u16 / u32 tallies)
import sys, collections, struct
sys.path.insert(0, __import__("os").path.dirname(__file__))
from pack import TABLES, records

def tallies(name, width):
    doff = [t for t in TABLES if t[0] == name][0][2]
    recs, h = records(doff)
    res = []
    for o in range(0, h["size"] - width + 1, width if width > 1 else 1):
        c = collections.Counter(int.from_bytes(r[o:o + width], "little") for r in recs)
        res.append((o, c))
    return recs, h, res

def top(c, n=5, hexa=False):
    f = (lambda v: "%#x" % v) if hexa else str
    return ", ".join("%s x%d" % (f(v), k) for v, k in c.most_common(n))

if __name__ == "__main__":
    name = sys.argv[1]
    ws = [int(sys.argv[sys.argv.index("--w") + 1])] if "--w" in sys.argv else [1, 2, 4]
    for w in ws:
        recs, h, res = tallies(name, w)
        print("== %s count=%d size=%d width=%d" % (name, h["count"], h["size"], w))
        for o, c in res:
            print("+%#04x u%d distinct=%d min=%#x max=%#x | %s" % (o, 8 * w, len(c), min(c), max(c), top(c, 6, hexa=(w > 1))))
    if "--rows" in sys.argv:
        recs, h = records([t for t in TABLES if t[0] == name][0][2])
        for i, r in enumerate(recs): print("%4d %s" % (i, r.hex(" ")))
