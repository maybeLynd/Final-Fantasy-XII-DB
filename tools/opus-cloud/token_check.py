"""token_check.py REC [REC...] - after hand corrections, re-apply interior_ingest's text rules to a record's rows: every
8-hex address a row names must appear in its body's listing, and the text stays within 1200 characters (OPUS, 2026-10-03)."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import listing as L  # noqa: E402

C = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "_index", "candidates"))
ADDR = re.compile(r"\b[0-9A-F]{8}\b")
rc = 0
for rec in sys.argv[1:]:
    d = json.load(open(os.path.join(C, rec, "rows.json"), encoding="utf-8"))
    bad = []
    for r in d["rows"]:
        lines, toks = L.listing(int(r["fn"], 16))
        known = {t.upper() for t in (toks or [])} | set(ADDR.findall("\n".join(lines).upper()))
        for a in sorted(set(ADDR.findall(r["text"]))):
            if a != r["fn"] and a not in known:
                bad.append((r["fn"], a))
        if len(r["text"]) > 1200:
            bad.append((r["fn"], "len %d" % len(r["text"])))
    print(rec, "rows", len(d["rows"]), "problems", bad or "none")
    rc |= bool(bad)
sys.exit(rc)
