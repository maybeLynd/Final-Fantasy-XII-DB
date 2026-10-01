#!/usr/bin/env python3
"""tools_provenance.py - what is in `Database/Tools/` that the database has never absorbed.

Charter §38 lists *"locate all existing research tools and historical work, import with
provenance"* as a first action, and it is still open. `research_import_gap.py` answers it for
`Collaboration/` prose (that is `ED-1`). **Nothing answered it for `Database/Tools/` itself**, which
holds the Ghidra toolchain, the GM160 evidence dumps and the handoff seals - 94 files that were
never added to git.

That is not a tidiness problem. **`COVERAGE.md` says its classified-coverage number is "regenerated
by `ReportV121Coverage.java`"**, the mission prompt's non-negotiables say *"update `GfzEnv.ps1`
after every certified checkpoint"*, and `AUDIT-LOG.md` cites `GfzEnv.ps1` as the authority on which
parent is certified. **A database whose numbers cite a tool the repository does not contain cannot
be reproduced from the repository.**

What this reports, per file
---------------------------
    kind        TOOL     .ps1 / .java / .py  - machinery a later session must be able to re-run
                EVIDENCE .tsv / .txt         - a dump produced by one of those tools
                HANDOFF  .md / .json         - a prior session's prose, seal or manifest
    cited       whether any database document names the file
    entries     8-hex tokens in the file that are real function entries in `functions.tsv`
    absorbed    of those, how many the database already cites
    gap         entries - absorbed, i.e. what importing this file could still add

**Every ratio prints its denominator**, and `entries` is deliberately *not* "addresses" - a token
that is not a function entry is not counted, because a coverage dump is full of eight-hex fields
that are sizes and offsets rather than addresses.

What it deliberately does not do
--------------------------------
It **does not judge whether a file's content is correct.** A GM160 evidence dump is a prior
session's claim about the binary, exactly like GFZ prose, and the mission prompt's order stands:
binary > fresh derivation > prior annotation. A high `gap` says *"this file names functions nobody
has written about"*, never *"import these findings"*. **They must still be read from the binary.**

It **does not measure prose absorption.** A handoff document can be fully absorbed and still name
functions the database does not cite, and a document can cite an address in passing without having
absorbed anything. `gap` is an attention proxy over function entries and nothing more.

Usage
-----
    python tools_provenance.py                       # report
    python tools_provenance.py --out <path.tsv>      # and write the side file
"""
import argparse
import collections
import hashlib
import io
import os
import re
import sqlite3
import sys
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
TOOLS = os.path.join(ROOT, "Database", "Tools")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
DBF = os.path.join(TOOLS, "work", "knowledge", "knowledge.sqlite")
FUNCS = os.path.join(TOOLS, "work", "graph_gn", "functions.tsv")

# The subtrees that were never added to git. `work/`, `parent/` and `radare2/` are gitignored on
# purpose (scratch, an 82 MB GZF, a third-party distribution) and are not this tool's business.
SUBTREES = ["docs", "evidence", "ghidra", os.path.join("analysis-kit", "historical")]

HEX8 = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")

KIND = {".ps1": "TOOL", ".java": "TOOL", ".py": "TOOL",
        ".tsv": "EVIDENCE", ".txt": "EVIDENCE",
        ".md": "HANDOFF", ".json": "HANDOFF"}


