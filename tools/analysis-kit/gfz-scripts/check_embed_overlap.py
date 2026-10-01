#!/usr/bin/env python3
"""Does a parent's own rows describe bytes that a declared child already claims?

THE BLIND SPOT THIS EXISTS FOR. `types_index.py --validate` checks that a type's rows TILE its
extent - no gap, no overlap - and it does that per type. It cannot see the other overlap: a
child declared `EMBED Parent +0xNN` occupies part of the parent's extent, and if the parent
also describes those bytes with its own rows, the same memory is described twice by two types
that each validate perfectly. The store reported 0 errors with 24,608 such bytes in it.

FOUND BY WALKING INTO IT. `BattleMenuPanelWidget3010` is `EMBED ManagerSub0209BE80_AB30 +0xC0
stride=0x3010 count=2`, so two panels hold parent +0xC0..+0x60E0. The parent's own rows cover
exactly that: 1,616 + 4 + 22,988 = 24,608. Worse than duplicated spans, one of the parent's
rows there is a NAMED uint32 with cited evidence while the child calls the same bytes part of
an 11,704-byte unobserved span.

WHAT COUNTS AS A FINDING, AND WHAT DOES NOT. A parent is EXPECTED to cover the child's range
with something - the extent has to tile. The store's settled way of doing that is ONE row whose
`ctype` names the child, which is how OPUS-CONTRA-SAVENEST was dispositioned: `SavePayload` has
`persistentFlagPayloadRegion` with ctype `PersistentFlagPayload`. So:

  * a single parent row spanning the child's range whose ctype names the child -> CLEAN,
  * anything else - several rows, or one row that does not name the child -> REPORTED.

A reported row is not automatically wrong. An `unobserved` span is the mildest case and may
simply predate the child's declaration; a NAMED row is the serious one, because two types then
assert incompatible things about the same bytes.

THE CONTROL IS MANDATORY, on this kit's own convention, AND IT IS SYNTHETIC ON PURPOSE.
The first version of this gate used the AB30/panel pair as its positive control - the real
finding it was written to catch. That control passed for exactly as long as the defect existed.
When FABLE's rule-0 disposition was executed and the pair collapsed into one region row, the
gate began refusing its own output on a clean store: `CONTROL ... NOT REPORTED FAIL`. A control
whose subject is a repairable defect expires the moment somebody does the work.

So the control is now a store this script builds in memory: a parent whose own two rows cover a
declared child's range, which MUST be reported, and a parent covering its child with one row
naming it, which MUST NOT be. Both must hold or the output is refused. Neither can be repaired
out from under the gate, and together they show the walk can return both answers - a positive
control alone only shows it can say yes.
"""
import collections
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
EMBED = re.compile(r"^EMBED\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)"
                   r"(?:\s+stride=0x([0-9A-Fa-f]+))?(?:\s+count=(\d+))?")


def load():
    types, fields = {}, collections.defaultdict(list)
    for r in csv.DictReader(io.open(D + "types.tsv", encoding="utf-8"), delimiter="\t"):
        types[r["type"]] = r
    for r in csv.DictReader(io.open(D + "fields.tsv", encoding="utf-8"), delimiter="\t"):
        try:
            fields[r["type"]].append((int(r["offset"], 16), int(r["size"]), r["name"],
                                      r.get("ctype", "")))
        except ValueError:
            pass
    for v in fields.values():
        v.sort()
    return types, fields


