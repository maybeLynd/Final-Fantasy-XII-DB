"""riprefs.py - every rip-relative operand whose target lies in [lo, hi), over every .pdata fragment of the shipping
image (ORACLE, 2026-09-30, RC-11). Fragments are decoded linearly from their own begin to end, so chained fragments
and code outside functions.tsv are covered. Blind spot: a reference formed through a base register loaded once.

Usage: python riprefs.py <lo_hex> [hi_hex]
Positive control, always run: the arena selection push's store of the active arena 022D89BC inside 0036C1F0 must be
found (the memory page: installs the active arena through the map, 0036C272-0036C27F).
"""
import sys
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
import img


def scan(lo, hi):
    hits = []
    for b, e, _u in img.PDATA:
        for x in img.dis(b, e - b):
            for i, o in enumerate(x.operands):
                if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                    t = x.address + x.size + o.mem.disp
                    if lo <= t < hi:
                        k = "lea" if x.mnemonic == "lea" else (
                            "w" if i == 0 and len(x.operands) > 1 and not x.mnemonic.startswith(("cmp", "test", "bt"))
                            else "r")
                        hits.append((img.owner(x.address), x.address, k, x.mnemonic, x.op_str, t))
    return hits


def main():
    lo = int(sys.argv[1], 16)
    hi = int(sys.argv[2], 16) if len(sys.argv) > 2 else lo + 8
    hits = scan(min(lo, 0x022D89BC), max(hi, 0x022D89C0))
    ctl = any(0x0036C1F0 <= a < 0x0036C290 and k == "w" and t == 0x022D89BC for _f, a, k, _m, _o, t in hits)
    print("%s  control: 0036C1F0 stores the active arena 022D89BC" % ("PASS" if ctl else "FAIL"))
    for f, a, k, m, ops, t in hits:
        if lo <= t < hi:
            print("%08X  %08X  %-3s  %-6s %-44s -> %08X" % (f or 0, a, k, m, ops, t))
    return 0 if ctl else 1


if __name__ == "__main__":
    sys.exit(main())
