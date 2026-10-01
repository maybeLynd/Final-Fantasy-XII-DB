"""gr1_jcc.py - SWE2-AUDIT-SPEC review of GR-1: the conditional tail calls structflow does not follow (2026-09-30).

gr1_transfers.out lists 8 jcc sites in the S4 walk that leave the function with r8 = slot + 0x18. Enter each target with
that r8 (depth 2, like S4) and with depth 4, and print every access covering slot +0x27 found there, and any unknown-
offset access or escape. Also the S3-side depth-0 call 00809662 (r9 = (E,0)) entered at depth 2 with r9 = (E,0).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)

JCC = [0x002E4C90, 0x0025B500, 0x00244F00, 0x002BED30, 0x001DBCE0, 0x003E6AF0, 0x004278D0]


def main():
    import retool as T
    import structflow as S
    SZ = T.sizes()
    for tgt, reg, tag in [(t, "r8", ("E", 0x18)) for t in JCC] + [(0x0087AF34, "r9", ("E", 0))]:
        for depth in (2, 4):
            if tgt not in SZ:
                print("%08X not in retool SZ" % tgt)
                break
            g = S.Flow([0x27], depth, stride=0x28, slot=0)
            g.enqueue(tgt, {reg: {tag}}, depth)
            while g.q:
                f = g.q.pop()
                dp, ent = g.entry[f]
                g.walk(f, ent, dp)
            print("%08X %s=%s depth %d: walked %d; +0x27 hits %s; unknown %d; escapes %d"
                  % (tgt, reg, tag, depth, len(g.entry),
                     ["%08X %s %s" % (h[1], h[2], h[6]) for h in sorted(g.hits, key=lambda h: h[1])] or "none",
                     len(g.unk), len(g.esc)))


if __name__ == "__main__":
    main()
