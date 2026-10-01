#!/usr/bin/env python3
"""Re-verify a document's cited addresses against the current parent's function graph.

This is the mechanical half of paying down provenance debt (the AH-* register). It
answers "do the addresses this document cites still exist, and are they still the
functions it says they are?"

It does NOT verify semantic claims -- that needs reading bodies. A green result here
is a necessary condition for advancing a `verified_against` stamp, not a sufficient
one.

Usage:
  verify_doc_addresses.py <doc.md> [<doc.md> ...] [--functions <functions.tsv>]
  verify_doc_addresses.py --all [--db <path>]        # every document

Exit code 1 if any cited address fails to resolve.
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys
import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

DEFAULT_DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
DEFAULT_FN = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
IMAGE_BASE = 0x00120000   # fixed: DYNAMIC_BASE is absent, so VA = RVA + this, always

# NOT IMPLEMENTED, deliberately: an "is this an RVA written as a VA?" check.
#
# Three such errors were found by hand on 2026-09-02 (.reloc and .gfids section addresses, and the
# TLS directory address), all from mixing two sources -- PE data directories and the section table
# hold RVAs, while every Ghidra address already includes the base.
#
# A guard was written for it and then removed, because it does not work on this image. The test
# "outside the image, but inside it once the base is added" fails both ways here:
#   * it MISSES every known case. 0x01BCBED8, 0x02F3C000 and 0x02EE3000 all land inside real
#     sections already -- the image spans 0x121000..0x3095400, so most RVAs are also valid VAs.
#   * it FLAGS quoted float bytes. 0000803F (1.0f) and 0000F041 (30.0f) are outside the image and
#     land in .text once the base is added, purely by coincidence.
# It produced two false positives and zero true ones. Catching this class needs the *semantics* of
# each citation ("the TLS directory is at X") checked against the real PE structure, which is what
# a falsification pass does by hand. A checker that only cries wolf is worse than none.

# 8 hex digits, the canonical form used throughout the database.
#
# This originally read `00[0-9A-Fa-f]{6}`, matching only the `.text` range. That left **51 cited
# addresses unverified by any tool** -- every `.data` and `.rdata` citation, including load-config
# and registry globals such as `01F44830` and `02EBF190`. Widened 2026-09-02 to the whole image.
#
# The cost of widening is that body-hash prefixes look like addresses (`0ee477c3...`,
# `0966b7b4...`). They are excluded by context: a hash prefix is followed **immediately** by an
# ellipsis, with no space.
#
# The whitespace matters. A first version allowed `\s*` before the ellipsis and wrongly excluded
# `002AF340 …` -- a real address at the end of a truncated list in the residual document. A rule
# written to remove false positives introduced one; the discriminator is that a truncated hash
# elides its own tail (`0ee477c3...`) while a truncated *list* elides further items (`… `).
# `\b` FAILS AFTER `0x`. Found by repos-c9, 2026-09-04: in `0x003304A0` the character before the
# leading `0` is `x`, a word character, so there is no word boundary and the address never matched.
# Measured across 227 documents: 31,001 bare addresses seen, **2,856 `0x`-prefixed silently
# dropped, 17 documents 100 % invisible to this gate** and 137 losing half their citations.
# Lookarounds instead of `\b`, which is the form check_located_not_read.py line 123 already used.
ADDR = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")
HASH_CONTEXT = re.compile(r"\b(0[0-9A-Fa-f]{7})[0-9A-Fa-f]*(?:\.\.\.|…)")


# A verdict in the text-gap registry that CONFIRMS what the address is. `UNCONFIRMED` is not one:
# those are the rows blocked on the UC-1 floor review, and pre-empting them here would be exactly
# the shortcut the registry's own header warns against - "a verdict with no evidence is worth less
# than no verdict".
SETTLED = ("TABLE", "PAD", "UNLISTED")


def load_text_gap_verdicts(db):
    """-> {ADDR: verdict} from the text-gap adjudication registry, {} if it is not there.

    Missing file is not an error: this checker predates the registry and must keep working without
    it. It then simply asks for every confirmation again, which is the old behaviour.
    """
    p = os.path.join(db, "_index", "candidates", "text-gap-citations-250.tsv")
    out = {}
    try:
        fh = io.open(p, encoding="utf-8", errors="replace")
    except OSError:
        return out
    with fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) >= 9 and c[8].strip():
                # verdict, and the REASON beside it. SWE2-FRONTIER's second pass (f5230908) gave
                # every one of the 78 UNCONFIRMED rows a reason - "interior point of the unlisted
                # run under 0012A290 ... admission pending UC-1". An UNCONFIRMED row that carries
                # one is DEFERRED on a named decision, not unexamined, and telling a reader to
                # "confirm in context" misdescribes it as neglected work.
                out[c[0].strip().upper()] = (c[8].strip(),
                                             c[9].strip() if len(c) >= 10 else "")
    return out


def load_functions(path):
    out = {r["entry"].upper(): r
           for r in csv.DictReader(io.open(path, encoding="utf-8"), delimiter="\t")}
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(DEFAULT_FN):
        _b = uc1_band.load()
        for e in _b["removed"]:
            out.pop("%08X" % e, None)
        for st, sz in _b["frontier"].items():
            k = "%08X" % st
            out[k] = {"entry": k, "name": "UC1-FRONTIER-%s" % k,
                      "body_bytes": str(sz)}
    return out


def load_ranges(path):
    """Sorted (entry, size, row) for interior-address lookup.

    Documents legitimately cite *instruction* addresses, not just function entries --
    a disassembly listing inside a document is evidence, and its addresses are real.
    An earlier version of this script flagged five such citations as unresolved and
    was wrong; the document was right. Classify, do not reject.
    """
    rows = []
    for r in csv.DictReader(io.open(path, encoding="utf-8"), delimiter="\t"):
        try:
            rows.append((int(r["entry"], 16), int(r["body_bytes"]), r))
        except (ValueError, KeyError):
            continue
    # UC-1 band (2026-09-28) when the input is the shared census: an interior
    # citation inside a frontier body must resolve to it, and 007EE7F0's
    # removal must not leave a phantom extent.
    if os.path.realpath(path) == os.path.realpath(DEFAULT_FN):
        _b = uc1_band.load()
        rows = [(e, s, r) for e, s, r in rows if e not in _b["removed"]]
        rows = [(e, _b["extend"].get(e, e + s) - e, r) for e, s, r in rows]
        rows += [(st, sz, {"entry": "%08X" % st,
                           "name": "UC1-FRONTIER-%08X" % st,
                           "body_bytes": str(sz)})
                 for st, sz in _b["frontier"].items()]
    rows.sort()
    return rows


def containing(rows, a):
    lo, hi, best = 0, len(rows) - 1, None
    while lo <= hi:
        m = (lo + hi) // 2
        if rows[m][0] <= a:
            best = rows[m]
            lo = m + 1
        else:
            hi = m - 1
    if best and best[0] <= a < best[0] + best[1]:
        return best
    return None


# THE FAR END OF A STATED RANGE IS A BOUND, NOT A CITATION.
#
# `the span of the 34,270 non-funclet bodies runs 00121000-008C1635` asserts an extent; it does not
# assert that `008C1635` is a function. The address is the last byte of the last body - 0x8C1635 -
# 0x121000 is 7,996,981, exactly the byte count the same sentence states - and the bytes there are
# zero padding. Reported as a `.text` non-function citation it was the single remaining REVIEW row
# in the corpus, asking a reader to confirm in context something that is arithmetic.
#
# Only the RIGHT-hand side is dropped. The left end of a range is a real entry and stays.
# 2026-09-14, OPUS.
RANGE_END = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?0[0-9A-Fa-f]{7}`?\s*[-–—]\s*`?"
                       r"(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")


def cited(text):
    """Addresses a document actually asserts, minus obvious non-addresses."""
    hashes = {m.group(1).upper() for m in HASH_CONTEXT.finditer(text)}
    range_ends = {m.group(1).upper() for m in RANGE_END.finditer(text)}
    out = []
    for m in ADDR.finditer(text):
        a = m.group(1).upper()
        if a in ("00000000",) or a in hashes:
            continue
        out.append(a)
    # NOT dropped here. A first version removed every range end and deleted 1,876 citations -
    # `0025B070`-`0025B111` is a real instruction address and verifying it is the point. The bound
    # case is narrower than "is a range end": it is "is a range end AND lands in .text outside any
    # body", which only the classifier can tell. Passed through, and handled there.
    return sorted(set(out)), range_ends


def load_sections(exe):
    """(name, lo, hi) per PE section, so a citation can be classified by where it lands."""
    d = io.open(exe, "rb").read()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    optoff = e + 24
    ib = struct.unpack_from("<Q", d, optoff + 24)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    optsz = struct.unpack_from("<H", d, e + 20)[0]
    base = e + 24 + optsz
    out = []
    for i in range(nsec):
        o = base + 40 * i
        nm = d[o:o + 8].rstrip(b"\0").decode()
        vs, va, rs, _pr = struct.unpack_from("<IIII", d, o + 8)
        out.append((nm, ib + va, ib + va + max(vs, rs)))
    return out


def section_of(secs, a):
    for nm, lo, hi in secs:
        if lo <= a < hi:
            return nm
    return None


def verify(doc, fns, rows, secs):
    """Classify every cited address rather than pass/fail it.

    Three legitimate non-entry classes exist and all three occur in this database:
      interior   an instruction inside a function (disassembly listings cite these)
      text-data  a jump/PSM table the compiler placed after its function, still in .text
                 -- cross-checked against the text-gap adjudication registry, see SETTLED below
      data       a global or string in .rdata/.data
    Only a .text address that is neither a function nor adjacent to one is a real ghost.
    """
    t = io.open(doc, encoding="utf-8").read()
    addrs, range_ends = cited(t)
    buckets = collections.defaultdict(list)
    owners = collections.Counter()
    for a in addrs:
        v = int(a, 16)
        r = fns.get(a)
        if r:
            buckets["entry"].append(a)
            owners[r.get("owner") or "-"] += 1
            continue
        if containing(rows, v):
            buckets["interior"].append(a)
            continue
        sec = section_of(secs, v) if secs else None
        if sec is None:
            buckets["literal"].append(a)          # not an address at all (quoted bytes)
        elif sec == ".text":
            # A RANGE END THAT LANDS IN NO BODY IS A BOUND. "the span runs 00121000-008C1635"
            # states an extent; 008C1635 is the last byte, the bytes there are zero padding, and
            # 0x8C1635-0x121000 is exactly the byte count the same sentence gives. Asking a reader
            # to confirm it in context asks them to confirm arithmetic. A range end that DOES
            # resolve is never touched - it is a real instruction address and verifying it is the
            # whole point.
            if a in range_ends:
                buckets["range-bound"].append(a)
            else:
                buckets["text-data"].append(a)    # jump table / pad after a function
        elif sec in (".pdata", ".xdata"):
            # The evidence standard bans unwind data as proof. A citation here is not
            # automatically wrong -- one document cites a .pdata entry precisely to say it is
            # inadmissible -- but every one should be deliberate.
            buckets["unwind-BANNED"].append(a)
        else:
            buckets["data"].append(a)             # .rdata / .data global or string
    return addrs, buckets, owners


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("docs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--functions", default=DEFAULT_FN)
    ap.add_argument("--exe", default=r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    fns = load_functions(a.functions)
    rows = load_ranges(a.functions)
    try:
        secs = load_sections(a.exe)
    except OSError:
        secs = None
    docs = list(a.docs)
    if a.all:
        for root, _d, files in os.walk(a.db):
            top = os.path.relpath(root, a.db).split(os.sep)[0]
            if not re.match(r"^\d\d-", top):
                continue
            docs += [os.path.join(root, f) for f in sorted(files)
                     if f.endswith(".md") and f != "README.md"]
    if not docs:
        ap.error("give document paths or --all")

    adjudged = load_text_gap_verdicts(a.db)
    bad = 0
    tot = collections.Counter()
    for doc in docs:
        addrs, b, owners = verify(doc, fns, rows, secs)
        rel = os.path.relpath(doc, a.db) if doc.startswith(a.db) else doc
        for k, v in b.items():
            tot[k] += len(v)
        # a .text address that is neither a function nor interior is worth a human look,
        # but jump tables legitimately live there -- report, do not fail.
        #
        # AND THE LOOK HAS ALREADY HAPPENED FOR MOST OF THEM. `_index/candidates/
        # text-gap-citations-250.tsv` is the adjudication of exactly this population: 250 cited
        # .text gap addresses, 147 decided TABLE, 19 PAD, 4 UNLISTED, 80 still UNCONFIRMED
        # (blocked on the UC-1 floor review). Until now nothing read it, so this checker kept
        # asking for a confirmation that had already been given -- 74 of the 94 REVIEW documents
        # carry only addresses that were adjudicated days ago. **An adjudication no instrument
        # consumes is an adjudication that gets made again.** 2026-09-14, OPUS.
        review = list(b.get("text-data", []))
        settled = [x for x in review if adjudged.get(x.upper(), ("", ""))[0] in SETTLED]
        deferred = [x for x in review if x not in settled
                    and adjudged.get(x.upper(), ("", ""))[1]]
        pending = [x for x in review if x not in settled and x not in deferred]
        if deferred and not pending:
            # every gap citation is either settled or DEFERRED with a stated reason - the document
            # is waiting on a decision, not on someone's attention
            if not a.quiet:
                top = ", ".join(f"{k}:{v}" for k, v in owners.most_common(3))
                parts = ", ".join(f"{len(v)} {k}" for k, v in sorted(b.items()))
                print(f"ok     {rel}")
                print(f"       {len(addrs)} cited: {parts}   [{top}]")
                print(f"       .text gap citations DEFERRED with a reason, not unexamined: "
                      f"{', '.join(deferred)}")
        elif pending:
            bad += 1
            print(f"REVIEW {rel}")
            print(f"       .text non-function addresses: {' '.join(pending)}")
            print(f"       (jump/PSM tables after a function are legitimate -- confirm in context)")
            if settled:
                print(f"       already adjudicated, not repeated here: "
                      f"{', '.join('%s=%s' % (x, adjudged[x.upper()][0]) for x in settled)}")
        elif settled and not a.quiet:
            top = ", ".join(f"{k}:{v}" for k, v in owners.most_common(3))
            parts = ", ".join(f"{len(v)} {k}" for k, v in sorted(b.items()))
            print(f"ok     {rel}")
            print(f"       {len(addrs)} cited: {parts}   [{top}]")
            print(f"       .text gap citations all adjudicated: "
                  f"{', '.join('%s=%s' % (x, adjudged[x.upper()][0]) for x in settled)}")
        elif not a.quiet:
            top = ", ".join(f"{k}:{v}" for k, v in owners.most_common(3))
            parts = ", ".join(f"{len(v)} {k}" for k, v in sorted(b.items()))
            print(f"ok     {rel}")
            print(f"       {len(addrs)} cited: {parts}   [{top}]")

    print(f"\n{len(docs)} document(s)")
    for k in ("entry", "interior", "text-data", "range-bound", "data", "unwind-BANNED",
              "literal"):
        if tot[k]:
            print(f"   {tot[k]:5d}  {k}")
    print(f"   {bad} document(s) with .text non-function citations to confirm")
    return 0

if __name__ == "__main__":
    sys.exit(main())
