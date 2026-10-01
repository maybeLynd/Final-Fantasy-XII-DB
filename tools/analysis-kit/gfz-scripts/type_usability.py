#!/usr/bin/env python3
"""type_usability.py - how usable are the store's GAME types, for the gate's first criterion?

The reconstruction gate asks for "usable types/ABIs/lifetimes". `types_index.py` already validates the
store's internal consistency - overlapping fields are errors, undeclared spans are gaps - and
`check_type_refs.py` already catches a ctype naming a type that does not exist. Neither asks the
question a reconstruction asks:

    if I had to declare this structure today, how much of it could I give a real type,
    how much would be opaque bytes, and how much would be a hole?

THREE CLASSES, PER TYPE, NEVER AVERAGED INTO ONE SCORE:

  TYPED       a field whose ctype resolves to something with content meaning - a scalar, a pointer,
              an array of those, or another store type.
  OPAQUE      offset and width known, contents not. This includes `UNRESOLVED` **and every byte
              array**: see below.
  UNDECLARED  no field row at all.

**A BYTE ARRAY IS OPAQUE, AND GETTING THAT WRONG INFLATED THIS TOOL BY ITSELF.** The first version
counted `uint8[65536]` as typed because it is declarable, which made `SpawnKeepImage` 100 percent
typed on the strength of two 64 KB banks that say nothing whatever about contents. A `uint8[N]` tells
a reconstruction exactly as much as `UNRESOLVED` does. Reclassifying byte arrays as opaque moved that
type from 100 percent to 0 and the store-wide byte-weighted figure from 87 to 63.

**AND THE DENOMINATOR MUST BE NAMED, because one type is most of it.** `SavePayload` is 353,424 of the
558,481 described bytes - 63 percent of the store by mass - and it is 89 percent typed, so it carries
any byte-weighted average on its own. Excluding it, the remaining 205,057 bytes are 17 percent typed.
This tool prints the weighted figure, the figure without the largest type, and the unweighted
per-type median, and refuses to pick one.

THE LIFETIME HALF is not about bytes: does the type state an instance or allocation site, a
constructor, and a destructor - counting an explicit "none, because the storage is in the image" as
stated, because that is an answer and a blank is not.

WHAT THIS IS NOT. Not an ABI proof, and nothing here compiles. A store that emits cleanly is
self-consistent, not correct against the binary; the ABI evidence is in the instruction widths the
field rows cite.
"""
import argparse
import collections
import io
import os
import re
import statistics
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "..", "..", "FFXII TZA"))
ARR = re.compile(r"^(.*?)\s*\[\s*(\d+)\s*\]$")
BYTEEL = {"uint8", "u8", "char", "unsigned char", "int8", "s8", "byte"}


def load(db):
    types, fields = {}, collections.defaultdict(list)
    for n, l in enumerate(io.open(os.path.join(db, "_types", "types.tsv"), encoding="utf-8")):
        if not n or not l.strip():
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) < 12:
            continue
        try:
            sz = int(c[1], 16)
        except ValueError:
            sz = 0
        types[c[0]] = dict(size=sz, cat=c[2], inst=c[3], ctor=c[5], dtor=c[6], readiness=c[7])
    for n, l in enumerate(io.open(os.path.join(db, "_types", "fields.tsv"), encoding="utf-8")):
        if not n or not l.strip():
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) < 5:
            continue
        try:
            fields[c[0]].append((int(c[1], 16), int(c[2]), c[4].strip()))
        except ValueError:
            pass
    return types, fields


