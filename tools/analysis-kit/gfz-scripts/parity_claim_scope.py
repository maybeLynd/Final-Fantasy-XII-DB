#!/usr/bin/env python3
"""parity_claim_scope.py - is an unexercised contract claim WORK, or is it SCOPE?

`parity_status.py` reports how many of a contract's section-15 claims the harness exercises. At
this checkout that is 395 of 716, and the gap reads like a backlog. For a large part of it that
reading is wrong, and the harnesses say so themselves.

`storage_read` is the clearest case. Its contract describes a save/load subsystem - a message pump,
a queue, a controller dispatcher, a thirteen-kind dispatcher, path builders, client shims. Its
harness reconstructs and drives TWO bodies, the read and the restore. Five claims are exercised, and
they are exactly the five claims about those two bodies; forty-five of the remaining rows say some
form of *upstream*, *behind the dispatcher*, *not among this suite's entries*. Those claims are not
waiting for test cases. They are waiting for the pilot to become a subsystem harness - which is the
INTEGRATION dimension, not the CONTRACT one. `field_gate` is the same shape in different words:
"the first 120 bytes of 1,297 are executed and the rest is not".

**This reports a FLOOR, never an estimate.** A row counts as out-of-pilot-scope only when its own
reason carries a literal marker its author wrote for that purpose, and only when the reason does not
also assert that something IS run. Everything else is UNCLASSIFIED and is claimed to be neither
kind. The output is therefore "at least N of the unexercised rows are scope rather than work",
which is a lower bound and survives being wrong about every unclassified row.

Controls (`--self-test`)
------------------------
The real negative control is the corpus, not a sentence written to pass: **no marker may fire on any
row a harness declares EXERCISED.** Four rows failed that control when it was first run and each was
a genuine defect in the markers - two of them were nouns ("the allocator", "the initialiser") rather
than scope statements, and are gone. Each marker family must also fire on a reason that carries it.
"""
import argparse
import ast
import collections
import os
import re
import sys

import kit_paths as KP

DIFF = os.path.join(KP.ROOT, "Reconstruction", "Tests", "Differential")

# Literal markers, written by harness authors to mean "this claim is about code this pilot does not
# contain or does not reach". Each is a phrase, not an inference.
SCOPE_MARKERS = [
    ("not driven", r"\bnot driven\b|\bnever driven\b|\bundriven\b"),
    ("upstream of this suite", r"\bupstream\b"),
    ("out of scope", r"\bout of (?:this fixture's |this pilot's |)scope\b"),
    ("not among the entries", r"not among this suite's entries|this suite's entries never|"
                              r"is not among this suite|a different entry family"),
    ("behind a dispatcher", r"\bsits? behind\b"),
    ("never runs here", r"\bnever runs?\b|\bnever reach(?:es|ed)\b|"
                        r"\bnothing here (?:loads|builds|saves)\b"),
    ("a different function", r"\ba different function\b|\bthe setter, not\b|"
                             r"\bthe dispatch table, not\b"),
    ("past the driven part", r"\bpast the (?:gate|pass|publish|read|restore|prologue)\b|"
                             r"\bstops at the\b|\bthe tail of the \w+, not\b"),
    ("the loop is not entered", r"\bis not entered\b|\bnever entered\b"),
    ("an image-wide census", r"census across the image|over the whole image|"
                             r"\bset/clear site census\b"),
    ("only part of the body", r"the first [\d,]+ bytes of [\d,]+ are executed"),
]

# A reason that ALSO asserts something IS run is not a pure scope statement, whatever phrase it
# contains. Four EXERCISED rows taught this: class_descriptor says "what is NOT driven is a
# NON-empty list"; class_descriptor_dtor says "every release goes through 00584730, which is
# hooked. The ALLOCATION half is not driven"; ramp_channels says "the allocator runs against
# hooks"; verb_dispatch says "compared against the original ... not only on the initialiser ones".
# All four matched a marker until this guard existed.
POSITIVE_GUARD = re.compile(
    r"\bis compared\b|\bare compared\b|\bis hooked\b|\bruns against\b|\bis exercised\b|"
    r"\bgoes through\b|\bis driven\b|\bare driven\b|\bcompared byte for byte\b|"
    r"\bcompared against the original\b|\bthe comparison is\b", re.I)

