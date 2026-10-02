"""c1_workspace_check.py - the instructions behind the CharacterRenderRecord +0x0C1 and +0x2FC rows as consumed
2026-10-01 from ASTRA's render-c1-nibble-producers, accounting-dispatch-index and skeleton-workspace-factory (OPUS).
FAILS n.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x002E29A4, "movzx", "edx, byte ptr [rsi + 0x10]"),
    (0x002E29B6, "shr", "edx, 4"),
    (0x002E29E9, "mov", "byte ptr [rcx + 0xc1], dl"),
    (0x002E3367, "movzx", "edx, byte ptr [rbx + 0x10]"),
    (0x002E3380, "shr", "edx, 4"),
    (0x002E33B3, "mov", "byte ptr [rcx + 0xc1], dl"),
    (0x0041F515, "movsx", "ebx, byte ptr [r14 + 0xc1]"),
    (0x0041F525, "mov", "edx, ebx"),
    (0x0041F527, "call", "0x3ab910"),
    (0x003AB932, "jmp", "0x36c5d0"),
    (0x0036C5D0, "movsxd", "r8, edx"),
    (0x0036C616, "mov", "byte ptr [rdx + 0x17], r8b"),
    (0x0041F443, "call", "0x3712e0"),
    (0x0041F4D2, "mov", "edx, 1"),
    (0x0041F4DB, "call", "0x3ab8b0"),
    (0x0041F4EA, "mov", "dword ptr [r14 + 0x2fc], eax"),
    (0x0041F57A, "call", "0x46e4d0"),
    (0x0041F57F, "cmp", "eax, -1"),
    (0x0041F584, "xor", "esi, esi"),
    (0x0041F586, "jmp", "0x41f595"),
    (0x0041F595, "mov", "ecx, dword ptr [rsi + 4]"),
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
