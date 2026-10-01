"""gr1_phase.py - SWE2-AUDIT-SPEC review of GR-1: who writes the command phase byte slot +0x15 (2026-09-30).

"Begin runs before poll / result" rests on 002621D0 dispatching on slot +0x15 (0 -> begin then poll, 1 -> poll, >= 2 ->
result). That holds only if +0x15 is 0 whenever a new command starts. This runs the package's structflow (instrument
under test, read-only) with fields [0x15]:
  P1  from the seven wait-slot functions, seeded at the +0xA8 load (the package's S3 setting), depth 3 and depth 5;
  P2  from every handler of the five command tables entered with r8 = slot + 0x18, depth 2 and depth 4;
and lists every write covering +0x15 with its text. Depth sensitivity for GR-1 itself: S3 at depth 5 and S4 at depth
4, the same +0x27 counts the package prints at depth 3 / 2.
"""
import os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)
import img as I  # noqa: E402

WAIT_FNS = [0x0025B400, 0x0025DF00, 0x0025E4C0, 0x002651A0, 0x0026B4C0, 0x0026B4E0, 0x003DBDC0]
TBL = {"0": 0x01EED700, "3": 0x01F281B0, "5": 0x01F29418, "7": 0x01F29440, "def": 0x01F26720}


def main():
    import retool as T
    import structflow as S
    SZ = T.sizes()

    def drain(g):
        while g.q:
            f = g.q.pop()
            dp, ent = g.entry[f]
            g.walk(f, ent, dp)

    for fld, depth in ((0x15, 3), (0x15, 5), (0x27, 5)):
        g = S.Flow([fld], depth, stride=0x28, slot=0, seed_loads={(f, 0xA8) for f in WAIT_FNS})
        g.run(sorted(WAIT_FNS))
        ws = sorted((h for h in g.hits if h[2] == "w"), key=lambda h: h[1])
        rs = sorted((h for h in g.hits if h[2] == "r"), key=lambda h: h[1])
        print("P1 field +0x%02X depth %d: walked %d; writes %d, reads %d; unknown %d, escapes %d, copies %d, indirect %s"
              % (fld, depth, len(g.entry), len(ws), len(rs), len(g.unk), len(g.esc), len(g.copies),
                 sorted("%08X" % a for f, a, t, x in g.indirect)))
        for h in ws:
            print("   W %08X %08X off=%02X w=%d %s" % (h[0], h[1], h[4], h[5], h[6]))
        if fld == 0x27:
            for h in rs:
                print("   R %08X %08X off=%02X w=%d %s" % (h[0], h[1], h[4], h[5], h[6]))
    cmds = []
    for fam, tbl in TBL.items():
        n = struct.unpack("<i", I.rd(tbl, 4))[0]
        for N in range(n):
            cmds.append(tuple(I.q(tbl + 32 * N + o) for o in (8, 0x10, 0x20)))
    H = sorted({h for c in cmds for h in c if h})
    for fld, depth in ((0x15, 2), (0x15, 4), (0x27, 4)):
        w = collections.defaultdict(set)
        r = set()
        unk = esc = 0
        for h in H:
            g = S.Flow([fld], depth, stride=0x28, slot=0)
            g.enqueue(h, {"r8": {("E", 0x18)}}, depth)
            drain(g)
            for x in g.hits:
                (w[(x[0], x[1], x[6])].add(h) if x[2] == "w" else r.add((x[0], x[1], x[6])))
            unk += len(g.unk)
            esc += len(g.esc)
        print("P2 field +0x%02X depth %d over %d handlers: write sites %d, read sites %d, unknown %d, escapes %d"
              % (fld, depth, len(H), len(w), len(r), unk, esc))
        if fld == 0x15:
            for (f, a, t), hs in sorted(w.items(), key=lambda kv: kv[0][1]):
                print("   W %08X %08X %-40s from %d handlers" % (f, a, t, len(hs)))
            for f, a, t in sorted(r, key=lambda x: x[1])[:40]:
                print("   R %08X %08X %s" % (f, a, t))


if __name__ == "__main__":
    main()
