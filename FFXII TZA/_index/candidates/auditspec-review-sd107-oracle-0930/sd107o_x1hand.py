"""sd107o_x1hand.py - print context for the six X1 sites that the .pdata linear decode did not land on, so they can
be read by hand: (a) the linear decode from the chunk start around the site, (b) back-decodes that land on the site."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import sd107o_extra as X  # noqa: E402  (re-runs X1-X3 quietly into stdout first)
T = X.T
print("\n\n######## X1 by-hand context")
for a in [0x001BABB9, 0x0036C5B6, 0x005B2E51, 0x005B31B1, 0x007797C9, 0x007797E8]:
    e = X.chunk(a)
    print("== %08X  chunk %s" % (a, ("%08X-%08X" % (X.IB + e[0], X.IB + e[1])) if e else "none"))
    if e:
        ins = [i for i in T.dis(X.IB + e[0], X.IB + e[1]) if a - 0x30 <= i.address <= a + 0x10]
        print("  linear from chunk start:")
        for i in ins:
            print("    %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    for back in (0x40, 0x30, 0x20):
        ii = T.dis(a - back, a + 0x10)
        if any(i.address == a for i in ii):
            print("  back-decode from -%#x lands:" % back)
            for i in ii[-10:]:
                print("    %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
            break
    else:
        print("  no back-decode from -0x40/-0x30/-0x20 lands on the site")
