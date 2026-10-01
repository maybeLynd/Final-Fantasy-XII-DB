#!/usr/bin/env python3
"""check_ebp.py - how much of the EBP script container is documented.

The population, and why it is allowed to be scored
--------------------------------------------------
**14 units: the container, plus every section type present in the corpus.**

The 13 section types were **censused, not chosen** — all 1,115 `us` `.ebp` files were extracted
from `FFXII_TZA.vbf` and unpacked, and these are the section indices that occurred:

    000  1114/1115  99.9%      008   423   37.9%  (strict pair with 009)
    002   828       74.3%      009   423   37.9%  (strict pair with 008)
    003   359       32.2%      010   113   10.1%  (strict pair with 011)
    004   209       18.7%      011   113   10.1%  (strict pair with 010)
    006    67        6.0%      012   842   75.5%
    014   140       12.6%      016   517   46.4%
    019   271       24.3%

`001`, `005`, `007`, `013`, `015`, `017`, `018` never occur in 1,115 files.

**The 14th unit is the container itself** — the `EBP2` header and its section directory. That one
is not censused because it is not a section; it is the thing that holds them, and there is exactly
one. Stated rather than hidden inside the count.

**Why a census and not a plan.** *"We intend six sheets and have written four"* grades itself:
choose a smaller intention, score higher. Every scored dimension in `progress.py` is anchored to
something outside the author's control — 34,270 functions from `functions.tsv`, 63 registry slots
re-derived from a tier-1 document's own bounds, and here 13 section types read out of the shipped
files.

**The population is frozen deliberately.** Re-running the census on a different language or a
different build could move it; if it ever does, that is a finding to write up, not a number to
quietly change. `--census` re-checks a directory of unpacked scripts against the frozen list and
reports any disagreement.

What counts as covered
----------------------
A unit is covered when a document **declares it in frontmatter**:

    ebp_units:
      - "container"
      - "section_000"

Declared, never scraped. A unit claimed by two documents is a **collision** under the standing
rule that no address — and no artefact — is described two ways.

Usage
-----
    python check_ebp.py --db "Database/FFXII TZA"
    python check_ebp.py --db "Database/FFXII TZA" --quiet
    python check_ebp.py --census <dir of *_unc folders>     # re-verify the population
    python check_ebp.py --self-test
"""
import argparse
import collections
import glob
import io
import os
import re
import sys

# The censused population. 13 sections + the container = 14 units.
SECTIONS = ["000", "002", "003", "004", "006", "008", "009",
            "010", "011", "012", "014", "016", "019"]
UNITS = ["container"] + ["section_%s" % s for s in SECTIONS]
CORPUS_SIZE = 1115           # us-language scripts unpacked for the census
CENSUS = {"000": 1114, "002": 828, "003": 359, "004": 209, "006": 67, "008": 423,
          "009": 423, "010": 113, "011": 113, "012": 842, "014": 140, "016": 517,
          "019": 271}

UNIT_LINE = re.compile(r"^\s*-\s*[\"']?(container|section_\d{3})[\"']?\s*$")
SKIP_DIRS = ("_index", "_templates", "_inbox")


def claimed_units(db):
    """unit -> [documents claiming it], from `ebp_units:` frontmatter lists."""
    out = collections.defaultdict(list)
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), db).replace(os.sep, "/")
            inside = False
            for line in io.open(os.path.join(root, fn), encoding="utf-8",
                                errors="replace").read().split("\n"):
                if line.strip().startswith("ebp_units:"):
                    inside = True
                    continue
                if inside:
                    m = UNIT_LINE.match(line)
                    if m:
                        out[m.group(1)].append(rel)
                    elif line.strip():
                        inside = False
    return out


