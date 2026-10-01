#!/usr/bin/env python3
"""check_uncompared_pairs.py - two functions that touch the same thing and have never been compared.

Why this exists
---------------
Two rankings already exist and **both score a single function**: bytes-per-line asks *how little did
we say about this one*, SSE density asks *what shape is this one*.

> **Almost every finding on 2026-09-03 came from reading a body, and almost every correction came
> from comparing two bodies.**

Neither existing list can see a pair, and the pairs are where the corrections came from:

  * one field read as a *remaining budget* in one function and a *fade factor* in another -- **both
    right; the field had two roles, and each reader had seen one site**;
  * two renderers over one record, one **masking** the fourth colour byte away and one **reading it
    into its own slot** -- the first could only say a byte was dropped;
  * two null conventions on one ranking -- one loading defaults **before** the test, the other
    dereferencing zero;
  * an ellipse clamp and a box clamp over one volume record.

**Every one of those was found by accident or by someone reading two things in a row.** This makes it
a query.

The signal
----------
**A global referenced by two or more functions, where no single document cites both.** Those functions
have never been compared *in writing*, whatever else is known about them.

**Fan-in is capped**, because a global touched by fifty functions is a hub and any two of them share
it trivially. The interesting case is a handful of touchers -- few enough that the shared address
means something, in documents that do not mention each other.

What it is NOT
--------------
**Not a defect list.** Two functions may share a global for no interesting reason at all, and this
tool cannot tell. It reports *unexamined adjacency*, which is a place to look, and its own false
positives are the same two the other lists have: a function read but cited only at its entry looks
uncompared, and a vendor function is not ours to compare.

**And its SITE COUNTS ARE LOWER BOUNDS, badly so for struct fields.** Measured against the census
file on 2026-09-03, inside one row (`+0x2348`, `001E8070` / `001E8580`):

    field                  census rows      sites the read found
    +0x2324                     1                    2
    +0x233C                     0                    2
    +0x2348                     2                    3
    +0x2340 / +0x2344           3 (writes only)      5

Two encodings hide sites, and **the second is the one to remember**:

**A base pointer.** `lea r12, [r14 + 0x2348]`, then every access reads `[r12 - 0x24]`. `001E8580`
contributes three rows for that whole record -- both from above the `lea`.

**An offset folded into an index constant.** `add rax, 0xcd; imul rax, rax, 0x2c` puts `0x233C` into
the INDEX, so the store carries no displacement. **`+0x233C` has zero rows in a census of 21,999** --
not undercounted, absent.

Two consequences: a row saying *two sites* may be a field with twenty, so **`fan-in` is not a measure
of how busy a field is**; and **"no writer found" is never a finding** -- a writer holding the record
pointer stores to `[reg + 0x25]` and is invisible by construction.

The one thing the undercount does NOT do is create false rows: every site it *does* report is real,
so a pair it surfaces is a genuine pair. It loses rows, it does not invent them.

**It does, however, inflate its own ROW count.** A contiguous structure yields one row per stride
with an identical toucher set: on 2026-09-03, five of the thirteen remaining rows (`+0xE30`,
`+0xE38`, `+0xE40`, `+0xE48`, `+0xE50`, six touchers each) were **one 4x4 float matrix**, read
sixteen floats at a time by `001E8580`. **38 % of the frontier was one structure.**

**Two improvements, recorded and not built:** collapse rows with an identical toucher set at adjacent
displacements, and carry the ACCESS WIDTH so a disagreement is visible before anyone opens a body --
`001CCB20` writes a *byte* at `+0xE30` where `001E8580` reads a *float*, which settles that they are
not the same object without a read.

**A note on which instrument said what.** The first published version of the table above was measured
with a raw instruction search and reported as if it were this census. The census is much the better
of the two -- 17 rows on that record against 4. **Measuring instrument A and reporting instrument B
is a mis-binding**, and the numbers here are now taken from the file this tool actually reads.

Usage
-----
    python check_uncompared_pairs.py --db "Database/FFXII TZA" --refs Tools/work/h78/data_refs.tsv
    python check_uncompared_pairs.py --self-test
"""
import argparse
import collections
import io
import itertools
import os
import sys

import check_located_not_read as C


def load_refs(path):
    """-> {target_address: {function_entry, ...}}  from `entry <TAB> target [<TAB> kind]`."""
    out = collections.defaultdict(set)
    f = io.open(path, encoding="utf-8", errors="replace")
    first = f.readline()
    if first and not first[:1].isdigit() and not first[:1].isalpha():
        pass
    else:
        _maybe_row(first, out)
    for line in f:
        _maybe_row(line, out)
    return out


