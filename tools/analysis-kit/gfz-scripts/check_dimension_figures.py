#!/usr/bin/env python3
"""check_dimension_figures.py - an index quoting a scored dimension at a value it no longer has.

WHY THIS EXISTS. Four canonical indexes were found on 2026-09-14 quoting a scored dimension at a
superseded value, every one of them by accident while doing something else:

  FINAL-AUDIT-PROTOCOL.md   "139 unresolved, 1,280 questions open" - 30 and 1,268
  TYPE-COVERAGE.md          "302 gaps" against "1,906 fields"      - 280 and 1,971
  RECONSTRUCTION-READINESS-GATE.md  "34 of 34 contracts executed, 0 nothing-executed" - 47 and 4,
                            which moved an L2 verdict off MET
  COMPLETION-PLAN.md        section 2, titled "Where it stands", with SEVEN of eight rows
                            superseded - `ebp_explained` read `0 / 14` and is FINISHED

**Finding four of these by accident is not a method**, which is the same sentence
`check_index_figures.py` opens with about a different figure class. That one watches the corpus
POPULATIONS - documents, contracts, unresolved. This one watches the eight SCORED DIMENSIONS, whose
values are produced by `progress.py` and are the numbers the completion argument is made of.

WHAT IT DOES. Runs `progress.py`, takes each dimension's current `numerator / denominator`, and
scans `_index/*.md` for a line that NAMES the dimension and quotes a different pair in the same
shape. A hit is a sentence asserting a score the scorer does not produce.

WHAT IT CANNOT DO, and the four lessons that shaped it - every one learned the expensive way today:

  A DATED HEADING OR A DATED FILENAME IS HISTORY. A plan's starting position, an audit-log entry,
  `GOAL-REVISION-2026-09-08.md` - all legitimately quote what was true on their date. Sticky down
  the heading tree, because a dated entry contains undated sub-headings.

  A STRUCK-THROUGH OR MARKED FIGURE IS A PRESERVED CORRECTION. This corpus is required to keep the
  number it replaced; suppressing that to make an index look consistent is the exact failure the
  evidence standard forbids.

  THE PAIR MUST BE NEAR THE NAME. `13,117` alone means nothing; `engine_explained | 6,811 / 34,270`
  is a claim. Requiring the dimension name within the same line is what stops this reporting every
  number in the corpus.

  AND THE REMEDY FOR A FALSE POSITIVE IS TO MARK THE PROSE, NOT TO WIDEN THIS. When my own
  replacement text for COMPLETION-PLAN tripped `check_index_figures`, the fix was to write "was 166
  ... is now 365" rather than teach the gate the phrase "went from". **Widening a test to clear the
  thing under test is how a gate stops working**, and this file is as vulnerable to that as any.

CONTROL, every run: `progress.py` must yield all eight dimensions, and at least one index must
quote one of them at its CURRENT value - otherwise the extractor is not reading what it claims to
and every zero below is meaningless.
"""
import argparse
import io
import os
import re
import subprocess
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")

DIM = re.compile(r"^\s{2}([a-z_]+)\s+\[[#.]+\]\s+([\d.]+)%\s+(\d[\d,]*)\s*/\s*(\d[\d,]*)")
DATED_HEAD = re.compile(r"^#{1,4}\s.*20\d\d-\d\d-\d\d")
DATED_FILE = re.compile(r"20\d\d-\d\d-\d\d")
# A preserved correction is marked. Keeping it is REQUIRED, so a marked line is never a defect.
MARKED = re.compile(r"~~|\bwas\b|\bwere\b|used to|previously|superseded|corrected|no longer|"
                    r"stale|overturned|earlier|original(ly)?|revised|replaced|restated|"
                    r"at the time|when written|starting position|\bhad\b", re.I)


# THE MARKER IS USUALLY NOT ON THE LINE IT CLEARS, and that is not a quirk of one document -
# it happened three separate times on 2026-09-14, in three different instruments:
#
#   an attribution lived in a table's COLUMN HEADER, one row above its entries
#   a repair read "All three are now read and classified at GN161" one line BELOW the claim
#   a preserved table was annotated by a block AFTER it - "the table above is kept ... it is not
#     the current state" - which is exactly the shape a correctly preserved correction takes here
#
# So MARKED is tested over a CONTEXT, not a line - and the context is STRUCTURAL rather than a line
# count. A fixed window cannot work here: a marker placed above a table has to reach the table's
# LAST row, and only the table knows how long it is. A six-line window left exactly one row of an
# eight-row table uncleared, in the middle, with a marker above it and another below.
#
# The context is the contiguous non-blank block the line sits in, PLUS the blocks immediately
# before and after it. That covers all three observed shapes - a column header inside the same
# block, a repair line inside the same block, an annotation in the neighbouring block - without a
# magic number, and it still will not let a marker at the other end of the document clear
# anything.
CONTEXT_BLOCKS = 1

