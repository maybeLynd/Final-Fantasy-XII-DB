#!/usr/bin/env python3
"""types_census2.py - the L2 types cell, measured against the forms of state contracts actually write
(SWE2-AUDIT-SPEC, 2026-10-03, OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003 item 1).

WHY. The ruled criterion (L2-VERDICTS.md, "The criterion is ACCEPTED"): types is MET when EVERY piece of state the
contract names - its Types and State sections and interface-table state rows - has a declared type with a measured
extent, at the granularity the contract names it. The instrument behind 50 of 52 types cells,
`Tools/analysis-kit/gfz-scripts/contract_named_state_census.py`, extracts only one syntax of one kind of state:

  * outside a fence it matches a backtick span that is EXACTLY an address (`ADDR`, `0xADDR`, `[ADDR]`, `ADDR+0xN`),
    so `dword[02EBA3F8]`, `byte [02099011]`, `[02B57EF0 + 8*fam]` are never seen (S-39's handshake word);
  * it never extracts record-relative state (`ActionDefinition +0x13`, a fenced `CollisionBody` layout), which is
    most of what contracts name (S-22's element mask).

WHAT THIS DOES. For every contract credited by a row of L2-VERDICTS.md (important-subsystems.tsv column 6), inside
the same sections the old census reads (its own `state_sections`, reused unchanged so the denominator is the ruled
one), it extracts:

  ABS   every data address (.data/.bss, the old DATA_LO..DATA_HI) appearing ANYWHERE in a backtick span or a fence
        line, with an optional `+0xNN` displacement in the same token - resolved with the old census's resolve();
  REC   record-relative state: `Name +0xNN` (prose, tables, fences) and fenced layouts (a line holding only a type
        name followed by indented `+0xNN` lines) - Name resolved against types.tsv, then against ALIASES below
        (each alias carries its evidence), and the offset against the type's field rows (old field_at()).

Classes: ABS -> FIELD / GAP-SPAN / PTR-CELL / UNDECLARED / RANGE-END / RANGE-START (as the old census) / OBJECT;
         OBJECT (SWE2-AUDIT-SPEC ruling 2026-10-03, OPUS-REQ-AUDITSPEC-CENSUS2-BARE-BASE-1003): a bare address (no
         displacement) that is exactly the base of a declared data span (a STATIC/ARRAY/PARRAY route) and has no
         field row at +0 names the OBJECT, which the route already covers - not an undeclared field at +0. The
         contract need not invent a +0 field to satisfy the census. With a displacement, or off the base, the old
         classes stand;
         REC -> FIELD / GAP-SPAN / OUT-OF-EXTENT / UNTYPED (no declared type of that name or alias).
MEANING-OPEN flag: a FIELD whose store row is DISCOVERED/UNKNOWN or whose meaning text says the meaning is not
established, while the contract line gives that offset a meaning. It is a worklist flag, not a defect by itself.

CONTROL (--selftest, also run first by default): an embedded fixture in the old census's own section grammar holds
(a) `dword[02EBA3F8]` in a State section, (b) a fenced `ActionDefinition` layout with `+0x13`, (c) the positive
control `02AEE054` (declared FIELD) and `EvaluationContext +0x004` (declared). The control asserts that THIS
extractor finds all four and that the OLD extractor (contract_named_state_census.ADDR / FENCE_ADDR over the same
state_sections) finds (c) but misses (a) and (b). If this file's extraction regressed to the old one, the control
fails - it is sensitive to exactly the defect it exists for. The fixture is embedded, so repairing S-39/S-22 does
not break it.

LIMITS. A worklist, not a score. Prose outside the ruled sections is not the denominator and is not read (as ruled).
Offsets named without a type name on the same line or layout (`| +0x13 | ... |` tables) are counted per contract
as UNATTRIBUTED and need a hand read. Names that are not CamelCase identifiers and not declared types are skipped.
Heap/stack state named only in words is invisible to any regex.

    types_census2.py [--selftest]      writes census2.tsv and census2_systems.tsv next to this file
"""
import collections
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import contract_named_state_census as OLD  # noqa: E402

