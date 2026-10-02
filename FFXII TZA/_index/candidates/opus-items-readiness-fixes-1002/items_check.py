"""items_check.py - the instructions behind the 12-Items readiness corrections (OPUS, 2026-10-02). FAILS n.
Items 1 (write dispatch +0x48), 4 (00308FF0 returns byte +0x0A for categories 5/6), 5/6 (the licence check reads the
stats record; row 6), 10 (the bazaar purchase gate), 12 (the purchase path), 13 (decode base 01F83530) and 14 (the
table root [02EBF190]+8).
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00300943, "mov", "rax, qword ptr [rsi + 0x48]"),
    (0x0030904A, "movzx", "eax, byte ptr [rcx + 0x1e]"),
    (0x0030904E, "sub", "al, 5"),
    (0x00309054, "movzx", "eax, byte ptr [rcx + 0xa]"),
    (0x00323EF3, "movzx", "eax, byte ptr [rsi + 5]"),
    (0x00323EFF, "cmp", "byte ptr [rsi + 4], 6"),
    (0x0030B194, "lea", "ecx, [r8 + 0x12]"),
    (0x0030B198, "call", "0x322c50"),
    (0x0056D4AC, "cmp", "eax, 0x2c0"),
    (0x0020E602, "add", "rax, qword ptr [rip + 0x1d74f27]"),
    (0x00317B36, "mov", "rax, qword ptr [rip + 0x2ba7653]"),
    (0x00317B3D, "add", "rax, 8"),
]


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and ins.op_str == ops
        fails += 0 if ok else 1
        got = "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<no decode>"
        print("%s %08X %s" % ("ok  " if ok else "FAIL", va, got))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
