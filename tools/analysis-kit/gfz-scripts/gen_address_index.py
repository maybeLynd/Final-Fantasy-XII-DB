#!/usr/bin/env python3
"""gen_address_index.py - regenerate ADDRESS-INDEX.md from the documents themselves.

Why this exists
---------------
`ADDRESS-INDEX.md` carries its own maintenance note:

> *"this file is hand-maintained while the database is small. Once enough documents exist, generate
> it by scanning the `.md` files for 8-hex-digit tokens..."*

**That threshold passed long ago and nobody noticed.** On 2026-09-03 the index held **74 addresses**
while the database cited **6,504 distinct functions across 102 documents** -- about 1 % coverage --
and none of the ten documents written that day appeared in it at all.

> **A hand-maintained index that has fallen two orders of magnitude behind is worse than no index: a
> reader who looks up an address and finds nothing concludes the database does not cover it.**

What it does
------------
Scans every document under a numbered category folder for backticked 8-hex-digit tokens, resolves
each to the function whose body contains it (so an interior address indexes to its function), and
writes one row per address with every document that cites it.

**An address cited by several documents gets one row listing all of them** -- that is the case a
reader most needs, and the hand-maintained file could not express it.

Deliberately NOT done
---------------------
It does not name the functions. The ledger's names are mechanical (`FUN_...`) for most of these, and
**a generated index asserting a name would be asserting something no document said.** Names belong in
documents; this file answers *"who talks about this address"* and nothing else.
"""
import argparse
import bisect
import collections
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
ADDR = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")
# A .tsv column holds bare hex with no backticks, so the markdown pattern matches nothing
# there. Using one extractor for both formats produced a confident "0 table-only addresses"
# that contradicted an independent count of 2,000 - a zero that meant "wrong query", not
# "nothing present". Different source formats need different extractors.
ADDR_BARE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])")
# A document that writes `FUN_002f9860` is talking about 002F9860, and the backtick pattern
# cannot see it -- the address is inside a token, not filling the span. That is the form the
# GFZ ledger gives every UNNAMED function, so the misses concentrated exactly on the
# functions an index is most needed for. Measured 2026-09-08: 375 authored functions were
# discussed in the corpus and absent from every citation instrument.
ADDR_SYMBOL = re.compile(r"(?:FUN|LAB|DAT|PTR|SUB|UNK|thunk_FUN)_(0[0-9A-Fa-f]{7})", re.I)
# A sha256 opens with eight hex digits. Every document states the exe hash, so leaving these
# in would index a citation of 73461D08 into every single file.
ADDR_LONGHEX = re.compile(r"\b(0[0-9A-Fa-f]{7})[0-9A-Fa-f]{8,}")
FENCED = re.compile(r"```.*?```", re.S)


