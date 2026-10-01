#!/usr/bin/env python3
"""check_cited_artifacts.py - does the thing a field row cites actually exist?

WHY THIS EXISTS, and it is not a tidiness check. On 2026-09-19 two types were found, hours
apart, whose rows cite a census by name and number while NO CENSUS FILE EXISTED:

    LegacyPs2GsTextureContext     27 rows citing "gen_ptr_census_depth1.py over PTR 0209A670,
                                  36 accesses at 15 offsets in 11 functions"
    FrameMarkerSingleton01F82C80  11 rows citing the same generator

Both were run to a CONSOLE. Nothing was written, so no map could name the file, so
`check_census_widths.py` had never compared one of those 38 rows - while their evidence column
read as though the type had been thoroughly censused. That is the worst shape a gap can take: it
does not look like a gap. The first was found by accident, the second by this check.

The common cause is dull and worth naming: **two of the kit's census generators had no `--out`.**
A tool that prints a report and writes no file produces evidence that is citable but not
re-readable, and the citation outlives the console.

WHAT IS CHECKED, and each one is a fact, not a judgement
--------------------------------------------------------
1. **A cited `*.py` exists somewhere under `Database/Tools`.** A row citing a script that was
   renamed or deleted is evidence nobody can re-run. This is the weakest of the three and the
   cheapest to satisfy. The scope is the whole tree, not the kit, for the reason recorded at
   `scan()`: 3,577 of the 3,904 Python files under Tools are peers' working scripts, and a row
   is perfectly entitled to cite one - the first live run reported such a citation as missing.
2. **A cited `*-accesses.tsv` exists on disk.** Naming a file that is not there is the direct
   form of the defect above.
3. **A type whose rows cite a CENSUS-PRODUCING generator is in one of the three census maps.**
   This is the one that found FrameMarkerSingleton01F82C80. Being in the map is what makes the
   census reachable by the width and interior gates; a file on disk that no map names is the
   EvaluationContext failure, already recorded in check_census_widths.py's own comments.

WHAT IS DELIBERATELY NOT CHECKED
--------------------------------
That the census AGREES with the rows. Reproducing a cited run is a per-type judgement - when
LegacyPs2GsTextureContext was regenerated it reproduced 36/15/11 exactly and that was worth
recording, but when FrameMarkerSingleton01F82C80 was, the depth-1 tool returned 9 accesses at 6
offsets against rows that rest on a body two calls deep, and the right answer was a DIFFERENT
generator, not a smaller census. A checker cannot make that call. It reports absence only.

THE PRODUCER LIST IS EXPLICIT, because a pattern over-matched
-------------------------------------------------------------
The first draft matched `*_scan.py` as well and reported four `ManagerSub*` types citing
`arg_extent_scan.py`, which measures an argument's extent and produces no census at all. Naming
the producers costs a line each and stops the check inventing findings.

    check_cited_artifacts.py [--self-test]
"""
import argparse
import collections
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP            # noqa: E402
import check_census_widths as C   # noqa: E402

PY = re.compile(r"\b([a-z0-9_]+\.py)\b")
TSV = re.compile(r"\b([a-z0-9][a-z0-9-]*-accesses\.tsv)\b")

# Tools whose product is a census FILE. Extend this when a new generator is added; a tool that
# only reports (arg_extent_scan, disp_sweep, any check_*) does not belong here.
PRODUCERS = frozenset((
    "gen_ptr_census.py",
    "gen_ptr_census_depth1.py",
    "gen_ptr_census_ctor.py",
    "gen_array_census.py",
    "gen_static_census.py",
    "gen_widget_census.py",
    "gen_route_seeded_census.py",
    "gen_offset_tracked_census.py",
    "gen_embed_census_depth1.py",
    "project_embed_census.py",
    "record_field_scan.py",
))


