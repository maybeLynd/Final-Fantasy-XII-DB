"""Does each column of the type store hold what that column claims to hold?

check_generator_artifacts.py catches code that leaked into PROSE. Nothing checked the STORE, and
the store is written by scripts too. Four artefact classes have now been found in it, every one by
accident or by an ad-hoc grep rather than by a check:

  * PROSE IN THE CTYPE COLUMN - 32 rows reading "active or pending field id (world-transition
    record)" where a type belongs, because the save pages put the description in the column the
    generator read as the type.
  * A WRITER/READER COUNT PAIR IN THE CTYPE COLUMN - 88 rows reading "1 / 49" or "0 / 2".
  * A NAME THAT IS AN ADDRESS FRAGMENT - 42 rows named `e35b0E3a2a` or `cd0DddEb0Fbd`, which is
    what a generator emits when it concatenates the sites it found instead of a label anybody
    chose. These are the dangerous ones: a reader takes them for names and a reconstruction emits
    them as identifiers.
  * A RECORD-KEEPING PHRASE AS A NAME - 17 rows named `notInTheStore`, from field-map cells that
    said "not in the store".

Every one passed types_index --validate, because that checks offsets, widths and overlaps - the
things a layout can be wrong about - and a column holding the wrong KIND of value is not a layout
error. This checks the kind.

THE DISCRIMINATORS, and why each is drawn where it is
-----------------------------------------------------
A NAME is garbage when it is composed ENTIRELY of hex characters and at least six long. Drawn
there because a looser rule - "starts with hex-looking letters" - flagged baseHp, defence,
BackFace and dead_mask, which are real names that happen to begin with a, b, c, d, e or f. Six
characters keeps short legitimate names like `hp` and `mp` safe.

A CTYPE is not a type when it is a bare `N / M`, or contains a space that does NOT follow a C type
keyword. Both halves of that were learned from this checker's own first run: flagging every space
reported 220 rows of which 205 were `unsigned char` and its relatives, and a length rule flagged 146
more that were real namespaced Phyre names like `PAnimation::VPAnimationWeightedBlenderController`.
LENGTH IS NOT A DISCRIMINATOR and the rule is gone. The first run's 366 findings were 351 mine.

Nothing here rewrites anything. Both artefact classes found in the store were withdrawn to
UNRESOLVED with their content preserved in the evidence column, because a count pair and a
description are real observations that were simply in the wrong column - and that is a judgement
for a person, not for a checker.

    check_store_artifacts.py [--self-test]
"""
import io
import os
import re
import sys
import collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")

HEXNAME = re.compile(r"^[0-9a-fA-F]{6,}$")
COUNTPAIR = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")
PHRASE = re.compile(r"^(notInTheStore|notInThe\w+|seeAbove|unknown\d*)$", re.I)
# A C type can legitimately contain a space - `unsigned char`, `unsigned __int64`. Flagging every
# space reported 220 rows of which 205 were these; the rule now requires the space NOT to follow a
# type keyword.
CKEYWORD = re.compile(r"^(unsigned|signed|const|struct|enum|long|short|volatile)\b")
# A FUNCTION-POINTER TYPE IS A TYPE, and it necessarily contains spaces and parentheses. The
# "ctype is prose" rule fires on any ctype containing a space that does not START with one of the
# keywords above, so `void (*)(LegacyPs2GsTextureContext*, uint32)` - a well-formed declarator -
# was the report's last standing finding. Added 2026-09-19 (OPUS) after the twelve genuine
# findings alongside it were fixed and this one turned out to be the gate misreading a correct
# row. Checked against prose it must still catch: "not written and not read on any path",
# "a pointer to the bank table" and "writer 3 / reader 12" are all still flagged.
FNPTR = re.compile(r"^[A-Za-z_][\w:<>, *]*\(\s*\*\s*\)\s*\(.*\)$")


def check(path):
    findings = collections.defaultdict(list)
    rows = 0
    for n, line in enumerate(io.open(path, encoding="utf-8")):
        if not n or not line.strip():
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 5 or c[0] == "type":
            continue
        rows += 1
        t, off, name, ctype = c[0], c[1], c[3].strip(), c[4].strip()

        if name and name != "UNRESOLVED":
            if HEXNAME.match(name):
                findings["name is an address fragment"].append((t, off, name))
            elif PHRASE.match(name):
                findings["name is a record-keeping phrase"].append((t, off, name))

        if ctype and ctype != "UNRESOLVED":
            if COUNTPAIR.match(ctype):
                findings["ctype is a writer/reader count pair"].append((t, off, ctype))
            elif " " in ctype and not CKEYWORD.match(ctype) and not FNPTR.match(ctype):
                findings["ctype is prose, not a type"].append((t, off, ctype[:44]))
    return rows, findings


def main():
    rows, findings = check(FIELDS)
    total = sum(len(v) for v in findings.values())
    print("STORE ROWS CHECKED: %d" % rows)
    print("COLUMNS HOLDING THE WRONG KIND OF VALUE: %d" % total)
    for kind in sorted(findings):
        hits = findings[kind]
        print()
        print("  %s: %d" % (kind, len(hits)))
        by_type = collections.Counter(t for t, _, _ in hits)
        for t, k in by_type.most_common(6):
            print("      %-28s %d" % (t, k))
        for t, off, v in hits[:3]:
            print("        e.g. %s +%s  [%s]" % (t, off, v))
    if not total:
        print("  none - every name is a name and every ctype is a type")
    return 1 if total else 0


FIXTURES = [
    ("hex-fragment name", "T\t0x0\t4\te35b0E3a2a\tuint32\t\t\t\t", 1),
    ("legitimate name that starts hex-ish", "T\t0x0\t4\tbaseHp\tuint32\t\t\t\t", 0),
    ("legitimate name, all hex letters but short", "T\t0x0\t4\tface\tuint32\t\t\t\t", 0),
    ("count pair in ctype", "T\t0x0\t4\tfield\t1 / 49\t\t\t\t", 1),
    ("prose in ctype", "T\t0x0\t4\tfield\tactive or pending field id\t\t\t\t", 1),
    ("record-keeping phrase as name", "T\t0x0\t4\tnotInTheStore\tuint32\t\t\t\t", 1),
    ("a real array ctype", "T\t0x0\t56\tentries\tWorldLootDropEntry[7]\t\t\t\t", 0),
    ("a real pointer ctype", "T\t0x0\t8\tp\tBattleStatsRecord*\t\t\t\t", 0),
    ("UNRESOLVED is not an artefact", "T\t0x0\t4\tUNRESOLVED\tUNRESOLVED\t\t\t\t", 0),
]


def self_test():
    import tempfile
    ok = True
    for label, row, want in FIXTURES:
        fd, p = tempfile.mkstemp(suffix=".tsv")
        os.close(fd)
        with io.open(p, "w", encoding="utf-8") as fh:
            fh.write("type\toffset\tsize\tname\tctype\tmeaning\treadiness\tconfidence\tevidence\n")
            fh.write(row + "\n")
        _, f = check(p)
        got = sum(len(v) for v in f.values())
        os.unlink(p)
        good = got == want
        ok &= good
        print("  %-42s found %d, expected %d  %s" % (label, got, want, "ok" if good else "FAILED"))
    print()
    print("fixtures: %s" % ("all discriminate correctly" if ok else "A FIXTURE FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    raise SystemExit(main())
