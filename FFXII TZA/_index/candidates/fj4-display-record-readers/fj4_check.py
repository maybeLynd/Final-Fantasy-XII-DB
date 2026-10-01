"""fj4_check.py - FJ-4: which code reads which field of the nine unit-display records in the menu block
(FABLE, Claude Opus 5.5, 2026-09-27). Static; runs fj4_record_readers.py and checks its report.
  C1 control: the builder 00283270 itself reads the type +0x60 of the records it fills, and 00283E40 (the party
     panel, which reads the records directly) is found at HP +0x20 and MP +0x2C.
  C2 the readers of the named fields, following record pointers into callees and out of the two record-returning
     accessors 00282DF0 / 00282E10:
       +0x20 HP, +0x24 effective max, +0x2C MP, +0x30 capacity: 00283E40 only
       +0x44 status presence: 00283E40, 002C5660, 002C56F0
       +0x86 charges: 00283E40, 00583D60;  +0x87 bars: 00283E40, 0055BFF0, 0055CD40, 00583D60
       +0x90 experience, +0x94 to next level: 002C1000
       +0x9A..+0xAA the five equipment words' high halves: 002CA7C0, 0057B1A0
       +0xB0 LP: 00283E40, 002C1000, 00560210, 005618E0;  +0xBA level: 00283E40, 00583D60;  +0xBB licence count: 0055BFF0, 0055CD40
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
out = subprocess.run([sys.executable, str(HERE / "fj4_record_readers.py")], capture_output=True, text=True).stdout
got = {}
for l in out.splitlines():
    m = re.match(r"\+0x([0-9A-F]{2}) w\[[^\]]*\]: \d+ reads, \d+ functions: (.*)$", l.strip())
    if m: got[int(m.group(1), 16)] = set(m.group(2).split())
acc = re.search(r"record-returning accessors: \[(.*)\]", out)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("C1 control: the builder reads +0x60; the party panel reads HP and MP",
      "00283270" in got.get(0x60, ()) and "00283E40" in got.get(0x20, ()) and "00283E40" in got.get(0x2C, ()))
want = {0x20: {"00283E40"}, 0x24: {"00283E40"}, 0x2C: {"00283E40"}, 0x30: {"00283E40"},
        0x44: {"00283E40", "002C5660", "002C56F0"}, 0x86: {"00283E40", "00583D60"},
        0x87: {"00283E40", "0055BFF0", "0055CD40", "00583D60"}, 0x90: {"002C1000"}, 0x94: {"002C1000"},
        0x9A: {"002CA7C0", "0057B1A0"}, 0x9E: {"002CA7C0", "0057B1A0"}, 0xA2: {"002CA7C0", "0057B1A0"},
        0xA6: {"002CA7C0", "0057B1A0"}, 0xAA: {"002CA7C0", "0057B1A0"},
        0xB0: {"00283E40", "002C1000", "00560210", "005618E0"}, 0xBA: {"00283E40", "00583D60"}, 0xBB: {"0055BFF0", "0055CD40"}}
bad = {"+0x%02X" % k: sorted(got.get(k, set()) ^ v) for k, v in want.items() if got.get(k, set()) != v}
check("C2 each named field's readers are exactly the listed functions; accessors 00282DF0 / 00282E10",
      not bad and acc and "00282DF0" in acc.group(1) and "00282E10" in acc.group(1), str(bad))
print("FAILS", fails)
sys.exit(1 if fails else 0)
