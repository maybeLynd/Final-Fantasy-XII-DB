#!/usr/bin/env python3
"""check_rules_index.py - the generated rules index against the rule documents it indexes.

`RULES.md` is produced by `gen_rules_index.py` and **nothing verified the committed file still
matched.** Measured today before this checker existed, and the gap is not cosmetic:

    source                      RULES.md said        actually
    EVIDENCE-STANDARD.md        48 entries, 1,246    221 entries, 5,121
    FINAL-AUDIT-PROTOCOL.md     11 entries,   175     48 entries, 1,163
    TEAM.md                     10 entries,   310     17 entries,   644

**The index was describing the evidence standard as a fifth of its size and the terminal audit
protocol as a quarter.** 173 standard entries and 37 protocol entries had no row - a reader coming
to RULES.md to find a rule would conclude most of them do not exist. That is the same failure
`ADDRESS-INDEX.md` documents about itself, in the document that indexes the project's rules.

WHAT FAILS IS WHAT A READER CANNOT REACH, not how much text differs:

  MISSING ENTRY   a heading exists in a source document and the index has no row for it.
                  The rule is unreachable from the index. FAILS.
  STALE ENTRY     the index offers an anchor the source no longer has. The link goes nowhere,
                  which is worse than silence because it looks like an answer. FAILS.
  COUNTS/PROSE    the "N entries, M lines" line and section ordering. These follow from the
                  entries; reported, never the reason for a failure.

**The remedy is one command** - `gen_rules_index.py --root <repo> --out <the file>` - which is why
failing is right here and wrong for a debt report. A finding that costs a person a month should not
fail a gate; one that costs a command should.

THE GENERATOR IS RUN, NOT RE-IMPLEMENTED, so this cannot disagree with the thing it checks, and a
regeneration that parses to no entries exits 2 rather than reporting a clean index.
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
# A row is a bullet carrying one markdown link into a source document.
ENTRY = re.compile(r"^- \[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)", re.M)
SOURCE = re.compile(r"^\*\*Source: \[`(?P<name>[^`]+)`\]\([^)]+\)\*\* — (?P<n>\d+) entries, "
                    r"(?P<lines>\d+) lines\.", re.M)


def entries(text):
    """The set of (anchor target) rows, which is what a reader clicks."""
    return {m.group("target") for m in ENTRY.finditer(text)}


def sources(text):
    return {m.group("name"): (int(m.group("n")), int(m.group("lines")))
            for m in SOURCE.finditer(text)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    committed = os.path.join(a.db, "_index", "RULES.md")
    if not os.path.isfile(committed):
        print("CANNOT RUN: no _index/RULES.md under %s" % a.db)
        return 2
    gen = os.path.join(KIT, "gen_rules_index.py")
    if not os.path.isfile(gen):
        print("CANNOT RUN: gen_rules_index.py is not in the kit")
        return 2
    root = os.path.dirname(os.path.dirname(a.db)) or "."
    tmp = os.path.join(tempfile.gettempdir(), "rules-index-regen.md")
    r = subprocess.run([sys.executable, gen, "--root", root, "--out", tmp],
                       capture_output=True, text=True)
    if not os.path.isfile(tmp):
        print("CANNOT RUN: the generator produced no file")
        print((r.stdout + r.stderr)[-400:])
        return 2
    fresh_text = io.open(tmp, encoding="utf-8", errors="replace").read()
    have_text = io.open(committed, encoding="utf-8", errors="replace").read()
    fresh, have = entries(fresh_text), entries(have_text)
    if not fresh:
        print("CANNOT RUN: the regenerated index parsed to no entries - the row shape has changed.")
        return 2

    missing = sorted(fresh - have)
    stale = sorted(have - fresh)
    fs, hs = sources(fresh_text), sources(have_text)

    print("THE GENERATED RULES INDEX, AGAINST THE RULE DOCUMENTS\n")
    print("  entries committed  : %d" % len(have))
    print("  entries regenerated: %d" % len(fresh))
    print()
    print("  %-28s %-22s %s" % ("source", "RULES.md says", "actually"))
    for name in sorted(set(fs) | set(hs)):
        h = hs.get(name)
        f = fs.get(name)
        mark = "" if h == f else "   <- DRIFTED"
        print("  %-28s %-22s %s%s"
              % (name[:28],
                 ("%d entries, %d lines" % h) if h else "(not indexed)",
                 ("%d entries, %d lines" % f) if f else "(no longer a source)", mark))
    print()
    print("  MISSING ENTRY - a rule the index cannot reach : %d" % len(missing))
    for t in missing[:12]:
        print("     %s" % t[:104])
    print("  STALE ENTRY - an anchor the source no longer has : %d" % len(stale))
    for t in stale[:12]:
        print("     %s" % t[:104])

    if missing or stale:
        print("\n  THE FIX IS ONE COMMAND, which is why this fails where a debt report would not:")
        print("    python gen_rules_index.py --root \"%s\" --out \"%s\"" % (root, committed))
        print("  Counts, ordering and prose are NOT the reason for the failure - they follow from")
        print("  the entries, and failing on them would make this red on cosmetic edits.")
        return 1
    print("\n  Every rule heading in every source has a row, and no row points at an anchor the")
    print("  source has lost. Counts and ordering are reported above, not enforced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
