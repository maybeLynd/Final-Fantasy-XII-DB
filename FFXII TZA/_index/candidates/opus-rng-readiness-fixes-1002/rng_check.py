"""rng_check.py - the instructions behind the 21-RNG readiness corrections (OPUS, 2026-10-02). FAILS n.
The PPFX xorshift128 0074BDE0 (counter 01F3CD6C stepped through MT's init recurrence, `sar 8`); the MT float draw
00863C80 seeds and twists through 00866D60 / 00866B90 and advances the cursor 02EB4230 itself, behind the do-once latch
02EB4234; the graphics twist 0018EE20 (masks, partners [+0x634] / [-0x38C], cursor +0x9C0 and count +0x9C8 set at the
end, no ISA test); the two +0x9BC operands of 0018D740; DAT_02089300's only clear and set and their boot callers; the
camera-shake sampler's float draw.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0074BFF5, "mov", "dword ptr [rip + 0x17f0d70], r8d"),
    (0x0074C007, "imul", "r8d, eax, 0x6c078965"),
    (0x0074C0BD, "sar", "edi, 8"),
    (0x00863C84, "cmp", "byte ptr [rip + 0x26505a9], 0"),
    (0x00863C99, "mov", "edx, 0x1571"),
    (0x00863CA3, "call", "0x866d60"),
    (0x00863CBA, "mov", "byte ptr [rip + 0x2650573], 1"),
    (0x00863CCE, "call", "0x866b90"),
    (0x00863CE8, "mov", "dword ptr [rip + 0x2650542], edx"),
    (0x0018EE39, "and", "r8d, 0x7ffffffe"),
    (0x0018EE40, "and", "edx, 1"),
    (0x0018EE54, "xor", "r8d, dword ptr [rax + 0x634]"),
    (0x0018EE68, "mov", "r9d, 0x18c"),
    (0x0018EE92, "xor", "edx, dword ptr [rax - 0x38c]"),
    (0x0018EECD, "mov", "dword ptr [r10 + 0x9c8], 0x270"),
    (0x0018EED8, "mov", "qword ptr [r10 + 0x9c0], r10"),
    (0x0018D761, "lea", "rdx, [rcx + 0x9bc]"),
    (0x0018D76C, "lea", "r10, [r9 + 0x9bc]"),
    (0x002368E1, "xor", "ebx, ebx"),
    (0x002368F8, "mov", "dword ptr [rip + 0x1e52a02], ebx"),
    (0x00236A44, "mov", "dword ptr [rip + 0x1e528b2], 1"),
    (0x0022A41A, "call", "0x2368d0"),
    (0x0022B77C, "call", "0x236a40"),
    (0x0037D291, "call", "0x379ce0"),
]


def extra(d, off, md):
    """0018EE20 to its ret: no rip-relative operand, so no test of the ISA dword 01F44858."""
    fails = 0
    for ins in md.disasm(d[off(0x0018EE20):off(0x0018EEE0)], 0x0018EE20):
        if "rip" in ins.op_str:
            fails += 1
            print("FAIL %08X rip-relative operand in the graphics twist: %s %s" % (ins.address, ins.mnemonic, ins.op_str))
    print("%s 0018EE20-0018EEDF has no rip-relative operand" % ("ok  " if not fails else "FAIL"))
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
    fails += extra(d, off, md)
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
