"""ebp_check.py - the instructions behind the 25-EBP readiness corrections (OPUS, 2026-10-02). FAILS n.
The section-count dword; the table's second dword; the pending-bit setter 0032ED70 (not a teardown); the 0x400 clear;
the weather byte roll; the two 0xFFFF words; the CC-10 reads; the u32[20] directory; the REQALL channel pops; the CAM7
+0x20 read; the always-zero kind-1 arm.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00264D7D, "shr", "rax, 2"),
    (0x00358A0F, "mov", "eax, dword ptr [r8 + rax*8 + 8]"),
    (0x0032ED73, "lea", "rcx, [rip + 0x1f980ce]"),
    (0x0032ED7A, "or", "qword ptr [rcx + rax*8], 1"),
    (0x00331715, "btr", "rbx, 0xa"),
    (0x0025ACCC, "call", "0x2658b0"),
    (0x005C5230, "xor", "eax, eax"),
    (0x005C5232, "ret", ""),
    (0x003DA204, "mov", "word ptr [rcx + 0x18], ax"),
    (0x003DA20B, "mov", "word ptr [rcx + 0x1a], ax"),
    (0x0037DAC4, "cmp", "word ptr [rcx + 4], 0"),
    (0x0037DADD, "movzx", "ebx, word ptr [rdi + 6]"),
    (0x0033051F, "mov", "eax, dword ptr [rdi + 0x18]"),
    (0x00330656, "mov", "eax, dword ptr [rdi + 0x5c]"),
    (0x00257341, "mov", "edx, dword ptr [rdi + 0x20]"),
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
