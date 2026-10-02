"""story_check.py - the instructions behind OPUS's 14-Story byte verdicts (OPUS, 2026-10-02). FAILS n.
Bank512's two accessor pairs over one region; the Primary gate's size and offset; the Primary setter's 2..0x1FF guard;
SetBank64A's signed-only guard and truncating index; the treasure chest's flag-before-draw and its two pairs; the trap
record's widths; 002628B0's zero store to +0x1534; the gate's thunk.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0032AAAB, "test", "byte ptr [rax + rdi + 0x14b4], dl"),
    (0x0032AAE7, "lea", "eax, [rcx + 0x100]"),
    (0x0032AB1F, "test", "byte ptr [rax + rdi + 0x14b4], dl"),
    (0x0032ADB6, "or", "byte ptr [rax + rcx + 0x14b4], bl"),
    (0x0032AE04, "lea", "eax, [rcx + 0x100]"),
    (0x0032AE3A, "or", "byte ptr [rax + rcx + 0x14b4], bl"),
    (0x0032A900, "test", "byte ptr [rax + rbx + 0x14f4], dl"),
    (0x0032A919, "ret", ""),
    (0x0032A920, "jmp", "0x32a8a0"),
    (0x0032AB64, "lea", "eax, [rcx - 2]"),
    (0x0032AB6A, "cmp", "eax, 0x1fd"),
    (0x0032AC77, "cmp", "ecx, 0x40"),
    (0x0032AC7A, "jge", "0x32acdf"),
    (0x0032AC9A, "sar", "edi, 3"),
    (0x0032AC9F, "shl", "bl, cl"),
    (0x002FAFFD, "call", "0x32ad70"),
    (0x002FB01D, "call", "0x379cd0"),
    (0x002FB0ED, "cmp", "esi, 0x5f"),
    (0x002FB0FE, "cmp", "esi, 0x32"),
    (0x002F8218, "call", "0x379cd0"),
    (0x002F8231, "cmp", "r8d, 0x4b"),
    (0x002F8253, "call", "0x32ad70"),
    (0x002FA7E8, "movzx", "eax, byte ptr [rdi + 4]"),
    (0x002FA81E, "movsx", "eax, word ptr [rdi + 2]"),
    (0x0026292A, "xor", "ebp, ebp"),
    (0x00262A76, "mov", "byte ptr [rax + 0x1534], bpl"),
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