def scan(db, kit, tools=None):
    # THE WHOLE Tools TREE, NOT THE KIT DIRECTORY, and this is the check's own first false
    # positive. Its first live run reported `verb_named_fields.py` as a script that does not
    # exist, cited by one ActorStorageRecord row. It exists: the row gives its path, and the
    # path is `Tools/work/FABLE/drift5/verb_named_fields.py` - a peer's working script, not a
    # kit one. 3,577 of the 3,904 Python files under Tools live outside the kit directory, so
    # scoping the existence test to the kit was not a near-miss; it was the wrong denominator,
    # and it turned every citation of a working script into a finding. The rule now is simply
    # "somewhere under Tools", which is what "a reader can go and run it" means here.
    if tools is None:
        tools = os.path.abspath(os.path.join(kit, "..", ".."))
    have_py = {os.path.basename(p)
               for p in glob.glob(os.path.join(tools, "**", "*.py"), recursive=True)}
    have_py |= {os.path.basename(p) for p in glob.glob(os.path.join(kit, "*.py"))}
    have_tsv = {os.path.basename(p).lower()
                for p in glob.glob(os.path.join(db, "**", "*.tsv"), recursive=True)}
    mapped = set(C.CENSUS) | set(C.STATIC_CENSUS) | set(C.SUBOBJECT_CENSUS)

    miss_py, miss_tsv = collections.Counter(), collections.Counter()
    unmapped = collections.defaultdict(collections.Counter)
    rows = 0
    with io.open(os.path.join(db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        next(fh, None)
        for line in fh:
            c = line.rstrip("\n").split("\t")
            if len(c) < 9:
                continue
            rows += 1
            ev = c[8]
            for m in set(PY.findall(ev)):
                if m not in have_py:
                    miss_py[m] += 1
            for m in set(TSV.findall(ev)):
                if m.lower() not in have_tsv:
                    miss_tsv[m] += 1
            if c[0] not in mapped:
                for m in set(PY.findall(ev)) & PRODUCERS:
                    unmapped[c[0]][m] += 1
    return rows, miss_py, miss_tsv, unmapped


def self_test():
    """The check must FIRE. A control that cannot is not a control.

    Run against a fixture whose rows cite a script and a census that do not exist, and against
    one that cites nothing at all.
    """
    import shutil
    import tempfile
    hdr = ("type\toffset\tsize\tname\tctype\tmeaning\treadiness\tconfidence\tevidence\n")
    bad = ("Widget\t0x00\t4\tx\tuint32\tm\tDISCOVERED\tHIGH\t"
           "Static: produced by no_such_tool.py, see no-such-census-accesses.tsv\n")
    unmapped = ("NoSuchType\t0x00\t4\tx\tuint32\tm\tDISCOVERED\tHIGH\t"
                "Static: gen_ptr_census_depth1.py over PTR 0x0\n")
    clean = ("Widget\t0x00\t4\tx\tuint32\tm\tDISCOVERED\tHIGH\tStatic: read at 001234AB\n")
    ok = True
    for label, body, want in (("doctored", bad + unmapped, (1, 1, 1)),
                              ("clean", clean, (0, 0, 0))):
        root = tempfile.mkdtemp()
        d = os.path.join(root, "_types")
        os.makedirs(d)
        io.open(os.path.join(d, "fields.tsv"), "w", encoding="utf-8",
                newline="").write(hdr + body)
        # The doctored fixture cites a producer as well, to exercise check 3. That producer
        # must EXIST inside the hermetic tree, or check 1 counts it too and the two assertions
        # stop being independent - which is exactly what happened when the existence scope was
        # widened, and the self-test caught it.
        io.open(os.path.join(root, "gen_ptr_census_depth1.py"), "w",
                encoding="utf-8", newline="").write("")
        # tools=root keeps the fixture hermetic: the real tree would satisfy the existence
        # test for any plausible script name and the doctored case could never fire.
        _r, mp, mt, um = scan(root, root, tools=root)
        got = (len(mp), len(mt), len(um))
        print("  %-9s -> missing scripts %d, missing censuses %d, unmapped types %d  (want %s)"
              % (label, got[0], got[1], got[2], want))
        ok &= got == want
        shutil.rmtree(root, ignore_errors=True)
    print("SELF-TEST", "PASSES" if ok else "FAILS")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()

    rows, miss_py, miss_tsv, unmapped = scan(a.db, HERE)
    print("CITED-ARTIFACT CHECK  a row that names a thing must name a thing that is there")
    print("  field rows read: %d" % rows)
    print()
    print("1. CITED SCRIPTS NOT IN THE KIT: %d" % len(miss_py))
    for k, n in miss_py.most_common():
        print("     %-40s cited by %d row(s)" % (k, n))
    print()
    print("2. CITED *-accesses.tsv NOT ON DISK: %d" % len(miss_tsv))
    for k, n in miss_tsv.most_common():
        print("     %-40s cited by %d row(s)" % (k, n))
    print()
    print("3. TYPES CITING A CENSUS PRODUCER BUT IN NO CENSUS MAP: %d" % len(unmapped))
    print("     The census may exist and still be unreachable: the width and interior gates")
    print("     iterate the maps, so a type absent from them is never compared at all.")
    for t, cc in sorted(unmapped.items(), key=lambda kv: -sum(kv[1].values())):
        print("     %-34s %2d row(s)  %s"
              % (t, sum(cc.values()), ", ".join("%s x%d" % kv for kv in cc.most_common(3))))
    return 1 if (miss_py or miss_tsv or unmapped) else 0


if __name__ == "__main__":
    sys.exit(main())
