#!/usr/bin/env python3
"""check_array_heads.py - a field that is really an ARRAY declared as its first element.

THE PATTERN, found three times by hand before this existed. A census records an access at
displacement D and the store declares ONE field there, sized from the access instruction - correctly,
because the rule is that a width comes from the instruction and never from the next offset. But when
that instruction is INDEXED - `byte [base + rcx + D]`, `word [base + rbx*2 + D]` - the field is
element ZERO of an array, and the rest of the array lands beside it as an unexplained span.

`ImageBackedStateBlock` had eight of these in a row between `+0x32C4` and `firedBitmap`;
`PersistentFlagPayload` had five. Both runs were closed by reading the accessor's own bound, and in
four cases the bound matched the distance to the next declared field EXACTLY.

WHAT THIS REPORTS, and what it deliberately does not. A candidate is a small field whose evidence
shows an indexed access and which is immediately followed by an UNKNOWN span. That is a shape, not a
conclusion: the fix is to read the accessor and find its bound, and the span must NOT simply be
folded into the field to make the layout look complete. The report exists to find the candidates,
not to license consuming them.

THE DISCRIMINATOR that makes this usable: the indexed instruction's DISPLACEMENT must equal the
field's own offset. Without it the check matched any indexed instruction quoted anywhere in a row's
evidence - including ones whose index runs over the PARENT's array of records, whose displacement is
a parent-relative offset or an unrelated global. Nine of the first thirteen candidates were exactly
that, and the check said nothing to distinguish them.

`--self-test` checks the operand pattern against an indexed access, a scaled one and a plain
displacement.
"""
import argparse
import csv
import os
import re
import sys

import kit_paths as KP

PHYRE = "22-Middleware-PhyreEngine"

# An indexed memory operand: a second register inside the brackets, with or without a scale.
INDEXED = re.compile(
    r"\[\s*(?:r[a-z0-9]+)\s*\+\s*(?:r[a-z0-9]+)\s*(?:\*\s*([1248])\s*)?\+\s*0x([0-9a-fA-F]+)\s*\]")
SPAN = re.compile(r"^(unobserved|declared)", re.I)


def num(s):
    s = (s or "").strip()
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s, 10)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=os.path.join(KP.DB, "_types"))
    ap.add_argument("--max-element", type=int, default=8,
                    help="a candidate's declared size must be at most this (default 8)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        yes = "003154FD movzx edx, byte ptr [rax + rcx + 0x32cc]"
        scaled = "0046B0DE movzx eax, word ptr [rax + rbx*2 + 0x1164]"
        no = "00254E27 and byte ptr [r9 + 0x32c4], al"
        for label, text, want in (("indexed", yes, True), ("scaled index", scaled, True),
                                  ("plain displacement", no, False)):
            got = bool(INDEXED.search(text))
            ok &= got == want
            print("  control %-20s %s" % (label, "as expected" if got == want else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    with open(os.path.join(a.store, "types.tsv"), encoding="utf-8", newline="") as fh:
        cats = {r["type"]: r["category"] for r in csv.DictReader(fh, delimiter="\t")}
    with open(os.path.join(a.store, "fields.tsv"), encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))

    by = {}
    for r in rows:
        by.setdefault(r["type"], []).append(r)

    found = []
    for t, fs in by.items():
        if cats.get(t) == PHYRE:
            continue
        fs = sorted(fs, key=lambda r: (num(r["offset"]) or 0))
        for i, f in enumerate(fs[:-1]):
            sz = num(f["size"]) or 0
            if sz == 0 or sz > a.max_element:
                continue
            if (f["confidence"] or "").strip().upper() == "UNKNOWN":
                continue
            if SPAN.match((f["name"] or "").strip()):
                continue
            nxt = fs[i + 1]
            if (nxt["confidence"] or "").strip().upper() != "UNKNOWN":
                continue
            if not SPAN.match((nxt["name"] or "").strip()):
                continue
            off, noff = num(f["offset"]), num(nxt["offset"])
            if off is None or noff is None or noff != off + sz:
                continue
            # THE DISCRIMINATOR. Without it this matched any indexed instruction quoted anywhere in
            # the evidence, including ones whose index runs over the PARENT's array of records and
            # whose displacement is a parent-relative offset or an unrelated global. Nine of the
            # first thirteen candidates were that. The instruction has to address THIS field.
            hit = None
            for m in INDEXED.finditer(f["evidence"] or ""):
                if int(m.group(2), 16) == off:
                    hit = m
                    break
            if hit is None:
                continue
            found.append((t, f, nxt, sz + (num(nxt["size"]) or 0), hit.group(0)))

    print("candidates - a small field with an INDEXED access, immediately followed by an "
          "UNKNOWN span")
    print("(a shape, not a conclusion: read the accessor's bound, and do not fold the span in "
          "to tidy the layout)")
    print()
    if not found:
        print("none")
        return 0
    bytype = {}
    for t, f, nxt, total, insn in found:
        bytype.setdefault(t, []).append((f, nxt, total, insn))
    for t in sorted(bytype, key=lambda k: -sum(x[2] for x in bytype[k])):
        rs = bytype[t]
        print("%s  - %d candidate(s), %d byte(s) if each is one array" %
              (t, len(rs), sum(x[2] for x in rs)))
        for f, nxt, total, insn in sorted(rs, key=lambda x: num(x[0]["offset"]) or 0):
            print("   +%-8s %-28s %sB declared, %sB span after it -> %d" %
                  (f["offset"], f["name"], f["size"], nxt["size"], total))
            print("        %s" % insn)
    print()
    print("total: %d candidate(s) across %d type(s), %d byte(s)"
          % (len(found), len(bytype), sum(x[3] for x in found)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
