"""status_check.py - the instructions behind the 10-Status readiness corrections (OPUS, 2026-10-02). FAILS n.
Items: 1 (status 28 halves HP and the applier fires), 2/4 (the evaluation context merges +0x68/+0x78 and takes the
target's status words), 5 (stage 3's slot table is 02EBF040), 8 (stage 5's base is MP's 0208D480 + 0x14), 13 (mode
0..5), 15 (002373C0 sets 0x800 only), 16 (11 stored), 23 (r14 zeroed), 38 (0030E816 is the recompute tail), and the
two image findings (stage 5 overwrites +0x24; the 0x14 fallback is a raw pointer).
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00386A94, "cmp", "ebx, 0x1c"),
    (0x00386AAE, "sar", "eax, 1"),
    (0x00386AB0, "mov", "dword ptr [rdi + 0x24], eax"),
    (0x0030E610, "test", "byte ptr [rsp + 0xac], bpl"),
    (0x0030E638, "call", "0x3112f0"),
    (0x00384827, "test", "byte ptr [r9 + r11 + 0x68], dl"),
    (0x00384831, "test", "byte ptr [r9 + r11 + 0x78], dl"),
    (0x0038484C, "or", "byte ptr [r9 + rbx + 0x1a], r8b"),
    (0x003855FD, "mov", "r8, qword ptr [rip + 0x2b39a3c]"),
    (0x00385604, "movzx", "ecx, word ptr [r8 + 8]"),
    (0x00386885, "lea", "rax, [rip + 0x1d06c08]"),
    (0x002F9439, "lea", "rax, [rip + 0x1d94040]"),
    (0x0030E4CB, "cmp", "eax, 5"),
    (0x003010C5, "call", "0x2373c0"),
    (0x003010CE, "or", "dword ptr [rip + 0x1d88268], 0x800"),
    (0x003010D8, "call", "0x3272e0"),
    (0x00387746, "mov", "eax, 0xb"),
    (0x0030FF07, "xor", "r14d, r14d"),
    (0x0030E816, "mov", "eax, dword ptr [rsp + 0x228]"),
    (0x0030E828, "call", "0x30fed0"),
    (0x00386A23, "mov", "dword ptr [r13 + 0x24], edx"),
    (0x003868BD, "mov", "ebx, 0x14"),
    (0x003868C2, "test", "rbx, rbx"),
    (0x00386E84, "mov", "word ptr [r15], ax"),
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