def walk(types, fields):
    """The whole decision, over any (types, fields) pair - the real store or a synthetic one."""
    findings, clean = [], []
    for child, row in sorted(types.items()):
        try:
            csize = int((row.get("size") or ""), 16)
        except ValueError:
            continue
        for alt in (row.get("route") or "").split("|"):
            m = EMBED.match(alt.strip())
            if not m:
                continue
            parent, off = m.group(1), int(m.group(2), 16)
            stride = int(m.group(3), 16) if m.group(3) else csize
            count = int(m.group(4)) if m.group(4) else 1
            if parent not in types:
                continue
            lo, hi = off, off + stride * count
            cover = [(o, s, n, ct) for o, s, n, ct in fields.get(parent, [])
                     if o < hi and o + s > lo]
            if not cover:
                continue
            # THE SETTLED SHAPES, and the first version of this check reported all of them.
            # A parent MUST cover the child's range - its own extent has to tile - so the
            # question is never "does it cover", it is "does it cover with one opaque block or
            # with its own field structure". Clean:
            #   * ONE row spanning the child's whole range, whatever its ctype. Naming the
            #     child in `ctype` is the store's best form (SavePayload's
            #     `persistentFlagPayloadRegion`), but `embedded00A0 u8[21216]` says the same
            #     thing less precisely and is not a contradiction;
            #   * exactly `count` rows, each one stride long and aligned to an element - the
            #     instances named individually, as BattleMenuWidget2DC0 does with
            #     `childWidgetA00F0` / `childWidgetB1710`.
            # Reporting those buried the two real cases among thirteen.
            spans_whole = (len(cover) == 1 and cover[0][0] <= lo and cover[0][0] + cover[0][1] >= hi)
            per_element = (len(cover) == count
                           and all(c[1] == stride and (c[0] - lo) % stride == 0 for c in cover))
            if spans_whole or per_element:
                clean.append((parent, child, "one block" if spans_whole else "per element",
                              child in (cover[0][3] or "")))
                continue
            named = [c for c in cover if "unobserved" not in c[2].lower()]
            byts = sum(min(o + s, hi) - max(o, lo) for o, s, _n, _ct in cover)
            findings.append((byts, parent, child, lo, hi, cover, named))

    return findings, clean


# CONSTRUCTOR-PROVEN BASES (2026-09-27, OPUS). An EMBED route is one way two types come to share bytes; a base
# constructor is the other. Every type whose own construction site is proved to build a Widget at its base (the
# maintained receipt widget-header-embedding/verified-sites.json: 69 whole-object sites and one prefix site) carries the
# shared 0xC0 header. The header's truth lives on `Widget`; a derived type REFERENCES it with ONE row at +0x00 whose
# ctype is Widget. A derived type that describes those bytes with its own rows is the drift 26ccf838a normalised away
# (1,412 duplicated rows, +0x98 / +0x9C re-typed as dwords, +0xA1 as a word) - that is what this rejects.
# Not rejected: the derived type's own fields at or past +0xC0, and a PREFIX-constructed record (ManagerSub7FB0Record,
# a 0xF0 widget at the base of a 0x110 record) - the base rule constrains only [0, 0xC0).
# EXCEPTIONS must be explicit and carry a reason; there are none today.
BASE_RECEIPT = os.path.join(KP.DB, "_index", "candidates", "widget-header-embedding", "verified-sites.json")
BASE_EXCEPTIONS = {}   # type -> reason


def walk_bases(types, fields, derived, base="Widget"):
    """[(type, rows below the base's end)] for derived types that do not reference the base with one row."""
    sz = (types.get(base) or {}).get("size") or ""
    # Widget's size cell reads "VARIABLE the construction size argument (0 -> 0xC0; ...)": the base extent is what a
    # zero size argument builds, 0xC0 - the size every embedded widgetBase0000 row already carries
    m = re.match(r"^0x([0-9A-Fa-f]+)$", sz.strip()) or re.search(r"\b0 -> 0x([0-9A-Fa-f]+)", sz)
    if not m:
        return None
    bsize = int(m.group(1), 16)
    out = []
    for t in sorted(derived):
        if t in BASE_EXCEPTIONS:
            continue
        cover = [(o, s, n, ct) for o, s, n, ct in fields.get(t, []) if o < bsize]
        if len(cover) == 1 and cover[0][0] == 0 and cover[0][1] >= bsize and cover[0][3].strip() == base:
            continue
        out.append((t, cover))
    return out


def control_bases():
    """Three fabricated derived types: a re-described header (REPORTED), an embedded header plus a derived field
    (SILENT), and a prefix-constructed record whose tail outgrows the constructed widget (SILENT)."""
    types = {"Widget": {"size": "0xC0"}}
    fields = {
        "CtrlDerivedDirty": [(0x00, 0x98, "ctrlProc", "void*"), (0x98, 0x28, "ctrlWords", "uint32")],
        "CtrlDerivedClean": [(0x00, 0xC0, "widgetBase0000", "Widget"), (0xC0, 0x10, "ctrlOwnField", "uint32")],
        "CtrlPrefixRecord": [(0x00, 0xC0, "widgetBase0000", "Widget"), (0xC0, 0x30, "ctrlPrefixTail", "u8[48]"),
                             (0xF0, 0x20, "ctrlRecordTail", "u8[32]")],
    }
    got = walk_bases(types, fields, ["CtrlDerivedDirty", "CtrlDerivedClean", "CtrlPrefixRecord"])
    names = [g[0] for g in (got or [])]
    ok = names == ["CtrlDerivedDirty"]
    print("CONTROL  re-described header REPORTED: %s   embedded header + derived field SILENT: %s   "
          "prefix-constructed record SILENT: %s" % ("PASS" if "CtrlDerivedDirty" in names else "FAIL",
                                                   "PASS" if "CtrlDerivedClean" not in names else "FAIL",
                                                   "PASS" if "CtrlPrefixRecord" not in names else "FAIL"))
    return ok