def _maybe_row(line, out):
    p = line.rstrip("\n").split("\t")
    if len(p) < 2:
        return
    try:
        fn = int(p[0], 16)
        tgt = int(p[1], 16)
    except ValueError:
        return                                  # the header row lands here and is skipped
    out[tgt].add(fn)


def docs_citing(db):
    """-> {function_entry: {document, ...}}, excluding `_index/` and index-sized documents."""
    entries, sizes, names, vendor = C.load(C.FUNCS)
    texts = []
    for root, _d, files in os.walk(db):
        if "_inbox" in root.split(os.sep):
            continue
        for fn in sorted(files):
            if fn.endswith(".md"):
                p = os.path.join(root, fn)
                texts.append((os.path.relpath(p, db).replace(os.sep, "/"),
                              io.open(p, encoding="utf-8", errors="replace").read()))
    idx = {rel for rel, t in texts
           if rel.startswith("_index/") or len(C.cited_addresses(t)) > 300}
    seen = C.classify([(r, t) for r, t in texts if r not in idx], entries, sizes)
    return {e: v[2] for e, v in seen.items()}, names, vendor


def rank(refs, cited, names, vendor, min_touch, max_touch):
    rows = []
    for tgt, fns in refs.items():
        fns = {f for f in fns if not vendor.get(f)}
        if not (min_touch <= len(fns) <= max_touch):
            continue
        known = {f: cited.get(f, set()) for f in fns}
        # Only interesting when the functions ARE documented -- otherwise it is an unread gap,
        # which the other two lists already cover.  **This list is about comparison, not coverage.**
        if sum(1 for f in fns if known[f]) < 2:
            continue
        shared = any(known[a] & known[b] for a, b in itertools.combinations(fns, 2))
        if shared:
            continue                            # some document already mentions two of them
        rows.append((tgt, sorted(fns), known))
    # **Rank by how many touchers are DOCUMENTED, not by fan-in.** A row where five of six functions
    # have no document is a coverage gap and the other two lists already own it; a row where four of
    # five are documented and no document mentions two of them is a genuine *comparison* gap -- the
    # thing this list exists for.  Fan-in breaks ties in the tight direction: fewer touchers means
    # the shared address is more likely to mean something.
    rows.sort(key=lambda r: (-sum(1 for f in r[1] if r[2][f]), len(r[1]), r[0]))
    return rows


SELF_REFS = {0x2000: {0x1000, 0x1100}, 0x3000: {0x1000, 0x1200}, 0x4000: {0x1000}}
SELF_CITED = {0x1000: {"a.md"}, 0x1100: {"b.md"}, 0x1200: {"a.md"}}


def self_test():
    rows = rank(SELF_REFS, SELF_CITED, {}, {}, 2, 8)
    got = {r[0] for r in rows}
    if got != {0x2000}:
        print("SELF-TEST FAILED: got %r, want {0x2000}" % [hex(x) for x in got])
        return 1
    print("self-test ok: reports the pair in two documents, skips the pair sharing a document "
          "and the single-toucher address")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--refs")
    ap.add_argument("--min-touchers", type=int, default=2)
    ap.add_argument("--max-touchers", type=int, default=6)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.db or not a.refs:
        return ap.error("--db and --refs required unless --self-test")
    if not os.path.exists(a.refs):
        print("SCANNED NOTHING: no reference census at %r" % a.refs)
        print("A clean result over an empty population is not a clean result.")
        return 2

    refs = load_refs(a.refs)
    cited, names, vendor = docs_citing(a.db)
    rows = rank(refs, cited, names, vendor, a.min_touchers, a.max_touchers)

    print("TOUCHING THE SAME THING, NEVER COMPARED")
    print("A global reached by %d-%d functions, where NO single document cites two of them."
          % (a.min_touchers, a.max_touchers))
    print("**Unexamined adjacency, not a defect.** Two functions may share a global for no")
    print("interesting reason; this says only that nobody has written them down together.\n")
    print("  %d address(es) from a census of %d\n" % (len(rows), len(refs)))
    for tgt, fns, known in rows[:a.top]:
        print("  %08X  touched by %d" % (tgt, len(fns)))
        for f in fns:
            d = sorted(known[f])
            print("      %08X  %-44s %s"
                  % (f, names.get(f, "")[:44],
                     ", ".join(os.path.basename(x) for x in d) if d else "(no document)"))
        print()
    if len(rows) > a.top:
        print("  ... %d more" % (len(rows) - a.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
