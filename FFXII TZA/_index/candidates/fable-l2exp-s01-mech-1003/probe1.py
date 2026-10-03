"""probe1.py - FABLE scratch: vtable listing and raw reference index for the S-01 mechanism functions."""
from rawref import Img, text_refs, data_refs, fmt_ref

img = Img.load()
VT = 0x008C5760
for i in range(31):
    v = img.u64(VT + 8 * i)
    print("slot %2d  %08X  %08X" % (i, VT + 8 * i, v))
for f in (0x0017CEB0, 0x0017D000, 0x0017CCD0, 0x0017CE50, 0x0017D090, 0x0017D4C0, 0x0022A0B0, 0x0017D6B0,
          0x0019B070, 0x0059A770, 0x0019B190, 0x0019B1F0, 0x00182F70, 0x00189000, 0x0018A840):
    refs, unc = text_refs(img, f)
    print("== %08X text refs %d unconfirmed %s" % (f, len(refs), ["%08X" % u for u in unc]))
    for r in refs:
        print("   " + fmt_ref(r))
    for d in data_refs(img, f):
        print("   data %s %08X %s %X" % d)
