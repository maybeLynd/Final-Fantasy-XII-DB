"""ai_check.py - the instructions behind the 09-Combat-AI readiness corrections (OPUS, 2026-10-02). FAILS n.
The order opcode is the entry's high byte (+9) and the seed is chosen by ~opcode & 1 (0x80000001 or 0x7FFFFFFF); the
AI-suspend bit returns before the 0x414D compare; enmity writes floor a positive entry at 1; an order set has room for
14 records and the rebuilders fill at most 12; the navigation gate reads order flag 0x0004; only 0x4051-0x4121 (not
0x4091) and 0x414B reach the percent roll in 00301830; the order handler table 01EEC460 has 359 entries and exactly 18
are zero.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00301B14, "movzx", "r12d, byte ptr [rdx + rdi*2 + 9]"),
    (0x00301B44, "not", "r12d"),
    (0x00301B4C, "and", "r12d, 1"),
    (0x00301BE8, "mov", "dword ptr [rsp + 0x138], 0x80000001"),
    (0x00301BF9, "mov", "dword ptr [rsp + 0x138], 0x7fffffff"),
    (0x00301511, "test", "byte ptr [rip + 0x1d87e28], 0x20"),
    (0x00301518, "jne", "0x30150a"),
    (0x00301576, "mov", "eax, 0x414d"),
    (0x003218DF, "mov", "r12d, 1"),
    (0x0032191D, "test", "ebx, ebx"),
    (0x0032191F, "jg", "0x321927"),
    (0x00321923, "cmovg", "ebx, r12d"),
    (0x00328160, "imul", "r13, rax, 0x170"),
    (0x00328187, "lea", "r15d, [r12 + 0xc]"),
    (0x00325DF4, "test", "byte ptr [rax + 4], 4"),
    (0x00301917, "cmp", "edx, 0x4050"),
    (0x0030191D, "jbe", "0x301a31"),
    (0x00301923, "cmp", "edx, 0x4091"),
    (0x0030192F, "cmp", "edx, 0x4122"),
    (0x00301A1B, "sub", "edx, 0x414b"),
    (0x00301A21, "je", "0x30193b"),
]
ZERO_IDS = [0x4025] + list(range(0x4036, 0x4046)) + [0x4128]


def extra(d, off):
    """01EEC460: 359 qword handlers for ids 0x4000-0x4166; the zero ones are exactly ZERO_IDS."""
    vals = [struct.unpack_from("<Q", d, off(0x01EEC460 + 8 * i))[0] for i in range(359)]
    zeros = [0x4000 + i for i, v in enumerate(vals) if v == 0]
    ok = zeros == ZERO_IDS
    print("%s 01EEC460 zero entries: %s" % ("ok  " if ok else "FAIL", " ".join("%04X" % z for z in zeros)))
    return 0 if ok else 1


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
    fails += extra(d, off)
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
