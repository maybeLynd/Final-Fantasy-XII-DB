"""rig_check.py - the instructions behind OPUS's consumption of ASTRA's two rig packages (OPUS, 2026-10-02). FAILS n.
003E1C50's conditional +0x70/+0x78 refresh and its unguarded lookup on a missing or inactive owner; 00421D20's first
read; the secondary skip on full DWORD +0x6C == -1 and the rebind 003E3CA0's unguarded secondary lookup; the signed16
+0x6C writer; the rig's raw +0x84 self cache; 003E3C30's unsigned count and index loop.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x003E1C66, "mov", "ecx, dword ptr [rcx + 0x70]"),
    (0x003E1C78, "je", "0x3e1cc6"),
    (0x003E1C7E, "cmp", "ax, -1"),
    (0x003E1C84, "mov", "ecx, ebx"),
    (0x003E1CA0, "cmove", "rcx, rbx"),
    (0x003E1CB6, "call", "0x421d20"),
    (0x003E1CC3, "mov", "dword ptr [rdi + 0x78], eax"),
    (0x003E1CD3, "cmp", "dword ptr [rdi + 0x6c], -1"),
    (0x003E1D1B, "mov", "dword ptr [rdi + 0x6c], 0xffffffff"),
    (0x003E1D49, "mov", "eax, dword ptr [rdi + 0x84]"),
    (0x003E1D4F, "cmp", "eax, edi"),
    (0x003E27EA, "mov", "dword ptr [rdi + 0x84], edi"),
    (0x00421D26, "mov", "ebx, dword ptr [rcx + 0x18]"),
    (0x00421D29, "cmp", "ebx, -1"),
    (0x003E3D01, "cmp", "dword ptr [rbx + 0x6c], -1"),
    (0x003E3D2D, "cmove", "rdx, rdi"),
    (0x003E3D49, "call", "0x421d20"),
    (0x003E3E18, "call", "0x421d20"),
    (0x004216D3, "movsx", "ebx, word ptr [rsi]"),
    (0x004216DB, "mov", "dword ptr [rax + 0x6c], ebx"),
    (0x003E3C42, "mov", "ecx, dword ptr [rcx + 0x88]"),
    (0x003E3C52, "cmp", "dword ptr [rsi + 0x8c], edi"),
    (0x003E3C58, "jbe", "0x3e3c8d"),
    (0x003E3C68, "mov", "ecx, dword ptr [rbx]"),
    (0x003E3C6A, "add", "rax, 0x230"),
    (0x003E3C70, "imul", "rcx, rcx, 0x290"),
    (0x003E3C7A, "call", "0x203170"),
    (0x003E3C8B, "jb", "0x3e3c60"),
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
