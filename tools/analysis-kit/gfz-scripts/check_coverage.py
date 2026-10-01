#!/usr/bin/env python3
"""Verify _index/COVERAGE.md document counts against what is actually on disk.

The COVERAGE index is hand-maintained, so it drifts. It drifted by 7 documents
across 3 categories before this check existed: two of those were caused by an
index update that hardcoded a count instead of incrementing it, and one was
stale from an earlier session.

Usage:  check_coverage.py [--db <path>] [--fix]

Exit code 1 if any category disagrees (so it can gate a seal).
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import head_scope as HS  # noqa: E402
import kit_paths as KP  # noqa: E402

DEFAULT_DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")


def count_on_disk(db):
    """One .md per system document; README.md is navigation, not content.

    COUNTED AT HEAD, NOT IN THE WORKING TREE. This walked the directory and counted whatever was
    sitting there, which on 2026-09-15 made it red over SIX untracked documents a peer was still
    writing in 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats. COVERAGE.md claimed 25 for
    that category and 25 is exactly right: 25 documents are published there. Running --fix would
    have written 31 - a published index describing six files nobody outside one working tree can
    read - and the next peer to commit would have reverted it.

    COVERAGE.md is a statement about the database, and the database is what is committed. A
    document that exists only in someone's tree is not coverage yet. Same ruling as check_links'
    HEAD/worktree split (2026-09-15, OPUS): a shared gate must not go red, or green, over an edit
    nobody has published. If git cannot answer, the walk is used and the report says so, because
    guessing is worse than a stated fallback.
    """
    head = HS.tracked_at_head(db, ".md")
    actual = collections.Counter()
    for root, _dirs, files in os.walk(db):
        rel = os.path.relpath(root, db)
        top = rel.split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for f in files:
            if f.endswith(".md") and f != "README.md":
                # abspath, not normpath: `--db` is usually RELATIVE, so os.walk yields relative
                # roots while HEAD's paths are absolute, and a relative-vs-absolute comparison
                # matched nothing and reported every category as 0.
                if head is not None and os.path.abspath(os.path.join(root, f)) not in head:
                    continue
                actual[top] += 1
    return actual, head is not None


def die(m):
    sys.stderr.write("check_coverage: " + m + "\n")
    raise SystemExit(2)


SYSTEMS_TABLE = re.compile(r"^\|\s*Category\s*\|\s*Systems documented\s*\|", re.M)


def systems_table_span(cov):
    """(start, end) of the 'Systems documented' table body, or None.

    ANCHORED 2026-09-14 (OPUS). Everything below keys on category name, and COVERAGE.md holds
    two tables keyed by category -- a `Category | funcs | docs | debt` summary and the real
    `Category | Systems documented | Status` table. Matching by name alone took whichever came
    first, which is how --fix once overwrote a summary row's FUNCTIONS column 572 -> 25 and left
    the real count untouched. The span is the guard: nothing outside it is read or rewritten.
    """
    m = SYSTEMS_TABLE.search(cov)
    if not m:
        return None
    start = cov.index("\n", m.end()) + 1
    end = cov.find("\n\n", start)
    return (start, len(cov) if end < 0 else end)


def read_claimed(db):
    cov = io.open(os.path.join(db, "_index", "COVERAGE.md"), encoding="utf-8").read()
    span = systems_table_span(cov)
    if span is None:
        die("COVERAGE.md has no 'Category | Systems documented' table -- refusing to guess "
            "which table holds the counts")
    claimed = {}
    for m in re.finditer(r"^\| (\d\d-[A-Za-z0-9-]+) \| (\d+) \|", cov[span[0]:span[1]], re.M):
        claimed[m.group(1)] = int(m.group(2))
    return cov, claimed


# DEFECT, found 2026-09-13 (OPUS) by diffing --fix against a backup instead of trusting it.
# The rewrite matches a row by CATEGORY NAME and does not check which table the row is in, and
# it takes the FIRST match. COVERAGE.md holds two tables keyed by category: a
# "category | functions | documents | per-doc" summary at ~line 111 and the real
# "Category | Systems documented | Status" table at ~line 128. For 02-Resource-And-Asset-
# Pipeline --fix hit the summary row, overwrote its FUNCTIONS column 572 -> 25, and left the
# real count row still reading 3. It corrupted one number and fixed nothing. The other summary
# rows survived only because their numbers carry thousands separators ("5,150"), which the
# pattern does not match - an accident of formatting, not a guard.
#
# Also: a category with NO row at all is reported as "claimed None" and --fix cannot add it.
# 25-EBP-Script-Container and 26-PKFL-Package-Container were both missing; added by hand with
# the count only, because a status is a judgement rather than a measurement.
#
# Until the match is anchored to the "Systems documented" table: BACK THE FILE UP AND DIFF
# BEFORE ACCEPTING --fix.
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--fix", action="store_true",
                    help="rewrite COVERAGE.md counts to match disk (descriptions untouched)")
    a = ap.parse_args(argv)

    actual, at_head = count_on_disk(a.db)
    cov, claimed = read_claimed(a.db)
    if not at_head:
        print("NOTE: git could not name HEAD's files, so this counts the WORKING TREE and may")
        print("      include documents nobody has published.")

    bad = []
    for k in sorted(set(claimed) | set(actual)):
        c, d = claimed.get(k), actual.get(k, 0)
        if c != d:
            bad.append((k, c, d))

    if not bad:
        print(f"COVERAGE consistent: {sum(actual.values())} documents across "
              f"{len(actual)} categories")
        return 0

    print(f"COVERAGE MISMATCH in {len(bad)} categor{'y' if len(bad)==1 else 'ies'}:")
    for k, c, d in bad:
        print(f"   {k:36s} claimed {c}  actual {d}")
    print(f"   totals: claimed {sum(claimed.values())}  actual {sum(actual.values())}")

    if a.fix:
        missing = [k for k, c, _d in bad if c is None]
        if missing:
            print("   REFUSING --fix: %d categor%s has no row in the 'Systems documented' table "
                  "(%s). A status is a judgement, not a measurement, so the row is added by hand."
                  % (len(missing), "y" if len(missing) == 1 else "ies", ", ".join(missing)))
            return 1
        lo, hi = systems_table_span(cov)
        head, table, tail = cov[:lo], cov[lo:hi], cov[hi:]
        for k, _c, d in bad:
            table, n = re.subn(rf"^\| {re.escape(k)} \| \d+ \|", f"| {k} | {d} |",
                               table, count=1, flags=re.M)
            if n != 1:
                print("   REFUSING --fix: %s matched %d rows inside the systems table" % (k, n))
                return 1
        io.open(os.path.join(a.db, "_index", "COVERAGE.md"), "w",
                encoding="utf-8", newline="\n").write(head + table + tail)
        print("   -> %d count(s) rewritten, inside the 'Systems documented' table only" % len(bad))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
