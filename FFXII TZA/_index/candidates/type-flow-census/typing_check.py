"""Declared type against the read instruction family, over every flow-census receipt beside this file (OPUS, 2026-09-27).

For each non-DISCOVERED 4-byte row of a type with a receipt (cpe-flow-accesses.tsv for CPostEffect, flow-<TYPE>.tsv for
the others), take the census's reads that start at the row's offset and are no wider than it.
  T1 REGRESSION: no row declared as a non-float scalar is read ONLY by scalar-single float instructions (at least two
     reads). This rejects the 2026-09-25 width-only census's uint32 default on floats; it FAILS on the store before the
     CPostEffect retype.
  P  positive control: a row already declared float (CPostEffect +0x6E4 glareLuminance) passes, being read as float
With --apply the offending rows are retyped to float in the store (FIELDS_PATH or --fields), their evidence keeping the
old type and the read count.
Not claimed: what the fields mean; rows read through a register copy only (a float moved as bits) are not judged.
"""
import csv, glob, os, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
FIELDS = Path(args[args.index("--fields") + 1]) if "--fields" in args else Path(os.environ.get("FIELDS_PATH") or HERE.parents[2] / "_types" / "fields.tsv")
APPLY = "--apply" in args
FLOAT = {"movss", "addss", "subss", "mulss", "divss", "comiss", "ucomiss", "maxss", "minss", "sqrtss", "cvtss2sd", "cvttss2si", "cvtss2si"}
recs = {"CPostEffect": HERE / "cpe-flow-accesses.tsv"}
for p in glob.glob(str(HERE / "flow-*.tsv")): recs[Path(p).name[5:-4]] = Path(p)
lines = FIELDS.read_bytes().decode("utf-8").splitlines(keepends=True)
def scan():
    bad = []; good_float = []
    idx = collections.defaultdict(list)
    for i, l in enumerate(lines):
        c = l.rstrip("\r\n").split("\t")
        if len(c) > 8 and c[0] in recs and c[6] != "DISCOVERED" and c[1].lower().startswith("0x") and c[2] == "4":
            idx[c[0]].append((i, int(c[1], 16), c[4], c[3]))
    for T, rs in idx.items():
        acc = [a for a in csv.DictReader(open(recs[T], encoding="latin1"), delimiter="\t")
               if "r" in a["kind"] and not a["field"].startswith("-")]
        by = collections.defaultdict(list)
        for a in acc: by[int(a["field"], 16)].append(a)
        for i, off, ty, name in rs:
            reads = [a for a in by.get(off, []) if int(a["width"]) <= 4]
            if len(reads) < 2: continue
            fl = [a for a in reads if a["instruction"].split()[0] in FLOAT]
            if ty in ("float", "f32"):
                if fl: good_float.append((T, off, name))
            elif len(fl) == len(reads):
                bad.append((i, T, off, name, ty, len(reads), sorted({a["instruction"].split()[0] for a in reads}), reads[0]["site"]))
    return bad, good_float
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
bad, good = scan()
if APPLY and bad:
    for i, T, off, name, ty, n, ops, site in bad:
        l = lines[i]; eol = l[len(l.rstrip("\r\n")):]; c = l.rstrip("\r\n").split("\t")
        c[4] = "float"
        c[8] += (" || RETYPED 2026-09-27 (OPUS): was '%s' - every read in the flow census is a scalar-single float instruction "
                 "(%d reads: %s; e.g. %s); the uint32 was the 2026-09-25 width-only census default. Control "
                 "_index/candidates/type-flow-census/typing_check.py T1." % (ty, n, "/".join(ops), site))
        lines[i] = "\t".join(c) + eol
    FIELDS.write_bytes("".join(lines).encode("utf-8"))
    print("retyped", len(bad), "rows")
    lines = FIELDS.read_bytes().decode("utf-8").splitlines(keepends=True)
    bad, good = scan()
check("T1 no non-float 4-byte row is read only as float", not bad,
      "(%d: %s)" % (len(bad), ", ".join("%s+0x%X" % (b[1], b[2]) for b in bad[:6])))
check("P a declared float row is read as float (CPostEffect +0x6E4)", ("CPostEffect", 0x6E4, "glareLuminance") in good)
print("FAILS", fails)
sys.exit(1 if fails else 0)
