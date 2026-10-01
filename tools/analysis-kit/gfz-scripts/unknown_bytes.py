#!/usr/bin/env python3
"""unknown_bytes.py - how much of each game-side type is actually unexplained?

The type store's UNKNOWN population is usually quoted as a ROW COUNT, and rows are a bad unit for
it. An undeclared span is one row whether it is 3 bytes or 3,916, so counting rows makes a type
with many small holes look worse than a type that is one enormous hole.

Measured by BYTES the order changes, and it changes the answer to "which record should be worked
next". Both numbers are printed so neither can be quoted without the other.

This measures the store, not the engine: `declared` is the bytes the store has field rows for, and
a type whose size is UNRESOLVED has no denominator and is reported without a share.

NESTING, and why the totals used to be wrong (fixed 2026-09-18, OPUS). An `EMBED`-routed type lives
INSIDE another declared type, so its bytes are counted twice if both are summed: once in the parent's
span and again as the child's own rows. That was tolerable while fifteen types were embedded; it
stopped being tolerable the moment seven more were declared in one package and the store-wide
denominator jumped 43,456 bytes without a single byte being explained.

**A metric that grows its own denominator whenever somebody declares a nested type rewards
restructuring and punishes nothing.** So the headline totals now count each byte ONCE, at the
outermost type that declares it, and the amount excluded is printed rather than hidden. Per-type rows
still list children - a child's own share is the right number when choosing what to work next - and
they are marked so nobody adds the column up.
"""
import argparse
import collections
import csv
import os
import re
import sys

import kit_paths as KP

PHYRE = "22-Middleware-PhyreEngine"
EMBED = re.compile(r"\bEMBED\s+(\S+)\s+\+0x", re.I)


def children_of(types, keep):
    """Types whose bytes are already counted inside a measured parent."""
    kids = {}
    for t in types:
        if t["type"] not in keep:
            continue
        for alt in (t.get("route") or "").split("|"):
            m = EMBED.match(alt.strip())
            if m and m.group(1) in keep and m.group(1) != t["type"]:
                kids[t["type"]] = m.group(1)
                break
    return kids


