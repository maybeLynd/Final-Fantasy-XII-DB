#!/usr/bin/env python3
"""Which declared types are touched by the SAME instructions at the SAME offsets?

THE BLIND SPOT THIS CLOSES. find_duplicate_shapes.py compares offset, size and NAME, which is
deliberate - offset-and-size agreement alone matches any two structs that begin with a pointer
and two dwords. But it therefore cannot see the case it was written to worry about: one
structure declared twice, whose fields two readers named differently. Names are the one piece of
evidence a second reader is guaranteed not to reproduce.

SO ASK THE CODE INSTEAD OF THE NAMES. If instruction `0051FA21` is recorded against type A at
+0x20 and against type B at +0x20, that one instruction is reaching both objects at the same
offset. It cannot be doing that to two different structures - either they are the same type, or
one begins with the other. Site identity is evidence; a name is an opinion.

TWO WAYS THIS GOES WRONG, and both are handled rather than hoped about:

  * GENERIC HELPERS. A memset thunk or a null-test touches everything at +0x0. Any site recorded
    against more than MAX_TYPES_PER_SITE types is dropped before matching - it is a utility, not
    a structural fact.
  * A SINGLE COINCIDENCE. One shared site at one displacement proves very little. A pair must
    share at least MIN_PAIRS site/displacement pairs across at least MIN_DISPS DISTINCT
    displacements, so the overlap has to have shape rather than volume.

WHAT A HIT IS NOT. Types related by embedding at offset 0 will match, correctly and by design -
a widget and the object whose first bytes are that widget genuinely are touched by the same
instructions. That is the same finding stated positively, and the output says which are already
declared as related so the reader is not asked to re-derive it.

CONTROLS, both required or the output is refused:
  * POSITIVE - RenderResourceEntryBank and RenderStrideC0Bank must group: the whole 0x60 bank
    descriptor is written by the shared 0051F9F0, so their artifacts share many sites.
  * NEGATIVE - a pair drawn from unrelated categories must NOT appear. The store's own
    ImageAddressArenaRecord and SaveImageHeader are used, because nothing reaches both.
"""
import collections
import csv
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import census_artifacts as CA  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
MAX_TYPES_PER_SITE = 8
MIN_PAIRS = 8
MIN_DISPS = 5
CONTROL_POS = ("RenderResourceEntryBank", "RenderStrideC0Bank")
CONTROL_NEG = ("ImageAddressArenaRecord", "SaveImageHeader")


def load_access():
    """type -> set of (site, displacement), plus artifacts that could not be attributed.

    THE ATTRIBUTION IS census_artifacts.load AND NOT A LEADING `#` COMMENT. The first version of
    this tool used the comment, which only 8 of 71 artifacts carry, so it ran over 11 % of its
    input while reporting both controls as passing - the negative control's types were simply
    never loaded. An absence of data is not an absence.
    """
    by_type, unresolved = CA.load()
    out = collections.defaultdict(set)
    for t, rows in by_type.items():
        for r in rows:
            site = (r.get("site") or "").strip()
            try:
                d = int(r["disp"], 16)
            except (ValueError, TypeError, KeyError):
                continue
            if site:
                out[t].add((site, d))
    return out, unresolved


def declared_relations():
    """Pairs the store already links, so a hit can say `already declared` instead of `new`."""
    rel = set()
    for r in csv.DictReader(io.open(D + "types.tsv", encoding="utf-8"), delimiter="\t"):
        for m in re.finditer(r"\b(?:EMBED|PARRAY|ARRAY)\s+(\w+)", r.get("route") or ""):
            rel.add(frozenset((r["type"], m.group(1))))
    for r in csv.DictReader(io.open(D + "fields.tsv", encoding="utf-8"), delimiter="\t"):
        ct = re.sub(r"[\[\]0-9*]+$", "", (r.get("ctype") or "").strip())
        if ct:
            rel.add(frozenset((r["type"], ct)))
    return rel


def main():
    acc, unresolved = load_access()
    owners = collections.defaultdict(set)
    for t, pairs in acc.items():
        for site, _d in pairs:
            owners[site].add(t)
    generic = {s for s, ts in owners.items() if len(ts) > MAX_TYPES_PER_SITE}

    kept = {t: {(s, d) for s, d in pairs if s not in generic} for t, pairs in acc.items()}
    types = sorted(kept)
    rel = declared_relations()

    groups = []
    for i, a in enumerate(types):
        for b in types[i + 1:]:
            shared = kept[a] & kept[b]
            if len(shared) < MIN_PAIRS:
                continue
            disps = {d for _s, d in shared}
            if len(disps) < MIN_DISPS:
                continue
            groups.append((len(shared), len(disps), a, b,
                           frozenset((a, b)) in rel, sorted(disps)))

    def has(pair):
        return any({a, b} == set(pair) for _n, _nd, a, b, _r, _ds in groups)

    ok_pos, ok_neg = has(CONTROL_POS), not has(CONTROL_NEG)
    print("CONTROL positive  %s / %s -> grouped   %s"
          % (CONTROL_POS[0], CONTROL_POS[1], "PASS" if ok_pos else "FAIL"))
    print("CONTROL negative  %s / %s -> absent    %s"
          % (CONTROL_NEG[0], CONTROL_NEG[1], "PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  both controls pass - the absences below are meaningful")
    print("  " + CA.coverage_line(acc, unresolved))
    print("  (%d site(s) dropped as generic helpers, each recorded against more than %d types)\n"
          % (len(generic), MAX_TYPES_PER_SITE))

    print("TYPE PAIRS SHARING >= %d SITE/OFFSET PAIRS OVER >= %d DISTINCT OFFSETS: %d"
          % (MIN_PAIRS, MIN_DISPS, len(groups)))
    for n, nd, a, b, declared, disps in sorted(groups, reverse=True):
        print("\n  %-34s %-34s %3d pair(s), %d offset(s)  %s"
              % (a, b, n, nd, "ALREADY DECLARED RELATED" if declared else "<== NOT DECLARED"))
        print("      offsets: %s%s"
              % (" ".join("+0x%X" % d for d in disps[:14]),
                 " ..." if len(disps) > 14 else ""))
    print("\nA pair here is touched by the same instructions at the same offsets. Either it is")
    print("one structure, or one type begins with the other. `ALREADY DECLARED RELATED` means")
    print("the store says so through a route or a ctype; `NOT DECLARED` means it does not.")


if __name__ == "__main__":
    sys.exit(main() or 0)
