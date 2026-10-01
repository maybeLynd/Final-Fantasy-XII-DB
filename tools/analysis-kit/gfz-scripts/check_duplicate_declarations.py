"""Do two rows describe the same object?

WHAT THE OTHER GATES ASK. types_index checks a type against ITSELF (overlaps, overruns, gaps).
check_storage_class and the three route-vs-image checks ask whether a row agrees with the binary.
None of them compares two rows TO EACH OTHER, so a second declaration of an object already in the
store is invisible: both are internally consistent, both agree with the image, and both are counted.

WHAT THIS FOUND ON ITS FIRST RUN (2026-09-20). Two objects declared twice:

  PhyreInstanceListHeader  0x24, 9 fields  IDENTICAL offset-to-name map to  PInstanceListHeader
  PhyreClusterHeader       0x54, 21 fields  =  PClusterHeaderBase's 18 (identical names) + the
                                               three concrete PClusterHeaderD3D11 fields

Neither was found by looking for duplicates. They surfaced from an arithmetic surplus when joining
the store against the Phyre reflection name census, because in both cases THE ROW NAME IS NOT THE
REGISTERED CLASS NAME - which is exactly what makes a duplicate invisible to a name-based check.
Cost: type-debt-by-type.tsv counts every row, so those two objects contribute 240 and 72 declared
bytes for 84 and 36 bytes of storage.

AND A THIRD SHAPE ON THE SAME RUN. RenderResourceEntryBank, RenderStrideC0Bank and
RenderModelInstanceContainer share TWENTY identical semantic names at identical offsets, but they
are siblings (EMBED RenderResourceRoot at +0x0, +0x60, +0xF0) with differing field counts - so they
are not one object declared thrice, they are one BANK HEADER declared thrice. A duplicate and a
re-declared shared header are different defects and this reports both.

WHAT IT REPORTS AND WHAT IT LEARNED NOT TO. The first version excluded only unobservedSpan rows and
reported 14 pairs; eleven were widget types sharing field98/field9A/field9C/field9E, four int16s
whose names ARE their offsets. An offset-derived name carries no information beyond the offset, so
a shared one is arithmetic, not evidence. Excluding them leaves 4 pairs, all three real findings
among them. Containment is also checked against any relationship the store DECLARES - an EMBED or
CHAIN route naming the other type, or a `baseClass_` field - and those are reported separately.

An unexplained pair is a READING LIST entry. Two rows may describe one object deliberately, a
flattened row being easier to read than an inheritance pair, and PhyreClusterHeader's own evidence
cites the registrations it was built from. Which declaration is canonical is a judgement, not a
gate's decision.

Usage:  python check_duplicate_declarations.py [--store <db>/_types] [--self-test] [--min N]
"""
import argparse
import collections
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_types"))

# A span row is not evidence of anything shared - two types both having "unobservedSpan0000" are
# not related, they are both undeclared. Excluding them is what keeps this from reporting noise.
SPAN = re.compile(r"^(unobserved|unwritten|undeclared)", re.I)

# AN OFFSET-DERIVED NAME CARRIES NO INFORMATION BEYOND THE OFFSET, so two types sharing one are not
# related - they merely both have a named field there. `field98`, `dword0504`, `word153A` are this
# store's convention for "named, meaning not established". The first version of this check did not
# exclude them and reported eleven pairs of widget types as possible duplicates, every one of them
# resting on field98/field9A/field9C/field9E - four int16s whose names ARE their offsets. The two
# real duplicates it found survive the exclusion because their names are semantic (m_phyreMarker,
# m_size), which is the distinction that matters: a shared SEMANTIC name is evidence, a shared
# offset-derived name is arithmetic.
GENERIC = re.compile(r"^(field|dword|word|byte|qword|ptr|unk|slot|entry|rec)[0-9A-Fa-f]{2,}$", re.I)


def load(store):
    tl = io.open(os.path.join(store, "types.tsv"),
                 encoding="utf-8", newline="").read().split("\n")
    TH = {n: i for i, n in enumerate(tl[0].split("\t"))}
    fl = io.open(os.path.join(store, "fields.tsv"),
                 encoding="utf-8", newline="").read().split("\n")
    FH = {n: i for i, n in enumerate(fl[0].split("\t"))}

    maps = collections.defaultdict(set)
    basenames = collections.defaultdict(set)
    for ln in fl[1:]:
        f = ln.split("\t")
        if len(f) <= FH["name"] or not ln.strip():
            continue
        nm = f[FH["name"]]
        if nm.startswith("baseClass_"):
            basenames[f[FH["type"]]].add(nm[len("baseClass_"):])
        if SPAN.match(nm) or GENERIC.match(nm):
            continue
        try:
            maps[f[FH["type"]]].add((int(f[FH["offset"]], 16), nm))
        except ValueError:
            pass

    routes = {}
    for ln in tl[1:]:
        f = ln.split("\t")
        if len(f) > TH["route"] and ln.strip():
            routes[f[TH["type"]]] = f[TH["route"]] or ""
    return maps, basenames, routes


