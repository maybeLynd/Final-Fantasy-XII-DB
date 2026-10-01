#!/usr/bin/env python3
"""check_embed_parent_fields.py - what the parent says is at the offset its child claims.

`check_storage_class.py` verifies that an `EMBED Parent +0xOFF` child FITS inside the parent's
declared size, and that two children do not overlap each other. **Neither it nor anything else asks
what the PARENT declares at that offset.** The child and the parent are two rows describing the same
bytes, and until now nothing compared them.

Four outcomes, and they mean different things:

  COVERED BY AN UNREAD SPAN   the parent calls those bytes unknown and the child explains them.
                              **This is the useful case** - the child's name and size are exactly
                              what the parent's span was missing, and the parent row can borrow it.
  EXACT                       the parent declares one field at that offset whose size matches the
                              child's span. The two agree and there is nothing to do.
  SPLIT ACROSS FIELDS         the parent declares several fields over the child's span. Normal for
                              a child whose members the parent enumerated first; reported, not
                              faulted.
  CONFLICT                    a single parent field of a DIFFERENT size straddles the child's start,
                              or the child starts inside a declared scalar. The two rows disagree
                              about what those bytes are.

No verdict is issued for the first three. Only CONFLICT is a defect, and even there the instrument
prints both rows rather than deciding which is right.

    python check_embed_parent_fields.py
"""
import argparse
import bisect
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP

R_EMBED = re.compile(r"^EMBED\s+([A-Za-z0-9_]+)\s*\+\s*(0x[0-9A-Fa-f]+)"
                     r"(?:\s+stride=(0x[0-9A-Fa-f]+|\d+))?(?:\s+count=(\d+))?")
