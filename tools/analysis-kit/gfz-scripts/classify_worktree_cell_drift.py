#!/usr/bin/env python3
"""classify_worktree_cell_drift.py - is an uncommitted TSV edit new work or a revert of committed work?

OPUS, 2026-09-24. The shared worktree's `_types/types.tsv` differed from HEAD in 137 rows, and the
differences were of two kinds that look identical in a diff: cells carrying NEW information nobody
has committed, and cells that had quietly gone BACK to a value an earlier commit had replaced - the
signature of a whole file written from an older base. Committing the first is publication;
committing the second destroys a peer's committed work. This tells them apart, cell by cell, and
edits nothing.

For every (key, column) where the worktree differs from HEAD it walks the file's committed history
(newest first) and classifies the worktree value as:

  REVERT     equals the value that cell held in an EARLIER commit - HEAD moved on, the worktree
             went back. Committing it undoes the commit named in `superseded_by`.
  NEW        appears in no committed version of that cell - someone's uncommitted work.
  ROW-ADDED / ROW-DELETED   the key exists on one side only.

    classify_worktree_cell_drift.py --file "Database/FFXII TZA/_types/types.tsv" [--depth 80]
                                    [--out drift.tsv]

The key is column 0 (fields.tsv: pass --key type,offset). Negative space: a NEW cell may still be
stale relative to a commit outside --depth; a REVERT is exact.
"""
import argparse
import csv
import io
import subprocess
import sys


def rows(text, keycols):
    r = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if not r:
        return [], {}
    h = r[0]
    ki = [h.index(k) for k in keycols] if keycols else [0]
    out = {}
    for x in r[1:]:
        if x and len(x) > max(ki):
            out[tuple(x[i] for i in ki)] = x
    return h, out


def git(*a):
    return subprocess.run(("git",) + a, capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="repo-relative path")
    ap.add_argument("--key", default="", help="comma list of key columns (default: column 0)")
    ap.add_argument("--depth", type=int, default=80)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    keycols = [k for k in a.key.split(",") if k]
    root = git("rev-parse", "--show-toplevel").strip()
    h, head = rows(git("show", "HEAD:" + a.file), keycols)
    _, wt = rows(io.open(root + "/" + a.file, encoding="utf-8").read(), keycols)
    commits = git("log", "--format=%h", "-n", str(a.depth), "--", a.file).split()
    history = []                       # [(commit, {key: row})], newest first; [0] is HEAD's version
    for c in commits:
        history.append((c, rows(git("show", "%s:%s" % (c, a.file)), keycols)[1]))
    out = []
    for k in sorted(set(head) | set(wt)):
        if k not in head:
            out.append((k, "*", "ROW-ADDED", "", ""))
            continue
        if k not in wt:
            out.append((k, "*", "ROW-DELETED", "", ""))
            continue
        for i, col in enumerate(h):
            hv = head[k][i] if i < len(head[k]) else ""
            wv = wt[k][i] if i < len(wt[k]) else ""
            if hv == wv:
                continue
            cls, sup = "NEW", ""
            newer = commits[0] if commits else ""
            for c, snap in history[1:]:
                old = snap.get(k)
                ov = (old[i] if old and i < len(old) else None)
                if ov == wv:
                    cls, sup = "REVERT", newer
                    break
                if ov != hv:
                    pass
                newer = c
            out.append((k, col, cls, sup, wv[:120]))
    from collections import Counter
    c = Counter((o[2], o[1]) for o in out)
    for (cls, col), n in sorted(c.items()):
        print("  %-12s %-16s %d" % (cls, col, n))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("key\tcolumn\tclass\tsuperseded_by\tworktree_value_head\n")
            for k, col, cls, sup, v in out:
                f.write("%s\t%s\t%s\t%s\t%s\n" % ("|".join(k), col, cls, sup, v.replace("\t", " ")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
