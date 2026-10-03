"""member_census.py [--min N] - unexplained members of every declared family, per page, with the scope guard's verdict and
whether OPUS already wrote packs for that family (inbox/ee/<page slug>-<family slug>-*.md). OPUS, 2026-10-03."""
import glob
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402
import f_pack  # noqa: E402
import mem_pack as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
mn = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 5
exp, _ = M.explained()
sizes = L.sizes()
rows = []
for p in glob.glob(os.path.join(cl.DB, "**", "*.md"), recursive=True):
    rel = os.path.relpath(p, cl.DB).replace(os.sep, "/")
    if rel.startswith("_"):
        continue
    head = io.open(p, encoding="utf-8", errors="replace").read(4000)
    if "function_families:" not in head:
        continue
    try:
        fams = M.families(rel)
    except Exception:
        continue
    for name, path in fams:
        if not os.path.exists(path):
            continue
        fs = [f for f in M.members(path) if f not in exp and f in sizes]
        if len(fs) < mn:
            continue
        slug = f_pack.slug_of(rel) + "-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        packed = len(glob.glob(os.path.join(HERE, "inbox", "ee", slug + "-*.md")))
        rows.append((len(fs), sum(sizes[f] for f in fs), rel, name, packed))
guard = {}
for n, b, rel, name, packed in sorted(rows, reverse=True):
    if rel not in guard:
        r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "scope_guard.py"), rel, "--json"],
                           capture_output=True, text=True)
        try:
            guard[rel] = json.loads(r.stdout)[0]["verdict"]
        except Exception:
            guard[rel] = "?"
    print("%5d %8d B  %-5s packs=%-2d %s  [%s]" % (n, b, guard[rel], packed, rel, name))