def current():
    """-> {dimension: (num, den)} from progress.py, the scorer itself."""
    r = subprocess.run([sys.executable, os.path.join(KIT, "progress.py")],
                       capture_output=True, text=True, cwd=REPO)
    out = {}
    for line in r.stdout.split("\n"):
        m = DIM.match(line)
        if m:
            out[m.group(1)] = (int(m.group(3).replace(",", "")),
                               int(m.group(4).replace(",", "")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()

    dims = current()
    if len(dims) < 8:
        print("CANNOT RUN: progress.py yielded %d dimension(s), expected 8. Nothing is reported,"
              % len(dims))
        print("because a partial scorer would make every zero below meaningless.")
        return 2
    print("CURRENT SCORED DIMENSIONS (progress.py)")
    for k, (n, d) in sorted(dims.items()):
        print("  %-20s %8s / %-8s" % (k, "{:,}".format(n), "{:,}".format(d)))

    idx = os.path.join(a.db, "_index")
    hits, confirmations, marked, historical = [], 0, 0, 0
    for fn in sorted(os.listdir(idx)):
        if not fn.endswith(".md"):
            continue
        file_dated = bool(DATED_FILE.search(fn))
        in_dated, level = False, 0
        all_lines = io.open(os.path.join(idx, fn), encoding="utf-8",
                            errors="replace").read().splitlines()
        # Contiguous non-blank runs, and for each line the index of the run it belongs to.
        runs, of_run, cur = [], {}, []
        for i, t in enumerate(all_lines):
            if t.strip():
                cur.append(i)
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        for ri, r in enumerate(runs):
            for i in r:
                of_run[i] = ri
        ctx_cache = {}

        def context_of(i):
            ri = of_run.get(i)
            if ri is None:
                return all_lines[i]
            if ri not in ctx_cache:
                lo = max(0, ri - CONTEXT_BLOCKS)
                hi = min(len(runs), ri + CONTEXT_BLOCKS + 1)
                idxs = [x for rr in runs[lo:hi] for x in rr]
                ctx_cache[ri] = "\n".join(all_lines[x] for x in idxs)
            return ctx_cache[ri]

        for ln, line in enumerate(all_lines, 1):
            hm = re.match(r"^(#{1,6})\s", line)
            if hm:
                lv = len(hm.group(1))
                if DATED_HEAD.match(line):
                    in_dated, level = True, lv
                elif in_dated and lv <= level:
                    in_dated, level = False, 0
            for dim, (n, d) in dims.items():
                if dim not in line:
                    continue
                for m in re.finditer(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)", line):
                    qn = int(m.group(1).replace(",", ""))
                    qd = int(m.group(2).replace(",", ""))
                    if (qn, qd) == (n, d):
                        confirmations += 1
                    elif file_dated or in_dated:
                        historical += 1
                    elif MARKED.search(context_of(ln - 1)):
                        marked += 1
                    else:
                        hits.append((fn, ln, dim, qn, qd, n, d, line.strip()[:120]))

    print("\n  quoted at the CURRENT value            : %d" % confirmations)
    print("  quoted differently, under a DATED scope: %d  (a plan or a log, correctly)" % historical)
    print("  quoted differently, MARKED as replaced : %d  (a preserved correction, required)"
          % marked)
    print("  quoted differently, UNMARKED           : %d" % len(hits))

    if confirmations == 0:
        print("\n  CONTROL FAILED: not one index quotes any dimension at its current value, so the")
        print("  extractor is not reading what it claims to. Every count above is meaningless.")
        return 2
    print("\n  control passed: the extractor finds current dimension values quoted in the indexes.")

    if hits:
        print("\nUNMARKED - each is a QUESTION. A figure may be deliberately historical and simply")
        print("not say so; the remedy is then to MARK THE PROSE, never to widen this test.\n")
        for fn, ln, dim, qn, qd, n, d, text in hits:
            print("  %s:%d  %s quoted %s/%s, scorer says %s/%s"
                  % (fn, ln, dim, "{:,}".format(qn), "{:,}".format(qd),
                     "{:,}".format(n), "{:,}".format(d)))
            print("      %s" % text)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
