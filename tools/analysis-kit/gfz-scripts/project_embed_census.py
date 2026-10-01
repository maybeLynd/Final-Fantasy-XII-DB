#!/usr/bin/env python3
"""project_embed_census.py - a child's census, projected out of its parent's.

`EMBED` is the largest group of game-side types with no census: 21 of them. **None needs a new
scan.** A child embedded at `Parent +0xOFF` occupies bytes the parent's census already records, at
parent-relative displacements; the child's census is those rows with `OFF` subtracted. Building a
scanner for them would re-derive evidence the corpus already holds.

    EMBED Parent +0xOFF                     child at parent + OFF, one instance
    EMBED Parent +0xOFF stride=0xS count=N  element i at parent + OFF + i*S

so a parent row at displacement `d` belongs to the child when `OFF <= d < OFF + N*S`, and its
child-relative displacement is `(d - OFF) % S`.

**THIS INVENTS NOTHING, AND THAT IS THE POINT.** Every emitted row is a parent row with one
subtraction applied; no instruction is decoded, no register is tracked, no heuristic is used. The
failure modes are correspondingly narrow and are checked rather than assumed:

  * the parent must itself have a census, or there is nothing to project;
  * the child's span must fit inside the parent's declared size - `check_storage_class.py` already
    enforces that, and it is re-tested here so a projection cannot silently run off the end;
  * a parent row inside the child's span but NOT on a child element boundary (when the child is an
    array) is kept with its modular displacement, because that is what the parent observed.

WHAT A PROJECTED CENSUS IS NOT. It is not independent evidence. If the parent's census is wrong at a
displacement, the child's is wrong at the same one, and a width cross-check that passes on both has
checked one fact twice. The emitted `route` column records `embed <Parent>+0xOFF` so a reader can
never mistake it for a scan.

    python project_embed_census.py --list
    python project_embed_census.py --type AiOrderRecord --out <path>
"""
import argparse
import csv
import glob
import io
import os
import re
import sys

import kit_paths as KP

R_EMBED = re.compile(r"^EMBED\s+([A-Za-z0-9_]+)\s*\+\s*(0x[0-9A-Fa-f]+)"
                     r"(?:\s+stride=(0x[0-9A-Fa-f]+|\d+))?(?:\s+count=(\d+))?")


def census_map():
    """The parent -> census filename map the width checker already curates."""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_census_widths.py")
    t = io.open(p, encoding="utf-8").read()
    return dict(re.findall(r'"([A-Za-z0-9_]+)":\s*"([^"]+-accesses\.tsv)"', t))


def find_file(name):
    hits = glob.glob(os.path.join(KP.DB, "**", name), recursive=True)
    return hits[0] if hits else None


def load_types():
    out = {}
    with io.open(os.path.join(KP.DB, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            try:
                size = int(f[1], 0)
            except ValueError:
                size = None
            out[f[0]] = (size, (f[12] or "").strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", default=None)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    types = load_types()
    cmap = census_map()

    rows = []
    for t, (size, route) in sorted(types.items()):
        for alt in route.split("|"):
            m = R_EMBED.match(alt.strip())
            if not m:
                continue
            parent, off = m.group(1), int(m.group(2), 0)
            stride = int(m.group(3), 0) if m.group(3) else (size or 0)
            count = int(m.group(4)) if m.group(4) else 1
            rows.append((t, size, parent, off, stride, count))
            break

    if a.list or not a.type:
        print("EMBED types: %d" % len(rows))
        print("  %-32s %-28s %-8s %-7s %-5s %s"
              % ("type", "parent", "offset", "stride", "count", "parent census"))
        n_ok = 0
        for t, size, parent, off, stride, count in rows:
            f = cmap.get(parent)
            ok = f and find_file(f)
            n_ok += 1 if ok else 0
            print("  %-32s %-28s %-8s 0x%-5X %-5d %s"
                  % (t[:32], parent[:28], hex(off), stride, count,
                     (f if ok else ("parent has no census" if not f else "file missing"))))
        print()
        print("  projectable now (the parent has a census on disk): %d of %d" % (n_ok, len(rows)))
        return 0

    sel = [r for r in rows if r[0] == a.type]
    if not sel:
        print("no EMBED route for %s" % a.type)
        return 2
    t, size, parent, off, stride, count = sel[0]
    f = cmap.get(parent)
    path = find_file(f) if f else None
    if not path:
        print("%s: parent %s has no census to project from" % (t, parent))
        return 2

    psize = types.get(parent, (None, ""))[0]
    span = stride * count
    if psize is not None and off + span > psize:
        print("REFUSED - %s +0x%X spans 0x%X, ending at 0x%X, past %s's declared 0x%X"
              % (t, off, span, off + span, parent, psize))
        return 1

    out, kept, seen = [], 0, set()
    with io.open(path, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        hdr = next(r, None)
        for row in r:
            if len(row) < 6:
                continue
            try:
                d = int(row[3], 0)
                site = int(row[2], 16)
            except ValueError:
                continue
            if not (off <= d < off + span):
                continue
            cd = (d - off) % stride
            if (site, cd) in seen:
                continue
            seen.add((site, cd))
            kept += 1
            # CARRY THE PARENT'S `exposed` MARK. The projection is the parent's evidence
            # rebased, so a parent row that came through a helper the whole image calls is
            # still that when it lands in the child - and dropping the mark here would let a
            # contaminated access into a child census unmarked, which is worse than in the
            # parent, because a child is small and one bad width can dominate its offset.
            # BOTH MARKS, not just the first one. `exposed` was carried when it was added and
            # `zeroclear` was not, which left the 7EA0 child census unmarked at the very six
            # offsets whose parent rows carry the mark - the same inconsistency, one mark later.
            # Listing them rather than copying the whole cell keeps the route column's own text
            # (`embed <Parent>+0xOFF`) authoritative about where the row came from.
            marks = "".join(" " + m for m in ("exposed", "zeroclear")
                            if len(row) > 6 and m in row[6])
            out.append((row[0], row[1], row[2], cd, row[4], row[5], marks))

    print("%s: EMBED %s +0x%X stride 0x%X count %d" % (t, parent, off, stride, count))
    print("  parent census %s (%s)" % (os.path.basename(path), path))
    print("  rows projected: %d at %d distinct offset(s)" % (kept, len({x[3] for x in out})))
    # `--out` is written even when the projection is empty: a header-only file is the
    # durable form of a MEASURED ABSENCE, and a batch runner that looks for the artifact
    # should find it rather than record a silent skip beside a genuine refusal
    # (OPUS-NOTICE-FRONTIER-PROJECT-EMBED-CENSUS-EXITS-NONZERO-ON-AN-EMPTY-PROJECTION).
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, cd, kind, txt, ex in sorted(out, key=lambda x: (x[3], x[2])):
                fh.write("%s\t%s\t%s\t0x%X\t%s\t%s\tembed %s+0x%X%s\t\n"
                         % (fn, nm, site, cd, kind, txt, parent, off, ex))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
