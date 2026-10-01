"""sd102_emitters.py - SD-102: what the two glyph emitters 002DAF30 and 002DAC70 put in their render commands (OPUS,
2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py. The GIF / VIF field
layouts are the PS2 hardware formats the database's Legacy-PS2-GS pages already decode (members/gen_gif_tags.py).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0
REG = {0x0: "PRIM", 0x1: "RGBAQ", 0x2: "ST", 0x3: "UV", 0x4: "XYZF2", 0x5: "XYZ2", 0xE: "A+D", 0xF: "NOP"}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def giftag(lo, hi):
    return {"NLOOP": lo & 0x7FFF, "EOP": lo >> 15 & 1, "PRE": lo >> 46 & 1, "PRIM": lo >> 47 & 0x7FF, "FLG": lo >> 58 & 3,
            "NREG": lo >> 60 & 0xF, "REGS": [REG.get(hi >> 4 * k & 0xF, "?%X" % (hi >> 4 * k & 0xF)) for k in range(lo >> 60 & 0xF or 16)]}


def prim(p):
    return {"type": ["POINT", "LINE", "LINESTRIP", "TRIANGLE", "TRISTRIP", "TRIFAN", "SPRITE", "?"][p & 7], "IIP": p >> 3 & 1,
            "TME": p >> 4 & 1, "FGE": p >> 5 & 1, "ABE": p >> 6 & 1, "AA1": p >> 7 & 1, "FST": p >> 8 & 1}


# E1 - 002DAF30 opens a chunk on the packet row [02EBEFC0 + 24 * [02EBEFF0]] (its buffer +0x20, the 32-byte header left
#      for the closer, E4), then writes 64 bytes from its argument (also kept at 022D8F30..022D8F6F), an A+D pair
#      (data [arg+0x88], register 0x14 = TEX1_1), four ints ([+0x5A] x3, [+0x58]) and a GIF tag
check("E1", txt(0x002DAF49).endswith("0x2be40a1]") and txt(0x002DAF4F) == "lea r9, [rax + rax*2]" and txt(0x002DAF69) == "add rax, 0x20"
      and txt(0x002DAF74).endswith("0x1ffdfb5], xmm2") and txt(0x002DAFD5) == "mov rax, qword ptr [rdx + 0x88]"
      and txt(0x002DAFE3) == "mov qword ptr [rcx + 8], 0x14" and txt(0x002DAFF4) == "movsx ecx, word ptr [rbx + 0x58]"
      and txt(0x002DAFF8) == "movsx eax, word ptr [rbx + 0x5a]" and txt(0x002DB009) == "mov dword ptr [rdx + 0xc], ecx",
      "row 02EBEFC0[+24*02EBEFF0]; 4x16 B from the argument (kept at 022D8F30); A+D TEX1_1 = [arg+0x88]; ints ([+0x5A] x3, [+0x58])")
# E2 - the GIF tag: 0xD000400000000001 | PRIM << 47, PRIM 0x15C when r8d != 0 else 0x154; REGS 0x431431431431E
lo = 0xD000400000000001
t1, t0 = giftag(lo | 0x15C << 47, 0x431431431431E), giftag(lo | 0x154 << 47, 0x431431431431E)
check("E2", txt(0x002DB004) == "mov eax, 0x15c" and txt(0x002DB00C) == "mov edx, 0x154" and txt(0x002DB01D) == "cmove eax, edx"
      and txt(0x002DB020) == "movabs rdx, 0xd000400000000001" and txt(0x002DB02A) == "shl rax, 0x2f"
      and txt(0x002DB034) == "movabs rax, 0x431431431431e"
      and t1["NLOOP"] == 1 and t1["EOP"] == 0 and t1["PRE"] == 1 and t1["FLG"] == 0 and t1["NREG"] == 13
      and t1["REGS"] == ["A+D"] + ["RGBAQ", "UV", "XYZF2"] * 4
      and prim(0x15C) == {"type": "TRISTRIP", "IIP": 1, "TME": 1, "FGE": 0, "ABE": 1, "AA1": 0, "FST": 1}
      and prim(0x154) == {"type": "TRISTRIP", "IIP": 0, "TME": 1, "FGE": 0, "ABE": 1, "AA1": 0, "FST": 1},
      "GIF tag NLOOP 1, PRE, PACKED, NREG 13 = A+D + (RGBAQ, UV, XYZF2) x 4; PRIM TRISTRIP textured alpha-blended UV, "
      "Gouraud (0x15C) or flat (0x154) by the third argument")
# E3 - then the draw context [01F811E8] (001B1C00) directly: 00181560 -> 001B1910; 001816F0 with the same four ints
#      ([+0x5A], [+0x5A], [+0x5A], [+0x58]) -> 001B1F80; 00181870(3) -> 001B2490
check("E3", txt(0x002DB047) == "call 0x181560" and txt(0x002DB04C) == "movsx ecx, word ptr [rbx + 0x5a]"
      and txt(0x002DB055) == "mov r8d, ecx" and txt(0x002DB058) == "mov edx, ecx" and txt(0x002DB05A) == "call 0x1816f0"
      and txt(0x002DB05F) == "mov ecx, 3" and txt(0x002DB069) == "jmp 0x181870" and txt(0x001B1C00).endswith("0x1dcf5e1]")
      and txt(0x00181570) == "jmp 0x1b1910" and txt(0x00181722) == "call 0x1b1f80" and txt(0x00181887) == "jmp 0x1b2490",
      "the same values also go to the draw context [01F811E8]: 001B1910, 001B1F80(x, x, x, y), 001B2490(3)")
# E4 - 002DAC70 first closes the open chunk: at its start +0x18 VIF FLUSHE (0x10000000) and +0x1C UNPACK V4-32 with
#      FLG, VU address 0 and NUM = the chunk's quadwords after its 0x20 header; a 7-quadword chunk (the header's only
#      content) is sealed and kicked at once (0016D6A0, 003A1DB0)
check("E4", txt(0x002DAC97) == "sub r9d, 0x20" and txt(0x002DAC9E) == "shr r9d, 4" and txt(0x002DACA9) == "shl eax, 0x10"
      and txt(0x002DACAC) == "or eax, 0x6c008000" and txt(0x002DACB1) == "mov dword ptr [r10 + 0x18], 0x10000000"
      and txt(0x002DACBD) == "cmp r9d, 7" and txt(0x002DACE7) == "call 0x16d6a0" and txt(0x002DACFE) == "call 0x3a1db0",
      "closes the previous chunk: FLUSHE + UNPACK V4-32 (FLG, addr 0, NUM from the cursor)")
# E5 - then a new chunk: FLUSHE + UNPACK V4-32 NUM 6 to VU address 0x100 (FLG), a GIF tag NLOOP 5 / NREG 1 / A+D, and
#      five A+D writes: TEX0_1 (6) - or TEX0_1 + TEX2_1 (0x16) for a 4-bit texture - from the texture record's +0x30,
#      register 0x7F = 0, TEX1_1 (0x14) = 0, TEST_1 (0x47) = [arg+0x80], ALPHA_1 (0x42) = [arg+0x78]
g = giftag(0x1000000000000005, 0xE)
check("E5", txt(0x002DAD1A) == "mov dword ptr [rax + 8], 0x10000000" and txt(0x002DAD21) == "mov dword ptr [rax + 0xc], 0x6c068100"
      and txt(0x002DAD31) == "movabs rcx, 0x1000000000000005" and txt(0x002DAD3E) == "mov qword ptr [rax + 8], 0xe"
      and g["NLOOP"] == 5 and g["NREG"] == 1 and g["REGS"] == ["A+D"] and g["PRE"] == 0
      and txt(0x002DAD9C) == "mov qword ptr [rdx + 8], 6" and txt(0x002DADE1) == "mov qword ptr [rcx + 8], 0x16"
      and txt(0x002DAE2E) == "mov qword ptr [rdx + 8], 6" and txt(0x002DAE42) == "mov qword ptr [rax + 8], 0x7f"
      and txt(0x002DAE3F) == "mov qword ptr [rax], rbp" and txt(0x002DAC88) == "xor ebp, ebp"
      and txt(0x002DAE60) == "mov qword ptr [rax + 8], 0x14" and txt(0x002DAE71) == "mov rax, qword ptr [rsi + 0x80]"
      and txt(0x002DAE7B) == "mov qword ptr [rcx + 8], 0x47" and txt(0x002DAE8C) == "mov rax, qword ptr [rsi + 0x78]"
      and txt(0x002DAE93) == "mov qword ptr [rcx + 8], 0x42",
      "UNPACK V4-32 x6 -> VU 0x100; GIF A+D x5: TEX0_1 (+TEX2_1), reg 0x7F = 0, TEX1_1 = 0, TEST_1 = [+0x80], ALPHA_1 = [+0x78]")
# E6 - the texture word: TEX0 is the record's +0x30 qword. PSM (record +0x38, bits 8-13) 0x14 (PSMT4): PSM rewritten to
#      0x13 (bits 20-25) and CBP (bit 37) + 4 * flags[7:4], then TEX2_1 carrying CSA = flags[3:0] (bit 56); PSM 0x13
#      (PSMT8): CBP + a flag-derived row; flag bit 16 set: the record's TEX0 with fixed CLUT bits instead
check("E6", txt(0x002DAD7F) == "and ecx, 0x3f00" and txt(0x002DAD85) == "cmp ecx, 0x1400" and txt(0x002DADA4) == "and rax, 0xfffffffffd3fffff"
      and txt(0x002DADAA) == "or rax, 0x1300000" and txt(0x002DADB0) == "shl rcx, 0x25" and txt(0x002DADD3) == "shl rax, 0x38"
      and txt(0x002DADEB) == "cmp ecx, 0x1300" and txt(0x002DAD52) == "bt eax, 0x10" and txt(0x002DAD69) == "movabs rcx, 0x6878000000000",
      "TEX0 from the texture record +0x30 with CLUT rebasing for PSMT4 (plus TEX2_1 CSA) and PSMT8")
# E7 - 002DD350 appends VIF FLUSHE + MSCAL (0x14000000 | the microprogram address, 02EBB764 >> 3 here), seals the chunk
#      and kicks it; 002DAC70 then mirrors the state into the draw context: 001819A0 (texture: width/height words of the
#      record's +0x20 object, the record, the palette byte, a flag), 00181910(TEST word), 001816B0(ALPHA word), 00181330
check("E7", txt(0x002DAE4F).endswith("0x2be090e]") and txt(0x002DAE5A) == "shr edx, 3" and txt(0x002DAEA3) == "call 0x2dd350"
      and txt(0x002DD35D) == "or edx, 0x14000000" and txt(0x002DD36B) == "mov dword ptr [rax + 8], 0x10000000"
      and txt(0x002DD39B) == "call 0x16d6a0" and txt(0x002DD3B2) == "call 0x3a1db0"
      and txt(0x002DAEEE) == "call 0x1819a0" and txt(0x002DAEF3) == "mov rcx, qword ptr [rsi + 0x80]" and txt(0x002DAEFA) == "call 0x181910"
      and txt(0x002DAEFF) == "mov rcx, qword ptr [rsi + 0x78]" and txt(0x002DAF03) == "call 0x1816b0" and txt(0x002DAF08) == "call 0x181330"
      and txt(0x00181929) == "jmp 0x1b22e0" and txt(0x001816C9) == "jmp 0x1b22d0" and txt(0x00181340) == "jmp 0x1b03d0",
      "MSCAL 02EBB764>>3, seal + kick; the same TEST / ALPHA / texture state also set on the draw context [01F811E8]")
print("FAILS %d" % fails)
