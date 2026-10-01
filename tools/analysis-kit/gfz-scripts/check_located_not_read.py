#!/usr/bin/env python3
"""check_located_not_read.py - functions the database has named but may never have opened.

Why this exists
---------------
On 2026-09-03 a session found `BattleStats_HasRequiredLicenseForAction` **named, located, cited --
and never read**.  The document had put a name on the door and stopped, and the section beside it
said flatly that the layout was not established.  **Every gate this project runs called that
document healthy**: the address resolved, the link worked, the name was in the index.

> **Located is not read, and no checker here could tell the difference.**

This one tries.  The signal is cheap and honest: **a function that has actually been read usually
gets interior addresses cited** -- an instruction anchor, a branch, a store, the offset a field is
read at.  A function that was merely located gets its entry cited and nothing else.

So: for every function the database cites, ask whether any document ever cites an address *inside*
its body.  Entry-only, on a large function, is the shape of a name on a door.

What this is NOT
----------------
**It is a suspicion, not a defect**, and the false positives are real and predictable:

  * a small function whose whole behaviour fits in one sentence needs no interior anchor;
  * a function cited only to say something *about* it ("this is one of 13 callers");
  * a genuine read written in prose, with the anchors carried by a decompiled listing rather
    than by backticked addresses.

**One of those false positives has now fired and been measured.** `0022A0B0` sat on the cut with
seven citations, every one at its entry. It had been read thoroughly; the reader simply had no
occasion to cite an interior address. An independent re-derivation confirmed its published memory
budget in full -- nine ids, nine sizes, the alignment tail, two unregistered allocations, the absent
id 10 -- and then **supplied the interior addresses so it would stop being a false positive.**

> **The cure for a false positive on this cut is not to relax the cut; it is to cite the evidence the
> document already rests on.** An interior anchor makes a row checkable rather than merely stated,
> which is what the cut is really asking for.

That is why it ranks by **body size** and prints a threshold rather than a verdict, and why it
exits 0 by default.  **A checker that called these defects would be asserting a check that never
ran** -- exactly the failure it exists to catch.

Usage
-----
    python check_located_not_read.py --db "Database/FFXII TZA" --min-size 400
    python check_located_not_read.py --self-test
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
SSE_CENSUS = os.path.join(KP.ROOT, "Database", "Tools", "work", "h78", "sse_loop_census.tsv")


def load_sse(path):
    """entry -> (instrs, sse_moves, backward_jumps), or {} if the census is absent.

    **A large SSE-move count against almost no backward jumps is never a processing pass** -- it is
    a big structure snapshotted to the stack, modified and written back.  That shape identified the
    text cluster as one family *before* any of it was opened, which is a stronger claim than
    bytes-per-line can make: bytes-per-line ranks by how little we SAID, this ranks by what the
    function IS.  The two are close to orthogonal, and that is the useful case.

    A population note that came with the census and belongs beside any figure taken from it:
    `sse_moves` counts **movups movss movaps movdqu movdqa movupd movapd**.  Hand counts of
    `movups` alone, or of `movups`+`movss`, are *different populations, not different
    measurements* -- do not quote one beside the other.
    """
    out = {}
    try:
        f = io.open(path, encoding="utf-8", errors="replace")
    except IOError:
        return out
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 5:
            continue
        try:
            out[int(p[0], 16)] = (int(p[2]), int(p[3]), int(p[4]))
        except ValueError:
            continue
    return out
ADDR = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")


# **"We have not documented it" and "it is not ours to document" are different states**, and until
# 2026-09-03 this tool could not tell them apart -- the same distinction as *not measured* versus
# *contradicts*.  The ledger already knows: a function tagged into a vendor or compiler code domain
# is library or compiler output, not engine code.  Marking them is not the same as hiding them: a
# CRT function on a high-SSE list is still a true observation, it is just not a gap in this database.
NOT_OURS = ("Microsoft", "ThirdParty", "CompilerGenerated")
DOMAIN = re.compile(r"GFZ\.V121\.CodeDomain\.([A-Za-z0-9_.]+)")


def load(path):
    entries, sizes, names, vendor = [], {}, {}, {}
    f = io.open(path, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                e = int(p[0], 16)
            except ValueError:
                continue
            entries.append(e)
            sizes[e] = int(p[2])
            names[e] = p[1]
            doms = DOMAIN.findall(p[8]) if len(p) > 8 else []
            hit = [d for d in doms if d.startswith(NOT_OURS)]
            vendor[e] = hit[0].split(".")[0] if hit else ""
    entries.sort()
    return entries, sizes, names, vendor


FENCE = re.compile(r"^\s*(```|~~~)", re.M)
BARE = re.compile(r"(?<![0-9A-Fa-f])(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")
SYMBOL = re.compile(r"(?:FUN|LAB|DAT|PTR|SUB|UNK|thunk_FUN)_(0[0-9A-Fa-f]{7})", re.I)


def cited_addresses(text):
    """Backticked addresses anywhere, PLUS bare ones inside code fences.

    Found by use, 2026-09-03: a document whose evidence is a disassembly listing writes its
    interior addresses **inside a fence, unbackticked** -- which is the most likely place for an
    interior anchor to live.  Requiring a backtick made every such document look unread, and the
    first one to expose it was this checker's own author's.

    > **The instrument could not see the evidence in the form the evidence is usually written in.**
    """
    out = set(ADDR.findall(text))
    # 2026-09-08, the same failure one form later: a document that writes `FUN_002f9860` is
    # citing 002F9860, and neither pattern above can see it, because the address is inside a
    # token rather than filling a span. That is the GFZ ledger's spelling for every UNNAMED
    # function -- so the form was missed precisely where a citation instrument is most needed.
    out |= set(SYMBOL.findall(text))
    fenced, buf = False, []
    for line in text.split(chr(10)):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            buf.append(line)
    out |= set(BARE.findall(chr(10).join(buf)))
    return out


def classify(texts, entries, sizes):
    """-> {entry: [n_entry_citations, n_interior_citations, {docs}]}"""
    seen = collections.defaultdict(lambda: [0, 0, set()])
    for rel, t in texts:
        for h in cited_addresses(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if not (e <= v < e + sizes[e]):
                continue
            seen[e][0 if v == e else 1] += 1
            seen[e][2].add(rel)
    return seen


SELF_ENTRIES = [0x1000, 0x2000]
SELF_SIZES = {0x1000: 900, 0x2000: 900}
SELF_TEXTS = [("a.md", "The check is `00001000`, named and cited, and that is all we say.\n"),
              ("b.md", "`00002000` loads at `00002014` and stores at `0000202C`.\n")]


def self_test():
    seen = classify(SELF_TEXTS, SELF_ENTRIES, SELF_SIZES)
    a, b = seen[0x1000], seen[0x2000]
    if not (a[0] == 1 and a[1] == 0 and b[0] == 1 and b[1] == 2):
        print("SELF-TEST FAILED: %r" % dict(seen))
        return 1
    print("self-test ok: entry-only read as located, interior anchors read as read")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--functions", default=FUNCS)
    ap.add_argument("--min-size", type=int, default=400)
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--min-docs", type=int, default=3)
    ap.add_argument("--min-leaned-size", type=int, default=300)
    ap.add_argument("--sse-census", default=SSE_CENSUS,
                    help="TSV of entry/body_bytes/instrs/sse_moves/backward_jumps/name. Adds a "
                         "SECOND ranking: SSE-heavy and loop-free, which finds what we MIS-TYPED "
                         "rather than what we under-described.")
    ap.add_argument("--index-threshold", type=int, default=300,
                    help="a document citing more distinct functions than this is an INDEX: it "
                         "locates rather than leans, and does not count toward the leaned-on tally")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db required unless --self-test")

    entries, sizes, names, vendor = load(a.functions)
    texts = []
    for root, _d, files in os.walk(a.db):
        if "_inbox" in root.split(os.sep):
            continue
        for fn in sorted(files):
            if fn.endswith(".md"):
                p = os.path.join(root, fn)
                texts.append((os.path.relpath(p, a.db).replace(os.sep, "/"),
                              io.open(p, encoding="utf-8", errors="replace").read()))

    seen = classify(texts, entries, sizes)
    cited = len(seen)
    entry_only = [(e, sizes[e], names.get(e, ""), v[2]) for e, v in seen.items() if v[1] == 0]
    big = sorted([r for r in entry_only if r[1] >= a.min_size], key=lambda r: -r[1])

    print("LOCATED, POSSIBLY NOT READ")
    print("A function that was read usually carries an interior anchor. Entry-only, on a large")
    print("body, is the shape of a name on a door. **These are suspicions, not defects.**\n")
    print("  %d functions cited; %d cited by their entry only (%.1f %%)"
          % (cited, len(entry_only), 100.0 * len(entry_only) / cited if cited else 0.0))
    print("  %d of those have a body of %d bytes or more\n" % (len(big), a.min_size))
    for e, sz, nm, docs in big[:a.top]:
        d = sorted(docs)
        print("  %08X  %7d B  %-46s %s%s"
              % (e, sz, nm[:46], os.path.basename(d[0]), " +%d" % (len(d) - 1) if len(d) > 1 else ""))
    if len(big) > a.top:
        print("\n  ... %d more at or above the threshold" % (len(big) - a.top))

    # The strongest cut, and the one worth acting on.  Size alone over-reports: a document whose
    # subject IS the unread ("the largest unclassified functions") legitimately lists big bodies
    # nobody has opened.  **Leaned on by several documents and never opened** does not have that
    # excuse -- it is a function the database has already built arguments on top of.
    # SECOND false-positive mode, found by use: `007E5160` had six citing documents and **five were
    # table rows in a 2,645-line vtable index**, which lists it as a class and a slot number and
    # claims nothing about its behaviour.
    #
    # **"Cited by N documents" is satisfied by an index, and an index does not lean on anything.**
    #
    # So a document citing an implausible number of distinct functions is treated as a locator, not
    # a dependant.  It is still shown -- and it earned that: a class name and a slot number are a
    # far better starting point than a bare address, so the "weak" citation was the useful one.
    # `_index/` holds the coordinator's shared files -- the audit log, the coverage notes, the
    # question register.  They cite addresses constantly and **none of them is a document about a
    # function**, so a citation there is an echo of the work rather than a dependency on it.
    #
    # Found by use: writing a note in `COVERAGE.md` about an uncited function gave that function a
    # citing document and moved it up the list. **An instrument that reacts to being written about
    # is measuring the writing.**
    idx = {rel for rel, t2 in texts
           if rel.startswith("_index/") or len(cited_addresses(t2)) > a.index_threshold}
    # **Ranking by citation count finds the load-bearing ones; ranking by bytes-per-line-of-prose
    # finds the FOURTH shape** -- read for one purpose with the rest of the body unexamined, where
    # the citation is honest and the claim is simply smaller than the function.
    #
    # > **A 553-byte function with one summary line reads very differently from a 553-byte function
    # > with forty.**
    #
    # It is not decisive and is not meant to be: it ranks the cut by where the gap between body and
    # claim is widest, which is exactly where that shape hides.
    lines_about = collections.Counter()
    for rel, t2 in texts:
        if rel in idx:
            continue
        for line in t2.split(chr(10)):
            for h in set(cited_addresses(line)):
                lines_about[int(h, 16)] += 1

    leaned = []
    for e, v in seen.items():
        real = sorted(d for d in v[2] if d not in idx)
        if v[1] == 0 and len(real) >= a.min_docs and sizes[e] >= a.min_leaned_size:
            prose = lines_about.get(e, 0)
            leaned.append((e, sizes[e], names.get(e, ""), real, len(v[2]),
                           sizes[e] // max(1, prose)))
    leaned.sort(key=lambda r: -r[5])
    print("\nLEANED ON AND NEVER OPENED")
    print("Cited by %d+ documents, body >= %d bytes, no interior anchor anywhere.\n"
          % (a.min_docs, a.min_leaned_size))
    print("Ranked by BYTES PER LINE OF PROSE - widest gap between body and claim first.\n")
    for e, sz, nm, d, raw, bpl in leaned[:a.top]:
        print("  %08X  %6d B  %6d B/line  %2d docs (%d idx)  %-34s %s"
              % (e, sz, bpl, len(d), raw, nm[:34], os.path.basename(d[0])))
    print("\n  %d function(s) in this cut." % len(leaned))

    sse = load_sse(a.sse_census)
    if sse:
        heavy = []
        for e, v in seen.items():
            if v[1] != 0 or e not in sse:
                continue
            instrs, moves, loops = sse[e]
            if moves >= 40 and loops <= 2:
                heavy.append((e, sizes[e], moves, loops, instrs, names.get(e, ""),
                              sorted(d for d in v[2] if d not in idx)))
        heavy.sort(key=lambda r: -(r[2] * 1000 // max(1, r[4])))
        print("\nSSE-HEAVY AND LOOP-FREE, NEVER OPENED")
        print("A large SSE-move count against almost no backward jumps is not a processing pass -")
        print("it is a big structure snapshotted, modified and written back. Ranked by SSE density.")
        print("`sse_moves` counts movups/movss/movaps/movdqu/movdqa/movupd/movapd - a WIDER")
        print("population than a movups-only hand count. Do not quote the two side by side.\n")
        for e, sz, moves, loops, instrs, nm, d in heavy[:a.top]:
            v = vendor.get(e, "")
            print("  %08X  %6d B  %3d%% sse  %d loop(s)  %2d docs  %-11s %-24s %s"
                  % (e, sz, moves * 100 // max(1, instrs), loops, len(d),
                     ("[%s]" % v[:9]) if v else "", nm[:24],
                     os.path.basename(d[0]) if d else "-"))
        nv = sum(1 for r in heavy if vendor.get(r[0]))
        print("\n  %d function(s) in this cut, of which %d are vendor or compiler output"
              % (len(heavy), nv))
        print("  A bracketed row is NOT a documentation gap - it is library or compiler code, and")
        print("  'we have not documented it' is a different state from 'it is not ours'.")
        print("  An UNbracketed row is engine or middleware code and IS in scope: address range is")
        print("  not evidence of provenance, and this column exists because a guess from one was wrong.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
