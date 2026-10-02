"""audit_check.py - the bytes behind the audit of the 10-Status package's page-text-only value items (OPUS,
2026-10-02): +9 is the beat (003876D0 -> +0x13C) and +8 the duration (00387730 -> +0xBC); the stage-4 gate masks 1 and
2; +0x1C2 is the level byte; 0030AB40 returns 0 on its guards and (match)+1 otherwise. FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00387714, "movzx", "eax, byte ptr [rcx + 9]"),
    (0x0038788D, "movzx", "eax, byte ptr [rbx + 8]"),
    (0x0030E581, "call", "0x387730"),
    (0x0030E594, "mov", "dword ptr [rsi + rdx*4 + 0xbc], ecx"),
    (0x0030E5A2, "call", "0x3876d0"),
    (0x0030E5AF, "mov", "word ptr [rsi + rcx*2 + 0x13c], ax"),
    (0x00385CC2, "mov", "ebp, 1"),
    (0x00385D65, "mov", "ecx, 2"),
    (0x0030C496, "mov", "byte ptr [rcx + 0x1c2], dil"),
    (0x0030C6CC, "cmp", "byte ptr [rdi + 0x1c2], 0x63"),
    (0x0030AC22, "sete", "cl"),
    (0x0030AC25, "lea", "eax, [rcx + 1]"),
    (0x0030AC42, "xor", "eax, eax"),
    (0x0030AC46, "xor", "eax, eax"),
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
