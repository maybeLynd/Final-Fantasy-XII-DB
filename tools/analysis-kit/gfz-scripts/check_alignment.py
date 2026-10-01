#!/usr/bin/env python3
"""check_alignment.py - the two ABI invariants nothing in this kit tests.

**NO INSTRUMENT HERE HAS EVER TESTED ALIGNMENT.** 112 `check_*` scripts, and the word `align`
appears in five of them only as prose about `nop` padding or about a control at a neighbouring
displacement. Yet alignment is one of the few hard, checkable facts about a struct compiled by MSVC
for x64, and a layout that violates it is either wrong or is something other than a struct:

  1. NATURAL ALIGNMENT   a scalar of width w sits at an offset that is a multiple of w.
  2. TAIL PADDING        a struct's size is a multiple of its strictest member's alignment, so
                         that an array of it keeps every element aligned.

A `uint32` at `+0x1A` is not a small error. It means the offset is wrong, or the record is packed
rather than compiled, or the row's `ctype` is the width of the WRITING INSTRUCTION rather than the
field. All three are worth knowing and they are not the same defect.

WHAT THIS DELIBERATELY DOES NOT DO
----------------------------------
**It does not take `ctype` as the field's width.** This store has a documented convention where
`size` is the field and `ctype` can be the width of the instruction that writes it -
`PostProcessParamContext +0x4A0` is `size = 1`, `ctype = uint32`, and it is a byte. Testing `ctype`
would report every one of those as misaligned and the report would be noise. **Alignment is taken
from `size`**, which is the field, and a row whose `ctype` disagrees is reported in a separate
column rather than flagged.

**It does not assume every type is a compiled struct.** A serialised record, a file header or a
wire format is packed on purpose and owes alignment nothing. A type whose rows are broadly
misaligned is far more likely to be one of those than to be broken, so the report gives each finding
its type's misaligned-row count and its category, and says which reading that supports.

Every earlier instrument in this kit over-reported on its first run - 90, 56, 9, 5, 16, 11353 - and
every time the cause was counting a shape instead of reading the rows. The columns below exist so
that this one can be read the same way without a second pass.

    python check_alignment.py --self-test
    python check_alignment.py

WHAT THIS GATE'S TWO HALVES TURNED OUT TO MEAN, measured 2026-09-19 (OPUS) by chasing every
finding to an instruction. THEY DO NOT BEHAVE THE SAME WAY AND A READER SHOULD NOT TREAT THEM
ALIKE:

  * THE NATURAL-ALIGNMENT HALF IS EXPECTED TO BE NON-EMPTY ON THIS IMAGE, and a non-empty list
    is NOT a backlog. Its findings carry a cited instruction AT THE MATCHING WIDTH - `mov word
    [rbx+0x21], r13w` at an odd offset, a `movsd` at 4 mod 8, two qwords at 0x3234/0x323C, a
    reflection-registered VVector2 at 0xDC, and so on. The image genuinely uses unaligned
    scalars and the store records them faithfully. Chasing these to zero would mean falsifying
    rows.

    BUT "NOT A BACKLOG" IS NOT "NOTHING TO CHECK", and this docstring said the stronger thing
    for a few hours. It read "all ELEVEN of its current findings are genuine", and one of the
    eleven was not: Widget +0xA1, upheld here on 2026-09-11 as a real unaligned uint16, was a
    COMBINED BYTE-PAIR INITIALISER READ AS ONE FIELD. `mov word ptr [rdi+0xa1], 0xff80` writes
    0x80 into +0xA1 and 0xFF into +0xA2, and both halves are addressed on their own elsewhere -
    +0xA1 read as a byte at 00245F38, +0xA2 written as a byte at 002483E9. Splitting it into
    two uint8 rows removed the only unaligned field in that type, and the count is ten.
    WHAT FOUND IT WAS NOT THIS GATE but check_census_widths, once Widget finally had a census
    wide enough to hold both accesses - which is the argument for censusing a type rather than
    arguing about it, and the reason the list is left unquantified here now.

  * THE TAIL-PADDING HALF IS WHERE A REAL STORE DEFECT TURNED UP. EvaluationContext was declared
    0x2A - the end of its last observed field - while its own builder 003847C0 stores a QWORD at
    +0x28, which writes through +0x30. The size was under-measured by six bytes and this check
    is what caught it. The other finding, FieldRecord at 0x3, is a genuine three-byte-stride
    packed record and needed nothing.

SO THE QUESTION TO ASK OF A FINDING HERE IS "IS THE SIZE RIGHT?" BEFORE "IS THE FIELD RIGHT?".
Every natural-alignment finding so far has been answered by "the field is right, it really is
unaligned"; the one real defect was answered by "the size is wrong". The comfortable reading -
"packed record, owes alignment nothing" - is correct sometimes and is how a working gate gets
quietly ignored, so it is worth one look at the constructor before it is applied.
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP

FIELDS = os.path.join(KP.DB, "_types", "fields.tsv")
TYPES = os.path.join(KP.DB, "_types", "types.tsv")

# A ctype that names a real scalar, used only to report agreement - never to drive the test.
W = {"uint8": 1, "u8": 1, "int8": 1, "i8": 1, "char": 1, "bool": 1, "byte": 1,
     "uint16": 2, "u16": 2, "int16": 2, "i16": 2, "short": 2, "word": 2,
     "uint32": 4, "u32": 4, "int32": 4, "i32": 4, "float": 4, "f32": 4, "dword": 4,
     "unsigned int": 4, "int": 4,
     "uint64": 8, "u64": 8, "int64": 8, "i64": 8, "double": 8, "f64": 8, "qword": 8,
     "void*": 8, "ptr": 8}
ARR = re.compile(r"^([A-Za-z_][A-Za-z0-9_ ]*?)\s*\[\s*(\d+)\s*\]$")


def ctype_width(ct):
    ct = (ct or "").strip()
    m = ARR.match(ct)
    if m:
        b = m.group(1).strip().lower()
        return W[b] * int(m.group(2)) if b in W else None
    return W.get(ct.lower())


def elem_align(size, ct):
    """The alignment this row's storage must satisfy.

    From `size`, not from `ctype`. A size of 1/2/4/8 is a scalar of that width. Anything else is an
    aggregate - an array or an unknown span - and an aggregate's alignment is its ELEMENT's, which
    the store does not record. For `u8[n]` the element is a byte and the answer is 1; otherwise the
    row is not testable and says so rather than guessing, because guessing 8 for every large span
    would invent findings out of spans nobody claimed were structs.
    """
    # THE ARRAY FORM IS TESTED FIRST, AND THE ORDER IS THE WHOLE POINT. Written the other way round
    # -- scalar shortcut first -- `u8[8]` has size 8 and was judged as a QWORD needing 8-byte
    # alignment, when it is eight bytes whose element alignment is 1 and which may sit anywhere.
    # That alone produced ten of the first run's thirty-nine findings, in a function whose entire
    # job was to avoid exactly this class of mistake.
    ct = (ct or "").strip()
    # AN EMPTY `ctype` ASSERTS NOTHING, so there is nothing to check. The `subAddr*` rows are the
    # case: no ctype, size 8, and a meaning that says "an address taken by <site> and passed on;
    # extent not established". The 8 records that a `lea` happened, NOT that an 8-byte field lives
    # there. Reading it as a qword made all four of them alignment findings about a width the store
    # never claimed.
    if not ct:
        return None
    m = ARR.match(ct)
    if m:
        b = m.group(1).strip().lower()
        return W[b] if b in W else None
    if size in (1, 2, 4, 8):
        return size
    return None


def scan(rows):
    """rows: (type, offset, size, name, ctype, meaning) -> misaligned, untestable"""
    bad, untestable = [], 0
    for ty, off, size, name, ct, meaning in rows:
        a = elem_align(size, ct)
        if a is None:
            untestable += 1
            continue
        if off % a:
            bad.append((ty, off, size, name, ct, a, off % a))
    return bad, untestable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fields", default=FIELDS)
    ap.add_argument("--types", default=TYPES)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        cases = [
            ("a dword on a dword boundary", [("T", 0x10, 4, "x", "uint32", "")], 0),
            ("a dword at +0x1A", [("T", 0x1A, 4, "x", "uint32", "")], 1),
            ("a byte anywhere", [("T", 0x1B, 1, "x", "uint8", "")], 0),
            ("a qword at +0x14", [("T", 0x14, 8, "p", "void*", "")], 1),
            ("a u8 span at an odd offset is fine", [("T", 0x13, 55, "s", "u8[55]", "")], 0),
            ("a span of unknown element is not judged", [("T", 0x13, 55, "s", "", "")], 0),
            ("size 1 / ctype uint32 is tested as a BYTE, not a dword",
             [("T", 0x4A1, 1, "x", "uint32", "ctor dword store makes this byte 0")], 0),
        ]
        for label, rows, n in cases:
            bad, _u = scan(rows)
            good = len(bad) == n
            ok = ok and good
            print("  %-56s misaligned=%d  %s" % (label, len(bad), "ok" if good else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    cat, tsize = {}, {}
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 3:
                continue
            cat[f[0]] = f[2]
            try:
                tsize[f[0]] = int(f[1], 0)
            except ValueError:
                pass

    rows = []
    with io.open(a.fields, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9:
                continue
            try:
                rows.append((f[0], int(f[1], 0), int(f[2], 0), f[3], f[4], f[5]))
            except ValueError:
                pass

    bad, untestable = scan(rows)
    per = collections.Counter(b[0] for b in bad)
    total_per_type = collections.Counter(r[0] for r in rows)

    print("=== 1. natural alignment ===")
    print("  field rows                        : %d" % len(rows))
    print("  testable (scalar size, or u8 span): %d" % (len(rows) - untestable))
    print("  not testable (aggregate, element width unrecorded): %d" % untestable)
    print("  MISALIGNED                        : %d  across %d type(s)" % (len(bad), len(per)))
    if bad:
        print()
        print("  %-30s %-8s %5s %-22s %-10s %5s %s"
              % ("type", "offset", "size", "name", "ctype", "align", "type's misaligned / rows"))
        for ty, off, size, name, ct, al, rem in sorted(bad, key=lambda x: (-per[x[0]], x[0], x[1])):
            print("  %-30s %-8s %5d %-22s %-10s %5d %d/%d  [%s]"
                  % (ty[:30], hex(off), size, name[:22], (ct or "")[:10], al,
                     per[ty], total_per_type[ty], cat.get(ty, "?")[:18]))
        print()
        print("  A type with MANY misaligned rows is most likely a packed/serialised record, which")
        print("  owes alignment nothing. A type with ONE is the interesting case: either the offset")
        print("  is wrong, or that row's size is.")
        print()
        # THE RESIDUE OF A REAL MISALIGNMENT IS RANDOM; a residue that is always the same is a
        # convention. A qword at offset = 4 (mod 8) cannot be a naturally-aligned qword field, but
        # it is exactly what TWO ADJACENT DWORDS look like when one 8-byte instruction covers them.
        res = collections.Counter((al, rem) for _t, _o, _s, _n, _c, al, rem in bad)
        print("  offset mod alignment - a flat spread means error, a spike means convention:")
        for (al, rem), n in sorted(res.items()):
            print("    align %d, offset %% %d == %d : %d row(s)" % (al, al, rem, n))
        unknown = [b for b in bad if re.match(r"(?i)^(unobserved|unknown|unread|pad)", b[3] or "")]
        print()
        print("  of the %d, rows whose NAME says nobody has read them (unobserved*/unknown*/pad*)"
              " : %d" % (len(bad), len(unknown)))
        print("  Those carry a width that is a SPAN LENGTH, not a proven scalar, so alignment says")
        print("  nothing about them - `u64` there means eight unread bytes, not a qword.")
        print("  Remaining rows with a semantic name : %d" % (len(bad) - len(unknown)))

    print()
    print("=== 2. tail padding: a type's size is a multiple of its strictest member alignment ===")
    strict = collections.defaultdict(int)
    for ty, off, size, name, ct, meaning in rows:
        al = elem_align(size, ct)
        if al:
            strict[ty] = max(strict[ty], al)
    viol = []
    for ty, al in sorted(strict.items()):
        s = tsize.get(ty)
        if s and al and s % al:
            viol.append((ty, s, al, s % al))
    print("  types with a known size and at least one testable member : %d"
          % len([t for t in strict if t in tsize]))
    print("  size NOT a multiple of the strictest member alignment    : %d" % len(viol))
    for ty, s, al, rem in viol:
        print("    %-30s size %-8s strictest align %d  remainder %d  [%s]"
              % (ty[:30], hex(s), al, rem, cat.get(ty, "?")[:18]))
    if not viol:
        print("    (none - every sized type can be arrayed without breaking its members)")
    return 1 if bad or viol else 0


if __name__ == "__main__":
    sys.exit(main())
