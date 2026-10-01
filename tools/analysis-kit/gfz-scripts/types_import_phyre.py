#!/usr/bin/env python3
"""types_import_phyre.py - move the recovered Phyre member schema into the canonical type store.

The gap
-------
`22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv` holds member
records recovered from the engine's own reflection registration calls - member name, byte offset,
C type - over 179 classes. The canonical type store, `_types/`, holds **2 types**. The knowledge
exists and is not where a query looks for it.

Why sizes are NOT derived from offset deltas
--------------------------------------------
The obvious derivation is `size[i] = offset[i+1] - offset[i]`. **It is unsound here, and this tool
measures why rather than assuming either way.**

Take only members whose C type is a genuine primitive, so the true size is known independently, and
compare it with the delta to the next recovered member:

    delta == the primitive's size : 202   (64.7 %)
    delta >  the primitive's size : 110   (35.3 %)

**A third of the time an unrecovered member sits in the gap.** The reflection table is a *sample* of
each class's members, not a layout, so a delta measures "distance to the next member anybody
recovered", which is not a size. Averaging or modal-voting the deltas would have produced
confident wrong sizes for exactly the engine types that have no other evidence.

So: **size comes from the C primitive table or it stays UNRESOLVED.** Nothing here is guessed.

What the import therefore claims
--------------------------------
`SIGNATURE RESOLVED`, not `TYPE RESOLVED`: the member names and offsets are known, the layout is
not complete, and each imported type carries its own measured completeness in its evidence column so
no later reader mistakes a sample for a struct.
"""
import argparse
import collections
import io
import os
import sys
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
SRC = os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                   "phyre-field-schema.tsv")

# Genuine C primitives only. An engine type's size has no evidence here and stays unresolved.
PRIMITIVE = {
    "bool": 1, "char": 1, "signed char": 1, "unsigned char": 1,
    "short": 2, "unsigned short": 2,
    "int": 4, "unsigned int": 4, "long": 4, "unsigned long": 4, "float": 4,
    "__int64": 8, "unsigned __int64": 8, "double": 8,
}


