"""render_slot_check.py - the instructions behind the render-slot consumption (ASTRA's three render packets) (OPUS, 2026-10-02). FAILS n.
Written by OPUS from the consumption notes; each line is an instruction a consumed fact rests on.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x004279FA, 'movsxd', 'rsi, dword ptr [rbx + 0x48808]'),
    (0x00427A4D, 'mov', 'word ptr [rdi], si'),
    (0x0041F754, 'call', '0x861ec0'),
    (0x0041F795, 'mov', 'word ptr [rbx], bp'),
    (0x0042915C, 'ret', ''),
    (0x00427D18, 'dec', 'dword ptr [rdi + 0x4880c]'),
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
