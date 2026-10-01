"""OPUS's reviewer negatives for NAS package 6 (X-8, YEBIS's product version), 2026-09-27.

  E1 the image's UTF-16 strings (Y1 scans single-byte text): none mentions YEBIS / PPFX / yeblic / Silicon Studio;
     sensitivity - the scan finds the image's VS_VERSION_INFO strings, which are UTF-16
  E2 the version resource is the game's own (FileVersion / ProductVersion 1.0.4.0, SQUARE ENIX) - no library version
  E3 (install-dependent, skipped when the client folder is absent) no YEBIS / PPFX / Silicon DLL ships beside the
     executable, so no separate library carries a version resource; FFXII_TZA_GameSetting.exe mentions none of them
Usage: python nas6_extra.py [client_x64_folder]
"""
import os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
CLIENT = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII MP Mod/FFXII_TestClient1/x64")
W = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")
KEY = re.compile(r"(?i)yebis|ppfx|yeblic|silicon")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
wide = [m.group().decode("utf-16le", "ignore") for m in W.finditer(d)]
hits = [s for s in wide if KEY.search(s)]
check("E1 no UTF-16 string mentions YEBIS / PPFX / Silicon (sensitivity: the version-resource strings are found)",
      not hits and "VS_VERSION_INFO" in wide and "ProductVersion" in wide, "(%d UTF-16 strings)" % len(wide))
i = wide.index("ProductVersion") if "ProductVersion" in wide else -1
check("E2 the version resource is the game's own", i >= 0 and wide[i + 1] == "1.0.4.0" and "SQUARE ENIX CO., LTD." in wide)
if CLIENT.is_dir():
    dlls = [p.name for p in CLIENT.rglob("*.dll")]
    gs = CLIENT / "FFXII_TZA_GameSetting.exe"
    g = gs.read_bytes() if gs.is_file() else b""
    gh = [m.group() for m in re.finditer(rb"[\x20-\x7e]{4,}", g) if KEY.search(m.group().decode("latin1"))] + \
         [s for s in (m.group().decode("utf-16le", "ignore") for m in W.finditer(g)) if KEY.search(s)]
    check("E3 no YEBIS / PPFX / Silicon DLL in the install; the settings program names none",
          not [n for n in dlls if KEY.search(n)] and bool(g) and not gh, "(%d DLLs)" % len(dlls))
else:
    print("SKIP  E3 client folder not present")
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
