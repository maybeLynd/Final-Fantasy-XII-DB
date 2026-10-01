#!/usr/bin/env python3
"""check_span_propagation.py - does a span's OWNING PAGE already know something the store does not?

THE GAP IS MEASURED, NOT SUPPOSED. `SavePayload`'s three largest spans - 11,940 bytes - carried
nothing in `fields.tsv` but *"extent-declared gap ... width = declared span, not an instruction
access"*. Meanwhile the type's own `documents` page,
`19-Save-Load-Settings/.../the-save-payload-field-map.md`, had a whole section proving all three
sit inside a `0x56690` memset, giving them a defined value and a lifetime. The finding existed; it
had simply never reached the store.

That is a propagation gap, and nothing was looking for it. Every other checker in this kit compares
the store against the image or against itself. This one compares the store against **the prose the
store itself points at**.

METHOD, deliberately narrow so the output is readable.

  * Take every field row whose name marks it a declared span (`unobserved*`, `unread*`).
  * Take the owning type's `documents` column - the pages the store itself nominates.
  * Search those pages for the span's offset, written the several ways this corpus writes an
    offset: `0x1538`, `+0x1538`, `0x01538`, and the same in lower case.
  * Report a hit ONLY when the span's own evidence cell does not already cite that page.

WHY THIS IS A CANDIDATE LIST AND NOT A DEFECT LIST. An offset is a short string and a page is long
prose: `0x20` occurs in most documents for unrelated reasons. So short offsets are the noisy case
and are reported separately, and **every hit needs a human to open the page**. The tool's claim is
only ever "this page mentions this offset and the store's row does not mention this page", which is
exactly the shape of the SavePayload miss.

    python check_span_propagation.py
    python check_span_propagation.py --min-width 3    # only distinctive offsets
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP

SPAN = re.compile(r"^(unobserved|unread|declaredGap|gap)", re.I)


def offset_forms(off):
    """The several spellings this corpus uses for one offset."""
    n = int(off, 16)
    out = set()
    for w in (0, 2, 3, 4, 5):
        h = ("%0*X" % (w, n)) if w else ("%X" % n)
        out.add("0x" + h)
        out.add("0x" + h.lower())
        out.add("+0x" + h)
        out.add("+0x" + h.lower())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--min-width", type=int, default=3,
                    help="skip offsets with fewer than this many hex digits; short ones match "
                         "unrelated prose constantly")
    a = ap.parse_args()

    docs_of, size_of = {}, {}
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0] and len(f) > 11:
                docs_of[f[0]] = [d.strip() for d in f[11].split(";") if d.strip()]

    spans = []
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and SPAN.match(f[3]):
                spans.append(f)
    print("declared spans: %d over %d type(s)"
          % (len(spans), len({s[0] for s in spans})))

    cache = {}

    def page(p):
        if p not in cache:
            fp = os.path.join(a.db, p)
            try:
                cache[p] = io.open(fp, encoding="utf-8", errors="replace").read()
            except OSError:
                cache[p] = None
        return cache[p]

    hits, nodoc, short = [], collections.Counter(), 0
    for f in spans:
        t, off, size, name, ev = f[0], f[1], int(f[2]), f[3], f[8]
        docs = docs_of.get(t) or []
        if not docs:
            nodoc[t] += 1
            continue
        h = off[2:].lstrip("0") or "0"
        if len(h) < a.min_width:
            short += 1
            continue
        forms = offset_forms(off)
        for p in docs:
            txt = page(p)
            if txt is None:
                continue
            if any(x in txt for x in forms):
                base = os.path.basename(p)
                if base in ev or p in ev:
                    continue                      # the row already cites this page
                hits.append((t, off, size, name, p))

    print("spans skipped, offset too short to search safely (<%d hex digits): %d"
          % (a.min_width, short))
    print("spans whose type nominates no document: %d over %d type(s)"
          % (sum(nodoc.values()), len(nodoc)))
    print()
    print("CANDIDATES - the type's own page mentions the offset and the row does not cite it: %d"
          % len(hits))
    hits.sort(key=lambda x: -x[2])
    by_type = collections.Counter(x[0] for x in hits)
    for t, off, size, name, p in hits[:40]:
        print("  %-28s %-9s %7d B  %-24s -> %s" % (t, off, size, name, os.path.basename(p)))
    if len(hits) > 40:
        print("  ... %d more" % (len(hits) - 40))
    print()
    print("bytes under candidate spans: %d" % sum(x[2] for x in hits))
    print("types with the most: %s" % ", ".join("%s %d" % kv for kv in by_type.most_common(6)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
