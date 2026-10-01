"""sd180_walk.py - SD-180 / SD-181: the emitter-volume walk after its shape dispatch, and where its base comes from
(OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return i.address + i.size + int(re.search(r"rip \+ 0x([0-9a-f]+)", i.op_str).group(1), 16)


# W1 - after the shape dispatch the walk 003631B0 loads three record floats and hands them, with the clamped point, to
#      00361810: +0x38 always (the attenuation argument), +0x54 / +0x58 for classes 0 and 1; the segment-chain class 2
#      passes 0 and a constant instead and adds 00362230's own float result
check("W1", txt(0x003632D1) == "movss xmm2, dword ptr [rbx + 0x58]" and txt(0x003632D6) == "movss xmm1, dword ptr [rbx + 0x54]"
      and txt(0x003632DB) == "movss xmm0, dword ptr [rbx + 0x38]" and txt(0x00363320) == "call 0x361810"
      and txt(0x003632A3) == "movaps xmm6, xmm0" and txt(0x003632AD) == "jmp 0x3632db",
      "record +0x38 (all), +0x54/+0x58 (classes 0/1) -> 00361810 with the clamped point")
# W2 - then 003638B0(record, ..., r9 = the running value); its result replaces the running value ONLY when 00361810's
#      float result is exactly 0.0 (ucomiss against the zeroed xmm7, jp / jne skip)
check("W2", txt(0x00363344) == "call 0x3638b0" and txt(0x00363336) == "mov r9d, ebp" and txt(0x00363349) == "ucomiss xmm6, xmm7"
      and txt(0x0036334C) == "jp 0x363352" and txt(0x0036334E) == "jne 0x363352" and txt(0x00363350) == "mov ebp, eax",
      "the running value takes 003638B0's result only when 00361810 returned 0.0")
# W3 - 003638B0 returns the record's signed byte +0x1A when it is >= 0 (without reaching the voice start), else the
#      running value it was given (esi = r9d)
check("W3", txt(0x003638D2) == "mov esi, r9d" and txt(0x003638D5) == "movzx ecx, byte ptr [rcx + 0x1a]"
      and txt(0x003638DE) == "js 0x3638e8" and txt(0x003638E0) == "movsx esi, cl" and txt(0x003638E3) == "jmp 0x3639ff"
      and txt(0x003639FF) == "mov eax, esi",
      "003638B0 returns record +0x1A (if >= 0) else the value passed in")
# W4 - the walk returns the running value (initial r9d from its caller); the driver 00362850 threads it through two
#      walks and dispatches it as 002DF410(1, 0xB4, value), remembering it at 022CBA80 (the map-ctrl page's reading)
check("W4", txt(0x003631BE) == "mov ebp, r9d" and txt(0x00363367) == "mov eax, ebp" and txt(0x00362B82) == "mov esi, eax"
      and txt(0x00362BBC) == "mov esi, eax" and txt(0x00362BD6) == "mov edx, 0xb4" and txt(0x00362BDB) == "mov ecx, 1"
      and txt(0x00362BE0) == "call 0x2df410" and rip(0x00362BE5) == 0x022CBA80,
      "return -> 002DF410(1, 0xB4, value), stored at 022CBA80")
# B1 (SD-181) - the base 022CBAF0: zeroed at boot (00362F70 from 00266D10) and on unload (00363730 from 00378230); set
#      only by 003635C0(rcx), whose one caller 003775D0 passes [02ADD060] = the map pack's slot-16 SP1 sound-emitter block
#      when bit 7 of the to-bind word 02ADD0F0 is set
w = sorted(x[1] for x in c["refs"].get(0x022CBAF0, ()) if txt(x[1]).startswith("mov qword ptr [rip"))
check("B1", w == [0x00362FA7, 0x003635CE, 0x00363737] and txt(0x003635CE) == "mov qword ptr [rip + 0x1f6851b], rcx"
      and [f for f, s in c["calls"].get(0x003635C0, ())] == [0x003775D0] and rip(0x003775EE) == 0x02ADD060
      and txt(0x003775EC) == "jns 0x37760a" and rip(0x003775D4) == 0x02ADD0F0,
      "writers of 022CBAF0: boot zero, unload zero, and 003635C0([02ADD060]) = the SP1 block")
print("FAILS %d" % fails)
