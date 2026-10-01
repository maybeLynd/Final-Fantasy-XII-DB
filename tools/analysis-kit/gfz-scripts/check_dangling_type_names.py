"""Find prose that names a type the store no longer declares.

WHY. A rename updates the typed columns - the `type` cell, the `route` that names a parent, the
`ctype` that spells a pointer - because checkers read those and complain. Prose is not read by
anything. On 2026-09-20 SWE2-STRUCT renamed ManagerSub0209AC30_00C0 to ManagerSub0209AC60_02F8_00C0;
the route followed and the ctype did not, which check_route_ctype_agreement.py caught at once. The
evidence cell that also names it was caught by nobody, and would have sat there indefinitely
pointing a reader at a type that does not exist.

HOW IT AVOIDS DROWNING IN NOISE. Prose is full of CamelCase that is not a type: function names,
field names, page titles, ordinary words. This does not try to recognise type names in general. It
looks only for tokens shaped like THIS STORE'S type names - CamelCase carrying an embedded or
trailing hex block of four or more digits, which is how nearly every declared type here is spelled
(ManagerSub0209AC30_00C0, PDeferredLightingSlot0080, BootSubBlock0338, ActiveLogEntry0198) - and
reports the ones that are not declared.

WHAT A HIT MEANS. Not automatically a defect. A cell may deliberately name a type that was renamed
away, precisely to record the rename, and a correction paragraph often must. The check says "this
prose names something undeclared"; a person says whether that is a stale reference or a deliberate
historical one. It is a reading list, like check_route_counts.py's.

Usage:  python check_dangling_type_names.py [--store <db>/_types] [--self-test]
"""
import argparse
import collections
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_types"))

# CamelCase with a hex block of >=4, optionally followed by _HEX - this store's type-name shape.
_SHAPE = re.compile(r"\b([A-Z][A-Za-z]*(?:[A-Z][A-Za-z]*)*[0-9A-F]{4,}(?:_[0-9A-F]{2,})?)\b")
_DIGIT = re.compile(r"[0-9]")


class SHAPE(object):
    """The regex plus one filter the regex cannot express cleanly.

    THE DIGIT REQUIREMENT IS LOAD-BEARING. `[0-9A-F]{4,}` also matches runs of hex LETTERS, so
    ordinary ALL-CAPS emphasis in prose matches the shape of a type name: TR-ACED, EMB-EDDED,
    ADDED, DEC-ODED. The first run of this check reported 33 "undeclared type names" whose top
    three were TRACED (192 mentions), EMBEDDED (48) and ADDED (48) - every one a word written in
    capitals, none a type. A real name in this store always carries an address or a size, so the
    hex block must contain at least one DIGIT.
    """

    @staticmethod
    def _ok(tok):
        m = re.search(r"[0-9A-F]{4,}(?:_[0-9A-F]{2,})?$", tok)
        return bool(m and _DIGIT.search(m.group(0)))

    @staticmethod
    def findall(text):
        return [t for t in _SHAPE.findall(text or "") if SHAPE._ok(t)]

    @staticmethod
    def fullmatch(tok):
        return bool(_SHAPE.fullmatch(tok)) and SHAPE._ok(tok)

PROSE = ("instance", "allocation_site", "ctor", "dtor", "evidence", "documents")

SELF_TEST = [
    ("ManagerSub0209AC30_00C0", True),
    ("PDeferredLightingSlot0080", True),
    ("BootSubBlock0338", True),
    ("ActiveLogEntry0198", True),
    ("BattleUnit", False),            # no hex block - correctly not matched
    ("SpawnRecord", False),
    ("0208E690", False),              # a bare address is not a type name
    ("CON-139", False),
    ("TRACED", False),               # hex LETTERS only - the false-positive class
    ("EMBEDDED", False),
    ("ADDED", False),
    ("DECODED", False),
]


def self_test():
    bad = 0
    for tok, want in SELF_TEST:
        got = bool(SHAPE.fullmatch(tok))
        if got != want:
            bad += 1
            print("MISS %-30s matched=%s want=%s" % (tok, got, want))
    print("shape self-test: %d case(s), %d failure(s)" % (len(SELF_TEST), bad))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", default=DEFAULT)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        raise SystemExit(1 if self_test() else 0)

    tl = io.open(os.path.join(a.store, "types.tsv"),
                 encoding="utf-8", newline="").read().split("\n")
    TH = {n: i for i, n in enumerate(tl[0].split("\t"))}
    declared = {l.split("\t")[0] for l in tl[1:] if l.strip()}

    fl = io.open(os.path.join(a.store, "fields.tsv"),
                 encoding="utf-8", newline="").read().split("\n")
    FH = {n: i for i, n in enumerate(fl[0].rstrip("\r").split("\t"))}

    hits = collections.defaultdict(list)
    for ln in tl[1:]:
        f = ln.split("\t")
        if len(f) <= TH["route"]:
            continue
        for col in PROSE:
            for tok in SHAPE.findall(f[TH[col]] or ""):
                if tok not in declared:
                    hits[tok].append(("types.tsv", f[TH["type"]], col))
    for ln in fl[1:]:
        f = ln.split("\t")
        if len(f) <= FH["evidence"]:
            continue
        for col in ("meaning", "evidence", "ctype"):
            for tok in SHAPE.findall(f[FH[col]] or ""):
                if tok not in declared:
                    hits[tok].append(("fields.tsv", "%s+%s" % (f[FH["type"]], f[FH["offset"]]), col))

    print("PROSE NAMING A TYPE THE STORE DOES NOT DECLARE\n")
    print("  declared types            %4d" % len(declared))
    print("  undeclared names in prose %4d" % len(hits))
    print()
    print("  A hit is a READING LIST entry, not a defect: a correction paragraph may name a type")
    print("  that was renamed away precisely in order to record the rename.")
    for tok in sorted(hits, key=lambda t: -len(hits[t])):
        where = hits[tok]
        print("\n   %-34s %d mention(s)" % (tok, len(where)))
        for f, row, col in where[:6]:
            print("        %-12s %-34s %s" % (f, row, col))


if __name__ == "__main__":
    main()
