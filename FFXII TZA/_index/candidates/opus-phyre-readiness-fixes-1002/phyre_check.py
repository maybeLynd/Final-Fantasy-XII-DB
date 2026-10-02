"""phyre_check.py - the instructions behind the 22-Phyre readiness corrections (OPUS, 2026-10-02). FAILS n.
The slot-7-before-slot-4 order; the AND-mask flag clear; the offset test; the running +0xF4 sum; PFXAA built in code;
the slot-4 tick's returns; the bool return of 006388C0; the descriptor destructor's vtable stamps.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0079C26B, "call", "qword ptr [rax + 0x38]"),
    (0x003A20B0, "and", "dword ptr [rax], 0x8000"),
    (0x001E3619, "cmp", "r9w, 4"),
    (0x0063E43B, "add", "dword ptr [rdx + 0xf4], ecx"),
    (0x0018CFD5, "call", "0x645db0"),
    (0x0079C2D6, "call", "qword ptr [rax + 0x20]"),
    (0x006389A1, "sete", "al"),
    (0x0017CDB2, "mov", "eax, 9"),
    (0x006333BC, "mov", "qword ptr [rcx], rax"),
    (0x00633568, "mov", "qword ptr [r15], rax"),
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
