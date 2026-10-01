"""sd5_display_requests.py - who sets / clears the application's one-shot display requests (+0x1E..+0x21, +0x29)?
(OPUS, 2026-09-30; register SD-5)

The keyboard transition pass (0079C259 -> 0079D010) runs only while bytes +0x1E, +0x1F, +0x20, +0x21 and +0x29 of the
application are all zero (0079C240-0079C257, inside the framework's per-frame update 0079C140). This census lists every
store to those bytes on every route the SD-7 census follows to the application object (the static object 01F7E350, the
framework pointer 02EA5368, the window data, and each GameApplication method's rcx), through the same value-flow engine
(../sd7-slot15-callers-0930/sd7_slot15_callers.py). Every memory operand whose base register holds APP + k is recorded.
Control P: the pass's own five reads at 0079C240-0079C254 are found.
"""
import collections, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sd7-slot15-callers-0930"))
import sd7_slot15_callers as S  # noqa: E402  (sets up the APP / APPVT tokens and the roots)
F, K, X, R = S.F, S.K, S.X, S.R

WANT = {0x1E, 0x1F, 0x20, 0x21, 0x29}
acc = collections.defaultdict(set)    # byte -> {(fn, addr, kind, text)}


class ByteCensus(S.AppCensus):
    def step(self, f, st, i, depth, stack, caller_writes):
        ops = i.operands
        for n, op in enumerate(ops):
            if op.type != X.X86_OP_MEM or op.mem.base in (0, X.X86_REG_RIP):
                continue
            bv = st.r.get(K.fullname(op.mem.base)[0], K.UNK)
            if bv is K.UNK:
                continue
            for b, o in bv:
                if b != "APP" or o is None or op.mem.index != 0:
                    continue
                lo = o + op.mem.disp
                for w in WANT:
                    if lo <= w < lo + max(op.size, 1):
                        kind = "W" if (n == 0 and i.mnemonic not in ("cmp", "test")) else "R"
                        acc[w].add((S.CUR[-1] if S.CUR else f, i.address, kind, "%s %s" % (i.mnemonic, i.op_str)))
        return super().step(f, st, i, depth, stack, caller_writes)


def main():
    t0 = time.time()
    refs, calls = F.scan()
    F.globals_root.clear()
    an = ByteCensus()
    roots = set(f for f, _, _ in refs.get(S.APP_OBJ, ())) | set(f for f, _, _ in refs.get(S.APP_PTR, ()))
    for f in sorted(roots):
        an.summary(f, (), 0, ())
    for f in sorted(set(f for f, _, _ in refs.get(S.GWLP_IAT, ()))):
        an.summary(f, (), 0, ())
    an.summary(S.WNDPROC, (("r9", K.vs(("CS", 0))),), 0, ())
    vt = S.vtable(S.VT)
    for f in sorted(set(x for x in vt[:31] if 0x00120000 <= x < 0x00900000)):
        an.summary(f, (("rcx", K.vs(("APP", 0))),), 0, ())
    print("bodies reached %d (%.0f s)" % (len(an.fns), time.time() - t0))
    p = all(any(x[1] == a and x[2] == "R" for xs in acc.values() for x in xs)
            for a in (0x0079C240, 0x0079C245, 0x0079C24A, 0x0079C24F, 0x0079C254))
    print("%s  P the pass gate's five reads (0079C240-0079C254) are found" % ("PASS" if p else "FAIL"))
    for w in sorted(WANT):
        xs = sorted(acc.get(w, ()))
        print("+0x%02X  writes: %s" % (w, "; ".join("%08X@%08X %s" % (x[0], x[1], x[3]) for x in xs if x[2] == "W") or "-"))
        print("       reads : %s" % (" ".join("%08X@%08X" % (x[0], x[1]) for x in xs if x[2] == "R") or "-"))
    print("escapes of the application pointer (holders not followed): %d; indirect calls with it: %d" % (
        len(set(an.escapes)), len(set(an.indirect))))
    return 0 if p else 1


if __name__ == "__main__":
    sys.exit(main())
