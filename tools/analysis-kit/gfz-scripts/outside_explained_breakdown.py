#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WHY a function sits outside `engine_explained` -- one row per reason, one bucket per function.

`check_dispositions` answers "is anything declared for this body" (A/B/C/D).
`progress.engine_explained` answers "does an evidence-bearing page cite this body inside it,
or at its entry when the body is under 128 bytes".  ~23.7k bodies fail the second test, and the
planner's question is WHICH kind of failure each one is -- a family already understood that only
lacks a qualifying citation is a different task from a body nothing has ever touched.

Every body in the census lands in EXACTLY ONE bucket, tested in this order:

  EXPLAINED                  in the scorer's set (control row, not a gap)
  DECLARED-UNPROPAGATED      an accepted B/C family claims it; no bearing page cites it
                             inside its body (or at entry under 128 B).  UNDERSTOOD FAMILY,
                             LACKING QUALIFYING CANONICAL PROPAGATION.
  ENTRY-ONLY-LARGE           a BEARING page cites it, but only at its entry, and the body is
                             >=128 B -- a mention that cannot carry a large body.
                             INSUFFICIENT INTERNAL EVIDENCE FOR LARGER FUNCTIONS.
  INTERIOR-NONBEARING        cited inside its body only by pages that are NOT evidence-bearing
                             (PARTIAL / REOPENED / unranked).  PARTIAL OR REOPENED
                             DOCUMENTATION.
  ENTRY-ONLY-NONBEARING      cited only at entry, only by non-bearing pages.
  UNCITED-MECHANICAL         no page cites it at all; name or shape marks it mechanical
                             (thunk_, Unwind@ is excluded upstream, `ret`-sized stubs, Ghidra
                             FUN_ placeholders are the rest -- sized bands reported).
  UNCITED-UNRESOLVED         no page cites it at all and nothing marks it mechanical.
                             GENUINELY UNRESOLVED SEMANTIC BEHAVIOUR.
  GHOST-CITE                 (not a body bucket) backtick addresses inside .text that land in
                             NO census body -- tooling/index lag, reported as a count.

