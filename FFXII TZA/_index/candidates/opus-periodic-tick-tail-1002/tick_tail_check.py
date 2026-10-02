"""tick_tail_check.py - the instructions behind the periodic tick 00310DB0's tail and gate structure as documented
2026-10-02 (OPUS). FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00310E41, "movzx", "eax, byte ptr [rcx + 5]"),
    (0x00310E51, "sub", "al, 0x1b"),
    (0x00310E53, "cmp", "al, 0xc"),
    (0x00310E5B, "cmp", "dword ptr [rcx + 0x48], 0"),
    (0x00310EF8, "call", "0x3138d0"),
    (0x00310EFD, "jmp", "0x3112c1"),
    (0x00310F12, "call", "0x265680"),
    (0x00310F19, "je", "0x3112a1"),
    (0x00310FAC, "call", "0x3112f0"),
    (0x00310FC9, "call", "0x2f8060"),
    (0x003110C3, "call", "0x2f9400"),
    (0x003110D7, "call", "0x300ce0"),
    (0x00311114, "mov", "rcx, qword ptr [rsi + 0x698]"),
    (0x0031111B, "call", "0x469e30"),
    (0x003112A4, "call", "0x321530"),
    (0x003112AC, "call", "0x2fe950"),
    (0x0031983B, "lea", "rax, [rip + 0x2ba775e]"),
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
