"""gi_static_check.py - the instructions behind the GI-14 / GI-16 / GI-17 / GI-18 / GI-19 answers and the layout page's 002D45C0
correction, decoded from the shipping image (OPUS, 2026-10-01). FAILS n; refuses if any cited instruction no longer
decodes as recorded.

GI-16: the fifth move-mode state - `00558607` stores word 0x401 at +0x37C (+0x37D = 4); the switch reads +0x37D at
       00557DF0.
GI-17 / layout: 002D45C0 clears and sets bit 16 of +0xE0 from `on & 1`, asks 00244820 for the focused widget, walks the
       +0x10 chain and accepts a kind nibble only when it is not 0, 1 or 4 (test 0xFFFFFFFA, then cmp 5), then calls
       003689E0. 0027EE80 passes 0x6E to 002C9400, which compares word +0x44 of [0209AC30]+0x2B8.
GI-14: the point emitter's store at 0039DAAC and GiPrim's 00863FF9 / 00864029 decode as listed, but the reading they
       were cited for in 518a7f2d8 is withdrawn: the emitter's pointer is the object plus 8, so its +0x30 is object
       +0x38, which GiPrim hands to 001EE650. The control for that is ../opus-gi14-blend-1001/gi14_check.py
       (re-corrected 2026-10-01, OPUS).
GI-18: the gambit editor and pick list arms whose page roles were struck (ids 18, 26, 0x121, 0x8000, 0x8003,
       16, 19/20, 5; list 1, 2, 8).
GI-19: 0040DBB0 resolves twice through 0020E600 per side: [rbp+1] (rbp = sub-entry + 3, so sub-entry +0x04) and
       record +0x08 -> [obj+0]; the u16 bone index is read at 0040DC7E and scaled by 0x290; sub-entries step 0x40.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00558607, "mov", "word ptr [rbp + 0x37c], 0x401"),
    (0x00557DF0, "movzx", "ecx, byte ptr [rbp + 0x37d]"),
    (0x002D45CA, "and", "dword ptr [rcx + 0xe0], 0xfffeffff"),
    (0x002D45D6, "and", "eax, 1"),
    (0x002D45DB, "shl", "eax, 0x10"),
    (0x002D45E1, "or", "dword ptr [rcx + 0xe0], eax"),
    (0x002D45E7, "call", "0x244820"),
    (0x002D4605, "test", "dl, 8"),
    (0x002D460D, "shl", "eax, 0x1c"),
    (0x002D4610, "sar", "eax, 0x1c"),
    (0x002D4613, "test", "eax, 0xfffffffa"),
    (0x002D4618, "jne", "0x2d461f"),
    (0x002D461A, "cmp", "eax, 5"),
    (0x002D461D, "jne", "0x2d463b"),
    (0x002D4622, "mov", "rbx, qword ptr [rbx + 0x10]"),
    (0x002D4636, "call", "0x3689e0"),
    (0x0027EE84, "mov", "ecx, 0x6e"),
    (0x0027EE89, "call", "0x2c9400"),
    (0x002C9409, "mov", "rcx, qword ptr [rax + 0x2b8]"),
    (0x002C9415, "movsx", "eax, word ptr [rcx + 0x44]"),
    (0x0039DAAC, "mov", "qword ptr [rdi + 0x30], rax"),
    (0x00863FF9, "mov", "eax, dword ptr [r14 + 0x30]"),
    (0x00864029, "call", "qword ptr [rbx + 0x40]"),
    (0x0040DBE8, "lea", "rbp, [rax + 3]"),
    (0x0040DC63, "mov", "ecx, dword ptr [rbp + 1]"),
    (0x0040DC66, "call", "0x20e600"),
    (0x0040DC6B, "mov", "ecx, dword ptr [r14 + 8]"),
    (0x0040DC72, "call", "0x20e600"),
    (0x0040DC77, "mov", "ecx, dword ptr [rax]"),
    (0x0040DC79, "call", "0x20e600"),
    (0x0040DC7E, "movzx", "ecx, word ptr [rbx]"),
    (0x0040DC89, "imul", "rdx, rcx, 0x290"),
    (0x0040ECE6, "movzx", "eax, byte ptr [r13]"),
    (0x0040ECEE, "add", "rbp, 0x40"),
    # GI-18 (the gambit editor 005691E0 and pick list 0056B4D0)
    (0x00569EDC, "call", "0x568fe0"),
    (0x00569EEC, "mov", "byte ptr [rcx + 0x331], 6"),
    (0x00569242, "cmp", "byte ptr [rax + 0xdeb], 0"),
    (0x00569252, "lea", "rdx, [rbx + 0x128]"),
    (0x00569259, "call", "0x3282c0"),
    (0x0056928F, "mov", "qword ptr [rdi + rax*8], rsi"),
    (0x00569293, "mov", "qword ptr [r15 + rax*8 + 0x2b896f8], rsi"),
    (0x00569ECA, "mov", "dword ptr [rbx + 0x344], eax"),
    (0x00569E06, "call", "0x264150"),
    (0x00569E20, "or", "edx, 0xffffffff"),
    (0x00569E26, "call", "0x56a1d0"),
    (0x005695E2, "movups", "xmmword ptr [rbx + 0x128], xmm0"),
    (0x00569612, "call", "0x2d7580"),
    (0x00569751, "cmp", "byte ptr [rax + rbx + 0x177], 0"),
    (0x0056B58D, "mov", "dword ptr [rax + 0xc8], ebp"),
    (0x0056ACBB, "mov", "dword ptr [rdi + 0x580], 0xb4"),
    (0x0056BA04, "call", "0x247510"),
    (0x0056B7FC, "call", "0x2d45c0"),
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
