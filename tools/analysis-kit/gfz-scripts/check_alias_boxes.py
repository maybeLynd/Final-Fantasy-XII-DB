#!/usr/bin/env python3
"""check_alias_boxes.py - one question tracked as open under two identities.

THE DEFECT, and it is not hypothetical. `AC-6` carried two different questions on one page: the
13-function cluster at `the-unresolved-158.md:224` and the re-derive-every-census question at :306,
while the register's `AC-6` row asks only the second. FABLE found it by reading; the cluster
question had no row of its own and was borrowing a neighbour's id, so it was invisible to every
count. The repair gave it `UQ-383`.

The general shape is a CHECKBOX carrying two question ids. That happens legitimately - the
2026-09-14 generation pass gave every open box a `UQ-` id, including boxes that already carried a
label-form id, and FABLE's ruling was that "the nine `UQ-` rows are superseded below and keep their
text; the boxes are left alone, so the `UQ-` label remains as a pointer". A box naming a live
question and a SUPERSEDED one is that pointer, and is correct.

WHAT IS NOT CORRECT is a box naming two ids that are BOTH STILL OPEN. Then one question is counted
twice, either id can be answered while the other stays open, and the register's open count is wrong
by construction. That is the AC-6 failure, and at HEAD seven boxes are in it.

WHY THIS FILE EXISTS AT ALL. The measurement was made on 2026-09-14 by
`Tools/work/FABLE/drift5/alias_boxes.py`, which `.gitignore` excludes - so the register cites a
figure nobody else can re-derive, and `check_cited_instruments` reports the citation. The method
needs no private tool: it is a census of checkbox lines and a read of the register's own verdicts,
both committed. Re-measured here, the 2026-09-14 figures have moved with the corpus - 11 alias
boxes in 1,384 checkbox blocks then, 17 in 1,406 now - which is exactly why a ratio against a
moving denominator has to carry its date, and why the instrument belongs in the kit rather than in
one agent's work directory.

usage: check_alias_boxes.py [--db DB] [--self-test] [--all]
"""
import argparse
import collections
import io
import os
import re
import sys

BOX = re.compile(r"^\s*[-*]\s*\[[ xX~]\]")
QID = re.compile(r"(?<![A-Za-z0-9])([A-Z]{1,4}-\d+)(?![A-Za-z0-9-])")
STRUCK = re.compile(r"~~.*?~~", re.S)
# A verdict word ANYWHERE in the row's cells, after struck text is dropped. Deliberately the same
# vocabulary the register uses for its own headline, plus SUPERSEDED - a superseded row is exactly
# the pointer FABLE's ruling describes and must not read as live.
CLOSED = re.compile(r"\bANSWERED\b|\bRESOLVED\b|\bCLOSED\b|\bWITHDRAWN\b|\bSUPERSED", re.I)
SKIP_DIRS = {".git", "__pycache__", "_templates", "_inbox"}


def register_state(db):
    """id -> OPEN | CLOSED, read from the register's rows the way the other gates read them."""
    p = os.path.join(db, "_index", "OPEN-QUESTIONS.md")
    state = {}
    if not os.path.exists(p):
        return state
    for line in io.open(p, encoding="utf-8", errors="replace"):
        m = re.match(r"\|\s*([A-Z]{1,4}-\d+)\s*\|", line)
        if m:
            rest = STRUCK.sub("", line[m.end():])
            state[m.group(1)] = "CLOSED" if CLOSED.search(rest) else "OPEN"
    return state


def alias_boxes(db, state):
    """(document, line, ids, live_ids) for every checkbox naming two or more REGISTERED ids."""
    out, boxes = [], 0
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            if rel.startswith("_index/OPEN-QUESTIONS"):
                continue          # the register lists ids by definition; it is not a box
            for n, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                if not BOX.match(line):
                    continue
                boxes += 1
                ids = sorted({i for i in QID.findall(STRUCK.sub("", line)) if i in state})
                if len(ids) < 2:
                    continue
                live = [i for i in ids if state[i] == "OPEN"]
                out.append((rel, n, ids, live))
    return out, boxes


def self_test():
    """Both ways. The dangerous error is calling a live pair a pointer and dropping a real finding."""
    state = {"AC-6": "OPEN", "UQ-383": "CLOSED", "SB-1": "OPEN", "UQ-255": "OPEN", "G-11": "CLOSED"}
    cases = [
        ("- [ ] what the cluster is. AC-6 - see UQ-383", 1, False,
         "live id beside a CLOSED one - the pointer FABLE's ruling allows"),
        ("- [ ] the block index. SB-1 and UQ-255 both open", 2, True,
         "TWO LIVE ids - the finding"),
        ("- [x] done. G-11 / UQ-383", 0, False, "both closed - nothing live"),
        ("- [ ] a box naming only SB-1", 0, False, "one id is not an alias box"),
        ("plain prose naming SB-1 and UQ-255, not a checkbox", 0, False, "not a box at all"),
        ("- [ ] ~~SB-1 and UQ-255~~ struck out entirely", 0, False, "struck text is not a claim"),
    ]
    ok = True
    for line, want_live, want_finding, why in cases:
        if not BOX.match(line):
            got_live, finding = 0, False
        else:
            ids = sorted({i for i in QID.findall(STRUCK.sub("", line)) if i in state})
            live = [i for i in ids if state[i] == "OPEN"]
            got_live = len(live) if len(ids) >= 2 else 0
            finding = len(ids) >= 2 and len(live) >= 2
        good = (got_live == want_live and finding == want_finding)
        ok &= good
        print("  %s %-52s live %d, finding %s" % ("ok  " if good else "FAIL", why, got_live,
                                                  finding))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join("Database", "FFXII TZA"))
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--all", action="store_true", help="list every alias box, not just findings")
    a = ap.parse_args()
    if a.self_test:
        print("check_alias_boxes self-test")
        return 0 if self_test() else 1

    state = register_state(a.db)
    if not state:
        print("no register at %s" % a.db)
        return 2
    rows, boxes = alias_boxes(a.db, state)
    findings = [r for r in rows if len(r[3]) >= 2]

    print("one question under two identities - checkbox blocks naming two registered ids\n")
    print("  checkbox blocks scanned        : %d" % boxes)
    print("  registered ids in the register : %d" % len(state))
    print("  alias boxes (two or more ids)  : %d" % len(rows))
    print("  of those, a POINTER - the other id is closed or superseded : %d"
          % (len(rows) - len(findings)))
    print("  of those, BOTH IDS STILL OPEN  : %d   <- the finding" % len(findings))

    if not self_test_quiet():
        print("\n  CONTROL FAILED: the self-test does not pass, so the counts above mean nothing.")
        return 2

    for rel, n, ids, live in (rows if a.all else findings):
        mark = "" if len(live) >= 2 else "   [pointer]"
        print("\n  %s:%d%s" % (rel, n, mark))
        print("     %s" % "  +  ".join("%s %s" % (i, state[i]) for i in ids))
    if not findings:
        print("\nno question is tracked as open under two identities.")
        return 0
    print("\n  Each is one question counted twice: either id can be answered while the other")
    print("  stays open, which is what AC-6 did. The cure is the missing row or a supersession,")
    print("  never a renumbering - a label carries the identity a question was asked under.")
    return 1


def self_test_quiet():
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return self_test()


if __name__ == "__main__":
    sys.exit(main())
