"""SWE2-AUDIT-SEM: which inline bulk loops (inline_bulk.tsv) can cover the T1 / T2 targets?
constant-base loops: covered when base <= T < base + extent (+ the per-iteration store span); unknown trip count
with base below T within 1 MB is listed for reading. Non-constant bases are summarised by base form."""
import csv, collections
T = {"T1 0215EFF4": 0x0215EFF4, "T2 01E02804": 0x01E02804, "T2 01E02810": 0x01E02810}
rows = list(csv.DictReader(open("inline_bulk.tsv"), delimiter="\t"))
for name, t in T.items():
    print("==", name)
    for r in rows:
        if r["base_const"] == "-":
            continue
        b = int(r["base_const"], 16)
        lo, hi = int(r["store_lo"]), int(r["store_hi"])
        if r["extent"] != "?":
            ext = int(r["extent"], 16)
            if b + lo <= t < b + ext + hi:
                print("  COVERS", r["head"], r["base_def"], "extent", r["extent"])
        elif b <= t < b + 0x100000:
            print("  UNKNOWN-COUNT below target:", r["head"], r["base_def"], "stride", r["stride"])
nc = collections.Counter(r["base_const"] == "-" for r in rows)
print("loops with constant base / non-constant:", nc[False], nc[True])
