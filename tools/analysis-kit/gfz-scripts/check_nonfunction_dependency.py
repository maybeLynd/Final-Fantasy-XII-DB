#!/usr/bin/env python3
"""check_nonfunction_dependency.py - which stale documents actually need the non-function export.

163 documents cannot transfer to the certified parent because they quote decompiler state, and FAS2
witnesses FUNCTION annotation only. That is the whole of `OPUS-REQ-ASTRA-NONFUNCTION-ANNOTATION-
EXPORT`, and ASTRA's lane is parked - so 163 documents wait on one dependency.

**THE 163 IS NOT ONE POPULATION.** `decompiler_tokens.PATTERNS` groups `FUN_`, `SUB_`, `DAT_`,
`LAB_`, `PTR_` and `UNK_` into a single "auto-name" class, and two of those six are not like the
other four:

    FUN_0025D740   a FUNCTION's default name.      FAS2 records `name` per function.
    DAT_02092170   a NON-function symbol's name.   FAS2 records nothing about it.

A page whose only decompiler token is `FUN_` is quoting something the function snapshot witnesses
exactly, and needs no new exporter to settle. **45 of the 163 are in that position** - they quote no
`DAT_`/`LAB_`/`PTR_`/`UNK_`, no `param_`, no `local_`, no `xVar`, no `undefined`, no cast and no
`in_`/`unaff_`/`extraout_`.

AND THE CLAIM IS TESTED PER TOKEN, not argued from the taxonomy. Every `FUN_`/`SUB_` address those
45 documents quote is looked up in the certified snapshot and in the snapshot of the generation the
document is stamped to, and the two `name` fields are compared. Today: **412 tokens, 0 missing from
the certified snapshot, 0 renamed.** Corroborated from the other direction by the whole-image
figure - across GN158 -> PARENT and GN160 -> PARENT, **0 functions renamed, 0 added, 0 removed**,
which is `check_delta_additivity`'s immutable-field result seen per field.

THIS DOES NOT TRANSFER ANYTHING. It says which documents the missing exporter is not needed for. The
other half of a transfer - that the document makes no uncorrected claim - is a separate test, and
writing a stamp is a separate act that needs its adjudication.

THE EXIT IS A CANARY, NOT A DEBT REPORT. It is 0 while the argument holds and 1 the moment a quoted
function is renamed or disappears from the certified snapshot, because that is exactly when these 45
stop being settleable without the exporter.
"""
import argparse
import collections
import io
import os
import re
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
WORK = os.path.join(REPO, "Database", "Tools", "work")
SKIP = ("_index", "_templates", "_inbox", "_experiments")

# The lineage, by the prefix a document's stamp carries.
SNAPSHOTS = {
    "GN158": os.path.join(WORK, "verify", "snapshot.fas2.GN158"),
    "GN160": os.path.join(WORK, "verify_GFZ_GN160", "snapshot.fas2"),
    "PARENT": os.path.join(WORK, "verify_GFZ_PARENT", "snapshot.fas2"),
}
STAMP_GEN = {"2ed8affb732f0def0a7852e0": "GN158",
             "fb9b5e7ea002c1626a53d47d": "GN159",     # no snapshot kept; bracketed by GN158/GN160
             "fa0db2933c988211ed4f3c76": "GN160",
             "11110a34acf6d0fc9ecd1727": "PARENT"}
CERTIFIED = "11110a34acf6d0fc9ecd1727"

STAMP = re.compile(r"gzf_sha256:\s*([0-9a-fA-F]{24})")
XFER = re.compile(r"transfers_to:\s*\n\s*parent:\s*([0-9a-fA-F]{24})")
# THE SPLIT THIS FILE EXISTS FOR. Two of the six auto-name prefixes name a FUNCTION.
FUNC_AUTO = re.compile(r"\b(?:FUN|SUB)_([0-9A-Fa-f]{4,})\b")
NONFUNC_AUTO = re.compile(r"\b(?:DAT|LAB|PTR|UNK)_[0-9A-Fa-f]{4,}\b")
# WHAT THE EXPORTER MUST REACH, for the documents that still need it. Two different pieces of
# Ghidra state hide behind the remaining tokens, and they are not the same build job.
TYPE_MANAGER = {"xVar", "undefined", "cast"}      # decompiler type propagation
PROTOTYPE_ONLY = {"param_", "local_"}             # default names when no prototype applies


def load(tag):
    p = SNAPSHOTS.get(tag)
    if not p or not os.path.isfile(p):
        return None
    from diff_fas2 import parse
    return parse(p)[1]


