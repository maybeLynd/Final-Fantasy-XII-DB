#!/usr/bin/env python3
"""check_name_artifacts.py - a field NAME that is really a fragment of its own row.

`named` is a headline figure: PROGRAM-STATE, TYPE-COVERAGE and COVERAGE-DIMENSIONS all quote it,
and every percentage derived from it is only as good as the claim that a named field has a name.
On 2026-09-16, twenty-eight did not. Three separate machine derivations, each reproducible from the
row itself, which is what proves none of them was ever a reading of the field:

    the meaning's first words, camel-cased    "**a copy of the action block...**"  -> aCopyOfThe
    the last two hex digits of two addresses  002681E0 + 002682B5                  -> e0B5
    addresses and words glued together        002E5180, 002E5264, Movement_Update  ->
                                              e5180E5264MovementUpdateactorframe

The mangled ones settle it beyond argument: `theDefinitionSText`, `theTargetUnitS`,
`theSourceSMerged` each carry a stray capital S where an apostrophe-s was eaten from
"the definition's text". Nobody writes that. And `aByteTheResolver` sat on TWO different fields.

WHY A GATE AND NOT ANOTHER SWEEP. The first census was done by hand and MISSED the third
derivation - it was found afterwards by following an unrelated naming candidate and noticing that
its already-named neighbour was not a name either. A hand census that misses a third of its class
is the argument for an instrument, not against one.

THE HARD PART IS NOT FINDING FRAGMENTS, IT IS NOT FLAGGING GOOD NAMES. Most names that echo their
meaning are fine: `baseHp`, `maxHp`, `parryChance` match the meaning's opening because a good
meaning starts by naming the thing. "Derived from the meaning" is not evidence of a defect. So the
three tests below are each narrow, and each was checked against the whole store before being kept:

  LEADING ARTICLE   a name beginning `the`/`a`/`an` before a capital is a sentence fragment.
                    25 hits, every one genuine.
  DUPLICATE         one type naming two different offsets the same thing. 1 hit, genuine.
  FOREIGN ADDRESS   the last five characters of an 8-hex address in the row's MEANING appear in
                    the name, and are not the field's own offset. A name encoding its own offset is
                    ordinary house style - `blockX3244Flags` is "block +0x3244 flags" and
                    `recordField414Default` names the +0x414 it stamps, and all three such names in
                    the store are correct. A name encoding the addresses out of its own evidence
                    cell is not.

                    THE TEST RUNS FROM THE ADDRESS, NOT FROM THE NAME, and that is not a detail.
                    The first cut looked for hex RUNS in the name and asked whether any address
                    contained one - and it missed the very row this gate was built for, because
                    `e5180E5264...` is two address tails concatenated, a ten-character run no
                    eight-character address can contain. Asking each address whether its tail
                    appears in the name catches a concatenation of any length.

usage: check_name_artifacts.py [--db DB] [--self-test]
"""
import argparse
import collections
import io
import os
import re
import sys

ARTICLE = re.compile(r"^(the|a|an)(?=[A-Z])")
# A NAME THAT IS A SENTENCE ABOUT THE FIELD rather than a name for it. Anchored at the
# START on purpose: `headerDwordWritten` is a participle modifying a noun and is a
# perfectly good name, while `writtenTimesByBattleformula` is a predicate with its
# subject missing. Measured over 1,417 named fields: this flags exactly one, and it is
# the artifact.
PREDICATE = re.compile(r"^(written|writes|reads|read|stores|stored|touched|counted|used)(?=[A-Z])")
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")


def findings(rows, I):
    art, dup, foreign = [], [], []
    by_type = collections.defaultdict(list)
    for r in rows:
        if len(r) <= I["evidence"]:
            continue
        name = r[I["name"]].strip()
        if not name or name == "UNRESOLVED":
            continue
        t, off = r[I["type"]], r[I["offset"]]
        by_type[(t, name)].append(off)
        if ARTICLE.match(name):
            art.append((t, off, name, "begins with an article - a sentence fragment"))
            continue
        if PREDICATE.match(name):
            art.append((t, off, name,
                        "begins with a verb - a sentence about the field, not a name for it"))
            continue
        # THE TEST IS THE ADDRESS'S TAIL, NOT THE NAME'S HEX RUN. Matching runs was the first cut
        # and it missed the very row this gate was built for: `e5180E5264...` is TWO address tails
        # concatenated, so the run is ten characters and no eight-character address can contain it.
        # Going the other way - does this address's last five characters appear in the name -
        # catches a concatenation of any length, and five characters is long enough that a
        # coincidence is not worth worrying about.
        low = name.lower()
        own = off.lower().replace("0x", "").lstrip("0")
        for addr in ADDR.findall(r[I["meaning"]]):
            # FOUR, not five. e080WritesItNine carries the last FOUR characters of
            # 0038E080 and the five-character test missed it. Measured before the
            # change: at four characters this flags exactly one name across 1,417
            # and it is that artifact - the own-offset exemption below is what
            # keeps house style (`blockX3244Flags`) passing.
            tail = addr[-4:].lower()
            if tail.lstrip("0") == own:
                continue                        # the field's own offset - house style
            if tail in low:
                foreign.append((t, off, name,
                                "contains %r, the tail of %s from its own meaning" % (tail, addr)))
                break
    for (t, name), offs in by_type.items():
        if len(offs) > 1:
            dup.append((t, ", ".join(offs), name, "one name on %d different offsets" % len(offs)))
    return art + foreign + dup


