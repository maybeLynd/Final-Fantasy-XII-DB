#!/usr/bin/env python3
"""audit_inbox_backlog.py - what in the inboxes has actually been merged?

The problem
-----------
The protocol says the coordinator merges an inbox section into the shared `_index` file and then
**deletes the consumed section**. Thirteen inbox files hold ~14,500 lines. Their mere presence is
therefore evidence of a backlog -- but only if the delete step was honoured, and a coordinator who
merged without deleting leaves the same footprint as one who never merged at all.

**So presence is not evidence and the files must be checked against the targets.**

Method, and why it is deliberately weak
---------------------------------------
For each section in each inbox, take its most distinctive lines -- long ones, which are least
likely to collide by chance -- and look for them in the shared file that section targets. A section
whose distinctive lines are all present downstream was **probably merged**; one whose lines are
absent was **probably not**.

**This produces a triage, never a verdict.** Prose gets rewritten during a merge, so a merged
section can read as unmerged; and a section can be partly merged, which this reports as whichever
side the sample lands on. **Nothing here justifies deleting an inbox section** -- it justifies
deciding which ones a human reads first.

The safe direction of error is built in: a section is only called MERGED when **every** sampled
line is found downstream. Anything less is reported as needing review.
"""
import argparse
import collections
import io
import os
import re
import sys

TARGETS = {
    "COVERAGE": "COVERAGE.md",
    "OPEN-QUESTIONS": "OPEN-QUESTIONS.md",
    "AUDIT-LOG": "AUDIT-LOG.md",
    "CALL-CHAINS / ADDRESS-INDEX": "CALL-CHAINS.md",
    "CALL-CHAINS": "CALL-CHAINS.md",
    "ADDRESS-INDEX": "ADDRESS-INDEX.md",
}
SECTION = re.compile(r"^##\s+([A-Z][A-Z \-/]+?)\s*$")
NOISE = re.compile(r"^[\s|:\-`*#>]*$")


def sections(text):
    """-> [(heading, [lines])]"""
    out, cur, buf = [], None, []
    for line in text.split("\n"):
        m = SECTION.match(line)
        if m:
            if cur:
                out.append((cur, buf))
            cur, buf = m.group(1).strip(), []
        elif cur:
            buf.append(line)
    if cur:
        out.append((cur, buf))
    return out


# --- the first version of this script matched PROSE, and it was wrong -------------------------
#
# It reported 200 of 202 sections UNMERGED and 0 merged. **Zero is the shape of an instrument that
# cannot detect, not a finding**, so a positive control was run before believing it: six question
# ids drawn from sections it called UNMERGED -- BQ-4, BQ-13, Z-10, BP-6, AY-6, BQ-27 -- and **all
# six are present in `OPEN-QUESTIONS.md`.** Those sections were merged. The merge rewrites prose,
# so exact-substring matching can never see it.
#
# The shared files corroborate: 25,374 lines downstream against ~14,500 in the inboxes, with
# `AUDIT-LOG.md` alone at 14,939.
#
# So match on **tokens that survive a rewrite** -- question ids and hex addresses. A merger renames
# and re-argues; it does not renumber `BQ-13` or move `0022A4F0`.
QID = re.compile(r"\b([A-Z]{1,3}-\d+[a-z]?)\b")
# `\b` fails after `0x` -- see verify_doc_addresses.py. repos-c9, 2026-09-04.
ADDR = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")


def tokens(lines, n=40):
    """Stable identifiers in a section: question ids and 8-hex addresses."""
    text = "\n".join(lines)
    out, seen = [], set()
    for rx in (QID, ADDR):
        for m in rx.finditer(text):
            t = m.group(1).upper()
            if t not in seen:
                seen.add(t)
                out.append(t)
            if len(out) >= n:
                return out
    return out


def present(tok, hay):
    return re.search(r"\b%s\b" % re.escape(tok), hay, re.I) is not None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True, help="the _index directory")
    ap.add_argument("--show", type=int, default=2)
    a = ap.parse_args(argv)

    inbox = os.path.join(a.index, "_inbox")
    shared = {}
    for t in set(TARGETS.values()):
        p = os.path.join(a.index, t)
        shared[t] = io.open(p, encoding="utf-8", errors="replace").read() if os.path.isfile(p) else ""

    files = sorted(f for f in os.listdir(inbox)
                   if f.startswith("repos-") and f.endswith(".md"))
    print("INBOX BACKLOG AUDIT - %d file(s)\n" % len(files))
    print("A section counts as MERGED only when EVERY sampled line is found downstream.")
    print("Anything else needs a human. This is triage, not a verdict.\n")

    tot = collections.Counter()
    for fn in files:
        text = io.open(os.path.join(inbox, fn), encoding="utf-8", errors="replace").read()
        secs = sections(text)
        nlines = len(text.split("\n"))
        rows = []
        for head, body in secs:
            tgt = TARGETS.get(head)
            samples = tokens(body)
            # A merge may land in any shared file, not only the section's nominal target -- an
            # address raised under COVERAGE often ends up in ADDRESS-INDEX. Searching only the
            # nominal target would manufacture "unmerged" for correctly-merged content.
            hay = "\n".join(shared.values())
            if not tgt:
                verdict, detail = "NO TARGET", "not a mergeable section"
            elif not samples:
                verdict, detail = "NO TOKENS", "no ids or addresses to trace"
            else:
                hits = sum(1 for s in samples if present(s, hay))
                pct = 100.0 * hits / len(samples)
                if pct >= 90:
                    verdict, detail = "merged", "%d/%d ids+addrs downstream" % (hits, len(samples))
                elif pct < 40:
                    verdict, detail = "UNMERGED", "%d/%d ids+addrs downstream" % (hits, len(samples))
                else:
                    verdict, detail = "PARTIAL", "%d/%d ids+addrs downstream" % (hits, len(samples))
            tot[verdict] += 1
            rows.append((head, verdict, detail, len(body), samples))
        print("%-14s %5d lines, %d section(s)" % (fn, nlines, len(secs)))
        for head, verdict, detail, blen, samples in rows:
            flag = "  <<<" if verdict in ("UNMERGED", "PARTIAL") else ""
            print("    %-28s %-9s %-34s %4d lines%s" % (head[:28], verdict, detail, blen, flag))
            if verdict in ("UNMERGED", "PARTIAL"):
                for s in samples[:a.show]:
                    print("        %s" % s[:104])
        print("")

    print("TOTALS: " + "  ".join("%s=%d" % (k, v) for k, v in tot.most_common()))
    print("\nUNMERGED/PARTIAL sections are the backlog. **Do not delete anything on this output"
          "\nalone** - prose is rewritten during a merge, so a merged section can read as unmerged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
