#!/usr/bin/env python3
"""check_name_coordinates.py - a field named in its PARENT's coordinates, on a rebased type.

WHY. A sub-object declared with `EMBED <Parent> +0xOFF` has its own offsets starting at zero,
but some of its rows kept names built from the address they had in the parent -
`ManagerSub0209BE80_8FA0`'s `ptr9FE8` sits at `+0x1048`, and `0x8FA0 + 0x1048 = 0x9FE8`. On a
type whose offsets run 0..0x1130 a name saying `9FE8` points a reader at an offset that does not
exist here. Half a type named in one coordinate system and half in another is a trap for exactly
the reader the naming is for.

THE RULE IS EXACT AND THAT MATTERS, because the first two attempts at it were not.

  * Attempt one matched any trailing hex-looking run. `[0-9A-Fa-f]{3,5}$` reads the `d` of
    "Dword" and the `e` of "Byte" as digits, so `ctorDword20` "names" 0xD20 and `stateByte5C`
    "names" 0xE5C. It reported 93 types, every one an artifact.
  * Attempt two required the delta to equal the type's OWN declared embed offset, which is the
    right rule - but still matched greedily, so `wordA09C` was read as `0xDA09C` (taking the `d`
    of "word") and MISSED, while its neighbour `bitsA09A` matched because `s` is not a hex
    digit. Two real rows were lost to the same artifact that invented ninety-three.

SO THE BOUNDARY IS THE STORE'S OWN CASING, not a hex test: these names are lowercase words
with an UPPERCASE hex tail, so the number is the maximal trailing run of digits and uppercase
A-F and a lowercase letter ends it. `ctorDword20` stops at the lowercase `d` and reads 0x20;
`stateByte5C` stops at the lowercase `e` and reads 0x5C; `wordA09C` stops at the lowercase `d`
and reads 0xA09C. That single rule fixes both earlier failures at once, and the correction found
FIVE MORE real rows than the hand count that preceded it - 13, not 8.

AND EMBED OFFSET 0 IS EXCLUDED: at `+0x0` the parent and child coordinates are identical, so
every row "matches" and nothing is learned - `ManagerSub7FB0Record` and `SecondaryContextElement`
are both that case.

WHAT IT DOES NOT DO. It does not rename anything. Most of these rows are cited by name in
between one and four documents, so a rename is a propagation with real cost across other agents'
pages; the rows are annotated instead and the rename is left as a recorded decision.

    check_name_coordinates.py [--self-test]
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP  # noqa: E402

EMB = re.compile(r"EMBED\s+\S+\s*\+\s*(0x[0-9A-Fa-f]+)")
HEXCH = set("0123456789abcdefABCDEF")


def trailing_numbers(name):
    """The trailing hex run, using the store's own casing convention as the boundary.

    These names are lowercase words with an UPPERCASE hex tail - `ptr9FE8`, `wordA09C`,
    `count5972`, `bits7C7C`. So the number is the maximal trailing run of digits and
    UPPERCASE A-F, and a lowercase letter ends it. That is what separates the real tail from
    the artifact: in `ctorDword20` the scan stops at the lowercase `d` and reads 0x20, not
    0xD20, and in `stateByte5C` it stops at the lowercase `e` and reads 0x5C, not 0xE5C -
    the two shapes that made a first attempt report 93 types of nothing. In `wordA09C` it
    stops at the lowercase `d` and reads 0xA09C, which a greedy run swallowed.

    THE CONVENTION IS AN ASSUMPTION AND IS STATED AS ONE. A field named in all caps, or one
    whose hex tail is lowercase, is not read correctly here - it is missed, never invented,
    which is the safe direction for a check that only ever raises questions.
    """
    run = ""
    for ch in reversed(name):
        if ch.isdigit() or (ch.isalpha() and ch.isupper() and ch in "ABCDEF"):
            run = ch + run
        else:
            break
    return [int(run, 16)] if run else []


def scan(db):
    t = list(csv.reader(io.open(os.path.join(db, "_types", "types.tsv"),
                                encoding="utf-8", newline=""), delimiter="\t"))
    h = t[0]
    iT, iR = h.index("type"), h.index("route")
    emb = {}
    for x in t[1:]:
        if len(x) <= iR:
            continue
        m = EMB.search(x[iR] or "")
        if m:
            v = int(m.group(1), 16)
            if v:                      # +0x0 makes the two coordinate systems identical
                emb[x[iT]] = v
    rows = list(csv.reader(io.open(os.path.join(db, "_types", "fields.tsv"),
                                   encoding="utf-8", newline=""), delimiter="\t"))
    hits = collections.defaultdict(list)
    for x in rows[1:]:
        if len(x) < 4 or x[0] not in emb:
            continue
        try:
            off = int(x[1], 16)
        except ValueError:
            continue
        for named in trailing_numbers(x[3]):
            if named - off == emb[x[0]]:
                hits[x[0]].append((x[1], x[3], named))
                break
    return emb, hits


def self_test():
    ok = True
    cases = [("ptr9FE8", 0x9FE8), ("wordA09C", 0xA09C), ("bitsA09A", 0xA09A),
             ("count5972", 0x5972)]
    for nm, want in cases:
        got = trailing_numbers(nm)
        hit = want in got
        ok &= hit
        print("  %-12s -> %-28s contains 0x%X: %s"
              % (nm, [hex(g) for g in got[:3]], want, "yes" if hit else "NO"))
    # the artifacts that broke attempt one must NOT produce the bogus number
    for nm, bogus in (("ctorDword20", 0xD20), ("stateByte5C", 0xE5C)):
        got = trailing_numbers(nm)
        clean = bogus not in got
        ok &= clean
        print("  %-12s -> %-28s excludes 0x%X: %s"
              % (nm, [hex(g) for g in got[:3]], bogus, "yes" if clean else "NO"))
    print("SELF-TEST", "PASSES" if ok else "FAILS")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    emb, hits = scan(a.db)
    n = sum(len(v) for v in hits.values())
    print("NAME-COORDINATE CHECK  a rebased type's row named for its address in the PARENT")
    print("  types with a non-zero declared EMBED offset: %d" % len(emb))
    print("  rows named in the parent's coordinates     : %d across %d type(s)"
          % (n, len(hits)))
    for t, items in sorted(hits.items()):
        print("    %-34s embed +0x%X" % (t, emb[t]))
        for off, nm, v in items:
            print("       %-8s %-22s name says 0x%X, this type's offset is %s" % (off, nm, v, off))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
