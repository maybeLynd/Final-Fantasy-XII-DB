#!/usr/bin/env python3
"""check_family_forms.py - a declared EC-7 family says its members are all N bytes. Are they?

`check_dispositions.py` is a stronger gate than it first looks: it already refuses a family whose
declared count disagrees with its members file, whose members are not function entries, that clashes
with another family, or that swallows an A-measured body. What it still cannot do is read the note.

`check_family_spans.py` covered the note's other testable shape - a link span - and reached 13 of the
94 families. **This one reaches far further**: 76 of the remaining 81 notes carry a UNIFORM SIZE
claim, written out as *"all 1,149 bodies are exactly 92 bytes"*, *"254 members all 53 bytes"*,
*"133 members, all 163 bytes"*. Those are the generated-code families - the reflection templates,
the deleting destructors, the static-initialiser registrations - and a uniform-size claim is the
strongest falsifiable statement in the whole EC-7 vocabulary: **one member of the wrong size refutes
it outright.**

    MATCH      every member's census body size equals the size the note claims
    MISMATCH   at least one does not                                    <- the finding
    NO-CLAIM   the inclusion clause states no single unambiguous size

NO-CLAIM is this checker declining, not a pass, and is reported separately.

On reading prose, again
-----------------------
The span checker reported three families as broken and was wrong all three times, because a family
note is structured prose: an inclusion rule, named individuals, a stated exception count, a
`Controls:` clause and a `NOT covered:` clause. The same discipline applies here and is enforced two
ways. Sizes are read from the INCLUSION CLAUSE ONLY, so a control sentence mentioning another
family's size cannot be mistaken for this family's claim; and a clause offering **more than one
distinct size** is declined outright rather than guessed at.
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# "all 1,149 bodies are exactly 92 bytes" / "254 members all 53 bytes" / "all 82 bytes"
SIZE = re.compile(r"\b(?:all|exactly|each)\s+(?:[\d,]+\s+(?:bodies|members|entries)\s+)?"
                  r"(?:are\s+)?(?:exactly\s+)?([\d,]{1,7})\s*bytes\b", re.I)


def sizes_claimed(clause):
    out = set()
    for m in SIZE.finditer(clause):
        try:
            out.add(int(m.group(1).replace(",", "")))
        except ValueError:
            pass
    return out



# "188 at 46 B", "110 at 75-76 B", "31 at 1,024 B" - a count and the size bucket it falls in.
VARIANT = re.compile(r"\b([\d,]{1,7})\s+at\s+([\d,]{1,7})(?:\s*-\s*([\d,]{1,7}))?\s*B\b")


# "301 B (203) and 302 B (120)" - the same partition with size first and the count in parentheses.
# NOT to be confused with "0063D010 (71 B)", an excluded address carrying its size: there the B is
# inside the parentheses, here it precedes them.
VARIANT2 = re.compile(r"\b([\d,]{1,7})\s*B\s*\(([\d,]{1,7})\)")


def variants_claimed(clause):
    """[(count, lo, hi)] - a declared partition of the membership by body size."""
    out = []
    for m in VARIANT2.finditer(clause):
        lo = int(m.group(1).replace(",", ""))
        n = int(m.group(2).replace(",", ""))
        out.append((n, lo, lo))
    for m in VARIANT.finditer(clause):
        n = int(m.group(1).replace(",", ""))
        lo = int(m.group(2).replace(",", ""))
        hi = int(m.group(3).replace(",", "")) if m.group(3) else lo
        if lo <= hi:
            out.append((n, lo, hi))
    return out


def check_variants(members, sizes, variants):
    """Return a list of complaints; empty means the declared partition reproduces exactly."""
    bad = []
    used = set()
    for n, lo, hi in variants:
        got = [m for m in members if m in sizes and lo <= sizes[m] <= hi]
        if len(got) != n:
            bad.append("declared %d members at %s B, census holds %d"
                       % (n, lo if lo == hi else "%d-%d" % (lo, hi), len(got)))
        used.update(got)
    # every member must land in some declared bucket, or the partition is not a partition
    stray = sorted(m for m in members if m in sizes and m not in used)
    if stray:
        bad.append("%d member(s) fall in NO declared size bucket, e.g. %08X (%d B)"
                   % (len(stray), stray[0], sizes[stray[0]]))
    return bad


def evaluate(db, sizes, parse_families, read_members, inclusion_clause):
    stats = collections.Counter()
    findings = []
    covered = collections.Counter()
    for doc, parts in parse_families(db):
        if len(parts) < 5:
            continue
        name, letter, rel, _c, note = (parts[0], parts[1], parts[2], parts[3],
                                       "|".join(parts[4:]))
        if letter not in ("B", "C", "D"):
            continue
        claimed = sizes_claimed(inclusion_clause(note))
        try:
            members = read_members(doc, rel)
        except (IOError, OSError, ValueError):
            stats["UNREADABLE"] += 1
            continue
        if len(claimed) != 1:
            # Second shape: a declared size PARTITION rather than one size.
            variants = variants_claimed(inclusion_clause(note))
            if variants:
                bad = check_variants(members, sizes, variants)
                if bad:
                    stats["MISMATCH"] += 1
                    covered["MISMATCH"] += len(members)
                    findings.append((os.path.basename(doc), name, letter,
                                     variants, len(members), bad))
                else:
                    stats["MATCH"] += 1
                    covered["MATCH"] += len(members)
                continue
            stats["NO-CLAIM"] += 1
            covered["NO-CLAIM"] += len(members)
            continue
        want = claimed.pop()
        wrong = sorted((m, sizes[m]) for m in members
                       if m in sizes and sizes[m] != want)
        if wrong:
            stats["MISMATCH"] += 1
            covered["MISMATCH"] += len(members)
            findings.append((os.path.basename(doc), name, letter, want,
                             len(members), wrong))
        else:
            stats["MATCH"] += 1
            covered["MATCH"] += len(members)
    return stats, covered, findings


def self_test():
    """A size checker that cannot fail a wrong family proves nothing."""
    sizes = {0x401000: 92, 0x401100: 92, 0x401200: 91}
    fams = [("d.md", ["fam-good", "C", "m.tsv", "2",
                      "all 2 bodies are exactly 92 bytes"]),
            ("d.md", ["fam-bad", "C", "m.tsv", "3",
                      "all 3 bodies are exactly 92 bytes"]),
            ("d.md", ["fam-two", "C", "m.tsv", "2",
                      "all 92 bytes, and the control family is all 40 bytes"])]
    mem = {"fam-good": [0x401000, 0x401100],
           "fam-bad": [0x401000, 0x401100, 0x401200],
           "fam-two": [0x401000, 0x401100]}
    cur = {"i": 0}
    order = ["fam-good", "fam-bad", "fam-two"]

    def pf(_db):
        return fams

    def rm(_doc, _rel):
        n = order[cur["i"]]
        cur["i"] += 1
        return mem[n]

    stats, _cov, find = evaluate(None, sizes, pf, rm, lambda n: n)
    ok = (stats["MATCH"] == 1 and stats["MISMATCH"] == 1 and stats["NO-CLAIM"] == 1
          and find and find[0][1] == "fam-bad" and find[0][5][0][1] == 91)
    print("self-test: %s  (match %d, mismatch %d, no-claim %d)"
          % ("PASS" if ok else "FAIL", stats["MATCH"], stats["MISMATCH"],
             stats["NO-CLAIM"]))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--functions")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")

    import check_dispositions as CD
    import check_family_spans as FS
    sizes = CD.load_functions(a.functions)
    stats, covered, findings = evaluate(a.db, sizes, CD.parse_families,
                                        CD.read_members, FS.inclusion_clause)

    total = stats["MATCH"] + stats["MISMATCH"] + stats["NO-CLAIM"]
    print("EC-7 family FORM check - are the members the size the note claims?")
    print("  %d declared B/C/D families" % total)
    print("    MATCH     %4d families %6d bodies   every member is the claimed size"
          % (stats["MATCH"], covered["MATCH"]))
    print("    MISMATCH  %4d families %6d bodies   <- the finding"
          % (stats["MISMATCH"], covered["MISMATCH"]))
    print("    NO-CLAIM  %4d families %6d bodies   no single unambiguous size; declining"
          % (stats["NO-CLAIM"], covered["NO-CLAIM"]))
    for doc, name, letter, want, n, wrong in findings:
        print("\n  %s :: %s  [%s]" % (doc, name, letter))
        if isinstance(want, list):
            print("    note declares a size partition over %d members: %s" % (
                n, "; ".join("%d at %s B" % (c, l if l == h else "%d-%d" % (l, h))
                             for c, l, h in want)))
            for line in wrong:
                print("      %s" % line)
        else:
            print("    note claims every one of %d members is %d bytes" % (n, want))
            print("    %d member(s) are not:" % len(wrong))
            for m, got in (wrong if a.list else wrong[:8]):
                print("      %08X  %d bytes" % (m, got))
            if not a.list and len(wrong) > 8:
                print("      ... %d more" % (len(wrong) - 8))
    return 0


if __name__ == "__main__":
    sys.exit(main())
