#!/usr/bin/env python3
"""Find answers stranded beside obsolete specifications: an address one document calls UNREAD
that another document says it has READ.

Written 2026-09-12 (OPUS) after three documents in one day were found carrying "`0046AB10` unread"
against a function the post-result-events page had read on 2026-09-11 - the status write, its own
section 2.6, and the HP write. One is an accident; three is a failure mode the database cannot see,
because nothing links the sentence that admits ignorance to the page that ended it.

What it does NOT do, deliberately:

  * it does not decide that a finding is stale. "Unread" and "read" can be about different things -
    a caller census versus a body, a field versus a function - so every hit is a PAIR WORTH A LOOK,
    not a defect. The tool reports; a person judges.
  * it does not look inside falsification-pass sections for the "unread" side, since those routinely
    quote the stale wording in the act of correcting it.

Exit status is always 0: this is an advisory, like check_counts.
"""
import argparse
import io
import os
import re
import sys

ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")

# The ignorance side. Kept narrow on purpose: "not known" and "open" are far too common.
UNREAD = re.compile(
    r"\b(unread|unopened|not\s+read|never\s+read|not\s+decoded|not\s+opened|"
    r"not\s+been\s+read|was\s+not\s+read|are\s+unread|is\s+unread)\b", re.I)

# The knowledge side: a document claiming it read something, usually with a date stamp.
READ = re.compile(
    r"\b(read\s+20\d\d-\d\d-\d\d|read\s+to\s+its\s+ret|read\s+whole|read\s+complete|"
    r"complete\s+bodies?\s+of|decoded\s+from\s+the\s+image|read\s+in\s+full|"
    r"body\s+read|now\s+read|已)\b", re.I)

# Narrative past tense: a page saying a thing WAS unread, while reporting that it no longer is.
# "the poster the HP page had left unread", "read here (previously listed 'not read')". Observed
# twice; matched only immediately before the phrase, so it cannot swallow a live admission.
PAST = re.compile(r"\b(had|previously|formerly|once|earlier|already)\s+(been\s+|left\s+|listed\s+)?"
                  r"[\"'“‘]?$", re.I)

WINDOW = 160          # characters either side of the address
PASS_HEADING = re.compile(r"^##+\s.*falsification pass", re.I)
STRIKE = re.compile(r"~~.*?~~", re.S)

# Append-only history. These files are CORRECT as written - they record what was unread on the day
# they were written, and rewriting them would destroy the record. They can never be a live claim.
HISTORY_FILES = ("_index/AUDIT-LOG.md", "_index/COVERAGE.md", "_index/PROGRAM-STATE.md")
HISTORY_DIR = "_index/_inbox/"


REGISTER = "_index/OPEN-QUESTIONS.md"
ANSWERED_ROW = re.compile(r"^\|.*\|\s*(ANSWERED|CLOSED|RESOLVED)\s*\|\s*$", re.I)


def is_history(rel):
    return rel.startswith(HISTORY_DIR) or rel in HISTORY_FILES


def drop_answered_rows(text):
    """A register row keeps the question's ORIGINAL wording while its state column says ANSWERED.

    That wording is a record of what was once unknown, not a live claim - the state column is the
    claim. Without this, every answered row that ever said "unread" reports as stranded forever.
    """
    return "".join(" " * (len(ln) - 1) + "\n" if ANSWERED_ROW.match(ln.rstrip("\n") + "\n")
                   else ln for ln in text.splitlines(True))


def context(text, start, end):
    """The window around a match - but never across a table-row boundary.

    Rows of a key-addresses table sit within a few dozen characters of each other, so a plain
    character window makes every address in the table inherit the words of its neighbours. This
    was most of the tool's first-run noise: `0020E600` "unread" because the row above it said
    another function was not read.
    """
    ls = text.rfind("\n", 0, start) + 1
    le = text.find("\n", end)
    le = len(text) if le < 0 else le
    if text[ls:le].lstrip().startswith("|"):
        return text[ls:le], ls
    lo = max(0, start - WINDOW)
    return text[lo:end + WINDOW], lo


