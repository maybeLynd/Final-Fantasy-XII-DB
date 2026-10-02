"""rewards_check.py - the instructions behind the 13-Rewards readiness corrections (OPUS, 2026-10-02). FAILS n.
Items 1 (LP gate), 3 (profile row +0x05 read), 4 (weighted pick when 022C3164 > 0), 6 (the extra-item gate compares
the condition item), 7 (counter 11 is LP), 10 (+0x18C experience cap, +0x190 LP), 11 (the level-up event is posted),
12 (the float-stat gate is the record kind byte), 14 (pool init numbers every slot) and 15 (HUD flags 0 then |8).
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x002F90E7, "movzx", "eax, byte ptr [rbx + 4]"),
    (0x002F90EB, "cmp", "al, 0x1a"),
    (0x002F90EF, "cmp", "al, 6"),
    (0x003181C7, "movzx", "eax, byte ptr [rcx + 5]"),
    (0x0031815C, "cmp", "dword ptr [rip + 0x1fab001], r14d"),
    (0x00318165, "call", "0x318820"),
    (0x00318527, "cmp", "dx, ax"),
    (0x00312489, "mov", "cl, 0xb"),
    (0x0031248F, "mov", "dword ptr [rdi + 0x190], r8d"),
    (0x00312432, "mov", "ecx, dword ptr [rdi + 0x18c]"),
    (0x00312438, "mov", "eax, 0x5f5e0ff"),
    (0x00312444, "mov", "dword ptr [rdi + 0x18c], ecx"),
    (0x0030C7DB, "cmp", "byte ptr [rdi + 5], 0"),
    (0x0030C7E4, "call", "0x46a690"),
    (0x0030C6D9, "cmp", "byte ptr [rdi + 5], 0"),
    (0x00319C3E, "mov", "dword ptr [rip + 0x2ba7418], 2"),
    (0x0028EF07, "mov", "dword ptr [rax + 0x7c7c], 0"),
    (0x0028EF18, "or", "dword ptr [rax + 0x7c7c], 8"),
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
