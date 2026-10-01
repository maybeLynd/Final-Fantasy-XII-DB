#!/usr/bin/env python3
"""Propose `_types/` field rows from a published access census.

Seven `*-accesses.tsv` censuses exist in this database and the type store lags most
of them: `BattleStatsRecord` sat at 0x1C8 bytes with ZERO fields beside a 1,280-row
census, and `BattleUnit` at 40 bytes of 0xF50 beside a 1,777-row one. The knowledge
was recovered; it just never reached the store. This turns a census into proposed
rows so that propagation is mechanical and repeatable rather than hand-written once
per type.

WHAT IT WILL NOT DO
-------------------
**It never decides a width it cannot read off an instruction.** The width comes from
the operand form of the access itself (`byte ptr`, `word ptr`, `dword ptr`,
`qword ptr`, `xmmword`), never from the distance to the next offset. That rule exists
because inferring width from the next offset is how a 2-byte field becomes a 4-byte
one whenever the byte after it happens to be unused.

**It never silently resolves a displacement that shows more than one width.** Those
are reported and, unless `--accept-dominant` is given, left OUT of the emitted rows.
A displacement read both as `dword` and as `word` may be a coarse zeroing store over
a narrow field, a sub-field read of a wider one, or -- as `BattleStatsRecord +0x10`
turned out to be -- a UNION whose shape depends on a discriminator elsewhere in the
record. Those three cases look identical in a census and are distinguished only by
reading the disassembly, so the tool hands them back rather than guessing.

`--accept-dominant` applies one narrow rule to the ones it can defend: when a width
accounts for at least `--dominance` of the accesses AND every rival width is WIDER,
the rivals are treated as coarse stores and the narrow width wins. A rival that is
NARROWER is never overridden, because a narrow read of a wide field and a wide store
over narrow fields are not symmetric -- the first is a sub-field read and the second
is a candidate union.

Arrays are taken from the field map's own `u16[5]`-style type column, declared whole,
and their interior positions dropped; an array whose declared extent would collide
with the next field is reported instead of emitted.

    store_from_census.py --type BattleUnit \\
        --census "<...>/battle-unit-accesses.tsv" \\
        --page   "<...>/the-battle-unit-field-map.md" [--accept-dominant] [--apply]

Without `--apply` it prints the proposal and writes nothing.
"""
import argparse
import collections
import io
import os
import re
import sys

# gfz-scripts -> analysis-kit -> Tools -> Database -> the checkout
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")

# The operand form is the only thing that settles a width.
FORMS = (("xmmword", 16), ("qword ptr", 8), ("dword ptr", 4), ("byte ptr", 1))
PAGE_ROW = re.compile(r"^\| `\+0x([0-9A-Fa-f]+)` \| (\d+) \| ([^|]*)\| ([^|]*)\|")
ARRAY_CT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\[(\d+)\]$")
ELEM = {"u8": 1, "s8": 1, "i8": 1, "u16": 2, "s16": 2, "i16": 2,
        "u32": 4, "s32": 4, "i32": 4, "f32": 4, "u64": 8, "s64": 8, "f64": 8}
CT = {"u8": "uint8", "s8": "int8", "i8": "int8", "u16": "uint16", "s16": "int16",
      "i16": "int16", "u32": "uint32", "s32": "int32", "i32": "int32", "f32": "float",
      "u64": "uint64", "s64": "int64", "f64": "double"}


# `nop dword ptr [rax + rax]` is the multi-byte NOP encoding. It carries a ModRM
# memory operand purely to pad, and touches nothing -- but a census that walks memory
# operands records it, and `dword ptr` then reads as a 4-byte access. 48 such rows
# exist across the eight censuses. They must never vote on a width.
NOP = re.compile(r"^\s*nop", re.I)


def width_of(instruction):
    if NOP.match(instruction):
        return None
    i = instruction.lower()
    for token, w in FORMS:
        if token in i:
            return w
    # `word ptr` only after the wider spellings have been ruled out
    if "word ptr" in i:
        return 2
    return None