def control():
    """The split must classify a constructed case each way, or the partition means nothing."""
    ok = True
    cases = [("a page naming `FUN_0025D740` and nothing else", True, False),
             ("a page naming `DAT_02092170`", False, True),
             ("a page naming both `FUN_0025D740` and `PTR_00401000`", True, True),
             ("a page naming neither", False, False)]
    for text, want_f, want_n in cases:
        if bool(FUNC_AUTO.search(text)) != want_f or bool(NONFUNC_AUTO.search(text)) != want_n:
            print("  CONTROL FAILED on %r" % text)
            ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    sys.path.insert(0, KIT)
    try:
        import decompiler_tokens as dt
    except ImportError:
        print("CANNOT RUN: decompiler_tokens is not importable")
        return 2
    if not control():
        print("\n  THE SPLIT'S CONTROL DID NOT FIRE - the partition below is unsupported.")
        return 2
    print("  control passed: the split classifies FUN_/SUB_ and DAT_/LAB_/PTR_/UNK_ each way.")

    cert = load("PARENT")
    if cert is None:
        print("CANNOT RUN: the certified snapshot is not in the tree")
        return 2

    buckets = collections.Counter()
    func_only, tokens, missing, renamed = [], 0, [], []
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, a.db).replace(os.sep, "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            m = STAMP.search(t)
            if not m:
                continue
            gen = STAMP_GEN.get(m.group(1).lower())
            if gen in (None, "PARENT"):
                continue
            x = XFER.search(t)
            if x and x.group(1).lower() == CERTIFIED:
                continue
            hits = [n for n, pat in dt.PATTERNS if pat.search(t)]
            if not hits:
                continue
            buckets["quoting decompiler state"] += 1
            if hits != ["auto-name"] or NONFUNC_AUTO.search(t):
                buckets["needs the non-function export"] += 1
                if NONFUNC_AUTO.search(t):
                    buckets["  non-function symbol"] += 1
                elif set(hits) & TYPE_MANAGER:
                    buckets["  data type manager"] += 1
                else:
                    buckets["  prototype only"] += 1
                continue
            func_only.append((rel, gen))
            buckets["function names only"] += 1

    # PER TOKEN, not per taxonomy. Every quoted function is looked up in the certified snapshot and
    # in the generation the document is stamped to; the `name` fields must be identical.
    snaps = {g: load(g) for g in ("GN158", "GN160")}
    for rel, gen in func_only:
        t = io.open(os.path.join(a.db, rel.replace("/", os.sep)),
                    encoding="utf-8", errors="replace").read()
        for mm in FUNC_AUTO.finditer(t):
            e = int(mm.group(1), 16)
            tokens += 1
            if e not in cert:
                missing.append((rel, e))
                continue
            for g, s in snaps.items():
                if s and e in s and s[e]["name"] != cert[e]["name"]:
                    renamed.append((rel, e, g))

    print("\n  stale, untransferred, quoting decompiler state : %d"
          % buckets["quoting decompiler state"])
    print("    needs the non-function export                : %d"
          % buckets["needs the non-function export"])
    print("      quote a NON-FUNCTION SYMBOL (DAT_/LAB_/PTR_/UNK_) : %d   the symbol table"
          % buckets["  non-function symbol"])
    print("      touch the DATA TYPE MANAGER (xVar/undefined/cast) : %d   type propagation"
          % buckets["  data type manager"])
    print("      only param_/local_ - no prototype applied         : %d   SEE BELOW"
          % buckets["  prototype only"])
    print("    quotes FUNCTION NAMES ONLY - FAS2 witnesses these : %d"
          % buckets["function names only"])
    print("\n  FUN_/SUB_ tokens in that second group         : %d" % tokens)
    print("    not present in the certified snapshot        : %d" % len(missing))
    print("    whose name differs from the certified parent : %d" % len(renamed))
    for rel, e in missing[:8]:
        print("      MISSING  %08X  %s" % (e, rel[:60]))
    for rel, e, g in renamed[:8]:
        print("      RENAMED  %08X  since %s  %s" % (e, g, rel[:52]))
    if not (missing or renamed):
        print("\n  So the export is NOT needed for those %d. Every decompiler token they carry is a"
              % buckets["function names only"])
        print("  function name, and every one is byte-identical in the certified snapshot.")
    if buckets["  prototype only"]:
        print("\n  THE prototype-only ROW IS NOT CLAIMED, DELIBERATELY. FAS2 records `prototype`")
        print("  and `signature_source`, so there is an argument that `param_1` is witnessed - the")
        print("  decompiler emits it precisely when no prototype applies, and whether one does is")
        print("  in the snapshot. That argument is NOT made here. It rests on an inference about")
        print("  how Ghidra names parameters, which type propagation can also do, and it is not")
        print("  testable from the shipped bytes. The %d documents above stay in the export's"
              % buckets["  prototype only"])
        print("  population. The 45 were different in kind: FUN_ IS the `name` field, compared per")
        print("  token against both snapshots - a comparison, not an inference about a tool.")
    print("\n  THIS TRANSFERS NOTHING. The other half of a transfer - that the document makes no")
    print("  uncorrected claim - is a separate test, and writing a stamp is a separate act.")
    return 1 if (missing or renamed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
