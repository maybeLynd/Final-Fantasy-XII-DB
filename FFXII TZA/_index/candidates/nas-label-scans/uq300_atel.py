"""uq300_atel.py - UQ-300 (what the acronym ATEL stands for): the shipped-artefact scan requirement 3 asks for when the
residue is a LABEL (OPUS, 2026-09-16 precedent). FABLE, Claude Opus 5.5, 2026-09-26.

  A1 every printable ASCII run (>= 4) and UTF-16LE run in the shipping exe containing "atel" (any case). Expected: the
     only uses are the word itself: "ATEL CONTROL", Atel* function names and katano\\atel*.c source paths. No run
     spells out an expansion (a phrase whose words start A-T-E-L).
  A2 every text-like file (.txt .ini .csv .json .xml .h .cfg) under the full game extract (D:/FFXII_TZA_extract, all nine
     languages): files containing "atel", and any A-T-E-L initial phrase anywhere in them.
  A3 the name instrument's blind spot, stated: an expansion composed at run time from pieces would need a template
     or prefix string, and A1 lists every run containing the letters; none is a template.
Prints the findings and PASS/FAIL; exit 1 on any FAIL.
"""
import os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
EXTRACT = Path("D:/FFXII_TZA_extract")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
d = EXE.read_bytes()
runs = {m.group(0).decode("latin1") for m in re.finditer(rb"[\x20-\x7e]{4,160}", d) if re.search(rb"atel", m.group(0), re.I)}
runs |= {m.group(0).decode("utf-16le") for m in re.finditer(rb"(?:[\x20-\x7e]\x00){4,120}", d)
         if re.search("atel", m.group(0).decode("utf-16le"), re.I)}
atel = sorted(r for r in runs if re.search(r"(?<![a-z])atel", r, re.I))
print("exe runs using the word:", atel)
EXPAND = re.compile(r"\bA\w*[\s_-]+T\w*[\s_-]+E\w*[\s_-]+L\w*", re.I)
check("A1 planted positive: the phrase matcher fires on a made-up expansion",
      EXPAND.search("xx Active Time Event Logic yy") is not None and EXPAND.search("ATEL CONTROL") is None)
check("A1 no exe string spells an A-T-E-L phrase", not any(EXPAND.search(r) for r in runs))
check("A1 control: the word itself is found", "ATEL CONTROL" in runs and any("atelload" in r for r in runs))
if not EXTRACT.exists():
    check("A2 extract present", False, str(EXTRACT)); print("FAILS", fails); sys.exit(1)
EXT = {".txt", ".ini", ".csv", ".json", ".xml", ".h", ".cfg"}
n = 0; with_word = []; phrases = []
for dp, dn, fn in os.walk(EXTRACT):
    for f in fn:
        if os.path.splitext(f)[1].lower() in EXT:
            n += 1
            t = open(os.path.join(dp, f), "rb").read().decode("latin1")
            if re.search("atel", t, re.I): with_word.append(os.path.join(dp, f))
            for m in re.finditer(r"\bATEL\b", t): phrases.append((f, t[max(0, m.start() - 60):m.end() + 60]))
print("text-like files scanned:", n)
check("A2 no text-like shipped file contains 'atel'", with_word == [] and phrases == [], str(with_word[:5]))
check("A2 control: the scan saw the corpus", n > 10000, str(n))
print("FAILS", fails)
sys.exit(1 if fails else 0)
