"""The file-schema page's Route 2 sentence: the class-descriptor globals read as zeroes because they have no file bytes
(SWE2-DATA 2026-09-30), static.
  S1 .data's SizeOfRawData ends below 02CA9DA0, so the span 02CA9DA0..02EBA030 is the section's virtual tail: the
     loader zero-fills it and the file carries nothing for it;
  S2 every class-descriptor global in the recovered field schema (phyre-field-schema.tsv, column class_obj) lies in
     that tail (no file offset);
  C1 control: a type record the same table names below the raw end (01F2E5A0) has file bytes and they are not all zero,
     so S2 can tell an initialised global from a zero-filled one.
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, secs, BASE  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


raw_end = [BASE + va + rs for n, va, vs, ro, rs in secs if n == ".data"][0]
check("S1 .data raw bytes end below the descriptor span", raw_end < 0x02CA9DA0 and off(0x02CA9DA0) is None
      and off(0x02EBA030) is None, "raw end %08X" % raw_end)
TSV = os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                   "phyre-field-schema.tsv")
rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
objs = sorted(set(int(r["class_obj"], 16) for r in rows if r["class_obj"]))
inside = [a for a in objs if 0x02CA9DA0 <= a <= 0x02EBA030]
tail = [a for a in objs if off(a) is None]
print("   %d distinct class-descriptor globals in the schema; %d inside the span; %d with no file bytes" % (
    len(objs), len(inside), len(tail)))
check("S2 every class-descriptor global has no file bytes", objs and len(tail) == len(objs))
o = off(0x01F2E5A0)
check("C1 control: 01F2E5A0 has file bytes, not all zero", o is not None and any(d[o:o + 0x40]))
print("RESULT the descriptors read as zeroes because they sit in .data's zero-filled virtual tail")
print("FAILS %d" % FAILS)
