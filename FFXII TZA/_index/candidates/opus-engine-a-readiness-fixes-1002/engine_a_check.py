"""engine_a_check.py - the instructions behind the 00-Engine readiness corrections, part A (OPUS, 2026-10-02). FAILS n.
The folded empty stub; the boot store of 01FD4A90; the mode-ladder bit-0 skip; the class registry's class-16 arm.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0016D6A0, "ret", "0"),
    (0x0022A2A3, "mov", "qword ptr [rip + 0x1daa7e6], rax"),
    (0x00313853, "je", "0x31386a"),
    (0x00322EE5, "mov", "rax, qword ptr [rip + 0x2b9c174]"),
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
