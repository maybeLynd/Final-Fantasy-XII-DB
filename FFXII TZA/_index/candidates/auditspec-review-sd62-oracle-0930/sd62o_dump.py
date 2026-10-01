"""sd62o_dump.py - SWE2-AUDIT-SPEC (SD-62 ORACLE review, 2026-09-30). Dumps the .pdata extent of each named function
and its linear decode, rip targets resolved (image bytes, qword peek), through this lane's ov31_indep loader.
    python sd62o_dump.py FUNC [FUNC ...]
"""
import os, struct, sys, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def chunks(fva):
    """every .pdata entry whose chain root is fva (primary + chained parts)."""
    res = []
    for e in PD:
        r = e
        while True:
            uo = T.off(T.IB + r[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
            if not (fl & 4):
                break
            r = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
        if T.IB + r[0] == fva:
            res.append((T.IB + e[0], T.IB + e[1]))
    return sorted(res)


def peek(va):
    o = T.off(va)
    if o is None:
        return "(virtual tail)"
    return "q=%016X" % struct.unpack("<Q", T.raw[o:o + 8])[0]


if __name__ == "__main__":
    for a in sys.argv[1:]:
        f = int(a, 16)
        ch = chunks(f)
        print("=== %08X chunks %s" % (f, " ".join("%08X-%08X" % c for c in ch)))
        for s, e in ch:
            for i in T.dis(s, e):
                line = "%08X  %-8s %s" % (i.address, i.mnemonic, i.op_str)
                for m, sz in T.mem_ops(i):
                    if m.base == T.X86_REG_RIP:
                        t = i.address + i.size + m.disp
                        line += "   ; -> %08X %s" % (t, peek(t))
                print(line)
