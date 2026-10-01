r"""nas6_yebis.py - review package 6: X-8's last residue, YEBIS's product version (FABLE, Claude Opus 5.5, 2026-09-27).

  Y1 every printable string of the image matching yebis / yeblic / ppfxlic / Silicon Studio is listed, and none holds a
     dotted number (no version literal).
  Y2 sensitivity: the same scanner finds the three banners whose versions are known - zlib 'inflate 1.2.11', Lua
     '5.2.1' and libvpx 'v1.6.0' - so a YEBIS banner would have been found.
  Y3 what the image does carry: the build line 'yeblic-ppfxlic-bl2015' in the source paths and the feature id
     'YEBIS_D3D11'; the __DATE__ 'Feb 18 2016' in the PPFX error format strings.
Exit 1 on any FAIL.
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
strs = [(m.start(), m.group()) for m in re.finditer(rb"[\x20-\x7e]{4,}", d)]
yeb = [s for o, s in strs if re.search(rb"yebis|yeblic|silicon ?studio|ppfxlic", s, re.I)]
check("Y1 no YEBIS-related string carries a version (%d strings)" % len(yeb),
      len(yeb) > 0 and not any(re.search(rb"\d+\.\d+", s) for s in yeb), str(sorted({s[:48] for s in yeb})))
known = {"zlib": rb"inflate 1\.2\.11", "lua": rb"Lua 5\.2\.1", "libvpx": rb"v1\.6\.0"}
found = {k: any(re.search(p, s) for o, s in strs) for k, p in known.items()}
check("Y2 sensitivity: the scanner finds the known banners", all(found.values()), str(found))
check("Y3 the image carries the build line and the build date, not a version",
      any(b"yeblic-ppfxlic-bl2015" in s for s in yeb) and any(b"YEBIS_D3D11" in s for s in yeb)
      and any(b"Feb 18 2016" in s for o, s in strs))
print("FAILS", fails); sys.exit(1 if fails else 0)
