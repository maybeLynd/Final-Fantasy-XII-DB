"""sd3_bit21.py - what aggregate capability-policy bit 21 changes (OPUS, 2026-09-30; register SD-3).
Asserts the two consumers' behaviour over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return "%s %s" % (i.mnemonic, i.op_str)


# A1 - the audio consumer 00229AF0: bit 21 of the aggregate -> tail-jump to the row-1 reader (skipping the rest);
#      otherwise, unless 00226BD0(0xF) is non-zero, Audio_SetGroupMask(0x3F, 1, 1) holds audio groups 0..5
check("A1", txt(0x00229AFE) == "call 0x2e0fa0" and txt(0x00229B03) == "bt eax, 0x15" and txt(0x00229B07).startswith("jae")
      and txt(0x00229B09) == "mov ecx, 1" and txt(0x00229B12) == "jmp 0x2e1020" and txt(0x00229B17) == "mov ecx, 0xf"
      and txt(0x00229B1C) == "call 0x226bd0" and txt(0x00229B25) == "mov edx, 1" and txt(0x00229B2A) == "lea ecx, [rax + 0x3f]"
      and txt(0x00229B2D) == "mov r8d, edx" and txt(0x00229B34) == "jmp 0x2df370",
      "bit 21 set -> 002E1020(1) and return; clear -> Audio_SetGroupMask(0x3F, 1, 1) unless 00226BD0(0xF) != 0")
# A2 - it runs on the full-screen state's event: Phyre::VTS::ScreenStateFullScreen slot 5 (007A3B20) sets state 3 and,
#      unless 00228480() refuses, tail-jumps 0017D4B0 -> 00229AF0
vt = T.rtti_class(0x01CB3FA8)
slot5 = int.from_bytes(R.at(0x01CB3FA8 + 5 * 8, 8), "little")
check("A2", vt == "Phyre::VTS::ScreenStateFullScreen" and slot5 == 0x007A3B20 and txt(0x007A3B60) == "mov dword ptr [rcx + 8], 3"
      and txt(0x007A3B67) == "call 0x228480" and txt(0x007A3B74) == "jmp 0x17d4b0" and txt(0x0017D4B0) == "jmp 0x229af0",
      "ScreenStateFullScreen slot 5, event 4 with [rdx+4] = 0 -> state 3 -> 0017D4B0 -> 00229AF0")
# I1 - the input consumer 00228380 (only caller 00253C70): with bit 21 in the aggregate it reads row 1 (002E1020(1));
#      if row 1 lacks bit 21 it returns 0, else the modal flag (ebx) drops from 1 to 0
check("I1", txt(0x00228396) == "mov ebx, 1" and txt(0x002283DA) == "bt esi, 0x15" and txt(0x002283E0) == "mov ecx, ebx"
      and txt(0x002283E2) == "call 0x2e1020" and txt(0x002283E7) == "bt eax, 0x15" and txt(0x002283EB).startswith("jae 0x22843a")
      and txt(0x002283ED) == "xor ebx, ebx" and sorted(f for f, _ in c["calls"].get(0x00228380, ())) == [0x00253C70],
      "bit 21: row-1 bit 21 clear -> return 0; set -> flag 0 instead of 1")
# I2 - the flag reaches 002282F0, which opens (once) the modal widget with handler 00229590, the flag as payload +8,
#      and keeps it at 01FD4940
check("I2", txt(0x00228424) == "mov ecx, ebx" and txt(0x00228435) == "jmp 0x2282f0" and txt(0x00228303).startswith("cmp qword ptr [rip")
      and txt(0x00228321) == "movsxd rcx, ecx" and txt(0x00228329) == "mov qword ptr [rsp + 0x28], rcx"
      and txt(0x0022832E).startswith("lea rdx, [rip") and txt(0x0022834A) == "call 0x244f50"
      and ins(0x0022832E).address + ins(0x0022832E).size + ins(0x0022832E).operands[1].mem.disp == 0x00229590,
      "002282F0(flag): if no modal at [01FD4940], create widget 00229590 with payload +8 = flag")
print("FAILS %d" % fails)
