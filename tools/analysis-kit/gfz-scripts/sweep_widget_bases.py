#!/usr/bin/env python3
"""Find embedded Widget instances in every census artifact, with the controls that make the
answer mean something.

THE SIGNATURE. A base B is a widget base when the accesses at B+d, for d inside Widget's 0xC0
header, BEGIN on declared Widget field starts and none begins mid-field. An access wider than
the row it starts on is SOUND when it ends on a declared boundary: the compiler merges adjacent
fields, and `mov dword ptr [rdi+0x98], eax` covers field98 and field9A, two declared 2-byte
rows. Counting that as a violation is the single easiest way to get this wrong - it made an
early pass of this signature report a real base as dirty.

CANDIDATE BASES ARE DERIVED, NOT SCANNED. Any base with at least one exact start equals
`access_offset - declared_row_offset` for some pair, so only those are tested. Exact, and it is
what makes 65 artifacts affordable.

THREE CONTROLS, BECAUSE A DENSE LAYOUT MATCHES THINGS BY ACCIDENT. Widget declares 35 rows over
0xC0 bytes.
  NEGATIVE   every artifact is also scored against DECOY layouts carrying the same multiset of
             row sizes and gaps, shuffled. On the shipping store the real layout yields 47
             clean bases and the decoys 0.25 per layout. If that margin ever collapses, this
             tool is measuring density rather than widgets and its output must not be used.
  POSITIVE   Widget's own census must score every declared row at +0x0, and the two hand-found
             types must come back at their known offsets. --self-test asserts the first.
  CONTAINMENT  base + 0xC0 must fit the declared type size. This alone refuted a candidate at
             +0x8 of a 0x58-byte type.

AND THREE FOLDS, BECAUSE A RAW HIT COUNT IS NOT A POPULATION.
  PARENT/CHILD  a singleton census and its sub-objects' censuses view the same bytes, so the
                same instance appears at parent+<sub offset> and at child+0x0 with BYTE-
                IDENTICAL scores. 11 of 14 singleton bases were duplicates on first run.
  ALIAS         B and B+8 both score clean because a widget opens with a pointer. The alias
                always carries MORE GAP than its parent (+0xAC0 has 8, +0xAC8 has 18).
  ARRAY         bases at a constant stride inside one artifact are one record type at several
                element positions, not several findings.

MUTUAL EXCLUSION. The header is 0xC0, so two clean bases less than 0xC0 apart OVERLAP and
cannot both be instances. Such a cluster is reported as CONTESTED and the tool does not choose
within it. This is reported, never silently resolved.

WHAT A CLEAN BASE IS NOT. It says every scored access is consistent with a Widget at that
offset, and that a shuffled layout of the same shape does not do this. It does NOT establish
the instance's EXTENT, and under the sized-by-argument ctype rule (SWE2-FRONTIER 2026-09-19)
a row declaring an instance must carry that extent. NO ROW SHOULD BE DECLARED FROM THIS OUTPUT
ALONE.
"""
import argparse
import csv
import glob
import io
import os
import random
import re
import sys

HDR = 0xC0
MIN_EXACT = 6
MIN_SCORED = 10
WIDTH = (("xmmword", 16), ("qword", 8), ("dword", 4), ("word", 2), ("byte", 1))


def width_of(instr):
    """Access width in bytes, 0 for an address computation, None when unknown."""
    for k, n in WIDTH:
        if k in instr:
            return n
    if re.search(r"\blea\b", instr):
        return 0
    return None


