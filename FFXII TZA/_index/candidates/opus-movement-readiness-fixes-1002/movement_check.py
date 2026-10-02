"""movement_check.py - the instructions behind the 06-Movement readiness corrections (OPUS, 2026-10-02). FAILS n.
The angle wraps (closed loops, the large-angle truncation, the biased truncating fmod); the steering commit (flag 0
writes the previous lanes, 004288B0 then 003B3CA0, the +6 reset); the turn-mode setter's arms; the order-goal decoder's
ranges and the 0x4020 / 0x4125 references; the stall thresholds; the arrival clamp; the turn limiter's latch; the
separation weight and query out; the per-fifty scale; the pool and cell globals; the time base; flag B's stores; the
nav header stride and portal bytes; the capsule out-vector; the pitch delta; the stop-and-turn chain; the 3-D default.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x003A1C65, "addss", "xmm0, xmm2"),
    (0x003A1C83, "addss", "xmm0, xmm2"),
    (0x0033CB73, "comiss", "xmm2, dword ptr [rip + 0x9d3f92]"),
    (0x0033CBE8, "subss", "xmm2, xmm0"),
    (0x0026B5B7, "jb", "0x26b5c3"),
    (0x0026A916, "cvttss2si", "eax, xmm0"),
    (0x003EC340, "movss", "dword ptr [rbx + 0x250], xmm1"),
    (0x003EC362, "cmp", "dword ptr [rsp + 0x50], ecx"),
    (0x003EC39E, "call", "0x4288b0"),
    (0x003EC3BC, "jmp", "0x3b3ca0"),
    (0x003EC2C1, "cmp", "word ptr [rbx + 6], -1"),
    (0x0026C16A, "jle", "0x26c1e6"),
    (0x0026C224, "mov", "dword ptr [rax + 0x58], 0x3e20d97c"),
    (0x0026C161, "jle", "0x26c272"),
    (0x0026C26D, "call", "0x2e6300"),
    (0x00312780, "cmp", "ebx, 0x4035"),
    (0x0031279E, "cmp", "ecx, 0x24"),
    (0x003127F1, "mov", "rcx, qword ptr [rdi + 0x6a0]"),
    (0x00312A57, "mov", "r8d, 0x14"),
    (0x0033C2B7, "subss", "xmm1, dword ptr [rip + 0x5b6e25]"),
    (0x0033C2E7, "cmp", "al, 0x3c"),
    (0x00339DBB, "ja", "0x339dc4"),
    (0x0033659D, "movzx", "ecx, byte ptr [rdx + 0x21]"),
    (0x00315377, "movss", "dword ptr [r15], xmm4"),
    (0x00314E27, "divss", "xmm0, xmm1"),
    (0x003DAF68, "movss", "xmm2, dword ptr [rip + 0x5181c0]"),
    (0x001EDDF2, "mov", "dword ptr [rip + 0x1c102b8], 2"),
    (0x003B7306, "xor", "ebx, ebx"),
    (0x00383883, "movzx", "r10d, word ptr [r11 + 0xa]"),
    (0x003838C4, "test", "byte ptr [rax + rdi*8 + 6], r8b"),
    (0x003DA663, "movss", "dword ptr [r14 + 0xc], xmm0"),
    (0x003A1A24, "call", "0x861f14"),
    (0x0033A06E, "call", "0x33ce60"),
    (0x00426493, "mov", "dword ptr [rcx + 0x48830], eax"),
    (0x002E596B, "call", "0x2654e0"),
    (0x002E274A, "test", "byte ptr [rax + 0x14f], 1"),
    (0x00269345, "divss", "xmm0, dword ptr [rcx + 0x58]"),
    (0x003019BF, "lea", "rcx, [rsp + 0x30]"),
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
