#!/usr/bin/env python3
"""check_chain_transitions.py - is every owner transition in a call chain labelled?

WHY THIS EXISTS. `CALL-CHAINS.md` rule 2 has said "mark every owner boundary and say who owns what"
since the index was written, and it never said *in what form*. So the corpus marks boundaries in
whatever wording each page reached for - `[OWNER TRANSITION into Audio]`, `<- OWNER TRANSITION:
middleware -> game`, and eight more shapes - and **nothing could count them**. Final-audit pass 21
stayed PARTIAL for want of a mechanical test.

Rule 6 supplies the form:

    [AUTHORITY NN -> NN]    the DECISION crosses
    [TRIGGER   NN -> NN]    only CONTROL crosses

`NN` is a two-digit category number, or `EXT` for an owner outside the image.

WHAT THIS MEASURES, AND WHAT IT CANNOT. It reports three populations:

  * **labelled**   - a well-formed AUTHORITY/TRIGGER with two owner codes that exist;
  * **unlabelled** - a transition marked in any of the legacy wordings, with no label. This is the
    backlog, and it is meant to be a number that goes down;
  * **malformed**  - a label that is neither verb, or names an owner code the corpus does not have.
    This is a defect, not a backlog: someone tried to follow the rule and the row does not parse.

**It cannot tell a MISLABELLED transition from a correct one.** Whether a hop hands over the decision
or merely control is a judgement about what a reimplementation must own, and no regular expression
settles it. The check measures form; rule 6 supplies the meaning, and a reader supplies the verdict.
Reporting a clean run as "pass 21 is satisfied" would be exactly the substitution this database
exists to avoid.

    python check_chain_transitions.py --self-test
    python check_chain_transitions.py
    python check_chain_transitions.py --db <dir> --quiet
"""
import argparse
import os
import re
import sys

import kit_paths as KP

# A labelled transition, in the form rule 6 defines.
#
# `*` is admissible on EITHER side - "more than one owner, selected elsewhere". The first draft
# allowed it only as the source, on the reasoning that a hop always knows where it landed; 002621D0
# is a dispatcher into familyTables[id>>12] and does not. That was a guess about the corpus which
# the corpus refuted within the hour. Both sides `*` is still refused: it says nothing at all.
LABELLED = re.compile(r"\[(AUTHORITY|TRIGGER)\s+([0-9]{2}|EXT|\*)\s*->\s*([0-9]{2}|EXT|\*)\]")

# Anything that announces an owner transition. Deliberately generous: the point is to find the ones
# that are NOT labelled, so this has to match the wordings that predate the rule - and the two
# OTHER senses of "owner" the corpus uses, so that a row reclassified out of rule 6 stays VISIBLE
# rather than merely dropping out of the scan. An invisible row cannot be audited or counted.
MARKER = re.compile(r"OWNER TRANSITION|owner transition|\[(AUTHORITY|TRIGGER)\b"
                    r"|MEMORY OWNERSHIP|DECISION SETTLES", re.I)

# A label-shaped thing that does not parse - someone followed the rule and got the form wrong.
MALFORMED = re.compile(r"\[(AUTHORITY|TRIGGER)\b(?![^\]]*\]\s*$)[^\]]*\]")


def owner_codes(db):
    out = {"EXT"}
    for name in os.listdir(db):
        if re.match(r"^[0-9]{2}-", name) and os.path.isdir(os.path.join(db, name)):
            out.add(name[:2])
    return out


def scan(db):
    rows = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, db).replace("\\", "/")
            if rel.startswith("_index/_inbox/"):
                continue                      # working notes, not the corpus
            if rel == "_index/FINAL-AUDIT-PROTOCOL.md":
                # The document that MEASURES conventions quotes them as examples. Its fenced blocks
                # are specimens, not chains, and counting them makes the protocol its own backlog.
                continue
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            # ONLY MARKERS INSIDE A FENCED BLOCK ARE TRANSITIONS. The rest are prose ABOUT owner
            # transitions - "this is an owner transition, not a trigger", "the thunk is the trigger"
            # - and they will never carry a label because they are not rows in a chain. Counting
            # them made the backlog eight larger than the work, which is the kind of inflated
            # denominator that makes a number useless to plan against.
            fenced = False
            for i, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("```"):
                    fenced = not fenced
                    continue
                if not MARKER.search(line):
                    continue
                rows.append((rel, i, line.strip(), fenced))
    return rows


#: The rule's own definition of the form. `[AUTHORITY NN -> NN]` is metasyntax, not a transition, and
#  without this the check reports the page that DEFINES the convention as the only place breaking it.
#  Third self-reference of the day in this kit; they are cheap to write and expensive to leave.
PLACEHOLDER = re.compile(r"\[(AUTHORITY|TRIGGER)\s+NN\s*->\s*NN\]")


#: A row that declares itself NOT a transition. Adding the disclaimer made the row match the marker
#  regex harder than before - "HANDOFF, not an owner transition" contains the very words the scan
#  looks for - so the one row that had been correctly reclassified stayed in the backlog. Fifth time
#  today a check has read its own output; the shape never changes.
DISCLAIMED = re.compile(r"not an owner transition|not a subsystem transition|\bHANDOFF\b"
                        r"|MEMORY OWNERSHIP|DECISION SETTLES", re.I)


