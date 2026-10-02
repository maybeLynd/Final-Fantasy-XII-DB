"""formula_check.py - the instructions behind the 08-Combat-Formula readiness corrections (OPUS, 2026-10-02). FAILS n.
Items 1 (foe HP cap 1,000,000,000), 10 (slot 98 x2.0), 11-12 (both variants scale Strength +0x2A), 16 (reset to -1),
19 (context +0x28 qword, 0x30 bytes).
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x002FF7C3, "mov", "eax, 0x3b9aca00"),
    (0x0038BE12, "mulss", "xmm0, dword ptr [rip + 0x195fdee]"),
    (0x0038A2D6, "movzx", "eax, byte ptr [rcx + 0x2c]"),
    (0x0038A2ED, "movzx", "eax, byte ptr [rcx + 0x2a]"),
    (0x0038A116, "movzx", "eax, byte ptr [rcx + 0x2d]"),
    (0x0038A12D, "movzx", "eax, byte ptr [rcx + 0x2a]"),
    (0x00384A59, "mov", "dword ptr [rip + 0x2769595], 0xffffffff"),
    (0x00384A63, "mov", "dword ptr [rip + 0x276958f], 0xffffffff"),
    (0x003847F3, "mov", "qword ptr [rcx + 0x28], rax"),
]


def extra():
    import struct
    d, off = fp.load_image()
    got = struct.unpack("<f", d[off(0x01CEBC08):off(0x01CEBC08) + 4])[0]
    ok = got == 2.0
    print("%s 01CEBC08 = %r" % ("ok  " if ok else "FAIL", got))
    return 0 if ok else 1


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
    fails += extra()
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
