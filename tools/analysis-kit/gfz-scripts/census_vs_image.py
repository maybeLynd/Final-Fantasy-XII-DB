#!/usr/bin/env python3
"""Compare a field-access census against an image-wide sweep, displacement by displacement.

WHY. A census is built from a function list, so it can only report accesses inside the functions it
was given. On 2026-09-15 the render-record tail census was NINE sites short, and seven of them
belonged to one function - FUN_00429140, the pending-list remover, a whole piece of the pool's
lifecycle that no page described because no census seed reached it. The census was right about what
it enumerated and wrong as a count of writers, and nothing distinguished those two readings.

THE TWO DIRECTIONS ARE NOT SYMMETRIC.

  in the census, not in the image   A REAL PROBLEM: a wrong address, or a site the linear sweep
                                    cannot decode. Always reported.
  in the image, not in the census   A CANDIDATE, and mostly noise: a displacement sweep cannot tell
                                    one type from another, so most of a surplus is other types
                                    sharing the offset. Reported only with --near, whose prefixes
                                    say which addresses belong to this type's own code. Without it
                                    the number is meaningless and is not printed - at displacement
                                    0x0 the image has 97,051 operands and every one of them is
                                    somebody else's.

THE PRECONDITION, checked rather than assumed. This compares by DISPLACEMENT, so a census row is
only comparable when its `disp` column is the displacement its instruction literally encodes. Some
censuses track a base pointer and record the RESOLVED field offset instead:
character-render-record-accesses.tsv files `movss dword ptr [rdx + 4]` under `disp` 0x184, because
rdx already points into the record. Those rows are EXCLUDED and counted, because a literal sweep
cannot see them - and a tolerance would be worse than useless here, since the excluded rows are
exactly the ones that would generate false differences in both directions.

usage: census_vs_image.py <census.tsv> [--base 0x48800] [--near 002E,0025B]
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from disp_image_census import census, EXE_DEFAULT  # noqa: E402

path = sys.argv[1]
base = int(sys.argv[sys.argv.index("--base") + 1], 16) if "--base" in sys.argv else 0
near = sys.argv[sys.argv.index("--near") + 1].split(",") if "--near" in sys.argv else []

rows = [l.rstrip("\r").split("\t") for l in io.open(path, encoding="utf-8").read().splitlines()]
head = rows[0]
ci = {n: head.index(n) for n in ("function", "site", "disp") if n in head}
if len(ci) < 3:
    sys.exit("expected function/site/disp columns, got: %s" % head)
ii = head.index("instruction") if "instruction" in head else None
LIT = re.compile(r"\[[^\]]*?(?:\+\s*(0x[0-9A-Fa-f]+|\d+))?\]")


def literal_disp(text):
    """The displacement the instruction encodes, or None when there is no memory operand."""
    m = LIT.search(text)
    if not m:
        return None
    g = m.group(1)
    if g is None:
        return 0
    return int(g, 16) if g.lower().startswith("0x") else int(g)


by_disp, excluded, nomem = {}, 0, 0
for r in rows[1:]:
    if len(r) <= max(ci.values()):
        continue
    d = int(r[ci["disp"]], 16)
    if ii is not None and len(r) > ii:
        got = literal_disp(r[ii])
        if got is None:
            nomem += 1
            continue
        if got != d + base:  # --base is part of the census's own convention, so apply it first
            excluded += 1
            continue
    by_disp.setdefault(d + base, set()).add(r[ci["site"]].upper())

print("%s: %d comparable displacement(s), %d site(s)"
      % (os.path.basename(path), len(by_disp), sum(len(v) for v in by_disp.values())))
if excluded or nomem:
    print("   EXCLUDED %d row(s) whose `disp` is a resolved offset rather than the encoded one%s"
          % (excluded, ", %d with no memory operand" % nomem if nomem else ""))
if not by_disp:
    sys.exit("nothing comparable in this census - its `disp` is not a literal displacement")

img, decoded, resyncs = census(EXE_DEFAULT, sorted(by_disp))
print("one sweep: %d instruction(s) decoded, %d resync(s)\n" % (decoded, resyncs))

census_only_total = flagged_total = 0
for d in sorted(by_disp):
    cen = by_disp[d]
    im = {"%08X" % a for a, _k, _m, _o, _b in img[d]}
    only_census = sorted(cen - im)
    flagged = sorted(a for a in (im - cen)
                     if any(a.startswith(p.upper()) for p in near)) if near else []
    if not only_census and not flagged:
        continue
    print("disp 0x%x  census %d, image %d" % (d, len(cen), len(im)))
    if only_census:
        census_only_total += len(only_census)
        print("   IN THE CENSUS, NOT IN THE SWEEP (read these): %s" % " ".join(only_census))
    if flagged:
        flagged_total += len(flagged)
        print("   in the image, not in the census, within --near: %s" % " ".join(flagged[:14]))

print("\n%d census site(s) the sweep cannot see" % census_only_total)
if near:
    print("%d image site(s) the census lacks, within the --near prefixes" % flagged_total)
else:
    print("(pass --near <prefixes> to see what the image has and the census does not)")