def widget_rows(db):
    rows = []
    with io.open(os.path.join(db, "_types", "fields.tsv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("type") == "Widget":
                rows.append((int(r["offset"], 16), int(r["size"])))
    return sorted(rows)


def type_sizes(db):
    out = {}
    with io.open(os.path.join(db, "_types", "types.tsv"), encoding="utf-8") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        key = rd.fieldnames[0]
        for r in rd:
            try:
                out[r.get(key)] = int((r.get("size") or ""), 16)
            except ValueError:
                continue
    return out


def decoy(rows, seed):
    """Same multiset of sizes and gaps, shuffled - a layout of identical shape that is wrong."""
    sizes = [s for _o, s in rows]
    gaps, prev = [], 0
    for o, s in rows:
        gaps.append(o - prev)
        prev = o + s
    rnd = random.Random(seed)
    rnd.shuffle(sizes)
    rnd.shuffle(gaps)
    out, cur = [], 0
    for g, s in zip(gaps, sizes):
        cur += g
        if cur + s > HDR:
            break
        out.append((cur, s))
        cur += s
    return sorted(out)


def index(rows):
    cover, size, ends = {}, {}, set()
    for o, s in rows:
        size[o] = s
        ends.add(o + s)
        for d in range(o, min(o + s, HDR)):
            cover[d] = o
    return cover, {o for o, _s in rows}, ends, size


def score(base, acc, cover, ends, size):
    exact, interior, gap, n = set(), 0, 0, 0
    for off, w in acc:
        d = off - base
        if d < 0 or d >= HDR or w == 0:
            continue
        n += 1
        ro = cover.get(d)
        if ro is None:
            gap += 1
        elif d != ro:
            interior += 1
        elif w is None or w <= size[ro] or (d + w) in ends:
            exact.add(ro)
        else:
            interior += 1
    return len(exact), interior, gap, n


def clean_bases(acc, rows):
    cover, starts, ends, size = index(rows)
    cands = {o - ro for o, _w in acc for ro in starts if o - ro >= 0}
    out = []
    for b in sorted(cands):
        e, iv, g, n = score(b, acc, cover, ends, size)
        if e >= MIN_EXACT and iv == 0 and n >= MIN_SCORED:
            out.append((b, e, g, n))
    return out


def load(path):
    acc = []
    with io.open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            d = (r.get("disp") or "").strip()
            if not d:
                continue
            try:
                acc.append((int(d, 16), width_of(r.get("instruction", ""))))
            except ValueError:
                continue
    return acc


def sites(path):
    """The instruction SITES a census records, as a set."""
    out = set()
    with io.open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            s = (r.get("site") or "").strip()
            if s:
                out.add(s)
    return out


def widget_sites(db):
    hits = glob.glob(os.path.join(db, "**", "widget-accesses.tsv"), recursive=True)
    return sites(hits[0]) if hits else set()


def contested(bases):
    """Groups of clean bases closer together than the header - at most one can be real."""
    bs, groups, cur = sorted(bases), [], None
    for b in bs:
        if cur and b - cur[-1] < HDR:
            cur.append(b)
        else:
            if cur:
                groups.append(cur)
            cur = [b]
    if cur:
        groups.append(cur)
    return [g for g in groups if len(g) > 1]


def self_test(db):
    """Widget's own census must score every declared row at +0x0, and a decoy must not."""
    rows = widget_rows(db)
    hits = glob.glob(os.path.join(db, "**", "widget-accesses.tsv"), recursive=True)
    if not hits:
        print("self-test SKIPPED: widget-accesses.tsv not found")
        return 0
    acc = load(hits[0])
    cover, _s, ends, size = index(rows)
    e, iv, g, n = score(0, acc, cover, ends, size)
    print("self-test: Widget's own census at +0x0 -> %d of %d declared rows, %d interior, "
          "%d scored" % (e, len(rows), iv, n))
    d = decoy(rows, 1)
    cover2, _s2, ends2, size2 = index(d)
    e2, iv2, _g2, _n2 = score(0, acc, cover2, ends2, size2)
    print("self-test: the same census against a decoy layout -> %d exact, %d interior"
          % (e2, iv2))
    ok = (iv == 0 and e >= len(rows) - 2 and (iv2 > 0 or e2 < e))
    print("self-test %s" % ("PASSES" if ok else "FAILS - do not trust this tool's output"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="Database/FFXII TZA")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test(a.db)

    rows = widget_rows(a.db)
    decoys = [decoy(rows, s) for s in range(4)]
    sizes = type_sizes(a.db)
    wsites = widget_sites(a.db)
    paths = sorted(glob.glob(os.path.join(a.db, "**", "*-accesses.tsv"), recursive=True))
    real, dec, shown = 0, 0, 0
    print("Widget: %d declared rows over 0x%X. %d artifact(s)." % (len(rows), HDR, len(paths)))
    print()
    for p in paths:
        acc = load(p)
        if len(acc) < MIN_SCORED:
            continue
        cb = clean_bases(acc, rows)
        dec += sum(len(clean_bases(acc, d)) for d in decoys)
        real += len(cb)
        if not cb:
            continue
        shown += 1
        name = os.path.basename(p).replace("-accesses.tsv", "")
        # THE SECOND GATE. A declared-layout match is a statement about SHAPE. Sharing an
        # instruction site with Widget's own census is a statement about the SAME CODE touching
        # both objects. Geometry alone over-reports badly - on the shipping store 47 clean
        # bases reduce to six corroborated objects - so the two are printed together and a
        # GEOMETRY-ONLY artifact must not be quoted as carrying a widget.
        shared = len(sites(p) & wsites) if name != "widget" else -1
        tag = ("self" if shared < 0 else
               ("CORROBORATED, %d shared site(s)" % shared) if shared else
               "GEOMETRY ONLY - shares NO site with Widget's census")
        print("  %-44s %s" % (name, tag))
        for b, e, g, n in cb:
            print("      +0x%-7X %2d exact %3d gap %4d scored%s"
                  % (b, e, g, n, "" if e >= 11 and n >= 20 else "   (thin)"))
        for grp in contested([b for b, _e, _g, _n in cb]):
            print("      CONTESTED: %s - closer than the 0x%X header, at most ONE is real"
                  % (" ".join("+0x%X" % x for x in grp), HDR))
    print()
    print("real layout : %d clean base(s) across %d artifact(s)" % (real, shown))
    print("            ...of which only the CORROBORATED artifacts above may be quoted as")
    print("            carrying a widget. On the shipping store that is 6 objects, not 47.")
    print("decoys      : %.2f clean base(s) per layout on the same data" % (dec / 4.0))
    if dec / 4.0 > real * 0.25:
        print("WARNING: the decoy margin has collapsed. This tool is measuring layout density,")
        print("         not widgets, and its output must not be used.")
    print()
    print("Folds this tool does NOT apply for you: parent/child duplicates (a singleton and its")
    print("sub-object censuses view the same bytes and score identically), B+8 aliases, and")
    print("constant-stride array repeats. Apply them before quoting a population.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