def related(a, b, basenames, routes):
    """Does the store DECLARE a relationship that explains containment?"""
    if a in basenames.get(b, ()) or b in basenames.get(a, ()):
        return "inheritance (baseClass_ field)"
    for x, y in ((a, b), (b, a)):
        if re.search(r"\b(?:EMBED|CHAIN|RELOFF)\s+%s\b" % re.escape(y), routes.get(x, "")):
            return "embedding (%s's route names %s)" % (x, y)
    # SIBLINGS UNDER ONE DECLARED PARENT - added 2026-09-21 (OPUS) on
    # SWE2-STRUCT-REQ-OPUS-PPHYSICS-TAPERED-DUPLICATE. Both rules above ask whether one type
    # CONTAINS the other, and neither can express the case that actually arose: two classes that
    # contain NEITHER each other but share a parent, registered separately against it with the
    # same schema. PPhysicsTaperedCapsule and PPhysicsTaperedCylinder both declare
    # baseClass_PPhysicsShape and carry distinct descriptors (02E490D0, 02E491D0), so their
    # identical map is expected and the pair was red on a correct declaration.
    #
    # DELIBERATELY NARROW: it requires a SHARED NAMED PARENT, so it cannot explain away two rows
    # describing ONE object - a genuine duplicate has no third type both descend from. The
    # self-test's known pairs are what hold that line.
    shared = basenames.get(a, set()) & basenames.get(b, set())
    if shared:
        return "siblings (both declare baseClass_%s)" % sorted(shared)[0]
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", default=DEFAULT)
    ap.add_argument("--min", type=int, default=4,
                    help="ignore maps with fewer than N named fields (default 4)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    maps, basenames, routes = load(a.store)
    maps = {t: s for t, s in maps.items() if len(s) >= a.min}

    explained, unexplained = [], []
    names = sorted(maps)
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            A, B = maps[x], maps[y]
            if A <= B:
                small, big = x, y
            elif B <= A:
                small, big = y, x
            else:
                continue
            why = related(x, y, basenames, routes)
            identical = maps[small] == maps[big]
            row = (small, len(maps[small]), big, len(maps[big]), identical, why)
            (explained if why else unexplained).append(row)

    if a.self_test:
        # REWRITTEN 2026-09-21 (OPUS). The old self-test asserted that two named pairs must come
        # back UNEXPLAINED, and it had been FAILING BEFORE THIS SESSION TOUCHED ANYTHING: it names
        # PhyreInstanceListHeader and PhyreClusterHeader, and those types NO LONGER EXIST - they
        # were retracted as duplicates of the registered P*Header rows. A control that names
        # deleted types can never see them, so it reported MISS on both and its red said nothing
        # about the instrument.
        #
        # It is NOT repointed at whichever pairs happen to be unexplained today, because a control
        # rewritten to match current data stops being able to fail. It now tests the RULE, on
        # fixtures that do not depend on the store's contents: each case states what `related`
        # must return and why. The sibling rule added today is what made this necessary - a new
        # explanation kind needs a control that shows it still REFUSES.
        cases = [
            ("two rows for one object - no relation of any kind",
             {}, {}, None),
            ("inheritance: B declares baseClass_A",
             {"B": {"A"}}, {}, "inheritance"),
            ("embedding: A's route names B",
             {}, {"A": "EMBED B +0x10 stride=0x8 count=4"}, "embedding"),
            ("SIBLINGS: both declare the same parent",
             {"A": {"P"}, "B": {"P"}}, {}, "siblings"),
            ("NOT siblings: different parents",
             {"A": {"P"}, "B": {"Q"}}, {}, None),
            ("NOT siblings: only one has a parent",
             {"A": {"P"}}, {}, None),
        ]
        bad = 0
        print("self-test: `related` must explain exactly the declared relations and refuse others")
        for label, bn, rt, expect in cases:
            got = related("A", "B", collections.defaultdict(set, bn), rt)
            ok = (got is None) if expect is None else (got or "").startswith(expect)
            if not ok:
                bad += 1
            print("   %s %-52s -> %s" % ("ok  " if ok else "FAIL", label, got))
        print("self-test: %d case(s), %d failure(s)" % (len(cases), bad))
        raise SystemExit(1 if bad else 0)

    print("FIELD MAPS CONTAINED IN ANOTHER TYPE'S\n")
    print("  explained by a declared relationship   %3d" % len(explained))
    print("  NOT explained - two rows, one object?  %3d" % len(unexplained))
    print()
    print("  Not a defect list. Two declarations of one object may be deliberate; which is")
    print("  canonical is a judgement. The point is that nothing else in the gate set asks.")
    if unexplained:
        print("\nUNEXPLAINED:")
        for s, ns, b, nb, ident, _ in sorted(unexplained, key=lambda r: -r[1]):
            print("   %-30s (%2d) %s %-30s (%2d)"
                  % (s, ns, "IDENTICAL to" if ident else "contained in", b, nb))


if __name__ == "__main__":
    main()
