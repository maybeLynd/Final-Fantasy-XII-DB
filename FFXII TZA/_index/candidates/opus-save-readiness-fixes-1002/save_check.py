"""save_check.py - the instructions behind the 19-Save-Load readiness corrections (OPUS, 2026-10-02). FAILS n.
0020E540 forwards to the ret-0 stub 0016D6A0 (not a writer); 002EF640 is a getter; the checksum flow (00583F99 stores
crc at +0xE200, 00583FA1 stores ~crc at [dest], the finaliser returns crc); the queue start gate sets bit 0; the
load-time stash copies five dwords; 001F3EA0 checks the directory then creates it.
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0016D6A0, "ret", "0"),
    (0x002EF640, "lea", "rax, [rip + 0x1e74c39]"),
    (0x002EF647, "ret", ""),
    (0x00583F99, "mov", "dword ptr [rdi + 0xe200], eax"),
    (0x00583F9F, "not", "ecx"),
    (0x00583FA1, "mov", "dword ptr [rdi], ecx"),
    (0x005820BD, "or", "dword ptr [rbx + 0xdc], 1"),
    (0x0058427B, "mov", "eax, dword ptr [rbx + 0x1244]"),
    (0x00584281, "mov", "dword ptr [rbx + 0x80], eax"),
    (0x001F3EAB, "call", "qword ptr [rip + 0x6cec6f]"),
    (0x001F3EB1, "cmp", "eax, -1"),
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
