#!/usr/bin/env python3
"""family_prover.py - is a candidate group ONE generated shape, or a thousand distinct functions?

Why this exists
---------------
`check_dispositions.py` verifies a family's **bookkeeping**: the members file exists, the count
matches, nobody claims a function twice.  **It does not and cannot verify that the members share a
shape** - that is the author's claim to make and the note's bar to meet.

This tool answers the shape question mechanically, and it was written because the answer contradicted
me.  I routed five `Native*` tag groups to FABLE as *"candidate B families, because a shared tag is
a shared shape."*  Run over those groups this reports roughly **one distinct shape per member** -
1,158 shapes across 1,331 members in the largest.  **A shared tag is a shared classification.  Only
shared bytes are a shared shape.**

How it decides
--------------
Take every member's complete body and **mask the operands that a generated family MUST vary**:

    * `E8`/`E9` rel32   - call and jump displacements
    * rip-relative `lea` / `mov` disp32 - addresses of vftables, statics and string literals

Then compare the remaining bytes.  A template-instantiated family collapses to a handful of images;
a group of individually written functions does not collapse at all.

**The mask is the instrument, and it has two known blind spots that are not hidden.** First: bodies
that differ only by an **immediate** - a field offset, a size, an index - are structurally one idiom
and will still show as distinct images.  `Phyre.ScriptVM.ObjectPointerAccessor` is the standing
example: two body sizes, 323 members, **323 distinct images**, because each accessor carries its own
field offset.  A group like that is *not disproved* by this tool; it is **unproved**, and it stays
undeclared until an instrument that can mask immediates says otherwise.  Reporting that difference
honestly is the whole point - a prover that called every failure a negative would be worse than no
prover.

Second, measured 2026-09-18 under OPUS-NOTE-SWE2-EC7-ABSTRACTDESC-48-BYTE-IMAGES: `masked()` walks
**bytes**, not instructions, so a literal `E8`/`E9`/REX byte inside an immediate is a false mask
trigger.  In the AbstractClassDescriptor constructors, `mov r9d, 0xE8` (member offset 58) makes the
scan skip the real `4C` REX of the `lea r8,[rip+disp32]` at offset 64, leaving that displacement
unmasked - 48 scan images where the operand-aware wildcard (verify_form_families.py /
gen_form_note.py) correctly counts 47.  Byte images quoted from this tool can overcount by exactly
this mechanism; the operand-aware mask is the canonical one.

Reading the output
------------------
    shapes == 1                      a generated family; declare it and state the shape in the note
    shapes few                       near-generated; check whether the sub-shapes differ only by an
                                     immediate before splitting them into separate rows
    shapes ~= members, sizes <= 3    UNPROVED, not disproved - one idiom differing by an immediate
    shapes ~= members, sizes many    NOT a family; do not write one row over it

**The size column is the discriminator, not the shape count.**  The first version of this file
ignored it and reported `ObjectPointerAccessor` - 323 members, **two** body sizes - as "not a
family", directly contradicting the blind-spot paragraph above.  A one-word verdict that disagrees
with its own caveat is worse than no verdict, because a reader trusts the word and never reaches
the paragraph.

Usage
-----
    python family_prover.py --db "Database/FFXII TZA"
    python family_prover.py --db "Database/FFXII TZA" --tag Phyre.ScriptVM.ObjectPushAdapter
    python family_prover.py --db "Database/FFXII TZA" --tag <tag> --emit members.tsv
"""
import argparse
import collections
import re
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_dispositions as cd          # noqa: E402
import frontier_census as fc             # noqa: E402

EXE = os.path.join(HERE, "..", "..", "work", "exe", "FFXII_TZA.exe")


def load_image(path=None):
    d = io.open(path or EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    image = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        vs, va, rs, pr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, vs, pr, rs))
    def off(va):
        r = va - image
        for sva, vs, pr, rs in secs:
            if sva <= r < sva + max(vs, rs):
                return pr + (r - sva)
        return None
    return d, off


def masked(d, off, a, n):
    """The body with every operand a generated family must vary blanked out."""
    o = off(a)
    if o is None:
        return None
    b = bytearray(d[o:o + n])
    i = 0
    while i < len(b) - 4:
        if b[i] in (0xE8, 0xE9):
            b[i + 1:i + 5] = b"\0\0\0\0"; i += 5; continue
        if b[i] in (0x48, 0x4C) and b[i + 1] in (0x8D, 0x8B, 0x89) and (b[i + 2] & 0xC7) == 0x05:
            b[i + 3:i + 7] = b"\0\0\0\0"; i += 7; continue
        i += 1
    return bytes(b)


def forms(d, off, a, n):
    """The body as a sequence of instruction FORMS: mnemonic + operand kinds, constants dropped.

    **This proves strictly less than `masked()` and the difference is the whole point.**
    `masked()` says *these bodies are the same bytes apart from addresses*.  This says *these
    bodies are the same instruction sequence, possibly with different constants* - which is what a
    per-field generated accessor looks like, and is also what two functions comparing against
    different thresholds look like.

    **An immediate can be the entire mechanic.**  Elsewhere in this database a single immediate is
    the difference between a unit dying at 0 HP and dying at 1000.  So a form match is evidence of
    a shared *shape*, never evidence that the constants do not matter, and a family declared on it
    must say what the varying constant IS - for the accessors, the field offset.

    Registers are kept.  Dropping them too would merge genuinely different code.
    """
    try:
        import capstone
    except ImportError:
        return None
    o = off(a)
    if o is None:
        return None
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    out = []
    for ins in md.disasm(d[o:o + n], a):
        ops = re.sub(r"\b(?:0x)?[0-9a-fA-F]{1,16}\b", "K", ins.op_str)
        out.append(ins.mnemonic + " " + ops)
    return tuple(out) if out else None


