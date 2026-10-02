"""render_a_check.py - the instructions behind the 17-Render readiness corrections, part A (OPUS, 2026-10-02). FAILS n.
The render-record trailer store; the walked list 02B3F508; the multiplier coercion; the base += delta step.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00426493, "mov", "dword ptr [rcx + 0x48830], eax"),
    (0x003AC1C1, "mov", "r10, qword ptr [rip + 0x2793340]"),
    (0x00417AB8, "cmove", "cx, r8w"),
    (0x003E439D, "add", "word ptr [rax], cx"),
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
