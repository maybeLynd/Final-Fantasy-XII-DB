"""gr1_pairs.py - SWE2-AUDIT-SPEC review of GR-1's S4 pairing (2026-09-30).

The package's structflow.py is the instrument UNDER TEST (read-only import, kit copy); tables are decoded by this
folder's img.py (independent). For every handler of the five command tables, entered with r8 = slot + 0x18 at depth 2
(the package's S4 setting), dump each access covering slot +0x27 (function, address, r/w, offset, width, text). Then,
for every READ, show which command(s) it belongs to, the role (begin / poll / result), and the candidate covering writes
the package's rule credits: any write in the begin handler (anywhere), or a write in the same handler's hit list at a
lower address. The strict re-check is done in gr1_strict.py on this output.
"""
import os, sys, struct, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)
import img as I  # noqa: E402


def main():
    import retool as T
    import structflow as S
    SZ = T.sizes()
    TBL = {"0": 0x01EED700, "3": 0x01F281B0, "5": 0x01F29418, "7": 0x01F29440, "def": 0x01F26720}
    cmds = []
    for fam, tbl in TBL.items():
        n = struct.unpack("<i", I.rd(tbl, 4))[0]
        for N in range(n):
            b, p, r = (I.q(tbl + 32 * N + o) for o in (8, 0x10, 0x20))
            cmds.append((fam, N, b or None, p or None, r or None))
    H = sorted({h for cm in cmds for h in cm[2:] if h})
    notsz = [h for h in H if h not in SZ]
    print("commands %d; unique handlers %d; handlers retool has no size for: %d %s" % (len(cmds), len(H), len(notsz),
                                                                                       ["%08X" % h for h in notsz][:8]))
    per = {}
    for h in H:
        if h not in SZ:
            continue
        g = S.Flow([0x27], 2, stride=0x28, slot=0)
        g.enqueue(h, {"r8": {("E", 0x18)}}, 2)
        while g.q:
            f = g.q.pop()
            dp, ent = g.entry[f]
            g.walk(f, ent, dp)
        per[h] = sorted(g.hits, key=lambda x: x[1])
    touch = [h for h in per if per[h]]
    print("handlers touching the window: %d" % len(touch))
    role = collections.defaultdict(list)
    for fam, N, b, p, r in cmds:
        for nm, h in (("begin", b), ("poll", p), ("result", r)):
            if h:
                role[h].append((fam, N, nm, b))
    out = {}
    for h in sorted(touch):
        print("handler %08X roles %s" % (h, sorted({(x[2]) for x in role[h]})))
        for x in per[h]:
            print("   %s %08X %08X %s %-5s off=%02X w=%d %s" % (("R" if x[2] == "r" else "W"), x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
        out["%08X" % h] = {"roles": [[a, b_, c, ("%08X" % d) if d else None] for a, b_, c, d in role[h]],
                           "hits": [["%08X" % x[0], "%08X" % x[1], x[2], x[3], x[4], x[5], x[6]] for x in per[h]]}
    json.dump(out, open(os.path.join(HERE, "gr1_pairs.json"), "w"), indent=0)
    # reads by command, with the package's credited cover
    print("== reads and the package's credited cover")
    for fam, N, b, p, r in cmds:
        for nm, h in (("begin", b), ("poll", p), ("result", r)):
            if not h or h not in per:
                continue
            for x in per[h]:
                if x[2] != "r":
                    continue
                bw = [y for y in per.get(b, []) if y[2] == "w"] if b else []
                sw = [y for y in per[h] if y[2] == "w" and y[1] < x[1]]
                print("   %s/%d %-6s read %08X in %08X (%s off=%02X w=%d) | begin %s writes %s | same-handler earlier %s"
                      % (fam, N, nm, x[1], x[0], x[6], x[4], x[5], ("%08X" % b) if b else "-",
                         ["%08X" % y[1] for y in bw], ["%08X@%08X" % (y[1], y[0]) for y in sw]))


if __name__ == "__main__":
    main()
