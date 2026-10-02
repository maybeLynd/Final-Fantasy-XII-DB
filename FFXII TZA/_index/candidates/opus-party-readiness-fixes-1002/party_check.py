"""party_check.py - the instructions behind the 11-Party readiness corrections (OPUS, 2026-10-02). FAILS n.
The slot assignment's only guard and its reset of the old slot; the 0x80-0xFE assignment band; the SetSaveData base and
map restores; the 01EED260 table; the board loop's leader-word gate; the NOT-bit-1 read; the bank end; the preset clear
size; the reserve loop that stops at index 1.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00269CDD, "test", "ebx, ebx"),
    (0x00269CE1, "mov", "qword ptr [rsi + rbx*8], rdi"),
    (0x00269CD9, "mov", "byte ptr [rcx + 0xf], 3"),
    (0x0026673E, "jns", "0x266795"),
    (0x003266D4, "add", "rdi, 0x5a48"),
    (0x00329CE1, "lea", "r14, [rip + 0x1bc3578]"),
    (0x0032113D, "je", "0x321158"),
    (0x0031711A, "mov", "ebx, 3"),
    (0x0023B1E3, "not", "ebx"),
    (0x0023B1E5, "and", "ebx, 1"),
    (0x00239C4F, "cmp", "word ptr [rbp + 0x20], r13w"),
    (0x00239C54, "jne", "0x239ce1"),
    (0x0016D6A0, "ret", "0"),
    (0x00327C63, "movsxd", "rcx, dword ptr [rdx + rax*4 + 0x7370]"),
    (0x002370CD, "mov", "r8d, 0x7410"),
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