TICK = re.compile(r"`([^`\n]+)`")
ADDR_IN = re.compile(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])(?:\s*\+\s*0x([0-9A-Fa-f]{1,5}))?")
NAME = r"(?<![0-9A-Za-z_])([A-Z][A-Za-z0-9_]*[a-z][A-Za-z0-9_]*)"   # needs a lowercase letter: hex digits of an address are not a name
REC_INLINE = re.compile(NAME + r"`?\s*(?:\[\s*)?\+\s*`?\s*0x([0-9A-Fa-f]{1,5})\b")
LAYOUT_HEAD = re.compile(r"^\s*" + NAME + r"\s*(?:\{|:|\(.*\))?\s*$")
LAYOUT_ROW = re.compile(r"^\s+\+?\s*0x([0-9A-Fa-f]{1,5})\b|^\s+\+0x([0-9A-Fa-f]{1,5})\b")
TABLE_OFF = re.compile(r"^\|\s*`?\+0x[0-9A-Fa-f]{1,5}`?\s*\|")
CAMEL = re.compile(r"^[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+$")
HEXISH = re.compile(r"^[0-9A-Fa-f]+$")
OPEN = re.compile(r"not established|semantics open|meaning not claimed|unknown|no reader", re.I)

# Hand-checked aliases: contract working name -> declared type. Each needs its evidence; an alias with none is
# not applied. Built from this run's UNTYPED list (see README), each checked by field-row agreement.
ALIASES = {
    # CONTRACT-separation-pass.md layout +0x06 layer .. +0xF0/+0xF4 radii vs MovementBody 0x130 rows
    "CollisionBody": ("MovementBody", "S-19 cell names MovementBody 0x130 x128 as the family's type"),
    # CONTRACT-effect-layers.md's FormulaEvaluationContext is BattleFormula_BuildEvaluationContext's object
    "FormulaEvaluationContext": ("EvaluationContext", "same builder 003847C0; EvaluationContext is its declared type"),
    # CONTRACT-resource-section-addressing.md +0x04 mode / +0x30 handle / +0x38 cache = RenderResourceEntry +0x004 kind
    # (row cites 00409600 ResourceEntry_GetResolvedBasePointer) / +0x030 reference / +0x038 resolvedCache
    "ResourceEntry": ("RenderResourceEntry", "store rows cite the contract's own accessors 00409600/00409730/00409A60"),
    # CONTRACT-heading-speed-to-position-delta.md +0x03 class bits / +0xB8 movement block = ActorStorageRecord
    # +0x003 packedKindAndSequence (kindCode << 5) / +0x0B8 contextPtr (Movement_SetSteeringMode reads it)
    "WorldActor": ("ActorStorageRecord", "+0x003 kind<<5 and +0x0B8 contextPtr rows match the layout"),
    # CONTRACT-binding-profiles.md 0x15C stride, +0x000 int[16], +0x040 entry[16] = InputBindingRecord 0x15C
    "BindingRecord": ("InputBindingRecord", "0x15C size, +0x000 digitalCodes[64 B], +0x040 axisEntries[256 B]"),
}
DEREF = re.compile(r"\*\s*\([^)]*\)\s*(?:0x)?0[0-9A-Fa-f]{7}\s*\+|\*\(\s*(?:0x)?0[0-9A-Fa-f]{7}\s*\)")


def load_types():
    names = set()
    for r in csv.DictReader(io.open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8"), delimiter="\t",
                            quoting=csv.QUOTE_NONE):
        names.add(r["type"])
    meaning = {}
    for r in csv.DictReader(io.open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8"), delimiter="\t",
                            quoting=csv.QUOTE_NONE):
        try:
            meaning[(r["type"], int(r["offset"], 16))] = (r.get("readiness") or "", r.get("meaning") or "")
        except (ValueError, TypeError):
            pass
    return names, meaning


def extract_new(text):
    """Yield (section, form, token, value, displacement_or_typename, line) for ABS and REC state."""
    layout = None
    for sec, line, fenced in OLD.state_sections(text):
        spans = [line] if fenced else TICK.findall(line)
        for sp in spans:
            for m in ADDR_IN.finditer(sp):
                v = int(m.group(1), 16)
                if OLD.DATA_LO <= v < OLD.DATA_HI:
                    yield sec, "ABS", m.group(0).strip(), v, int(m.group(2), 16) if m.group(2) else 0, line
        for m in REC_INLINE.finditer(line):
            yield sec, "REC", m.group(0), m.group(1), int(m.group(2), 16), line
        if fenced:
            h = LAYOUT_HEAD.match(line)
            r = LAYOUT_ROW.match(line)
            if h and not r:
                layout = h.group(1)
            elif r and layout:
                yield sec, "REC", "%s +0x%s" % (layout, r.group(1) or r.group(2)), layout, int(r.group(1) or r.group(2), 16), line
            elif not line.strip():
                layout = None
        else:
            layout = None
            if TABLE_OFF.match(line):
                yield sec, "UNATTRIBUTED", line.strip()[:60], None, None, line


