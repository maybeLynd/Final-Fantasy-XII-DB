"""engine_b_check.py - the instructions behind the 00-Engine readiness corrections, part B (OPUS, 2026-10-02). FAILS n.
The third vf00 writer; the CLIP word shift; the registered console thunk; the one store to 01F82D20; the inc-only
console counter.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0036DD87, "movups", "xmmword ptr [rip + 0x1b8b662], xmm0"),
    (0x0025A8EE, "shl", "eax, 6"),
    (0x008AB7C7, "jmp", "0x5dddb0"),
    (0x00798261, "mov", "qword ptr [rip + 0x17eaab8], rax"),
    (0x001D1C8E, "inc", "ecx"),
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
