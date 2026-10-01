#!/usr/bin/env python3
"""contradiction_index.py - extract, validate and query the contradiction ledger.

The gap this closes
-------------------
Charter §7 requires the knowledge to answer *"all contradictions involving a subsystem"*.
`knowledge_db.py queries` has listed that as **unsupported** since the schema was built, with the
note *"Contradictions are recorded as prose corrections in AUDIT-LOG.md and as in-document
strikethrough. There is no contradiction record type. This is the single biggest gap."*

It is a real corpus, not a hypothetical one. Across the database:

    117 of 219 documents contain a correction marker
    251 strikethrough spans
    165 DATED correction headers outside the audit log

**This project overturns its own claims often enough that the history is evidence**, and it was
greppable only.

What is extracted mechanically, and what is not
----------------------------------------------
A dated header - `CORRECTED 2026-09-02`, `RETRACTED …`, `SUPERSEDED …`, `WITHDRAWN …`,
`OVERTURNED …` - gives, with no judgement at all: the **document**, the **line**, the **kind** and
the **date**. Those four fields are filled by this tool.

**`claim`, `correction` and `instrument` are not extractable from prose and are left
`UNSUMMARISED`.** A summary written by a regex would be a fabrication with a citation attached. The
ledger therefore starts mostly empty in those columns and **says how empty** on every run.

`instrument` is the column worth filling. This project's wrong answers have repeatedly come from a
wrong *instrument* rather than a wrong reading - an `E8`-only reachability scan, endpoint-subtraction
arithmetic, a linear register taint, an ABI-violating stub, a leaf-name merge. A ledger that can be
asked *"which instrument has produced the most wrong answers"* is knowledge this database does not
otherwise hold.
"""
import argparse
import collections
import io
import os
import re
import sys

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
DB = os.path.join(ROOT, "Database", "FFXII TZA")
LEDGER = os.path.join(DB, "_index", "CONTRADICTIONS.tsv")

KINDS = ("CORRECTED", "RETRACTED", "SUPERSEDED", "WITHDRAWN", "OVERTURNED")
HEAD = re.compile(r"\b(%s)\s+(20\d\d-\d\d-\d\d)" % "|".join(KINDS))
COLUMNS = ["id", "date", "kind", "category", "document", "line", "claim", "correction",
           "instrument", "addresses"]


def snippet(line):
    s = re.sub(r"[`*~>#\[\]]", "", line).strip()
    return (s[:150] + "…") if len(s) > 150 else s


def extract(db):
    out = []
    for root, dirs, files in os.walk(db):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), db).replace("\\", "/")
            if rel.startswith("_index/AUDIT-LOG"):
                continue          # the audit log is the narrative; documents are the claims
            lines = io.open(os.path.join(root, fn), encoding="utf-8",
                            errors="replace").read().split("\n")
            for n, line in enumerate(lines, 1):
                m = HEAD.search(line)
                if not m:
                    continue
                cat = rel.split("/")[0]
                addrs = ",".join(sorted(set(re.findall(r"\b(0[0-9A-F]{7})\b", line))))
                out.append({"date": m.group(2), "kind": m.group(1), "category": cat,
                            "document": rel, "line": str(n), "claim": snippet(line),
                            "correction": "UNSUMMARISED", "instrument": "UNSUMMARISED",
                            "addresses": addrs})
    out.sort(key=lambda r: (r["date"], r["document"], int(r["line"])))
    for i, r in enumerate(out, 1):
        r["id"] = "CON-%03d" % i
    return out


def read_ledger(path):
    if not os.path.exists(path):
        return []
    rows, head = [], None
    for line in io.open(path, encoding="utf-8", errors="replace").read().split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        if head is None:
            head = line.split("\t")
            continue
        rows.append(dict(zip(head, line.split("\t") + [""] * len(head))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["extract", "status", "by-category", "by-instrument"])
    ap.add_argument("--db", default=DB)
    ap.add_argument("--ledger", default=LEDGER)
    a = ap.parse_args()

    if a.command == "extract":
        found = extract(a.db)
        existing = {(r["document"], r["line"]): r for r in read_ledger(a.ledger)}
        kept = 0
        for r in found:
            old = existing.get((r["document"], r["line"]))
            if old:
                # a hand-written summary is never overwritten by the extractor
                for c in ("claim", "correction", "instrument"):
                    if old.get(c) and old[c] != "UNSUMMARISED":
                        r[c] = old[c]
                        kept += 1
        with io.open(a.ledger, "w", encoding="utf-8", newline="\n") as f:
            f.write("# CONTRADICTIONS.tsv - claims this database has overturned.\n")
            f.write("#\n")
            f.write("# date/kind/category/document/line/addresses are EXTRACTED MECHANICALLY from\n")
            f.write("# dated correction headers by contradiction_index.py. Re-running preserves any\n")
            f.write("# hand-written claim/correction/instrument and refills the rest.\n")
            f.write("#\n")
            f.write("# claim/correction/instrument are UNSUMMARISED until a human writes them. A\n")
            f.write("# summary produced by a regex would be a fabrication with a citation attached.\n")
            f.write("#\n")
            f.write("# `instrument` is the column worth filling: which tool or method produced the\n")
            f.write("# wrong answer. That is the query this ledger exists for.\n")
            f.write("\t".join(COLUMNS) + "\n")
            for r in found:
                f.write("\t".join(r.get(c, "") for c in COLUMNS) + "\n")
        print("extracted %d dated correction(s) into %s" % (len(found), a.ledger))
        print("hand-written summary cells preserved: %d" % kept)
        return 0

    rows = read_ledger(a.ledger)
    if not rows:
        sys.stderr.write("no ledger at %s - run `extract` first\n" % a.ledger)
        return 2

    if a.command == "status":
        n = len(rows)
        summ = sum(1 for r in rows if r.get("correction", "") not in ("", "UNSUMMARISED"))
        inst = sum(1 for r in rows if r.get("instrument", "") not in ("", "UNSUMMARISED"))
        print("contradiction records            : %d" % n)
        print("  with a written correction      : %d  (%.1f %%)" % (summ, 100.0 * summ / n))
        print("  with a named instrument        : %d  (%.1f %%)" % (inst, 100.0 * inst / n))
        print("  UNSUMMARISED                   : %d" % (n - summ))
        print()
        k = collections.Counter(r["kind"] for r in rows)
        for kk, v in k.most_common():
            print("  %-11s %4d" % (kk, v))
        return 0

    if a.command == "by-category":
        c = collections.Counter(r["category"] for r in rows)
        print("  category                              corrections")
        for kk, v in c.most_common():
            print("  %-38s %4d" % (kk, v))
        return 0

    if a.command == "by-instrument":
        c = collections.Counter(r["instrument"] for r in rows
                                if r.get("instrument", "") not in ("", "UNSUMMARISED"))
        if not c:
            print("no record names an instrument yet - that column is the point of this ledger")
            return 0
        print("  instrument that produced the wrong answer          times")
        for kk, v in c.most_common():
            print("  %-50s %4d" % (kk[:50], v))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