def extract_old(text):
    for sec, line, fenced in OLD.state_sections(text):
        for m in (OLD.FENCE_ADDR if fenced else OLD.ADDR).finditer(line):
            yield int(m.group(1), 16)


FIXTURE = """# CONTRACT-fixture
## 3. Types

```
ActionDefinition
  +0x13  u8  element mask - 0x01 Fire
```

`EvaluationContext +0x004` is the merged flags word; `02AEE054` is the multiplier.

## 5. State

| read | `dword[02EBA3F8]` |
"""


def bare_base(v, d, cls, spans):
    """OBJECT when the token is a bare declared span base with no +0 field (see Classes)."""
    if d or cls != "GAP-SPAN":
        return None
    base = [sp for sp in spans if sp[0] == v and sp[3] != "pointer cell"]
    return base[0][2] if base else None


def selftest(names):
    new = list(extract_new(FIXTURE))
    old = set(extract_old(FIXTURE))
    abs_new = {v for _s, f, _t, v, _d, _l in new if f == "ABS"}
    rec_new = {(v, d) for _s, f, _t, v, d, _l in new if f == "REC"}
    checks = [
        ("new finds width-prefixed 02EBA3F8", 0x02EBA3F8 in abs_new),
        ("new finds fenced ActionDefinition +0x13", ("ActionDefinition", 0x13) in rec_new),
        ("new finds positive control 02AEE054", 0x02AEE054 in abs_new),
        ("new finds positive control EvaluationContext +0x004", ("EvaluationContext", 0x4) in rec_new),
        ("old finds positive control 02AEE054 (instrument alive)", 0x02AEE054 in old),
        ("old MISSES 02EBA3F8 (the blind spot exists)", 0x02EBA3F8 not in old),
        ("EvaluationContext is a declared type (store alive)", "EvaluationContext" in names),
    ]
    # bare-base OBJECT: sensitive both ways - a bare declared base is OBJECT, the same base + 8 is not, and an
    # address outside every span is never OBJECT
    sp = [(0x02097D20, 0x02097D20 + 2 * 0x860, "CameraContext", "static", 0x860)]
    checks += [
        ("bare declared base with no +0 field -> OBJECT", bare_base(0x02097D20, 0, "GAP-SPAN", sp) == "CameraContext"),
        ("base + displacement is not OBJECT", bare_base(0x02097D20, 8, "GAP-SPAN", sp) is None),
        ("an address off the span base is not OBJECT", bare_base(0x02097D28, 0, "GAP-SPAN", sp) is None),
        ("a FIELD at +0 stays FIELD", bare_base(0x02097D20, 0, "FIELD", sp) is None),
    ]
    for k, v in checks:
        print("  %-55s %s" % (k, "PASS" if v else "FAIL"))
    return all(v for _k, v in checks)


