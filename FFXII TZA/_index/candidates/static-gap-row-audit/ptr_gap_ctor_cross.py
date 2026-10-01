"""Cross-check PTR/PARRAY-routed types' gap rows with an INDEPENDENT seed: census_receiver_fixpoint SEED=ctor on the
type's constructor (from the types.tsv ctor column: 'proc=XXXXXXXX' or the first 8-hex token). Reports every
(displacement, width) the ctor-seeded census reaches inside a row the store calls unobserved."""
import csv
import io
import json
import os
import re
import subprocess
import sys

T = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_types"
GFZ = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
OUT = r"C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos\7af7f6f5-0967-4b0e-aef9-d5a1b93313e1\scratchpad\ctorx"
os.makedirs(OUT, exist_ok=True)
types = {r["type"]: r for r in csv.DictReader(io.open(T + r"\types.tsv", encoding="utf-8"), delimiter="\t")}
gaps = {}
for r in csv.DictReader(io.open(T + r"\fields.tsv", encoding="utf-8"), delimiter="\t"):
    t = r["type"]
    route = types.get(t, {}).get("route") or ""
    if not re.match(r"(PTR|PARRAY) 0x[0-9A-Fa-f]+(\s|$)", route):
        continue
    if r["name"].lower().startswith(("unobserved", "gap", "pad")) or "no censused access" in r["meaning"].lower() \
            or "not reached" in r["meaning"].lower():
        try:
            gaps.setdefault(t, []).append((int(r["offset"], 16), int(r["size"]), r["name"]))
        except ValueError:
            pass
report = []
for t, gl in sorted(gaps.items()):
    ctor = types[t].get("ctor") or ""
    m = re.search(r"proc=([0-9A-Fa-f]{8})", ctor) or re.search(r"\b(00[0-9A-Fa-f]{6})\b", ctor)
    if not m:
        report.append((t, "no ctor address", []))
        continue
    c = m.group(1).upper()
    ext = int(types[t]["size"], 16)
    js = os.path.join(OUT, "%s.json" % t)
    env = dict(os.environ, SEED="ctor", EMIT_JSON=js)
    try:
        subprocess.run([sys.executable, "census_receiver_fixpoint.py", c, "0", hex(ext)], cwd=GFZ, env=env,
                       capture_output=True, timeout=900)
        d = json.load(open(js, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        report.append((t, "census failed at %s: %s" % (c, e), []))
        continue
    hits = []
    for k, sites in d.get("sites", {}).items():
        dp, w = map(int, k.split(":"))
        for (o, n, nm) in gl:
            if dp < o + n and dp + max(w, 1) > o:
                hits.append((nm, "+0x%X" % dp, w, sorted(sites)[:2]))
    report.append((t, "ctor %s converged=%s disp=%d" % (c, d.get("converged"), len(d.get("sites", {}))), hits))
for t, st, hits in report:
    print("%-34s %s  gap-hits=%d %s" % (t, st, len(hits), hits[:4]))
print("types with ctor-census hits inside gap rows:", sum(1 for r in report if r[2]))
