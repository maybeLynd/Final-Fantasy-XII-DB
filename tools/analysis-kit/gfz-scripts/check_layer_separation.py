#!/usr/bin/env python3
"""FINAL-AUDIT-PROTOCOL pass 12 - layer separation: PrimaryOwner vs CodeDomain, overlap 0.

EVIDENCE-STANDARD, "The two orthogonal layers":

    PrimaryOwner (V120) - which FFXII subsystem owns the state/resource/lifecycle transaction?
                          An authority classification.
    CodeDomain   (V121) - what mechanism/library/runtime behaviour does this function implement?
                          May describe generic maths, containers, middleware or rendering
                          WITHOUT GRANTING ANY OWNERSHIP.

Pass 12 fails if any document conflates them. That has two halves and only one was ever checked.

READ THE HEADING ABOVE AS THE STANDARD NOW WORDS IT: "two INDEPENDENT layers - one label per
function". It said "orthogonal" until 2026-09-13, which invited the reading that one function may
carry both; it may not. The rule is stated in the imperative and the checkpoint verifier enforces
it, which is why HALF ONE below is a canary rather than a discriminator.

HALF ONE - THE LEDGER, A REGRESSION CANARY. Does any FUNCTION carry both layers? fas2_export.py already computes this
and prints it to stderr as a side effect of an export, so the measurement existed but was not a
protocol pass. It is recomputed here from the exported table rather than read from the snapshot
header, because EVIDENCE-STANDARD's own rule is that the GFZ is a claim and not a source.

HALF TWO - THE DOCUMENTS, which nothing checked. A document's `owner_layer:` frontmatter names the
layer it is written against. Three things can go wrong, and they are NOT the same defect:

  SHORTHAND       `PrimaryOwner:Script` where the ledger says `Script_VM_Native_Bridge`. A naming
                  inconsistency; the subsystem is real and the claim is right.
  INVENTED        `PrimaryOwner:Battle` - the ledger has no Battle owner at all; it splits combat
                  into CombatAction, CombatFormula and CombatAI. The document asserts an authority
                  the classification does not have.
  CONFLATION      `PrimaryOwner:Middleware_PhyreEngine`, `PrimaryOwner:Compiler_CRT_Runtime`,
                  `PrimaryOwner:Third_Party_Libraries`. THIS is what pass 12 hunts: middleware, the
                  CRT and third-party libraries are the standard's own examples of CodeDomain -
                  mechanism, explicitly granting no ownership - being written as ownership.

Reporting all three as one number would hide the only one that is a layer error.

Usage:
    python fas2_export.py <snapshot.fas2> --tsv fas2.tsv
    python check_layer_separation.py --db "Database/FFXII TZA" --fas2 fas2.tsv
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

# The standard's OWN CodeDomain examples - middleware, libraries, the compiler runtime. A
# PrimaryOwner label built from one of these is asserting ownership from a mechanism class.
#
# DELIBERATELY NARROW, AFTER THE FIRST VERSION OVER-REPORTED. It also matched `runtime` and
# `debug`, which took `PrimaryOwner:Runtime` and `PrimaryOwner:Debug` for conflations. They are
# not: the ledger HAS `CoreRuntimeScheduling`, so `Runtime` is most likely shorthand for a real
# owner, and `Debug` has no ledger counterpart at all, which makes it invented rather than
# conflated. Calling either a layer error would inflate the one bucket that must stay clean.
MECHANISM = re.compile(r'middleware|phyre|compiler|crt|third.?party|librar', re.I)


def norm(s):
    return re.sub(r'[^a-z]', '', s.lower())


class WrongInput(Exception):
    """The --fas2 file is not a fas2_export TSV. Distinct from 'the ledger is empty'."""


def ledger_owners(fas2_tsv):
    """-> (owner counts, functions carrying both layers), or raise WrongInput.

    THE COLUMNS ARE CHECKED FIRST, and that is the whole point. `coverage.tsv` sits beside
    `snapshot.fas2` in a Stage-4 verify directory and is the obvious thing to reach for; it has no
    header of this shape, so DictReader takes its V121_COVERAGE banner as the header and every
    `row.get('owner')` comes back None. The gate then printed "PrimaryOwner labels: 0", declared
    the canary quiet BECAUSE there was nothing to be noisy about, compared 164 document labels
    against an empty ledger, called all 164 INVENTED, filed them under "not a layer error" and
    EXITED 0. With the real export the same corpus reads 22 labels, 164 exact matches, zero
    conflations. A pass that cannot distinguish those two runs is not measuring anything.

    An empty ledger from a well-formed file is NOT an error here - that is a real reading and the
    caller reports it. Only a file without the columns is refused.
    """
    owners = collections.Counter()
    both = 0
    with io.open(fas2_tsv, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        missing = [c for c in ("owner", "code_domains") if c not in (reader.fieldnames or [])]
        if missing:
            raise WrongInput(
                "%s is missing the column(s) %s - this is not a fas2_export.py --tsv file.\n"
                "  Its header reads: %s\n"
                "  Generate the right one with:  fas2_export.py <snapshot.fas2> --tsv <out.tsv>"
                % (os.path.basename(fas2_tsv), ", ".join(missing),
                   ", ".join((reader.fieldnames or ["<none>"])[:6])))
        for row in reader:
            o = (row.get('owner') or '').strip()
            d = (row.get('code_domains') or '').strip()
            if o:
                owners[o] += 1
            if o and d:
                both += 1
    return owners, both


def doc_labels(db):
    labels = collections.defaultdict(list)
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs
                   if d not in ('_index', '_experiments') and not d.startswith('.')]
        for fn in files:
            if not fn.endswith('.md'):
                continue
            p = os.path.join(root, fn)
            t = io.open(p, encoding='utf-8', errors='replace').read()
            m = re.search(r'^owner_layer:\s*(.+)$', t, re.M)
            if not m:
                continue
            rel = os.path.relpath(p, db).replace(os.sep, '/')
            for lab in re.findall(r'PrimaryOwner:([A-Za-z0-9_.]+)', m.group(1)):
                labels[lab].append(rel)
    return labels


def classify(lab, owners):
    """SHORTHAND / INVENTED / CONFLATION for a label the ledger does not contain exactly."""
    if MECHANISM.search(lab):
        return 'CONFLATION'
    nl = norm(lab)
    for o in owners:
        no = norm(o)
        if no.startswith(nl) or nl.startswith(no):
            return 'SHORTHAND'
        # SpawnLifecycle vs Spawn_Encounter_Lifecycle: neither is a prefix of the other, but the
        # label's parts all appear in the ledger name, in order. A matcher that missed this would
        # report a naming slip as an invented subsystem.
        parts = re.findall(r'[A-Z][a-z]+|[a-z]+', lab)
        if parts and all(norm(x) in no for x in parts):
            return 'SHORTHAND'
    return 'INVENTED'


def self_test():
    """Both directions on the input precondition, because only one of them used to exist."""
    import tempfile
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("  FAIL %-56s got %r, want %r" % (label, got, want))
        else:
            print("  ok   %-56s %r" % (label, got))

    d = tempfile.mkdtemp(prefix="layer-")
    good = os.path.join(d, "export.tsv")
    io.open(good, "w", encoding="utf-8", newline="").write(
        "entry\tname\towner\tcode_domains\n"
        "00401000\tA\tUI\t\n"
        "00401100\tB\tAudio\t\n"
        "00401200\tC\t\tCxxRuntime\n")
    owners, both = ledger_owners(good)
    check("a well-formed export is read", (len(owners), both), (2, 0))

    empty = os.path.join(d, "empty.tsv")
    io.open(empty, "w", encoding="utf-8", newline="").write(
        "entry\tname\towner\tcode_domains\n00401000\tA\t\t\n")
    check("an EMPTY but well-formed export is a reading, not a refusal",
          len(ledger_owners(empty)[0]), 0)

    banner = os.path.join(d, "coverage.tsv")
    io.open(banner, "w", encoding="utf-8", newline="").write(
        "V121_COVERAGE internal=38161 owner=9409 overlap=0\n1\tActor.Something\n")
    try:
        ledger_owners(banner)
        check("a banner-headed file is REFUSED", "read", "WrongInput")
    except WrongInput:
        check("a banner-headed file is REFUSED", "WrongInput", "WrongInput")

    both_layers = os.path.join(d, "overlap.tsv")
    io.open(both_layers, "w", encoding="utf-8", newline="").write(
        "entry\tname\towner\tcode_domains\n00401000\tA\tUI\tCxxRuntime\n")
    check("the canary counts a function carrying BOTH layers", ledger_owners(both_layers)[1], 1)
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--db")
    ap.add_argument("--fas2",
                    help="fas2_export.py --tsv output for the certified snapshot")
    a = ap.parse_args(argv)
    if a.self_test:
        print("check_layer_separation self-test")
        return self_test()
    if not (a.db and a.fas2):
        return ap.error("--db and --fas2, or --self-test")

    try:
        owners, both = ledger_owners(a.fas2)
    except WrongInput as e:
        print("check_layer_separation: REFUSING - %s" % e)
        return 2
    print("FINAL-AUDIT-PROTOCOL pass 12 - layer separation")
    print("\n  HALF ONE - the ledger")
    print("    PrimaryOwner labels                : %d" % len(owners))
    print("    functions carrying BOTH layers     : %d" % both)
    # A CANARY, NOT A DISCRIMINATOR (2026-09-13, after FABLE-NOTICE-OPUS-LAYER-OVERLAP-RULE).
    # EVIDENCE-STANDARD states one label per function in the imperative and the checkpoint verifier
    # enforces it, so `both` cannot be non-zero while the pipeline is well formed. Printing 0 as
    # "PASS" overstates it: a canary that has never sung is not evidence that an audit discriminates.
    # Kept, because it would catch the tagger changing - and it still fails loudly if it ever fires.
    print("    -> %s" % ("CANARY QUIET: 0, as the one-label-per-function rule requires. This half "
                         "cannot fail while that rule holds upstream - it is a regression detector, "
                         "NOT a discriminating check. Half two is the half that can fail."
                         if both == 0 else
                         "FAIL: %d functions carry both layers" % both))

    labels = doc_labels(a.db)
    exact = {l: v for l, v in labels.items() if l in owners}
    off = {l: v for l, v in labels.items() if l not in owners}
    buckets = collections.defaultdict(dict)
    for lab, docs in off.items():
        buckets[classify(lab, owners)][lab] = docs

    print("\n  HALF TWO - the documents")
    print("    documents declaring a PrimaryOwner : %d"
          % len({d for v in labels.values() for d in v}))
    print("    labels matching the ledger exactly : %d distinct, %d uses"
          % (len(exact), sum(len(v) for v in exact.values())))
    for kind in ('CONFLATION', 'INVENTED', 'SHORTHAND'):
        b = buckets.get(kind, {})
        print("    %-11s : %d distinct, %d uses"
              % (kind, len(b), sum(len(v) for v in b.values())))

    conf = buckets.get('CONFLATION', {})
    if conf:
        print("\n  THE PASS-12 DEFECT - ownership asserted from a mechanism classification.")
        print("  The standard's CodeDomain examples are middleware, libraries and runtime, and it")
        print("  says in terms that they grant NO ownership:")
        for lab, docs in sorted(conf.items(), key=lambda kv: -len(kv[1])):
            print("    PrimaryOwner:%-24s x%d" % (lab, len(docs)))
            for d in docs:
                print("        %s" % d)

    inv = buckets.get('INVENTED', {})
    if inv:
        print("\n  NOT A LAYER ERROR, BUT AN AUTHORITY THE LEDGER DOES NOT HAVE:")
        for lab, docs in sorted(inv.items(), key=lambda kv: -len(kv[1])):
            print("    PrimaryOwner:%-24s x%-3d e.g. %s" % (lab, len(docs), docs[0][:52]))

    sh = buckets.get('SHORTHAND', {})
    if sh:
        print("\n  NAMING ONLY - the subsystem is real, the spelling is not the ledger's:")
        for lab, docs in sorted(sh.items(), key=lambda kv: -len(kv[1])):
            print("    %-26s x%d" % (lab, len(docs)))

    return 1 if (both or conf) else 0


if __name__ == '__main__':
    sys.exit(main())