Usage: outside_explained_breakdown.py [--tsv OUT] [--json]
"""

import argparse
import bisect
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_dispositions as cd                       # noqa: E402  one corpus, one loader

MECHANICAL_PREFIX = ("thunk_", "FUN_")
MECHANICAL_BYTES = 16        # a <=16-byte uncited body is a stub/prolog class, not a question


def load_names(path):
    """entry -> census name, for the mechanical-prefix test only."""
    out = {}
    with io.open(path, encoding="utf-8", errors="replace") as f:
        head = f.readline().rstrip("\n").split("\t")
        ia, inm = head.index("entry"), head.index("name")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) <= max(ia, inm):
                continue
            try:
                out[int(p[ia], 16)] = p[inm]
            except ValueError:
                continue
    return out


def measure(db, sizes, paths=None):
    """Return per-body records: entry -> (explained, declared, cites).

    cites: bitfield over the body's citation shape --
      1 = interior cite on a BEARING page        2 = entry cite on a BEARING page
      4 = interior cite on a NON-bearing page    8 = entry cite on a NON-bearing page
    declared: the accepting family name or None (from check_dispositions' own acceptance pass).
    """
    entries = sorted(sizes)
    recs = {e: {"cites": 0, "declared": None} for e in entries}
    ghost = 0

    # --- citation pass ------------------------------------------------------
    for p in (paths if paths is not None else cd.docs(db)):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        bearing = cd._bearing(t)
        for h in cd.CITE.findall(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if not (e <= v < e + sizes[e]):
                if i + 1 < len(entries) and entries[i + 1] <= v:
                    ghost += 1          # inside .text, in no body -- the index, not the cite
                continue
            recs[e]["cites"] |= (1 if v > e else 2) if bearing else (4 if v > e else 8)

    # --- declared-member pass. The gate's OWN verdicts are consulted: a REFUSED family
    # propagates nothing, so its members are their own bucket, not DECLARED-UNPROPAGATED.
    # (Before this, the pass recorded every claim as propagation-pending: SEAD's stale
    # members file was refused by the gate - 24 members already A - yet its 818 members
    # still counted as "declared", hiding them from the unexplained tail.)
    ev = cd.evaluate(db, sizes, paths)
    refused = {who for who, _ in ev["refusals"]}
    for doc, parts in cd.parse_families(db, paths):
        if len(parts) < 5:
            continue
        name, letter, rel = parts[0], parts[1], parts[2]
        if letter not in cd.LETTERS:
            continue
        try:
            members = cd.read_members(doc, rel)
        except (IOError, OSError, ValueError):
            continue
        who = "%s :: %s" % (os.path.basename(doc), name)
        for m in members:
            if m not in recs:
                continue
            if who in refused:
                recs[m].setdefault("declared_refused", who)
            elif recs[m]["declared"] is None:
                recs[m]["declared"] = who
    return recs, ghost


def classify(entry, rec, sizes):
    c = rec["cites"]
    if c & 1 or (c & 2 and sizes[entry] < 128):
        return "EXPLAINED"
    if rec["declared"]:
        return "DECLARED-UNPROPAGATED"
    if rec.get("declared_refused"):
        return "DECLARED-REFUSED"
    if c & 4:
        return "INTERIOR-NONBEARING"
    if c & 2:
        return "ENTRY-ONLY-LARGE"          # bearing page saw it, only named it: >=128 B here
    if c & 8:
        return "ENTRY-ONLY-NONBEARING"
    return "UNCITED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=cd.DEFAULT_DB)
    ap.add_argument("--fn", default=cd.DEFAULT_FN)
    ap.add_argument("--tsv", help="write per-body bucket assignments here")
    args = ap.parse_args()

    sizes = cd.load_functions(args.fn)
    names = load_names(args.fn)
    recs, ghost = measure(args.db, sizes)

    buckets = collections.Counter()
    uncited_mech, uncited_unres = collections.Counter(), collections.Counter()
    declared_fams = collections.Counter()
    for e, rec in recs.items():
        b = classify(e, rec, sizes)
        if b == "UNCITED":
            nm = names.get(e, "")
            b = ("UNCITED-MECHANICAL"
                 if sizes[e] <= MECHANICAL_BYTES or nm.startswith(MECHANICAL_PREFIX)
                 else "UNCITED-UNRESOLVED")
            tgt = uncited_mech if b == "UNCITED-MECHANICAL" else uncited_unres
            tgt["<=32B" if sizes[e] <= 32 else "<=128B" if sizes[e] <= 128
                else "<=512B" if sizes[e] <= 512 else ">512B"] += 1
        buckets[b] += 1
        if b == "DECLARED-UNPROPAGATED":
            declared_fams[rec["declared"]] += 1
        recs[e]["bucket"] = b

    total = len(recs)
    outside = total - buckets["EXPLAINED"]
    print("OUTSIDE-EXPLAINED BREAKDOWN -- %d census bodies, %d explained (%.1f%%)"
          % (total, buckets["EXPLAINED"], 100.0 * buckets["EXPLAINED"] / total))
    print()
    for b in ("DECLARED-UNPROPAGATED", "DECLARED-REFUSED", "ENTRY-ONLY-LARGE",
              "INTERIOR-NONBEARING", "ENTRY-ONLY-NONBEARING", "UNCITED-MECHANICAL",
              "UNCITED-UNRESOLVED"):
        n = buckets.get(b, 0)
        print("  %-24s %6d  (%4.1f%% of the gap)" % (b, n, 100.0 * n / outside if outside else 0))
    print("  %-24s %6d" % ("ghost cites", ghost))
    print()
    print("  uncited-mechanical by size:", dict(uncited_mech))
    print("  uncited-unresolved by size:", dict(uncited_unres))
    print()
    print("  top DECLARED-UNPROPAGATED families:")
    for fam, n in declared_fams.most_common(12):
        print("    %5d  %s" % (n, fam[:78]))

    if args.tsv:
        with io.open(args.tsv, "w", encoding="utf-8", newline="") as f:
            f.write("entry\tbucket\tsize\tdeclared\n")
            for e in sorted(recs):
                f.write("%08X\t%s\t%d\t%s\n" % (e, recs[e]["bucket"], sizes[e],
                                                recs[e]["declared"] or ""))


if __name__ == "__main__":
    main()
