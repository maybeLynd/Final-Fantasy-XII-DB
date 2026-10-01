"""Can a checker find a function documented twice, on two pages? NO - AND THIS IS THE PROOF.

WHY THIS EXISTS. EVIDENCE-STANDARD 13bb found 002ABF70 (577 B) read in full by two documents that
do not cite each other - ui-request-router.md as "an eight-mode jump table", and
measuring-text-by-drawing-it-with-the-output-off.md as "the animation stepper" - and claimed the
corpus-wide count of that shape is unknown. This probe was written to measure it.

IT FAILED ITS OWN CONTROL, AND THE FAILURE IS THE RESULT.

The discriminator was INTERIOR CITATION: a document citing only a function's entry address is
mentioning it; one citing an address strictly inside the body has read it. Two documents doing the
second thing to one function should be the 002ABF70 shape. The control asked whether 002ABF70 is in
the output.

  002ABF70 IS NOT IN THE OUTPUT.

  ui-request-router.md            cites 16 interior addresses (002ABF79 .. 002AC1B4)
  measuring-text-...-off.md       cites ZERO - only the entry

and yet the second page carries a seven-row field table for the state block, names the dispatch as
`state[+0xB0] & 0xFF` over states 0-5 and 7, and identifies state 2 as a fade from what it does to
+0x5A. IT READ THE FUNCTION COMPLETELY AND QUOTED NOT ONE ADDRESS INSIDE IT, because it read it as
decompiled prose and field offsets rather than as instructions.

  >> A PAGE CAN READ A FUNCTION IN FULL AND CITE ONLY ITS ENTRY. SO NO ADDRESS-LEVEL PREDICATE CAN
  >> FIND THIS CLASS, AND THAT INCLUDES EVERY CHECKER IN THIS KIT.

That is the same finding as 13au, where `explained by nothing` turned out to be an address-level
predicate applied to structure-level documentation, and the same as passes 7, 21 and 23: AN
INSTRUMENT MEASURES THE STRUCTURE IT PARSES, NOT THE STRUCTURE THE CONTENT LIVES IN. Here it is the
instrument I wrote to measure that very thing.

THE CONTROL IS LEFT FAILING ON PURPOSE. Loosening it to one interior address would make 002ABF70
appear and would be fraud: the measuring page has zero, not one. Widening to entry-only citation
makes every mention a reading and returns thousands. There is no threshold that separates them,
because the signal is not in the addresses.

WHAT THE NUMBER BELOW IS. 504 functions are cited interior-deep by two or more documents. That is a
real measurement of a DIFFERENT thing - mostly legitimate, a producer page and a consumer page each
quoting the call sites they care about - and it is NOT the count of doubly-read functions. It is
published as candidates, not findings, and every row needs both pages read before it means anything.

Run from the repository root.
"""
import bisect
import collections
import io
import os
import re
import sys
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import check_dispositions as CD

DB = 'Database/FFXII TZA'
SKIP_DIR = ('_index', '_experiments', '_types')
SKIP_FILE = ('the-unresolved-158.md',)
HEX = re.compile(r'\b([0-9A-Fa-f]{8})\b')
CONTROL = 0x002ABF70

sizes = CD.load_functions(None)
ks = sorted(sizes)


def owner(va):
    i = bisect.bisect_right(ks, va) - 1
    return ks[i] if i >= 0 and ks[i] <= va < ks[i] + sizes[ks[i]] else None


seen = collections.defaultdict(lambda: collections.defaultdict(set))
ndoc = 0
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d not in SKIP_DIR]
    for fn in files:
        if not fn.endswith('.md') or fn in SKIP_FILE:
            continue
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, DB).replace(os.sep, '/')
        ndoc += 1
        txt = io.open(p, encoding='utf-8', errors='replace').read()
        for m in HEX.finditer(txt):
            va = int(m.group(1), 16)
            if va < 0x120000 or va > 0x1000000:
                continue
            f = owner(va)
            if f is None or f == va:
                continue
            seen[f][rel].add(va)

dup = {}
for f, docs in seen.items():
    deep = [d for d, a in docs.items() if len(a) >= 2]
    if len(deep) >= 2:
        dup[f] = deep

print("documents scanned                             : %d" % ndoc)
print("functions with >=1 interior citation          : %d" % len(seen))
print("functions cited interior-deep by 2+ documents : %d" % len(dup))
print("   (deep = that document cites >=2 distinct interior addresses)")
byn = collections.Counter(len(v) for v in dup.values())
for n in sorted(byn):
    print("      by exactly %2d documents : %d" % (n, byn[n]))

print("\nCONTROL - the case this probe was built from")
docs = seen.get(CONTROL, {})
for d, a in sorted(docs.items()):
    print("   %-70s interior citations: %d" % (d[:70], len(a)))
if CONTROL in dup:
    print("   PASS - and that is unexpected; re-read this file's header before trusting it.")
else:
    print("   FAIL, DELIBERATELY LEFT FAILING. 002ABF70 is read in full by two documents and this")
    print("   probe cannot see it, because one of them cites no address inside the body at all.")
    print("   The 504 above is therefore NOT the count of doubly-read functions. Nothing here")
    print("   licenses a disposition, and no metric moves.")

out = DB + '/_index/candidates/functions-cited-deep-by-two-documents.tsv'
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# NOT A FINDING LIST, AND NOT THE 13bb COUNT - see probe_double_documentation.py, whose\n")
    f.write("# control FAILS: the function that motivated it, 002ABF70, is absent from these rows\n")
    f.write("# because one of the two documents that read it cites zero addresses inside its body.\n")
    f.write("# What this file is: functions cited interior-deep (>=2 distinct interior addresses)\n")
    f.write("# by two or more documents. Entry-only citations excluded as mentions; _index/,\n")
    f.write("# _experiments/, _types/ and the-unresolved-158.md census listing excluded.\n")
    f.write("# A ROW IS NOT A DUPLICATION. A producer page and a consumer page legitimately quote\n")
    f.write("# the same call sites. Every row needs both documents read before it means anything.\n")
    f.write("function\tsize\tdocuments\tpaths\n")
    for fa in sorted(dup, key=lambda x: -len(dup[x])):
        f.write("%08X\t%d\t%d\t%s\n" % (fa, sizes[fa], len(dup[fa]), ' | '.join(sorted(dup[fa]))))
print("\nwrote %s (%d rows)" % (out, len(dup)))
