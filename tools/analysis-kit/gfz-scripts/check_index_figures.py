#!/usr/bin/env python3
"""check_index_figures.py - canonical index documents quoting a figure that has since moved.

WHY THIS EXISTS. Criterion 5 of the completion condition is that canonical publications and indexes
are INTERNALLY CONSISTENT. Four separate index staleness defects were found by accident on
2026-09-14 alone, each while doing something else:

  FINAL-AUDIT-PROTOCOL.md   "still genuinely unmechanised: 3, 5, 8, 13, 25, 26" - three of the six
                            had instruments, each naming its pass in its own first line
  FINAL-AUDIT-PROTOCOL.md   a readiness table reading "would fail today: 0" when two passes fail
  FINAL-AUDIT-PROTOCOL.md   "rule 5 unmet in 34 of 35, pending the index owner's call" - the call
                            had been made the same night
  RECONSTRUCTION-READINESS-GATE.md  "every contract carries section 8" - true of 34, false of 47

Every one was true when written. **A canonical index does not go wrong by being written badly; it
goes wrong by being right and then not being revisited.** Finding those by accident is not a
method, so this looks for the class on purpose.

WHAT IT DOES. A small set of figures this project quotes constantly - the census population, the
ledger unresolved count, the document count, the contract count - are measured live, then every
`_index/*.md` is scanned for a DIFFERENT value used in the same role. A hit is a sentence that says
a number the corpus no longer agrees with.

WHAT IT IS NOT. It cannot tell a stale figure from a DELIBERATELY HISTORICAL one, and this corpus
is full of the latter on purpose - corrections preserve the number they replaced, and dated addenda
quote what was true on their date. So a hit is a QUESTION, and the tool says which of the two it
cannot distinguish. Suppressing preserved history to make an index look consistent would be the
exact failure the evidence standard forbids.

CONTROL: a figure nobody quotes must produce no hits, and the live population must be found in at
least one index, or the extractor is not reading the documents it claims to read.

AND A SECOND, CONSTRUCTED CONTROL, because the 2026-09-14 narrowing took this from 12 unmarked hits
to 3 and a narrowing that large has to prove it kept the thing the gate exists for. Four sentences
are tested every run against the same regexes the walk uses: `6 of 218 documents` MUST flag, and
`414 mentions across 96 documents` / `61 fences, 288 fields, across 31 documents` / `Of 17 documents
containing one` must NOT. If that ever stops holding the tool refuses to report at all.

WHAT ACTUALLY SEPARATES THE TWO FORMS - established by mutation, and I read it wrong twice first.
SCOPE requires a count, then a UNIT WORD, then a trailing preposition: `414 such mentions across `.
`6 of ` has the preposition but no unit word between it and the count. That is structural. Three
mutations do NOT break it - dropping the `(?!of\b)` lookahead, adding `of` to the alternation, or
BOTH together - because the required unit word carries the separation on its own. Only making the
unit word optional AND adding `of` defeats it, and that mutation is caught: the tool exits 2 and
reports nothing. **A mutation that does not fire means the code is robust OR the mutation missed
its target; three times here it was the second**, which is visible only because it was run.

The `(?!of\b)` lookahead is therefore REDUNDANT and is kept deliberately: it states the intent at
the point of the pattern, and a later edit that relaxes `[A-Za-z()\\-]+` would otherwise silently
remove the only guard.
"""
import argparse
import io
import os
import re
import subprocess
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
# FOUR levels, not three, and this was wrong from the moment the file was written.
# KIT is <repo>/Database/Tools/analysis-kit/gfz-scripts, so three dirname calls land on
# <repo>/Database - and every path built from it became <repo>/Database/Database/... . The
# `unresolved` figure is looked up with os.path.isfile and simply OMITTED when the file is not
# there, so the metric was never measured and never complained: LIVE FIGURES has printed only
# `contracts` and `documents` since the first run and nobody noticed, including me writing the
# summary of that run. **A capability guarded by isfile fails silently by design** - the guard is
# there so a missing input does not crash the gate, and it also means a WRONG PATH looks exactly
# like a missing input. Found 2026-09-14 while checking a peer's correct fix to the directory
# NAME (verify_GFZ_GN160 -> verify_GFZ_PARENT, which tracks the role rather than the generation);
# the name was right and the root was wrong, so the fix could not take effect.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))

