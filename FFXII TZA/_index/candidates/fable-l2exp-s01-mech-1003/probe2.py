"""probe2.py - FABLE scratch: overlap sweep around +0x113C, the class ctor, AsyncJobManager ensure callers."""
from rawref import Img, text_refs, data_refs, fmt_ref, disp_sweep

img = Img.load()
for d in range(0x1130, 0x1140):
    for x in disp_sweep(img, d):
        site, text, size, acc, fn, st = x
        if d + size > 0x113C and d <= 0x113C:
            print("OVERLAP d=%X  %08X  %-45s size=%d acc=%d fn=%s %s" % (d, site, text, size, acc,
                                                                       fn and "%08X" % fn, st))
print("-- disp 0x1130 / 0x1138 all widths")
for d in (0x1130, 0x1138):
    for x in disp_sweep(img, d):
        site, text, size, acc, fn, st = x
        print("d=%X  %08X  %-45s size=%d acc=%d fn=%s %s" % (d, site, text, size, acc, fn and "%08X" % fn, st))
for f in (0x008C5760, 0x0019A0A0, 0x0019A170, 0x00228480):
    refs, unc = text_refs(img, f)
    print("== %08X refs %d unc %s" % (f, len(refs), unc))
    for r in refs:
        print("   " + fmt_ref(r))
    for dd in data_refs(img, f):
        print("   data %s %08X %s %X" % dd)
