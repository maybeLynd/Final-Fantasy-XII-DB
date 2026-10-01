"""gr45_residue.py - the +0x0B accesses gr45_census.py could not type, cross-examined (GR-4/GR-5 review, 2026-09-30).

For every access covering +0x0B in gr45_census's S0..S3 set whose base has an unfollowed leaf (and no row leaf), print
the unfollowed leaves (a stack-pointer leaf `ENTRY:rsp` = an rbp/rsp frame access, shown separately), whether the
reviewed package's rowflow.py (instrument under test, read-only) has ANY tag on the base or index register at that
instruction, and whether rowflow walked the function at all. A residue access that neither instrument can type is
listed for reading by hand.
"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "gr4-gr5-action-row-readers-0930"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)
import gr45_census as G  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402


def main():
    import rowflow as RF
    Fl = RF.Flow(list(range(60)), 3)
    Fl.run(RF.slot_functions())
    walked_extents = [(f, f + RF.SZ[f]) for f in Fl.entry]
    sites = [int(l, 16) for l in open(os.path.join(HERE, "pkg_slot_sites.txt")) if l.strip()]
    S0 = {G.owner(a) for a in sites}
    allf = G.reach(S0, 3)
    F = 0x0B
    res = []
    cls = collections.Counter()
    for b in sorted(allf):
        ins = G.func(b)[0]
        for j, x in enumerate(ins):
            if x.mnemonic in ("lea", "nop") or x.mnemonic.startswith("prefetch"):
                continue
            for op in x.operands:
                if op.type != X86_OP_MEM:
                    continue
                bs = G.fam(x, op.mem.base)
                if bs in (None, "rip", "rsp"):
                    continue
                c = G.covers(op.mem.disp, op.size, F)
                if not c:
                    continue
                s = G.src(b, j, bs)
                si = G.fam(x, op.mem.index)
                if si and op.mem.scale == 1:
                    s = s | G.src(b, j, si)
                if "ROWBASE" in s:
                    cls["row"] += 1
                    continue
                unf = sorted(l for l in s if l.split(":")[0] in G.UNFOLLOWED)
                if not unf:
                    cls["typed non-row"] += 1
                    continue
                frame_only = all(l == "ENTRY:rsp" for l in unf)
                inwalk = any(lo <= x.address < hi for lo, hi in walked_extents)
                pr = Fl.probe.get(x.address, {})
                rt = sorted(map(str, (pr.get(bs, set()) | (pr.get(si, set()) if si else set()))))
                key = ("frame(rsp-derived)" if frame_only else "unfollowed") + (" / rowflow-tag" if rt else "") + \
                      ("" if inwalk else " / not walked by rowflow")
                cls[key] += 1
                if not frame_only:
                    res.append((b, x, c, op.size, unf, rt, inwalk))
    print("+0x0B covering accesses in S0..S3 by typing outcome: %s" % dict(sorted(cls.items())))
    print("residue (an unfollowed leaf other than the stack pointer): %d" % len(res))
    for b, x, c, w, unf, rt, inwalk in res:
        print("   %08X %08X %-5s w%-2d %-46s %-40s rowflow %s%s" % (b, x.address, c, w, "%s %s" % (x.mnemonic, x.op_str),
                                                              ",".join(unf)[:40], rt or "-", "" if inwalk else " (not walked)"))


if __name__ == "__main__":
    main()
