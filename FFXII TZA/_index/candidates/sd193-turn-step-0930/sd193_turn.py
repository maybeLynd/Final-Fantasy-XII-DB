"""sd193_turn.py - SD-193: what 003EC040 computes for mode 3's turn (OPUS, 2026-09-30).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py. The arithmetic of the three helpers is
ALSO re-computed in Python from their instruction semantics and compared on sample angles (a model, not an execution).
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


def f32(a):
    return struct.unpack("<f", R.at(a, 4))[0]


PI = f32(0x01CEBC50)
# H1 - the constants: +-pi and +-2pi, and the rate multiplier 01DFE0BC (1.0 in the file; the boot fixups store 0.5 at
#      001EDDE0, CONTRACT-boot-fixups.md)
check("H1", abs(PI - math.pi) < 1e-6 and abs(f32(0x01CEBC78) - 2 * math.pi) < 1e-5 and f32(0x01DFE0BC) == 1.0
      and txt(0x001EDDE0) == "movss dword ptr [rip + 0x1c102d4], xmm1",
      "pi = %.6f, 2pi, multiplier 01DFE0BC = 1.0 in the file (0.5 after the boot fixup)" % PI)
# H2 - 003A1980(x, s) = min(|x|, s); 003A1AD0(cur, target, step): d = wrap(target - cur) into [-pi, pi]; if
#      min(|d|, step) == step, move cur by step toward d's sign, else take target; wrap the result
check("H2", txt(0x003A1987).startswith("andps xmm2") and txt(0x003A1992) == "minss xmm0, xmm1"
      and txt(0x003A1AEF) == "subss xmm4, xmm3" and txt(0x003A1B4B) == "minss xmm7, xmm9" and txt(0x003A1B50) == "ucomiss xmm7, xmm9"
      and txt(0x003A1B60) == "subss xmm3, xmm7" and txt(0x003A1B66) == "addss xmm3, xmm7" and txt(0x003A1B6C) == "movaps xmm3, xmm8",
      "003A1AD0 = constant-rate shortest-path approach; 003A1980 = min(|x|, s)")
# H3 - 003EC510(d, dir): wrap d into [-pi, pi]; 0 stays 0; dir 0 lifts a negative d by 2pi (always the positive way
#      round), dir 1 drops a positive d by 2pi (always the negative way round)
check("H3", txt(0x003EC55C) == "je 0x3ec56d" and txt(0x003EC56D) == "comiss xmm1, xmm0" and txt(0x003EC572) == "addss xmm0, xmm3"
      and txt(0x003EC563) == "comiss xmm0, xmm1" and txt(0x003EC568) == "addss xmm0, xmm2",
      "003EC510 = the delta forced into one turning direction")
# E1 - 003EC040(record index, target, mode, fast): the step is 01DFE0BC x the record 003E56C0 resolves, +0x24 (mode
#      path) or +0x28 (when the fourth argument is non-zero, through 003A1AD0); mode 2 -> 003A1AD0 (shortest way);
#      modes 0 / 1 -> turn by step in the forced direction and snap to target once within one step; mode < 0 or > 2,
#      or no record -> the target at once
check("E1", txt(0x003EC139) == "mulss xmm2, dword ptr [rax + 0x28]" and txt(0x003EC146) == "call 0x3a1ad0"
      and txt(0x003EC15A) == "mulss xmm6, dword ptr [rax + 0x24]" and txt(0x003EC16C) == "cmp edi, 2" and txt(0x003EC17F) == "call 0x3a1ad0"
      and txt(0x003EC1B6) == "call 0x3ec510" and txt(0x003EC1BE) == "call 0x3a1980" and txt(0x003EC1C6) == "ja 0x3ec1e7"
      and txt(0x003EC1CC) == "addss xmm6, dword ptr [rbx + 0x124]" and txt(0x003EC1E1) == "subss xmm0, xmm6"
      and txt(0x003EC1E7) == "movaps xmm0, xmm7" and txt(0x003EC161) == "js 0x3ec1e7",
      "mode 2 shortest-way approach, modes 0/1 fixed-direction step, else the target")
# E2 - it holds the current heading (+0x124) while the render object's animation id (+0xCC & 0xFFF) is 0x0D, 0x35 or
#      0x36 in state 1, and returns 0 for an invalid record or a hidden-and-parked one
check("E2", txt(0x003EC0F3) == "cmp esi, 0x35" and txt(0x003EC0F8) == "cmp esi, 0x36" and txt(0x003EC0FD) == "cmp esi, 0xd"
      and txt(0x003EC102) == "movss xmm0, dword ptr [rbx + 0x124]" and txt(0x003EC1EC) == "xorps xmm0, xmm0",
      "holds for animation ids 0x0D/0x35/0x36; 0 for an invalid record")


# M1 - a model check of the helpers' arithmetic on sample angles (the instruction semantics above, in Python)
def wrap(a):
    while -PI > a:
        a += 2 * PI
    while a > PI:
        a -= 2 * PI
    return a


def approach(cur, tgt, step):
    d = wrap(tgt - cur)
    m = min(abs(d), step)
    out = (cur - m if 0 > d else cur + m) if m == step else tgt
    return wrap(out)


cases = [(0.0, 1.0, 0.25, 0.25), (0.0, -1.0, 0.25, -0.25), (0.0, 0.1, 0.25, 0.1), (3.0, -3.0, 0.2, 3.2 - 2 * PI)]
ok = all(abs(approach(a, b, s) - want) < 1e-5 for a, b, s, want in cases)
check("M1", ok, "model: approach(0,1,.25)=.25, (0,-1,.25)=-.25, snaps within a step, crosses the +-pi seam the short way")
print("FAILS %d" % fails)
