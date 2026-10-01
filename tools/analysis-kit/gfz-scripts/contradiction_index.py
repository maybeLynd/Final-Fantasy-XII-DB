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
import os
import re
import sys
import tempfile
from pathlib import Path
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
LEDGER = os.path.join(DB, "_index", "CONTRADICTIONS.tsv")

KINDS = ("CORRECTED", "RETRACTED", "SUPERSEDED", "WITHDRAWN", "OVERTURNED")
HEAD = re.compile(r"\b(%s)\s+(20\d\d-\d\d-\d\d)" % "|".join(KINDS))
COLUMNS = ["id", "date", "kind", "category", "document", "line", "claim", "correction",
           "instrument", "addresses", "source_header", "source_status"]
MANUAL = ("claim", "correction", "instrument", "addresses")


def snippet(line):
    s = re.sub(r"[`*~>#\[\]]", "", line).strip()
    return (s[:150] + "…") if len(s) > 150 else s


def extract(db):
    out = []
    for root, dirs, files in os.walk(db):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", "work"})
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), db).replace("\\", "/")
            if rel.startswith("_index/AUDIT-LOG"):
                continue          # the audit log is the narrative; documents are the claims
            lines = Path(root, fn).read_text(encoding="utf-8").split("\n")
            for n, line in enumerate(lines, 1):
                # This page explains the extractor and quotes example markers. Its
                # actual permanent corrections are Markdown headings, not examples.
                if rel.casefold() == "_index/contradiction-ledger.md" and not re.match(r"^#{1,6}\s", line):
                    continue
                m = HEAD.search(line)
                if not m:
                    continue
                cat = rel.split("/")[0]
                addrs = ",".join(sorted(set(re.findall(r"\b(0[0-9A-F]{7})\b", line))))
                out.append({"date": m.group(2), "kind": m.group(1), "category": cat,
                            "document": rel, "line": str(n), "claim": snippet(line),
                            "correction": "UNSUMMARISED", "instrument": "UNSUMMARISED",
                            "addresses": addrs, "source_header": " ".join(line.split()),
                            "source_status": "present"})
    out.sort(key=lambda r: (r["date"], r["document"], int(r["line"])))
    return out


def merge(found, existing):
    """Keep identities/history; refuse ambiguous adoption before touching the ledger.

    Legacy rows may adopt a unique exact snippet of their original source line.
    A hand-written claim is not a source anchor: ambiguous legacy rows require an
    explicitly reviewed source_header migration. Line numbers never identify rows.
    """
    ids = [r.get("id", "") for r in existing]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"CON-\d+", x) for x in ids):
        raise ValueError("existing ledger has duplicate or invalid IDs")
    def key(row):
        return row["document"].replace("\\", "/").casefold(), row.get("source_header", "")
    def group(row):
        return key(row)[0], row["date"], row["kind"]
    anchors = [key(r) for r in found]
    if len(set(anchors)) != len(anchors):
        raise ValueError("duplicate source anchors; explicit disambiguation required")
    old_anchors = [key(r) for r in existing if r.get("source_header")]
    if len(set(old_anchors)) != len(old_anchors):
        raise ValueError("existing ledger has duplicate source anchors")
    used, result, kept = set(), [], 0
    for old in existing:
        if old.get("source_header"):
            candidates = [i for i, row in enumerate(found) if key(row) == key(old)]
        else:
            candidates = [i for i, row in enumerate(found) if group(row) == group(old)
                          and row["claim"] == old.get("claim")]
        if len(candidates) > 1 or any(i in used for i in candidates):
            raise ValueError("ambiguous source adoption for " + old["id"])
        if candidates:
            i = candidates[0]
            used.add(i)
            row = dict(found[i], id=old["id"])
            for column in MANUAL:
                if old.get(column) and old[column] != "UNSUMMARISED":
                    row[column] = old[column]
                    kept += 1
        else:
            row = dict(old, source_status="missing" if old.get("source_header") else "legacy-unmatched")
        result.append(row)
    # A changed header in the same document/date/kind could be a renamed record,
    # not new history. Never guess or create a second identity for that case.
    unresolved = {group(r) for r in result if r.get("source_status") != "present"}
    if any(group(row) in unresolved for i, row in enumerate(found) if i not in used):
        raise ValueError("unmatched history overlaps new markers; review source_header anchors first")
    next_id = max((int(x.split("-")[1]) for x in ids), default=0) + 1
    for i, row in enumerate(found):
        if i not in used:
            result.append(dict(row, id="CON-%03d" % next_id))
            next_id += 1
    return result, kept


def read_ledger(path):
    if not os.path.exists(path):
        return []
    rows, head = [], None
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        if head is None:
            head = line.split("\t")
            if len(set(head)) != len(head) or set(head) - set(COLUMNS) or not set(COLUMNS[:10]) <= set(head):
                raise ValueError("unsupported or incomplete ledger columns")
            continue
        cells = line.split("\t")
        if len(cells) != len(head):
            raise ValueError("ledger row has the wrong cell count")
        rows.append(dict(zip(head, cells)))
    return rows


def write_ledger(path, rows, expected):
    """Atomic replacement, with a stale-input check and no lossy column coercion."""
    lines = ["# CONTRADICTIONS.tsv - stable identities and preserved correction history.",
             "# source_header anchors the normalized full source line; line is only a location.",
             "# Existing claim/correction/instrument/addresses cells survive extraction.",
             "# Missing sources retain their IDs and cells; ambiguous adoption aborts.",
             "\t".join(COLUMNS)]
    for row in rows:
        cells = [row.get(c, "") for c in COLUMNS]
        if any(any(ch in cell for ch in "\t\r\n") for cell in cells):
            raise ValueError("a ledger cell contains a tab or newline")
        lines.append("\t".join(cells))
    parent = os.path.dirname(os.path.abspath(path))
    fd, temporary = tempfile.mkstemp(prefix=".contradictions-", suffix=".tmp", dir=parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("\n".join(lines) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        actual = Path(path).read_bytes() if os.path.exists(path) else None
        if actual != expected:
            raise ValueError("ledger changed during extraction; retry under publication ownership")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["extract", "status", "by-category", "by-instrument"])
    ap.add_argument("--db", default=DB)
    ap.add_argument("--ledger", help="defaults to <db>/_index/CONTRADICTIONS.tsv")
    a = ap.parse_args()
    if a.ledger is None:
        a.ledger = os.path.join(a.db, "_index", "CONTRADICTIONS.tsv")

    if a.command == "extract":
        expected = Path(a.ledger).read_bytes() if os.path.exists(a.ledger) else None
        found = extract(a.db)
        rows, kept = merge(found, read_ledger(a.ledger))
        write_ledger(a.ledger, rows, expected)
        print("found %d dated correction(s); retained %d total records in %s" % (len(found), len(rows), a.ledger))
        print("hand-written summary cells preserved: %d" % kept)
        print("unmatched historical records: %d" % sum(r["source_status"] != "present" for r in rows))
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
        print("  source missing/unmatched       : %d" % sum(
            r.get("source_status", "present") != "present" for r in rows))
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
