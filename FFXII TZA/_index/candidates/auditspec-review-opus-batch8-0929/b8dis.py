"""b8dis.py - SWE2-AUDIT-SPEC (batch-8 review, 2026-09-29). Resolving disassembler over the certified image.

    python b8dis.py START END [START END ...]     linear decode, rip targets resolved (u32/f32 peek; "(virtual tail)"
                                                  past raw data = zero-initialised)
Reuses the image loader of ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted there).
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402


def peek(va):
    o = T.off(va)
    if o is None:
        return "(virtual tail / unmapped)"
    b = T.raw[o:o + 4]
    u = struct.unpack("<I", b)[0]
    return "u32=%08X f32=%g" % (u, struct.unpack("<f", b)[0])


def dump(a, b):
    for i in T.dis(a, b):
        s = "%08X  %-9s %s" % (i.address, i.mnemonic, i.op_str)
        for m, sz in T.mem_ops(i):
            if m.base == T.X86_REG_RIP:
                t = i.address + i.size + m.disp
                s += "   ; -> %08X %s" % (t, peek(t))
        print(s)


if __name__ == "__main__":
    a = sys.argv[1:]
    for k in range(0, len(a), 2):
        dump(int(a[k], 16), int(a[k + 1], 16))
        print("---")
