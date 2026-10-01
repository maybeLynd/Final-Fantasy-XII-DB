#!/usr/bin/env python3
"""Functions NAMED for a type that its own access census does not contain.

The sharpest version of "a census is only as wide as its function list", and the one with no
heuristic in it. If the function list carries CharacterRenderRecord_UpdateRootDistanceFade and the
CharacterRenderRecord census does not, that is not a coincidence of shared offsets and not a
judgement about relevance - somebody named that function after the type, and the census that claims
to enumerate the type's accesses has never looked inside it.

Written 2026-09-15, after three rows in one day turned out to rest on a census whose function list
was missing the function that settled them: FUN_003EC260 stores the render record's rotation triple
and resolved a type conflict the store had held since 2026-09-14.

IT REPORTS, IT DOES NOT CONCLUDE. A named function may legitimately touch none of the type's fields
- it may take one by pointer and pass it straight on - and a census would be right to be silent
about it. What it may not be is UNCONSIDERED.

PAIRS ARE EXPLICIT, AND THAT IS DELIBERATE. The first version guessed each census's type prefix from
the named functions it already contained, and the guesses were wrong often enough to be worthless:
it paired save-payload-accesses.tsv with BattleStats (the payload EMBEDS battle stats, it is not
that type) and actor-manager-record-accesses.tsv with ScriptVM, then reported a confident total of
370 across both the sound and the mis-paired. --scan still offers the guesses, clearly marked, as a
place to start; a guessed pairing is not a result and its numbers are not to be quoted.

usage: census_named_gaps.py <census.tsv> <TypePrefix> [<census.tsv> <TypePrefix> ...]
       census_named_gaps.py --scan          (guesses pairs; every one needs confirming)
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

funcs = {}
for line in io.open(FUNCS, encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    if len(c) > 2:
        funcs[c[0].upper()] = c[1]


def census_functions(path):
    out = set()
    for line in io.open(path, encoding="utf-8", errors="replace").read().splitlines()[1:]:
        c = line.split("\t")
        if c and re.fullmatch(r"[0-9A-Fa-f]{8}", c[0].strip()):
            out.add(c[0].strip().upper())
    return out


def report(path, prefix, guessed=False):
    cen = census_functions(path)
    if not cen:
        print("%s: no function column to read" % path)
        return 0
    named = [(a, n) for a, n in funcs.items() if n.startswith(prefix + "_")]
    missing = sorted((a, n) for a, n in named if a not in cen)
    rel = os.path.relpath(path, DB).replace("\\", "/")
    print("%s\n   %s%s_*: %d so named, %d in the census, %d MISSING"
          % (rel, "GUESSED PREFIX (confirm before quoting) " if guessed else "", prefix,
             len(named), len(named) - len(missing), len(missing)))
    for a, n in missing:
        print("      %s %s" % (a, n))
    return len(missing)


args = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--scan" in sys.argv:
    print("GUESSED PAIRINGS. The prefix is taken from whichever named functions the census already")
    print("contains, which is the census's testimony about itself and is often wrong. Confirm each")
    print("pairing against what the census is actually a census OF before using any number here.\n")
    for root, _dirs, files in os.walk(DB):
        for fn in sorted(files):
            if not fn.endswith("-accesses.tsv"):
                continue
            p = os.path.join(root, fn)
            stems = {}
            for a in census_functions(p):
                n = funcs.get(a, "")
                if "_" in n and not n.startswith("FUN_"):
                    stems[n.split("_")[0]] = stems.get(n.split("_")[0], 0) + 1
            if stems:
                report(p, max(stems, key=stems.get), guessed=True)
elif len(args) >= 2:
    total = 0
    for path, prefix in zip(args[0::2], args[1::2]):
        total += report(path, prefix)
    print("\n%d named function(s) absent from the census of their own type" % total)
else:
    raise SystemExit(__doc__)
