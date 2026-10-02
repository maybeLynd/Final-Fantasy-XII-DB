"""thirdparty_check.py - the instructions and strings behind the 23-ThirdParty readiness corrections (OPUS, 2026-10-02).
FAILS n. The 17-byte read in the checker; the fourth return value; the ImGui context 02EA58C0; the empty-string
sentinel 02EBA2E0 / 02EBA2E1; the decoder banner and copyright strings.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0082E4CC, "mov", "r8d, 0x11"),
    (0x0016F010, "mov", "eax, 1"),
    (0x00169624, "lea", "rcx, [rip + 0x2d3c295]"),
    (0x00160167, "lea", "rdi, [rip + 0x2d5a172]"),
    (0x0016016E, "lea", "rax, [rip + 0x2d5a16c]"),
]
STRINGS = [
    (0x01CBA5D1, b"HCA Decoder (Float) Ver.2.05.00"),
    (0x01CBA610, b"\nCopyright (c) 2009-2010 CRI Middleware"),
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
    for va, want in STRINGS:
        got = bytes(d[off(va):off(va) + len(want)])
        ok = got == want
        fails += 0 if ok else 1
        print("%s %08X %r" % ("ok  " if ok else "FAIL", va, got))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
