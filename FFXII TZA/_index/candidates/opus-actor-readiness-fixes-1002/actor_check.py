"""actor_check.py - the instructions behind the 04-Actor readiness corrections (OPUS, 2026-10-02). FAILS n.
The record's +0x03 packing; the region map's 0xC8 / 0xA0 select on the sub flag; the slot-index store; the initialiser's
+0x1C mask and +0xC8 override fill; the +0x08 rewrites; the manager range start and count; the bits 8/13 read; the
manager slot stride; side A's two index tests; the rate setter's entry store; the separate binds; the 02ADD980 table;
the 02EBF1A0 global; the unit-slot bound; the field clears and sets; the zero-extended sign test.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00267B0E, "shl", "al, 5"),
    (0x00266B83, "cmp", "byte ptr [r9 + rax*4 + 0x1cec329], 1"),
    (0x00266B8C, "mov", "eax, 0xc8"),
    (0x00266B93, "mov", "eax, 0xa0"),
    (0x002665EB, "mov", "word ptr [rbx], r10w"),
    (0x002666F1, "and", "dword ptr [rbx + 0x1c], 0xffffdeff"),
    (0x002668A0, "lea", "rdi, [rbx + 0xc8]"),
    (0x002668B0, "rep stosw", "word ptr [rdi], ax"),
    (0x00266607, "and", "dl, 0xdf"),
    (0x0026667A, "and", "byte ptr [rbx + 8], 0x7f"),
    (0x00225D36, "movzx", "ebp, word ptr [rax + 0x1de]"),
    (0x00225D45, "add", "r14d, ebp"),
    (0x003DF73A, "test", "dword ptr [rbx + 0x1c], 0x2100"),
    (0x002630AB, "imul", "r14, rax, 0x288"),
    (0x003DA42E, "js", "0x3da4c3"),
    (0x003DA438, "jae", "0x3da4c3"),
    (0x003DD1F3, "add", "rax, 0x10"),
    (0x0037DCFA, "lea", "rax, [rip + 0x275fc7f]"),
    (0x002369E5, "lea", "rdi, [rip + 0x2c887b4]"),
    (0x002368FE, "mov", "dword ptr [rip + 0x1e57d9c], eax"),
    (0x00234503, "and", "dword ptr [rbx], 0xffdfffff"),
    (0x0023611F, "movzx", "eax, dl"),
    (0x005C5230, "xor", "eax, eax"),
    (0x0030C4B1, "mov", "byte ptr [rcx + 0x88], r8b"),
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