SIZE_SPREAD_IS_IDIOM = 3     # this few distinct body sizes over many members is one idiom


def verdict(n, n_sizes, n_shapes):
    """Short verdict. **Body-size spread is the discriminator, not shape count alone.**

    Corrected 2026-09-13, an hour after this file was written, because the first version called
    `ObjectPointerAccessor` NOT A FAMILY: 323 members, **two** body sizes, 323 distinct masked
    images.  Two sizes across 323 bodies is a generated idiom whose members differ by an
    *immediate* - and the docstring says in as many words that this mask cannot see immediates.
    **The verdict line contradicted the caveat directly above it**, which is worse than having no
    verdict, because a reader trusts the one-word answer and never reaches the paragraph.
    """
    if n_shapes == 1:
        return "FAMILY"
    if n_sizes <= SIZE_SPREAD_IS_IDIOM and n_shapes >= 0.5 * max(n, 1):
        return "unproved (immediates)"
    if n_shapes >= 0.5 * max(n, 1):
        return "not a family"
    return "partial"


def verdict_text(n, n_sizes, n_shapes):
    v = verdict(n, n_sizes, n_shapes)
    return {
        "FAMILY": "ONE SHAPE - a generated family. State the shape in the note and declare it.",
        "unproved (immediates)":
            "UNPROVED, NOT DISPROVED - only %d distinct body size(s) over %d members, so these are "
            "one idiom whose members differ by an IMMEDIATE this mask cannot see. Do not declare "
            "on this evidence, and do not conclude they are unrelated either." % (n_sizes, n),
        "not a family":
            "NOT A FAMILY - about one shape per member across %d distinct body sizes. Do not write "
            "one row over this." % n_sizes,
        "partial":
            "PARTIAL - consider splitting by shape, or inspect whether the sub-shapes differ only "
            "by an immediate.",
    }[v]


def frontier(db, sizes):
    a_set, _eo, _ai, _da = cd.measure_a(db, sizes)
    declared = set()
    for doc, parts in cd.parse_families(db):
        if len(parts) >= 5 and parts[1] in cd.LETTERS:
            try:
                declared |= set(cd.read_members(doc, parts[2]))
            except Exception:
                pass
    return set(sizes) - a_set - declared


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--tag", default=None, help="prove one group instead of surveying")
    ap.add_argument("--top", type=int, default=18)
    ap.add_argument("--emit", default=None, help="write the group's members to this path")
    ap.add_argument("--forms", action="store_true",
                    help="compare instruction FORMS (constants dropped) instead of bytes")
    a = ap.parse_args(argv)
    db = a.db or cd.DEFAULT_DB
    d, off = load_image()
    sizes = cd.load_functions()
    rows, idx = fc.load_rows()
    front = frontier(db, sizes)

    def tag(x):
        return (rows[x][idx["tags"]] if x in rows else "") or ""

    key = (lambda x: forms(d, off, x, sizes[x])) if a.forms else           (lambda x: masked(d, off, x, sizes[x]))

    def prove(members):
        szs = collections.Counter(sizes[x] for x in members)
        shapes = collections.Counter()
        for x in members:
            m = key(x)
            if m is not None:
                shapes[m] += 1
        top = shapes.most_common(1)[0][1] if shapes else 0
        return szs, shapes, top

    if a.tag:
        mem = sorted(x for x in front if a.tag in tag(x))
        szs, shapes, top = prove(mem)
        print("%s   [%s]" % (a.tag, "FORMS - constants dropped" if a.forms else "bytes"))
        print("  members %d   distinct sizes %d   distinct shapes %d   largest %.1f%%"
              % (len(mem), len(szs), len(shapes), 100.0 * top / max(len(mem), 1)))
        print("  sizes: %s" % szs.most_common(6))
        print("  %s" % verdict_text(len(mem), len(szs), len(shapes)))
        if a.emit:
            io.open(a.emit, "w", encoding="utf-8", newline="\n").write(
                "".join("%08X\n" % x for x in mem))
            print("  wrote %d members to %s" % (len(mem), a.emit))
        return 0

    groups = collections.Counter()
    for x in front:
        for seg in tag(x).split(";"):
            if seg.startswith("GFZ.V121.CodeDomain."):
                groups[seg] += 1
    print("%-62s %6s %5s %6s %6s  %s" % ("tag group", "n", "sizes", "shapes", "top%", "verdict"))
    print("-" * 104)
    for k, v in groups.most_common(a.top):
        mem = [x for x in front if k in tag(x)]
        szs, shapes, top = prove(mem)
        n = max(len(mem), 1)
        print("%-62s %6d %5d %6d %5.1f%%  %s"
              % (k[20:82], len(mem), len(szs), len(shapes), 100.0 * top / n,
                 verdict(len(mem), len(szs), len(shapes))))
    print()
    print("A shared tag is a shared classification. Only shared bytes are a shared shape.")
    print("'partial' may be immediates this mask cannot see - unproved is not disproved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
