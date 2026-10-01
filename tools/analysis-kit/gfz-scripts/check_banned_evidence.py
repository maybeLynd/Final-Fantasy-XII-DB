#!/usr/bin/env python3
"""check_banned_evidence.py - FINAL-AUDIT-PROTOCOL pass 6, runnable now as a DIAGNOSTIC.

The protocol's pass 6 sweeps every document for `.pdata`, `.xdata`, unwind, EH map, IP-to-state and
`_IMAGE_RUNTIME_FUNCTION_ENTRY`, and **fails if any appears as evidence rather than as a thing being
excluded**. That last clause is the whole pass: these terms are supposed to appear, in the sentences
that say the database does not lean on them.

THIS IS NOT A GATE PASS. The gate runs only when the database is otherwise believed complete
(unresolved = 0, every system documented, OPEN-QUESTIONS empty), and it is not. Running the cheap
passes early finds defects while they are cheap to fix, instead of burning a thirty-pass streak on
something a grep could have caught months earlier.

Why a raw grep is worthless here
--------------------------------
A plain sweep returns ~392 hits and is dominated by ONE directory name -
`24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/` - appearing inside markdown link
targets. A path is not a claim. The count also cannot tell an exclusion from a use, which is the
only distinction the pass actually makes. So this classifies instead of counting:

    PATH       the term is inside a link target or an inline-code path - not prose at all
    EXCLUDED   the sentence says the database does NOT rest on it (the intended state)
    REVIEW     everything else - a human has to read it

REVIEW is the output that matters. PATH and EXCLUDED are printed as totals so the classification
itself stays auditable.

The unit EXCLUDE reads is the PARAGRAPH, not the physical line (2026-09-17, FABLE)
--------------------------------------------------------------------------------
Ruling on OPUS-REQ-FABLE-PASS6-HALF-THE-REVIEW-QUEUE-IS-A-REFUSAL-ON-THE-NEXT-LINE. A physical line
is a wrapping artefact: markdown breaks a sentence wherever the author's editor did, so a refusal
("... is not evidence") routinely sits one line below the term it governs, and the first version of
this test could not see it. Measured at HEAD with ONE variable changed - same TERMS, same EXCLUDE,
same LINKY stripping, same skip sets - the REVIEW queue was 146 lines per line, 98 per sentence and
48 per paragraph, and every one of the 50 lines the paragraph clears beyond the sentence was read:
all are correction/withdrawal notes or reference censuses whose paragraph refuses the metadata in
another sentence. None was a use. So the paragraph is the unit: a heading, a table row, a fenced
line or a list item is its own paragraph; prose runs to the next blank line. The TERM is still
found per line (PATH stays a per-line test, and the listing still prints the line), only the
refusal test widens. The page-level disposition registry below already treated the PAGE as the
reviewer's unit, so the line-scoped refusal was the odd one out. The residue that survives the
paragraph is read by hand and classified in the FABLE inbox under the same date.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispositions as DISP  # noqa: E402

TERMS = re.compile(
    r"\.pdata|\.xdata|_IMAGE_RUNTIME_FUNCTION_ENTRY|IP-to-state|IP2State|unwind|"
    r"UNW_FLAG_CHAININFO|RUNTIME_FUNCTION|EH map|ehmap",
    re.I)

# Markers that a sentence is REFUSING the evidence rather than using it.
EXCLUDE = re.compile(
    r"\bnot\b|\bnever\b|\bno\b|\bwithout\b|\bexclud|\brather than\b|\binstead of\b|\bbanned\b|"
    r"\brefus|\bignor|\bforbid|\bdisallow|\bdoes not\b|\bcannot\b|\bcan't\b|\bavoid|\bunusable\b|"
    r"\bdiscard|\brejected\b|\bnot evidence\b|\btextbook way\b|\bwould be\b|\bare excluded\b|"
    # OPUS 2026-09-18, ruling on FABLE-REQ-OPUS-PASS6-SIX-REFUSAL-WORDS-EXCLUDE-LACKS.
    # THREE OF THE SIX PROPOSED WORDS, AND THE THREE REFUSED ARE NOT THE SET THE REQUEST
    # OFFERED AS RISKY. `bans` because `banned` is already here and a rule-stating
    # sentence uses the third person - 6 lines, every one literal. `excl.` because a
    # table HEADER CELL has no room for a sentence, which is precisely why a prose-shaped
    # pattern misses "stored RVA (excl. all unwind data)" - 2 lines. `inadmissible`
    # because it is an admissibility verdict that cannot mean anything else, though it
    # clears NOTHING today and that is said out loud rather than left to be discovered.
    # REFUSED: `nothing` (2 lines, one of them vtable-method-index 2640, which is
    # arithmetic - "sum to exactly that and to nothing else" - not a refusal); `none`
    # (1 line, already cleared by `bans`); and `non-`, WHICH THE REQUEST CALLED SAFE - it
    # clears the same wrong line 2640 ("non-funclet") and clears unowned-code 729 only by
    # coincidence of matching a SECTION-NAME negation. "non-trivial" next to a `.pdata`
    # mention would clear a page that rests on it.
    # EXCLUDE IS TRIAGE, NOT A VERDICT: "the database bans unwind data, but here we use
    # it anyway" clears on any of these, and that is true of every word above too. The
    # gate is the hand reading plus the disposition registry.
    r"\bbans\b|\bexcl\.|\binadmissible\b",
    re.I)

# A markdown link target, or a PATH-SHAPED code span / bare path segment.
#
# Stripping every `code span` was the first version and its own self-test refused it: a sentence
# that discusses `.pdata` in prose writes the term in code formatting, so blanking all code spans
# files real discussion as PATH. Only spans that look like a path - containing a slash, or ending
# in .md - are link noise.
LINK_TARGET = re.compile(r"\]\([^)]*\)")           # markdown link target
CODE_SPAN = re.compile(r"`[^`]*`")                  # any code span, consumed IN PAIRS left to right
BARE_PATH = re.compile(r"(?:\.{0,2}/)?[\w.-]+/[\w./-]+")   # bare path segment


def strip_linky(text):
    """Blank link targets, path-shaped code spans and bare path segments.

    The three were one alternation until 2026-09-17. Its code-span branch, `[^`]*(?:/|.md)[^`]*`,
    could START at the CLOSING backtick of one span and run to the OPENING backtick of the next,
    blanking everything between two code spans whenever a slash sat in between - including the
    refusal words. Harmless-looking on one line, it fired on the first paragraph the widened test
    reflowed (EXP-040 line 35: `0031076C` ... not the entire function ... evidence/x.py ... `003105D0`).
    Consuming spans in pairs with re.sub cannot start at a closing backtick."""
    text = LINK_TARGET.sub(" ", text)
    text = CODE_SPAN.sub(lambda m: " " if ("/" in m.group() or ".md" in m.group()) else m.group(),
                         text)
    return BARE_PATH.sub(" ", text)
# `_inbox` is board traffic, not documents - check_doc_self excludes it for the same reason.
SKIP_DIRS = {".git", "_templates", "_inbox"}
# The protocol, the standard and the log that DEFINE or RECORD the ban necessarily quote the terms.
SKIP_FILES = {"FINAL-AUDIT-PROTOCOL.md", "EVIDENCE-STANDARD.md", "AUDIT-LOG.md"}

# A page INSIDE the exception-handling area has unwind metadata as its SUBJECT: it is documenting
# the machinery, not borrowing it to prove something else. Those are bucketed separately rather than
# skipped, because "the subject is exempt" is a claim that should stay visible and countable.
#
# Deliberately narrow: `Lazy-Static-Initialization` and `Binary-Hardening-And-Hooking` are NOT
# exempt. A lazy-statics page resting on unwind records is exactly what this pass exists to surface.
SUBJECT_DIR = re.compile(r"Exception|Unwind", re.I)


# A line that starts a paragraph of its own: heading, table row, fence, list item.
OWN_UNIT = re.compile(r"^\s*#|^\s*\||^```")
ITEM_START = re.compile(r"^\s*[-*] |^\s*\d+\. ")
QUOTE = re.compile(r"^\s*>\s?")


def paragraphs(lines):
    """Yield (start, end) index pairs of the units EXCLUDE reads. A heading, table row or fenced
    line is its own unit. A list item starts a unit that runs through its continuation lines. Prose
    runs to the next blank line, heading, table row, fence or list item."""
    n = len(lines)
    i = 0
    while i < n:
        if lines[i].strip() == "":
            i += 1
            continue
        if OWN_UNIT.match(lines[i]):
            yield i, i + 1
            i += 1
            continue
        j = i + 1
        while j < n and lines[j].strip() != "" and not OWN_UNIT.match(lines[j]) \
                and not ITEM_START.match(lines[j]):
            j += 1
        yield i, j
        i = j


def classify(line, paragraph=None):
    """PATH / EXCLUDED / REVIEW for one line that already matched TERMS. `paragraph` is the reflowed
    unit the line sits in; when it is None the line is its own unit (the pre-2026-09-17 behaviour,
    kept for the self-test's single-line cases)."""
    stripped = strip_linky(line)
    if not TERMS.search(stripped):
        return "PATH"
    scope = strip_linky(paragraph) if paragraph is not None else stripped
    return "EXCLUDED" if EXCLUDE.search(scope) else "REVIEW"


def sweep(db):
    counts = {"PATH": 0, "EXCLUDED": 0, "SUBJECT": 0, "REVIEW": 0}
    review = []
    files = 0
    for root, dirs, names in os.walk(db):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for n in sorted(names):
            if not n.endswith(".md") or n in SKIP_FILES:
                continue
            files += 1
            p = os.path.join(root, n)
            try:
                text = open(p, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            lines = text.splitlines()
            owner = {}
            for a, b in paragraphs(lines):
                unit = " ".join(QUOTE.sub("", x).strip() for x in lines[a:b])
                for k in range(a, b):
                    owner[k] = unit
            for i, line in enumerate(lines, 1):
                if not TERMS.search(line):
                    continue
                verdict = classify(line, owner.get(i - 1, line))
                if verdict == "REVIEW" and SUBJECT_DIR.search(root):
                    verdict = "SUBJECT"
                counts[verdict] += 1
                if verdict == "REVIEW":
                    review.append((os.path.relpath(p, db), i, line.strip()))
    return files, counts, review


def self_test():
    """The classifier must separate the three cases, or its totals mean nothing."""
    cases = [
        ("see [funclets](../Exception-Handling-And-Unwind/x.md) for more", "PATH"),
        ("the `.pdata`-derived list is not used here", "EXCLUDED"),
        ("parents were enumerated from .pdata chained entries", "REVIEW"),
        ("no unwind table was consulted", "EXCLUDED"),
        ("the unwinder recognises that form as an epilog", "REVIEW"),
        # two code spans with a slash between them: the refusal sits between the spans and must
        # survive the stripping (the closing-backtick defect, 2026-09-17)
        ("the `.pdata` record, which is not evidence - see evidence/x.py - ends at `00310618`",
         "EXCLUDED"),
    ]
    bad = 0
    for text, want in cases:
        got = classify(text)
        if got != want:
            bad += 1
            print("  SELF-TEST FAIL: %r -> %s, wanted %s" % (text, got, want))
    # Paragraph scope (2026-09-17): the refusal on the NEXT line governs; a table row is its own
    # unit so a neighbouring refusal does NOT reach it; a bullet's continuation line is inside it.
    para_cases = [
        (["parents were enumerated from .pdata chained entries.",
          "That population is not used: every parent was re-derived from the body."], 0, "EXCLUDED"),
        (["| `.pdata` | `0x02E78000` | 35,713 entries |",
          "| `.reloc` | not used as evidence | 0 |"], 0, "REVIEW"),
        (["- the loader's extent came from the unwind entry",
          "  and was then refused in favour of the byte-verified end."], 0, "EXCLUDED"),
        (["the unwinder recognises that form as an epilog.", "", "None of this is evidence."], 0,
         "REVIEW"),
    ]
    for lines, idx, want in para_cases:
        units = {}
        for a, b in paragraphs(lines):
            unit = " ".join(QUOTE.sub("", x).strip() for x in lines[a:b])
            for k in range(a, b):
                units[k] = unit
        got = classify(lines[idx], units[idx])
        if got != want:
            bad += 1
            print("  SELF-TEST FAIL (paragraph): %r -> %s, wanted %s" % (lines, got, want))
    total = len(cases) + len(para_cases)
    print("self-test: %d of %d cases correct" % (total - bad, total))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list", action="store_true", help="print every REVIEW line")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")

    files, counts, review = sweep(a.db)
    total = sum(counts.values())

    # PASS 24 APPLIED TO PASS 6. The subject is the PAGE and the evidence is that
    # page's REVIEW lines joined, so a reviewed page stays quiet until ANY of its
    # banned-term lines changes - at which point the disposition LAPSES and the page
    # is reported again. A page is the unit a reviewer actually reads, and a line
    # number is not stable across an edit above it.
    reg = DISP.Registry(a.db, "check_banned_evidence.py")
    by_page = {}
    # THE SUBJECT IS POSIX-SPELLED. os.path.relpath yields backslash separators on
    # Windows, so a registry row written with forward slashes would silently never
    # match: the lookup returns None, nothing is suppressed AND nothing is reported.
    # That is the worst of both, and the silence is how it would go unnoticed.
    for p, i, line in review:
        by_page.setdefault(p.replace(os.sep, "/"), []).append((i, line))
    live = []
    for p in sorted(by_page):
        page_lines = by_page[p]
        joined = chr(10).join(t for _, t in page_lines)
        if reg.suppressed(p, joined):
            continue
        live.extend((p, i, t) for i, t in page_lines)
    suppressed_lines = len(review) - len(live)
    review = live
    print("FINAL-AUDIT-PROTOCOL pass 6 - banned evidence sweep (DIAGNOSTIC, not a gate pass)")
    print("  %d markdown files, %d lines mentioning a banned term" % (files, total))
    print("    PATH      %4d   inside a link target or code span - not a claim" % counts["PATH"])
    print("    EXCLUDED  %4d   the sentence refuses the evidence - the intended state"
          % counts["EXCLUDED"])
    print("    SUBJECT   %4d   inside Exception-Handling-And-Unwind, where it IS the subject"
          % counts["SUBJECT"])
    print("    REVIEW    %4d   of which %d sit on pages with a reviewed disposition"
          % (counts["REVIEW"], suppressed_lines))
    print("    TO READ   %4d   <- the only number that matters" % len(review))
    if a.list:
        for p, i, line in review:
            print("\n  %s:%d\n    %s" % (p, i, line[:300]))
    print()
    lines_out = reg.report()
    for line in lines_out:
        print(line)
    if lines_out:
        print()
    print("  A raw grep returns %d and is dominated by one directory name; the split is the result."
          % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