def recensus(root):
    """Re-derive the section population from a directory of unpacked `*_unc` folders."""
    seen = collections.Counter()
    dirs = glob.glob(os.path.join(root, "*_unc"))
    for d in dirs:
        for f in glob.glob(os.path.join(d, "section_*.bin")):
            seen[os.path.basename(f)[8:11]] += 1
    return len(dirs), seen


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--census", help="directory holding unpacked <name>.ebp_unc folders")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        import tempfile
        return self_test(tempfile.mkdtemp())

    if a.census:
        n, seen = recensus(a.census)
        print("re-census over %d unpacked scripts (frozen population was %d)" % (n, CORPUS_SIZE))
        drift = 0
        for s in sorted(set(seen) | set(CENSUS)):
            was, now = CENSUS.get(s), seen.get(s)
            flag = "" if was == now else "   <-- DISAGREES WITH THE FROZEN POPULATION"
            if was != now:
                drift += 1
            print("  section_%s  frozen %-5s  now %-5s%s" % (s, was, now, flag))
        if drift:
            print("\n%d section(s) disagree. This is a FINDING to write up, not a number to "
                  "quietly change." % drift)
        return 1 if drift else 0

    if not a.db:
        return ap.error("--db, --census or --self-test required")

    claims = claimed_units(a.db)
    valid = {u: d for u, d in claims.items() if u in UNITS}
    stray = {u: d for u, d in claims.items() if u not in UNITS}
    collisions = {u: d for u, d in valid.items() if len(d) > 1}

    if a.quiet:
        print("%d\t%d" % (len(valid), len(UNITS)))
        return 0

    print("EBP SCRIPT CONTAINER COVERAGE")
    print("  population: %d units - the container plus %d section types, the sections censused"
          % (len(UNITS), len(SECTIONS)))
    print("              by unpacking all %d us-language scripts. Not a plan; a census." % CORPUS_SIZE)
    print("")
    print("  covered:    %d / %d  (%.2f %%)"
          % (len(valid), len(UNITS), 100.0 * len(valid) / len(UNITS)))
    print("")
    for u in UNITS:
        if u in valid:
            print("    [x] %-14s %s" % (u, ", ".join(valid[u])))
        else:
            pct = "" if u == "container" else "  (in %d of %d files)" % (
                CENSUS[u[-3:]], CORPUS_SIZE)
            print("    [ ] %-14s%s" % (u, pct))

    rc = 0
    if collisions:
        rc = 1
        print("\n  UNITS CLAIMED TWICE - nothing is described two ways:")
        for u in sorted(collisions):
            print("    %-14s %s" % (u, ", ".join(collisions[u])))
    if stray:
        rc = 1
        print("\n  DECLARED UNITS THAT ARE NOT IN THE POPULATION:")
        for u in sorted(stray):
            print("    %-14s %s" % (u, ", ".join(stray[u])))
        print("  A section index outside the census is either a typo or a real discovery.")
        print("  If it is real, re-run --census and write up what changed.")
    return rc


SELF_A = """---
system: a
ebp_units:
  - "container"
  - "section_000"
---
body
"""
SELF_B = """---
system: b
ebp_units:
  - "section_000"
  - "section_777"
---
body
"""


def self_test(tmp):
    db = os.path.join(tmp, "ebp_db")
    if not os.path.isdir(db):
        os.makedirs(db)
    io.open(os.path.join(db, "a.md"), "w", encoding="utf-8").write(SELF_A)
    io.open(os.path.join(db, "b.md"), "w", encoding="utf-8").write(SELF_B)
    claims = claimed_units(db)
    valid = {u for u in claims if u in UNITS}
    if valid != {"container", "section_000"}:
        print("SELF-TEST FAILED: valid %s" % sorted(valid))
        return 1
    if len(claims["section_000"]) != 2:
        print("SELF-TEST FAILED: collision not detected")
        return 1
    if "section_777" in valid:
        print("SELF-TEST FAILED: out-of-population unit accepted")
        return 1
    if len(UNITS) != 14 or sum(1 for u in UNITS if u.startswith("section_")) != 13:
        print("SELF-TEST FAILED: population is %d units" % len(UNITS))
        return 1
    print("self-test ok: 14 units (container + 13 censused sections), a collision caught, "
          "and a section index outside the census refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
