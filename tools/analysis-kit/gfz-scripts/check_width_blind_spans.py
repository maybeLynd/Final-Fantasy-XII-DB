#!/usr/bin/env python3
"""Measure blind spot 12 store-wide: which `unobserved` spans are covered by a WIDER access?

Every `*-accesses.tsv` in this store records a `disp` column and no WIDTH column, and
`receiver_census.py` files each access under the displacement where the access STARTS. An access
that begins before a span and reaches into it is therefore filed under its own offset and is
invisible at the span's - so a span can read "no censused access" while being written every frame
by a wider neighbour.

That was measured on `BattleUnit` at 5 of 30 spans. This asks the same question of every type in
the store that has an access artifact, using the artifact that already exists: the width is
recoverable from the `instruction` column, which records the operand keyword.

WHAT A HIT IS AND IS NOT. A covering access proves the bytes are CARRIED - usually by a block copy
that also spans several declared fields - not that anything reads them for their own sake. So a
hit is a reason to rewrite the row's justification, never a licence to name a field. The report
says COVERED, deliberately, and not `used`.

Widths come from the operand keyword (`qword ptr`, `xmmword ptr`, …) or from the mnemonic for the
SSE moves that carry no keyword. An instruction whose width cannot be read is counted as 1 byte,
which UNDER-reports coverage; the count of those is printed so the figure can be read as a floor.
"""
import collections
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP

STORE = os.environ.get("STORE") or r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA"
KW = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "tbyte": 10, "ymmword": 32}
KWRE = re.compile(r"\b(byte|word|dword|qword|xmmword|tbyte|ymmword) ptr\b")


def width(ins):
    if not ins:
        return None
    m = KWRE.search(ins)
    if m:
        return KW[m.group(1)]
    head = ins.split(None, 1)[0]
    if head in ("movss",): return 4
    if head in ("movsd",): return 8
    if head in ("movaps", "movups", "movdqa", "movdqu", "movapd", "movupd"): return 16
    return None


def load_fields():
    per = collections.defaultdict(list)
    with io.open(os.path.join(STORE, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            try:
                per[f["type"]].append((int(f["offset"], 16), int(f["size"]), f["name"]))
            except (ValueError, KeyError):
                continue
    return per


def guess_type(path, types):
    """Map an artifact filename to a declared type name, or None. Conservative on purpose."""
    stem = os.path.basename(path)
    for suf in ("-accesses.tsv", ".tsv"):
        if stem.endswith(suf):
            stem = stem[:-len(suf)]
    key = stem.replace("-", "").replace("_", "").lower()
    for t in types:
        if t.lower() == key:
            return t
    # the artifacts are named after the type with hex suffixes and qualifiers appended
    best = None
    for t in types:
        tl = t.lower()
        if key.startswith(tl) and (best is None or len(t) > len(best)):
            best = t
    return best


def main():
    per = load_fields()
    types = list(per)
    arts = []
    for root, _dirs, files in os.walk(STORE):
        for fn in files:
            if fn.endswith("-accesses.tsv"):
                arts.append(os.path.join(root, fn))
    arts.sort()

    tot_art = mapped = 0
    tot_spans = tot_cov = 0
    unread = 0
    rows = []
    for a in arts:
        tot_art += 1
        with io.open(a, encoding="utf-8", newline="") as fh:
            recs = list(csv.DictReader(fh, delimiter="\t"))
        if not recs or "disp" not in recs[0]:
            continue
        t = guess_type(a, types)
        if not t:
            continue
        mapped += 1
        acc = []
        for r in recs:
            try:
                d = int(r["disp"], 16)
            except (ValueError, KeyError, TypeError):
                continue
            w = width(r.get("instruction", ""))
            if w is None:
                unread += 1
                w = 1
            acc.append((d, w, r))
        spans = [(o, s, n) for o, s, n in per[t] if n.startswith(("unobservedSpan", "unobservedTail"))]
        tot_spans += len(spans)
        cov = []
        for lo, sz, nm in spans:
            c = [(d, w, r) for d, w, r in acc if d < lo < d + w]
            if c:
                cov.append((nm, lo, sz, c))
        tot_cov += len(cov)
        if cov:
            rows.append((t, os.path.relpath(a, STORE), len(spans), cov))

    print("access artifacts found          : %d" % tot_art)
    print("mapped to a declared type       : %d" % mapped)
    print("unobserved spans on those types : %d" % tot_spans)
    print("COVERED by a wider access       : %d" % tot_cov)
    print("instructions whose width could not be read (counted as 1, so this is a FLOOR): %d\n"
          % unread)
    for t, a, nspan, cov in sorted(rows, key=lambda r: -len(r[3])):
        print("=== %-38s %d of %d span(s) covered   [%s]" % (t, len(cov), nspan, a))
        for nm, lo, sz, c in sorted(cov, key=lambda x: x[1]):
            d, w, r = c[0]
            print("      %-24s +0x%04X..%04X   covered from +0x%04X width %-2d  %s"
                  % (nm, lo, lo + sz, d, w, (r.get("instruction") or "")[:52]))
    print("\nA COVERED SPAN IS NOT A FIELD. The covering access is normally a block copy that also")
    print("spans several declared fields, so it proves the bytes are carried along, not that")
    print("anything reads them for their own sake. Each hit is a row whose REASON is wrong.")


main()
