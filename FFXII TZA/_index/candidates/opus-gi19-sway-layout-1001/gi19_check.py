"""gi19_check.py - the instructions behind GI-19's answer (OPUS, 2026-10-01). FAILS n.

- 003E1C50 calls 0040EEA0(rig, S) for slot 0 and then sets S+0x08 = encode(&rig+0x78);
- rig+0x78 = encode(00421D20(render record)), and 00421D20 returns the resource entry's +0x84;
- 0040EEA0 relocates S+0x00, E+0x08 and A+0x04 against S;
- 0040DBB0 reads S+0x08 -> rig+0x78 -> bone array, and the "second 4x4" comes from bone row +0x150..+0x180.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x003E1D97, "lea", "edx, [rdi + rax]"),
    (0x003E1D9A, "call", "0x40eea0"),
    (0x003E1D9F, "lea", "rcx, [rdi + 0x78]"),
    (0x003E1DB5, "mov", "dword ptr [rax + 8], ebx"),
    (0x003E1CB6, "call", "0x421d20"),
    (0x003E1CC3, "mov", "dword ptr [rdi + 0x78], eax"),
    (0x00421D26, "mov", "ebx, dword ptr [rcx + 0x18]"),
    (0x00421D3B, "mov", "rcx, qword ptr [rax + 0xd98]"),
    (0x00421D44, "call", "0x2ed570"),
    (0x00421D4E, "mov", "ecx, dword ptr [rax + 0x84]"),
    (0x0040EEAE, "mov", "rdi, rdx"),
    (0x0040EEC2, "lea", "ecx, [rdi + rax]"),
    (0x0040EECC, "mov", "dword ptr [rdi], eax"),
    (0x0040EEF2, "lea", "r14, [rax + 8]"),
    (0x0040EF0C, "lea", "ecx, [rdi + rax]"),
    (0x0040EF16, "mov", "dword ptr [r14], eax"),
    (0x0040EF39, "lea", "ecx, [rdi + rax]"),
    (0x0040EF45, "mov", "dword ptr [r15 - 0x1c], eax"),
    (0x0040DC63, "mov", "ecx, dword ptr [rbp + 1]"),
    (0x0040DC6B, "mov", "ecx, dword ptr [r14 + 8]"),
    (0x0040DD9D, "mov", "ecx, dword ptr [r14 + 8]"),
    (0x0040DDAD, "movzx", "ecx, word ptr [rbx - 8]"),
    (0x0040DDB5, "imul", "rdi, rcx, 0x290"),
    (0x0040DDC5, "add", "rdi, rax"),
    (0x0040DE9E, "movups", "xmm0, xmmword ptr [rdi + 0x150]"),
    (0x0040DEE5, "movups", "xmm0, xmmword ptr [rdi + 0x180]"),
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