def self_test():
    I = {"type": 0, "offset": 1, "name": 2, "meaning": 3, "evidence": 4}
    rows = [
        ["T", "0x718", "aCopyOfThe", "**a copy of the action block**", "ev"],
        ["T", "0x0B8", "e5180E5264MovementUpdateactorframe",
         "`002E5180` (`002E5264`); `Movement_UpdateActorFrame`", "ev"],
        ["T", "0x3244", "blockX3244Flags", "block +0x3244 flags (bit 0 kept)", "ev"],
        ["T", "0x028", "recordField414Default", "the value stamped into every record's +0x414",
         "ev"],
        ["T", "0x008", "baseHp", "base HP, the unmodified value", "ev"],
        ["T", "0x074", "writtenTimesByBattleformula",
         "written 40 times by BattleFormula_ResolveCandidateStatusApplications", "ev"],
        ["T", "0x078", "e080WritesItNine", "`0038E080` writes it nine times", "ev"],
        ["T", "0x03C", "headerDwordWritten", "header dword written by the finalizer", "ev"],
        ["U", "0x08C", "sameName", "one thing", "ev"],
        ["U", "0x090", "sameName", "another thing", "ev"],
    ]
    got = {(f[1], f[2]) for f in findings(rows, I)}
    cases = [
        (("0x718", "aCopyOfThe"), True, "a sentence fragment fires"),
        (("0x0B8", "e5180E5264MovementUpdateactorframe"), True,
         "an address tail out of its own meaning fires"),
        (("0x3244", "blockX3244Flags"), False, "a name encoding its OWN offset does not"),
        (("0x028", "recordField414Default"), False, "a name encoding a field offset does not"),
        (("0x008", "baseHp"), False, "a good name that echoes its meaning does not"),
        (("0x074", "writtenTimesByBattleformula"), True,
         "a name that is a sentence about the field fires"),
        (("0x078", "e080WritesItNine"), True,
         "a FOUR-character address tail fires"),
        (("0x03C", "headerDwordWritten"), False,
         "a participle modifying a noun does NOT fire"),
        (("0x08C, 0x090", "sameName"), True, "one name on two offsets fires"),
    ]
    ok = True
    for key, want, why in cases:
        hit = key in got
        if hit != want:
            ok = False
        print("  %s %-52s %s" % ("ok  " if hit == want else "FAIL", why, hit))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join("Database", "FFXII TZA"))
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        print("check_name_artifacts self-test")
        return 0 if self_test() else 1

    p = os.path.join(a.db, "_types", "fields.tsv")
    if not os.path.exists(p):
        print("no field store at %s" % p)
        return 2
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    hdr = lines[0].split("\t")
    I = {k: hdr.index(k) for k in hdr}
    rows = [l.split("\t") for l in lines[1:] if l.strip()]

    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        control = self_test()
    if not control:
        print("CONTROL FAILED: the self-test does not pass, so the count below means nothing.")
        return 2

    named = sum(1 for r in rows if len(r) > I["name"]
                and r[I["name"]].strip() not in ("", "UNRESOLVED"))
    bad = findings(rows, I)
    print("a field name that is a fragment of its own row\n")
    print("  named fields          : %d" % named)
    print("  control               : all nine shapes classify correctly")
    print("  NAMES THAT ARE NOT NAMES : %d   <- the finding" % len(bad))
    if not bad:
        print("\nevery named field carries a name rather than a piece of its own row.")
        return 0
    print()
    for t, off, name, why in bad:
        print("  %-26s %-14s %-34s %s" % (t, off, name[:34], why))
    print("\n  A fragment is not a name. Withdraw it to UNRESOLVED unless the noun phrase under")
    print("  it is sound, in which case drop the article and keep it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