def classify(ct, sz, types):
    """typed = the ctype names something; opaque = width and offset only.

    THE HAND-MAINTAINED VOCABULARY IS GONE, because it was wrong three times. It began without
    pointers, so `void*` counted as opaque and a record of four pointers read 0 percent typed. It then
    lacked `i32`, so `VmValueStack`'s two `i32[64]` arrays read as opaque as well. A list of accepted
    spellings is a thing to keep wrong, and the store does not need one: `check_store_artifacts.py`
    already guarantees that every ctype in the store is a type rather than prose.

    So the rule is the honest one, with exactly two exclusions:
      UNRESOLVED   - the column says outright that nothing is known;
      a byte array - `uint8[N]` and its spellings tell a reconstruction precisely as much as
                     UNRESOLVED does, and counting them as knowledge inflated the store-wide figure
                     from 63 percent to 87.
    Everything else names something and counts.
    """
    if not ct or ct == "UNRESOLVED":
        return "opaque"
    m = ARR.match(ct)
    el = (m.group(1).strip() if m else ct).strip()
    if el.endswith("*"):
        return "typed"
    if el in BYTEEL and (m or sz > 1):
        return "opaque"
    return "typed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--all", action="store_true", help="list every type, not only the extremes")
    a = ap.parse_args()
    types, fields = load(a.db)
    game = [t for t, d in types.items() if d["cat"] and not d["cat"].startswith("22-")]

    rows = []
    for t in game:
        d = types[t]
        ty = op = 0
        for off, sz, ct in fields[t]:
            if classify(ct, sz, types) == "typed":
                ty += sz
            else:
                op += sz
        # A type with no declared extent has none to fall back on but the sum of its own fields,
        # and that fallback makes `undeclared` ZERO BY CONSTRUCTION - the failure this database
        # names in EVIDENCE-STANDARD, "a metric that returns its value by construction is not a
        # measurement". FieldRecordTable scored "size 4, 100% typed, 0% undeclared" on one declared
        # field and no known extent. The fallback stays, because a row still has to be printed, but
        # the type is marked and kept out of the tallies that would otherwise be flattered by it.
        synth = not d["size"]
        tot = d["size"] or (ty + op)
        life = sum(1 for k in ("inst", "ctor", "dtor")
                   if d[k] and d[k].strip() and d[k].strip() != "UNRESOLVED")
        rows.append((t, tot, ty, op, max(0, tot - ty - op), life, d["readiness"], synth))
    rows.sort(key=lambda r: -(r[2] / float(r[1]) if r[1] else 0))

    print("GAME TYPE USABILITY   (byte arrays count as OPAQUE - see the module docstring)")
    print()
    print("  %-28s %8s %6s %6s %6s  life" % ("type", "size", "typed", "opaqu", "undec"))
    show = rows if a.all else rows[:8] + rows[-8:]
    prev = None
    for t, tot, ty, op, un, life, rd, synth in show:
        if prev is not None and not a.all and t == rows[-8][0]:
            print("  %s" % ("... %d more ..." % (len(rows) - 16)))
        prev = t
        print("  %-28s %8d %5d%% %5d%% %5d%%  %d/3"
              % (t[:28], tot, 100 * ty // tot if tot else 0,
                 100 * op // tot if tot else 0, 100 * un // tot if tot else 0, life))

    T = sum(r[1] for r in rows)
    TY = sum(r[2] for r in rows)
    OP = sum(r[3] for r in rows)
    UN = sum(r[4] for r in rows)
    # THE DENOMINATOR PROBLEM RECURS ONE LEVEL DOWN, so name the top TWO. Excluding only the
    # largest type still leaves a denominator dominated by the second: SavePayload and
    # SpawnKeepImage together are about 87 percent of all described bytes, and the second is 0
    # percent typed because it is two 64 KB banks. Installing 158 fields on another type moved the
    # single-exclusion figure by 0.2 points, which looks like the work failing and is the measure
    # failing. The per-type median is the view that responds to work.
    ranked = sorted(rows, key=lambda r: -r[1])
    big, big2 = ranked[0], ranked[1]
    rest = [r for r in rows if r[0] != big[0]]
    Tr = sum(r[1] for r in rest)
    TYr = sum(r[2] for r in rest)
    rest2 = [r for r in rows if r[0] not in (big[0], big2[0])]
    Tr2 = sum(r[1] for r in rest2)
    TYr2 = sum(r[2] for r in rest2)
    per = sorted(100.0 * r[2] / r[1] for r in rows if r[1])

    print()
    print("  THREE VIEWS, AND THIS TOOL DOES NOT PICK ONE.")
    print("    byte-weighted, all %d game types : typed %.1f%%  opaque %.1f%%  undeclared %.1f%%"
          % (len(rows), 100.0 * TY / T, 100.0 * OP / T, 100.0 * UN / T))
    print("      denominator %d bytes, of which %s alone is %d (%.0f%%)"
          % (T, big[0], big[1], 100.0 * big[1] / T))
    print("    byte-weighted WITHOUT %-14s : typed %.1f%% of %d bytes"
          % (big[0], 100.0 * TYr / Tr, Tr))
    print("      but %s is %d of those (%.0f%%) and is %.0f%% typed, so:"
          % (big2[0], big2[1], 100.0 * big2[1] / Tr, 100.0 * big2[2] / big2[1] if big2[1] else 0))
    print("    byte-weighted without BOTH        : typed %.1f%% of %d bytes"
          % (100.0 * TYr2 / Tr2, Tr2))
    print("      the two together are %.0f%% of every described byte in the store"
          % (100.0 * (big[1] + big2[1]) / T))
    print("    per-type, unweighted             : median %.0f%%  mean %.0f%%"
          % (statistics.median(per), sum(per) / len(per)))
    print()
    print("  types at 100%% typed : %d        types below 25%% : %d"
          % (sum(1 for p in per if p >= 99.5), sum(1 for p in per if p < 25)))
    print("  lifetime stated in all three places : %d of %d"
          % (sum(1 for r in rows if r[5] == 3), len(rows)))
    synths = [r for r in rows if r[7]]
    real_zero = sum(1 for r in rows if r[4] == 0 and not r[7])
    print("  types with no undeclared bytes      : %d measured%s"
          % (real_zero,
             ("  (+%d with a SYNTHESISED extent, whose 0%% is by construction, not measured: %s)"
              % (len(synths), ", ".join(sorted(r[0] for r in synths)))) if synths else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
