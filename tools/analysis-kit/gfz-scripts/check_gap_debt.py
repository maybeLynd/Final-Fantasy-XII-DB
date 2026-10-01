#!/usr/bin/env python3
"""check_gap_debt.py - the 649 declared gap rows, against the censuses that should have made them.

WHY. `types_index --validate` reports **0 gaps**, and that means every byte of every declared type
is covered by some row. 649 of those rows are `unobservedSpan*` - **79,450 bytes, 8.5 % of the
store** - whose whole content is "extent-declared gap; width = declared span, not an instruction
access". Byte coverage, not description. A reader cannot tell a gap nobody looked at from a gap
that was looked at hard and found empty, and those are different debts: the first is work not done,
the second is a fact about the object.

WHAT THIS DOES. 74 types carry a `*-accesses.tsv` census. For every gap row in one of those types,
it counts the censused access sites whose displacement falls INSIDE the gap's span, and sorts each
row into one of three classes:

  UNREAD    the type was censused and nothing in the census touches this span. The gap is a
            measured absence over that census's population - which is not the same as unused, and
            the header of every such census says what it did and did not follow.
  TOUCHED   an UNAMBIGUOUS, type-specific site READS OR WRITES a byte of this span. That is a
            defect: a row saying `no instruction access` over such bytes is wrong on its face.
            **This is currently ZERO, and getting it to zero took four corrections to this file
            rather than any change to the store.**
  AMBIGUOUS the census touches the span only from sites that ALSO reach other displacements in the
            same census. Not a defect.
  INHERITED every function reaching the span also censuses against another type, so it is shared
            code working on something the types have in common. The span is a child's interior.
  UNMEASURED  the type has no census. Nothing is claimed about these bytes at all, and they are
            the honest majority of the debt.

THE RESULT IS ABOUT THIS FILE, NOT ABOUT THE STORE, and it is worth stating plainly: the first run
reported **14 defects and every one of them was mine.** In order of discovery -

  3 were RECEIVER AMBIGUITY (below), 8 were CHILD INTERIORS reached only by shared code, and the
  last 2 were `lea` instructions: `lea eax, [rdx - 1]` and `lea rdi, [rsi + 0x20]`, both recorded
  with `kind` = `addr`. **Taking a span's address is not reading a byte in it**, and a row saying
  `no instruction access` is not contradicted by it. An address-taken span is its own debt - an
  undescribed sub-object - and `addr`/`a` rows are now skipped outright.

So **not one of the 649 gap rows is contradicted by a real read**, which is a fact about the store
worth having: the gap rows are honest. What they are not is *informative*, and that is the debt the
counts above rank.

WHY AMBIGUOUS HAD TO BECOME ITS OWN CLASS, because it inverted a finding. In
`ManagerSub0209BE80_57E0`, 109 of 252 distinct (site, instruction) pairs reach EXACTLY THREE
displacements, and every one of them is `{d, d+0xD0, d+0x1A0}` - 218 deltas of 0xD0 and nothing
else. The first run read that as five gap rows wrongly declaring bytes unread. It is the opposite.
**Every one of those 109 sites belongs to a GENERIC widget function** - `002465F0` the constructor,
`00246AD0` the animation starter, `00244DD0` the backward starter, `002482E0` the release,
`00273A20` the liveness latch - whose receiver arrives in a register, so the census charged one
instruction to all three candidate bases because it could not tell which. Meanwhile the 141
single-displacement sites belong to TYPE-SPECIFIC functions (`003FA160` 40 sites, `003F9F40` 29)
and land on the distinctive offsets - `0xC0`/`0xC4`/`0xC8`, `0x192`, `0x262`, `0x270`+.

So a multi-displacement site is evidence about the RECEIVER, not about the byte: it says three
objects of one shape sit at +0x000, +0x0D0 and +0x1A0, which is what `0xD0`, the minimum widget
extent, predicts. It is emphatically NOT evidence that those particular bytes are read in this
type's coordinates. Counting it as a read would charge every generic widget call to every widget
in the image.

WHAT IT DOES NOT DO. It does not open callees, follow pointers out of the record, or judge whether
an UNREAD span is padding, a reserved field or a live member read through some route the census
cannot see. It ranks debt; it does not discharge it. And a type with no census is reported as
UNMEASURED rather than silently dropped, because the difference between `nobody looked` and
`looked and found nothing` is the entire point of the file.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

FIELDS = os.path.join(KP.DB, "_types", "fields.tsv")


def load_registry():
    """The census map from check_census_widths, read rather than duplicated.

    A DATA CONTRACT, explicit since 2026-09-29 (FRONTIER-REQ-OPUS-COMPOSER-PREREQ-REPAIRS, matrix A03): loading the module
    runs none of its checks (they sit under __main__), so only its import has to succeed (exit 0: any SystemExit at import
    is a broken prerequisite, not a finding) and CENSUS must be a non-empty dict of name -> record. Before, a SystemExit
    was swallowed and whatever CENSUS existed was used. GAP_DEBT_CENSUS_SOURCE overrides the file (tests only)."""
    import prereq
    p = os.environ.get("GAP_DEBT_CENSUS_SOURCE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_census_widths.py")
    def valid(m):
        c = getattr(m, "CENSUS", None)
        if not isinstance(c, dict) or not c:
            return "CENSUS is not a non-empty dict"
        return None
    mod, why = prereq.run(p, [p], names=("CENSUS",), exits=(0,), validate=valid)
    if why:
        print("PREREQUISITE FAILED: %s - no gap-debt verdict is computed" % why)
        sys.exit(2)
    return dict(mod.CENSUS)


def find_census(name):
    for root, _dirs, files in os.walk(KP.DB):
        if name in files:
            return os.path.join(root, name)
    return None


def num(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s)
    except ValueError:
        return None


def census_displacements(path):
    """Displacements the census reached, split by whether the reaching site is unambiguous.

    A (site, instruction) pair that reaches more than one displacement in the same census did not
    reach them all - it reached one, and the census could not tell which base. Such a site says
    something about the receiver and nothing about the byte, so its hits are kept apart.
    """
    per_site = collections.defaultdict(set)
    raw = io.open(path, encoding="utf-8", newline="").read().split("\n")
    if not raw:
        return {}, {}
    head = raw[0].split("\t")
    if "disp" not in head:
        return {}, {}
    i_d = head.index("disp")
    i_s = head.index("site") if "site" in head else None
    i_i = head.index("instruction") if "instruction" in head else None
    i_k = head.index("kind") if "kind" in head else None
    i_n = head.index("note") if "note" in head else None
    for line in raw[1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        c = line.split("\t")
        if len(c) <= i_d:
            continue
        d = num(c[i_d])
        if d is None:
            continue
        # `addr`/`a` is a lea: the span's ADDRESS is taken, no byte in it is touched. A row saying
        # `no instruction access` is not contradicted by that, and both of the rows this file first
        # reported as its last two defects were exactly this - `lea eax, [rdx - 1]` and
        # `lea rdi, [rsi + 0x20]`. Address-taken spans are their own debt (an undescribed
        # sub-object) and are counted separately.
        if i_k is not None and len(c) > i_k and c[i_k].strip() in ("addr", "a"):
            continue
        # `receiver-foreign` in the note marks a site whose tracked registers resolve to a
        # DIFFERENT object than the seeded receiver - the census's receiver pair collapses
        # (e.g. `[r14 + r12 - 0x60]` where r12 is a second object minus the base, not an
        # index, so the access lands on that object, never on this type). The row stays in
        # the file because the scanner did see the site; it is simply not this type's byte.
        if i_n is not None and len(c) > i_n and "receiver-foreign" in c[i_n]:
            continue
        site = c[i_s] if i_s is not None and len(c) > i_s else "?"
        ins = c[i_i] if i_i is not None and len(c) > i_i else ""
        per_site[(site, ins)].add(d)
    firm, soft = collections.defaultdict(list), collections.defaultdict(list)
    for (site, _ins), ds in per_site.items():
        tgt = firm if len(ds) == 1 else soft
        for d in ds:
            tgt[d].append(site)
    return firm, soft


def census_functions(path):
    """disp -> the functions that reach it, for telling shared code from type-specific code."""
    out = collections.defaultdict(set)
    raw = io.open(path, encoding="utf-8", newline="").read().split("\n")
    if not raw:
        return out
    head = raw[0].split("\t")
    if "disp" not in head or "function" not in head:
        return out
    i_d, i_f = head.index("disp"), head.index("function")
    i_k = head.index("kind") if "kind" in head else None
    i_n = head.index("note") if "note" in head else None
    for line in raw[1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        c = line.split("\t")
        if len(c) <= max(i_d, i_f):
            continue
        if i_k is not None and len(c) > i_k and c[i_k].strip() in ("addr", "a"):
            continue
        if i_n is not None and len(c) > i_n and "receiver-foreign" in c[i_n]:
            continue
        d = num(c[i_d])
        if d is not None:
            out[d].add(c[i_f])
    return out


def shared_functions(reg, seen):
    """Functions that appear in MORE THAN ONE registered census.

    A function censused against several different types is operating on something those types have
    in common - a base class, an embedded child, a shared helper - rather than on a member of any
    one of them. That is measurable here without naming a single address, which is the point: the
    widget object model is the case that forced this, but the rule is not about widgets.
    """
    where = collections.defaultdict(set)
    for t, art in reg.items():
        if art not in seen:
            seen[art] = find_census(art)
        p = seen[art]
        if not p:
            continue
        raw = io.open(p, encoding="utf-8", newline="").read().split("\n")
        head = raw[0].split("\t")
        if "function" not in head:
            continue
        i_f = head.index("function")
        for line in raw[1:]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            c = line.split("\t")
            if len(c) > i_f:
                where[c[i_f]].add(art)
    return set(f for f, arts in where.items() if len(arts) > 1)


def unprefixed_gaps(raw, I):
    """Rows carrying types_index's OWN gap boilerplate under a name that is not `unobserved*`.

    THIS FILE COUNTS GAPS BY NAME PREFIX, which is a CONVENTION and not a measurement, so a gap row
    that was renamed drops out of every total here. Two broader attempts to find such rows by
    reading the meaning text both failed, in both directions, and neither number was publishable:
    matching phrases like `no observed access` swept in `iniPath` (520 B, a real path field with a
    stated capacity) and `scriptGlobalSpaceLow` (2048 B, the script-global variable space), while
    excluding rows whose evidence merely happens to cite an address dropped a row whose meaning
    opens by calling itself a gap.

    The ONE rule that is not a heuristic keys on the generator's own boilerplate - the exact opening
    `types_index --validate` writes for a gap it creates. That finds exactly one row today:
    `PersistentFlagPayload.scriptGlobalSpaceUndeclaredTail`, 778 bytes.

    ITS LIMIT, STATED SO THE NUMBER IS NOT MISREAD: only 406 of the 724 prefixed rows still carry
    that boilerplate, because the rest have been described since. So this detector finds gaps nobody
    has re-worded, and a gap row that was BOTH renamed and re-worded is invisible to it and to every
    rule tried. The totals in this file are a floor by convention, and the size of the undercount is
    not mechanically determinable.
    """
    out = []
    for line in raw[1:]:
        if not line.strip():
            continue
        c = line.split("\t")
        if len(c) <= max(I["name"], I["meaning"]):
            continue
        if c[I["name"]].startswith("unobserved"):
            continue
        if c[I["meaning"]].lstrip().lower().startswith("declared gap span"):
            out.append((c[I["type"]], c[I["offset"]], c[I["name"]], num(c[I["size"]])))
    return out


def main():
    reg = load_registry()
    raw = io.open(FIELDS, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    I = {k: head.index(k) for k in head}
    renamed = unprefixed_gaps(raw, I)
    gaps = collections.defaultdict(list)
    for line in raw[1:]:
        if not line.strip():
            continue
        c = line.split("\t")
        if not c[I["name"]].startswith("unobservedSpan"):
            continue
        off, size = num(c[I["offset"]]), num(c[I["size"]])
        if off is None or not size:
            continue
        gaps[c[I["type"]]].append((off, size, c[I["name"]]))

    seen = {}
    shared = shared_functions(reg, seen)
    unread = touched = ambig = unmeasured = inherited = 0
    ub = tb = ab = ib = mb = 0
    findings = []
    ambiguous = []
    inherit = []
    ranked = []
    for t in sorted(gaps):
        art = reg.get(t)
        path = None
        if art:
            if art not in seen:
                seen[art] = find_census(art)
            path = seen[art]
        firm, soft = census_displacements(path) if path else (None, None)
        fnmap = census_functions(path) if path else {}
        for off, size, name in gaps[t]:
            if firm is None:
                unmeasured += 1
                mb += size
                continue
            hit = sorted(set((d, s) for d, ss in firm.items()
                             if off <= d < off + size for s in ss))
            maybe = sorted(set((d, s) for d, ss in soft.items()
                               if off <= d < off + size for s in ss))
            reach = set()
            for d, fs in fnmap.items():
                if off <= d < off + size:
                    reach |= fs
            if hit and reach and reach <= shared:
                inherited += 1
                ib += size
                inherit.append((t, name, off, size, sorted(reach)))
            elif hit:
                touched += 1
                tb += size
                findings.append((t, name, off, size, hit))
            elif maybe:
                ambig += 1
                ab += size
                ambiguous.append((t, name, off, size, maybe))
            else:
                unread += 1
                ub += size
                ranked.append((size, t, name, off, len(firm)))

    tot = unread + touched + ambig + inherited + unmeasured
    print("DECLARED GAP ROWS AGAINST THE CENSUSES THAT SHOULD HAVE MADE THEM")
    print("  gap rows                                   : %d" % tot)
    print("  types holding them                         : %d" % len(gaps))
    print("  of those types, censused                   : %d of %d registered"
          % (len(set(t for t in gaps if reg.get(t))), len(reg)))
    print()
    print("  UNREAD     censused, nothing touches the span   : %5d rows, %7d bytes" % (unread, ub))
    print("  TOUCHED    an UNAMBIGUOUS site touches it       : %5d rows, %7d bytes  <-- defect"
          % (touched, tb))
    print("  AMBIGUOUS  touched only by multi-base sites     : %5d rows, %7d bytes  (not a defect)"
          % (ambig, ab))
    print("  INHERITED  reached only by SHARED functions     : %5d rows, %7d bytes  (a child, "
          "not a parent field)" % (inherited, ib))
    print("  UNMEASURED no census for the type               : %5d rows, %7d bytes"
          % (unmeasured, mb))
    print()
    if findings:
        print("TOUCHED - a row saying `no instruction access` over bytes ONE instruction reads:")
        for t, name, off, size, hits in findings:
            print("  %-34s %-22s +0x%04X..+0x%04X" % (t, name, off, off + size))
            for d, s in hits[:6]:
                print("       census reaches +0x%X at %s" % (d, s))
            if len(hits) > 6:
                print("       ... and %d more" % (len(hits) - 6))
    else:
        print("TOUCHED: none. Every censused gap is a measured absence over its census.")
    print()
    if inherit:
        print("INHERITED - every function reaching this span also censuses against another type.")
        print("  Shared code operating on something the types have in common - a base class or an")
        print("  embedded child - so the span is a CHILD'S INTERIOR, not an undeclared parent field.")
        for t, name, off, size, fs in inherit:
            print("  %-34s %-22s +0x%04X..+0x%04X  via %s%s"
                  % (t, name, off, off + size, " ".join(fs[:6]),
                     " +%d more" % (len(fs) - 6) if len(fs) > 6 else ""))
        print()
    if ambiguous:
        print("AMBIGUOUS - reached only by sites that also reach other displacements here.")
        print("  The site says three objects share a shape; it does not say these bytes are read.")
        for t, name, off, size, hits in ambiguous:
            print("  %-34s %-22s +0x%04X..+0x%04X  (%d site(s))"
                  % (t, name, off, off + size, len(set(s for _d, s in hits))))
        print()
    print("GAPS THIS FILE CANNOT SEE, because it counts by NAME and they were renamed:")
    if renamed:
        for t, off, name, size in sorted(renamed, key=lambda x: -x[3]):
            print("  %6d B  %-30s %-8s %s" % (size, t, off, name))
        print("  Found by the generator's own boilerplate, which is the only rule here that is not")
        print("  a heuristic. LIMIT: it sees only gaps nobody has re-worded, so the totals above")
        print("  are a floor BY CONVENTION and the undercount is not mechanically determinable.")
    else:
        print("  none - every row carrying the gap boilerplate is named unobserved*.")
    print()
    print("THE LARGEST UNREAD SPANS - censused and empty, ranked by bytes:")
    for size, t, name, off, ndisp in sorted(ranked, reverse=True)[:15]:
        print("  %7d bytes  %-34s +0x%04X  (census reached %d displacements)"
              % (size, t, off, ndisp))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
