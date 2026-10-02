"""ui_check.py - the instructions behind the 16-UI readiness corrections (OPUS, 2026-10-02). FAILS n.
The widget bit-10 set; the constructor's bit-14 re-set; the half-rate predicate; the 0xD81 mask that kills the
26-unit branch; the 0x7F byte mask; the +0x570 bit-1 test; the bit-0 test in 00244DD0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00245097, "bts", "eax, 0xa"),
    (0x002466F2, "or", "dword ptr [rdi + 0x40], eax"),
    (0x001EDEDA, "not", "ecx"),
    (0x00254A1E, "mov", "ecx, 0xd81"),
    (0x003FFACA, "and", "r8b, 0x7f"),
    (0x0055A186, "test", "byte ptr [rcx + 0x570], 2"),
    (0x00244E1A, "test", "dl, 1"),
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
