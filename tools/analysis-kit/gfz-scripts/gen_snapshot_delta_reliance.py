"""gen_snapshot_delta_reliance.py - measures which stale-stamped documents quote a GFZ tag beside a changed function.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/snapshot_delta_reliance.py`, which `.gitignore` excludes.
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
"""
import os as _os
import sys as _sys

# The repository root, four levels above this file: gfz-scripts -> analysis-kit -> Tools -> Database
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# snapshot_delta_reliance.py - do the 20 SNAPSHOT-DELTA documents rely on what actually changed?
#
# FABLE's ruling established the transfer witness and re-sorted 176 documents. 103 transfer on
# snapshot identity and are stamped; 53 quote decompiler state and wait on a non-function export;
# **20 sit in a genuine snapshot delta** - they cite a function whose per-function record differs
# between their stamped generation and the certified parent.
#
# BUT THE RULING ALSO SAYS WHAT DIFFERS: *"differ GN158->GN160 in 19 functions and GN159->GN160 in
# 15, plate comment + tags only; embedded EXE identical."* **Names, bodies, sizes, prototypes and
# calling conventions are unchanged.** So a document in this class is only AFFECTED if it relies on
# the two things that moved: the plate comment text, or the GFZ tag.
#
# THE TEST. For each of the 20, and only for the functions its own row names as delta functions:
# does the document quote a `GFZ.*` tag for that function, or reproduce plate-comment text? A page
# that cites the function by address and argues from its BODY is untouched by a comment edit.
#
# WHY THIS IS NOT THE SAME QUESTION I ALREADY ANSWERED. `delta_staleness.py` asked whether a document
# CALLS one of these functions unclassified - a claim a new tag falsifies. This asks the converse:
# whether the document LEANS on the annotation at all. A page can be silent about classification and
# still quote a tag as evidence, and that page would not have been caught by the first pass.
#
# A hit is not a defect - it means the document must be re-read against the current annotation before
# its stamp can transfer. A clean result means the delta is real and irrelevant to that page, which is
# the ordinary case when the thing that changed is a comment.

import io, os, re, sys

DB = "Database/FFXII TZA"
R = os.path.join(DB, "_index", "candidates", "provenance-snapshot-resort.tsv")
TAG = re.compile(r"GFZ\.[A-Za-z0-9_.]+")


def main():
    rows = [l.rstrip("\n").split("\t") for l in io.open(R, encoding="utf-8") if l.strip()]
    h = rows[0]
    di, ci, fi = h.index("document"), h.index("snapshot_class"), h.index("cited_delta_functions")

    hits, clean = [], []
    for r in rows[1:]:
        if len(r) <= fi or r[ci].strip() != "SNAPSHOT-DELTA":
            continue
        doc, fns = r[di], r[fi].split()
        p = os.path.join(DB, doc.replace("/", os.sep))
        try:
            t = io.open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        lines = t.split("\n")
        found = []
        for n, line in enumerate(lines, 1):
            up = line.upper()
            near = [f for f in fns if f.upper() in up]
            if not near:
                continue
            for m in TAG.finditer(line):
                found.append((n, near[0], m.group(0)[:70], " ".join(line.split())[:110]))
        (hits if found else clean).append((doc, fns, found))

    print("SNAPSHOT-DELTA documents: %d\n" % (len(hits) + len(clean)))
    print("  What actually differs between these generations, per FABLE's ruling:")
    print("    plate comment + tags only. Names, bodies, sizes, prototypes, calling conventions")
    print("    and the embedded EXE are identical.\n")
    print("  QUOTE A GFZ TAG ON A LINE NAMING ONE OF THEIR DELTA FUNCTIONS: %d" % len(hits))
    for doc, fns, found in hits:
        print("      %s" % doc)
        for n, fn, tag, line in found[:4]:
            print("          line %-5d %s  %s" % (n, fn, tag))
            print("              %s" % line)
    print()
    print("  NO TAG QUOTED beside a delta function: %d" % len(clean))
    for doc, fns, _f in clean:
        print("      %-66s %s" % (doc[:66], " ".join(fns)[:40]))
    print()
    print("  A clean row means the page cites the function by address and argues from its body,")
    print("  so a comment or tag edit cannot have falsified it. That is the ordinary case when")
    print("  the thing that moved is annotation text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
