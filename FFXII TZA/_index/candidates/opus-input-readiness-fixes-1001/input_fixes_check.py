"""input_fixes_check.py - the instructions behind the six 15-Input corrections, decoded from the shipping image
(OPUS, 2026-10-01). FAILS n; refuses if any cited instruction no longer decodes as recorded.

001965E0: r11 loaded once with 01F80F94 and never written in the loop, so profile 1 is scanned three times.
00196290: three 0x15C copies 01F80130/01F8028C/01F803E8 -> 01DF1738/01DF1894/01DF19F0; r8d = 2 is the round count.
00196FF0: the poll walks five 0x15C records from 01DF1480 (records 1 and 2 are 01DF15DC and 01DF1738).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x001965E5, "mov", "r9d, 3"),
    (0x001965EB, "lea", "r11, [rip + 0x1dea9a2]"),
    (0x00196600, "xor", "edx, edx"),
    (0x00196602, "mov", "rax, r11"),
    (0x0019666E, "sub", "r9, rbx"),
    (0x00196671, "jne", "0x196600"),
    (0x00196290, "mov", "r8d, 2"),
    (0x00196296, "lea", "rcx, [rip + 0x1c5b49b]"),
    (0x001962A0, "lea", "rdx, [rip + 0x1de9e89]"),
    (0x00196334, "lea", "rdx, [rip + 0x1de9f51]"),
    (0x0019633E, "lea", "rcx, [rip + 0x1c5b54f]"),
    (0x001963D4, "lea", "rdx, [rip + 0x1c5b615]"),
    (0x001963DE, "lea", "rax, [rip + 0x1dea003]"),
    (0x00197089, "lea", "rsi, [rip + 0x1c5a3f0]"),
    (0x001970A9, "lea", "r14d, [rax + 5]"),
    (0x001970BB, "add", "rsi, 0x15c"),
]
# rip-relative targets, recomputed from the decoded instruction (next address + displacement)
TARGETS = {0x001965EB: 0x01F80F94, 0x00196296: 0x01DF1738, 0x001962A0: 0x01F80130, 0x00196334: 0x01F8028C,
           0x0019633E: 0x01DF1894, 0x001963D4: 0x01DF19F0, 0x001963DE: 0x01F803E8, 0x00197089: 0x01DF1480}


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and ins.op_str == ops
        if ok and va in TARGETS:
            disp = int(ops.split("+ ")[1].rstrip("]"), 16)
            ok = va + ins.size + disp == TARGETS[va]
        fails += 0 if ok else 1
        got = "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<no decode>"
        tgt = " -> %08X" % TARGETS[va] if va in TARGETS else ""
        print("%s %08X %s%s" % ("ok  " if ok else "FAIL", va, got, tgt))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