# `[rcx + rax*8]` has no displacement constant, so a census records it at +0x000.
# It is not a field access at offset zero: the width belongs to an ARRAY ELEMENT
# reached through the base, and counting it makes the field at +0x000 look like it
# has two widths. ActorManagerSlot +0x000 showed {8: 11, 4: 2} for exactly this
# reason -- the two 4s were `movss dword ptr [rcx + rax*8], xmm2`. Nine such rows
# exist across the seven censuses, so this is rare and worth setting aside rather
# than reasoning around.
INDEXED = re.compile(r"\[\s*\w+\s*\+\s*\w+\s*\*\s*[1248]\s*\]")


# An unrolled SIMD block copy reads a run of `movups xmmword` at consecutive 16-byte
# displacements. Each one is a MOVE, not a field: BattleUnit_SnapshotAndSuspendAction-
# State copies 9 * 0x80 bytes from unit+0x6B0 in one loop, and its eight unrolled
# `movups` land on eight displacements that are not 16 bytes wide and mostly not even
# 16-byte aligned fields. This is the SECOND time the idiom has corrupted a layout --
# the save payload map turned one unrolled iteration of a 0x200-byte copy into eight
# 16-byte fields, which is what OPUS-CONTRA-GROUPBANK was about. A function making
# four or more xmmword accesses to one type is copying it, so its xmmword rows are set
# aside from width voting and the functions are named.
BULK_XMM_MIN = 4


# Not every `*-accesses.tsv` is a FIELD census. formula-scratch-block-accesses.tsv
# carries `word, site, kind, instruction, function, name` - a census of global
# addresses, not struct offsets - and parsing it with the field-census column
# positions silently reads addresses as function names and function names as access
# kinds. It produced a plausible-looking "44 functions, 0 accesses" in another tool
# before anyone noticed. Refuse what we cannot read rather than mis-read it.
FIELD_CENSUS_HEADER = "function	name	site	disp	kind	instruction	route	note"


def read_census(path):
    per = collections.defaultdict(collections.Counter)
    example = {}
    rows = 0
    indexed_at_zero = 0
    indexed_unknown = 0
    xmm_by_fn = collections.Counter()
    raw = []
    for n, line in enumerate(io.open(path, encoding="utf-8")):
        if n == 0:
            if line.rstrip("\n") != FIELD_CENSUS_HEADER:
                raise SystemExit(
                    "%s is not a field census. Its header is:\n  %s\n"
                    "expected:\n  %s"
                    % (path, line.rstrip("\n"), FIELD_CENSUS_HEADER))
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 6:
            continue
        try:
            off = int(c[3], 16)
        except ValueError:
            continue
        rows += 1
        if off == 0 and INDEXED.search(c[5]):
            indexed_at_zero += 1
            continue
        if len(c) > 7 and c[7] == "idx?":
            # an unscaled second register the scan could not resolve: record + disp + unknown.
            # The displacement is not a field of this type (TWOREG, 2026-09-12).
            indexed_unknown += 1
            continue
        w = width_of(c[5])
        if w:
            if w == 16:
                xmm_by_fn[c[0]] += 1
            raw.append((off, w, c[0], c[2], c[5]))
    bulk = {fn for fn, n in xmm_by_fn.items() if n >= BULK_XMM_MIN}
    set_aside = 0
    for off, w, fn, site, ins in raw:
        if w == 16 and fn in bulk:
            set_aside += 1
            continue
        per[off][w] += 1
        example.setdefault((off, w), (site, ins))
    if indexed_unknown:
        print("  rows with an unresolved second register (`idx?`) set aside: %d (record + disp + unknown, not a field at disp)"
              % indexed_unknown)
    return per, example, rows, indexed_at_zero, sorted(bulk), set_aside


