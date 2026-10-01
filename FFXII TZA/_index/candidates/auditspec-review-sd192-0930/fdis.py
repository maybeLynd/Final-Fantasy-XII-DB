"""fdis.py - SWE2-AUDIT-SPEC (SD-192/SD-163/SD-161 reviews, 2026-09-30). Function-aligned disassembler.

    python fdis.py ADDR [ADDR ...]   for each ADDR, find the .pdata RUNTIME_FUNCTION containing it, decode linearly
                                     from that entry's BeginAddress and print from ADDR-0x30 to ADDR+0x40
                                     (instruction boundaries are those of the linear decode from the .pdata start)
    python fdis.py -f ADDR           print the whole .pdata extent (Begin..End) of the entry containing ADDR
Loader: ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted there). Chained unwind entries are
separate RUNTIME_FUNCTIONs; the begin printed is the entry's own, so a chained fragment prints its fragment start.
"""
import bisect, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

IB = T.IB


def pdata():
    for n, v, vs, p, rs, x in T.SECS:
        if n == ".pdata":
            blob = T.raw[p:p + min(vs, rs)]
            out = []
            for k in range(0, len(blob) - 11, 12):
                b, e, u = struct.unpack_from("<III", blob, k)
                if b:
                    out.append((IB + b, IB + e, IB + u))
            out.sort()
            return out
    raise SystemExit("no .pdata")


PD = pdata()
BEG = [b for b, e, u in PD]


def entry(a):
    k = bisect.bisect_right(BEG, a) - 1
    if k >= 0 and PD[k][0] <= a < PD[k][1]:
        return PD[k]
    return None


def peek(i):
    s = ""
    for m, sz in T.mem_ops(i):
        if m.base == T.X86_REG_RIP:
            t = i.address + i.size + m.disp
            o = T.off(t)
            s += "   ; -> %08X %s" % (t, ("u32=%08X" % struct.unpack("<I", T.raw[o:o + 4])[0]) if o is not None else "(virtual tail)")
    return s


def show(a, lo=0x30, hi=0x40, whole=False):
    e = entry(a)
    if not e:
        print("%08X: no .pdata entry" % a)
        return
    b, end, u = e
    print("== %08X in .pdata [%08X, %08X)" % (a, b, end))
    for i in T.dis(b, end):
        if whole or a - lo <= i.address <= a + hi:
            print("%08X  %-9s %s%s%s" % (i.address, i.mnemonic, i.op_str, peek(i), "   <==" if i.address == a else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    whole = False
    if args and args[0] == "-f":
        whole, args = True, args[1:]
    for x in args:
        show(int(x, 16), whole=whole)