def load(path):
    entries, sizes = [], {}
    f = io.open(path, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                e = int(p[0], 16)
                entries.append(e)
                sizes[e] = int(p[2])
            except ValueError:
                pass
    entries.sort()
    return entries, sizes


def tracked_only(db):
    """The files git has under `db`. -> set of db-relative paths, or None if git cannot answer.

    THE INDEX DESCRIBES THE REPOSITORY, AND THIS WALK DESCRIBED THE WORKING TREE. An untracked file
    put its addresses into one agent's regeneration and not another's, so two agents regenerating
    this canonical file produced different content and overwrote each other - observed 2026-09-14,
    where nineteen addresses cited only by an untracked `msvc-runtime-tail.tsv` were written by one
    regeneration and removed by the next two. A row nobody else can produce is not a row the index
    owes. When git cannot answer, the walk falls back to the old behaviour rather than silently
    indexing nothing.
    """
    import subprocess
    # THE AMBIENT ENVIRONMENT IS STRIPPED, AND THAT IS THE POINT OF THESE TWO LINES. Measured in
    # this repository: with GIT_DIR set and no GIT_WORK_TREE, `git ls-files` run inside the db
    # answers from the REPOSITORY ROOT (`.claude/rules/...`), so not one path matches the
    # db-relative path the walk computes and every file is skipped as untracked. GIT_INDEX_FILE
    # is stripped for the same reason - `publish_paths.sh` sets it - though a private index
    # seeded by read-tree was tested and does list everything.
    env = dict(os.environ)
    for var in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE"):
        env.pop(var, None)
    try:
        r = subprocess.run(["git", "ls-files", "-z"], cwd=db, capture_output=True, timeout=180,
                           env=env)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    got = {q.decode("utf-8", "replace").replace("\\", "/") for q in r.stdout.split(b"\0") if q}
    # AN EMPTY ANSWER IS "GIT CANNOT ANSWER", NOT "NOTHING IS TRACKED". A database with zero
    # tracked files is not a state worth serving, and serving it empties the index.
    return got or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--functions", default=FUNCS)
    ap.add_argument("--force", action="store_true",
                    help="write even if the new index has under half the rows of the old one")
    a = ap.parse_args()

    entries, sizes = load(a.functions)
    by_entry = collections.defaultdict(set)     # cited by a prose document
    by_table = collections.defaultdict(set)     # recorded only in a side file
    docs = tables = 0
    tracked = tracked_only(a.db)
    skipped_untracked = 0

    # THE WALK IS COLLECTED BEFORE IT IS FILTERED, so the git answer can be checked against it.
    found = []
    for root, _d, files in os.walk(a.db):
        top = os.path.relpath(root, a.db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for fn in sorted(files):
            if fn.endswith(".md") or fn.endswith(".tsv"):
                found.append((root, fn))

    # A WRONG --db IS SILENT: os.walk on a path that does not exist yields nothing and the
    # generator used to write a stub over the canonical file at exit 0. That is how a peer
    # committed ec044d8f. Zero files is a bad argument, not an empty corpus.
    if not found:
        sys.stderr.write("REFUSING TO WRITE: no .md or .tsv under a numbered category in %s\n"
                         "That is a wrong --db, not an empty corpus. Nothing was written.\n"
                         % os.path.abspath(a.db))
        return 3

    # AND THE GIT ANSWER IS CHECKED AGAINST THE WALK. With GIT_DIR set and no GIT_WORK_TREE, git
    # answers from the repository root and matches NOTHING here; skipping every file would empty
    # the index. An answer that disagrees with the tree this badly is about the query.
    if tracked is not None:
        rels = {os.path.relpath(os.path.join(r, f), a.db).replace(os.sep, "/") for r, f in found}
        hit = len(rels & tracked)
        if hit * 2 < len(rels):
            sys.stderr.write("IGNORING git ls-files: it covers %d of the %d files walked. The "
                             "paths are not\ncomparable - check GIT_DIR/GIT_WORK_TREE. Falling "
                             "back to the working tree.\n" % (hit, len(rels)))
            tracked = None

    for root, fn in found:
        # .tsv side files are indexed too, but kept in a SEPARATE bucket. A verb-table row
        # is a transcription, not an explanation -- the database's own rule, from
        # check_named_not_cited.py. Folding the two together would inflate coverage; leaving
        # the tables out entirely leaves 2,000 recorded addresses unfindable. So: findable,
        # and marked as what they are.
        is_md = fn.endswith(".md")
        is_tsv = fn.endswith(".tsv")
        if not (is_md or is_tsv):
            continue
        if is_md:
            docs += 1
        else:
            tables += 1
        rel = os.path.relpath(os.path.join(root, fn), a.db).replace(os.sep, "/")
        # NOT IN THE REPOSITORY, NOT IN THE INDEX - see tracked_only().
        if tracked is not None and rel not in tracked:
            skipped_untracked += 1
            docs -= 1 if is_md else 0
            tables -= 0 if is_md else 1
            continue
        t = io.open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
        bucket = by_entry if is_md else by_table
        t = ADDR_LONGHEX.sub(" ", t)
        if is_md:
            # Three forms, all of them unambiguous: a code span holding just the
            # address, a GFZ symbol containing it, and a quoted disassembly listing.
            # A bare address in a SENTENCE is deliberately NOT one of them -- it
            # cannot be told apart from a constant of the same width, and it earned
            # its exclusion: `+0x118 = 0x003C0000` reads as a citation of
            # FUN_003bfff0, and `0x00555556` (divide-by-3 magic) as one of 00555400.
            hexes = ADDR.findall(t) + ADDR_SYMBOL.findall(t)
            hexes += [h for blk in FENCED.findall(t) for h in ADDR_BARE.findall(blk)]
        else:
            hexes = ADDR_BARE.findall(t)
        for h in hexes:
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i >= 0 and entries[i] <= v < entries[i] + sizes[entries[i]]:
                bucket[entries[i]].add(rel)

    shared = sum(1 for v in by_entry.values() if len(v) > 1)
    out = []
    out.append("# Address index")
    out.append("")
    out.append("Address -> the documents that cite it. Ghidra image base `0x00120000`.")
    out.append("")
    out.append("**GENERATED — do not hand-edit.** `Tools/analysis-kit/gfz-scripts/gen_address_index.py`")
    out.append("")
    out.append("This file was hand-maintained and held **74 addresses** while the database cited")
    out.append("**%d distinct functions across %d documents** — about 1 %% coverage, with none of the"
               % (len(by_entry), docs))
    out.append("documents written on 2026-09-03 appearing at all. Its own header had said to generate")
    out.append("it *\"once enough documents exist\"*, and that threshold passed unnoticed.")
    out.append("")
    out.append("> **A hand-maintained index two orders of magnitude behind is worse than no index: a")
    out.append("> reader who looks up an address and finds nothing concludes the database does not")
    out.append("> cover it.**")
    out.append("")
    out.append("**Interior addresses resolve to their containing function**, so a citation of an")
    out.append("instruction indexes under the function it is in. **It does not name functions** — the")
    out.append("ledger's names are mechanical for most of these, and a generated index asserting a name")
    out.append("would assert something no document said. This answers *who talks about this address*")
    out.append("and nothing else.")
    out.append("")
    table_only = sorted(e for e in by_table if e not in by_entry)
    out.append("**%d addresses cited by a document · %d by more than one.**" % (len(by_entry), shared))
    out.append("")
    out.append("**A further %d addresses are recorded only in a `.tsv` side file** and are listed "
               "below the main table, marked `table only`. **A table row is a transcription, not an "
               "explanation** — it makes the address findable and asserts nothing about whether the "
               "database understands it. They are deliberately *not* counted as cited." % len(table_only))
    out.append("")
    out.append("| Address | Documents |")
    out.append("|---|---|")
    for e in sorted(by_entry):
        ds = sorted(by_entry[e])
        cell = " · ".join("[%s](../%s)" % (os.path.basename(d)[:-3], d) for d in ds)
        if e in by_table:
            cell += " · *(also in %s)*" % ", ".join(os.path.basename(x) for x in sorted(by_table[e]))
        out.append("| `%08X` | %s |" % (e, cell))
    out.append("")
    out.append("## Recorded only in a side file — %d addresses" % len(table_only))
    out.append("")
    out.append("| Address | Side file |")
    out.append("|---|---|")
    for e in table_only:
        out.append("| `%08X` | %s — *table only* |"
                   % (e, ", ".join(os.path.basename(x) for x in sorted(by_table[e]))))
    out.append("")
    # A REGENERATION MAY NOT DELETE THE FILE. Not a quality threshold - ordinary drift of a few
    # hundred rows passes untouched in both directions - but a floor under catastrophe, because
    # this tool once wrote 4 lines over 26,094 and exited 0. See ec044d8f.
    if not a.force and os.path.isfile(a.out):
        try:
            prev = io.open(a.out, encoding="utf-8", errors="replace").read()
        except OSError:
            prev = ""
        had = len(re.findall(r"^\|\s*`0[0-9A-Fa-f]{7}`", prev, re.M))
        now = len(by_entry) + len(table_only)
        if had and now * 2 < had:
            sys.stderr.write(
                "REFUSING TO WRITE: %s holds %d rows and this run produced %d - less than half.\n"
                "A regeneration that empties a canonical index is a defect in the run, not news\n"
                "about the corpus; ec044d8f committed 4 lines over 26,094 that way. If the shrink\n"
                "is real, pass --force.\n" % (a.out, had, now))
            return 3
    io.open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("wrote %s: %d addresses from %d documents, %d shared; "
          "%d more recorded only in %d side file(s)"
          % (a.out, len(by_entry), docs, shared, len(table_only), tables))
    return 0


if __name__ == "__main__":
    sys.exit(main())
