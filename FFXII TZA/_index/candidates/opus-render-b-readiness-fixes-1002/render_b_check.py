"""render_b_check.py - the instructions behind the 17-Render readiness corrections, part B (OPUS, 2026-10-02). FAILS n.
The 0x640 command object; the page-budget subtraction and mask; the whole-chain maximum; the two-bit clear; the
floor-probe mask; the draw-list sort key; the 35.0 lens constant.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x001DB875, "mov", "edx, 0x640"),
    (0x00467AB7, "sub", "eax, dword ptr [rip + 0x283e54b]"),
    (0x00467AC3, "and", "eax, 0xfffff800"),
    (0x002F743B, "cmovl", "esi, eax"),
    (0x002F2DA4, "and", "byte ptr [rcx + 1], 0xf9"),
    (0x002F377A, "test", "byte ptr [rdi + 0x4b], 4"),
    (0x003A3B53, "mov", "eax, dword ptr [rsi + r9 + 8]"),
    (0x00193EF0, "movss", "xmm0, dword ptr [rip + 0x75f234]"),
]
FLOATS = [(0x008F312C, 35.0)]


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
    for va, want in FLOATS:
        got = struct.unpack("<f", d[off(va):off(va) + 4])[0]
        ok = got == want
        fails += 0 if ok else 1
        print("%s %08X float %r" % ("ok  " if ok else "FAIL", va, got))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