UNREAD = re.compile(r"^(unobserved|unknown|unread|pad)", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default=os.path.join(KP.DB, "_types", "types.tsv"))
    ap.add_argument("--fields", default=os.path.join(KP.DB, "_types", "fields.tsv"))
    a = ap.parse_args()

    sizes, routes = {}, {}
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            try:
                sizes[f[0]] = int(f[1], 0)
            except ValueError:
                pass
            routes[f[0]] = (f[12] or "").strip()

    fields = collections.defaultdict(list)
    with io.open(a.fields, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9 or not f[0]:
                continue
            try:
                fields[f[0]].append((int(f[1], 0), int(f[2], 0), f[3], f[4]))
            except ValueError:
                pass
    for k in fields:
        fields[k].sort()

    buckets = collections.Counter()
    covered, conflicts, splits = [], [], []
    n = 0
    for child, route in sorted(routes.items()):
        for alt in route.split("|"):
            m = R_EMBED.match(alt.strip())
            if not m:
                continue
            parent, off = m.group(1), int(m.group(2), 0)
            stride = int(m.group(3), 0) if m.group(3) else sizes.get(child, 0)
            count = int(m.group(4)) if m.group(4) else 1
            span = stride * count
            if not span or parent not in fields:
                buckets["parent has no field rows"] += 1
                break
            n += 1
            pf = fields[parent]
            starts = [x[0] for x in pf]
            i = bisect.bisect_right(starts, off) - 1
            inside = [x for x in pf if x[0] < off + span and x[0] + x[1] > off]
            if not inside:
                buckets["no parent field covers it"] += 1
                break
            if len(inside) == 1:
                po, ps, pn, pc = inside[0]
                if po == off and ps == span:
                    buckets["EXACT"] += 1
                elif re.match(r"^%s\s*\[\s*\d+\s*\]$" % re.escape(child), (pc or "").strip()):
                    # THE PARENT DECLARES AN ARRAY OF THE CHILD. `BattleTargetBuffer +0x8` is
                    # `entries BattleTargetEntry[32]`, 512 bytes, and the child is its 16-byte
                    # ELEMENT embedded at the same offset. Judged by size alone that reads as a
                    # child buried inside an unrelated field, which is how this check reported its
                    # only "conflict" on the first run. The two rows are the same fact stated at
                    # two granularities, and they agree.
                    buckets["EXACT (parent declares an array of the child)"] += 1
                elif UNREAD.match(pn or ""):
                    buckets["COVERED BY AN UNREAD SPAN"] += 1
                    covered.append((child, span, parent, off, po, ps, pn))
                elif po <= off and po + ps >= off + span:
                    buckets["CONFLICT - inside one declared field"] += 1
                    conflicts.append((child, span, parent, off, po, ps, pn, pc))
                else:
                    buckets["CONFLICT - straddles a declared field"] += 1
                    conflicts.append((child, span, parent, off, po, ps, pn, pc))
            else:
                if all(UNREAD.match(x[2] or "") for x in inside):
                    buckets["COVERED BY UNREAD SPANS"] += 1
                    covered.append((child, span, parent, off, inside[0][0],
                                    sum(x[1] for x in inside), "%d unread spans" % len(inside)))
                else:
                    buckets["SPLIT ACROSS FIELDS"] += 1
                    splits.append((child, span, parent, off, inside))
            break

    print("EMBED children checked against their parent's field rows: %d" % n)
    for k, v in buckets.most_common():
        print("  %-36s %d" % (k, v))
    print()
    if covered:
        print("COVERED BY AN UNREAD SPAN -- the parent calls these bytes unknown and the child names them:")
        for child, span, parent, off, po, ps, pn in covered:
            print("  %-30s 0x%-5X  is inside  %s +0x%-5X %-3d %s"
                  % (child[:30], span, parent[:24], po, ps, pn))
        print()
    if conflicts:
        print("CONFLICT -- the parent declares something else over those bytes:")
        for child, span, parent, off, po, ps, pn, pc in conflicts:
            print("  %-30s at %s +0x%-5X span 0x%X" % (child[:30], parent[:24], off, span))
            print("        parent row: +0x%-5X %-4d %-24s %s" % (po, ps, pn[:24], pc))
        print()
    if splits:
        print("SPLIT ACROSS FIELDS -- normal where the parent enumerated the members first:")
        for child, span, parent, off, inside in splits:
            print("  %-30s at %s +0x%-5X over %d parent field(s)"
                  % (child[:30], parent[:24], off, len(inside)))
        print()

    # PASS 2, and it is the generalisation of the one finding pass 1 produced. A field whose ctype
    # NAMES a type is a second statement about the same bytes, so its size must be that type's size
    # (or N times it for an array). `BattleUnit +0x200 navigationPathState NavigationPathState` was
    # declared 152 bytes against a child of 0x490, and the 1,016-byte difference sat beside it as an
    # unread span -- 1,016 bytes the store could already name one level down.
    ARR = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*(\d+)\s*\]$")
    named, mismatched = 0, []
    for tname, rows in sorted(fields.items()):
        for off, size, fname, ct in rows:
            ct = (ct or "").strip()
            m = ARR.match(ct)
            base, mult = (m.group(1), int(m.group(2))) if m else (ct, 1)
            if base not in sizes:
                continue
            named += 1
            want = sizes[base] * mult
            if want != size:
                mismatched.append((tname, off, size, ct, want, want - size))
    print("PASS 2 -- field rows whose ctype names a known type: %d" % named)
    print("  size matches the named type's size : %d" % (named - len(mismatched)))
    print("  size DISAGREES                     : %d" % len(mismatched))
    for tname, off, size, ct, want, delta in sorted(mismatched, key=lambda x: -abs(x[5])):
        print("    %-28s +0x%-5X declared %-6d ctype %-24s implies %-6d  delta %+d"
              % (tname[:28], off, size, ct[:24], want, delta))
    if mismatched:
        print("  A DELTA IS NOT AUTOMATICALLY THE FIELD'S FAULT: the named type's own size can be")
        print("  the wrong one. Read both rows; the one case found so far was the field, and the")
        print("  missing bytes were carried beside it as an unread span.")

    # PASS 3 -- CHAIN and RELOFF are parent/child links too, and the parent's row at the offset has
    # to be the right SHAPE for the verb. `check_storage_class.py` states it checks the CHAIN case
    # and reports nothing for these six routes either way, so they are checked here explicitly:
    #
    #   CHAIN  Parent +0xOFF   instance = *(parent + OFF)               -> an 8-byte POINTER
    #   RELOFF Parent +0xOFF   instance = parent + *(int32*)(parent+OFF) -> a 4-byte INTEGER
    #
    # A CHAIN meeting an integer is a different ABI, not a typo, which is why the verbs are distinct.
    R_LINK = re.compile(r"^(CHAIN|RELOFF)\s+([A-Za-z0-9_]+)\s*\+\s*(0x[0-9A-Fa-f]+)")
    PTRCT = re.compile(r"(\*$|^void\*$|^ptr$)")
    link_ok, link_bad = 0, []
    for child, route in sorted(routes.items()):
        for alt in route.split("|"):
            m = R_LINK.match(alt.strip())
            if not m:
                continue
            verb, parent, off = m.group(1), m.group(2), int(m.group(3), 0)
            row = next((x for x in fields.get(parent, [])
                        if x[0] <= off < x[0] + x[1]), None)
            if row is None:
                link_bad.append((child, verb, parent, off, None, "no parent field covers it"))
                continue
            po, ps, pn, pc = row
            if verb == "CHAIN":
                good = ps == 8 and bool(PTRCT.search((pc or "").strip()))
                want = "an 8-byte pointer"
            else:
                good = ps == 4 and re.match(r"^(u?int32|i32|u32)$", (pc or "").strip())
                want = "a 4-byte integer"
            if good:
                link_ok += 1
            else:
                link_bad.append((child, verb, parent, off, (po, ps, pn, pc), want))
    print()
    print("PASS 3 -- CHAIN / RELOFF links whose parent row must match the verb: %d"
          % (link_ok + len(link_bad)))
    print("  parent declares the right shape : %d" % link_ok)
    print("  does NOT                        : %d" % len(link_bad))
    for child, verb, parent, off, row, want in link_bad:
        print("    %-30s %s %s +0x%X wants %s" % (child[:30], verb, parent[:22], off, want))
        if row:
            print("        parent row: +0x%-5X %-4d %-22s %s" % (row[0], row[1], row[2][:22], row[3]))
    # PASS 4 -- DYNAMIC routes are free text and not consumable by a generator, but where the text
    # names a TYPE and an offset it is still a claim about a declared field, and that is checkable.
    # Three of the eight do; the other five say "owner" without saying which type owns them, which
    # is a documentation gap rather than a defect - a reader cannot resolve them without opening the
    # owning page, and no instrument can resolve them at all.
    R_DYN = re.compile(r"\*\(\s*([A-Z][A-Za-z0-9_]*)\s*\+\s*(0x[0-9A-Fa-f]+)\s*\)")
    dyn_ok, dyn_bad, dyn_unnamed, dyn_undeclared = 0, [], 0, {}
    for child, route in sorted(routes.items()):
        if not route.strip().startswith("DYNAMIC"):
            continue
        # A `count=*(Type+off)` expression is a COUNT READ, not a pointer dereference to the
        # object, so it must not be checked as one. Naming the LegacyPs2Gs owner in its children's
        # routes turns `count=*(owner+0x224)` into `count=*(LegacyPs2GsTextureContext+0x224)`, and
        # +0x224 is a uint32 element count -- correct, and reported as a defect by a rule that
        # assumes every deref yields the object. The count clauses are stripped first.
        base_only = re.sub(r"count=\*\([^)]*\)", "", route)
        found = R_DYN.findall(base_only)
        if not found:
            if re.search(r"\bowner\b", route):
                dyn_unnamed += 1
            continue
        for parent, off in found:
            o = int(off, 0)
            if parent not in sizes:
                # THE NAMED OWNER IS NOT A DECLARED TYPE, which is a different gap from a declared
                # type missing a field, and only the second is a defect. `AudioParameterRamp` names
                # `Category` because its owning page does (DQ-1, FABLE 2026-09-14) and `Category`
                # has no row; naming it is strictly better than the anonymous `owner` it replaced,
                # and reporting that as a field defect would punish the improvement.
                dyn_undeclared.setdefault(parent, set()).add(child)
                continue
            row = next((x for x in fields.get(parent, []) if x[0] <= o < x[0] + x[1]), None)
            if row is None:
                dyn_bad.append((child, parent, o, None))
            elif row[1] == 8 and PTRCT.search((row[3] or "").strip()):
                dyn_ok += 1
            else:
                dyn_bad.append((child, parent, o, row))
    print()
    print("PASS 4 -- DYNAMIC routes whose text names a type and offset: %d"
          % (dyn_ok + len(dyn_bad)))
    print("  the named field exists and is a pointer : %d" % dyn_ok)
    print("  it does not                             : %d" % len(dyn_bad))
    for child, parent, o, row in dyn_bad:
        print("    %-30s dereferences %s +0x%X" % (child[:30], parent[:22], o))
        if row:
            print("        parent row: +0x%-5X %-4d %-22s %s" % (row[0], row[1], row[2][:22], row[3]))
        else:
            print("        parent declares no field there")
    print("  the named owner is itself an undeclared type : %d" % len(dyn_undeclared))
    for p2, kids in sorted(dyn_undeclared.items()):
        print("    %-24s named by %s -- no type row exists" % (p2[:24], ", ".join(sorted(kids))))
    print("  DYNAMIC routes that say \"owner\" without naming the type : %d" % dyn_unnamed)
    print("  Those are unresolvable by any instrument and by a reader who has not opened the")
    print("  owning page. Recorded as a documentation gap, not counted as a defect.")
    return 1 if (conflicts or mismatched or link_bad or dyn_bad) else 0


if __name__ == "__main__":
    sys.exit(main())
