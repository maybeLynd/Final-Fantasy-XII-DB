"""growth_check.py - the instructions and constants behind the float-stat growth formula 002F9BD0 (OPUS, 2026-10-02).
FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x002F9BD0, "movd", "xmm1, edx"),
    (0x002F9BD4, "cvtdq2ps", "xmm1, xmm1"),
    (0x002F9BD7, "mulss", "xmm1, dword ptr [rip + 0x5cbf55]"),
    (0x002F9BDF, "addss", "xmm1, xmm0"),
    (0x002F9BE3, "comiss", "xmm1, dword ptr [rip + 0x5f954a]"),
    (0x002F9BEC, "movss", "xmm0, dword ptr [rip + 0xa15d88]"),
    (0x0030C757, "movzx", "edx, byte ptr [rbp + 0x1f]"),
    (0x0030C768, "movzx", "edx, byte ptr [rbp + 0x22]"),
    (0x0030C77E, "movzx", "edx, byte ptr [rbp + 0x25]"),
    (0x0030C794, "movzx", "edx, byte ptr [rbp + 0x28]"),
    (0x0030C712, "movzx", "ebp, word ptr [rcx + 8]"),
    (0x0030C71A, "imul", "ebp, ecx"),
]


def extra():
    import struct
    d, off = fp.load_image()
    fails = 0
    for va, want in ((0x008C5B34, 0.0078125), (0x008F3134, 100.0), (0x00D0F97C, 99.99999237060547)):
        got = struct.unpack("<f", d[off(va):off(va) + 4])[0]
        ok = got == want
        fails += 0 if ok else 1
        print("%s %08X = %r" % ("ok  " if ok else "FAIL", va, got))
    return fails


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
