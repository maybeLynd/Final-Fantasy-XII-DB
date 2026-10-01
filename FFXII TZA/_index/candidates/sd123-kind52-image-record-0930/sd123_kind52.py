"""sd123_kind52.py - SD-123: what effect record kind 0x52 is (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py. The kind table is effect-element-type-dispatch.md's record-store
table (loader 00500C00, destroy 00500AA0, node 0x1D0).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# I1 - the header: format byte -> +0xA0 (low 6 bits; 0xFF = no image), bit 6 -> +0x1C8, bit 7 -> +0x1CA; palette count
#      byte -> +0xA2; words -> +0x1CC, +0x1CE, +0xA8, +0xAA, and +0xA8 / +0xAA copied to +0xA4 / +0xA6
check("I1", txt(0x00500C23) == "movzx ecx, byte ptr [rbx]" and txt(0x00500C30) == "cmp cl, 0xff" and txt(0x00500C39) == "and byte ptr [rdi + 0xa0], 0x3f"
      and txt(0x00500C4E) == "mov word ptr [rdi + 0x1c8], ax" and txt(0x00500C58) == "mov word ptr [rdi + 0x1ca], ax"
      and txt(0x00500C63) == "mov byte ptr [rdi + 0xa2], al" and txt(0x00500C83) == "mov word ptr [rdi + 0xa8], ax"
      and txt(0x00500C92) == "mov word ptr [rdi + 0xaa], ax" and txt(0x00500CA0) == "mov word ptr [rdi + 0xa4], ax"
      and txt(0x00500CAE) == "mov word ptr [rdi + 0xa6], ax" and txt(0x00500C6D) == "mov word ptr [rdi + 0x1cc], ax",
      "header: format +0xA0 (+ bits 6/7), palette count +0xA2, two size pairs +0xA8/+0xAA and +0x1CC/+0x1CE")
# I2 - the palettes: format 1 (or 0x81) takes 1,024-byte entries (count << 10: 256 colours x 4), format 0 (or 0x80)
#      64-byte entries (count << 6: 16 colours x 4); each palette goes through the CLUT submit 001837A0 and 00183760, the
#      two handles stored at +0xC8 + 8i and +0x148 + 8i; any other format fails the load
check("I2", txt(0x00500CEC) == "sub ecx, 1" and txt(0x00500CF1) == "sub ecx, 0x7f" and txt(0x00500CFB) == "xor eax, eax"
      and txt(0x00500D08) == "shl ebp, 0xa" and txt(0x00500D6F) == "shl ebp, 6" and txt(0x00500D5B) == "add r14d, 0x400"
      and txt(0x00500D31) == "call 0x1837a0" and txt(0x00500D38) == "mov qword ptr [rbx - 0x80], rax"
      and txt(0x00500D45) == "call 0x183760" and txt(0x00500D4A) == "mov qword ptr [rbx], rax" and txt(0x00500D16) == "lea rbx, [rdi + 0x148]",
      "palettes: 256 x 4 B (format 1/0x81) or 16 x 4 B (format 0/0x80), created per palette, handles at +0xC8 / +0x148")
# I3 - the image: the size pairs are tested against their power-of-two ceilings (0017FEA0, the 16-bit smear-and-
#      increment) and the surface is created from width x height products through the render-layer calls
check("I3", txt(0x00500E3F) == "call 0x17fea0" and txt(0x00500EC5) == "call 0x17fea0" and txt(0x00500ED4) == "call 0x17fea0"
      and txt(0x00500F4A) == "call 0x183ee0" and txt(0x00500F7B) == "call 0x184140" and txt(0x00500FBF) == "call 0x184130"
      and txt(0x00501000) == "call 0x184370" and txt(0x0050103D) == "call 0x183a00" and txt(0x00501078) == "call 0x183c60"
      and txt(0x005010B3) == "call 0x183eb0" and txt(0x00500FA4) == "movzx edx, word ptr [rdi + 0xa8]"
      and txt(0x00500FB4) == "movzx r8d, word ptr [rdi + 0xaa]",
      "the image surface: power-of-two tests, then creation sized by +0xA8 x +0xAA")
# I4 - who holds them: the mesh record (kind 0x54) resolves its +0x1C ids as kind 0x52 handles (003AA280 with edx = 0x52)
#      into the +0x184 array, and the draw picks one per primitive (+0x188); the evaluator 00431830 follows an element's
#      +0xB0 mesh to handle 0 and reads that record's +0x10
check("I4", txt(0x004370D0) == "mov edx, 0x52" and txt(0x004370DA) == "call 0x3aa280" and txt(0x004370B2) == "mov dword ptr [rdi + 0x184], eax"
      and txt(0x00431AC4) == "mov ecx, dword ptr [rax + 0x184]" and txt(0x00431AEA) == "mov rax, qword ptr [rax]"
      and txt(0x00431AF2) == "mov rcx, qword ptr [rax + 0x10]",
      "meshes hold kind-0x52 handles (one per texture slot); 00431830 reads a handle's record +0x10")
print("FAILS %d" % fails)
