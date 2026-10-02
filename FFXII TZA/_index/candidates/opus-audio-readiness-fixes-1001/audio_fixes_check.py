"""audio_fixes_check.py - the instructions and table entries behind the 18-Audio corrections, read from the shipping
image (OPUS, 2026-10-01). Each check is (address, mnemonic, a substring the operands must contain). FAILS n.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    # item 1: the second gate - a zero goes to the work, a non-zero falls through to xor eax, eax
    (0x002DF236, "cmp", "ecx, -1"), (0x002DF23B, "call", "0x3603c0"), (0x002DF240, "test", "eax, eax"),
    (0x002DF242, "je", "0x2df256"), (0x002DF244, "xor", "eax, eax"),
    # item 2: the boot bank setup writes -1 to A twice and to C once
    (0x003A14BE, "mov", "0xffffffff"), (0x003A153D, "mov", "0xffffffff"), (0x003A15BC, "mov", "0xffffffff"),
    # item 3: 002DF010 passes r9d = 0x7F and r8d = 0x40
    (0x002DF02B, "mov", "r9d, 0x7f"), (0x002DF03F, "lea", "r8d, [r9 - 0x3f]"),
    # item 4: 00360C20 returns byte +0; 00360C70 stores the index at +3
    (0x00360C66, "movzx", "eax, byte ptr [r10 + rcx*8]"), (0x00360C90, "mov", "byte ptr [rax + 3], cl"),
    # item 5: 003A0E20's argument order
    (0x003A0E30, "movzx", "edx, cl"), (0x003A0E36, "shr", "ecx, 8"), (0x003A0E3C, "movzx", "ecx, cl"),
    # item 7: the gate is raised in state 10; +0xD4 == 0x42 gates the teardown call
    (0x0027F646, "mov", "ecx, dword ptr [rbx + 0xc0]"), (0x0027F67B, "call", "0x249fc0"),
    (0x0027F629, "cmp", "0x42"), (0x0027F632, "call", "0x2d6f90"), (0x002D6FD4, "call", "0x249fc0"),
    # item 8: the controller constructs its member at +0x20 through the pool template
    (0x00217FE6, "call", "0x212710"),
    # item 9: the broadcast reloads the vtable inside the loop
    (0x00222580, "mov", "rax, qword ptr [rdi]"), (0x00222596, "jne", "0x222580"),
    # item 10: six command bits
    (0x00222C8F, "test", "+ 0x3c], 1"), (0x0022356E, "test", "dil, 2"), (0x00225466, "test", "+ 0x3c], 4"),
    (0x00223596, "test", "dil, 8"), (0x002235AA, "test", "dil, 0x10"), (0x002235BE, "test", "dil, 0x20"),
    # item 11: 002130E0 installs 00906DC8; 00212710 installs 00906CD0
    (0x002130E0, "lea", "rax, [rip"), (0x00212726, "lea", "[rip"),
    # item 12: the lazy object is cached at +0x20; slot 8 tests +0x50
    (0x00221D16, "mov", "rax, qword ptr [rcx + 0x20]"), (0x00221D47, "mov", "qword ptr [rdi + 0x20], rbx"),
    (0x00222F26, "cmp", "qword ptr [rcx + 0x50], 0"), (0x00222F3A, "call", "0x221d10"),
    # item 33: the .sab +0x0A reader
    (0x007EE01D, "movzx", "ebx, word ptr [rcx + 0xa]"), (0x007EE02B, "cmp", "bx, 1"),
    # item 20: r8 (0x40) feeds the pan setter, r9 (0x7F) the volume setter
    (0x002252DA, "mov", "ebp, r8d"), (0x002252E5, "mov", "esi, r9d"), (0x00225367, "mov", "edx, ebp"),
    (0x0022536C, "call", "0x2256f0"), (0x00225374, "mov", "edx, esi"), (0x00225379, "call", "0x2257e0"),
    (0x00225750, "lea", "edi, [rsi - 0x40]"), (0x0022581F, "divss", "xmm1"),
    # item 23: the musicinfo pointer
    (0x00361014, "mov", "rdx, qword ptr [rip"),
    # item 26: dt from an unsigned QPC difference, passed through 007AAEA0
    (0x007AAECD, "movaps", "xmm8, xmm0"), (0x007AB030, "movaps", "xmm1, xmm8"), (0x007AB037, "call", "0x7aa770"),
    # item 27: out-of-range exit and arm 0
    (0x007A9E5A, "ja", "0x7a9f14"), (0x007A9F14, "xorps", "xmm0, xmm0"),
    # item 28: the ramp record's duration and target reads
    (0x007BFF11, "movss", "+ 0x25c]"), (0x007BFF1F, "movss", "+ 0x254]"),
    # item 29: the weight-byte test
    (0x007CF83C, "cmp", "byte ptr [rax + 4], 0"), (0x007CF849, "cmp", "byte ptr [rax + 0x10], 0"),
    # item 31: the presentation PRNG reads its mode and state
    (0x003A6E60, "mov", "[rip"),
]
RIP_TARGETS_EXTRA = {0x00361014: 0x022CBA50}
CSV_VTABLE, CSV_LAST = 0x01CB8360, 0x007E26B0
RIP_TARGETS = {0x002130E0: 0x00906DC8, 0x00212726: 0x00906CD0}
# item 15: AmbientSound vs SoundSourceObject vtable slots (own bodies 0, 34, 35; slot 7 inherited)
VT_AMBIENT, VT_SSO = 0x01CB9C88, 0x01CB98A8
SLOTS_DIFFER = [0, 1, 34, 35, 39]
SLOT7_SHARED = 0x007F0210


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, frag in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and frag in ins.op_str
        tgt = RIP_TARGETS.get(va) or RIP_TARGETS_EXTRA.get(va)
        if ok and tgt:
            disp = int(ins.op_str.split("rip + ")[1].split("]")[0], 16)
            ok = va + ins.size + disp == tgt
        fails += 0 if ok else 1
        print("%s %08X %s" % ("ok  " if ok else "FAIL", va, "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<none>"))
    q = lambda a: struct.unpack("<Q", d[off(a):off(a) + 8])[0]
    amb = [q(VT_AMBIENT + 8 * i) for i in range(40)]
    sso = [q(VT_SSO + 8 * i) for i in range(40)]
    differ = [i for i in range(40) if amb[i] != sso[i]]
    ok = differ == SLOTS_DIFFER and amb[7] == sso[7] == SLOT7_SHARED
    fails += 0 if ok else 1
    print("%s vtables: Ambient differs from SoundSourceObject at %s; slot 7 both %08X" % ("ok  " if ok else "FAIL", differ, amb[7]))
    # item 36: CoreSourceVoice has 17 code slots, 0-16; slot 17 is not a .text pointer
    s16, s17 = q(CSV_VTABLE + 8 * 16), q(CSV_VTABLE + 8 * 17)
    ok = s16 == CSV_LAST and not (0x00121000 <= s17 < 0x00A00000)
    fails += 0 if ok else 1
    print("%s CoreSourceVoice slot 16 %08X, slot 17 %X (not code)" % ("ok  " if ok else "FAIL", s16, s17))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
