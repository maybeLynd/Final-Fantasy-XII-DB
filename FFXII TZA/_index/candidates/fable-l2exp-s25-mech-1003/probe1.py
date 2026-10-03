"""probe1.py - FABLE scratch: raw reference index for the S-25 set selector and switch (not the check)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img, text_refs, data_refs, fmt_ref, disp_sweep  # noqa: E402

img = Img.load()


def show(name, lo, hi=None):
    refs, unc = text_refs(img, lo, hi)
    print("== %s %08X: %d refs, %d unconfirmed" % (name, lo, len(refs), len(unc)))
    for r in refs:
        print("   " + fmt_ref(r))
    for u in unc:
        print("   UNCONFIRMED %08X" % u)
    d = data_refs(img, lo, hi)
    print("   data: %d %s" % (len(d), [("%s %08X %s" % (s, a, k)) for s, a, k, v in d][:12]))


show("selector 00305AB0", 0x00305AB0)
show("walk 00305CC0", 0x00305CC0)
show("switch 002FDDA0", 0x002FDDA0)
show("static set 01EEC320", 0x01EEC320, 0x01EEC370)
show("static set 01EEC370", 0x01EEC370, 0x01EEC3C0)
show("fallback rec 01EEC298", 0x01EEC298, 0x01EEC2B0)
show("directory slot 02EBF168", 0x02EBF168, 0x02EBF170)
show("party sets 02089378", 0x02089378, 0x02089378 + 40 * 0x170)
show("resolver 0020E600", 0x0020E600)
show("bit22 helper 00308270", 0x00308270)
for disp in (0x6B5, 0x6E0, 0x6E8, 0x6F0, 0x6F8, 0x748):
    rows = disp_sweep(img, disp)
    print("== disp +0x%X: %d sites" % (disp, len(rows)))
    if disp in (0x6B5,):
        for r in rows:
            print("   %08X %-40s size=%d acc=%d fn=%s %s" % (r[0], r[1], r[2], r[3], ("%08X" % r[4]) if r[4] else "-", r[5]))
