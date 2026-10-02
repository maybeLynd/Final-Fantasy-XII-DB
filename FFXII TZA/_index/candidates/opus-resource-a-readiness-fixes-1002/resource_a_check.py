"""resource_a_check.py - the instructions behind the 02-Resource readiness corrections, part A (OPUS, 2026-10-02).
FAILS n. The byte-count argument and its cap; the dormant stepper's round-up; the kind-0xFF gate; the 767-entry rebase
loop; the 0x50-byte resource entry; the 64-slot registry end 02EBF200; the missed fifth inner binder; the unchecked
row lookup.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0032E92C, "mov", "dword ptr [r10 + 0x28], esi"),
    (0x0032E713, "cmp", "eax, 0x80000"),
    (0x0046DDE6, "add", "eax, 0x7ff"),
    (0x0032E0D7, "cmp", "al, 0xff"),
    (0x003A9BAD, "mov", "ebx, 8"),
    (0x003A9BF0, "cmp", "rbx, 0x1800"),
    (0x00409F23, "mov", "edx, 0x50"),
    (0x00237031, "mov", "qword ptr [rip + 0x2c881c8], rcx"),
    (0x00236D94, "call", "0x3847b0"),
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
