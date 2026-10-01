"""RC-29 companion: the 008FCE00 table's entries are developer-console command ids (SWE2-DATA 2026-09-30), static.

The console object's constructor/label filler 001D0390 stores each command's label string at [obj + 0x130 + 8*id]
(the layout the console pages record: 'label[294] at 0x130 + 8*id'). This script recovers those stores from the
filler's body (lea reg,[rip+string] followed by mov qword [rdi + disp], reg; id = (disp - 0x130) / 8), then prints
every page of the 008FCE00 table with the label of each entry, so the table reads as what it is: the console's
page layout (14 pages x 22 rows), the order the renderer 001CD0E0 draws the rows in.
Controls: C1 the recovered label for id 14 must be 'Invincible:' and id 12 'Read Json Data:' (the console-names page
rows); C2 the kind-7 reading is tested directly: under it page 3 would be the 'Loca' / bin_menu id run 0xDF, 0xE1..,
so its labels must NOT be menu-resource names if the console reading holds.
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, dis, cstr  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


body = dis(0x001D0390)
labels = {}
regval = {}
for x in body:
    if x.mnemonic == "lea":
        t = rip_t(x)
        if t is not None:
            regval[x.op_str.split(",")[0].strip()] = t
            continue
    m = re.match(r"qword ptr \[rdi \+ 0x([0-9a-f]+)\], (\w+)$", x.op_str)
    if x.mnemonic == "mov" and m:
        disp, reg = int(m.group(1), 16), m.group(2)
        if 0x130 <= disp < 0x130 + 8 * 0x127 and (disp - 0x130) % 8 == 0 and reg in regval:
            s = cstr(regval[reg], 120)
            if s is not None:
                labels[(disp - 0x130) // 8] = s
print("labels recovered from 001D0390: %d (ids %d..%d)" % (len(labels), min(labels), max(labels)))
check("C1 id 12 = 'Read Json Data:' and id 14 = 'Invincible:'",
      labels.get(12, "").startswith("Read Json Data") and labels.get(14, "").startswith("Invincible"),
      "%r / %r" % (labels.get(12), labels.get(14)))

LO = 0x008FCE00
tab = [[struct.unpack_from("<I", d, off(LO) + (r * 0x16 + c) * 4)[0] for c in range(0x16)] for r in range(14)]
missing = 0
for r, row in enumerate(tab):
    print("page %d:" % (r + 1))
    for c, v in enumerate(row):
        if v:
            lab = labels.get(v)
            missing += lab is None
            print("   row %2d id %3d  %s" % (c, v, lab if lab is not None else "(no label store)"))
used = {v for row in tab for v in row if v}
print("ids used %d, with a label store %d, without %d" % (len(used), len(used & set(labels)), len(used - set(labels))))
print("ids without a label store:", sorted(used - set(labels)))
check("C2 page 3 (the '0xDF, 0xE1..' run read as Loca/bin_menu ids) carries console labels, not resource names",
      sum(1 for v in tab[2] if v in labels) >= 18,
      "%d of %d entries labelled" % (sum(1 for v in tab[2] if v in labels), sum(1 for v in tab[2] if v)))
print("FAILS %d" % FAILS)
