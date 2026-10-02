"""spawn_check.py - the instructions behind the 05-Spawn readiness corrections (OPUS, 2026-10-02). FAILS n.
The dead-mask bit (32-bit shift, sign-extended); the operand table's getter (zero-extend) and consumer (sign-extend);
the continuous-entry match (flags & 2 and flags & 5); 0208E6A0 is the battle-unit count; the eligibility argument;
the frame counter; the native cooldown compare; the deferred completion's route; the -2 accessor; the 64-entry ledger
reset; the copy on a difference; the guard's two reset paths; the handler-0xC call sites; the height mode.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00306F74, "shl", "eax, cl"),
    (0x00306F76, "cdqe", ""),
    (0x00306F78, "or", "qword ptr [rdx + 8], rax"),
    (0x00264D3D, "movzx", "eax, word ptr [rdx + rax*2]"),
    (0x003211BD, "call", "0x264d20"),
    (0x003211C2, "movsx", "ecx, ax"),
    (0x00235413, "test", "r8b, 2"),
    (0x00235419, "test", "r8b, 5"),
    (0x002368EB, "mov", "eax, 0x20"),
    (0x002368FE, "mov", "dword ptr [rip + 0x1e57d9c], eax"),
    (0x00236914, "imul", "ecx, eax, 0xf50"),
    (0x00234DC3, "mov", "r12d, dword ptr [rsp + 0xb0]"),
    (0x0032A135, "inc", "dword ptr [rip + 0x1d63321]"),
    (0x002345CA, "call", "0x32a100"),
    (0x002358D1, "sub", "ecx, dword ptr [r14 + 0xc]"),
    (0x002358D5, "cmp", "ecx, eax"),
    (0x002358D7, "jb", "0x2359c4"),
    (0x003251A4, "call", "0x307110"),
    (0x00307133, "or", "byte ptr [rax + rcx*8], 1"),
    (0x0041DC9E, "call", "rax"),
    (0x0041DD1D, "call", "rax"),
    (0x0041CEE3, "call", "rax"),
    (0x00417CDF, "call", "rax"),
    (0x00236194, "mov", "eax, 0xfffffffe"),
    (0x00307090, "lea", "rax, [rip + 0x2bba339]"),
    (0x00307099, "lea", "rdx, [rip + 0x2bba930]"),
    (0x00235B76, "call", "0x2ef4a0"),
    (0x00233C3F, "call", "0x237df0"),
    (0x00233C48, "jmp", "0x237df0"),
    (0x00233C59, "jmp", "0x237df0"),
    (0x00239E33, "mov", "esi, 1"),
    (0x00239FA7, "mov", "ecx, esi"),
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
