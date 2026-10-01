"""gen_provenance_path.py - what has to happen, document by document, for the provenance gate to go green.

`check_provenance` is red and `unresolved`-style figures are quoted at it constantly, but **nobody
has written down what would actually close it.** "163 owe re-verification" is a count, not a plan:
the 163 need four different things, and one of those things is already argued.

The population is `check_provenance`'s own - documents under a numbered category, `README.md`
excluded - so these figures compose with the gate's rather than describing some other set.

  A  already transferred to the certified parent    nothing to do
  B  transfer targets GN160                         RE-POINT one generation. The `voided_by`
                                                    clause is a condition on the delta and the
                                                    delta is measured additive, so 61 of these
                                                    hold and 6 owe re-adjudication.
  D  no transfer, quotes only FUNCTION NAMES        a NEW transfer, settleable from FAS2 today -
                                                    the names are in the snapshot and none changed
  E  no transfer, quotes non-function state         the exporter. THIS is what ASTRA is blocked on
  -  image-derived, no gzf stamp                    cannot go stale; names no parent

**THE EXPORTER'S POPULATION HAS NOW BEEN REVISED THREE TIMES AND EACH TIME FOR A DIFFERENT REASON**,
which is worth stating plainly rather than quietly printing the fourth number:

  53   the request's original figure
  163  a denominator that had GROWN since it was written
  118  a denominator that was never one population - 45 quote only function names
  E    documents with NO adjudicated transfer at all, which is the number that actually blocks

The 118 counts every document that quotes non-function state, including those whose GN160 transfer
was already adjudicated on a stated basis. Bucket B's re-point extends an existing adjudication by
one generation; it does not re-open what that adjudication accepted. So the exporter blocks E, and
B is blocked on the review instead.

**Nothing here transfers, re-points or stamps anything.** It says what each bucket needs.
"""
import argparse
import collections
import io
import os
import re
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
ENV = os.path.join(REPO, "Database", "Tools", "ghidra", "run", "GfzEnv.ps1")
STAMP = re.compile(r"gzf_sha256:\s*([0-9a-fA-F]{24})")
XFER = re.compile(r"transfers_to:\s*\n\s*parent:\s*([0-9a-fA-F]{24})")
BASIS = re.compile(r"transfers_to:\s*\n(?:[ \t]+\w+:.*\n)*?[ \t]+basis:\s*(.+)")
NONFUNC = re.compile(r"\b(?:DAT|LAB|PTR|UNK)_[0-9A-Fa-f]{4,}\b")


def certified():
    """The certified parent's prefix, read from GfzEnv.ps1 - never from a summary of it."""
    if not os.path.isfile(ENV):
        return None
    m = re.search(r"\$GfzParentSha\s*=\s*'([0-9a-f]{64})'",
                  io.open(ENV, encoding="utf-8", errors="replace").read())
    return m.group(1)[:24] if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    sys.path.insert(0, KIT)
    try:
        import decompiler_tokens as dt
    except ImportError:
        print("CANNOT RUN: decompiler_tokens is not importable")
        return 2
    cert = certified()
    if not cert:
        print("CANNOT RUN: the certified parent is not readable from GfzEnv.ps1")
        return 2

    cat = collections.Counter()
    rows = []
    # check_provenance's OWN population: numbered categories, README.md excluded. Using a different
    # one would give figures that look like the gate's and are not.
    for root, _d, files in os.walk(a.db):
        top = os.path.relpath(root, a.db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for fn in sorted(files):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            rel = os.path.relpath(os.path.join(root, fn), a.db).replace(os.sep, "/")
            t = io.open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            m = STAMP.search(t)
            if not m:
                cat["image-derived"] += 1
                continue
            x = XFER.search(t)
            if x and x.group(1).lower() == cert:
                cat["A"] += 1
                rows.append((rel, "A", "nothing"))
                continue
            if x:
                b = BASIS.search(t)
                bb = (b.group(1).strip().split(" - ")[0] if b else "(basis unstated)")
                cat["B"] += 1
                cat["B:" + bb[:24]] += 1
                rows.append((rel, "B", "re-point; basis " + bb[:40]))
                continue
            hits = [n for n, pat in dt.PATTERNS if pat.search(t)]
            if not hits:
                cat["C"] += 1
                rows.append((rel, "C", "a new transfer; quotes no decompiler state"))
            elif hits == ["auto-name"] and not NONFUNC.search(t):
                cat["D"] += 1
                rows.append((rel, "D", "a new transfer; FAS2 witnesses the function names"))
            else:
                cat["E"] += 1
                rows.append((rel, "E", "the non-function exporter"))

    print("WHAT WOULD CLOSE THE PROVENANCE GATE\n")
    print("  population: check_provenance's own - numbered categories, README.md excluded\n")
    order = [("A", "already transferred to the certified parent", "nothing to do"),
             ("B", "transfer targets an older parent", "RE-POINT one generation"),
             ("C", "no transfer, quotes no decompiler state", "a new transfer"),
             ("D", "no transfer, FUNCTION NAMES only", "a new transfer, from FAS2 today"),
             ("E", "no transfer, non-function state", "THE EXPORTER - this is the block")]
    for k, what, need in order:
        print("  %s  %-42s %4d   %s" % (k, what, cat[k], need))
    print("  -  %-42s %4d   cannot go stale" % ("image-derived, names no parent", cat["image-derived"]))
    gz = sum(cat[k] for k in "ABCDE")
    print("\n  GZF-derived: %d   image-derived: %d   total: %d"
          % (gz, cat["image-derived"], gz + cat["image-derived"]))
    print("\n  bucket B by the basis its transfer already states:")
    for k, v in sorted(cat.items()):
        if k.startswith("B:"):
            print("      %-34s %4d" % (k[2:], v))
    print("\n  THE EXPORTER BLOCKS %d, NOT 163 AND NOT 118. Those counted documents whose GN160"
          % cat["E"])
    print("  transfer was ALREADY adjudicated on a stated basis; a re-point extends that")
    print("  adjudication by one generation rather than re-opening what it accepted. The figure")
    print("  has been revised three times now - 53, then 163, then 118 - each for a different")
    print("  reason, and this one is stated as a bucket rather than as a fourth flat number.")
    dest = os.path.join(a.db, "_index", "candidates", "provenance-path-to-green.tsv")
    out = ["# What each stale document needs for check_provenance to go green.",
           "#",
           "# Generated by gen_provenance_path.py over check_provenance's own population.",
           "# NOTHING HERE TRANSFERS, RE-POINTS OR STAMPS ANYTHING.",
           "#",
           "# A already transferred · B re-point · C/D a new transfer · E the exporter",
           "#",
           "# document\tbucket\twhat it needs"]
    out += ["%s\t%s\t%s" % r for r in sorted(rows)]
    io.open(dest, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n  wrote %s" % os.path.relpath(dest, REPO).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
