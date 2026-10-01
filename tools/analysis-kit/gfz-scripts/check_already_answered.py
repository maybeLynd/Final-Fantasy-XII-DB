#!/usr/bin/env python3
"""check_already_answered.py - does the database already cover this, before anyone is assigned it?

Why this exists
---------------
On 2026-09-03, inside about ten minutes, the same failure happened three times:

  1. A slice was told it "needed" a mechanism its own document had already published as its
     headline finding (25 rows of `signed pair addss +/-K`).
  2. A session was assigned the identity of the object at `01F82D20` and re-derived the whole
     thing from the other end -- while `19-Save-Load-Settings/.../game-settings-ini-and-runtime-
     config.md` already held it, and `OPEN-QUESTIONS.md` row **AU-6** already said so, in a line
     that had scrolled past the coordinator in his own tool output that same session.
  3. Four "console-invisible" properties were raised as a live thread. All four are named in that
     same document: 11 `WindowSize`, 19 `DeviceID`, 20 `LUIDLow`, 21 `LUIDHigh`.

> **The database is now large enough that not knowing what it contains costs more than not knowing
> what the binary contains.**

Every one of the three was recoverable by grep. None was recovered, because the check was a habit
rather than a step. This makes it a step.

What it does
------------
Given addresses and/or terms, reports every document that cites them, every `OPEN-QUESTIONS.md`
row that mentions them, and -- the part that matters -- whether any such row already carries an
ANSWERED-class verdict.

**A hit is not a veto.** Independent re-derivation is worth something, and the re-derivation above
corrected a reference count (159 -> 157) in the document it duplicated. The output is meant to make
the duplication a *decision* instead of a discovery.

Usage
-----
    python check_already_answered.py --db "Database/FFXII TZA" --addr 01F82D20 --term "GameSetting"
    python check_already_answered.py --self-test
"""
import argparse
import io
import os
import re
import sys

ANSWERED = ("ANSWERED", "CLOSED", "DONE", "DISSOLVED", "REFUTED", "WITHDRAWN", "SUPERSEDED",
            "SATISFIED", "MEASURED", "TRIAGED", "BOUNDED", "RESOLVED", "DUPLICATE", "REVISED",
            "CONFIRMED")


def scan(db, addrs, terms):
    """-> (doc hits, register hits).  Register hits carry whether the row looks answered."""
    docs, rows = [], []
    pats = [re.compile(re.escape(x), re.I) for x in terms]
    # Normalise "0x00510160" and "00510160" to the same bare uppercase hex. The prefix used to
    # be matched literally, so a 0x-prefixed query silently missed every document and side file
    # that writes addresses bare -- which is most of them, and every .tsv. A wrong "no existing
    # coverage" is the most expensive output this tool can produce.
    ups = [a.upper()[2:] if a.upper().startswith("0X") else a.upper() for a in addrs]
    for root, _d, files in os.walk(db):
        for fn in sorted(files):
            # .tsv as well as .md: the database's machine-readable side files -- the verb
            # table, the Phyre field schema, the type store, the experiment checks -- hold real
            # answers, and scanning only prose made them invisible. EF-5 was filed as an open
            # question while scriptvm-verb-table.tsv already answered it in full.
            if not (fn.endswith(".md") or fn.endswith(".tsv")):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            up = t.upper()
            hits = [a for a in ups if a in up] + [q.pattern for q in pats if q.search(t)]
            if not hits:
                continue
            if fn == "OPEN-QUESTIONS.md":
                for n, line in enumerate(t.split("\n"), 1):
                    lu = line.upper()
                    if not any(a in lu for a in ups) and not any(q.search(line) for q in pats):
                        continue
                    if not line.startswith("|"):
                        continue
                    bare = re.sub(r"[*~`]", "", line).upper()
                    done = any(("| " + k) in bare or ("|**" + k) in bare for k in ANSWERED)
                    rows.append((n, done, line.strip()))
            else:
                docs.append((rel, sorted(set(hits))))
    return docs, rows


SELF_TEST_DOC = "The object at `01F82D20` is the GameSetting.ini configuration object.\n"
SELF_TEST_REG = ("| ID | Question | Status |\n"
                 "| AU-6 | What the singleton at `0x01F82D20` is. | **ANSWERED - the config obj.** |\n"
                 "| AU-9 | What `0x01F82D20` bit 3 does. | still open |\n")


def self_test(tmp):
    d = os.path.join(tmp, "selftest_db")
    idx = os.path.join(d, "_index")
    cat = os.path.join(d, "00-Engine-Core-Runtime")
    for x in (idx, cat):
        if not os.path.isdir(x):
            os.makedirs(x)
    io.open(os.path.join(cat, "settings.md"), "w", encoding="utf-8").write(SELF_TEST_DOC)
    io.open(os.path.join(idx, "OPEN-QUESTIONS.md"), "w", encoding="utf-8").write(SELF_TEST_REG)
    docs, rows = scan(d, ["01F82D20"], ["GameSetting"])
    ok = (len(docs) == 1 and len(rows) == 2
          and rows[0][1] is True and rows[1][1] is False)
    if not ok:
        print("SELF-TEST FAILED: docs=%r rows=%r" % (docs, rows))
        return 1
    print("self-test ok: finds the document, both register rows, and tells answered from open")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--addr", nargs="*", default=[])
    ap.add_argument("--term", nargs="*", default=[])
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        import tempfile
        return self_test(tempfile.mkdtemp())

    if not a.db or (not a.addr and not a.term):
        return ap.error("--db and at least one --addr or --term, unless --self-test")

    docs, rows = scan(a.db, a.addr, a.term)
    if not docs and not rows:
        print("no existing coverage found - the block is new")
        return 0

    print("THE DATABASE ALREADY TOUCHES THIS. A hit is not a veto; it is a decision to make.\n")
    if docs:
        print("  documents (%d):" % len(docs))
        for rel, hits in docs:
            print("      %-70s  %s" % (rel, ", ".join(hits)))
        print()
    if rows:
        done = [r for r in rows if r[1]]
        print("  OPEN-QUESTIONS.md rows (%d, of which %d already read as ANSWERED):"
              % (len(rows), len(done)))
        for n, d, line in rows:
            print("      line %-5d %-9s %s" % (n, "ANSWERED" if d else "open", line[:110]))
        print()
        if done:
            print("  ** At least one register row already answers this. Read it before assigning. **")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
