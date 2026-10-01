"""Battle locomotion anchors (SWE2-DATA 2026-09-30), static.
  L1 UpdateDetourRecoveryState 0033C870: its one addss from memory adds the float at 009146E4, which is 5.0 (0033C956);
  L2 CheckActorPairClearance 0033D660: mulss by 01CEBB70 = 0.5 (0033D747) and divss by 008F311C = 3.0 (0033D751);
  L3 the steering dispatcher 00339F00 tests the low five bits of [ctx+0x100] and calls 0033CEF0 for 1 and 4,
     0033D200 for 2, 0033CE60 for 3, 0033CDE0 for 5 and 0033BAA0 for 6 (0033A039..0033A0A6);
  L4 DecodeOrderGoal 00312730 is 965 bytes in the function list;
Control C1: the same constant reader returns 0.0 for the known zero at 01EF93F0 (the clamp page's C0), so a wrong
offset would not silently produce the expected values.
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, off, funcs  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def rt(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


def f32(a):
    return struct.unpack_from("<f", d, off(a))[0]


u = {x.address: x for x in dis(0x0033C870)}
adds = [x for x in u.values() if x.mnemonic == "addss" and rt(x)]
check("L1 detour recovery adds 5.0 (0033C956, 009146E4)",
      len(adds) == 1 and adds[0].address == 0x0033C956 and rt(adds[0]) == 0x009146E4 and f32(0x009146E4) == 5.0,
      "%d addss from memory" % len(adds))
c = {x.address: x for x in dis(0x0033D660)}
check("L2 pair clearance: mulss 0.5 (0033D747, 01CEBB70), divss 3.0 (0033D751, 008F311C)",
      c[0x0033D747].mnemonic == "mulss" and rt(c[0x0033D747]) == 0x01CEBB70 and f32(0x01CEBB70) == 0.5
      and c[0x0033D751].mnemonic == "divss" and rt(c[0x0033D751]) == 0x008F311C and f32(0x008F311C) == 3.0)
s = dis(0x00339F00)
arms = {}
cur = None
for x in s:
    if 0x0033A039 <= x.address <= 0x0033A0A6:
        if x.mnemonic == "cmp" and x.op_str.startswith("al,"):
            cur = int(x.op_str.split(",")[1], 0)
        if x.mnemonic == "call" and cur is not None:
            arms[cur] = int(x.op_str, 16)
print("   dispatcher arms: " + ", ".join("%d -> %08X" % (k, v) for k, v in sorted(arms.items())))
check("L3 modes 1/4 -> 0033CEF0, 2 -> 0033D200, 3 -> 0033CE60, 5 -> 0033CDE0, 6 -> 0033BAA0",
      arms == {1: 0x0033CEF0, 2: 0x0033D200, 3: 0x0033CE60, 4: 0x0033CEF0, 5: 0x0033CDE0, 6: 0x0033BAA0}
      and any(x.op_str == "rdi, qword ptr [rcx + 0x100]" for x in s))
check("L4 DecodeOrderGoal 00312730 is 965 bytes", funcs.get(0x00312730) == 965, str(funcs.get(0x00312730)))
check("C1 control: the constant reader gives 0.0 at 01EF93F0", f32(0x01EF93F0) == 0.0)
print("FAILS %d" % FAILS)