# Phrases that mark a sentence as deliberately historical. A figure inside one of these is a
# preserved correction, not a stale claim, and the corpus is REQUIRED to keep them.
#
# A BARE DATE COUNTS, and leaving it out made this gate unable to enforce the rule it exists for.
# EVIDENCE-STANDARD addendum 2026-09-14bg says a ratio against a moving denominator "must state the
# date it was measured, or be replaced by a generated query". Four figures were stamped exactly
# that way - "6 of 221 documents, as measured 2026-09-08" - and the gate still counted them as
# unmarked, because it looked for the words "as of 2026-09-0" and nothing else. **A gate that does
# not accept the remedy it demands cannot be satisfied**, which is a worse failure than a false
# positive: it makes compliance invisible.
HISTORICAL = re.compile(
    r"~~|used to|previously|was\s+\d|superseded|corrected|withdrawn|retracted|no longer|"
    r"at the time|when written|stale|overturned|before\b|earlier|"
    r"original(ly)?|revised|replaced|"
    r"20\d\d-\d\d-\d\d", re.I)


def measure(db):
    """The figures worth checking, measured live. -> {label: (value, how)}"""
    out = {}
    # documents in numbered categories, the denominator progress.py uses
    n = 0
    for dirpath, dirs, files in os.walk(db):
        top = os.path.relpath(dirpath, db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        n += sum(1 for f in files if f.endswith(".md") and f != "README.md")
    out["documents"] = (n, "walk of numbered categories, README excluded")

    c = 0
    for dirpath, dirs, files in os.walk(db):
        c += sum(1 for f in files if f.startswith("CONTRACT-") and f.endswith(".md"))
    out["contracts"] = (c, "CONTRACT-*.md across the corpus")

    # Verify-GfzCheckpoint always writes its residual to work\verify_GFZ_PARENT -
    # the directory name tracks the ROLE, not the generation, so this survives
    # every checkpoint advance.
    resid = os.path.join(REPO, "Database", "Tools", "work", "verify_GFZ_PARENT",
                         "residual_addrs.txt")
    if os.path.isfile(resid):
        k = sum(1 for line in io.open(resid, encoding="utf-8", errors="replace")
                if re.search(r"[0-9A-Fa-f]{8}", line))
        # SAY WHICH SIDE OF THE REPACK THIS IS. During a checkpoint advance the CERTIFIED parent
        # and the PACKED dump disagree, and both numbers are true of different things: on
        # 2026-09-14 this file read 30 while `progress.py` read 139, because the GN161 residual-109
        # application was certified and the function dump had not been regenerated. Neither is
        # wrong and a reader comparing them without the label would take one for a defect in the
        # other - which is precisely the confusion this gate exists to prevent, arriving through
        # the gate itself.
        note = "verify_GFZ_PARENT/residual_addrs.txt - the CERTIFIED parent"
        cov = os.path.join(os.path.dirname(resid), "coverage.tsv")
        packed = os.path.join(REPO, "Database", "Tools", "work", "verify", "coverage.tsv")
        try:
            h1 = io.open(cov, encoding="utf-8", errors="replace").readline()
            h2 = io.open(packed, encoding="utf-8", errors="replace").readline()
            g1 = re.search(r"unresolved=(\d+)", h1)
            g2 = re.search(r"unresolved=(\d+)", h2)
            if g1 and g2 and g1.group(1) != g2.group(1):
                note += "; the PACKED dump still reads unresolved=%s, so an advance is applied " \
                        "and not packed" % g2.group(1)
        except OSError:
            pass
        out["unresolved"] = (k, note)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(REPO, "Database", "FFXII TZA"))
    a = ap.parse_args()
    db = a.db
    idx = os.path.join(db, "_index")
    if not os.path.isdir(idx):
        print("no _index under %s" % db)
        return 2

    figures = measure(db)
    print("LIVE FIGURES")
    for k, (v, how) in sorted(figures.items()):
        print("  %-12s %6d   (%s)" % (k, v, how))

    # ONLY A DENOMINATOR IS A CLAIM ABOUT THE CORPUS. The first working run reported 48, and
    # reading them showed most are SUBSET COUNTS: "13 documents that owed a first audit", "414
    # mentions across 96 documents", "734 rule headings across 10 documents". None of those says
    # anything about how large the corpus is, and flagging them treats every sentence containing
    # a number and a noun as a claim about the total.
    #
    # What IS a claim is the denominator form - "6 of 221 documents", "138 of 306 documents",
    # "across 219 documents", "out of 211 documents". Those name the population, and when the
    # population has grown they are measurements of a date that does not say which date.
    ROLES = {
        "documents": r"documents?|pages?",
        "contracts": r"contracts?",
        "unresolved": r"unresolved|residuals?",
    }
    # the number must be introduced as a total: "of N", "across N", "out of N", "all N"
    DENOM = re.compile(r"\b(?:of|across|among|from|all)\s+$", re.I)

    # "ACROSS N DOCUMENTS" IS A SCOPE, NOT A POPULATION, when something else is being spread over
    # it. Read on 2026-09-14, all twelve unmarked hits resolved and exactly ONE was a claim about
    # how large the corpus is:
    #
    #   "414 such mentions across 96 documents"              96 is where the 414 live
    #   "61 fence(s), 288 field(s), across 31 document(s)"   31 is where they were found
    #   "734 rule headings across 10 documents"              10 is where the headings are
    #   "Of 17 documents containing one, at least 3 ..."     qualified by its own wording
    #   "All 13 documents that owed a first audit"           a named subset
    #   "13296 distinct functions across 404 documents"      404 = numbered categories INCLUDING
    #                                                        README.md; this tool's 365 EXCLUDES
    #                                                        them. Two conventions, both correct.
    #   "6 of 218 documents (2.75 %)"                        <- THE ONLY POPULATION CLAIM
    #
    # The reliable denominator form is `N of M documents` with M UNQUALIFIED. A count of some OTHER
    # unit followed by `across/among/from M documents` states where that count was measured.
    # Flagging those treats every sentence containing a number and a document as a claim about
    # corpus size - the over-reach the `subsets` counter already exists to stop, arriving through a
    # different door.
    #
    # NOTHING IS NARROWED FOR THE REAL FORM: `N of M documents` still flags whenever M is not the
    # live value. That is the shape the one real finding takes, and the shape addendum 2026-09-14bg
    # is about. The control below proves it by construction.
    SCOPE = re.compile(r"\b\d[\d,]*\s+(?!of\b)[A-Za-z()\-]+[^.]{0,80}?"
                       r"\b(?:across|among|from)\s+$", re.I)
    QUALIFIER = re.compile(r"^\s*(?:documents?|pages?)\s+"
                           r"(?:that|which|containing|with|owed|owing|carrying|citing)\b", re.I)

    # HISTORY IN THIS CORPUS IS STRUCTURAL, NOT LEXICAL. The first run reported 175 hits and 74
    # were AUDIT-LOG.md, where every entry correctly states the scope of ITS OWN DATE - "Scope: all
    # 25 documents citing addresses" was true when written and is the log doing its job. A lexical
    # test for "used to" / "previously" cannot see that, because nothing in the sentence is stale.
    #
    # What marks history here is a DATED HEADING: "### 2026-09-02 - ..." in the log, "## Addendum
    # 2026-09-13n" in the standard. Everything under one is a record of a date. Judging those as
    # current figures is the instrument judging a population the convention was never written for -
    # the same error FINAL-AUDIT pass 7 records making with auxiliary tables.
    DATED_HEAD = re.compile(r"^#{1,4}\s.*20\d\d-\d\d-\d\d")

    hits, historical, confirmations, subsets = [], [], 0, 0
    for fn in sorted(os.listdir(idx)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(idx, fn)
        # A DOCUMENT NAMED FOR A DATE IS A RECORD OF THAT DATE. `GOAL-REVISION-2026-09-08.md` is
        # the goal revision OF 2026-09-08; every figure in it is that day's reading by
        # construction, the same way a dated heading works one level down. Not a convenience: the
        # filename is a stronger date marker than any phrase inside the prose.
        file_is_dated = bool(re.search(r"20\d\d-\d\d-\d\d", fn))
        # THE FLAG HAS TO BE STICKY DOWN THE HEADING TREE. A dated entry contains undated
        # sub-headings - "### 2026-09-02 - database established" then "#### Scope" - and resetting
        # on every heading flipped it off immediately, which is why the first structural attempt
        # changed nothing at all: 74 AUDIT-LOG hits before, 74 after. A section stays historical
        # until a heading at the SAME OR SHALLOWER level says otherwise.
        in_dated = False
        dated_level = 0
        for ln, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
            hm = re.match(r"^(#{1,6})\s", line)
            if hm:
                level = len(hm.group(1))
                if DATED_HEAD.match(line):
                    in_dated, dated_level = True, level
                elif in_dated and level <= dated_level:
                    in_dated, dated_level = False, 0
            for label, (live, _how) in figures.items():
                role = ROLES[label]
                for m in re.finditer(r"\b(\d[\d,]{1,6})\s+(?:%s)\b" % role, line, re.I):
                    val = int(m.group(1).replace(",", ""))
                    if val == live:
                        confirmations += 1
                        continue
                    before = line[:m.start(1)]
                    if not DENOM.search(before):
                        subsets += 1
                        continue
                    # A scope ("414 mentions across 96 documents") or an explicitly qualified
                    # subset ("of 17 documents containing one") is not a claim about corpus size.
                    if SCOPE.search(before) or QUALIFIER.match(line[m.end(1):]):
                        subsets += 1
                        continue
                    rec = (fn, ln, label, val, live, line.strip()[:150])
                    is_hist = file_is_dated or in_dated or HISTORICAL.search(line)
                    (historical if is_hist else hits).append(rec)

    print("\n  figures quoted that MATCH the live value        : %d" % confirmations)
    print("  quoted differently, inside historical wording   : %d  (preserved on purpose)"
          % len(historical))
    print("  quoted differently, with NO historical marker   : %d" % len(hits))

    # CONTROL, CONSTRUCTED -----------------------------------------------------
    # The SCOPE and QUALIFIER tests took this from 12 unmarked hits to 3. A narrowing that large
    # has to prove it did not narrow away the thing the gate exists for, and "DJ-1 still shows"
    # is luck rather than proof - it would stop being true the moment DJ-1 is fixed. So the two
    # forms are tested by construction, every run, against the same regexes the walk uses.
    # MIRRORS THE WALK EXACTLY, and the first version did not: it matched "17 documents" as one
    # unit, so `line[m.end():]` began after the noun and QUALIFIER - which looks for
    # "documents containing" - could never fire. The control failed, which is the control working;
    # it caught a difference between itself and the code path it claims to test. A control that
    # does not reproduce the real matching is testing a different function.
    def _would_flag(line, num):
        m = re.search(r"\b(%s)\s+(?:documents?|pages?)\b" % num, line, re.I)
        if not m:
            return None
        before = line[:m.start(1)]
        if not DENOM.search(before):
            return False
        return not (SCOPE.search(before) or QUALIFIER.match(line[m.end(1):]))

    must_flag = _would_flag("the vocabulary is stated in 6 of 218 documents (2.75 %)", 218)
    must_not = [_would_flag("reports 414 such mentions across 96 documents", 96),
                _would_flag("61 fence(s), 288 field(s), across 31 documents in 10 categories", 31),
                _would_flag("Of 17 documents containing one, at least 3 have every marker", 17)]
    print("\n  constructed control: a real denominator flags = %s; three scope/qualified forms "
          "flag = %s" % (must_flag, must_not))
    if must_flag is not True or any(x is not False for x in must_not):
        print("  CONTROL FAILED: the denominator test no longer separates a population claim from")
        print("  a scope count. Every count above is unfounded.")
        return 2
    print("  control passed: the narrowing still catches `N of M documents`.")

    # CONTROL -----------------------------------------------------------------
    # EXTRACTOR HEALTH IS "IT READ QUOTED FIGURES AT ALL", not "some index quotes today's value".
    # The first version required a live match, which is a fact about the corpus: once every index
    # figure had been dated (c31659ad9), no index quoted the live value and the control failed on a
    # healthy extractor, exiting 2 over a real unmarked hit (found 2026-10-01 by a text-only audit
    # pre-run, cloud stream A; OPUS wrote this tool on 2026-09-14). A broken extractor reads nothing
    # in any role, so the sum below is zero exactly when the walk is blind.
    extracted = confirmations + len(historical) + len(hits) + subsets
    if extracted == 0:
        print("\n  CONTROL FAILED: the walk extracted no quoted figure in any role, so the extractor")
        print("  is not reading what it claims to. Every zero above would be meaningless.")
        return 2
    print("\n  control passed: the extractor read %d quoted figures (%d of them the live value)."
          % (extracted, confirmations))

    if hits:
        print("\nQUOTED FIGURES WITH NO HISTORICAL MARKER - each is a QUESTION, not a defect.")
        print("This tool CANNOT tell a stale figure from a deliberately historical one; it can")
        print("only tell you the sentence carries no marker saying which it is.\n")
        for fn, ln, label, val, live, text in hits:
            print("  %s:%d  %s %d, live is %d" % (fn, ln, label, val, live))
            print("      %s" % text)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