def walk(sub):
    base = os.path.join(TOOLS, sub)
    for root, _dirs, files in os.walk(base):
        for f in sorted(files):
            p = os.path.join(root, f)
            yield p, os.path.relpath(p, TOOLS).replace(os.sep, "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DBF)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    if not os.path.exists(a.db):
        sys.stderr.write("no index at %s - run `knowledge_db.py build`\n" % a.db)
        return 2
    import knowledge_db as _kd
    _status, _stale, _meta = _kd.freshness_report(a.db)
    if _status != "current":
        print("index %s (built %s, pin=%s) - figures below read a dated snapshot:"
              % (_status.upper(), _meta.get("built_at"),
                 (_meta.get("pinned_commit") or "worktree")[:12]))
        for _line in _stale[:10]:
            print("  STALE " + _line)

    conn = sqlite3.connect(a.db)
    cited = set(r[0] for r in conn.execute(
        "SELECT DISTINCT resolved_entry FROM citations WHERE resolved_entry IS NOT NULL"))

    entries = set()
    for ln in io.open(a.funcs, encoding="utf-8", errors="replace"):
        p = ln.split("\t", 1)
        if len(p) > 1 and re.match(r"^[0-9A-F]{8}$", p[0]):
            entries.add(p[0])

    # Every filename mentioned anywhere in the database, so "is this file cited" is one pass.
    named = set()
    for root, dirs, files in os.walk(DB):
        for f in files:
            if not f.endswith((".md", ".tsv")):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for tok in re.findall(r"[A-Za-z0-9_.\-]+\.(?:ps1|java|py|tsv|txt|json|md)", t):
                named.add(tok)

    rows = []
    for path, rel in sorted(x for sub in SUBTREES for x in walk(sub)):
        blob = open(path, "rb").read()
        text = blob.decode("utf-8", "replace")
        ext = os.path.splitext(rel)[1].lower()
        found = set(m.group(1).upper() for m in HEX8.finditer(text)) & entries
        rows.append({
            "rel": rel,
            "kind": KIND.get(ext, "OTHER"),
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "cited": os.path.basename(rel) in named,
            "entries": len(found),
            "absorbed": len(found & cited),
        })

    tot = collections.Counter()
    for r in rows:
        tot[r["kind"]] += 1
        tot[r["kind"] + ":bytes"] += r["bytes"]

    print("Charter §38: existing research tools and historical work under `Database/Tools/`.")
    print("94-file corpus that git has never tracked. `gap` = function entries a file names that")
    print("NO database document cites. It is an attention proxy, not a list of findings to trust.")
    print()
    print("  %-52s %-8s %7s %5s %6s %8s %5s" %
          ("file", "kind", "bytes", "cited", "entries", "absorbed", "gap"))
    for r in sorted(rows, key=lambda x: (-(x["entries"] - x["absorbed"]), x["rel"])):
        gap = r["entries"] - r["absorbed"]
        print("  %-52s %-8s %7d %5s %6d %8d %5d"
              % (r["rel"][-52:], r["kind"], r["bytes"], "yes" if r["cited"] else "-",
                 r["entries"], r["absorbed"], gap))

    print()
    for k in ("TOOL", "EVIDENCE", "HANDOFF", "OTHER"):
        if tot[k]:
            print("  %-9s %3d file(s), %8d bytes" % (k, tot[k], tot[k + ":bytes"]))
    ncited = sum(1 for r in rows if r["cited"])
    print()
    print("  named by a database document : %d of %d" % (ncited, len(rows)))
    allf = set()
    for r in rows:
        allf.add(r["rel"])
    union_entries = set()
    union_gap = set()
    for path, rel in sorted(x for sub in SUBTREES for x in walk(sub)):
        text = open(path, "rb").read().decode("utf-8", "replace")
        f = set(m.group(1).upper() for m in HEX8.finditer(text)) & entries
        union_entries |= f
        union_gap |= (f - cited)
    print("  distinct function entries    : %d" % len(union_entries))
    print("  ...cited by no document      : %d  (%.1f %% of %d)"
          % (len(union_gap), 100.0 * len(union_gap) / len(union_entries) if union_entries else 0,
             len(union_entries)))
    print()
    print("  A high gap is a REASON TO READ THE BINARY, never a finding to copy across.")

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("file\tkind\tbytes\tsha256\tcited_by_a_document\t"
                     "function_entries\tabsorbed\tgap\n")
            for r in sorted(rows, key=lambda x: x["rel"]):
                fh.write("%s\t%s\t%d\t%s\t%s\t%d\t%d\t%d\n"
                         % (r["rel"], r["kind"], r["bytes"], r["sha256"],
                            "yes" if r["cited"] else "no", r["entries"], r["absorbed"],
                            r["entries"] - r["absorbed"]))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
