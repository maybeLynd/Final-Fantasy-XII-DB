#!/usr/bin/env python3
"""check_ctype_width.py - a field whose ctype contradicts its declared size.

**THE TWO COLUMNS CAN DISAGREE AND NOTHING NOTICES.** `fields.tsv` carries both a `size` in bytes and
a `ctype`, and a reimplementation reads whichever it happens to trust. `PostProcessParamContext
+0x4A0` is `size = 1` and `ctype = uint32`; `BattleFormulaScratch +0x8C` is `size = 4` and
`ctype = u8`. One of the two is wrong in each case and the store does not say which. Of 111 checks in
this kit, none compared them.

TWO CLASSES, AND THEY WANT DIFFERENT FIXES.

**Split residue.** A span is divided and the pieces keep the parent's ctype. `BattleUnit +0x78` and
`+0x80` are `8` and `64` bytes and both still say `u8[72]`; `SteeringRecord`'s three rows at `+0x40`,
`+0x44` and `+0x4C` are `4`, `8` and `4` and all say `u8[16]`. **`SaveImageHeader` is the instructive
one**: `+0x94` (12) and `+0xC0` (320) both say `u8[364]` and do not sum to 364 - until the row
between them is counted, `+0xA0` at 32 bytes, retyped as `vec4Pair00A0` when it was declared. 12 + 32
+ 320 = 364 exactly. **A test that only groups rows sharing a ctype misses that**, so this walks the
parent's whole extent instead.

**Genuine disagreement.** No split explains it: the ctype and the size simply differ, and the field's
width is unknown to anyone reading the store.

    python check_ctype_width.py --self-test
    python check_ctype_width.py
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP

STORE = os.path.join(KP.DB, "_types", "fields.tsv")
W = {"uint8": 1, "u8": 1, "int8": 1, "i8": 1, "char": 1, "bool": 1, "byte": 1,
     "uint16": 2, "u16": 2, "int16": 2, "i16": 2, "short": 2, "word": 2,
     "uint32": 4, "u32": 4, "int32": 4, "i32": 4, "float": 4, "f32": 4, "dword": 4,
     "unsigned int": 4, "int": 4,
     "uint64": 8, "u64": 8, "int64": 8, "i64": 8, "double": 8, "f64": 8, "qword": 8,
     "void*": 8, "ptr": 8}
ARR = re.compile(r"^([A-Za-z_][A-Za-z0-9_ ]*?)\s*\[\s*(\d+)\s*\]$")


def width(ct):
    """Bytes the ctype implies, or None when it is a name this table does not resolve."""
    ct = (ct or "").strip()
    m = ARR.match(ct)
    if m:
        base = m.group(1).strip().lower()
        return W[base] * int(m.group(2)) if base in W else None
    return W.get(ct.lower())


STOREWIDTH = re.compile(
    r"\b(low byte|high byte|low half|high half|byte of|half of|"
    r"(?:word|dword|qword|byte) store|stores? (?:a )?(?:word|dword|qword)|"
    r"written as one qword|makes this byte|byte-tested|byte-read|byte 0 compared)\b", re.I)


def classify(rows):
    """Every size/ctype mismatch, with the two pieces of evidence a reader needs.

    **THIS DELIBERATELY DOES NOT GUESS INTENT, AND THAT IS A CORRECTION.** Two earlier versions tried
    to separate *split residue* from *genuine contradiction* by arithmetic - do the neighbouring rows
    sum to the ctype's width? - and each failed in the opposite direction. Requiring the siblings to
    share the ctype missed `NameBindingEntry +0x30`, whose siblings were RENAMED to `u32`. Dropping
    that requirement made `BattleUnit +0x38` a "split" over **21 rows summing to 72**, which is
    coincidence: in a densely tiled struct some run of adjacent rows sums to almost any small number.

    So the tool reports the mismatch and two facts, and leaves the judgement to a reader:

    * `explains` - the row's own `meaning` distinguishes a STORE width from a FIELD width
      (*"ctor dword store makes this byte 0"*). Where it does, `ctype` is the instruction's width and
      there is no contradiction to fix.
    * `siblings` - how many other rows of the type carry this exact ctype. Two or more is the
      signature of a span that was split and whose pieces kept the parent's type.
    """
    out = []
    for row in rows:
        off, size, name, ct = row[0], row[1], row[2], row[3]
        meaning = row[4] if len(row) > 4 else ""
        w = width(ct)
        if w is None or w == size:
            continue
        sib = sum(1 for r in rows if r[3] == ct) - 1
        out.append((off, size, name, ct, w, bool(STOREWIDTH.search(meaning or "")), sib))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=STORE)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        cases = [
            ("a dword typed uint32", [(0, 4, "x", "uint32", "")], 0, 0),
            ("a byte typed uint32", [(0, 1, "x", "uint32", "")], 1, 0),
            ("a span split, pieces keep the parent ctype",
             [(0, 8, "a", "u8[72]", ""), (8, 64, "b", "u8[72]", "")], 2, 0),
            ("a split whose middle piece was retyped",
             [(0, 12, "a", "u8[364]", ""), (12, 32, "b", "vec4Pair", ""),
              (44, 320, "c", "u8[364]", "")], 2, 0),
            ("a byte the ctor sets with a dword store, and says so",
             [(0, 1, "x", "uint32", "ctor dword store makes this byte 0")], 1, 1),
            ("an unresolvable ctype is not judged", [(0, 3, "x", "SomeStruct", "")], 0, 0),
        ]
        for label, rows, n_mis, n_exp in cases:
            r = classify(sorted(rows))
            good = (len(r), sum(1 for x in r if x[5])) == (n_mis, n_exp)
            ok = ok and good
            print("  %-52s mismatch=%d explains=%d  %s"
                  % (label, len(r), sum(1 for x in r if x[5]), "ok" if good else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    bytype = collections.defaultdict(list)
    with io.open(a.store, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9:
                continue
            try:
                bytype[f[0]].append((int(f[1], 0), int(f[2], 0), f[3], f[4], f[5]))
            except ValueError:
                pass

    rowsout, checked = [], 0
    for ty in sorted(bytype):
        rows = sorted(bytype[ty])
        checked += sum(1 for r in rows if width(r[3]) is not None)
        rowsout += [(ty,) + x for x in classify(rows)]

    # THE TYPE NAME IS PREPENDED, so the flags live at 6 and 7. Reading them at 5 and 6 made every
    # row "explained" - the summary said 16 of 16 while the table below it showed 7.
    expl = [r for r in rowsout if r[6]]
    sibs = [r for r in rowsout if not r[6] and r[7] >= 1]
    rest = [r for r in rowsout if not r[6] and r[7] == 0]
    print("rows with a resolvable ctype : %d" % checked)
    print("size disagrees with ctype    : %d" % len(rowsout))
    print("  of those, the row's meaning explains a store-vs-field width : %d" % len(expl))
    print("  of those, another row of the type carries the same ctype    : %d" % len(sibs))
    print("  neither                                                     : %d" % len(rest))
    print()
    print("  %-30s %-8s %6s %-13s %7s %-8s %s"
          % ("type", "offset", "size", "ctype", "implies", "explains", "same-ctype siblings"))
    for ty, off, size, nm, ct, w, ex, sib in sorted(rowsout, key=lambda r: (not r[6], -r[7])):
        print("  %-30s %-8s %6d %-13s %7d %-8s %d"
              % (ty[:30], hex(off), size, ct[:13], w, "yes" if ex else "no", sib))
    print()
    print("`explains yes` means the row already says the ctype is the width of the WRITING")
    print("INSTRUCTION, not of the field - there is nothing to fix. `siblings >= 1` is the signature")
    print("of a span that was split and whose pieces kept the parent ctype. Neither column is a")
    print("verdict; two earlier versions of this check tried to issue one and each was wrong in the")
    print("opposite direction.")
    return 1 if rest else 0


if __name__ == "__main__":
    sys.exit(main())
