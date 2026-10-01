"""ov58d_residue.py - the indexed residue of ov58d_flow.tsv, grouped by what can be read off each store (OPUS, 2026-09-30).

For every store the census could not place at a known state offset:
  INDEXED-BELOW    base + a non-negative index, with the base's own state offset `lo` below region A's end: grouped by
                   `lo` against the state layout (the 40 BattleStatsRecords at +0x008..+0x4748, region A at
                   +0x4748..+0x4F10, the other class arrays to +0x4F84, the backup and later fields above);
  INDEXED-UNKNOWN  a state-derived base whose offset is unknown (a widened join, or pointer arithmetic from an unknown
                   offset);
  REGISTRY-STORAGE a class-storage pointer read from an unknown registry row;
  RECORD-INDEXED   a battle-stats record (00320AB0's return, or a 022C1740 entry) plus an index;
  RECORD-OUTSIDE   a battle-stats record plus a displacement outside its 0x1C8 bytes.
Stores classed RECORD (inside one record, so below +0x4728) are not residue.
Prints, per group, the functions and store counts, so each group can be bounded by reading its index.
"""
import collections, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [l.rstrip("\n").split("\t") for l in io.open(os.path.join(HERE, "ov58d_flow.tsv"), encoding="utf-8")][1:]
LO_RE = re.compile(r"lo=(-?0x[0-9a-f]+)")


def zone(lo):
    if lo < 0x8:
        return "below the stats records (< +0x8)"
    if lo < 0x4748:
        return "in the stats-record array (+0x8..+0x4747)"
    if lo < 0x4F10:
        return "inside region A"
    return "above region A"


groups = collections.defaultdict(lambda: collections.defaultdict(set))
for cls, fn, addr, text, size, base in rows:
    if cls == "INDEXED-BELOW":
        m = LO_RE.search(base)
        g = zone(int(m.group(1), 16)) if m else "INDEXED-BELOW without lo"
    elif cls in ("INDEXED-UNKNOWN", "REGISTRY-STORAGE", "RECORD-INDEXED", "RECORD-OUTSIDE"):
        g = cls
    else:
        continue
    groups[g][fn].add(addr)
for g, fns in sorted(groups.items()):
    print("%-45s %4d functions %5d stores" % (g, len(fns), sum(len(v) for v in fns.values())))
    for fn, addrs in sorted(fns.items(), key=lambda kv: -len(kv[1]))[:12]:
        print("    %s  %d  e.g. %s" % (fn, len(addrs), " ".join(sorted(addrs)[:3])))
