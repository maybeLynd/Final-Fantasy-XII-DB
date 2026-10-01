"""rwr_recipes.py - decode recipes 25 / 26 and their calculator slots from the image (FABLE, 2026-09-30).
Run from Database/Tools/work/FABLE/pub140-scratch (borrows disw.py's image loader and section-aware off()).
Control: recipe pointer 25 must equal 0x01EF9E60 and 26 must equal 0x01EF9EB0 (the page's published addresses)."""
import sys, struct
import os as _os
# disw.py (the image loader) lives in Database/Tools/work/FABLE/pub140-scratch; run from there, or from the DD record folder
for _d in (_os.getcwd(), _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work",
                                       "FABLE", "pub140-scratch"),
           r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/FABLE/pub140-scratch"):
    if _os.path.isfile(_os.path.join(_d, "disw.py")):
        _os.chdir(_d)
        break
sys.argv = ["x", "0"]
exec(open("disw.py").read().split("fn = int")[0])
q = lambda va: struct.unpack_from("<Q", d, off(va))[0]
i32 = lambda va: struct.unpack_from("<i", d, off(va))[0]
RECIPES, SLOTS = 0x01EF96C0, 0x01EFA5C0
for r, want in ((25, 0x01EF9E60), (26, 0x01EF9EB0)):
    p = q(RECIPES + 8 * r)
    assert p == want, "control failed: recipe %d -> %08X, page says %08X" % (r, p, want)
    lists, cur, a = [], [], p
    while len(lists) < 2 and a < p + 0x200:
        v = i32(a)
        a += 4
        if v == -1:
            if cur or lists:
                lists.append(cur)
                cur = []
            continue
        cur.append(v)
    print("control ok; recipe %d -> %08X  preview %s  committed %s" % (r, p, lists[0] if lists else None, lists[1] if len(lists) > 1 else None))
    for name, lst in zip(("preview", "committed"), lists):
        for s in lst:
            f = q(SLOTS + 8 * s)
            print("   %-9s slot %3d -> %08X %s (%s B)" % (name, s, f, names.get(f, "?"), funcs.get(f, "?")))
