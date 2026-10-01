"""sd141_readers.py - SD-141: who reads the flying-fade pair mMapShadowFlyingFadeRange / mMapShadowFlyingFadeSpeed after
001C7940 stores them to 02CB8414 / 02CB8410 (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py and the `pe` module of _index/candidates/rc22-34-resource-readers-0930/
(38,161 bodies). Every read route is swept:
  F1 rip-relative operands at the two addresses, and any rip-relative operand whose access range covers them;
  F2 image-base-relative operands (displacement = address - 0x00120000);
  F3 a lea of ANY address followed, in the same function, by [reg + d] landing on or covering them;
  F4 stored qwords holding either address.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R, c = T.R, T.scan()
K = {0x02CB8410: "mMapShadowFlyingFadeSpeed", 0x02CB8414: "mMapShadowFlyingFadeRange"}
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


# F1 - rip-relative: the only references at either address are 001C7940's two stores; nothing in 02CB83E0..02CB8417 is
#      wider than a dword, so no wide access covers them
exact = {k: sorted((f, a, kd) for f, a, kd in c["refs"].get(k, ())) for k in K}
near = sorted((g, f, a, kd) for g in range(0x02CB83E0, 0x02CB8418) for f, a, kd in c["refs"].get(g, ()))
wide = [n for n in near if n[0] not in K and ("xmmword" in "%s" % R.md.disasm(R.at(n[2], 16), n[2], 1).__next__().op_str
                                             or "qword" in "%s" % R.md.disasm(R.at(n[2], 16), n[2], 1).__next__().op_str)]
check("F1", exact == {0x02CB8410: [(0x001C7940, 0x001C9040, "W")], 0x02CB8414: [(0x001C7940, 0x001C8FFF, "W")]} and not wide,
      "rip-relative: only the two stores in 001C7940 (001C9040, 001C8FFF); no wider access in 02CB83E0..02CB8417")
# F2 / F3 - image-base-relative displacements, and lea-derived bases, over every body
disp = {k - 0x00120000 for k in K}
f2, f3, nlea = [], [], 0
for f in pe.funcs:
    regs = {}
    for x in pe.dis(f):
        for m in re.finditer(r"\[(\w+)(?: \+ \w+\*\d)? \+ (0x[0-9a-f]+)\]", x.op_str):
            if m.group(1) != "rip" and int(m.group(2), 16) in disp:
                f2.append((f, x.address))
        m = re.match(r"(r\w+), \[rip \+ (0x[0-9a-f]+)\]$", x.op_str)
        if x.mnemonic == "lea" and m:
            regs[m.group(1)] = x.address + x.size + int(m.group(2), 16)
            nlea += 1
            continue
        for reg, t in list(regs.items()):
            for mm in re.finditer(r"\[%s(?: \+ \w+\*\d)?(?: \+ (0x[0-9a-f]+|\d+))?\]" % reg, x.op_str):
                a = t + (int(mm.group(1), 0) if mm.group(1) else 0)
                if any(a <= k < a + 16 for k in K):
                    f3.append((f, x.address))
            if x.op_str.startswith(reg + ",") and x.mnemonic not in ("cmp", "test"):
                regs.pop(reg, None)
check("F2", not f2, "no image-base-relative operand on either address")
check("F3", not f3 and nlea > 40000, "no read through a lea-derived base lands on either (%d leas followed)" % nlea)
# F4 - no stored pointer to either
check("F4", all(not T.qword_sites(k) for k in K), "no stored qword holds either address")
# C1 - control: the same census sees the neighbour 02CB8404's rip read in 001FA820
check("C1", any(f == 0x001FA820 and kd == "R" for f, a, kd in c["refs"].get(0x02CB8404, ())),
      "control: the neighbour 02CB8404 does have a reader (001FA820), and the census reports it")
print("FAILS %d" % fails)
