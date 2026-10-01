"""wsn_lists.py - dump the three authored status-id lists the stat rebuild 002FEF30 walks (FABLE, 2026-09-30).
Run from Database/Tools/work/FABLE/pub140-scratch (it borrows disw.py's image loader and section-aware off())."""
import sys
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
for va, n, reg, loop in ((0x00D10290, 16, "r12d", "002FF5B2-002FF63C"), (0x00D102A0, 16, "r13d", "002FF650-002FF6DA"),
                         (0x00D102B0, 12, "r14", "002FF6F0-002FF77A")):
    o = off(va)
    ids = list(d[o:o + n])
    print("%08X  %2d ids  -> %-4s  loop %s  ids %s" % (va, n, reg, loop, ids))
# control: the same off() reads a known .rdata constant the rebuild's neighbours use (10.0f at 008F8180)
import struct
print("control 008F8180 f32 =", struct.unpack_from("<f", d, off(0x008F8180))[0])