def read_page(path):
    """offset -> (declared size, type token, description) from the field map table."""
    out = {}
    if not path or not os.path.exists(path):
        return out
    for line in io.open(path, encoding="utf-8"):
        m = PAGE_ROW.match(line.strip())
        if not m:
            continue
        off = int(m.group(1), 16)
        desc = m.group(4).strip()
        if "not named by any page" in desc:
            desc = ""
        ct = m.group(3).strip()
        # NOT every field map puts a type in its third column. The save pages put the
        # DESCRIPTION there, and taking it as a ctype wrote sentences like "active or
        # pending field id (world-transition record)" into 32 rows' type column. A type
        # is one token; anything with a space or longer than a type name is prose, and
        # prose belongs in the meaning column if anywhere.
        if " " in ct or len(ct) > 24:
            if not desc or desc == ct:
                desc = ct
            ct = ""
        out[off] = (int(m.group(2)), ct, desc)
    return out


def short_name(desc):
    """A store identifier from the page's prose, or UNRESOLVED. Deliberately dumb:
    a bad auto-name is worse than none, so anything unclear stays UNRESOLVED."""
    if not desc:
        return "UNRESOLVED"
    bold = re.search(r"\*\*(.+?)\*\*", desc)
    text = (bold.group(1) if bold else desc)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"[`*]", "", text).strip()
    if text.startswith("inside "):
        return "UNRESOLVED"
    # A cell that is ENTIRELY italic is the field map's convention for a remark
    # about the record-keeping - `*not in the store*`, `*not named by any page*` -
    # rather than a description of the field. Naming a field from one produced
    # seventeen rows called `notInTheStore`, which asserts the opposite of what the
    # page was saying. Anything wholly italic is a remark, never a name.
    if desc.startswith("*") and desc.endswith("*") and desc.count("*") <= 4:
        return "UNRESOLVED"
    words = re.findall(r"[A-Za-z][A-Za-z0-9]*", text)[:4]
    if not words or len(" ".join(words)) < 3:
        return "UNRESOLVED"
    head = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    return head if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", head) else "UNRESOLVED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--census", required=True)
    ap.add_argument("--page")
    ap.add_argument("--fields", default=FIELDS)
    ap.add_argument("--accept-dominant", action="store_true")
    ap.add_argument("--dominance", type=float, default=0.75)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    per, example, rows, indexed0, bulk_fns, bulk_n = read_census(a.census)
    page = read_page(a.page)
    print("census rows %d, displacements with a readable width %d" % (rows, len(per)))
    if indexed0:
        print("  indexed accesses at +0x000 set aside: %d (array elements, not a field there)"
              % indexed0)
    if bulk_fns:
        print("  xmmword rows set aside as BLOCK COPIES: %d, from %s"
              % (bulk_n, ", ".join(bulk_fns)))

    # Rows already in the store occupy SPANS, not points. Skipping a proposal only
    # when its offset collides exactly would let a new row land inside an existing
    # one -- `BattleUnit +0x000` is already 8 bytes, so a proposal at +0x004 is
    # inside it, not beside it. Read the extents and treat them as occupied.
    existing = []
    for line in io.open(a.fields, encoding="utf-8"):
        c = line.rstrip("\n").split("\t")
        if len(c) > 2 and c[0] == a.type:
            try:
                existing.append((int(c[1], 16), int(c[2])))
            except ValueError:
                pass
    existing.sort()
    if existing:
        print("  already in the store       %d row(s), %d byte(s)"
              % (len(existing), sum(w for _, w in existing)))

    def occupied(off, size):
        return any(off < e + w and e < off + size for e, w in existing)

    # 1. arrays from the page's own type column
    arrays = {}
    for off, (size, ct, desc) in sorted(page.items()):
        m = ARRAY_CT.match(ct)
        if not m or m.group(1) not in ELEM:
            continue
        arrays[off] = (ELEM[m.group(1)] * int(m.group(2)), ct, desc)

    # 2. settle each displacement
    emit, conflicts, settled, interior = [], [], [], 0
    for off in sorted(per):
        if any(b <= off < b + arrays[b][0] for b in arrays if b != off):
            interior += 1
            continue
        if off in arrays:
            size, ct, desc = arrays[off]
            emit.append((off, size, short_name(desc), CT.get(ct, ct), desc, off))
            continue
        c = per[off]
        best, n = c.most_common(1)[0]
        if len(c) > 1:
            rivals = [w for w in c if w != best]
            defensible = (n >= a.dominance * sum(c.values())) and all(w > best for w in rivals)
            if not (a.accept_dominant and defensible):
                # A displacement already covered by a declared row is settled, whatever
                # the census says about it -- reporting it as a conflict overstates the
                # backlog. BattleSystemState reported 32 and most were already declared,
                # which made the real adjudication job look several times larger than it
                # was. Count them separately so neither number is lost.
                if occupied(off, best):
                    settled.append(off)
                else:
                    conflicts.append((off, dict(c)))
                continue
        size = best
        _, ct, desc = page.get(off, (None, "", ""))
        emit.append((off, size, short_name(desc), CT.get(ct, ct) or "UNRESOLVED", desc, off))

    # 3. overlaps are a defect in the proposal, never something to paper over
    emit.sort()
    kept, dropped, held, end = [], [], [], -1
    for r in emit:
        if r[0] < end:
            dropped.append(r[0])
        elif occupied(r[0], r[1]):
            held.append(r[0])
            end = max(end, r[0] + r[1])
        else:
            kept.append(r)
            end = r[0] + r[1]
    if held:
        print("  inside an existing row     %d: %s"
              % (len(held), ", ".join("+0x%03X" % h for h in held[:12])))

    print("  arrays declared whole      %d" % len(arrays))
    print("  interior positions dropped %d" % interior)
    print("  rows proposed              %d  (%d bytes)"
          % (len(kept), sum(r[1] for r in kept)))
    if settled:
        print("  multi-width but ALREADY DECLARED, so settled: %d" % len(settled))
    print("  WITHHELD, width conflict   %d" % len(conflicts))
    for off, c in conflicts:
        print("      +0x%03X  %s   <- read the disassembly; may be a union" % (off, c))
    if dropped:
        print("  WITHHELD, would overlap    %d: %s"
              % (len(dropped), ", ".join("+0x%03X" % d for d in dropped)))

    if not a.apply:
        print("\n(dry run - pass --apply to write)")
        return 0

    lines = io.open(a.fields, encoding="utf-8", newline="").read().rstrip("\n").split("\n")
    # Compare offsets as NUMBERS. The store writes them at mixed widths -- 0x00,
    # 0x000 and 0x0008 all occur -- so a string comparison reads `0x004` and
    # `0x0004` as different keys and would append a duplicate row. The span guard
    # above would still catch the overlap, but a check that only works because
    # another check backs it up is not a check.
    have = set()
    for _l in lines:
        _c = _l.split("\t")
        if len(_c) > 1 and _c[0] == a.type:
            try:
                have.add(int(_c[1], 16))
            except ValueError:
                pass
    added = 0
    for off, size, name, ct, desc, src in kept:
        key = "0x%03X" % off
        if off in have:
            continue
        c = per.get(off, {})
        w = size if off not in arrays else (per[off].most_common(1)[0][0] if off in per else 0)
        ex = example.get((off, w))
        ev = ("width from the access instruction, never from the next offset: %d of %d observed "
              "accesses at this displacement are %d-byte"
              % (c.get(w, 0), sum(c.values()) or 0, w))
        if ex:
            ev += "; e.g. %s %s" % (ex[0], ex[1])
        if off in arrays:
            ev += ". Declared whole from the field map's %s; its interior positions are not " \
                  "separate fields" % arrays[off][1]
        ev += ". Census: " + os.path.basename(a.census)
        lines.append("\t".join([
            a.type, key, str(size), name, ct or "UNRESOLVED",
            re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", desc))[:600],
            "TYPE RESOLVED" if name != "UNRESOLVED" else "SIGNATURE RESOLVED", "PROVEN", ev]))
        added += 1
    io.open(a.fields, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
    print("\nappended %d row(s) for %s" % (added, a.type))
    return 0


if __name__ == "__main__":
    sys.exit(main())
