"""Audit: every DISCOVERED gap row ('unobserved*' / 'gap' names or meanings saying no census reached it) on a type with a
STATIC or ARRAY route - does any rip-relative instruction target a byte inside it? Uses data_xref_scan.scan (no new scanner).
ARRAY routes: the gap is checked in every element (count from the route; skipped when the count is symbolic)."""
import collections
import csv
import io
import re
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import data_xref_scan as X  # noqa: E402

T = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_types"
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
G = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
types = {r["type"]: r for r in csv.DictReader(io.open(T + r"\types.tsv", encoding="utf-8"), delimiter="\t")}
bases = {}
for t, r in types.items():
    route = r.get("route") or ""
    m = re.match(r"STATIC 0x([0-9A-Fa-f]+)", route)
    if m:
        bases[t] = [int(m.group(1), 16)]
        continue
    m = re.match(r"ARRAY 0x([0-9A-Fa-f]+) stride=0x([0-9A-Fa-f]+) count=(\d+)", route)
    if m:
        b, s, c = int(m.group(1), 16), int(m.group(2), 16), int(m.group(3))
        if c <= 4096:
            bases[t] = [b + i * s for i in range(c)]
gaps = []
for r in csv.DictReader(io.open(T + r"\fields.tsv", encoding="utf-8"), delimiter="\t"):
    t = r["type"]
    if t not in bases:
        continue
    nm, mean = r["name"], r["meaning"].lower()
    if not (nm.lower().startswith(("unobserved", "gap", "pad")) or "no censused access" in mean or "not reached" in mean
            or "no observed access" in mean):
        continue
    try:
        o, n = int(r["offset"], 16), int(r["size"])
    except ValueError:
        continue
    gaps.append((t, o, n, nm))
want = {}
for t, o, n, nm in gaps:
    for b in bases[t]:
        for a in range(b + o, b + o + n):
            want[a] = (t, o, n, nm)
print("types with static/array routes:", len(bases), " gap rows:", len(gaps), " bytes:", len(want))
blob = open(EXE, "rb").read()
res = X.scan(blob, X.sections_of(blob), X.entries(G), set(want))
hit = collections.defaultdict(lambda: [0, set(), set()])
for a, hs in res.items():
    k = want[a]
    hit[k][0] += len(hs)
    for ins, mn, ops, f in hs:
        hit[k][1].add("%08X" % ins)
        hit[k][2].add("%08X" % f)
for (t, o, n, nm), (c, sites, fns) in sorted(hit.items(), key=lambda x: -x[1][0]):
    print("%-34s +0x%04X %4d %-22s refs=%-4d fns=%-3d e.g. %s" % (t, o, n, nm, c, len(fns), ",".join(sorted(sites)[:3])))
print("gap rows with direct references:", len(hit), "of", len(gaps))
