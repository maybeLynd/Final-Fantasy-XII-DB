"""ov21_page_count_check.py - the instructions behind the RenderResourceEntryBank +0x018 / +0x01C / +0x022 / +0x058
rows as consumed 2026-10-01 from ASTRA's ov21-page-selection-invariant and ov21-count-publication-window (OPUS).
FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    # selector 0051F7A0: signed <= 0 goes to the acquisition, and the walk starts at +0x18
    (0x0051F7AA, "cmp", "word ptr [rcx + 0x22], 0"),
    (0x0051F7B2, "jle", "0x51f825"),
    (0x0051F7E9, "mov", "edi, dword ptr [rbx + 0x18]"),
    (0x0051F81D, "mov", "edi, dword ptr [rdx + 8]"),
    (0x0051F825, "mov", "rcx, rbx"),
    (0x0051F828, "call", "0x51f6b0"),
    # append 0051F6B0: head when empty, tail read and written
    (0x0051F743, "cmp", "dword ptr [rbx + 0x18], -1"),
    (0x0051F749, "mov", "dword ptr [rbx + 0x18], eax"),
    (0x0051F74C, "movsxd", "rsi, dword ptr [rbx + 0x1c]"),
    (0x0051F782, "mov", "dword ptr [rbx + 0x1c], ecx"),
    # unlink 0051F880
    (0x0051F930, "cmp", "esi, dword ptr [rbx + 0x18]"),
    (0x0051F938, "mov", "dword ptr [rbx + 0x18], eax"),
    (0x0051F93B, "cmp", "esi, dword ptr [rbx + 0x1c]"),
    (0x0051F943, "mov", "dword ptr [rbx + 0x1c], eax"),
    # count publication order
    (0x0051FC71, "inc", "dword ptr [r14 + 0x14]"),
    (0x0051FCB2, "inc", "dword ptr [rbx + 0x58]"),
    (0x0051FD5E, "mov", "dword ptr [rax + 0x14], ecx"),
    (0x0051FE0C, "dec", "dword ptr [rdi + 0x58]"),
    # RenderStrideC0Element +0x094 producers (ASTRA's skeletonref-producer-slice)
    (0x00372914, "mov", "dword ptr [rsi + 0x94], eax"),
    (0x00372991, "add", "eax, dword ptr [rsi + 0x90]"),
    (0x003729A9, "mov", "dword ptr [rsi + 0x94], eax"),
    (0x003729BD, "call", "0x861eba"),
    (0x00371435, "mov", "dword ptr [rbx + 0x94], eax"),
    (0x00371459, "add", "eax, dword ptr [rbx + 0x90]"),
    (0x00371469, "mov", "dword ptr [rbx + 0x94], eax"),
    (0x00371487, "call", "0x3e1c50"),
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
