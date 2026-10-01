#!/usr/bin/env python3
"""census_ard_container.py - the FF12AR03 area container and its .nmb pair, over the whole corpus.

The unit is the AREA
--------------------
`.ard` lives at `ps2data/plan_master/<locale>/plan_map/<area>/area/<area>.ard`, one level ABOVE the
per-map `.ebp`. **332 files but 166 logical areas**: every `.ard` ships twice, under the `ch` and
`in` locale trees and no other. A census that counts files double-counts, so this keys on the AREA
STEM and reports the duplication rather than inheriting it.

`.nmb` is a strict pair with it -- identical stem sets, same `area/` folder, never one without the
other -- so it is censused here too rather than separately.

Why census before sheets
------------------------
The same reason EBP's 14 units are trustworthy: the denominator was fixed by measurement before
anyone wrote prose. **Nothing about what these tables MEAN is decided here.** The community reads
`.ard` as per-area enemy status and attributes; that is tier 9 until a reader is named in the
binary, and this script deliberately reports structure only.

Usage
-----
    python census_ard_container.py --vbf "<...>\\FFXII_TZA.vbf" \
        --out Tools/work/formats/ard-container-census.tsv
    python census_ard_container.py --self-test
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))
MAGIC = b"FF12AR03"
STEM = re.compile(r"plan_map/([^/]+)/area/([^/]+)\.(ard|nmb)$", re.I)


def parse_paths(names):
    """-> {stem: {'ard': [paths], 'nmb': [paths]}} keyed by AREA, not by file."""
    out = collections.defaultdict(lambda: {"ard": [], "nmb": []})
    for p in names:
        m = STEM.search(p.replace("\\", "/"))
        if m:
            out[m.group(2).lower()][m.group(3).lower()].append(p)
    return out


def st2e_offsets(blob):
    """Every `st2e` occurrence, so the count is measured rather than assumed to be one."""
    out, i = [], blob.find(b"st2e")
    while i >= 0:
        out.append(i)
        i = blob.find(b"st2e", i + 1)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.vbf:
        return ap.error("--vbf or --self-test required")

    import vbfextract as V
    f = io.open(a.vbf, "rb")
    names, blocks = V.load_index(f)
    areas = parse_paths(names)

    print("FF12AR03 AREA CONTAINER CENSUS")
    print("  %d area stems; %d .ard files, %d .nmb files"
          % (len(areas), sum(len(v["ard"]) for v in areas.values()),
             sum(len(v["nmb"]) for v in areas.values())))

    dup = collections.Counter(len(v["ard"]) for v in areas.values())
    pairless = [s for s, v in areas.items() if not v["ard"] or not v["nmb"]]
    print("  copies of each .ard: %s" % dict(dup))
    print("  areas missing one half of the pair: %d %s"
          % (len(pairless), ("- " + ", ".join(sorted(pairless)[:5])) if pairless else ""))

    rows, badmagic = [], []
    hdr = collections.defaultdict(collections.Counter)
    tabs = collections.Counter()
    nmb_sizes = collections.Counter()
    identical = 0
    for stem in sorted(areas):
        v = areas[stem]
        if not v["ard"]:
            continue
        blobs = []
        for p in v["ard"]:
            try:
                blobs.append(V.read_entry(f, names, blocks, p))
            except Exception:
                pass
        if not blobs:
            continue
        b = blobs[0]
        if len(blobs) > 1 and all(x == b for x in blobs[1:]):
            identical += 1
        if b[:8] != MAGIC:
            badmagic.append(stem)
            continue
        # header dwords after the 8-byte magic
        for off in range(8, 48, 4):
            if off + 4 <= len(b):
                hdr[off][struct.unpack_from("<I", b, off)[0]] += 1
        n = len(st2e_offsets(b))
        tabs[n] += 1
        nb = 0
        if v["nmb"]:
            try:
                nb = len(V.read_entry(f, names, blocks, v["nmb"][0]))
            except Exception:
                nb = -1
        nmb_sizes[nb] += 1
        rows.append((stem, len(b), n, nb, len(v["ard"])))

    print("  parsed %d areas; magic FF12AR03 in %d, other in %d"
          % (len(rows), len(rows), len(badmagic)))
    print("  **duplicate copies byte-identical in %d of %d areas**" % (identical, len(rows)))
    print("")
    print("  st2e tables per .ard : %s" % ", ".join("%d->%d" % kv for kv in sorted(tabs.items())))
    print("  .ard size range      : %d - %d B" % (min(r[1] for r in rows), max(r[1] for r in rows)))
    print("  .nmb size range      : %d - %d B" % (min(nmb_sizes), max(nmb_sizes)))
    print("")
    print("  header dwords after the magic (value -> areas):")
    for off in sorted(hdr):
        c = hdr[off]
        tag = "INVARIANT" if len(c) == 1 else "%d values" % len(c)
        print("    +0x%02X  %-11s %s" % (off, tag, c.most_common(4)))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# FF12AR03 area census - census_ard_container.py\n")
            o.write("# Keyed by AREA STEM. `copies` is how many locale trees ship it.\n")
            o.write("# st2e_tables is MEASURED, not assumed. Meaning is NOT decided here.\n")
            o.write("area\tard_bytes\tst2e_tables\tnmb_bytes\tcopies\n")
            for r in rows:
                o.write("%s\t%d\t%d\t%d\t%d\n" % r)
        print("\nwrote %s" % a.out)
    return 0


def self_test():
    names = ["ps2data/plan_master/in/plan_map/ztc_d/area/ztc_d.ard",
             "ps2data/plan_master/ch/plan_map/ztc_d/area/ztc_d.ard",
             "ps2data/plan_master/in/plan_map/ztc_d/area/ztc_d.nmb",
             "ps2data/plan_master/us/plan_map/ztc_d/ztc_d01/global/ztc_d01.ebp"]
    a = parse_paths(names)
    ok = True
    if list(a) != ["ztc_d"]:
        print("SELF-TEST FAILED: stems %s" % list(a)); ok = False
    if len(a["ztc_d"]["ard"]) != 2 or len(a["ztc_d"]["nmb"]) != 1:
        print("SELF-TEST FAILED: pairing %s" % a["ztc_d"]); ok = False
    if st2e_offsets(b"xxst2eyyst2e") != [2, 8]:
        print("SELF-TEST FAILED: st2e scan"); ok = False
    if not ok:
        return 1
    print("self-test ok: keyed by area not file, both locale copies collapse to one stem, "
          ".ebp ignored, st2e occurrences counted not assumed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
