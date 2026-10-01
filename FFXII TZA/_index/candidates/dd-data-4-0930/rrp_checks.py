"""Reflected render parameters page: the two uncited claims the DD read found (SWE2-DATA 2026-09-30), static + data.

  K1 keymap.ini (ConfigData of an installed copy of the game, D:/FFXII MP Mod/FFXII_TestClient1/ConfigData): its
     [Setting] section declares ButtonCount=16, AnalogCount=8, KeyCount=3, and [Button] / [Analog] / [KeyFunction]
     hold 16 / 8 / 3 numeric codes, [Mouse] holds Left / Middle / Right.
  F1 mMapShadowFlyingFadeRange / ...Speed (008FB030 / 008FB050) are looked up only in 001C7940 (four lea sites), each
     through the member lookup 001FF740 with a fall-back to the defaults document when the key is absent, and stored
     as floats into two globals, 02CB8414 (Range, 001C8FFF) and 02CB8410 (Speed, 001C9040).
  F2 no rip-relative instruction reads those two globals; the same sweep finds the two stores (positive control C1),
     so the absence is of rip-relative readers only - a base-register read is not excluded.
"""
import configparser, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis, raw_rip_refs, owner  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


cp = configparser.ConfigParser()
cp.optionxform = str
cp.read("D:/FFXII MP Mod/FFXII_TestClient1/ConfigData/keymap.ini")
st = cp["Setting"]
print("   keymap sections %s" % cp.sections())
check("K1 keymap.ini: 16 buttons, 8 analog codes, 3 key functions, mouse Left/Middle/Right",
      (st["ButtonCount"], st["AnalogCount"], st["KeyCount"]) == ("16", "8", "3")
      and len(cp["Button"]) == 16 and len(cp["Analog"]) == 8 and len(cp["KeyFunction"]) == 3
      and list(cp["Mouse"]) == ["Left", "Middle", "Right"])
names = raw_rip_refs(0x008FB030, 0x008FB06A)
print("   name refs %s" % ["%08X->%08X" % (r[0], r[3]) for r in names])
f = {x.address: x for x in dis(0x001C7940)}
check("F1 the two names are read only in 001C7940 and stored to 02CB8414 / 02CB8410",
      [r[0] for r in names] == [0x001C8FBF, 0x001C8FD6, 0x001C8FF8, 0x001C9017]
      and all(owner(r[0]) == 0x001C7940 for r in names)
      and f[0x001C8FC9].op_str == "0x1ff740" and f[0x001C8FFF].mnemonic == "movss"
      and f[0x001C9040].mnemonic == "movss")
g = raw_rip_refs(0x02CB8410, 0x02CB8418)
print("   global refs %s" % ["%08X %s" % (r[0], r[1]) for r in g])
check("C1 control: the sweep finds the two stores", sorted(r[0] for r in g if r[1] == "movss"
                                                          and r[2].startswith("dword ptr [rip")) == [0x001C8FFF, 0x001C9040])
check("F2 no rip-relative reader of either global", all(r[0] in (0x001C8FFF, 0x001C9040) for r in g))
print("RESULT keymap counts anchored; the flying-fade pair is read into two globals no rip-relative code reads")
print("FAILS %d" % FAILS)