def load(path):
    lines = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
    head = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        if line.strip():
            rows.append(dict(zip(head, line.split("\t") + [""] * len(head))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--store", default=os.path.join(DB, "_types"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    rows = load(a.src)
    seen = {}
    dup = 0
    for r in rows:
        try:
            off = int(r["offset"], 16)
        except ValueError:
            continue
        key = (r["class_leaf"], r["member"], off)
        if key in seen:
            dup += 1
            continue
        seen[key] = r
    by = collections.defaultdict(list)
    for (cls, member, off), r in seen.items():
        by[cls].append((off, member, r["type"], r))
    for cls in by:
        by[cls].sort()

    # LEAF-NAME COLLISIONS. The grouping key is the leaf class name, which is what a reader wants
    # to see - but a template container has one leaf name and many instantiations, and grouping
    # them merges genuinely distinct types into one row. Measured here rather than assumed:
    # `PArray` has 60 full names behind it and `PSharray` 9. Their members happen to have the same
    # offsets in every instantiation, so the merge produced no overlap and the validator saw
    # nothing wrong - **a silent merge that passes validation is exactly the kind that survives.**
    # These are flagged, weakened to CLASSIFIED, and say so in their own evidence column.
    full_names = collections.defaultdict(set)
    for r in rows:
        if r.get("class_leaf") and r.get("class"):
            full_names[r["class_leaf"]].add(r["class"])
    merged = {c: len(v) for c, v in full_names.items() if len(v) > 1}

    # --- the delta soundness test, reported every run ----------------------------------------
    eq = ne = 0
    for cls, items in by.items():
        for i in range(len(items) - 1):
            off, _, ctype, _ = items[i]
            if ctype in PRIMITIVE:
                d = items[i + 1][0] - off
                if d == PRIMITIVE[ctype]:
                    eq += 1
                elif d > PRIMITIVE[ctype]:
                    ne += 1
    tested = eq + ne

    known = sum(1 for items in by.values() for _, _, t, _ in items if t in PRIMITIVE)
    total = sum(len(v) for v in by.values())

    span_tot = known_tot = 0
    complete = 0
    for cls, items in by.items():
        last_off, _, last_t, _ = items[-1]
        span = last_off + PRIMITIVE.get(last_t, 0)
        if span <= 0:
            continue
        acc = sum(PRIMITIVE[t] for _, _, t, _ in items if t in PRIMITIVE)
        span_tot += span
        known_tot += acc
        if acc >= span:
            complete += 1

    print("source rows                          : %d" % len(rows))
    print("  duplicate (class, member, offset)  : %d collapsed" % dup)
    print("  distinct members                   : %d over %d classes" % (total, len(by)))
    print()
    print("DELTA SOUNDNESS TEST  (primitive members that have a next recovered member)")
    print("  tested                             : %d" % tested)
    if tested:
        print("  delta == the primitive's size      : %d  (%.1f %%)" % (eq, 100.0 * eq / tested))
        print("  delta >  the primitive's size      : %d  (%.1f %%)  <- a member is MISSING between"
              % (ne, 100.0 * ne / tested))
    print("  VERDICT: the schema is a SAMPLE of each class's members, not a layout.")
    print("           Sizes are taken from C primitives only; everything else stays UNRESOLVED.")
    print()
    print("SIZE COVERAGE")
    print("  members with a known size          : %d of %d (%.1f %%)"
          % (known, total, 100.0 * known / total))
    print("  bytes accounted for, all classes   : %d of %d (%.1f %%)"
          % (known_tot, span_tot, 100.0 * known_tot / span_tot if span_tot else 0.0))
    print("  classes whose recovered members fill their own span : %d of %d"
          % (complete, len(by)))
    print()
    print("LEAF-NAME COLLISIONS  (one leaf name, several full class names)")
    print("  leaf names that merge more than one class : %d of %d" % (len(merged), len(by)))
    for c, n in sorted(merged.items(), key=lambda kv: -kv[1]):
        print("     %-22s %d instantiations merged - imported as CLASSIFIED, not a struct"
              % (c, n))

    if not a.write:
        print("\n(dry run - pass --write to update the store)")
        return 0

    tp = os.path.join(a.store, "types.tsv")
    fp = os.path.join(a.store, "fields.tsv")
    existing = set(l.split("\t")[0] for l in
                   io.open(tp, encoding="utf-8").read().splitlines()[1:] if l.strip())

    at = af = 0
    with io.open(tp, "a", encoding="utf-8", newline="\n") as ft, \
            io.open(fp, "a", encoding="utf-8", newline="\n") as ff:
        for cls, items in sorted(by.items()):
            if cls in existing:
                continue
            last_off, _, last_t, _ = items[-1]
            span = last_off + PRIMITIVE.get(last_t, 0)
            acc = sum(PRIMITIVE[t] for _, _, t, _ in items if t in PRIMITIVE)
            pct = (100.0 * acc / span) if span else 0.0
            note = ("Phyre reflection registrations: %d member(s) recovered, %d of %d bytes to "
                    "the last member accounted for (%.0f %%). A SAMPLE, not a complete layout - "
                    "see types_import_phyre.py for the delta soundness test."
                    % (len(items), acc, span, pct))
            if cls in merged:
                note = ("MERGED LEAF NAME: %d distinct full class names share it (template "
                        "instantiations), so these members are the UNION across all of them and "
                        "this row is NOT one struct. " % merged[cls]) + note
            ft.write("\t".join([
                cls, "UNRESOLVED", "22-Middleware-PhyreEngine", "", "", "", "",
                "CLASSIFIED" if cls in merged else "SIGNATURE RESOLVED", "HIGH", "L1",
                note,
                "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/"
                "member-registration-and-the-recovered-field-schema.md"]) + "\n")
            at += 1
            for off, member, ctype, r in items:
                sz = PRIMITIVE.get(ctype)
                ff.write("\t".join([
                    cls, "0x%03X" % off, str(sz) if sz else "0", member, ctype, "",
                    "TYPE RESOLVED" if sz else "SIGNATURE RESOLVED",
                    "HIGH" if sz else "UNKNOWN",
                    "reflection registration at %s (caller %s); size %s"
                    % (r.get("site", "?"), r.get("caller", "?"),
                       "from the C primitive" if sz else "UNRESOLVED - engine type")]) + "\n")
                af += 1
    print("\nwrote %d type(s) and %d field(s) into %s" % (at, af, a.store))
    return 0


if __name__ == "__main__":
    sys.exit(main())
