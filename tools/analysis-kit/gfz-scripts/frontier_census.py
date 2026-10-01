#!/usr/bin/env python3
"""frontier_census.py - what the EC-7 frontier is actually made of, so lanes can be chosen.

`check_dispositions.py` answers *how much* is dispositioned.  This answers *what is left*, which is
the question a family lane is picked from.  It **imports** that module and adds nothing to it: the
schema, the refusal rules and the denominator live there and are not duplicated here.

The four buckets
----------------
The split the work is organised by, not a taxonomy for its own sake:

    A  direct semantic disposition   already measured by check_dispositions (interior citation
                                     from a DOCUMENTED page).  Not frontier.
    B  proven family disposition     already declared and accepted.  Not frontier.

    C-candidate  middleware / library / generated.  Tagged Phyre.*, ThirdParty.*, Thunk.*, or
                 carrying a CRT / EASTL / Lua name.  **These are C lanes**: the bar is naming the
                 upstream and the boundary, not explaining a body, so they are the largest and
                 cheapest population and the plan says to take them first.

    ARCH         unresolved architectural functions.  Everything else: this game's own routines,
                 dispatchers, adapters and callbacks.  **These are the expensive ones**, and their
                 size distribution is printed because a 12-byte adapter and a 3 KB dispatcher are
                 not the same unit of work.

A tag is evidence of shape, not of disposition
----------------------------------------------
**A C-candidate is a candidate and nothing more.**  Nothing here dispositions anything: this tool
has no declaration surface and writes nothing.  A function moves out of the frontier only when a
page declares it, with a note that meets the bar, and `check_dispositions.py` accepts the row.
The `GFZ.V121.CodeDomain` tags come from the checkpoint export, so a bucket here inherits whatever
that classifier got wrong, which is the reason these counts are called candidates in every line of
the output.

Usage
-----
    python frontier_census.py --db "Database/FFXII TZA"
    python frontier_census.py --db "Database/FFXII TZA" --list C --limit 40
"""
import argparse
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_dispositions as cd          # noqa: E402
import uc1_band                          # noqa: E402

FUNCS = os.path.join(HERE, "..", "..", "work", "graph", "functions.tsv")

MIDDLEWARE_TAGS = (".Phyre.", ".ThirdParty.", ".Thunk.")
MIDDLEWARE_NAMES = ("EASTL", "eastl", "lua", "Lua", "Phyre", "PhyreEngine",
                    "std::", "operator new", "operator delete", "_Cnd_", "_Mtx_", "_Thrd_")
CRT_NAMES = ("memcpy", "memset", "memmove", "strlen", "strcmp", "strchr", "sqrtf", "sprintf",
             "malloc", "free", "realloc", "calloc", "wcs", "mbs", "_chkstk", "atexit")


def load_rows(path=None):
    path = path or FUNCS
    out = {}
    with io.open(path, encoding="utf-8", errors="replace") as f:
        h = f.readline().rstrip("\n").split("\t")
        idx = {k: i for i, k in enumerate(h)}
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < len(h):
                p += [""] * (len(h) - len(p))
            try:
                out[int(p[idx["entry"]], 16)] = p
            except ValueError:
                pass
    return out, idx


def bucket(entry, row, idx):
    """C-candidate or ARCH. Deliberately conservative: a doubtful case stays ARCH."""
    if row is None:
        return "ARCH"
    tags = row[idx["tags"]] or ""
    name = row[idx["name"]] or ""
    if any(t in tags for t in MIDDLEWARE_TAGS):
        return "C"
    if any(n in name for n in MIDDLEWARE_NAMES):
        return "C"
    if any(name == n or name.startswith(n) for n in CRT_NAMES):
        return "C"
    if row[idx["thunk"]] not in ("", "0", "false", "False"):
        return "C"
    return "ARCH"


def size_bands(sizes, addrs):
    b = collections.Counter()
    for a in addrs:
        n = sizes[a]
        b["1 tiny   <= 16 B" if n <= 16 else
          "2 small  <= 64 B" if n <= 64 else
          "3 medium <= 256 B" if n <= 256 else
          "4 large  <= 1 KB" if n <= 1024 else
          "5 huge    > 1 KB"] += 1
    return b


