#!/usr/bin/env python3
"""check_script_catalog.py - FINAL-AUDIT pass 25, made re-runnable.

Pass 25 is *"re-verify every ff12-script claim against the bundled source, not from memory; fails
if any catalog ID, header offset or field name differs."*

IT HAS BEEN RUN, ONCE, BY HAND: 1,224 of 1,224 script verbs identical (recorded in
check_sidefile_headers.py's docstring, which is the byproduct that run turned up). A one-off hand
check is not enough for this protocol, and the reason is structural rather than tidy-minded:

    "If any pass disproves anything, fix it by evidence and RESTART ALL THIRTY FROM PASS 1."

Thirty passes with a restart on any failure means every un-mechanised pass is paid again by hand
on every restart, and the passes most likely to be skipped under that load are exactly the ones
that cost the most to redo. So this makes pass 25's largest surface a command.

WHAT THIS COVERS, AND WHAT IT DOES NOT. Pass 25 names three things: catalog IDs, header offsets
and field names. This checks the FIRST - the verb catalog - completely, by comparing every row of
`scriptvm-dispatch.tsv` against the `{ 0xNNNN, { L"name", argc, ... } }` table in the bundled
`CScriptContainerInitializers.cpp`. Header offsets and EBP field names are a different surface and
are NOT checked here; pass 25 is not closed by this tool, it is made cheaper.

    Counting an instrument as coverage is the "volume is not explanation" mistake in a different
    costume - the protocol says so about its own inventory, and it applies to this file too.

CONTROL, on every run: the comparison is re-run against a deliberately corrupted copy of the side
file (one verb renamed, one arg count changed, one id removed). All three must be reported. A
comparison that cannot fail is not a comparison, and this pass's whole value is its ability to say
"identical" and be believed.
"""
import argparse
import io
import os
import re
import sys

# Resolved from THIS FILE, not from the working directory. run_gates.py invokes every checker
# with `--db <path>` and its own cwd; a default built from a relative string would have made this
# one exit 2 there and read as a refusal rather than as a mis-invocation - which is exactly the
# misreading NOT_A_CORPUS_GATE was introduced to stop for two other checkers.
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
DEFAULT_DB = os.path.join(_REPO, "Database", "FFXII TZA")
DEFAULT_CATALOG = os.path.join(_REPO, "Collaboration", "tools", "ffxii", "ff12-script-master",
                               "ff12-script", "CScriptContainerInitializers.cpp")
SIDEFILE = os.path.join("01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-dispatch.tsv")

# { 0x0001, { L"setpos", 3, false, true, true, {...} }},
ENTRY = re.compile(r"\{\s*0x([0-9A-Fa-f]{1,4})\s*,\s*\{\s*L\"([^\"]+)\"\s*,\s*(\d+)")


def load_catalog(path):
    text = io.open(path, encoding="utf-8", errors="replace").read()
    out = {}
    for m in ENTRY.finditer(text):
        out[int(m.group(1), 16)] = (m.group(2), int(m.group(3)))
    return out


def load_sidefile(path):
    rows = {}
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        header = None
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if header is None:
                header = f
                continue
            if len(f) < 3 or not f[0].strip():
                continue
            try:
                cid = int(f[0].strip(), 16)
            except ValueError:
                continue
            args = f[2].strip()
            rows[cid] = (f[1].strip(), int(args) if args.isdigit() else None)
    return rows