PROBES = {
    "not driven": "the pump is not driven",
    "upstream of this suite": "00582540 is upstream of this suite",
    "out of scope": "the capture and restore pair, out of this fixture's scope",
    "not among the entries": "not among this suite's entries",
    "behind a dispatcher": "00580A80 sits behind the 0x1D dispatch",
    "never runs here": "the completion remapper never runs",
    "a different function": "a different function; the ladder's own behaviour",
    "past the driven part": "the publish is past the gate",
    "the loop is not entered": "the drive loop is not entered",
    "an image-wide census": "a set/clear site census across the image",
    "only part of the body": "the first 120 bytes of 1,297 are executed and the rest is not",
}


def contract_map(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except SyntaxError:
        return None
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CONTRACT_MAP":
            try:
                return ast.literal_eval(n.value)
            except ValueError:
                return None
    return None


def marker_of(why):
    if POSITIVE_GUARD.search(why):
        return None
    for name, pat in SCOPE_MARKERS:
        if re.search(pat, why, re.I):
            return name
    return None


def collect(diff_dir):
    out = {}
    for fn in sorted(os.listdir(diff_dir)):
        if not (fn.startswith("diff_") and fn.endswith(".py")):
            continue
        rows = contract_map(os.path.join(diff_dir, fn))
        if rows is not None:
            out[fn[5:-3]] = rows
    return out


def self_test(diff_dir):
    ok = True
    fired = []
    for name, rows in collect(diff_dir).items():
        for r in rows:
            if r[1] == "EXERCISED" and marker_of(r[2]):
                fired.append((name, marker_of(r[2]), r[2][:80]))
    print("  corpus negative control: %d EXERCISED row(s) match a scope marker%s"
          % (len(fired), "" if not fired else "  - THE MARKERS ARE TOO LOOSE"))
    for nm, m, why in fired[:10]:
        print("      %-22s [%s] %s" % (nm, m, why))
    ok = ok and not fired
    negative = "both sides are driven at a negative record index and both refuse"
    for name, _ in SCOPE_MARKERS:
        hit = marker_of(PROBES[name])
        good = hit == name and marker_of(negative) is None
        ok = ok and good
        print("  control %-24s %s" % (name, "FIRES" if good else "BROKEN (fired %r)" % hit))
    print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
    return 0 if ok else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", default=DIFF)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--full", action="store_true", help="every harness, not only the top fourteen")
    a = ap.parse_args()

    if a.self_test:
        return self_test(a.diff)

    status = collections.Counter()
    scope = collections.Counter()
    per = {}
    for name, rows in collect(a.diff).items():
        ex = un = sc = 0
        for r in rows:
            status[r[1]] += 1
            if r[1] == "EXERCISED":
                ex += 1
                continue
            un += 1
            m = marker_of(r[2])
            if m:
                sc += 1
                scope[m] += 1
        per[name] = (len(rows), ex, un, sc)

    tot_rows = sum(p[0] for p in per.values())
    tot_un = sum(p[2] for p in per.values())
    tot_sc = sum(p[3] for p in per.values())

    print("harnesses with a CONTRACT_MAP: %d" % len(per))
    print("section-15 rows mapped       : %d" % tot_rows)
    for k, v in status.most_common():
        print("   %-16s %d" % (k, v))
    print()
    print("Of the %d rows that are not EXERCISED, AT LEAST %d (%.0f %%) are SCOPE, not work."
          % (tot_un, tot_sc, 100.0 * tot_sc / max(tot_un, 1)))
    print("Their own reason carries a literal marker saying the claim is about code this pilot")
    print("does not contain or does not reach. The other %d are UNCLASSIFIED and are claimed to be"
          % (tot_un - tot_sc))
    print("neither: this is a floor, not an estimate.")
    print()
    for k, v in scope.most_common():
        print("   %-24s %d" % (k, v))
    print()
    print("%-24s %5s %5s %5s %5s   %s" % ("harness", "rows", "exer", "unex", "scope", "reading"))
    order = sorted(per.items(), key=lambda kv: -kv[1][2])
    for name, (rows, ex, un, sc) in (order if a.full else order[:14]):
        if un == 0:
            reading = "every testable claim exercised"
        elif sc == un:
            reading = "EVERY unexercised claim is out of this pilot's scope"
        elif sc == 0:
            reading = "no scope marker - these may be reachable work"
        else:
            reading = "%d of %d unexercised are scope" % (sc, un)
        print("%-24s %5d %5d %5d %5d   %s" % (name, rows, ex, un, sc, reading))
    if not a.full:
        print("   (--full for all %d)" % len(per))
    return 0


if __name__ == "__main__":
    sys.exit(main())
