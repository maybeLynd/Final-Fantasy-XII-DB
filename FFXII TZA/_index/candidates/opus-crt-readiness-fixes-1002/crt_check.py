"""crt_check.py - the instructions behind the 24-CRT readiness corrections (OPUS, 2026-10-02). FAILS n.
The lazy-static guard's footer and slow-path compare; the unhandled-exception filter; the condition-variable sleep;
the arena accounting byte; the name buffer's NUL.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x008092C5, "inc", "eax"),
    (0x00189D43, "jle", "0x189d76"),
    (0x007980F7, "call", "qword ptr [rip + 0x12a153]"),
    (0x0080940B, "call", "rbx"),
    (0x00369DAD, "mov", "dword ptr [rip + 0x1f6f061], 0xff"),
    (0x0036C696, "mov", "byte ptr [rbx - 5], 0"),
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
