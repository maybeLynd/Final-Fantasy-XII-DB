"""sd23_sound_slots.py - what the Sound family's slots 38 (+0x130) and 39 (+0x138) answer, and how callers use it
(OPUS, 2026-09-30; register SD-23). Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0
FALSE, TRUE = 0x007E57B0, 0x007E5800
PRIMARY = {0x01CB5A30: "Sound", 0x01CB87A8: "RandomSound", 0x01CB8940: "VariationSound", 0x01CB8AD8: "OrderSound",
           0x01CB8C70: "CycleSound", 0x01CB8E08: "SwitchSound"}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


# F1 - the two bodies: 007E57B0 `xor al, al; ret` (false), 007E5800 `mov al, 1; ret` (true)
check("F1", ins(FALSE).op_str == "al, al" and ins(FALSE + 2).mnemonic == "ret" and ins(TRUE).op_str == "al, 1"
      and ins(TRUE + 2).mnemonic == "ret", "007E57B0 returns false, 007E5800 returns true")
# F2 - each primary vtable (RTTI-named) and its slots 38 / 39
ans = {}
for vt, name in PRIMARY.items():
    cls = T.rtti_class(vt)
    s38, s39 = struct.unpack("<2Q", R.at(vt + 38 * 8, 16))
    ans[name] = (cls, {FALSE: "false", TRUE: "true"}.get(s38, "%08X" % s38), {FALSE: "false", TRUE: "true"}.get(s39, "%08X" % s39))
exp = {"Sound": ("false", "true"), "RandomSound": ("false", "true"), "VariationSound": ("true", "true"),
       "OrderSound": ("false", "true"), "CycleSound": ("false", "false"), "SwitchSound": ("false", "true")}
check("F2", all(ans[n][0] == "SQEX::Sd::Driver::" + n and ans[n][1:] == exp[n] for n in exp),
      "slot 38 true only for VariationSound; slot 39 false only for CycleSound: %s" % {n: v[1:] for n, v in ans.items()})
# F3 - the 16 calls through +0x130 in the audio range: 12 test the byte result (the Sound family's boolean), 4 in
#      007F0820 use a float result (comiss / subss on xmm0) and so are another class's slot 38
sites = []
for f, n in T.sizes().items():
    if not 0x007A0000 <= f < 0x00800000:
        continue
    d = R.at(f, n)
    if d:
        sites += [(f, i) for i in R.md.disasm(d, f) if i.mnemonic == "call" and i.op_str.endswith("+ 0x130]") and "rip" not in i.op_str]
boolean, floaty = [], []
for f, i in sites:
    nxt = [x for x in R.md.disasm(R.at(i.address + i.size, 24), i.address + i.size)][:3]
    uses = " ".join("%s %s" % (x.mnemonic, x.op_str) for x in nxt)
    (boolean if "test al, al" in uses else floaty).append((f, i.address, uses))
check("F3", len(sites) == 16 and len(boolean) == 12 and len(floaty) == 4 and all(f == 0x007F0820 for f, _, _ in floaty)
      and all("xmm0" in u for _, _, u in floaty),
      "boolean sites %d, float sites %d (all in 007F0820)" % (len(boolean), len(floaty)))
for f, a, u in sorted(boolean):
    print("      bool  %08X@%08X  %s" % (f, a, u[:70]))
for f, a, u in sorted(floaty):
    print("      float %08X@%08X  %s" % (f, a, u[:70]))
# F4 - the two calls through +0x138 test the byte result
s39 = [(0x007BF0A0, 0x007BF183), (0x007F0820, 0x007F0A23)]
check("F4", all(ins(a + 6).op_str == "al, al" for _, a in s39), "slot 39 sites 007BF183 (true -> [obj+0x54] = 7), 007F0A23 (true -> slot 37)")
print("FAILS %d" % fails)
