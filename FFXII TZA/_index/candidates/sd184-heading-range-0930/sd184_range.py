"""sd184_range.py - SD-184 narrowed: when the heading normaliser 0033CB70 mis-normalises, and which unnormalised st+0xE0
writers are bounded by their source (OPUS, 2026-09-30). Static, the certified image, via retool.py; M1 is a Python model
of 0033CB70's two paths from its instructions (a model, not an execution).
"""
import math, os, struct, sys

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


f32 = lambda a: struct.unpack("<f", R.at(a, 4))[0]
PI, TWO, FOUR = f32(0x01CEBC50), f32(0x01CEBC78), f32(0x00D10B0C)
# N1 - 0033CB70's gate: |x| > 4pi (00D10B0C / 00D10B20) takes the fast path x - trunc(x / 2pi) * 2pi and returns with
#      no further wrap; otherwise it adds / subtracts 2pi in loops until x is in [-pi, pi]
check("N1", abs(FOUR - 4 * math.pi) < 1e-5 and f32(0x00D10B20) == -FOUR and txt(0x0033CB7A) == "ja 0x33cbcd" and txt(0x0033CB87) == "ja 0x33cbcd"
      and txt(0x0033CBCD).startswith("divss xmm0") and txt(0x0033CBD5) == "cvttss2si eax, xmm0" and txt(0x0033CBE8) == "subss xmm2, xmm0"
      and txt(0x0033CBEF) == "ret" and txt(0x0033CBA0) == "addss xmm2, xmm1" and txt(0x0033CBC0) == "addss xmm2, xmm1",
      "fast path for |x| > 4pi = %.5f, loops otherwise" % FOUR)


def norm(x):
    if x > FOUR or -FOUR > x:
        return x - int(x / TWO) * TWO
    while x > PI:
        x -= TWO
    while -PI > x:
        x += TWO
    return x


# M1 - the model: in range for |x| <= 4pi; the fast path leaves values in (-2pi, 2pi), e.g. 16 -> 3.43, -16 -> -3.43,
#      while 13 -> 0.43 happens to land in range
check("M1", all(-PI <= norm(x) <= PI for x in [i * 0.37 for i in range(-33, 34)]) and abs(norm(16.0) - (16.0 - 2 * TWO)) < 1e-5
      and norm(16.0) > PI and norm(-16.0) < -PI and -PI <= norm(13.0) <= PI,
      "model: |x| <= 4pi always lands in [-pi, pi]; 16.0 -> %.4f and -16.0 -> %.4f do not" % (norm(16.0), norm(-16.0)))
# S1 - 003003F0 (the facing publish) is called three times: 00325BB0 passes st+0xE0 itself (a re-publish of the current
#      heading), 00326D60 passes facings from its party snapshot at 022C25A0 (twice)
calls = sorted(c["calls"].get(0x003003F0, ()))
check("S1", calls == [(0x00325BB0, 0x00325D5C), (0x00326D60, 0x00326F86), (0x00326D60, 0x0032707D)]
      and txt(0x00325D33) == "movss xmm2, dword ptr [rbx + 0xe0]" and txt(0x00327076) == "movss xmm2, dword ptr [rax + r8 + 0x30]",
      "facing publish callers: a re-publish and the party snapshot")
# S2 - the snapshot 00326BB0 fills each of four 0x30 entries with the member's position (00265020) and its facing
#      (00265200 -> [022C25B1 + 0x1F] = 022C25D0 + 0x30 i); that facing is movementState +0xA8, whose single writer
#      002E5E10 re-runs the sign-biased wrap into [-pi, pi] on every store (heading-speed-to-position-delta.md)
check("S2", txt(0x00326C96) == "call 0x265020" and txt(0x00326C9F) == "call 0x265200" and txt(0x00326CA4) == "movss dword ptr [rsi + 0x1f], xmm0"
      and txt(0x00326CBD) == "cmp ebx, 4" and txt(0x00326CB1) == "add rbp, 0x30",
      "the snapshot stores each member's wrapped facing")
# S3 - 0033CEF0's fallbacks store the dispatcher's desired heading, which is 004687F0's yaw-from-direction result
check("S3", txt(0x00339FF9) == "call 0x4687f0" and txt(0x0033A005) == "movaps xmm6, xmm0" and txt(0x0033A041) == "movaps xmm1, xmm6",
      "the mode-1/4 desired heading is a yaw-from-direction result")
print("FAILS %d" % fails)