def control():
    """Two fabricated pairs: one that must be reported, one that must not."""
    types = {
        "CtrlParentDirty": {"size": "0x100", "route": ""},
        "CtrlChildDirty": {"size": "0x100", "route": "EMBED CtrlParentDirty +0x0"},
        "CtrlParentClean": {"size": "0x100", "route": ""},
        "CtrlChildClean": {"size": "0x100", "route": "EMBED CtrlParentClean +0x0"},
    }
    fields = {
        # two rows over the child's range, one of them named: the shape this gate exists for
        "CtrlParentDirty": [(0x00, 0x80, "ctrlNamedField", "uint32"),
                            (0x80, 0x80, "unobservedSpanCtrl", "u8[128]")],
        # one row spanning the whole child and naming it: the settled form
        "CtrlParentClean": [(0x00, 0x100, "ctrlChildRegion", "CtrlChildClean")],
    }
    findings, clean = walk(types, fields)
    hit = [f for f in findings if (f[1], f[2]) == ("CtrlParentDirty", "CtrlChildDirty")]
    miss = [f for f in findings if (f[1], f[2]) == ("CtrlParentClean", "CtrlChildClean")]
    ok_named = bool(hit) and len(hit[0][6]) == 1
    print("CONTROL  two-row parent REPORTED: %s   one-row parent SILENT: %s   "
          "named row counted: %s"
          % ("PASS" if hit else "FAIL", "PASS" if not miss else "FAIL",
             "PASS" if ok_named else "FAIL"))
    return bool(hit) and not miss and ok_named


def main():
    if not control() or not control_bases():
        print("\ncontrol failed - the walk is broken and the output is refused")
        return 2
    print("  control passes - the absences below are meaningful\n")
    types, fields = load()
    findings, clean = walk(types, fields)
    print("PARENTS DESCRIBING BYTES A DECLARED CHILD ALREADY CLAIMS: %d" % len(findings))
    for byts, parent, child, lo, hi, cover, named in sorted(findings, reverse=True):
        flag = "  <== %d NAMED row(s)" % len(named) if named else ""
        print("\n  %-30s <- %-30s +0x%X..+0x%X  %s B%s"
              % (parent, child, lo, hi, format(byts, ","), flag))
        for o, s, n, ct in cover[:6]:
            print("        +0x%04X %-6d %-26s %s" % (o, s, n, ct))
    print("\nCLEAN - the parent covers the child with one opaque block, or one row per "
          "element: %d" % len(clean))
    untyped = [c for c in clean if not c[3]]
    print("   of those, %d do not name the child in `ctype`. The store's best form does "
          "(SavePayload's `persistentFlagPayloadRegion`); these say the same thing less "
          "precisely and are NOT contradictions." % len(untyped))
    import json
    try:
        derived = json.load(io.open(BASE_RECEIPT, encoding="utf-8"))
    except (OSError, ValueError):
        derived = None
    if derived is None:
        print("\nCONSTRUCTOR-PROVEN BASES: receipt unreadable (%s) - NOT CHECKED" % BASE_RECEIPT)
        base_bad = None
    else:
        base_bad = walk_bases(types, fields, derived)
        print("\nDERIVED TYPES RE-DESCRIBING THEIR CONSTRUCTOR-PROVEN Widget HEADER: %d (of %d proved; %d prefix-only "
              "sites, which prove base identity, not extent)"
              % (len(base_bad), len(derived), sum(1 for v in derived.values() if len(v) > 3 and v[3] != "whole")))
        for t, cover in base_bad:
            print("  %-34s %d row(s) below +0xC0, e.g. %s" % (t, len(cover), [(hex(o), n) for o, s, n, ct in cover[:3]]))
    print("\nA reported row is not automatically wrong: an `unobserved` span may simply predate")
    print("the child's declaration. A NAMED row is the serious case - two types then assert")
    print("incompatible things about the same bytes.")


if __name__ == "__main__":
    sys.exit(main() or 0)
