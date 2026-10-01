#!/usr/bin/env python3
"""check_unread_vs_census.py - a span that says "no censused access" while its census has one.

**THE ROW MAKES A CHECKABLE CLAIM AND NOTHING CHECKED IT.** Hundreds of field rows carry the
boilerplate *"declared gap span - inside the record by extent, no censused access"*. That is a
statement about a specific artefact: the type's access census. When the census exists, the claim can
simply be tested, and where it fails the row is wrong in the most correctable way a row can be -
the evidence is already on disk and merely unread.

The check was not worth writing when 20 types had a census. It is now: the map reaches **48**, and
13 of those are `EMBED` children projected out of their parents, whose displacements no scan had
ever attributed to the child before.

METHOD. For every type in `check_census_widths.py`'s map, take every field row whose NAME marks it
unread (`unobserved*`, `unknown*`, `unread*`, `pad*`) and ask whether the census holds any access at
a displacement inside `[offset, offset+size)`. A hit is reported with the instructions, because the
instruction is what makes it actionable - a `lea` is an address taken and says little, while a
`mov dword` is a field.

WHAT A HIT IS NOT. It is not automatically a defect in the row. A census can attribute an access to
the wrong displacement - `indexed at zero displacement` is a known class in this kit, where
`[rcx + rax*8]` is filed at `+0x000` - and a projected census inherits whatever its parent got
wrong. So hits are printed with their instruction text and NOT counted as errors; the reader
decides, which is the same rule every other instrument here follows.

    python check_unread_vs_census.py
"""
import argparse
import collections
import csv
import glob
import io
import os
import re
import sys

import kit_paths as KP

UNREAD = re.compile(r"^(unobserved|unknown|unread|pad)", re.I)
CLAIM = re.compile(r"no censused access", re.I)


def census_map():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_census_widths.py")
    t = io.open(p, encoding="utf-8").read()
    return dict(re.findall(r'\n    "([A-Za-z0-9_]+)":\s*"([^"]+-accesses\.tsv)"', t))


def find(name):
    hits = glob.glob(os.path.join(KP.DB, "**", name), recursive=True)
    return hits[0] if hits else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-only", action="store_true",
                    help="only rows whose meaning actually says 'no censused access'")
    a = ap.parse_args()

    cmap = census_map()
    fields = collections.defaultdict(list)
    with io.open(os.path.join(KP.DB, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9 or not f[0]:
                continue
            try:
                fields[f[0]].append((int(f[1], 0), int(f[2], 0), f[3], f[5], f[8]))
            except ValueError:
                pass

    total_spans = checked = hits = 0
    out = []
    for tname, fname in sorted(cmap.items()):
        path = find(fname)
        if not path:
            continue
        acc = collections.defaultdict(list)
        with io.open(path, encoding="utf-8", newline="") as fh:
            rr = csv.reader(fh, delimiter="\t")
            next(rr, None)
            for row in rr:
                if len(row) < 6:
                    continue
                try:
                    acc[int(row[3], 0)].append((row[2], row[4], row[5]))
                except ValueError:
                    pass
        for off, size, name, meaning, evidence in sorted(fields.get(tname, [])):
            if not UNREAD.match(name or ""):
                continue
            if a.claim_only and not CLAIM.search(meaning or ""):
                continue
            total_spans += 1
            checked += 1
            found = []
            for d in range(off, off + size):
                for site, kind, txt in acc.get(d, []):
                    found.append((d, site, kind, txt))
            if found:
                hits += 1
                out.append((tname, off, size, name, found))

    # SECOND PASS, a different artifact: the name marks the row unread while the row's
    # own EVIDENCE records accesses. The census-file pass above sees only the 74 types in
    # the map; this one reads the store itself, so it catches types whose accesses were
    # found by a run no TSV covers (found 2026-09-28: BootSingleton01F7F598 +0xCF0/+0xDA8
    # and PApplication +0x001D/+0x0D50 all carried "no censused access no longer holds"
    # under unobserved* names - renamed that day).
    POSITIVE = re.compile(
        r"FOR THIS SPAN\s*:\s*(?:[1-9]\d*\s*displacement|\+0x)|"
        r"'no censused access' no longer holds|still records accesses under",
        re.I)
    stale = []
    for tname, rows in fields.items():
        for off, size, name, meaning, evidence in rows:
            if UNREAD.match(name or "") and POSITIVE.search(evidence or ""):
                stale.append((tname, off, size, name))

    print("types with a census in the map : %d" % len(cmap))
    print("unread spans in those types    : %d" % checked)
    print("spans WITH a censused access   : %d" % hits)
    print("unread-named rows whose OWN evidence records accesses : %d" % len(stale))
    print()
    for tname, off, size, name, found in sorted(out, key=lambda x: -len(x[4])):
        print("  %-30s +0x%-5X %-3d %-24s %d access(es)" % (tname[:30], off, size, name[:24], len(found)))
        seen = set()
        for d, site, kind, txt in found[:4]:
            k = (d, txt)
            if k in seen:
                continue
            seen.add(k)
            print("        +0x%-5X %s %-4s %s" % (d, site, kind, txt[:64]))
    print()
    for tname, off, size, name in sorted(stale):
        print("  STALE-NAME  %-30s +0x%-5X %-3d %s" % (tname[:30], off, size, name[:30]))
    print("A HIT IS NOT AUTOMATICALLY A DEFECT. A census can file an access at the wrong")
    print("displacement -- `indexed at zero displacement` is a known class here -- and a projected")
    print("census inherits its parent's mistakes. The instruction text is printed so the reader can")
    print("tell a `lea` from a `mov dword`; nothing is counted as an error.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
