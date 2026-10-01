#!/usr/bin/env python3
"""check_layout_units.py - catch decompiler ARRAY INDICES transcribed as BYTE OFFSETS.

Why this exists
---------------
On 2026-09-02 `class-descriptor-and-metadata-system.md` gave the PClassDescriptor layout with four
intrusive lists at +0x10/+0x12/+0x14/+0x16 and the class name at +0x0C.  Those are qword INDICES.
Ghidra prints `param_1[0x10]` when the variable is `undefined8 *`, and the subscript was transcribed
straight into a layout table.  In bytes the lists are +0x80/+0x90/+0xA0/+0xB0.

A modder using +0x0C as a byte offset reads the wrong memory, so this is not cosmetic.  It is the
same species as a GHOST ADDRESS: a printed reading that is not physically what it claims to be.

The tell is mechanical.  Two fields cannot both be pointers and sit 2 bytes apart.  So: parse the
layout blocks, and flag any field whose declared width does not fit before the next field starts.

What it does NOT do
-------------------
It cannot tell a genuine tight-packed struct from an index table, and it does not try.  Unions,
bitfields, deliberately overlapping views and "the next line is a sub-field of this one" are all
legitimate and all trip it.  Every hit is a QUESTION, not a defect.  It is tuned to be quiet: only
pointer-and-wider types are checked, because those are where the index/offset confusion actually
bites and where a 1-or-2 byte stride is least defensible.

Usage
-----
    python check_layout_units.py --db "Database/FFXII TZA"
    python check_layout_units.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import io
import os
import re
import sys

# "+0x18  ptr  m_worldMatrix   the thing it points at"
FIELD = re.compile(r"^\s*\+0x([0-9A-Fa-f]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s+(\S+)")

# Only types wide enough that a 1-2 byte stride is indefensible.  Narrow types are skipped
# entirely: a u8 next to a u8 is normal and flagging it would bury the real hits.
WIDTH = {
    "ptr": 8, "pointer": 8, "u64": 8, "s64": 8, "i64": 8, "qword": 8, "f64": 8, "double": 8,
    "u32": 4, "s32": 4, "i32": 4, "dword": 4, "f32": 4, "float": 4, "int": 4,
}

# Narrow types are not SUBJECTS of this check (see WIDTH), but a narrow field is exactly what a
# documented view into a packed word looks like, so the overlap exemption below has to be able to
# recognise one. Kept separate so that widening this map can never turn a narrow type into a
# subject. 2026-09-14, OPUS.
NARROW = {"u8": 1, "s8": 1, "i8": 1, "byte": 1, "char": 1, "bool": 1,
          "u16": 2, "s16": 2, "i16": 2, "word": 2}

SELF_TEST = """
```
Bad
  +0x0C  ptr    className
  +0x10  ptr    listA
  +0x12  ptr    listB
```
```
Good
  +0x18  ptr    m_worldMatrix
  +0x20  f32    m_intensity
  +0x24  f32    m_innerRange
```
"""


def scan_text(text, rel, out):
    for block in re.findall(r"```[^\n]*\n(.*?)```", text, re.S):
        fields = []
        for line in block.split("\n"):
            m = FIELD.match(line)
            if m:
                fields.append((int(m.group(1), 16), m.group(2).lower(), m.group(3), line.strip()))
        if len(fields) < 2:
            continue
        # only consider blocks that are monotonically non-decreasing -- a real layout
        if any(fields[i][0] > fields[i + 1][0] for i in range(len(fields) - 1)):
            continue
        for i in range(len(fields) - 1):
            off, ty, name, raw = fields[i]
            nxt = fields[i + 1][0]
            w = WIDTH.get(ty)
            if w is None or w < 4:
                continue
            gap = nxt - off
            if 0 < gap < w:
                # A LINE THAT DECLARES ITS OWN OVERLAP IS NOT A SUSPECT STRIDE.
                #
                # Found 2026-09-08 on `how-a-sound-request-becomes-a-voice.md`, whose line reads
                # `+0x14  u64  = 0xFFFFFFFFFFFFFFFF on reset (covers +0x14 and +0x18)` -- and the
                # document proves it two hundred lines later from the machine code:
                # `48 c7 41 14 ff ff ff ff` is `mov qword [rcx+0x14], -1`, covering +0x14..+0x1B,
                # with the next write a dword at +0x1C. **The document was right, had the bytes,
                # and said so on the line itself.** This checker's own docstring already says
                # deliberately overlapping views are legitimate; it just could not see one being
                # declared.
                if re.search(r"covers\s+\+0x[0-9A-Fa-f]+\s+and\s+\+0x[0-9A-Fa-f]+", raw):
                    continue
                # A PACKED WORD WITH A NARROWER VIEW INSIDE IT IS THE SAME CASE, DECLARED THE
                # OTHER WAY ROUND.
                #
                # Found 2026-09-14 on `the-voice-pack-slots-and-the-voice-verbs.md`, whose cue
                # entry reads `+0x08 u32 bits 0-23 offset of the cue's bank in the pack; bits
                # 24-30 volume (clamped 0..0x7F); bit 31 pending`, and then `+0x0B u8 the volume
                # byte, as the starter reads it (& 0x7F)`. The u8 IS bits 24-30 of that word --
                # the page names the mask on the line -- and the same pattern repeats at `+0x0C`
                # / `+0x0F pan`. The first line enumerates its own bit fields, so a narrower
                # field landing inside it is a documented view rather than an offset transcribed
                # from an array index, which is the thing this check is hunting.
                #
                # Kept tight on purpose: the wider line must ITSELF declare bit positions, and the
                # overlapping field must be STRICTLY NARROWER. Two equal-width fields at the same
                # place, or a wide field with no bit breakdown, still report.
                nxt_w = NARROW.get(fields[i + 1][1], WIDTH.get(fields[i + 1][1]))
                if re.search(r"\bbits?\s+\d+", raw, re.I) and nxt_w is not None and nxt_w < w:
                    continue
                out.append((rel, raw, "declared %s (%d bytes) but next field starts %d byte(s) later"
                            % (ty, w, gap)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        out = []
        scan_text(SELF_TEST, "<self-test>", out)
        # positive control: the Bad block must produce exactly 2 hits, the Good block 0
        if len(out) != 2:
            print("SELF-TEST FAILED: expected 2 hits, got %d" % len(out))
            for o in out:
                print("   ", o)
            return 1
        print("self-test ok: 2 hits on the index-as-offset block, 0 on the real layout")
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    out = []
    for root, _dirs, files in os.walk(a.db):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, a.db)
            scan_text(io.open(p, encoding="utf-8").read(), rel, out)

    if not out:
        print("no suspect layout strides found")
        print("(run --self-test to confirm the check still fires; a clean run from a broken "
              "parser is worthless)")
        return 0

    print("SUSPECT LAYOUT STRIDES - each is a QUESTION, not a defect.")
    print("A field cannot be 8 bytes wide and 2 bytes from its neighbour. Unions and")
    print("overlapping views are legitimate; decompiler ARRAY INDICES transcribed as byte")
    print("offsets are not. Check which one this is.\n")
    for rel, raw, why in out:
        print("  %s\n      %s\n      %s\n" % (rel, raw, why))
    print("%d suspect stride(s)" % len(out))
    return 1


if __name__ == "__main__":
    sys.exit(main())