def self_test():
    """A parent of 0x100 containing a 0x40 child must total 0x100, not 0x140."""
    types = [{"type": "Parent", "category": "x", "route": "STATIC 0x1000"},
             {"type": "Child", "category": "x", "route": "EMBED Parent +0x20"},
             {"type": "Loner", "category": "x", "route": "PTR 0x2000"}]
    keep = {t["type"] for t in types}
    kids = children_of(types, keep)
    ok = (kids == {"Child": "Parent"})
    print("  the EMBED child is recognised                %s" % ("yes" if ok else "BROKEN"))
    top = sorted(t for t in keep if t not in kids)
    ok2 = (top == ["Loner", "Parent"])
    print("  the parent and an unrelated type stay top    %s" % ("yes" if ok2 else "BROKEN"))
    # a route that EMBEDs into something NOT measured must not be treated as a child
    types2 = [{"type": "Orphan", "category": "x", "route": "EMBED NotDeclared +0x10"}]
    ok3 = (children_of(types2, {"Orphan"}) == {})
    print("  EMBED into an unmeasured parent is not a kid %s" % ("yes" if ok3 else "BROKEN"))
    # and the arithmetic the nesting exists for
    b = {"Parent": 0x100, "Child": 0x40, "Loner": 0x10}
    u = {"Parent": 0x08, "Child": 0x30, "Loner": 0x00}
    tb = sum(b[t] for t in top)
    tu = sum(u[t] for t in top) + sum(u[t] for t in kids)
    ok4 = (tb == 0x110 and tu == 0x38)
    print("  span counted once, child UNKNOWN still counted   %s"
          % ("yes" if ok4 else "BROKEN (%X, %X)" % (tb, tu)))
    good = ok and ok2 and ok3 and ok4
    print("  %s" % ("all controls behave" if good else "AT LEAST ONE CONTROL IS BROKEN"))
    return 0 if good else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=os.path.join(KP.DB, "_types"))
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--phyre", action="store_true", help="include the Phyre reflection samples")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    with open(os.path.join(a.store, "types.tsv"), encoding="utf-8", newline="") as fh:
        types = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(a.store, "fields.tsv"), encoding="utf-8", newline="") as fh:
        fields = list(csv.DictReader(fh, delimiter="\t"))

    keep = {t["type"] for t in types if a.phyre or t["category"] != PHYRE}
    cat = {t["type"]: t["category"] for t in types}

    rows = collections.Counter()
    unk_rows = collections.Counter()
    bytes_all = collections.Counter()
    unk_bytes = collections.Counter()
    for f in fields:
        t = f["type"]
        if t not in keep:
            continue
        try:
            b = int(f["size"])
        except (TypeError, ValueError):
            b = 0
        rows[t] += 1
        bytes_all[t] += b
        if (f["confidence"] or "").strip().upper() == "UNKNOWN":
            unk_rows[t] += 1
            unk_bytes[t] += b

    kids = children_of(types, keep)
    top = [t for t in keep if t not in kids]
    tot_b = sum(bytes_all[t] for t in top)
    # A CHILD'S UNKNOWN BYTES ARE STILL UNKNOWN. The parent's row for an embedded type is a
    # declaration that something lives there, not a description of it - it is `TYPE RESOLVED` and so
    # contributes nothing to the UNKNOWN count, while the child it names can be 99 % holes. Counting
    # only the top level therefore reported those bytes as explained: before the array pass of
    # 2026-09-18, ManagerSub0209BE80_00A0 alone hid 21,182 unknown bytes behind one `HIGH` row, which
    # is four per cent of the whole store's denominator. So each byte is counted once at its MOST
    # SPECIFIC description: the parent supplies the denominator, the child supplies the verdict.
    #
    # ASSUMPTION, stated because it is not checked: a parent's covering row for an embedded child is
    # not itself UNKNOWN. If it were, that span would be counted unknown twice. Every EMBED row this
    # store writes for a declared child is TYPE RESOLVED or better.
    tot_u = sum(unk_bytes[t] for t in top) + sum(unk_bytes[t] for t in kids)
    dbl_b = sum(bytes_all[t] for t in kids)
    dbl_u = sum(unk_bytes[t] for t in kids)
    print("types measured           : %d, of which %d are EMBED children counted inside a parent"
          % (len(keep), len(kids)))
    print("field rows               : %d, of which UNKNOWN %d (%.1f %%)"
          % (sum(rows.values()), sum(unk_rows.values()),
             100.0 * sum(unk_rows.values()) / max(sum(rows.values()), 1)))
    print("declared bytes           : %d, of which UNKNOWN %d (%.1f %%)"
          % (tot_b, tot_u, 100.0 * tot_u / max(tot_b, 1)))
    print("  %d byte(s) live in EMBED children. Their SPAN is counted once, in the parent;"
          % dbl_b)
    print("  their %d UNKNOWN byte(s) ARE counted above, because a parent's EMBED row declares that"
          % dbl_u)
    print("  something is there and says nothing about what - the child holds the verdict.")
    print()
    print("THE TWO ORDERS DISAGREE, which is the point of printing both.")
    print()
    print("%-32s %5s %9s %9s %8s  %s" % ("type", "rows", "unkRows", "unkBytes", "declared", "share"))
    for t, b in unk_bytes.most_common(a.top):
        share = 100.0 * b / max(bytes_all[t], 1)
        print("%-32s %5d %9d %9d %8d  %5.1f %%%s"
              % (t, rows[t], unk_rows[t], b, bytes_all[t], share,
                 ("   in " + kids[t]) if t in kids else ""))
    print()
    print("A row marked `in <parent>` is an EMBED child: its bytes are inside that parent's span,")
    print("so this column does not add up to the total above, and is not meant to.")
    print()
    print("by ROW count instead, the first %d are:" % min(a.top, 10))
    for t, n in unk_rows.most_common(min(a.top, 10)):
        print("   %-32s %3d row(s), %6d byte(s), %5.1f %% of the type"
              % (t, n, unk_bytes[t], 100.0 * unk_bytes[t] / max(bytes_all[t], 1)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
