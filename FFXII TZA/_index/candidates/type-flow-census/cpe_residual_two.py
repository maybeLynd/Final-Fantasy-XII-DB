"""cpe_residual_two.py - OPUS (Claude Opus 5.5), 2026-09-28. Two CPostEffect 'mixed' rows that the existing rules settle
once applied with the typed-access rule of ramp-channel-recut (a plain mov / movd / movq carries width only).

  T1 +0x600 (8): reads are movss at +0x600 and +0x604 and tile the span; the other accesses are a movss store, one qword
     store over both, and 16-byte moves that end (from +0x5F4) or start at +0x604 - all on the new boundaries (cpe_recut.py's
     full-tile case, which never reached this span) -> +0x600 float, +0x604 float
  T2 +0x5A0 (8): +0x5A4 is read by comiss / movss and by one plain mov; the plain mov carries width only, so the typed
     reads make it a float (cpe_partial_recut.py rejected it as 'conflicting read types' because it typed the mov as
     uint32). +0x5A0 has no read (one 4-byte write) and stays a DISCOVERED remainder
  C  controls from the same receipt stay 'mixed': +0x730 (a dword also read as two words) and +0x20C (a dword also read
     at its top byte)
  S  REGRESSION: the store has +0x600 / +0x604 / +0x5A4 float and +0x5A0 u8[4] DISCOVERED (FAILS before the patch)
Usage: python cpe_residual_two.py [--patch]
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIELDS = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/type-flow-census/cpe_residual_two.py"
R = list(csv.DictReader(open(os.path.join(HERE, "cpe-flow-accesses.tsv"), encoding="utf-8"), delimiter="\t"))
A = sorted({(int(r["field"], 16), int(r["width"]), r["kind"], r["instruction"].split()[0], r["site"]) for r in R
            if not r["field"].startswith("-") and r["kind"] != "addr"})
def near(o, n): return [a for a in A if a[0] < o + n and a[0] + a[1] > o]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
FLOATM = lambda m: m.endswith("ss") or m in ("comiss", "ucomiss")
a600 = near(0x600, 8)
reads600 = sorted({(a[0], a[1], a[3]) for a in a600 if "r" in a[2] and a[1] <= 8})
t1 = (reads600 == [(0x600, 4, "movss"), (0x604, 4, "movss")]
      and all(a[1] == 16 and 0x604 in (a[0], a[0] + a[1]) or a[0] in (0x600, 0x604) and a[0] + a[1] in (0x604, 0x608) for a in a600))
check("T1", t1, "+0x600 reads %s; every other access on 0x600 / 0x604 / 0x608 or a 16-byte move ending or starting at 0x604" % reads600)
a5a = near(0x5A0, 8)
r5a4 = sorted({a[3] for a in a5a if a[0] == 0x5A4 and "r" in a[2]})
t2 = (r5a4 == ["comiss", "mov", "movss"] and not [a for a in a5a if a[0] == 0x5A0 and "r" in a[2]]
      and all(a[0] in (0x5A0, 0x5A4) and a[1] == 4 for a in a5a))
check("T2", t2, "+0x5A4 read by %s (the plain mov is width only); +0x5A0 written only" % r5a4)
c730 = sorted({(a[0], a[1]) for a in near(0x730, 4) if "r" in a[2]}); c20c = sorted({(a[0], a[1]) for a in near(0x20C, 4) if "r" in a[2]})
check("C", c730 == [(0x730, 2), (0x730, 4), (0x732, 2)] and (0x20F, 1) in c20c and (0x20C, 4) in c20c,
      "+0x730 reads %s and +0x20C reads %s overlap and stay 'mixed'" % (c730, c20c))
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    for o in (0x600, 0x5A0):
        i = next(i for i, l in enumerate(fl) if cells(l)[0] == "CPostEffect" and int(cells(l)[1], 16) == o)
        c = cells(fl[i])
        if not c[3].startswith("mixed"): continue
        eol = fl[i][len(fl[i].rstrip("\r\n")):]; w = len(c)
        def row(r): return "\t".join(r + [""] * (w - len(r))) + eol
        was = " || WAS %s %s %s %s: %s" % (c[1], c[2], c[3], c[4], c[5])
        if o == 0x600:
            new = [row(["CPostEffect", "0x%X" % f, "4", "field%X" % f, "float",
                        "read as float (movss) at %s; also stored by movss and by one qword store over +0x600..+0x607, and "
                        "reached by 16-byte moves from +0x5F4. Width and type from the read side; what it holds is not claimed." %
                        ", ".join(sorted({a[4] for a in a600 if a[0] == f and "r" in a[2]})[:3]),
                        "TYPE RESOLVED", "PROVEN", "CPOSTEFFECT RESIDUAL 2026-09-28 (OPUS, %s T1)%s" % (REC, was)]) for f in (0x600, 0x604)]
        else:
            new = [row(["CPostEffect", "0x5A0", "4", "unobservedSpan5A0", "u8[4]", "written 4 bytes only; no read in the flow census",
                        "DISCOVERED", "UNKNOWN", "CPOSTEFFECT RESIDUAL REMAINDER 2026-09-28 (OPUS, %s T2)" % REC]),
                   row(["CPostEffect", "0x5A4", "4", "field5A4", "float",
                        "read as float (comiss / movss) at %s; one plain 32-bit mov read carries width only. What it holds is not claimed." %
                        ", ".join(sorted({a[4] for a in a5a if a[0] == 0x5A4 and "r" in a[2] and a[3] != "mov"})[:3]),
                        "TYPE RESOLVED", "PROVEN", "CPOSTEFFECT RESIDUAL 2026-09-28 (OPUS, %s T2)%s" % (REC, was)])]
        fl[i:i + 1] = new
    open(FIELDS, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
F = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == "CPostEffect"}
check("S", all(F.get(o, [0] * 5)[4] == "float" for o in (0x600, 0x604, 0x5A4)) and F.get(0x5A0, [0] * 7)[6] == "DISCOVERED"
      and F[0x5A0][4] == "u8[4]", "the store has +0x600 / +0x604 / +0x5A4 float and +0x5A0 u8[4]")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