def classify(line, codes):
    if PLACEHOLDER.search(line):
        return None, "the rule's own definition of the form, not a transition"
    if DISCLAIMED.search(line) and not LABELLED.search(line):
        return "declared", "declared as a different kind of ownership, not a rule-6 transition"
    m = LABELLED.search(line)
    if m:
        bad = [c for c in (m.group(2), m.group(3)) if c not in codes and c != "*"]
        if bad:
            return "malformed", "owner code %s is not a category" % ", ".join(bad)
        if m.group(2) == "*" and m.group(3) == "*":
            return "malformed", "both sides * says nothing at all"
        if m.group(2) == m.group(3):
            return "malformed", "a transition from %s to itself" % m.group(2)
        return "labelled", "%s %s -> %s" % (m.group(1), m.group(2), m.group(3))
    if re.search(r"\[(AUTHORITY|TRIGGER)\b", line, re.I):
        return "malformed", "label present but does not parse as [VERB NN -> NN]"
    return "unlabelled", "legacy marker, no rule-6 label"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        codes = {"18", "22", "00", "EXT"}
        cases = [
            ("  -> 00249C60(localIndex)   [AUTHORITY 01 -> 18]", "labelled", False),
            ("  -> 0017CCD0               [TRIGGER 22 -> 00]", "labelled", True),
            ("  -> 00249C60   [OWNER TRANSITION into Audio]", "unlabelled", True),
            ("  <- OWNER TRANSITION: middleware -> game", "unlabelled", True),
            ("  -> x  [AUTHORITY 22 -> 99]", "malformed", True),
            ("  -> x  [TRIGGER 22 -> 22]", "malformed", True),
            ("  -> x  [AUTHORITY audio -> game]", "malformed", True),
            ("  -> 00249C60  [AUTHORITY * -> 18]", "labelled", True),
            ("  -> x  [TRIGGER 22 -> *]", "labelled", True),
            ("  -> x  [TRIGGER * -> *]", "malformed", True),
            ("  -> 0017D6E0", None, True),
            ("    [AUTHORITY NN -> NN]    the DECISION crosses", None, True),
            ("  -> 0018C610   <- HANDOFF, not an owner transition", "declared", True),
            ("  -> 001A5760  [MEMORY OWNERSHIP, not a subsystem transition]", "declared", True),
        ]
        ok = True
        for line, want, in_codes in cases:
            use = codes if in_codes else {"01", "18"}
            hit = bool(MARKER.search(line))
            got = classify(line, use)[0] if hit else None
            good = (got == want)
            ok = ok and good
            print("  %-46s -> %-11s %s" % (line.strip()[:46], got, "ok" if good else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    codes = owner_codes(a.db)
    rows = scan(a.db)
    buckets = {"labelled": [], "unlabelled": [], "malformed": [], "prose": [], "declared": []}
    skipped = 0
    for rel, line_no, line, fenced in rows:
        kind, why = classify(line, codes)
        if kind is None:
            skipped += 1
            continue
        # OUTSIDE A FENCE, NOTHING IS A TRANSITION - not even a line that looks labelled. This began
        # as a skip for unlabelled prose only, and then a page explaining WHY a hop is not an owner
        # transition quoted `[AUTHORITY 17 -> 17]` as the thing it declined to write, and the check
        # reported the explanation as the defect. Fourth self-reference caught in this kit today;
        # the pattern is always the same - a check that reads text will eventually read text ABOUT
        # itself, and the fix is a structural rule, not another marker word.
        if not fenced:
            buckets["prose"].append((rel, line_no, line, "prose about transitions, not a chain row"))
            continue
        buckets[kind].append((rel, line_no, line, why))

    if not a.quiet:
        for kind in ("malformed", "unlabelled"):
            for rel, line_no, line, why in buckets[kind]:
                print("%-10s %s:%d" % (kind.upper(), rel, line_no))
                print("    %s" % line[:110])
                print("    %s" % why)
            if buckets[kind]:
                print()

    inchain = (len(buckets["labelled"]) + len(buckets["unlabelled"])
               + len(buckets["malformed"]) + len(buckets["declared"]))
    print("transition rows in chains : %d  (+%d prose mentions, +%d metasyntax)"
          % (inchain, len(buckets["prose"]), skipped))
    print("  labelled (rule 6)     : %d" % len(buckets["labelled"]))
    print("  UNLABELLED (backlog)  : %d" % len(buckets["unlabelled"]))
    print("  declared other kind   : %d" % len(buckets["declared"]))
    print("  MALFORMED (defect)    : %d" % len(buckets["malformed"]))
    print()
    print("This measures FORM. Whether a hop hands over the DECISION or only control is a judgement")
    print("about what a reimplementation must own, and no regular expression settles it - a clean")
    print("run here is not pass 21 satisfied, it is pass 21 having something to read.")
    return 1 if buckets["malformed"] else 0


if __name__ == "__main__":
    sys.exit(main())
