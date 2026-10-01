"""rwr_slots.py - which calculator slots (table 0x01EFA5C0, 202 x 8 B) point at a given function (FABLE, 2026-09-30).
Run from Database/Tools/work/FABLE/pub140-scratch. Control: slot 35 must be 003895D0 and slot 42 00389820."""
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
SLOTS = 0x01EFA5C0
tab = [struct.unpack_from("<Q", d, off(SLOTS + 8 * i))[0] for i in range(202)]
assert tab[35] == 0x003895D0 and tab[42] == 0x00389820, "control failed"
for want in (0x00389040, 0x00388FE0, 0x0038B220, 0x0038B6A0, 0x003896B0):
    print("%08X %-45s slots %s" % (want, names.get(want, "?"), [i for i, f in enumerate(tab) if f == want]))
