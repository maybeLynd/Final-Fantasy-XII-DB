#!/usr/bin/env python3
"""Census displacements a type's store rows do not cover, and whether the gap file already knows them.

A field row covers [offset, offset+size). A displacement the census records that falls in no row is
a field the store does not declare - unless it is INSIDE a declared multi-byte field, which is the
ordinary case for a lane of a vec4 and not a gap at all.

WHAT IT FOUND, 2026-09-16 (OPUS), over five censuses: the store is ESSENTIALLY COMPLETE against them.
CharacterRenderObject 63/63 covered, CharacterRenderSystemTail 24/24, MovementContext 58/58,
SecondaryContext 2 uncovered, CharacterRenderRecord 4, SpawnRecord 8. And NONE of the fourteen is
cleanly declarable, which is the useful half:

  * CharacterRenderRecord's four are three `lea` address-takings - no width evidence at all - and one
    artefact, `lea eax, [rdx - 1]`, which is arithmetic the census resolved to an offset.
  * SpawnRecord's six 16-byte ones are ONE function, Spawn_SelectContinuousEntry (00235360), writing
    `movups` through an advancing `rcx` from +0x00 to +0xB0. That is a block initialisation, not
    sixteen-byte fields, and the store's own rows already reject that inference twice (+0x120's
    `movups` over four slots, +0x414's). It is also one function against a two-function bar.
  * SpawnRecord's +0x108 has two writers of DIFFERENT widths - a byte at 0030C4B1 and a word at
    00327D57 - reached as `[rdi + rdx*4 + 0x88]`, so an element of a stride-4 array rather than a
    scalar. +0x10A is its neighbour and has one writer.

So a run that reports uncovered displacements is a reading list, and the right answer to most of it
is "do not declare this". The counts are the result; declaring from them would be the error.

usage: uncovered_disps.py <TypeName> <census.tsv> [--base 0x48800]

--base is for a census whose `disp` is object-relative while its instructions carry an absolute
displacement (the render-system tail, +0x18 vs 0x48818). Passing it when the store rows are ALSO
object-relative reports every row as uncovered, which is what happened on the first run here.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA")
STORE = os.path.join(DB, "_types", "fields.tsv")
GAPS = os.path.join(DB, "_types", "recoverable-layout-gaps.tsv")

type_ = sys.argv[1]
census = sys.argv[2]
base = int(sys.argv[sys.argv.index("--base") + 1], 16) if "--base" in sys.argv else 0

spans = []
for line in io.open(STORE, encoding="utf-8").read().splitlines()[1:]:
    c = line.rstrip("\r").split("\t")
    if len(c) > 3 and c[0] == type_:
        try:
            spans.append((int(c[1], 16), int(c[2]), c[3]))
        except ValueError:
            pass
spans.sort()

known = set()
if os.path.exists(GAPS):
    for line in io.open(GAPS, encoding="utf-8", errors="replace").read().splitlines()[1:]:
        c = line.split("\t")
        if len(c) > 1 and c[0] == type_:
            try:
                known.add(int(c[1], 16))
            except ValueError:
                pass

rows = [l.rstrip("\r").split("\t") for l in io.open(census, encoding="utf-8",
                                                    errors="replace").read().splitlines()]
head = rows[0]
di, ii = head.index("disp"), (head.index("instruction") if "instruction" in head else None)
seen = {}
for r in rows[1:]:
    if len(r) <= di:
        continue
    try:
        d = int(r[di], 16) + base
    except ValueError:
        continue
    seen.setdefault(d, r[ii] if ii is not None and len(r) > ii else "")


def covering(d):
    for off, size, name in spans:
        if off <= d < off + max(size, 1):
            return off, size, name
    return None


uncovered, inside = [], 0
for d in sorted(seen):
    cov = covering(d)
    if cov is None:
        uncovered.append(d)
    elif cov[0] != d:
        inside += 1

print("%s: %d store row(s), %d census displacement(s)" % (type_, len(spans), len(seen)))
print("  inside a declared multi-byte field (not a gap): %d" % inside)
print("  covered by no row at all                      : %d" % len(uncovered))
if known:
    print("  of those, already in recoverable-layout-gaps  : %d"
          % sum(1 for d in uncovered if d in known))
print()
for d in uncovered:
    print("   +0x%03X  %-6s %s" % (d, "KNOWN" if d in known else "NEW", seen[d][:76]))
