"""gr1_transfers.py - SWE2-AUDIT-SPEC review of GR-1: transfers structflow does not hand tags across (2026-09-30).

structflow.py (instrument under test, read-only) returns on any jcc and on a direct call / jmp to a target retool has
no size for; at depth 0 it hands nothing on. In every function walked for S3 (seven wait functions, depth 3) and for
S4 (each handler, r8 = slot + 0x18, depth 2), list those transfers where a slot tag (E, k) sits in rcx / rdx / r8 / r9
(structflow's own probe), plus direct calls made at depth 0 with a tagged argument (not followed).
"""
import os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)
import img as I  # noqa: E402

WAIT_FNS = [0x0025B400, 0x0025DF00, 0x0025E4C0, 0x002651A0, 0x0026B4C0, 0x0026B4E0, 0x003DBDC0]
TBL = [0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440, 0x01F26720]


def scan(g, R, SZ, label, out, cnt):
    for f, (dp, ent) in g.entry.items():
        end = f + SZ.get(f, 0)
        for x in R.md.disasm(R.at(f, SZ[f]), f):
            m = x.mnemonic
            if not (m.startswith("j") or m == "call") or not x.operands or x.operands[0].type != 2:
                continue
            tgt = x.operands[0].imm
            pr = g.probe.get(x.address, {})
            tags = {r: sorted(map(str, v)) for r, v in pr.items() if r in ("rcx", "rdx", "r8", "r9")
                    and any(isinstance(t, tuple) for t in v)}
            if not tags:
                continue
            if m == "call":
                kind = "call-unsized" if tgt not in SZ else ("call-depth0" if dp == 0 else None)
            elif m == "jmp":
                kind = None if (f <= tgt < end) else ("jmp-unsized" if tgt not in SZ else ("jmp-depth0" if dp == 0 else None))
            else:
                kind = None if f <= tgt < end else "jcc-out"
            if kind:
                cnt[(label, kind)] += 1
                out.add((label, kind, f, x.address, "%s %s" % (m, x.op_str), repr(tags)))


def main():
    import retool as T
    import structflow as S
    R, SZ = T.R, T.sizes()
    out, cnt = set(), collections.Counter()
    g = S.Flow([0x27], 3, stride=0x28, slot=0, seed_loads={(f, 0xA8) for f in WAIT_FNS})
    g.run(sorted(WAIT_FNS))
    scan(g, R, SZ, "S3", out, cnt)
    H = set()
    for tbl in TBL:
        n = struct.unpack("<i", I.rd(tbl, 4))[0]
        for N in range(n):
            for o in (8, 0x10, 0x20):
                h = I.q(tbl + 32 * N + o)
                if h:
                    H.add(h)
    for h in sorted(H):
        gh = S.Flow([0x27], 2, stride=0x28, slot=0)
        gh.enqueue(h, {"r8": {("E", 0x18)}}, 2)
        while gh.q:
            f = gh.q.pop()
            dp, ent = gh.entry[f]
            gh.walk(f, ent, dp)
        scan(gh, R, SZ, "S4", out, cnt)
    print("unfollowed transfers with a slot tag in an argument register: %s" % dict(sorted(cnt.items())))
    by = collections.defaultdict(list)
    for z in sorted(out, key=lambda z: (z[0], z[1], z[3])):
        by[(z[0], z[1])].append(z)
    for k, zs in by.items():
        print("%s %s: %d distinct sites" % (k[0], k[1], len({z[3] for z in zs})))
        seen = set()
        for z in zs:
            if z[3] in seen:
                continue
            seen.add(z[3])
            if len(seen) <= 25:
                print("   %08X %08X %-36s %s" % (z[2], z[3], z[4], z[5]))


if __name__ == "__main__":
    main()
