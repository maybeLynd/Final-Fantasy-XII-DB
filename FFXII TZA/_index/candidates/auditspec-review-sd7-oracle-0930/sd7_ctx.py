"""sd7_ctx.py - SWE2-AUDIT-SPEC, SD-7 review: by-hand context for the E1 loads sd7_rbp.py could not settle from the
prologue: 0074C8B3 ([rbp+0xa8] in 0074C790), 00771BF3 ([rbp+0xa8] in 00771B30), 00764F97 / 00765016, 00767BBC / 00767D47 ([rax+0xa8]), 0078E3D6
([rcx+0x80]), 0061ECD3 ([rcx+0x110], no .pdata). Prints every write of the base register on the aligned linear walk of
the chunk up to the load, plus the 6 instructions before the load, so the base can be read."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sd7_rbp as S  # noqa: E402  (re-prints sd7_rbp's own sections first)
L = S.L
print("\n\n######## by-hand context")
for la, reg in [(0x0074C8B3, "rbp"), (0x00771BF3, "rbp"), (0x00764F97, "rax"), (0x00765016, "rax"), (0x00767BBC, "rax"), (0x00767D47, "rax"),
                (0x0078E3D6, "rcx"), (0x0061ECD3, "rcx")]:
    e = S.chunk(la)
    print("== %08X base %s chunk %s" % (la, reg, ("%08X-%08X" % (S.IB + e[0], S.IB + e[1])) if e else "none"))
    if e:
        ins = L.dis(S.IB + e[0], la + 8)
    else:
        ins = []
        for back in (0x60, 0x50, 0x40, 0x30):
            ii = L.dis(la - back, la + 8)
            if any(i.address == la for i in ii):
                ins = ii
                break
    w = [i for i in ins if reg in S.writes(i) and i.address < la]
    print("  writes of %s before the load: %s" % (reg, ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in w[-4:]]))
    k = [n for n, i in enumerate(ins) if i.address == la]
    if k:
        for i in ins[max(0, k[0] - 6):k[0] + 1]:
            print("    %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    else:
        print("  load NOT on the aligned walk")