def frontier_set(db=None, sizes=None):
    """The live EC-7 frontier: every function neither directly dispositioned (A) nor a declared
    family member. This is what the untracked arch_frontier.txt / c_frontier.txt files were a
    materialisation of -- callers should compute it here rather than read a cache."""
    db = db or cd.DEFAULT_DB
    if sizes is None:
        sizes = cd.load_functions()
    a_set, _eo, _ai, _da = cd.measure_a(db, sizes)
    declared = set()
    # accepted families are reported by count only, so re-read them for membership
    for doc, parts in cd.parse_families(db):
        if len(parts) >= 5 and parts[1] in cd.LETTERS:
            try:
                declared |= set(cd.read_members(doc, parts[2]))
            except Exception:
                pass
    # UC-1 frontier bodies are frontier BY RULING: a family declaration naming
    # one is refused in evaluate, so it cannot remove the body from the
    # frontier here either.
    declared -= uc1_band.frontier_starts()
    return set(sizes) - a_set - declared


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--list", choices=("C", "ARCH"), default=None)
    ap.add_argument("--limit", type=int, default=30)
    a = ap.parse_args(argv)
    db = a.db or cd.DEFAULT_DB

    sizes = cd.load_functions()
    rows, idx = load_rows()
    r = cd.evaluate(db, sizes)
    frontier = sorted(frontier_set(db, sizes))

    groups = collections.defaultdict(list)
    for e in frontier:
        groups[bucket(e, rows.get(e), idx)].append(e)

    total = len(sizes)
    print("FFXII TZA - EC-7 frontier census (what is left, and in what shape)")
    print()
    print("  population                                    : %6d" % total)
    if r.get("band"):
        print("     post-2026-09-28: %d listed + %d UC-1 frontier; %d held"
              " (uncertainty, never counted)" % (r["band"]["listed"],
              r["band"]["frontier"], r["band"]["held"]))
    print("  A  direct semantic disposition   (measured)   : %6d  %5.2f%%"
          % (r["A"], 100.0 * r["A"] / total))
    print("  B  proven family disposition     (declared)   : %6d" % r["B"])
    print("  C  dispositioned                 (declared)   : %6d" % r["C"])
    print("  D  declared exception            (declared)   : %6d" % r["D"])
    print("  -" * 34)
    print("  FRONTIER                                      : %6d  %5.2f%%"
          % (len(frontier), 100.0 * len(frontier) / total))
    print()
    print("  and the frontier splits into two very different jobs:")
    print()
    cn, an = len(groups["C"]), len(groups["ARCH"])
    print("    C-CANDIDATE  middleware / library / generated : %6d  %5.1f%% of the frontier"
          % (cn, 100.0 * cn / max(len(frontier), 1)))
    print("                 bar: name the upstream and the boundary. Cheapest population.")
    print("    ARCH         unresolved architectural         : %6d  %5.1f%%"
          % (an, 100.0 * an / max(len(frontier), 1)))
    print("                 bar: explain it, or class-explain it with a reproduction test.")
    print()
    for label, key in (("C-candidate", "C"), ("architectural", "ARCH")):
        print("  %s by body size:" % label)
        for k, v in sorted(size_bands(sizes, groups[key]).items()):
            print("      %-20s %6d" % (k[2:], v))
        print()
    print("  largest tag groups inside the ARCHITECTURAL bucket - candidate B families,")
    print("  because a shared tag is a shared shape and a shared shape is what B is for:")
    tags = collections.Counter()
    for e in groups["ARCH"]:
        t = (rows[e][idx["tags"]] if e in rows else "") or "(untagged)"
        tags[t.split(";")[0][:58] or "(untagged)"] += 1
    for k, v in tags.most_common(12):
        print("      %-58s %6d" % (k, v))
    print()
    print("  NOTHING HERE IS A DISPOSITION. A function leaves the frontier only when a page")
    print("  declares it and check_dispositions.py accepts the row. These buckets are shape")
    print("  evidence drawn from the checkpoint's own tags, and inherit that classifier's errors.")

    if a.list:
        print()
        print("  first %d of the %s bucket:" % (a.limit, a.list))
        for e in groups[a.list][:a.limit]:
            nm = rows[e][idx["name"]] if e in rows else ""
            print("      %08X  %6d B  %s" % (e, sizes[e], nm[:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
