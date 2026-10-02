"""items_check.py - the facts behind 18-Audio readiness items 17 and 18 as settled 2026-10-02 (OPUS): 01CEBBA8 is the
float 1.0 with no writer, and 02EAD34C's one writer stores 8. Item 16 rests on UQ-242's dated answer. FAILS n.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x007AF06A, "mov", "dword ptr [rip + 0x26fe2d8], 8"),
    (0x007AECE0, "mov", "eax, dword ptr [rip + 0x26fe666]"),
]


def extra():
    import struct, subprocess
    d, off = fp.load_image()
    f = struct.unpack("<f", d[off(0x01CEBBA8):off(0x01CEBBA8) + 4])[0]
    here = os.path.dirname(os.path.abspath(__file__))
    rt = os.path.normpath(os.path.join(here, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "retool.py"))
    out1 = subprocess.run([sys.executable, "-B", rt, "refs", "01CEBBA8"], capture_output=True, text=True, cwd=os.path.dirname(rt)).stdout
    out2 = subprocess.run([sys.executable, "-B", rt, "refs", "02EAD34C"], capture_output=True, text=True, cwd=os.path.dirname(rt)).stdout
    w1 = sum(1 for l in out1.splitlines() if " W " in l)
    w2 = [l for l in out2.splitlines() if " W " in l]
    fails = 0
    for ok, label in ((f == 1.0, "01CEBBA8 = %r" % f), (w1 == 0, "01CEBBA8 writers = %d" % w1),
                      (len(w2) == 1 and "007AF06A" in w2[0], "02EAD34C writers = %d" % len(w2))):
        fails += 0 if ok else 1
        print("%s %s" % ("ok  " if ok else "FAIL", label))
    return fails


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
    fails += extra()
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
