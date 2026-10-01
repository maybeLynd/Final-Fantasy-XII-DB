#!/usr/bin/env python3
"""check_formats.py - how much of the authored-data registry is explained as a format.

The denominator problem, and why this one is allowed to exist
-------------------------------------------------------------
A "formats covered" metric is worthless if the denominator is a wish list. *"We plan seven
format sheets and have written four"* grades itself: pick a smaller plan, score higher.

Every other dimension in `progress.py` is anchored to something read out of the binary --
34,270 functions from `functions.tsv`, the residual list, the register's own rows. This one
uses the same discipline:

> **The population is the authored-data pointer registry**, established at tier 1 in
> `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`: bounds `0x02EBF008` to
> `0x02EBF1F8`, an 8-byte stride, **63 slots**. Scanned from `.text`, reopened three times,
> and one claim in it already overturned (a slot that is runtime state, not a table).

**This script re-derives that count rather than trusting it.** It reads the bounds and the
stride out of the document, computes `(end - start) / stride + 1`, and **fails if the arithmetic
disagrees with the number the document states.** A denominator nobody can re-derive is a
denominator nobody should score against.

What counts as covered
----------------------
A slot is covered when **some document declares it in frontmatter**:

    registry_slots:
      - "0x02EBF0C0"
      - "0x02EBF138"

Not by prose, and not by mentioning the address in passing. A document has to make the claim
in a machine-readable field, which means:

- the numerator cannot drift as prose is edited;
- claiming a slot is a deliberate act with an owner;
- and **the same slot claimed by two documents is reported as a collision**, because this
  project's standing rule is that no address is described two ways.

**Coverage is measured across the whole database, not one folder.** A slot explained inside a
system document counts exactly as much as one explained in a dedicated format sheet -- the
metric is about the engine being understood, not about where the file lives.

What this does NOT measure
--------------------------
**Container formats have no denominator here and are not scored.** The save image, the VBF
bigfile, `.ebp` script bytecode, `.phyre` assets and `game-settings.ini` are real formats with
real documents, but there is no censused universe of them -- so any fraction would be invented.
They are reported as a **bare count**, which is honest, instead of as a percentage, which would
not be.

> **A number without a denominator is honest; a number with a made-up one is not.**

Usage
-----
    python check_formats.py --db "Database/FFXII TZA"
    python check_formats.py --db "Database/FFXII TZA" --quiet   # one line, for progress.py
    python check_formats.py --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

REGISTRY_DOC = os.path.join("02-Resource-And-Asset-Pipeline",
                            "authored-data-table-registry.md")

# `0x02EBF008` - `0x02EBF1F8` ... 63 slots, 8-byte stride
BOUNDS = re.compile(r"`(0x0[0-9A-Fa-f]{7})`\s*[-–—]\s*`(0x0[0-9A-Fa-f]{7})`")
STRIDE = re.compile(r"(\d+)\s*-\s*byte stride", re.I)
# the POPULATION statement, "N slots, M-byte stride" - not the first "N slots" anywhere: the registry page's
# frontmatter came to say "the other 26 slots" (the open subset, UQ-80), and the loose pattern read that as the
# population and refused a page that states 64 consistently (2026-09-27, OPUS)
STATED = re.compile(r"(\d+)\s+slots,\s*\d+\s*-\s*byte stride", re.I)

SLOT_LINE = re.compile(r"^\s*-\s*[\"']?(0x0[0-9A-Fa-f]{7})[\"']?\s*$")
# "retained" dirs hold byte-identical page copies kept as consumer preimages; their claims are receipts, not live
# claims (the rule FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES applies to check_questions; 2026-09-27, OPUS)
SKIP_DIRS = ("_index", "_templates", "_inbox", "retained")

# Container formats: named, counted, deliberately NOT scored (see the docstring).
CONTAINER_KEY = "container_format:"


def derive_population(db):
    """(start, end, stride, count) from the registry document, arithmetic cross-checked."""
    p = os.path.join(db, REGISTRY_DOC)
    t = io.open(p, encoding="utf-8", errors="replace").read()

    b = BOUNDS.search(t)
    s = STRIDE.search(t)
    if not b or not s:
        raise ValueError("registry document does not state bounds and stride in the expected form")
    start, end, stride = int(b.group(1), 16), int(b.group(2), 16), int(s.group(1))
    if stride <= 0 or end < start or (end - start) % stride:
        raise ValueError("bounds %08X-%08X do not lie on a %d-byte stride" % (start, end, stride))
    derived = (end - start) // stride + 1

    # Cross-check against the count the document states in words.  The two are produced
    # differently -- one by arithmetic here, one by a scan recorded there -- so agreement is
    # worth something and disagreement is worth stopping for.
    m = STATED.search(t)
    if m and int(m.group(1)) != derived:
        raise ValueError("registry states %s slots; bounds/stride give %d -- refusing to score "
                         "against a denominator its own source contradicts"
                         % (m.group(1), derived))
    return start, end, stride, derived


def claimed_slots(db):
    """slot -> [documents claiming it], from `registry_slots:` frontmatter lists."""
    out = collections.defaultdict(list)
    containers = collections.defaultdict(list)
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, db).replace(os.sep, "/")
            lines = io.open(path, encoding="utf-8", errors="replace").read().split("\n")
            inside = False
            for line in lines:
                if line.startswith(CONTAINER_KEY):
                    name = line[len(CONTAINER_KEY):].strip().strip("\"'")
                    if name:
                        containers[name].append(rel)
                    continue
                if line.strip().startswith("registry_slots:"):
                    inside = True
                    continue
                if inside:
                    m = SLOT_LINE.match(line)
                    if m:
                        out[int(m.group(1), 16)].append(rel)
                    elif line.strip():
                        inside = False
    return out, containers


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--quiet", action="store_true",
                    help="one machine-readable line: covered<TAB>total<TAB>containers")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        import tempfile
        return self_test(tempfile.mkdtemp())
    if not a.db:
        return ap.error("--db required unless --self-test")

    start, end, stride, total = derive_population(a.db)
    claims, containers = claimed_slots(a.db)

    valid = {s: d for s, d in claims.items()
             if start <= s <= end and (s - start) % stride == 0}
    stray = {s: d for s, d in claims.items() if s not in valid}
    collisions = {s: d for s, d in valid.items() if len(d) > 1}

    if a.quiet:
        print("%d\t%d\t%d" % (len(valid), total, len(containers)))
        # QUIET IS AN OUTPUT FORMAT, NOT A VERDICT. This returned 0 unconditionally, and --quiet is
        # the mode the publishing chain runs, so the one form of this gate anybody actually
        # exercised COULD NOT FAIL -- two registry slots have been claimed by two documents each
        # and every chain run since reported it green. The line stays one line for progress.py;
        # the exit code now says exactly what the full run says. 2026-09-14, OPUS.
        return 1 if (collisions or stray) else 0

    print("AUTHORED-DATA REGISTRY COVERAGE")
    print("  population: %d slots, %08X-%08X on an %d-byte stride"
          % (total, start, end, stride))
    print("              derived here from the registry document's own bounds, and cross-checked")
    print("              against the slot count it states. Not a target; a census.")
    print("")
    print("  covered:    %d / %d  (%.2f %%)" % (len(valid), total, 100.0 * len(valid) / total))
    print("")
    if valid:
        for s in sorted(valid):
            print("    %08X  %s" % (s, ", ".join(valid[s])))
    else:
        print("    (no document declares a `registry_slots:` list yet)")

    if containers:
        print("")
        print("  container formats documented: %d  -- COUNTED, NOT SCORED" % len(containers))
        print("  There is no censused universe of container formats, so a percentage here would")
        print("  be invented. A number without a denominator is honest; the alternative is not.")
        for name in sorted(containers):
            print("    %-28s %s" % (name, ", ".join(containers[name])))

    rc = 0
    if collisions:
        rc = 1
        print("")
        print("  SLOTS CLAIMED TWICE - no address is described two ways:")
        for s in sorted(collisions):
            print("    %08X  %s" % (s, ", ".join(collisions[s])))
    if stray:
        rc = 1
        print("")
        print("  CLAIMED SLOTS OUTSIDE THE REGISTRY (bad address, or the wrong array):")
        for s in sorted(stray):
            print("    %08X  %s" % (s, ", ".join(stray[s])))
    return rc


SELF_REGISTRY = """---
system: registry
---
| Address | Role | Verified |
|---|---|---|
| `0x02EBF008` - `0x02EBF1F8` | the registry: 63 slots, 8-byte stride | scanned |
"""

SELF_DOC_A = """---
system: a
registry_slots:
  - "0x02EBF0C0"
  - "0x02EBF138"
