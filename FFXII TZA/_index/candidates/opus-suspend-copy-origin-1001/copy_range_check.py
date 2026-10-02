"""copy_range_check.py - the instructions the commit-action contract's suspend-copy correction cites, decoded from the
shipping image (OPUS, 2026-10-01). Refuses (FAILS n) if any cited instruction no longer decodes as recorded.

Restore 0030EDA0 copies [unit+0x6B0, unit+0xBA0): base at 0030EDA7, the loop's lead lea at 0030EDB6 runs before the
stores at rcx-0x80 (0030EDC7), the tail ends at +0xBA0, and the scan compares the saved r8 (0030EE5D). Snapshot
0030EFF0 refuses on flag 24 or (word +0x714 <= 0x21E and byte +0x6B4 >= 6), copies from +0x6B0, memsets it and
stores +0xB88. The automatic engage 00312FA0 clears +0x28, snapshots, then commits 0x96 with a cancel argument of 0;
the recommit 0030FA00 passes 1.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0030EDA0, "mov", "r8, qword ptr [rcx + 0xb88]"),
    (0x0030EDA7, "add", "rcx, 0x6b0"),
    (0x0030EDB1, "mov", "edx, 9"),
    (0x0030EDB6, "lea", "rcx, [rcx + 0x80]"),
    (0x0030EDC7, "movups", "xmmword ptr [rcx - 0x80], xmm0"),
    (0x0030EE13, "movups", "xmmword ptr [rcx], xmm0"),
    (0x0030EE44, "movups", "xmmword ptr [rcx + 0x60], xmm0"),
    (0x0030EE5D, "cmp", "r8, rdx"),
    (0x0030EFFF, "bt", "rax, 0x18"),
    (0x0030F00A, "mov", "eax, 0x21e"),
    (0x0030F00F, "cmp", "word ptr [rcx + 0x714], ax"),
    (0x0030F016, "ja", None),
    (0x0030F018, "cmp", "byte ptr [rcx + 0x6b4], 6"),
    (0x0030F01F, "jae", None),
    (0x0030F02A, "call", "0x30dfa0"),
    (0x0030F04A, "lea", "rax, [rbx + 0x6b0]"),
    (0x0030F0AC, "mov", "r8d, 0x4f0"),
    (0x0030F0E5, "lea", "rcx, [rbx + 0x6b0]"),
    (0x0030F0F1, "mov", "qword ptr [rbx + 0xb88], rdi"),
    (0x00312FB5, "mov", "dword ptr [rcx + 0x28], 0"),
    (0x0031307B, "call", "0x30eff0"),
    (0x00313096, "mov", "r8d, 0x96"),
    (0x0031309C, "mov", "dword ptr [rsp + 0x20], 0"),
    (0x003130DC, "call", "0x30f760"),
    (0x0030FA54, "mov", "dword ptr [rsp + 0x20], 1"),
    (0x0030FA5C, "call", "0x30f760"),
]


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and (ops is None or ins.op_str == ops)
        fails += 0 if ok else 1
        got = "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<no decode>"
        print("%s %08X %-8s %s" % ("ok  " if ok else "FAIL", va, mn, got))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
