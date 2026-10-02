"""scriptvm_check.py - the instructions behind the 01-Script-VM readiness corrections (OPUS, 2026-10-02). FAILS n.
The interpreter's default-arm stop request; the system-stop request start; the family-table fill; the phase byte's two
writers; the 12-bit command mask; the read-in machine's stores; the 0x740 render base.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0025E555, "mov", "ebp, 1"),
    (0x00226C7A, "or", "dword ptr [rip + 0x1dada53], r13d"),
    (0x003DC2D5, "lea", "rax, [rip + 0x1b4a444]"),
    (0x0026230B, "mov", "byte ptr [rdi + 0x15], 1"),
    (0x0026220C, "and", "r15d, 0xfff"),
    (0x0037CEBB, "mov", "byte ptr [rbx + 0xa], 0"),
    (0x00261B97, "mov", "word ptr [rsi + 0x14], 0x107"),
    (0x002E944B, "inc", "dword ptr [rbx + 0x24]"),
    (0x002E949A, "cmp", "dword ptr [rdx + 0x24], eax"),
    (0x00266B54, "lea", "rax, [rdx + 0x120]"),
    (0x0034FE99, "jmp", "0x37ca00"),
    (0x003DBDD4, "movsx", "rax, byte ptr [rcx + 0x11]"),
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
