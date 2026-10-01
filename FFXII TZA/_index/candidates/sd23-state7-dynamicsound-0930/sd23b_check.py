"""sd23b_check.py - SD-23's two limits closed: what state 7 of the Sound tick 007BF0A0 is (the terminal state slot 39
gates), and which class 007F0820 is (SQEX::Sd::Lay::DynamicSound, whose slot 38 is a float field) (OPUS, 2026-09-30).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py (RTTI reader included).
"""
import os, re, struct, sys

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


# S1 - the Sound tick 007BF0A0 does nothing for a sound in state 0, 1 or 7 (007BF0B7 / 007BF0C0 -> 007BF99F)
check("S1", txt(0x007BF0A8) == "mov eax, dword ptr [rcx + 0x54]" and txt(0x007BF0B7) == "cmp eax, 1" and txt(0x007BF0BA) == "jbe 0x7bf99f"
      and txt(0x007BF0C0) == "cmp eax, 7" and txt(0x007BF0C3) == "je 0x7bf99f",
      "the tick skips states 0, 1 and 7")
# S2 - it drops dead children from the list at +0x400 (count +0x4C; 007B5070 resolves each handle, null -> removed), then:
#      outside states 2..4 and with no child left, state 6 always becomes 7, and any other state becomes 7 only when slot 39
#      (+0x138) answers true
check("S2", txt(0x007BF0E9) == "lea rsi, [rcx + 0x400]" and txt(0x007BF113) == "call 0x7b5070" and txt(0x007BF142) == "dec dword ptr [rbx + 0x4c]"
      and txt(0x007BF16A) == "lea eax, [rcx - 2]" and txt(0x007BF16D) == "cmp eax, 2" and txt(0x007BF172) == "cmp dword ptr [rbx + 0x4c], r15d"
      and txt(0x007BF178) == "cmp ecx, 6" and txt(0x007BF17B) == "je 0x7bf18d" and txt(0x007BF183) == "call qword ptr [rax + 0x138]"
      and txt(0x007BF18D) == "mov dword ptr [rbx + 0x54], 7",
      "no children left: state 6 -> 7 always; other states -> 7 only if slot 39 says so")
# S3 - the only other writer of state 7 is the start step 007BD120: a start that completes at once (007BD13F) or fails
#      (the bank lookup 007AAA20 null, or 007A9A10 negative -> 007BD16D, returning -1); nothing in the audio range compares
#      +0x54 with 7 except the tick's own skip
st7 = []
for f, n in SZ.items():
    if 0x007A0000 <= f < 0x00800000:
        for i in R.md.disasm(R.at(f, n), f):
            if re.match(r"dword ptr \[r\w+ \+ 0x54\], 7$", i.op_str):
                st7.append((i.address, i.mnemonic))
check("S3", sorted(st7) == [(0x007BD13F, "mov"), (0x007BD16D, "mov"), (0x007BF18D, "mov")]
      and txt(0x007BD160) == "call 0x7aaa20" and txt(0x007BD174) == "or eax, 0xffffffff" and txt(0x007BD18B) == "call 0x7a9a10"
      and txt(0x007BD192) == "js 0x7bd16d" and txt(0x007BD197) == "je 0x7bd13f",
      "state 7 writers: start completed, start failed, last child gone - the terminal state")
# D1 - 007F0820 is a method of SQEX::Sd::Lay::DynamicSound: its one caller 007F1670 is slot 10 of that class's vtable,
#      whose slot 38 is `movss xmm0, [rcx + 0xE8]` (a float field) and slot 39 the shared `mov al, 1`
site = T.qword_sites(0x007F1670)
vs, name = T.vtable_start(site[0]) if len(site) == 1 else (None, None)
q = lambda k: struct.unpack("<Q", R.at(vs + 8 * k, 8))[0]
check("D1", [f for f, s in c["calls"].get(0x007F0820, ())] == [0x007F1670] and name == "SQEX::Sd::Lay::DynamicSound"
      and (site[0] - vs) // 8 == 10 and txt(q(38)) == "movss xmm0, dword ptr [rcx + 0xe8]" and q(39) == 0x007E5800
      and txt(0x007E5800) == "mov al, 1",
      "007F0820 is DynamicSound's: slot 38 = float +0xE8, slot 39 = true")
print("FAILS %d" % fails)
