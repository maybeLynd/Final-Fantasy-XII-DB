"""lin.py - SWE2-AUDIT-SPEC (SD-161 review, 2026-09-30). Whole-function linear decoder.

    python lin.py START [START ...]
Decodes from START until an int3/padding run is reached with no earlier branch target beyond it (so chained .pdata
fragments and cold tails reached by jumps inside the body are included). rip operands are resolved.
Loader: ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted there).
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402


def body(start, limit=0x4000):
    o = T.off(start)
    far = start
    out = []
    for i in T.md.disasm(T.raw[o:o + limit], start):
        if i.mnemonic == "int3" and i.address >= far:
            break
        out.append(i)
        if (i.mnemonic.startswith("j") or i.mnemonic == "call") and re.fullmatch(r"0x[0-9a-f]+", i.op_str):
            t = int(i.op_str, 16)
            if i.mnemonic != "call" and start <= t < start + limit:
                far = max(far, t)
        if i.mnemonic == "ret" or (i.mnemonic == "jmp" and not i.op_str.startswith("0x")):
            if i.address + i.size > far:
                break
        if i.mnemonic == "jmp" and re.fullmatch(r"0x[0-9a-f]+", i.op_str) and i.address + i.size > far \
                and not (start <= int(i.op_str, 16) < i.address):
            break
    return out


def fmt(i):
    s = "%08X  %-9s %s" % (i.address, i.mnemonic, i.op_str)
    for m, sz in T.mem_ops(i):
        if m.base == T.X86_REG_RIP:
            s += "   ; -> %08X" % (i.address + i.size + m.disp)
    return s


if __name__ == "__main__":
    for a in sys.argv[1:]:
        b = body(int(a, 16))
        print("== %s (%d instructions, to %08X)" % (a, len(b), b[-1].address if b else 0))
        for i in b:
            print(fmt(i))
