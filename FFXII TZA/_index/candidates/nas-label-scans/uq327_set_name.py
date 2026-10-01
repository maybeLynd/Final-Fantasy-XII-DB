"""uq327_set_name.py - UQ-327 (is the sixth virtual of the two EASTL allocator classes `set_name`?): the shipped-artefact
scan requirement 3 asks for when the residue is a LABEL (FABLE, Claude Opus 5.5, 2026-09-26).

The slot is proven, and its body is the folded `ret 0` stub `0016D6A0`, which carries no identity. The name `set_name` is
a tier-6 inference from EASTL's public interface. A shipped artefact could still name it.
  S1 the exe carries no method-name string for the allocator interface: `set_name` and `get_name` occur nowhere (ASCII
     or UTF-16), while the class names do (RTTI `.?AVallocator@eastl@@`, `.?AVallocator_memory_log@eastl@@`) - MSVC
     RTTI records class names, never method names. Control: the class names are found.
  S2 none of the text-like files of the full nine-language extract contains `set_name`.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
EXTRACT = Path("D:/FFXII_TZA_extract")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
u16 = lambda s: s.encode("utf-16le")
check("S1 no set_name / get_name string (ASCII or UTF-16)",
      not any(re.search(p, d, re.I) for p in (rb"set_name", rb"get_name", re.escape(u16("set_name")), re.escape(u16("get_name")))))
check("S1 control: the allocator class names are present",
      b".?AVallocator@eastl@@" in d and b".?AVallocator_memory_log@eastl@@" in d)
if not EXTRACT.exists():
    check("S2 extract present", False, str(EXTRACT)); print("FAILS", fails); sys.exit(1)
EXT = {".txt", ".ini", ".csv", ".json", ".xml", ".h", ".cfg"}
n = 0; hits = []
for dp, dn, fn in os.walk(EXTRACT):
    for f in fn:
        if os.path.splitext(f)[1].lower() in EXT:
            n += 1
            if b"set_name" in open(os.path.join(dp, f), "rb").read(): hits.append(f)
check("S2 no text-like shipped file contains set_name", hits == [] and n > 10000, "%d files, hits %s" % (n, hits[:3]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
