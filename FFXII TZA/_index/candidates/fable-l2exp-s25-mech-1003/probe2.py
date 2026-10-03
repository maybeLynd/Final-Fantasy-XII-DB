"""probe2.py - FABLE scratch: callers of 0030BF20 and context; the C-path installers of +0x6E0."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img, text_refs, data_refs, fmt_ref, disp_sweep  # noqa: E402

img = Img.load()
for t in (0x0030BF20, 0x00377C20, 0x0030BCD0):
    refs, unc = text_refs(img, t)
    print("== %08X: %d refs, %d unconfirmed, data %d" % (t, len(refs), len(unc), len(data_refs(img, t))))
    for r in refs[:80]:
        print("   " + fmt_ref(r))
for r in disp_sweep(img, 0x6E0, 8):
    if r[3] & 2:
        print("W +0x6E0 %08X %-44s fn=%s" % (r[0], r[1], ("%08X" % r[4]) if r[4] else "-"))
for disp in (0x6F8, 0x748, 0x6E8, 0x6F0):
    for r in disp_sweep(img, disp):
        if r[3] & 2 and r[4] and 0x00230000 <= r[4] < 0x00330000:
            print("W +0x%X %08X %-44s fn=%08X" % (disp, r[0], r[1], r[4]))