---
body
"""

SELF_DOC_B = """---
system: b
container_format: save-image
registry_slots:
  - "0x02EBF0C0"
  - "0x02FFFFF8"
---
body
"""


def self_test(tmp):
    db = os.path.join(tmp, "fmt_db")
    d = os.path.join(db, "02-Resource-And-Asset-Pipeline")
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(os.path.join(d, "authored-data-table-registry.md"), "w",
            encoding="utf-8").write(SELF_REGISTRY)
    io.open(os.path.join(db, "a.md"), "w", encoding="utf-8").write(SELF_DOC_A)
    io.open(os.path.join(db, "b.md"), "w", encoding="utf-8").write(SELF_DOC_B)

    start, end, stride, total = derive_population(db)
    if (start, end, stride, total) != (0x02EBF008, 0x02EBF1F8, 8, 63):
        print("SELF-TEST FAILED: population %08X-%08X/%d -> %d" % (start, end, stride, total))
        return 1
    claims, containers = claimed_slots(db)
    valid = {s for s in claims if start <= s <= end and (s - start) % stride == 0}
    if valid != {0x02EBF0C0, 0x02EBF138}:
        print("SELF-TEST FAILED: valid slots %s" % sorted("%08X" % s for s in valid))
        return 1
    if len(claims[0x02EBF0C0]) != 2:
        print("SELF-TEST FAILED: collision not detected")
        return 1
    if 0x02FFFFF8 in valid:
        print("SELF-TEST FAILED: out-of-registry slot accepted")
        return 1
    if list(containers) != ["save-image"]:
        print("SELF-TEST FAILED: containers %s" % list(containers))
        return 1

    # The cross-check must actually fire, or it is decoration.
    bad = SELF_REGISTRY.replace("63 slots", "99 slots")
    io.open(os.path.join(d, "authored-data-table-registry.md"), "w", encoding="utf-8").write(bad)
    try:
        derive_population(db)
    except ValueError:
        pass
    else:
        print("SELF-TEST FAILED: stated/derived disagreement did not raise")
        return 1

    print("self-test ok: 63 derived from bounds+stride and cross-checked, two slots counted, "
          "a collision and an out-of-registry slot both caught, and the disagreement guard fires")
    return 0


if __name__ == "__main__":
    sys.exit(main())
