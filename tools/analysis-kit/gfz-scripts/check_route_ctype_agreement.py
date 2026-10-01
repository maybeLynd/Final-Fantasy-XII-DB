#!/usr/bin/env python3
"""check_route_ctype_agreement.py - the route column and the ctype column, made to answer together.

WHY THIS EXISTS, and it comes from a false negative rather than a theory.
`check_prose_only_edges.py` finds pointer fields whose target is named in PROSE but not in the
ctype. It reads meanings, so it inherits everything wrong with reading meanings: on 2026-09-20 it
reported `ActorStorageRecord +0xA0` and `+0xA8` as edges to `ActorManagerSlot`, having matched that
name inside a CORRECTED clause that exists precisely to say the citation was REMOVED. It matched a
withdrawal as though it were an assertion. Meanwhile the real edge at `+0xA8` - to `ActorWaitSlot` -
was sitting one column away in a machine-readable form, and was not reported at all.

THE STORE ALREADY STATES THESE EDGES WITHOUT PROSE. A child type whose route is
`CHAIN Parent +0xOFF` is asserting that the parent's field at OFF HOLDS A POINTER to it. `EMBED
Parent +0xOFF` asserts the child sits INLINE there. Either way the parent's field row at that offset
is talking about the same bytes, and the two columns should agree. Where the field's ctype is
anonymous - `void*`, a bare integer, an untyped blob or empty - the edge exists in the route column
and NOT in the pointer graph, so a census generator, a gate or a reconstruction cannot follow it.
That is the same unusable-knowledge failure, found by crossing two structured columns instead of
grepping English.

WHAT THIS REPORTS, in three buckets that want different actions:
  1. ANONYMOUS ctype    - the route asserts the edge and the ctype does not carry it. Writing the
                          ctype asserts nothing new; it makes an existing claim machine-readable.
  2. NON-TYPE spelling  - the ctype is an explicit dead end (a sized byte blob, `UNRESOLVED`)
                          where a type is declared. Read before touching: `uint8[560]` over a
                          declared 0x230 type is a spelling to fix, but a union arm is NOT.
  2b. DIFFERENT type    - the ctype names some other declared type. Always read this one.
  3. no field row       - the parent has no row at the offset its child's route names. That is a
                          layout question, not a spelling one.

WHAT IT DOES NOT DO. It writes nothing, and it does not treat a disagreement as an error. A field
may legitimately stay anonymous: `BattleStatsRecord +0x88` is a union discriminated by `+0x05` whose
kind-0 arm is a `GambitConfig`, and writing `GambitConfig` there would promote one arm to the whole
field. A parent offset claimed by TWO children with identical routes must not be typed as either
until the duplicate is resolved - `ActorStorageRecord +0xA8`, claimed by both `ActorWaitSlot` and
`VmResultEntry`, is that case. Both are reported and both are for a person to judge.

IT ALSO COVERS WHAT check_route_collisions.py CANNOT. That checker populates only from routes with a
literal base/stride/count, so it is structurally blind to CHAIN and EMBED - which is exactly where a
parent-relative duplicate lives. Two children claiming one parent offset are reported here.

Exit 1 when anything is reported, so a new disagreement is visible; the accepted state belongs in
the gate baseline, not in a threshold here.
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.join("Database", "FFXII TZA")
TYPES = os.path.join(ROOT, "_types", "types.tsv")
FIELDS = os.path.join(ROOT, "_types", "fields.tsv")

# Carries no type identity AND no explicit shape: the field is simply untyped.
ANON = re.compile(r"""^(?:
      void\s*\*
    | u?int(?:8|16|32|64)(?:_t)?\s*\*?
    | u(?:8|16|32|64)
    | q?word | dword | ptr |
)$""", re.IGNORECASE | re.VERBOSE)

# An explicit NON-type where one is declared: a sized byte blob, or a stated dead end.
# Separate bucket because the action differs - a blob spanning exactly the child's size is a
# spelling to fix, while `UNRESOLVED` on a union arm is a decision to leave alone.
BLOB = re.compile(r"^(?:u?int(?:8|16|32|64)?\[\d+\]|u\d+\[\d+\]|UNRESOLVED)$", re.IGNORECASE)

ROUTE = re.compile(r"\b(CHAIN|EMBED)\s+(\w+)\s*\+\s*(0x[0-9A-Fa-f]+|\d+)")


def load(path):
    rows = [l.rstrip("\n").split("\t") for l in io.open(path, encoding="utf-8")
            if l.strip() and not l.startswith("#")]
    head = {n: i for i, n in enumerate(rows[0])}
    width = max(head.values())
    return head, [r for r in rows[1:] if len(r) > width]


def num(text):
    text = (text or "").strip()
    try:
        return int(text, 16) if text.lower().startswith("0x") else int(text)
    except ValueError:
        return None


def main():
    if not os.path.exists(TYPES):
        sys.stderr.write("run me from the repository root (%s not found)\n" % TYPES)
        return 2
    th, types = load(TYPES)
    fh, fields = load(FIELDS)

    declared = {r[0]: r for r in types}
    sizes = {r[0]: num(r[1]) for r in types}
    # A tagged union declares several rows at one offset (the second and later open with `OVERLAY `, which
    # types_index honours). Keying one row per offset let the last occupant hide the first, so a route to the
    # first occupant read as a disagreement (OPUS, 2026-09-28, the AB30 union; FABLE rule-0 ruling 5604b7413).
    allrows = collections.defaultdict(list)
    for r in fields:
        off = num(r[1])
        if off is not None:
            allrows[(r[0], off)].append(r)
    frows = {k: (next((x for x in v if not x[fh["meaning"]].startswith("OVERLAY ")), v[0])) for k, v in allrows.items()}

    buckets = collections.defaultdict(list)
    claimants = collections.defaultdict(list)

    for r in types:
        child = r[0]
        for alt in r[th["route"]].split(" | "):
            m = ROUTE.search(alt.strip())
            if not m:
                continue
            verb, parent, off = m.group(1), m.group(2), num(m.group(3))
            if parent not in declared or off is None:
                continue
            claimants[(parent, off)].append((child, verb))
            fr = frows.get((parent, off))
            # the route may name a later occupant of a union: match against the occupant whose ctype names the child
            for x in allrows.get((parent, off), []):
                if re.sub(r"\s+", "", x[fh["ctype"]]).startswith(child):
                    fr = x
            if fr is None:
                buckets["no field row at that offset"].append(
                    (parent, off, verb, child, "-"))
                continue
            ct = fr[fh["ctype"]].strip()
            # Whitespace-tolerant: the store writes 'T*' 362 times and 'T *' 3 times, and a
            # checker that reads only the majority spelling reports correct rows as mismatches.
            # Found 2026-09-20 when two freshly-written, correct CHAIN edges were flagged
            # 'DIFFERENT type' purely for the space before the asterisk.
            ct_n = re.sub(r"\s+", "", ct)
            if ct_n == child or ct_n == child + "*" or re.match(r"^%s(\*|\[)" % re.escape(child), ct_n):
                continue
            detail = "%s / ctype=%r" % (fr[fh["name"]], ct)
            extra = ""
            if sizes.get(child) and num(fr[2]) == sizes[child]:
                extra = "  <- spans exactly the child's %d bytes" % sizes[child]
            if ANON.match(ct) or ct == "":
                buckets["ANONYMOUS ctype"].append((parent, off, verb, child, detail + extra))
            elif BLOB.match(ct):
                buckets["ctype spells a NON-TYPE where one is declared"].append(
                    (parent, off, verb, child, detail + extra))
            else:
                buckets["ctype names a DIFFERENT type"].append(
                    (parent, off, verb, child, detail + extra))

    dupes = {k: v for k, v in claimants.items() if len(v) > 1}

    print("CHAIN/EMBED routes crossed against the parent's field ctype")
    print("declared types: %d   parent offsets claimed by a route: %d\n"
          % (len(declared), len(claimants)))

    total = 0
    for name in ("ANONYMOUS ctype", "ctype spells a NON-TYPE where one is declared",
                 "ctype names a DIFFERENT type", "no field row at that offset"):
        rows = sorted(buckets.get(name, []))
        total += len(rows)
        print("%s : %d" % (name, len(rows)))
        for parent, off, verb, child, detail in rows:
            print("    %-32s +0x%-5X %-5s -> %-30s %s" % (parent, off, verb, child, detail))
        print()

    print("parent offsets claimed by MORE THAN ONE child : %d" % len(dupes))
    for (parent, off), who in sorted(dupes.items()):
        print("    %-32s +0x%-5X <- %s" % (parent, off,
              ", ".join("%s (%s)" % (c, v) for c, v in sorted(who))))
    print()

    print("A route is the store asserting an edge in a machine-readable column. Where the")
    print("ctype does not carry it, the claim is present and unusable. NOTHING IS WRITTEN")
    print("here: a union arm, a duplicate claimant and a deliberate blob are all legitimate")
    print("reasons for a ctype to stay anonymous, and only a person can tell them apart.")

    return 1 if (total or dupes) else 0


if __name__ == "__main__":
    sys.exit(main())