def owns(ctx, s0, e0, pattern):
    """True when THIS address is the one the phrase is about.

    A table row can name five functions and say that one of them is unread. Associating the phrase
    with every address in the row was the tool's largest remaining noise class - it is how
    `002F8E90` and `003588B0` reported as stranded when the word belonged to a different address
    further along the same row.

    The rule: take the nearest occurrence of the phrase, and require that no OTHER address sits
    between it and this one.
    """
    best = None
    for m in pattern.finditer(ctx):
        if pattern is UNREAD and PAST.search(ctx[max(0, m.start() - 24):m.start()]):
            continue                      # "had left unread", "previously listed 'not read'"
        d = m.start() - e0 if m.start() >= e0 else s0 - m.end()
        if d < 0:
            continue
        if best is None or d < best[0]:
            best = (d, m.start(), m.end())
    if best is None:
        return False
    _, ps, pe = best
    lo, hi = (e0, ps) if ps >= e0 else (pe, s0)
    return not any(lo <= o.start() < hi for o in ADDR.finditer(ctx))


def strip_pass_sections(text):
    """Drop '## ... Falsification pass ...' blocks: they quote stale wording while correcting it."""
    out, skipping, level = [], False, 0
    for line in text.splitlines(True):
        m = re.match(r"^(#+)\s", line)
        if m:
            if PASS_HEADING.match(line):
                skipping, level = True, len(m.group(1))
                continue
            if skipping and len(m.group(1)) <= level:
                skipping = False
        if not skipping:
            out.append(line)
    return "".join(out)


def scan(db):
    unread, read = {}, {}
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in {".git"}]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, db).replace("\\", "/")
            raw = io.open(p, encoding="utf-8", errors="replace").read()
            # Strikethrough is this database's own marker for superseded wording: blank it out so a
            # correction that is already recorded does not read as a live admission of ignorance.
            live = STRIKE.sub(lambda mm: " " * (mm.end() - mm.start()), raw)
            if rel == REGISTER:
                live = drop_answered_rows(live)
            body = "" if is_history(rel) else strip_pass_sections(live)
            for m in ADDR.finditer(body):
                a = m.group(1).upper()
                ctx, base = context(body, m.start(), m.end())
                if owns(ctx, m.start() - base, m.end() - base, UNREAD):
                    line = body.count("\n", 0, m.start()) + 1
                    unread.setdefault(a, []).append((rel, line, " ".join(ctx.split())[:180]))
            claimtext = "" if is_history(rel) else live
            for m in ADDR.finditer(claimtext):
                a = m.group(1).upper()
                ctx, base = context(claimtext, m.start(), m.end())
                if owns(ctx, m.start() - base, m.end() - base, READ):
                    line = raw.count("\n", 0, m.start()) + 1
                    read.setdefault(a, []).append((rel, line, " ".join(ctx.split())[:180]))
    return unread, read


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "FFXII TZA"))
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--addr", help="report only this address")
    args = ap.parse_args()
    db = os.path.abspath(args.db)
    if not os.path.isdir(db):
        print("no such database directory: %s" % db)
        return 0

    unread, read = scan(db)
    want = None
    if args.addr:
        # NOT lstrip("0x"): that strips every leading '0' and 'x', so "0026DAC0" becomes "26DAC0"
        # and matches nothing. The first version of this line did exactly that, and made --addr
        # report zero pairs for every address - a filter that always answers "clean".
        want = args.addr.strip().upper()
        if want.startswith("0X"):
            want = want[2:]
        want = want.rjust(8, "0")
    pairs = []
    for a, sites in sorted(unread.items()):
        if want and a.upper() != want:
            continue
        claims = read.get(a)
        if not claims:
            continue
        # Same document on both sides is usually a page reading one thing and not another.
        cross = [(d, l, c) for d, l, c in claims if d not in {s[0] for s in sites}]
        if cross:
            pairs.append((a, sites, cross))

    print("addresses called unread somewhere : %d" % len(unread))
    print("addresses some document says it read : %d" % len(read))
    print("PAIRS - called unread in one document, read in another : %d" % len(pairs))
    print()
    for a, sites, claims in pairs[:args.limit]:
        print("%s" % a)
        for d, l, c in sites[:3]:
            print("   unread : %s:%d" % (d, l))
            print("            %s" % c)
        for d, l, c in claims[:2]:
            print("   read   : %s:%d" % (d, l))
            print("            %s" % c)
        print()
    if len(pairs) > args.limit:
        print("...%d more, pass --limit" % (len(pairs) - args.limit))
    print("A pair is not a defect. 'Unread' and 'read' can be about different things - a caller")
    print("census versus a body, a field versus a function. The tool reports; a person judges.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
