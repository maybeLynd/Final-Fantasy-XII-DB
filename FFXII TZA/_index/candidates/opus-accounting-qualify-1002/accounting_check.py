"""accounting_check.py - the instructions behind the 2026-10-02 qualification of OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY
and the two carried SWE2-DATA additions on the allocator page (OPUS). FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    # 003AB910: the boolean picks the helper; edx is untouched
    (0x003AB91A, "test", "cl, 3"),
    (0x003AB923, "setne", "r8b"),
    (0x003AB932, "jmp", "0x36c5d0"),
    (0x003AB937, "jmp", "0x36c620"),
    (0x0036C5D0, "movsxd", "r8, edx"),
    (0x0036C616, "mov", "byte ptr [rdx + 0x17], r8b"),
    (0x0036C646, "movsxd", "rax, edx"),
    (0x0041F515, "movsx", "ebx, byte ptr [r14 + 0xc1]"),
    (0x0041F525, "mov", "edx, ebx"),
    (0x0041F527, "call", "0x3ab910"),
    (0x002E29B6, "shr", "edx, 4"),
    (0x002E29E9, "mov", "byte ptr [rcx + 0xc1], dl"),
    (0x002E3380, "shr", "edx, 4"),
    (0x002E33B3, "mov", "byte ptr [rcx + 0xc1], dl"),
    # carried SWE2-DATA additions: the arena spin and pre_cpp_initialization
    (0x0036BFF8, "bt", "eax, ecx"),
    (0x0036BFFB, "jb", "0x36c002"),
    (0x0036C000, "jmp", "0x36c000"),
    (0x00808D60, "call", "0x809b44"),
    (0x00808D65, "call", "0x5c5230"),
    (0x00808D70, "jmp", "0x862046"),
    (0x00809B4B, "jmp", "qword ptr [rip + 0xb86fe]"),
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
