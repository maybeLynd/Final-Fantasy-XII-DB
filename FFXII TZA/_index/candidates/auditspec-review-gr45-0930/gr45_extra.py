"""gr45_extra.py - SWE2-AUDIT-SPEC review of rowflow.py's remaining blind spots (GR-4/GR-5, 2026-09-30).

rowflow.py is the instrument UNDER TEST (read-only import); byte reads and raw scans come from the independent img45.py.

X1  control transfers rowflow does not hand tags across, in every function it walked (all 60 offsets, depth 3):
    a jcc whose target is outside the walked extent (rowflow's step returns on any j* that is not a direct jmp), a direct
    jmp to a target retool has no size for, and a direct call to a target retool has no size for. For each, the row /
    base tags (rowflow's own probe) on rcx, rdx, r8, r9 at that instruction. A transfer with a row tag in an argument
    register would be an unfollowed hand-off.
X2  every function rowflow records as returning a row / base tag: its raw rel32 callers (E8/E9 and 0F 8x, img45) against
    the direct callers retool knows (which rowflow re-walks), and stored 64-bit pointers to it (an indirect caller's
    rax would carry the row unseen).
"""
import os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "gr4-gr5-action-row-readers-0930")
sys.path.insert(0, HERE)
sys.path.insert(0, PKG)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)
import img45 as I  # noqa: E402


def main():
    import rowflow as RF
    R, SZ, SC = RF.R, RF.SZ, RF.SC
    ALL = list(range(60))
    Fl = RF.Flow(ALL, 3)
    Fl.run(RF.slot_functions())
    walked = sorted(Fl.entry)
    rowtag = lambda v: {t for t in v if t not in ("H", "F")}
    counts = collections.Counter()
    flagged = []
    for f in walked:
        end = f + SZ.get(f, 0)
        for x in R.md.disasm(R.at(f, SZ[f]), f):
            m = x.mnemonic
            if not (m.startswith("j") or m == "call") or not x.operands or x.operands[0].type != 2:
                continue
            tgt = x.operands[0].imm
            if m == "call":
                if tgt in SZ:
                    continue
                kind = "call-unsized"
            elif m == "jmp":
                if f <= tgt < end or tgt in SZ:
                    continue
                kind = "jmp-unsized"
            else:
                if f <= tgt < end:
                    continue
                kind = "jcc-out"
            counts[kind] += 1
            pr = Fl.probe.get(x.address, {})
            tags = {r: sorted(map(str, rowtag(pr.get(r, set())))) for r in ("rcx", "rdx", "r8", "r9")
                    if rowtag(pr.get(r, set()))}
            if tags or kind != "call-unsized":
                flagged.append((kind, f, x.address, "%s %s" % (m, x.op_str), tags))
    print("X1 walked functions %d; transfers rowflow does not follow: %s" % (len(walked), dict(counts)))
    tagged = [z for z in flagged if z[4]]
    print("X1 with a row/base tag in rcx/rdx/r8/r9: %d" % len(tagged))
    for z in flagged:
        print("   %-12s %08X %08X %-40s %s" % (z[0], z[1], z[2], z[3], z[4] or "-"))
    print("X2 row/base-returning functions: %d" % len(Fl.retsum))
    for f in sorted(Fl.retsum):
        rawc = I.raw_rel32_sites(f)
        known = {s for c, s in SC["calls"].get(f, ())}
        extra = [("%08X %s" % s) for s in rawc if s[0] not in known]
        stored = []
        pat = f.to_bytes(8, "little")
        for n, v, vs, p, rs, xx in I.SECS:
            blob = I.raw[p:p + min(vs, rs)]
            k = blob.find(pat)
            while k >= 0:
                stored.append("%s %08X" % (n, v + k))
                k = blob.find(pat, k + 1)
        print("   %08X ret %-18s raw rel32 %d (retool-known %d; not known: %s); stored ptrs %s"
              % (f, sorted(map(str, Fl.retsum[f])), len(rawc), len(known), extra or "none", stored or "none"))


if __name__ == "__main__":
    main()
