"""gi15_check.py - the instructions behind the GI-15 answers and the four cross-page corrections, decoded from the
shipping image (OPUS, 2026-10-01). FAILS n; refuses if any cited instruction no longer decodes as recorded.

- 003737C0 takes a record when flags bit 8 is SET; 00409250 returns link bits 0-11 when flags bit 30 is clear.
- 0x3F (00520510): +0x14 = word[cmd+2], +0x16 = word[cmd+0x10] & 0xFFF, +0x18 = word[cmd+0x10] >> 15, +0x16 zeroed when
  word[cmd+2] == 0xFFFF. 0x48 (005205B0): +0x14 = 00372800's result, +0x16 / +0x18 from word[cmd+2].
- 00520E90 passes +0x16 as the preset (edx) and +0x14 as the bone (r9) to 0040ABF0, which stores +0x3E / +0x3C;
  0040FF30 reads the bone at +0x3C and scales it by 0x290.
- the priority map is 01F00410 (00423790 and 00422DE0).
- 003E7210 reads FCP section 5: [record + 0x400] + 0x0A.
- 004218A0 / 004219C0: the no-key path sets bit 26 and +0x2F2 = 1, then both paths test bit 26; 004219C0 retries 0x1E.
- 0x34 arm 0x01 stores the float in the n <= 1 path and uses it as the ramp target otherwise.
- the camera-shake gate 02B4D7A2 in 003D7FF0; verb 0x4A0's handler 003517C0 tail-jumps to 002EA880.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x0037382D, "test", "dword ptr [rsi + 4], 0x100"),
    (0x00373834, "jne", "0x37383f"),
    (0x00409250, "test", "dword ptr [rcx + 4], 0x40000000"),
    (0x0040925E, "mov", "eax, dword ptr [rcx]"),
    (0x00409260, "and", "eax, 0xfff"),
    (0x00520528, "movzx", "ecx, word ptr [r8 + 0x10]"),
    (0x00520533, "movzx", "edx, word ptr [rdx + 2]"),
    (0x00520542, "mov", "word ptr [rsp + 0x36], ax"),
    (0x00520556, "mov", "word ptr [rsp + 0x34], dx"),
    (0x0052055B, "mov", "word ptr [rsp + 0x38], cx"),
    (0x00520560, "cmp", "dx, ax"),
    (0x00520567, "mov", "word ptr [rsp + 0x36], ax"),
    (0x00520630, "call", "0x372800"),
    (0x00520635, "movzx", "edx, word ptr [rbp + 2]"),
    (0x00520642, "mov", "word ptr [rsp + 0x34], ax"),
    (0x0052064F, "mov", "word ptr [rsp + 0x36], cx"),
    (0x00520663, "mov", "word ptr [rsp + 0x36], bx"),
    (0x00520FA2, "movzx", "edi, word ptr [r14 + 0x14]"),
    (0x00520FA7, "movzx", "esi, word ptr [r14 + 0x16]"),
    (0x00520FBF, "mov", "r9d, edi"),
    (0x00520FC7, "mov", "edx, esi"),
    (0x00520FC9, "call", "0x40abf0"),
    (0x0040AC1E, "mov", "byte ptr [rcx + 0x3e], dil"),
    (0x0040AC2E, "test", "edx, edx"),
    (0x0040ACC0, "mov", "word ptr [rbx + 0x3c], si"),
    (0x00410303, "movzx", "ecx, word ptr [rdi + 0x3c]"),
    (0x00410307, "imul", "rdx, rcx, 0x290"),
    (0x004238F5, "lea", "rax, [rip + 0x1adcb14]"),
    (0x00423909, "setle", "bpl"),
    (0x00422DE3, "lea", "rax, [rip + 0x1add626]"),
    (0x003E723B, "mov", "r8, qword ptr [rsi + 0x400]"),
    (0x003E724B, "movzx", "ecx, word ptr [r8 + 0xa]"),
    (0x0042194E, "or", "dword ptr [rbx + 0x284], 0x4000000"),
    (0x0042195D, "mov", "word ptr [rbx + 0x2f2], ax"),
    (0x0042198E, "test", "dword ptr [rbx + 0x284], 0x4000000"),
    (0x00421A6F, "or", "dword ptr [rsi + 0x284], 0x4000000"),
    (0x00421A9C, "mov", "edx, 0x1e"),
    (0x00421AC1, "call", "0x46e640"),
    (0x005208BA, "movss", "dword ptr [rdx + 0x24], xmm0"),
    (0x005208CF, "subss", "xmm1, dword ptr [rdx + 0x24]"),
    (0x003D7FFF, "cmp", "byte ptr [rip + 0x277579c], 0"),
    (0x003517D2, "jmp", "0x2ea880"),
]
TARGETS = {0x004238F5: 0x01F00410, 0x00422DE3: 0x01F00410, 0x003D7FFF: 0x02B4D7A2}


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and ins.op_str == ops
        if ok and va in TARGETS:
            disp = int(ops.split("rip + ")[1].split("]")[0], 16)
            ok = va + ins.size + disp == TARGETS[va]
        fails += 0 if ok else 1
        got = "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<no decode>"
        tgt = " -> %08X" % TARGETS[va] if va in TARGETS else ""
        print("%s %08X %s%s" % ("ok  " if ok else "FAIL", va, got, tgt))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
