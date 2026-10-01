#!/usr/bin/env python3
"""check_stranded_absence.py - claims of namelessness about addresses that now have names.

WHY THIS CLASS EXISTS AND WHY IT RECURS. An ADDITIVE checkpoint advance renames nothing, so no page
quoting a function's name goes stale. It does not follow that nothing goes stale: a sentence saying
an address is UNRESOLVED, UNNAMED, UNOWNED or UNCLASSIFIED is a claim about the RESIDUAL SET, and
every advance takes addresses OUT of that set. **Those claims are falsified BY the advance,
precisely because it was additive.** 128 addresses left the set between GN158 and GN161.

This recurs at every advance and always will, which is why it is an instrument and not a one-off
sweep. `99-Unresolved-Residual/` is full of the class by construction - it is the folder whose
subject is what has no owner.

WHAT IT MEASURES. For every document whose `gzf_sha256` names a superseded parent, any line that
BOTH cites an address resolved since that stamp AND uses absence language. Each such line is sorted
into five kinds, and only one of them is a defect:

  LIVE CLAIM        the line still asserts namelessness with nothing marking it as historical
  REPAIRED          it names the correction - "residual when surveyed, classified at GN161 ..."
  PAST              ordinary past tense, "was residual", "no longer", struck through
  LINK-TITLE ONLY   the absence word appears only inside a markdown link LABEL
  SURVEY REFERENCE  it refers to the survey or the list as an artifact, not to a current state

LINK-TITLE ONLY IS NOT A CURIOSITY, IT IS THE DOMINANT FALSE POSITIVE HERE. The canonical page is
*titled* `the unresolved 158`, so EVERY page that links to it contains the word "unresolved" beside
whatever addresses it discusses. A sweep without this test reports the corpus's own cross-references
as stale claims - and reports more of them the better cross-referenced the corpus becomes.

HOW THE KINDS WERE ESTABLISHED, because it took three passes. A first sweep found 37 lines in 13
documents and they were routed to the folder's owner, who corrected 29, verified 5 as history and
re-routed 3. **A naive re-run then reported 25 still matching, which reads like the repair failed
and is wrong**: a corrected sentence still contains the word `residual` and the same address,
because it now says *"residual when surveyed, classified at GN161 as ..."*. That is the repair, not
the defect. Two further refinements - the repair vocabulary, then link labels - took the same 25
lines to 9 REPAIRED, 5 PAST, 3 LINK-TITLE, 1 SURVEY REFERENCE and 7 LIVE.

**A count that does not fall after a repair is a claim about the INSTRUMENT, not about the work.**

CONTROLS, every run: the resolved set must be non-empty and must nest inside the stamped set, or the
lineage is not additive and nothing below is founded; at least one line in the corpus must classify
as REPAIRED, or the repair vocabulary has drifted away from what the corpus actually writes; and a
constructed line of each kind is classified, so a future edit cannot quietly collapse the kinds.
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_transfer_eligible import (ADDR, RESIDUAL_FILES, STAMP,  # noqa: E402
                                     lineage_tags, load_addrs)

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")

ABS = r"unresolved|unnamed|unowned|no owner|no name|residual|unclassified"
ABSENCE = re.compile(r"\b(?:%s)\b" % ABS, re.I)
LINKLABEL = re.compile(r"\[[^\]]*\b(?:%s)\b[^\]]*\]\([^)]*\)" % ABS, re.I)
# NAMING A CHECKPOINT GENERATION IS ITSELF THE REPAIR SIGNAL, and that is a rule rather than a
# fitted pattern: a STRANDED claim predates the advance and cannot mention it, while a repaired one
# is ABOUT the advance. Widened 2026-09-14 after a peer wrote a better repair than this could read:
#
#   "the GN158->GN161 advance changed only CodeDomain tags and comments, so neither structural
#    figure can move ... so '386 unclassified native routines' may now overstate by <=4. The
#    original parent list is not preserved, so an exact per-class recount awaits method recovery;
#    the totals stand."
#
# That bounds the error, cites the advance, says why an exact recount is impossible and states what
# survives - and the earlier pattern called it a LIVE CLAIM, because it happened not to use the
# words "when surveyed". **The count went 6 -> 7 and neither new debt nor a regression caused it.**
# Verified against all six known live claims and both known repairs: 0 misclassifications.
# WRITTEN WITH AN EDITOR-SAFE REPLACE, NOT A SHELL HEREDOC. The first attempt went through
# `python - <<'PY'` and every backslash-b in a non-raw string became a literal BACKSPACE (0x08), so
# the pattern read <BS>GN1\d\d<BS> and could never match. sed and the terminal render 0x08
# invisibly, so the file LOOKED correct and the self-test failed for no visible reason -
# only repr() showed it. Second time this session, against a standing note not to patch
# regexes by heredoc.
REPAIRED = re.compile(r"when surveyed|158 survey|at survey date|now classified|since classified|"
                      r"classified since|\bGN1\d\d\b|\bGM1\d\d\b|\bR109\b", re.I)
PAST = re.compile(r"\bwas\b|\bwere\b|\bused to\b|\bno longer\b|\bwent\b|~~|\bpreviously\b|"
                  r"\bhas since\b|\bat the time\b", re.I)
SURVEYREF = re.compile(r"residual survey|the survey\b|survey used|residual list|"
                       r"residual_addrs|the 158\b", re.I)


def classify(line, context=None):
    """-> one of the five kinds, or None when the line makes no absence statement.

    `context` is the contiguous block the line sits in (a paragraph or a blockquote). ONLY the
    REPAIRED test reads it, and that is deliberate.

    **A PROSE REPAIR SPANS LINES, AND THE MARKER IS OFTEN NOT ON THE LINE THAT NEEDS IT.** The case
    that forced this: a four-line blockquote naming `GN158->GN161` on its first line and carrying
    the absence word - *"so '386 unclassified native routines' may now overstate by <=4"* - on its
    fourth. Line by line, the fourth reads as a LIVE CLAIM while the paragraph it belongs to is one
    of the most careful repairs in the corpus.

    The other tests stay line-scoped on purpose. Widening PAST or SURVEY REFERENCE to a paragraph
    would let one historical sentence clear a live claim sitting three lines below it, which is the
    over-clearing this instrument exists to avoid.
    """
    if not ABSENCE.search(line):
        return None
    if not ABSENCE.search(LINKLABEL.sub("", line)):
        return "LINK-TITLE ONLY"
    if REPAIRED.search(context if context is not None else line):
        return "REPAIRED"
    if PAST.search(line):
        return "PAST"
    if SURVEYREF.search(line):
        return "SURVEY REFERENCE"
    return "LIVE CLAIM"


def _self_test():
    cases = [
        ("`002B8EE0`, residual when surveyed - classified at GN161 `Presentation.Icon.Pulsing`",
         "REPAIRED"),
        ("[The unresolved 158](the-unresolved-158.md) groups them", "LINK-TITLE ONLY"),
        ("`001E8580` was residual #6 by size and marked unread", "PAST"),
        ("the call graph the residual survey used records `002AAE40`", "SURVEY REFERENCE"),
        ("Four unclassified residual functions call `0017F850`", "LIVE CLAIM"),
        # the peer repair that the first pattern misread - asserted so a future narrowing cannot
        # quietly lose it again
        ("the GN158->GN161 advance changed only CodeDomain tags, so \"386 unclassified native "
         "routines\" may now overstate by <=4", "REPAIRED"),
        # and its converse: a live claim must not be cleared just because a number is near it
        ("- The residual functions `003BDDE0`, `003BDFF0` and `003C1A20` read the table",
         "LIVE CLAIM"),
        ("the transform composer has 82 distinct callers", None),
    ]
    bad = [(t, want, classify(t)) for t, want in cases if classify(t) != want]

    # THE MULTI-LINE CASES, asserted separately because they are the ones a line-scoped test
    # cannot see. The marker sits on a DIFFERENT line of the same paragraph - above it in the
    # blockquote case, below it in the cluster case - and both are real corpus text.
    ctx_cases = [
        ("groups `002B8EE0`, `002BCB00` and `002DBDD0` as residual",
         "groups `002B8EE0`, `002BCB00` and `002DBDD0` as residual\n"
         "cluster 3, 6,775 bytes. **All three are now read and classified at GN161**:",
         "REPAIRED"),
        ('so "386 unclassified native routines" may now overstate by <=4',
         "> the GN158->GN161 advance changed only CodeDomain tags and comments\n"
         '> so "386 unclassified native routines" may now overstate by <=4',
         "REPAIRED"),
        # AND THE CONVERSE, which is what stops block context becoming over-clearing: a LIVE claim
        # must stay live even when an unrelated repaired sentence shares its paragraph.
        ("- The residual functions `003BDDE0` and `003C1A20` read the table",
         "- The residual functions `003BDDE0` and `003C1A20` read the table\n"
         "- an unrelated neighbour sentence with no marker at all",
         "LIVE CLAIM"),
    ]
    for line, ctx, want in ctx_cases:
        got = classify(line, ctx)
        if got != want:
            bad.append((line, want, got))

    for t, want, got in bad:
        print("  SELF-TEST FAIL: wanted %s, got %s for %r" % (want, got, t[:60]))
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--list", action="store_true", help="print every line, not only LIVE CLAIM")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if not _self_test():
        print("\n  CONTROL FAILED: the five kinds are no longer separated. Nothing is reported.")
        return 2
    print("  control passed: a constructed line of each kind classifies correctly.")
    if a.self_test:
        return 0

    sets = {k: load_addrs(v) for k, v in RESIDUAL_FILES.items()}
    if any(v is None for v in sets.values()):
        print("CANNOT RUN: a residual set is not in the tree")
        return 2
    if not (sets["PARENT"] <= sets["GN160"] <= sets["GN158"]):
        print("CONTROL FAILED: the residual sets do not nest, so the lineage is not additive")
        print("in the resolved direction and this whole class is unfounded. Nothing reported.")
        return 2
    resolved = {"GN158": sets["GN158"] - sets["PARENT"],
                "GN159": sets["GN158"] - sets["PARENT"],   # superset; GN159 has no kept file
                "GN160": sets["GN160"] - sets["PARENT"]}
    if not resolved["GN158"]:
        print("no address has left the residual set since the oldest stamp - nothing to check")
        return 0
    print("  addresses resolved since GN158: %d   since GN160: %d"
          % (len(resolved["GN158"]), len(resolved["GN160"])))

    tags = lineage_tags()
    kinds = collections.Counter()
    live = []
    for dirpath, _d, files in os.walk(a.db):
        if any(os.sep + x in dirpath for x in ("_index", "_types", "_templates")):
            continue
        for fn in sorted(files):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            p = os.path.join(dirpath, fn)
            txt = io.open(p, encoding="utf-8", errors="replace").read()
            m = STAMP.search(txt)
            if not m:
                continue
            tag = tags.get(m.group(1)[:24].lower())
            if tag not in resolved:
                continue
            rel = os.path.relpath(p, a.db)
            lines = txt.split("\n")
            # The contiguous non-blank run a line sits in - its paragraph or blockquote. Only the
            # REPAIRED test reads it; see classify().
            blocks = {}
            start = 0
            for i, s in enumerate(lines):
                if not s.strip():
                    for j in range(start, i):
                        blocks[j] = "\n".join(lines[start:i])
                    start = i + 1
            for j in range(start, len(lines)):
                blocks[j] = "\n".join(lines[start:])

            for ln, line in enumerate(lines, 1):
                hit = {h.group(1).upper().zfill(8) for h in ADDR.finditer(line)} & resolved[tag]
                if not hit:
                    continue
                k = classify(line, blocks.get(ln - 1, line))
                if k is None:
                    continue
                kinds[k] += 1
                if k == "LIVE CLAIM" or a.list:
                    live.append((rel, ln, k, sorted(hit)[:3], line.strip()[:130]))

    total = sum(kinds.values())
    print("\nLINES CITING A RESOLVED ADDRESS WITH ABSENCE LANGUAGE: %d" % total)
    for k in ("LIVE CLAIM", "REPAIRED", "PAST", "LINK-TITLE ONLY", "SURVEY REFERENCE"):
        print("  %-18s %4d%s" % (k, kinds[k], "   <- the only defect kind"
                                 if k == "LIVE CLAIM" else ""))

    # CONTROL: the repair vocabulary must still match what the corpus writes.
    if total and not kinds["REPAIRED"]:
        print("\n  CONTROL FAILED: not one line in the corpus reads as REPAIRED. Either no repair")
        print("  has ever been made, or the repair vocabulary has drifted from what authors write")
        print("  and every LIVE CLAIM above is suspect. Read before routing.")
        return 2
    if total:
        print("\n  control passed: the corpus contains repaired lines this recognises.")

    if live:
        print("\n%s" % ("EVERY LINE" if a.list else "LIVE CLAIMS - each is a QUESTION for the "
                        "document's owner, not a verdict"))
        for rel, ln, k, ex, text in sorted(live):
            print("  %-58s :%-5d %-16s %s" % (rel[:58], ln, k if a.list else "", " ".join(ex)))
            print("      %s" % text)
    return 1 if kinds["LIVE CLAIM"] else 0


if __name__ == "__main__":
    sys.exit(main())
