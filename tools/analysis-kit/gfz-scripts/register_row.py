#!/usr/bin/env python3
"""register_row.py - change ONE row of OPEN-QUESTIONS.md, with the read/write window closed.

WHY THIS EXISTS
---------------
`_index/OPEN-QUESTIONS.md` took **93 commits on 2026-09-14 alone**, from every identity on the
board. It is the highest-traffic shared file in the corpus, and every agent edits it the same way:
read the whole file, change one row, write the whole file back.

**That is a read-modify-write on a file somebody else is also editing.** If a peer commits a row
between the read and the write, the write reverts it - silently, with no conflict, because the file
was never in the index. Nothing about a clean `git status` afterwards would show it.

Nothing has been lost yet, and that is luck rather than design: on 2026-09-14 OPUS's in-flight work
rode into a peer's commit three times inside ninety minutes, and each time the read happened to come
after the peer's write rather than before it. Once it comes before, a row disappears.

WHAT THIS DOES ABOUT IT
-----------------------
Two things, both small:

1. **Re-reads the file immediately before writing** and refuses if it changed since the read this
   process did. The window is microseconds instead of however long the caller spent composing prose.
2. **Touches exactly one row.** The rest of the file is written back byte-identical, so even a
   successful race can only affect the row named on the command line.

It does NOT lock, and deliberately so: a lock on a file this busy would serialise nine identities
behind whoever is slowest, and the board already has `@publication` for work that must be serial.
The defect here is a window, not a lack of mutual exclusion.

Usage:
    register_row.py --id UQ-303 --append " **ANSWERED 2026-09-14 (OPUS)** - ..."
    register_row.py --id BM-3 --replace-verdict OPEN --with "**PARTLY ANSWERED ...**"
    register_row.py --self-test
"""
import argparse
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "FFXII TZA", "_index", "OPEN-QUESTIONS.md"))


def _digest(path):
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


def _row_pattern(qid):
    return re.compile(r"^\|\s*%s\s*\|.*$" % re.escape(qid), re.M)


def edit(path, qid, append=None, replace=None, with_text=None):
    """-> (ok, message). Never writes unless exactly one row matches and the file is unchanged."""
    before = _digest(path)
    text = io.open(path, encoding="utf-8").read()
    pat = _row_pattern(qid)
    hits = pat.findall(text)
    if len(hits) != 1:
        return False, ("%d rows match %s - refusing. A register id naming two rows is a defect "
                       "check_question_ids reports; this tool will not guess which one." % (len(hits), qid))
    row = hits[0]
    if append is not None:
        stripped = row.rstrip()
        if not stripped.endswith("|"):
            return False, "the row does not end in a pipe; refusing to guess its shape"
        new = stripped[:-1].rstrip() + " " + append.strip() + " |"
    else:
        if replace not in row:
            return False, "%r does not occur in the row - refusing" % replace
        if row.count(replace) != 1:
            return False, "%r occurs %d times in the row - refusing" % (replace, row.count(replace))
        new = row.replace(replace, with_text, 1)

    # THE WINDOW, CLOSED. Everything above is pure computation on a snapshot; this is the only
    # moment the file is touched, and it refuses if anybody wrote in between.
    if _digest(path) != before:
        return False, ("the register changed while this edit was being computed - re-run. THIS IS "
                       "THE CHECK WORKING, not a failure: writing now would have reverted whatever "
                       "landed.")
    io.open(path, "w", encoding="utf-8", newline="\n").write(text.replace(row, new, 1))
    return True, "row %s updated" % qid


def self_test():
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "reg.md")
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        "| A-1 | q | OPEN |\n| A-2 | q | OPEN |\n| A-1 | dup | OPEN |\n")
    cases = []
    ok, msg = edit(p, "A-2", append="**ANSWERED**")
    cases.append(("append to a unique row", ok and "| A-2 | q | OPEN **ANSWERED** |"
                  in io.open(p, encoding="utf-8").read()))
    ok, msg = edit(p, "A-1", append="x")
    cases.append(("refuse a duplicated id", not ok and "2 rows match" in msg))
    ok, msg = edit(p, "A-9", append="x")
    cases.append(("refuse an absent id", not ok and "0 rows match" in msg))
    ok, msg = edit(p, "A-2", replace="OPEN", with_text="CLOSED")
    cases.append(("replace a unique substring", ok))
    ok, msg = edit(p, "A-2", replace="ZZZ", with_text="x")
    cases.append(("refuse an absent substring", not ok))
    bad = [n for n, good in cases if not good]
    for n, good in cases:
        print("  %-34s %s" % (n, "ok" if good else "FAIL"))
    print("self-test: %d of %d cases correct" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", default=DEFAULT)
    ap.add_argument("--id")
    ap.add_argument("--append")
    ap.add_argument("--replace-verdict", dest="replace")
    ap.add_argument("--with", dest="with_text")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.id or (a.append is None and a.replace is None):
        return ap.error("--id and one of --append / --replace-verdict required")
    ok, msg = edit(a.register, a.id, a.append, a.replace, a.with_text)
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
