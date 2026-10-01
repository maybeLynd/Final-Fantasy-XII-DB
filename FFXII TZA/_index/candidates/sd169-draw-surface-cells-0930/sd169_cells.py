"""sd169_cells.py - SD-169: which GS register, if any, the draw-surface cells 022D8EAC (+0x9C) and 022D8EB0 (+0xA0)
correspond to (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
GS register numbers: 0x50 BITBLTBUF, 0x51 TRXPOS, 0x52 TRXREG, 0x53 TRXDIR (the PS2 GS map the Legacy-PS2-GS pages use).
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


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# G1 - the boot values (0036D280): +0x9C (022D8EAC) = 512, +0xA0 (022D8EB0) = 512, 022D8EB4 = 448, 022D8EA8 = 0
check("G1", txt(0x0036D286).endswith("0x1f6bc1c], 0x200") and txt(0x0036D2A3).endswith("0x1f6bc03], 0x200")
      and txt(0x0036D2AD).endswith("0x1f6bbfd], 0x1c0") and txt(0x0036D290).endswith("0x1f6bc12], eax"),
      "boot: width cells 512 / 512, height 448")
# G2 - 00244200 builds a GIF A+D packet (tag 0x1000000000008007: NLOOP 7, EOP, one A+D register per loop): the first
#      value goes to register 0x50 BITBLTBUF and is SBP = [022D8EA8] * [022D8EB4] * width >> 6, SBW = width >> 6,
#      DBP = 0x333C, DBW = width >> 6 (width = +0x9C); then 0x51 TRXPOS, 0x52 TRXREG, 0x53 TRXDIR = 2 (local -> local),
#      and further TRXPOS / TRXREG pairs whose TRXREG width is [022D8EAC] with height 16 (0x10 << 32)
check("G2", txt(0x00244224).endswith("0x2094c81]") and txt(0x00244241) == "sar edx, 6" and txt(0x0024425A) == "sar eax, 6"
      and txt(0x0024426E) == "or rax, 0x333c0000" and txt(0x00244274) == "shl rax, 0x10" and txt(0x00244278) == "or rsi, rax"
      and txt(0x002442AC) == "movabs rcx, 0x1000000000008007" and txt(0x002442B9) == "mov qword ptr [rax + 8], 0xe"
      and txt(0x002442CF) == "mov qword ptr [rax], rsi" and txt(0x002442D2) == "mov qword ptr [rax + 8], 0x50"
      and txt(0x002442F2) == "mov qword ptr [rcx + 8], 0x51" and txt(0x00244315) == "mov qword ptr [rcx + 8], 0x52"
      and txt(0x0024432B) == "mov qword ptr [rax], 2" and txt(0x00244332) == "mov qword ptr [rax + 8], 0x53"
      and txt(0x002442A2) == "movabs rdx, 0x1000000000" and txt(0x00244362).endswith("0x2094b43]") and txt(0x00244378) == "mov qword ptr [rcx + 8], 0x52",
      "+0x9C = the transfer width: BITBLTBUF SBW/DBW (>> 6) and TRXREG RRW (strips of 16 lines), local -> local")
# G3 - +0xA0 (022D8EB0) has one writer (the boot 0036D280) and one reader, 0036D2F0, which passes it only as an argument
#      to 0016D6A0 - the shared bare `ret` - so it reaches no GS register or any other consumer
refs = sorted((f, a, k) for f, a, k in c["refs"].get(0x022D8EB0, ()))
check("G3", refs == [(0x0036D280, 0x0036D2A3, "W"), (0x0036D2F0, 0x0036D342, "R")] and txt(0x0036D34E) == "call 0x16d6a0"
      and txt(0x0016D6A0).startswith("ret"),
      "+0xA0: set to 512 at boot, read once into a call to the empty stub 0016D6A0 - no register, no effect")
print("FAILS %d" % fails)