def credited():
    out = collections.defaultdict(list)
    for line in io.open(os.path.join(DB, "_index", "important-subsystems.tsv"), encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if p and p[0].startswith("S-") and len(p) > 5:
            for c in p[5].split(";"):
                c = c.strip()
                if c:
                    out[os.path.normpath(os.path.join(DB, "_index", c))].append(p[0])
    return out


def main():
    names, meaning = load_types()
    print("selftest:")
    ok = selftest(names)
    if not ok:
        print("SELFTEST FAILED - census not run")
        return 1
    if "--selftest" in sys.argv:
        return 0
    spans, fields, sizes = OLD.load_store()
    rows = []
    for path, systems in sorted(credited().items()):
        if not os.path.exists(path):
            rows.append((",".join(systems), os.path.relpath(path, DB), "-", "MISSING", "", "", "", "", ""))
            continue
        text = io.open(path, encoding="utf-8", errors="replace").read()
        seen = set()
        for sec, form, tok, v, d, line in extract_new(text):
            rel = os.path.relpath(path, DB).replace(os.sep, "/")
            if form == "ABS":
                key = ("A", v + d)
                if key in seen:
                    continue
                seen.add(key)
                cls, tname, where = OLD.resolve(v + d, spans, fields, sizes)
                ends = {int(m.group(2), 16) for m in OLD.RANGE.finditer(line)}
                starts = {int(m.group(1), 16): int(m.group(2), 16) for m in OLD.RANGE.finditer(line)}
                derefd = any(("%08X" % v).lower() in m.group(0).lower() for m in DEREF.finditer(line))
                if d and not derefd and cls == "UNDECLARED":
                    bcls, btype, _bw = OLD.resolve(v, spans, fields, sizes)
                    if bcls == "PTR-CELL" or btype.endswith("Pointer"):
                        cls, tname, where = "AMBIGUOUS-DEREF", btype, ("ADDR+0x%X where ADDR is a declared pointer cell (%s):"
                                                                        " likely the pointee's +0x%X - hand read" % (d, btype, d))
                if d and derefd:
                    # `*(char**)ADDR + off`: the displacement is on the POINTEE; classify the cell itself, mark DEREF
                    cls, tname, where = OLD.resolve(v, spans, fields, sizes)
                    where = "DEREF pointee +0x%X (pointee type needs a hand read); cell: %s" % (d, where)
                bb = bare_base(v, d, cls, spans)
                if bb:
                    cls, tname, where = "OBJECT", bb, ("the base of the declared %s span; the contract names the object,"
                                                         " covered by its route (bare-base ruling)" % bb)
                if cls in ("UNDECLARED", "GAP-SPAN") and v in ends:
                    cls = "RANGE-END"
                elif cls == "UNDECLARED" and v in starts and starts[v] > v:
                    if OLD.covered_fraction(v, starts[v], spans) >= 0.9:
                        cls, where = "RANGE-START", "start of a range >=90% declared (old census rule)"
                old_seen = v in set(extract_old(text))
                rows.append((",".join(systems), rel, sec[:40], form, "%08X%s" % (v, "+0x%X" % d if d else ""),
                             cls, tname, where, "" if old_seen else "NEW-ONLY"))
            elif form == "REC":
                if not (v in names or v in ALIASES or CAMEL.match(v)):
                    continue
                key = ("R", v, d)
                if key in seen:
                    continue
                seen.add(key)
                t = v if v in names else (ALIASES[v][0] if v in ALIASES else None)
                if t is None:
                    cls, where = "UNTYPED", "no declared type or alias named %s" % v
                else:
                    size = sizes.get(t)
                    if size is not None and d >= size:
                        cls, where = "OUT-OF-EXTENT", "+0x%X >= size 0x%X" % (d, size)
                    else:
                        cls, where = OLD.field_at(t, d, fields, sizes)
                flag = ""
                if cls == "FIELD" and t:
                    rd, mn = meaning.get((t, d), ("", ""))
                    if rd in ("DISCOVERED", "UNKNOWN") or OPEN.search(mn or ""):
                        flag = "MEANING-OPEN"
                rows.append((",".join(systems), rel, sec[:40], form, tok.strip()[:60], cls, t or "", where, flag))
            else:
                rows.append((",".join(systems), os.path.relpath(path, DB).replace(os.sep, "/"), sec[:40], form,
                             tok, "UNATTRIBUTED", "", "", ""))
    with io.open(os.path.join(HERE, "census2.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("systems\tcontract\tsection\tform\ttoken\tclass\ttype\twhere\tflag\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    per = collections.defaultdict(collections.Counter)
    for r in rows:
        for s in r[0].split(","):
            per[s][r[5]] += 1
            if r[8]:
                per[s][r[8]] += 1
    bad = ("UNDECLARED", "UNTYPED", "OUT-OF-EXTENT")
    with io.open(os.path.join(HERE, "census2_systems.tsv"), "w", encoding="utf-8", newline="\n") as f:
        cols = ["FIELD", "OBJECT", "GAP-SPAN", "PTR-CELL", "UNDECLARED", "UNTYPED", "OUT-OF-EXTENT", "RANGE-END",
                "UNATTRIBUTED", "MEANING-OPEN", "NEW-ONLY"]
        f.write("system\t" + "\t".join(cols) + "\n")
        for s in sorted(per, key=lambda x: int(x[2:]) if x[2:].isdigit() else 999):
            f.write(s + "\t" + "\t".join(str(per[s][c]) for c in cols) + "\n")
    tot = collections.Counter(r[5] for r in rows)
    print("rows %d  %s" % (len(rows), dict(tot)))
    print("systems with UNDECLARED/UNTYPED/OUT-OF-EXTENT:",
          sorted((s for s in per if any(per[s][b] for b in bad)), key=lambda x: int(x[2:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
