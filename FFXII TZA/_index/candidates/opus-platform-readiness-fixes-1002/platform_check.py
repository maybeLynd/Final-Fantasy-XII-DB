"""platform_check.py - the instructions behind the 20-Platform readiness corrections (OPUS, 2026-10-02). FAILS n.
Mode 0 is a signed compare; the negative-sum clamp; the two id bounds; counter 11 takes the per-award increment; the
Steam entry bound; the evaluator's mode-byte read.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00316B09, "cmp", "edi, eax"),
    (0x00316BA1, "xor", "ebx, ebx"),
    (0x00316A50, "cmp", "cl, 0x1e"),
    (0x00312484, "mov", "edx, esi"),
    (0x0020CC80, "cmp", "rbx, 0x3c90"),
    (0x00315EFA, "movzx", "eax, byte ptr [r15 + r14*8 + 0xbf0462]"),
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
