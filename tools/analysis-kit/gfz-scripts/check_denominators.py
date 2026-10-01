#!/usr/bin/env python3
"""check_denominators.py - find percentages whose denominator is never stated.

Why this exists
---------------
Proposed by a parallel session on 2026-09-02 after a falsification pass found that three of its ten
findings across two documents were **the same shape**: a correction or an exclusion applied to one
number and not to the number printed beside it.

  * a census stale by two, because one figure was refreshed and the one next to it was not;
  * a scan correction applied to a distinct-function count and not to the slot counts on the same
    line (`.data` understated ~15-fold as a result);
  * an exclusion of 3,891 exception funclets that four separate figures depend on and no caption
    declares.

Their rule, which this implements the mechanizable half of:

    **Re-derive every number in a table from ONE stated population, and fail the table if any row
    needs a different one.**

The half a script can do is the percentage: a percentage is a numerator and a denominator, and the
denominator is the population. If a document writes "70.4 % of the executable" and the only
population that reproduces 70.4 % is 34,270 -- the non-funclet subset -- while the document says
"the executable", the denominator is doing work nobody declared.  Against all 38,161 the same
numerator is 63.2 %.

What it does
------------
For each `N ... P %` pair on a line (or across a short window), it tries every KNOWN population and
reports which one reproduces P.  Then it asks whether that population is NAMED anywhere near the
claim.  Three outcomes:

  RECONCILED   exactly one known population reproduces P, and the document names it nearby.  Silent.
  UNDECLARED   exactly one population reproduces P, and the document does not name it nearby.  This
               is the defect the rule is aimed at.
  UNRECONCILED no known population reproduces P.  Usually a local population (a table of 112
               records, say) -- reported at low priority, because it may be perfectly correct.

What it does NOT do
-------------------
It cannot re-derive a count from the binary, so it does not know whether N itself is right.  It only
checks that N, P and a *stated* population are mutually consistent.  A document that is wrong in the
same way twice will pass.

It also cannot see a population defined three sections earlier in prose; the window is deliberately
local, because a denominator a reader has to hunt for is most of the defect.

Usage
-----
    python check_denominators.py --db "Database/FFXII TZA"
    python check_denominators.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

# The certified populations, from `Tools/work/verify_GFZ_PARENT/coverage.tsv` line 1
# (GN161, 2026-09-14).  A percentage in this database is nearly always taken
# against one of these. UPDATE AT EVERY CHECKPOINT SEAL - the values are the
# moving part; documents that quoted an older generation's population keep
# their numbers only inside a dated marker.
POPULATIONS = {
    38956: "listed + UC-1 frontier incl. funclets (38,160 listed + 796; post-2026-09-29 series)",
    38955: "listed + UC-1 frontier incl. funclets (38,160 listed + 795; 2026-09-28, pre-257-up application)",
    38856: "listed + UC-1 1-64 frontier incl. funclets (38,160 + 696; 2026-09-28, pre-65-256 application)",
    38161: "all internal functions",
    38160: "listed functions incl. funclets, post-2026-09-28 (38,161 less removed 007EE7F0)",
    35065: "listed + UC-1 frontier (34,269 listed + 796 frontier; post-2026-09-29 series)",
    35064: "listed + UC-1 frontier (34,269 + 795; 2026-09-28, pre-257-up application)",
    34965: "listed + UC-1 1-64 frontier (34,269 + 696; 2026-09-28, pre-65-256 application)",
    34270: "non-funclet functions, pre-2026-09-28 series (38,161 less the 3,891 funclets)",
    34269: "listed non-funclet functions, post-2026-09-28 (after 007EE7F0's removal)",
    28137: "CodeDomain-tagged functions",
    10024: "functions with no CodeDomain",
    9409:  "PrimaryOwner functions",
    3891:  "exception funclets",
    796:   "UC-1 B band frontier bodies (696 + 99 + 1; admitted 2026-09-28/29)",
    795:   "UC-1 B band frontier bodies (696 + 99; admitted 2026-09-28)",
    696:   "UC-1 1-64 B band frontier bodies (admitted 2026-09-28)",
    99:    "UC-1 65-256 B band frontier bodies (admitted 2026-09-28)",
    585:   "FinalNoPrimaryOwner functions",
    30:    "unresolved functions",
}

# Series synonyms -- members name the SAME logical population across a dated
# series break. Added 2026-09-28 (UC-1): listing 34,270 alongside 34,269 (and
# 38,161 alongside 38,160) made every percentage in their shared band reconcile
# to TWO populations, and reconcile()'s exactly-one-hit rule then skipped them
# all -- the negative control went dead (AUDITSPEC-CONTRA-DATA-UC1BAND-DENOM-
# SELFTEST). A figure hitting every member of one group is ONE logical hit on
# that population; naming ANY member declares it. Hits spanning two groups
# (e.g. 34,269 vs the frontier-inclusive 34,965) stay ambiguous and skipped.
# First element is the current-series representative printed in findings.
SERIES_SYNONYMS = [
    (34269, 34270),   # listed non-funclet: post-break / pre-2026-09-28
    (38160, 38161),   # listed incl. funclets: post-break / pre-2026-09-28
    (35065, 35064, 34965),   # frontier incl.: post-257-up / post-65-256 / pre-65-256
    (38956, 38955, 38856),   # frontier incl. funclets: post-257-up / post-65-256 / pre-65-256
]


def synonym_group(pop):
    """The series group `pop` belongs to, as a set; {pop} when ungrouped."""
    for g in SERIES_SYNONYMS:
        if pop in g:
            return set(g)
    return {pop}

# "7,186 of 10,923 = 65.8 %", "8,458 of it (35.1 %)", "24,116 functions ... 70.4 %"
# `(?!\d|\.\d)` keeps NUM from splitting a decimal: "100.1 %" must not read as
# numerator 100 over a 1 % figure (found 2026-09-28 on TYPE-COVERAGE.md's
# "reported 100.1 % where the truth is 100.0 %" -- num 100, pct 1, reconciling
# to 10,024 at 0.998 %). A period followed by a digit is a decimal point; a
# sentence-ending "34,270." still terminates the number.
NUM = r"(\d[\d,]{2,})(?!\d|\.\d)"
PCT = r"(\d{1,3}(?:\.\d{1,2})?)\s*%"
PAIR = re.compile(NUM + r"[^\n%]{0,80}?" + PCT)
# An explicit "N of D" states its own denominator and is self-declaring.
OF = re.compile(NUM + r"\s+(?:of|/|out of)\s+" + NUM)

TOL = 0.06   # a percentage printed to one decimal reconciles within about this much


def to_int(s):
    return int(s.replace(",", ""))


def reconcile(num, pct):
    """Which known populations reproduce `pct` as num/pop?"""
    hits = []
    for pop in POPULATIONS:
        if pop <= 0 or num > pop:
            continue
        if abs(100.0 * num / pop - pct) <= TOL:
            hits.append(pop)
    return hits


def scan(text, rel, out):
    lines = text.split("\n")
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith(("#", ">")):
            continue
        for m in PAIR.finditer(line):
            num, pct = to_int(m.group(1)), float(m.group(2))
            if num < 100:
                continue
            hits = reconcile(num, pct)
            # Same-generation synonyms collapse to one logical hit: a figure
            # inside a series break's shared band is a statement about that
            # population, and its declaration may name either series value.
            for g in SERIES_SYNONYMS:
                if hits and set(hits) <= set(g):
                    hits = [g[0]]
                    break
            if len(hits) != 1:
                continue                      # unreconciled, or ambiguous -- not this check's job
            pop = hits[0]
            group = synonym_group(pop)
            # Is the population NAMED near the claim?  Its digits, with or without separators, in a
            # window around the line.  An explicit "N of D" on the line counts as declaring D.
            # +/-10, and measured from the TABLE rather than the line.  At +/-4 this check
            # reported the partition table in `vtable-method-index.md`, whose caption declares
            # "all 34,270 functions" five lines above the first row -- a false positive
            # manufactured by the window, the same defect class as a scanner regex that only
            # matched `0x`-prefixed displacements.  A caption sits above a header row and a
            # separator row, so caption-to-last-row distance grows with the table's height.
            lo = n - 10
            for b in range(n - 1, max(1, n - 14), -1):
                if not lines[b - 1].lstrip().startswith("|"):
                    lo = b - 10          # first non-table line above: search from there
                    break
            window = "\n".join(lines[max(0, lo):n + 4])
            forms = [f for m in group for f in ("%d" % m, "{:,}".format(m))]
            declared = any(f in window for f in forms)
            if not declared:
                for om in OF.finditer(window):
                    if to_int(om.group(2)) in group:
                        declared = True
                        break
            # A LOCAL DENOMINATOR THAT REPRODUCES THE FIGURE IS DECLARED, even when it is not one
            # of POPULATIONS. Added 2026-09-14 (OPUS) after this check reported
            # `_index/UNEXPLAINED-GLOBALS.md` for a row reading "508 of 33,382 explained by
            # nothing (1.52 %)": 508/33,382 = 1.5218 %, the printed figure, while the only KNOWN
            # population inside TOL was 34,270 at 1.4823 %. The old "N of D" escape only accepted
            # D when D was the reconciled population, so a document stating a legitimate local
            # denominator could never satisfy it -- and rewriting the row to name 34,270 would
            # have made the percentage wrong. **This does not weaken the check**: a D that does
            # not reproduce the printed percentage is still not accepted, and the numerator has to
            # match too. Same defect class as the `100 %`-row case below.
            if not declared:
                for om in OF.finditer(window):
                    d = to_int(om.group(2))
                    if (to_int(om.group(1)) == num and d > 0
                            and abs(100.0 * num / d - pct) <= TOL):
                        declared = True
                        break
            # A CAPTION-STATED LOCAL DENOMINATOR is declared the same way an
            # inline "N of D" is. Found 2026-09-28 on COMPLETION-PLAN.md's
            # entry-only size table: the caption reads "Of the 10,790
            # entry-only functions" -- D stated ahead of the rows, in reverse
            # word order, so neither the `N of D` escape nor the named-digits
            # check could see it. The row "| 1,024 B or more | 317 | 2.9 %"
            # then reconciled `1,024` against 34,965 while the real numerator
            # is the other number in the row: 317 / 10,790 = 2.9 %. Rule: a
            # window naming `of [the] NUM` accepts the figure when ANY number
            # on the flagged line reproduces the percentage against it.
            if not declared:
                for om in re.finditer(r"\b[Oo]f\s+(?:the\s+)?" + NUM, window):
                    d = to_int(om.group(1))
                    if d <= 0:
                        continue
                    for nm in re.finditer(NUM, line):
                        if abs(100.0 * to_int(nm.group(1)) / d - pct) <= TOL:
                            declared = True
                            break
                    if declared:
                        break
            # A TABLE THAT CARRIES ITS OWN `100 %` ROW HAS DECLARED ITS DENOMINATOR, and it is a
            # local one this checker's population list does not contain.
            #
            # Found 2026-09-08 on `why-the-unowned-code-has-no-owner.md`: a table whose first row
            # reads `| certified .rdata function-pointer slots | 27,202 | 100 % |` and whose last
            # reads `| uncharacterised | 266 | 0.98 % |`. **266 / 27,202 = 0.978 %, which rounds to
            # exactly the figure printed.** The checker instead reconciled it against 28,009
            # CodeDomain-tagged functions -- a global population that gives 0.95 %, not 0.98 -- and
            # then reported the document for not naming a denominator it never used.
            #
            # **The document was right and the checker was wrong**, and the tolerance that let a
            # 0.95 match a printed 0.98 is why. Rather than re-tune the tolerance and hope, a local
            # `100 %` row is now believed over any inferred population.
            if not declared:
                for b in range(n, max(1, n - 24), -1):
                    row = lines[b - 1].lstrip()
                    if not row.startswith("|"):
                        break
                    for rm in PAIR.finditer(row):
                        if abs(float(rm.group(2)) - 100.0) < 0.001:
                            local = to_int(rm.group(1))
                            if local and abs(100.0 * num / local - pct) < 0.05:
                                declared = True
                    if declared:
                        break
            if not declared:
                out.append((rel, n, num, pct, pop, line.strip()))


SELF_TEST_BAD = "The residual is 24,116 functions, **70.4 % of the executable**.\n"
SELF_TEST_OK = ("Of the 34,270 non-funclet functions the residual is 24,116, "
                "**70.4 % of them**.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        # 24,116 / 34,270 = 70.37 %.  Undeclared in the first, declared in the second.
        bad, ok = [], []
        scan(SELF_TEST_BAD, "<bad>", bad)
        scan(SELF_TEST_OK, "<ok>", ok)
        if len(bad) != 1 or len(ok) != 0:
            print("SELF-TEST FAILED: bad=%d (want 1) ok=%d (want 0)" % (len(bad), len(ok)))
            return 1
        # And a control the check must NOT fire on: a percentage of a local population.
        local = []
        scan("41 of the 112 records, 36.6 %.\n", "<local>", local)
        if local:
            print("SELF-TEST FAILED: fired on a local population it cannot know")
            return 1
        # Series synonyms (2026-09-28 UC-1): naming EITHER member of the
        # 34,270/34,269 group declares the figure. The raw reconcile() hits
        # both - that is what killed the negative control above.
        raw = reconcile(24116, 70.4)
        if set(raw) != {34270, 34269}:
            print("SELF-TEST FAILED: reconcile(24116,70.4) = %s (want both series members)"
                  % raw)
            return 1
        syn = []
        scan("Of the 34,269 listed non-funclet functions the residual is 24,116, "
             "**70.4 % of them**.\n", "<syn>", syn)
        if syn:
            print("SELF-TEST FAILED: post-break synonym 34,269 did not declare the figure")
            return 1
        # A DIFFERENT population is not a declaration: naming 34,965 (frontier-
        # inclusive) does not cover a figure reconciling to the listed series.
        wrong = []
        scan("The residual is 24,116 of the 34,965 frontier-inclusive functions, "
             "**70.4 %**.\n", "<wrong>", wrong)
        if len(wrong) != 1:
            print("SELF-TEST FAILED: naming a different population suppressed the finding "
                  "(wrong=%d, want 1)" % len(wrong))
            return 1
        print("self-test ok: fires on the undeclared denominator, silent on the declared one, "
              "on series synonyms and on local populations")
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    out = []
    # POPULATION. `_inbox/` holds peer handoff notes, which `COVERAGE.md` does not count as
    # documents. `AUDIT-LOG.md` is an APPEND-ONLY historical record: a figure written there was
    # correct when written, and retro-editing a log to satisfy a checker destroys the one property
    # that makes it worth keeping. Both are excluded and both counts are printed.
    APPEND_ONLY = ("AUDIT-LOG.md",)
    skipped = {"inbox": 0, "append_only": 0}

    for root, _d, files in os.walk(a.db):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, a.db)
            if "_inbox" in rel.replace(chr(92), "/").split("/"):
                skipped["inbox"] += 1
                continue
            if fn in APPEND_ONLY:
                skipped["append_only"] += 1
                continue
            scan(io.open(p, encoding="utf-8", errors="replace").read(), rel, out)

    print("population: every .md under the database root, EXCLUDING %d in _inbox/ and %d "
          "append-only log(s)" % (skipped["inbox"], skipped["append_only"]))
    print()

    if not out:
        print("no percentage relies on an undeclared certified population")
        return 0

    print("PERCENTAGES WHOSE DENOMINATOR IS NEVER STATED NEARBY")
    print("Each is a QUESTION, not a defect: the figure may be right and merely unlabelled.")
    print("But a reader cannot check it, and a reader taking the obvious denominator gets a")
    print("different number -- which is how '70.4 % of the executable' meant 63.2 %.\n")
    by = collections.defaultdict(list)
    for rel, n, num, pct, pop, line in out:
        by[rel].append((n, num, pct, pop, line))
    for rel in sorted(by):
        print("  %s" % rel)
        for n, num, pct, pop, line in by[rel]:
            print("      line %d  %s = %.4g%% only of %s (%s)"
                  % (n, "{:,}".format(num), pct, "{:,}".format(pop), POPULATIONS[pop]))
            print("        %s" % line[:100])
        print()
    print("%d undeclared denominator(s) in %d document(s)" % (len(out), len(by)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
