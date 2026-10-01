#!/usr/bin/env python3
"""overlay_drop_census.py - what does each uncommitted continuation overlay REMOVE from the file it rewrites?

OPUS, 2026-09-25. The external continuation sections (EXTERNAL-CONTINUATION.md SECTION-01..12)
are applied uncommitted to the shared worktree. Reviewed one by one, their corrections re-read
correctly against the image - and two of the first four rewrites silently dropped executed or
cited facts that HEAD carried. A correction that removes the evidence for what it keeps leaves the
file weaker, and a diff does not show that at a glance. This lists, per modified markdown file,
the citation tokens HEAD has and the worktree lost: 8-hex-digit addresses, EXP ids, invariant ids.

    overlay_drop_census.py [--db "Database/FFXII TZA"] [--out drops.tsv]

A dropped token is a QUESTION, not a verdict: a rewrite may restate a fact without its address,
or remove a claim that was wrong. Each needs a reader. Read-only; nothing is edited.
"""
import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys

TOKENS = (("address", re.compile(r"\b00[0-9A-F]{6}\b")),
          ("exp", re.compile(r"\bEXP-\d{3}\b")),
          ("invariant", re.compile(r"\b(?:I|WT|SS|AR|BU|U|R|Q)\d{1,2}\b")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join("Database", "FFXII TZA"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                          text=True).stdout.strip()
    db = os.path.join(root, a.db)
    touched = {}
    # SECTIONs 11-12 list their paths in modified_paths.json; 01-10 carry them inside
    # PATCH_MANIFEST.json in varying shapes - so every string ending in .md anywhere in either
    # manifest counts, which is robust to the shape and over-inclusive only by files the overlay
    # names without changing (those diff clean and are skipped below).
    def strings(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, dict):
            for k, v in x.items():
                yield from strings(k)
                yield from strings(v)
        elif isinstance(x, list):
            for v in x:
                yield from strings(v)
    for mp in glob.glob(os.path.join(db, "_experiments", "evidence", "continuation-section*",
                                     "*.json")):
        if os.path.basename(mp) not in ("modified_paths.json", "PATCH_MANIFEST.json"):
            continue
        sec = re.search(r"section(\d+)", mp).group(1)
        try:
            data = json.load(io.open(mp, encoding="utf-8"))
        except ValueError:
            continue
        for p in strings(data):
            p = p.replace("\\", "/")
            if not p.endswith(".md") or "_experiments/evidence/" in p:
                continue
            p = p.split("FFXII TZA/", 1)[-1]
            touched.setdefault(p, set()).add("S" + sec)
    rows = []
    for rel, secs in sorted(touched.items()):
        full = os.path.join(db, rel)
        gitpath = (a.db.replace("\\", "/") + "/" + rel)
        head = subprocess.run(["git", "show", "HEAD:" + gitpath], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", cwd=root).stdout
        if not head or not os.path.exists(full):
            continue
        wt = io.open(full, encoding="utf-8", errors="replace").read()
        if wt == head:
            continue
        for kind, rx in TOKENS:
            lost = sorted(set(rx.findall(head)) - set(rx.findall(wt)))
            for t in lost:
                rows.append((rel, ",".join(sorted(secs)), kind, t))
        print("%-78s %-9s words %5d -> %5d  lost: %s" % (
            rel[:78], ",".join(sorted(secs)), len(head.split()), len(wt.split()),
            " ".join("%s=%d" % (k, sum(1 for r in rows if r[0] == rel and r[2] == k))
                     for k, _ in TOKENS)))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("file\tsections\tkind\ttoken\n")
            for r in rows:
                f.write("\t".join(r) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