def compare(cat, side):
    """-> (name_mismatch, arg_mismatch, side_not_in_catalog, catalog_not_in_side)"""
    nm, am, extra = [], [], []
    for cid, (verb, args) in sorted(side.items()):
        if cid not in cat:
            extra.append((cid, verb))
            continue
        cverb, cargs = cat[cid]
        if verb != cverb:
            nm.append((cid, verb, cverb))
        elif args is not None and args != cargs:
            am.append((cid, verb, args, cargs))
    missing = sorted(c for c in cat if c not in side)
    return nm, am, extra, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--catalog", default=DEFAULT_CATALOG)
    a = ap.parse_args()

    sf = os.path.join(a.db, SIDEFILE)
    if not os.path.isfile(a.catalog):
        print("bundled catalog not found: %s" % a.catalog)
        print("pass 25 cannot run without the ff12-script source it is defined against.")
        return 2
    if not os.path.isfile(sf):
        print("side file not found: %s" % sf)
        return 2

    cat = load_catalog(a.catalog)
    side = load_sidefile(sf)
    print("FINAL-AUDIT PASS 25 - script verb catalog")
    print("  bundled catalog : %d entries  (%s)" % (len(cat), a.catalog))
    print("  database side file: %d rows  (%s)" % (len(side), SIDEFILE))

    nm, am, extra, missing = compare(cat, side)
    agree = len(side) - len(nm) - len(am) - len(extra)
    print("\n  verbs identical in name and arg count: %d of %d" % (agree, len(side)))

    bad = False
    if nm:
        bad = True
        print("\n  VERB NAME DIFFERS (%d):" % len(nm))
        for cid, v, cv in nm[:40]:
            print("    %04X  database %-24s bundled %s" % (cid, v, cv))
    if am:
        bad = True
        print("\n  ARG COUNT DIFFERS (%d):" % len(am))
        for cid, v, args, cargs in am[:40]:
            print("    %04X  %-24s database %s  bundled %s" % (cid, v, args, cargs))
    if extra:
        bad = True
        print("\n  IN THE DATABASE, NOT IN THE BUNDLED CATALOG (%d):" % len(extra))
        for cid, v in extra[:40]:
            print("    %04X  %s" % (cid, v))
    if missing:
        # NOT A FAILURE, AND THE SIDE FILE'S OWN HEADER SAYS WHY - carried here so this line
        # never reads as 730 undocumented verbs to whoever runs the pass next. The database
        # documents the DISPATCH TABLE IN THE IMAGE: 1,224 records at VA 01EED720, stride 0x20,
        # re-derived from the binary 2026-09-08. The catalog is an AUTHORED COMMUNITY ARTIFACT of
        # 1,954 verb names and is not verifiable against the image. So a catalog entry with no
        # record here is a verb this build's table does not contain - the expected direction of
        # the asymmetry. The direction that WOULD fail is the other one, and it is 0.
        print("\n  IN THE BUNDLED CATALOG, NOT IN THE DATABASE (%d) - EXPECTED, not a failure:"
              % len(missing))
        print("    the database documents the image's 1,224-record dispatch table; the catalog is")
        print("    an authored community list of 1,954 names. The failing direction is the other")
        print("    one - database ids absent from the catalog - and that is %d." % len(extra))
        for cid in missing[:20]:
            print("    %04X  %s" % (cid, cat[cid][0]))
        if len(missing) > 20:
            print("    ... and %d more" % (len(missing) - 20))

    # CONTROL ---------------------------------------------------------------
    print("\n  CONTROL: a corrupted copy of the side file must be caught on all three counts.")
    if len(side) < 3:
        print("    CONTROL SKIPPED: too few rows to corrupt. Negatives are not trustworthy.")
        return 2
    ids = sorted(side)
    bogus = dict(side)
    bogus[ids[0]] = ("__not_a_verb__", side[ids[0]][1])
    bogus[ids[1]] = (side[ids[1]][0], (side[ids[1]][1] or 0) + 7)
    del bogus[ids[2]]
    c_nm, c_am, c_extra, c_missing = compare(cat, bogus)
    caught = (len(c_nm) >= 1, len(c_am) >= 1, ids[2] in c_missing)
    if not all(caught):
        print("    CONTROL FAILED: name=%s argcount=%s removal=%s -- this comparison cannot"
              % caught)
        print("    detect the differences pass 25 exists to detect, so 'identical' means nothing.")
        return 2
    print("    control passed: renamed verb, wrong arg count and removed id all reported.")

    if bad:
        print("\n  PASS 25 FAILS on the verb catalog.")
        return 1
    print("\n  Pass 25's verb-catalog surface is clean. Header offsets and EBP field names are")
    print("  the rest of pass 25 and are NOT checked here - this makes the pass cheaper, not closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
