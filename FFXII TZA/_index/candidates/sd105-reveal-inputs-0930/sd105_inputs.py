"""sd105_inputs.py - SD-105: the text reveal's authored inputs - the text block's +0x90 default, the writer of the fade
step +0x50, and the signed word at [rbp+0x1C] the progress ratio scales (OPUS, 2026-09-30). Static, the certified
image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# V1 - +0x90 is set to -(s8)+0x9E (the lag bound; 8 by the base fill 002AC1E0, per UQ-173) by all three builders:
#      the shared wrapper 002B32D0 and the kind-0 builders 002B3C30 / 002B3D50
check("V1", txt(0x002B33B1) == "movsx ecx, byte ptr [rdi + 0x9e]" and txt(0x002B33C8) == "neg ax" and txt(0x002B33DC) == "mov word ptr [rdi + 0x90], ax"
      and txt(0x002B3CE9) == "movsx eax, byte ptr [rbx + 0x9e]" and txt(0x002B3CF0) == "neg ax" and txt(0x002B3CF8) == "mov word ptr [rbx + 0x90], ax"
      and txt(0x002B3D84) == "movsx eax, byte ptr [rdi + 0x9e]" and txt(0x002B3D99) == "neg ax" and txt(0x002B3DB4) == "mov word ptr [rdi + 0x90], ax",
      "+0x90 = -(s8)+0x9E in 002B32D0, 002B3C30 and 002B3D50 (-8 with the default bound)")
# V2 - the fade step +0x50 is written by 002B32D0 as 1.0 / (s8)+0x9E (1.0 = 01CEBBA8): one lag unit per step (0.125
#      with the bound 8); the message-window run builder 002A4830 copies +0x50 wholesale from its source record
one = struct.unpack("<f", R.at(0x01CEBBA8, 4))[0]
check("V2", txt(0x002B33B8).endswith("0x1a387e8]") and one == 1.0 and txt(0x002B33D9) == "cvtdq2ps xmm0, xmm0"
      and txt(0x002B33EC) == "divss xmm1, xmm0" and txt(0x002B33F0) == "movss dword ptr [rdi + 0x50], xmm1"
      and txt(0x002A48B9) == "movups xmm1, xmmword ptr [rax + 0x50]" and txt(0x002A48C5) == "movups xmmword ptr [rcx + 0x50], xmm1",
      "+0x50 = 1.0 / (s8)+0x9E in 002B32D0; 002A4830 copies it from the source record")
# V3 - the order inside 002B32D0: the builder call first (002B3C30 at 002B3354 or 002B3D50 at 002B3384), then +0x90 and
#      +0x50 - so every element built through the wrapper ends with both set from +0x9E
check("V3", txt(0x002B3354) == "call 0x2b3c30" and txt(0x002B3384) == "call 0x2b3d50" and 0x002B3384 < 0x002B33DC < 0x002B33F0,
      "002B32D0 sets +0x90 / +0x50 after either builder")
# V4 - [rbp+0x1C] in the control-code engine 002AC5F0 is +0x8C of the nested element it builds on its frame at
#      [rbp-0x70] (-0x70 + 0x8C = +0x1C): 002AD569 stores 002B43C0's result there (the nested run's count - a reading);
#      the outer run's progress ratio (+0x10D8 / the per-call total [rbp-0x78]) scales it and the smaller value is kept
#      (002AD653-002AD6CD) before the outer counters are saved and +0x10D8 replaced for the nested draw
check("V4", txt(0x002AD532) == "lea rcx, [rbp - 0x70]" and txt(0x002AD550) == "call 0x2b43c0" and txt(0x002AD569) == "mov word ptr [rbp + 0x1c], ax"
      and -0x70 + 0x8C == 0x1C and txt(0x002AD653) == "movsx ecx, word ptr [rbp + 0x1c]" and txt(0x002AD670).startswith("movd xmm2, dword ptr [r8 + 0x10d8]")
      and txt(0x002AD68C) == "divss xmm2, xmm0" and txt(0x002AD697) == "mulss xmm2, xmm1" and txt(0x002AD6C5) == "cmovl cx, dx"
      and txt(0x002AD6CD) == "mov word ptr [rbp + 0x1c], cx" and txt(0x002AD70B) == "mov dword ptr [r8 + 0x10d8], edx",
      "[rbp+0x1C] = the nested element's +0x8C, scaled by the outer reveal's progress")
print("FAILS %d" % fails)
