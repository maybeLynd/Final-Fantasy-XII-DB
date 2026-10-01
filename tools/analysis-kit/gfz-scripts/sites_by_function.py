#!/usr/bin/env python3
"""Map an image-wide displacement census onto the function list: which functions, and how many.

A store row that says "across N distinct functions" is a claim about the image, not about a census,
so it should be counted from the image. usage: sites_by_function.py <disp_hex> [<disp_hex> ...]
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from disp_image_census import census, EXE_DEFAULT  # noqa: E402

FUNCS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "..", "work", "graph", "functions.tsv"))
funcs = []
for line in io.open(FUNCS, encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    if len(c) > 2 and c[2].isdigit():
        funcs.append((int(c[0], 16), int(c[2]), c[1]))
funcs.sort()


def owner(va):
    lo, hi = 0, len(funcs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        a, n, nm = funcs[mid]
        if va < a:
            hi = mid - 1
        elif va >= a + n:
            lo = mid + 1
        else:
            return "%08X %s" % (a, nm)
    return "(no listed function)"


disps = [int(a, 16) for a in sys.argv[1:] if not a.startswith("--")]
img, decoded, resyncs = census(EXE_DEFAULT, disps)
print("one sweep: %d instruction(s), %d resync(s)\n" % (decoded, resyncs))
for d in disps:
    seen = {}
    for a, kind, _m, _o, _b in img[d]:
        seen.setdefault(owner(a), []).append("%08X%s" % (a, kind))
    print("disp 0x%x: %d site(s) in %d distinct function(s)" % (d, len(img[d]), len(seen)))
    for f in sorted(seen):
        print("   %-52s %s" % (f, " ".join(sorted(seen[f]))))
    print()
