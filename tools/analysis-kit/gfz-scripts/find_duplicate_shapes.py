#!/usr/bin/env python3
"""Which declared types are the SAME shape, described more than once?

WHY THIS MATTERS AND IT IS NOT TIDINESS. A reconstruction emits one struct per declared type. If
two types are the same structure reached by different routes, the output has two incompatible
definitions of one thing, and a change to one silently diverges from the other. The store already
holds a case: RenderResourceRoot embeds ONE bank descriptor three times, at +0x0, +0x60 and
+0xF0, and all three are declared separately - 18 of 19 rows identical in offset, size and name,
and the one row they disagreed on was WRONG on two of them.

THE TEST IS A RUN OF IDENTICAL ROWS FROM OFFSET ZERO. Two types share a prefix when their rows
agree on offset, size AND name for every row up to some offset. Name is included deliberately:
offset-and-size agreement alone matches any two structs that happen to start with a pointer and
two dwords, which is most of them. Agreeing on the NAMES as well means the same reader named
them the same way from the same evidence.

A shared prefix is not automatically a defect - a genuine base class, or a header a family
deliberately shares, is the same finding stated positively. What it is never is invisible.

WHAT IT FOUND ON THE DAY IT WAS WRITTEN, four groups and every one of them worth the run:

  * the three bank descriptors, ALL TWENTY ROWS identical through +0x60. RenderResourceEntryBank
    is 20 rows and ends there, so it IS the descriptor; the other two extend it;
  * PInstanceListHeader and PhyreInstanceListHeader - nine rows, identical, both ending at 0x24.
    Not a prefix: the SAME TYPE DECLARED TWICE, differing only in ctype spelling;
  * PClusterHeaderBase and PhyreClusterHeader - 18 identical rows through +0x48, the base and
    the whole, with the relationship declared nowhere a tool can follow;
  * BattleMenuChildWidget1620 and BattleMenuWidget2DC0 - nine rows through +0x9C, which is
    Widget's own header. Both ARE widgets, so this group is the check agreeing with something
    already known, and it is the reason the threshold is not set lower.

THE CTYPE SPELLING IS DELIBERATELY NOT COMPARED, and the instance-list pair shows why. Their
only difference in nine rows is `unsigned int` against `uint32`, because one layout came from
Phyre's own reflection registration, which names C++ types, and the other from the file format.
Comparing spellings would have hidden the duplicate behind a difference that is really two
independent derivations agreeing - which is corroboration, not disagreement.
"""
import collections
import csv
import io
import os
import sys

sys.path.insert(0, "Database/Tools/analysis-kit/gfz-scripts")
import kit_paths as KP  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
MIN_ROWS = 6
CONTROL = {"RenderResourceEntryBank", "RenderStrideC0Bank", "RenderModelInstanceContainer"}


def main():
    rows = collections.defaultdict(list)
    for r in csv.DictReader(io.open(D + "fields.tsv", encoding="utf-8"), delimiter="\t"):
        try:
            rows[r["type"]].append((int(r["offset"], 16), int(r["size"]), r["name"]))
        except ValueError:
            pass
    for v in rows.values():
        v.sort()

    # group by the longest identical prefix, greedily: bucket on the first MIN_ROWS rows, then
    # extend within each bucket.
    buckets = collections.defaultdict(list)
    for t, v in rows.items():
        if len(v) >= MIN_ROWS:
            buckets[tuple(v[:MIN_ROWS])].append(t)

    groups = []
    for key, types in buckets.items():
        if len(types) < 2:
            continue
        n = MIN_ROWS
        while all(len(rows[t]) > n for t in types) and \
                len({rows[t][n] for t in types}) == 1:
            n += 1
        groups.append((n, rows[types[0]][n - 1][0] + rows[types[0]][n - 1][1], sorted(types)))

    ctrl = [g for g in groups if CONTROL.issubset(set(g[2]))]
    print("CONTROL - the three bank descriptors group together: %s"
          % ("PASS" if ctrl else "FAIL"))
    if not ctrl:
        print("\ncontrol failed - output refused")
        return 2
    print("  control passes - the absences below are meaningful\n")

    print("TYPES SHARING AN IDENTICAL PREFIX OF >= %d ROWS: %d group(s)" % (MIN_ROWS, len(groups)))
    for n, end, types in sorted(groups, key=lambda g: -g[0]):
        print("\n  %d rows, through +0x%X:" % (n, end))
        for t in types:
            print("      %-38s %d row(s) total" % (t, len(rows[t])))
        diff = []
        for t in types:
            if len(rows[t]) > n:
                diff.append("%s -> +0x%03X %s" % (t, rows[t][n][0], rows[t][n][2]))
            else:
                diff.append("%s -> ends" % t)
        print("      first divergence: %s" % "; ".join(diff))


if __name__ == "__main__":
    sys.exit(main() or 0)
