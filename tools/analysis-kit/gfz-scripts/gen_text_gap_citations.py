"""gen_text_gap_citations.py - seeds the cited .text addresses that are neither a function entry nor inside a listed body.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/seed_text_tables.py`, which `.gitignore` excludes.
A canonical candidates file under `_index/candidates/` named it in its header, so the instruction
for reproducing a file this corpus cites pointed at a tool no peer had. Found by extending
`check_cited_instruments.py` to side files - it had been closed over `_index/*.md` and the kit's own
`*.py` and was blind to `.tsv` entirely.

THE BODY BELOW IS THE ORIGINAL, UNCHANGED. Rewriting its paths and defaults while publishing it
would mean the tool in the kit is not the tool that produced the file beside it, and seeing how the
rows were derived is the whole reason for publishing. The only addition is the two lines under this
docstring, which resolve the repository root from `__file__` and change into it so the tool's
repo-relative paths mean what they have always meant, from any working directory.

NAMED `gen_*`, NOT `check_*`: `run_gates.py` globs `check_*.py`, and a generator under that prefix
would run as a gate every suite and rewrite its own output as a side effect of auditing.

> **DO NOT RUN THIS WITHOUT READING THE NEXT SENTENCE.** ADJUDICATED. `text-gap-citations-250.tsv` carries a `verdict` column and a `why` column written by hand. Seeding again discards both.
"""
import os as _os
import sys as _sys

# The repository root, four levels above this file: gfz-scripts -> analysis-kit -> Tools -> Database
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# seed_text_tables.py - seed the confirmation registry for .text gap citations.
#
# FINAL-AUDIT pass 1 fails if a cited address "is not a function (or is cited as one and is data)".
# 250 distinct cited addresses sit in .text between two listed bodies. verify_doc_addresses already
# says jump and PSM tables after a function are legitimate and asks for confirmation IN CONTEXT --
# but context lives in 91 different pages, and nothing records the confirmation once it is made, so
# the same 250 are re-read on every audit.
#
# This seeds ONE registry with the evidence a confirmer needs per row, so the job is reading rather
# than researching. It confirms nothing itself: every row lands as UNCONFIRMED.
#
# Run from the repo root.

import io, os, re, struct, collections, bisect

DB = "Database/FFXII TZA"
OUT = os.path.join(DB, "_index", "candidates", "text-gap-citations-250.tsv")
IMAGE = 0x120000
d = io.open(r"Database\Tools\work\exe\FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs, o = [], pe + 24 + optsz
for _ in range(nsec):
    n = d[o:o + 8].rstrip(b"\0").decode()
    vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((n, va, vsz, rptr, rsz))
    o += 40


def fileoff(va):
    r = va - IMAGE
    for _n, sva, vsz, rptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return rptr + (r - sva)
    return None


def section_of(va):
    r = va - IMAGE
    for n, sva, vsz, _rp, _rs in secs:
        if sva <= r < sva + vsz:
            return n
    return None


fh = io.open(r"Database\Tools\work\graph\functions.tsv", encoding="utf-8", errors="replace")
head = fh.readline().rstrip("\n").split("\t")
i = {n: k for k, n in enumerate(head)}
fns, name = [], {}
for ln in fh:
    q = ln.rstrip("\n").split("\t")
    if q and re.fullmatch(r"[0-9A-Fa-f]{8}", q[0]):
        try:
            a, n = int(q[0], 16), int(q[i["body_bytes"]])
        except ValueError:
            continue
        fns.append((a, n))
        name[a] = q[i["name"]] if i.get("name", 99) < len(q) else ""
fns.sort()
starts = [a for a, _ in fns]

# `0x`-PREFIXED CITATIONS WERE INVISIBLE TO THIS. The lookbehind rejects a match preceded by `x`,
# which is there to stop `0x0016d6a3` matching at the `0016d6a3` - but the intent was to avoid a
# PARTIAL match, not to drop the address entirely. `verify_doc_addresses` gets this right with an
# optional `(?:0x)?` in the pattern, and the two instruments consequently disagreed about the
# population: `0x0016d6a3` in image-hardening-cfg-aslr-dep-and-stack-cookies.md is a real cited
# `.text` gap address that never got a registry row. Matched to the checker's pattern.
# 2026-09-14, OPUS.
ADDR = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")
hits = collections.defaultdict(set)
for root, dirs, files in os.walk(DB):
    dirs[:] = [x for x in dirs if not x.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(root, fn), DB).replace("\\", "/")
        t = io.open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
        for m in ADDR.finditer(t):
            v = int(m.group(1), 16)
            if section_of(v) != ".text":
                continue
            k = bisect.bisect_right(starts, v) - 1
            if k < 0:
                continue
            a, n = fns[k]
            if v == a or a < v < a + n:
                continue
            hits[v].add(rel)


def indirect_jmp(a, n):
    o1 = fileoff(a)
    if o1 is None:
        return "?"
    body = d[o1:o1 + n]
    for j in range(len(body) - 1):
        if body[j] == 0xFF and (body[j + 1] & 0x38) == 0x20:
            return "yes"
    return "no"


def nextfn(va):
    k = bisect.bisect_right(starts, va)
    return starts[k] if k < len(starts) else None


os.makedirs(os.path.dirname(OUT), exist_ok=True)
w = io.open(OUT, "w", encoding="utf-8", newline="\n")
w.write("# Cited .text addresses that are not a function entry and not inside any listed body.\n#\n")
w.write("# Generated by Database/Tools/work/OPUS/seed_text_tables.py (OPUS, 2026-09-14).\n#\n")
w.write("# WHY THIS FILE EXISTS. FINAL-AUDIT pass 1 fails if a cited address 'is not a function\n")
w.write("# (or is cited as one and is data)'. verify_doc_addresses already grants that jump and\n")
w.write("# PSM tables after a function are legitimate and asks for confirmation IN CONTEXT - but\n")
w.write("# the context is spread over 91 pages and nothing records a confirmation once it is made,\n")
w.write("# so the same 250 addresses are re-read at every audit. One registry, confirmed once.\n#\n")
w.write("# EVERY ROW IS UNCONFIRMED. This file seeds the evidence; it decides nothing. Set verdict\n")
w.write("# to TABLE (a jump/PSM/dispatch table belonging to prev_fn), UNLISTED (a body the function\n")
w.write("# list does not contain - see UC-1), PAD, or DEFECT (cited as a function and is not one),\n")
w.write("# and put the reason in `why`.\n#\n")
w.write("# prev_fn_indirect_jmp = the preceding body contains an FF /4 indirect jmp, which is what a\n")
w.write("# jump-table user looks like. It is a HINT, not a verdict: it says the shape is available,\n")
w.write("# not that this address is that table.\n#\n")
w.write("# addr\tprev_fn\tprev_name\tprev_end\tdelta_from_end\tnext_fn\tprev_fn_indirect_jmp\t"
        "first_bytes\tverdict\twhy\tcited_by\n")

rows = 0
for va in sorted(hits):
    k = bisect.bisect_right(starts, va) - 1
    a, n = fns[k]
    off = fileoff(va)
    blob = d[off:off + 8].hex(" ") if off is not None else ""
    nf = nextfn(va)
    w.write("%08X\t%08X\t%s\t%08X\t%d\t%s\t%s\t%s\tUNCONFIRMED\t\t%s\n"
            % (va, a, (name.get(a) or "")[:44], a + n, va - (a + n),
               ("%08X" % nf) if nf else "-", indirect_jmp(a, n), blob,
               ";".join(sorted(hits[va]))))
    rows += 1
w.close()
print("wrote %s (%d rows)" % (OUT, rows))
