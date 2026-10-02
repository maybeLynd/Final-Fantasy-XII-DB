"""action_check.py - the instructions behind the 07-Combat-Action readiness corrections (OPUS, 2026-10-02). FAILS n.
The commit's band split and its skipped attacker mask; the kind-1 latch; the combo record's two tables and the
stats byte +4 index; the stack target buffers and the +0x01 reader; the 64-entry queue drained eight at a time; the
32-entry arrays; the +0x38 dword test; the stand window's frame-rate word; the knockback writer; the script verb that
fills the buffer; the parked slot byte.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0030F7A5, "ja", "0x30f7d9"),
    (0x0030F849, "cmp", "ecx, 1"),
    (0x0030F8B6, "ja", "0x30f97a"),
    (0x0030F975, "call", "0x313b30"),
    (0x0030F97A, "mov", "eax, 1"),
    (0x0038869F, "movzx", "eax, byte ptr [rsi + 5]"),
    (0x003886A7, "movzx", "edi, byte ptr [rsi + 4]"),
    (0x00308813, "movzx", "edx, byte ptr [rsi + 1]"),
    (0x00313CF7, "mov", "edi, 8"),
    (0x00313D18, "and", "cl, 0x3f"),
    (0x00384925, "lea", "edx, [r8 + 0x21]"),
    (0x0031148D, "cmp", "dword ptr [rbx + 0x38], -1"),
    (0x00311493, "movzx", "ecx, word ptr [rbx + 0x38]"),
    (0x0031137A, "call", "0x385ba0"),
    (0x00337B75, "imul", "ecx, dword ptr [rip + 0x1ac6538], 0x1e"),
    (0x003075CB, "or", "dword ptr [r14 + 8], 0x100"),
    (0x003495B2, "call", "0x313120"),
    (0x0031325F, "call", "0x316cf0"),
    (0x0031328C, "call", "0x316cd0"),
    (0x00311DA5, "mov", "byte ptr [rax + rcx*4], bpl"),
    (0x00385756, "movzx", "ecx, byte ptr [rax + 0x6b9]"),
    (0x00469894, "mov", "edx, 6"),
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
