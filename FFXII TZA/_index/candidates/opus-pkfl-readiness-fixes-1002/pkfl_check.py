"""pkfl_check.py - the instructions behind the 26-PKFL readiness corrections (OPUS, 2026-10-02). FAILS n.
Byte 0 is read by every slot reader; the slot's second dword is its size; the four completions each clear their own
bit (13 .mot, 12 .snd, 15 .vpc, 14 .vpcjp).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0032F273, "cmp", "byte ptr [rcx], 0"),
    (0x0032F38E, "mov", "eax, dword ptr [rcx + rax*8 + 0xc]"),
    (0x003302D0, "btr", "rbx, 0xd"),
    (0x00331780, "btr", "rbx, 0xc"),
    (0x00331840, "btr", "rbx, 0xf"),
    (0x003317E0, "btr", "rbx, 0xe"),
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
