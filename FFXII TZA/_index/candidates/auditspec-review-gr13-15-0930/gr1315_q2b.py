"""gr1315_q2b.py - classify the NEW UI-window hits of gr1315_q2.py: for each function, print its holder loads and the
instruction window before each hit, so the base object can be typed by hand; plus raw callers (E8/E9 + jcc) and
rip lea references of each root."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0]]
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import gr1315_q2 as Q  # noqa: E402
T = Q.T

NEW = [0x003FF1F0, 0x0056A1D0, 0x0056A890, 0x0056AE80, 0x0056B100, 0x0057FB00]
for f in NEW:
    ins, order = Q.decode(f)
    print("== %08X  extent %s" % (f, ["%08X-%08X" % c for c in Q.CHUNKS.get(f, [])]))
    rc = T.rel32_callers(f)
    jc = T.jcc_callers(f)
    rr = T.rip_refs(f, f + 1)
    print("  rel32 callers %s ; jcc %s ; rip %s" % (rc, jc, ["%08X %s %s" % h[:3] for h in rr]))
    print("  entry taint from callers: %s" % sorted(Q.callee_in.get(f, set())))
    for a in order:
        i = ins[a]
        if Q.is_holder_load(i):
            print("  holder load %08X %s %s" % (a, i.mnemonic, i.op_str))
    for a in sorted(Q.hits):
        if Q.root(a) == f:
            k = order.index(a)
            print("  -- hit %08X" % a)
            for b in order[max(0, k - 14):k + 2]:
                print("     %08X %s %s" % (b, ins[b].mnemonic, ins[b].op_str))
