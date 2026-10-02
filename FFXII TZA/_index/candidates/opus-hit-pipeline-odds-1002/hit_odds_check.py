"""hit_odds_check.py - the instructions behind the hit pipeline's odds as documented 2026-10-02 (OPUS): knockback
00388350, counter chance 00388490, combo 00388550 (1.8f / 0.7f), the ranged critical 00389140 and the post-modifiers
00390F20. FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0038836C, "cmp", "byte ptr [rcx + 0x1c2], bpl"),
    (0x00388379, "call", "0x379cd0"),
    (0x00388387, "div", "ecx"),
    (0x00388398, "call", "0x379cd0"),
    (0x00388409, "movzx", "eax, byte ptr [rcx + 0x1b]"),
    (0x00388490, "test", "dword ptr [r8 + 8], 0x2018"),
    (0x003884C5, "movzx", "eax, byte ptr [rdx + 0x2d]"),
    (0x003884C9, "shr", "eax, 1"),
    (0x003884D6, "add", "eax, eax"),
    (0x003891B3, "movzx", "ebx, byte ptr [rbx + 0x1c]"),
    (0x003891B7, "call", "0x379cd0"),
    (0x003891D0, "cmp", "ebx, r8d"),
    (0x003891D9, "or", "dword ptr [rax + 0x18], 1"),
    (0x00390F2F, "test", "byte ptr [rdx + 0x6f], 4"),
    (0x00390F7B, "mov", "eax, 0x270f"),
    (0x00390F9C, "cmp", "dword ptr [rip + 0x275d02e], 0xb3"),
]


def extra():
    import struct
    d, off = fp.load_image()
    fails = 0
    for va, want in ((0x00908E1C, 1.7999999523162842), (0x008F3104, 0.699999988079071)):
        got = struct.unpack("<f", d[off(va):off(va) + 4])[0]
        fails += 0 if got == want else 1
        print("%s %08X = %r" % ("ok  " if got == want else "FAIL", va, got))
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
