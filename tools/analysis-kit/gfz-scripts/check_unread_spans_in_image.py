#!/usr/bin/env python3
"""check_unread_spans_in_image.py - a span the store calls unread, with content in the image.

`ItemClassDescriptor +0x40` was a sixteen-byte span recorded as *"declared gap span ... no censused
access"*. Half of it holds a per-class **function pointer** in 12 of its 15 records. Nothing had
looked, because "unread" is a statement about ACCESSES and this is a question about BYTES: for a
type whose storage is initialised data in the shipped image, the content of an unread span can
simply be read.

**`unread` means nobody has been seen to touch it. It does not mean empty, and where the storage is
authored it does not even mean unknown.** A span holding a `.text` pointer in most of its records is
a function-pointer field whatever the access census says.

SCOPE, and it is narrow on purpose. Only types whose route puts their bytes inside a section's RAW
data are eligible - `STATIC` and `ARRAY`. A `.bss` address is past the raw data and reads as zero,
so a zero there is the file telling us nothing, and `PTR`/`PARRAY` reach storage that is allocated
or relocated at runtime. Ineligible types are counted, not judged.

WHAT IT REPORTS, per unread span:
    ptr   qword slots inside the span that land in `.text`   -> a function pointer field
    data  qword slots that land in `.data`/`.rdata`          -> a pointer field
    nz    slots that are merely non-zero                     -> content of some kind

**No verdict.** A non-zero span may be padding the compiler filled, an inline array, or a field.
Only the `.text` column is close to self-interpreting, and even that is reported with its count.

    python check_unread_spans_in_image.py
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys

import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
R_STATIC = re.compile(r"^STATIC\s+(0x[0-9A-Fa-f]+)")
R_ARRAY = re.compile(r"^ARRAY\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s+"
                     r"stride=(0x[0-9A-Fa-f]+|\d+)\s+count=(\d+)")
UNREAD = re.compile(r"^(unobserved|unknown|unread|pad)", re.I)


def sections(raw):
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    base = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    out, off = [], pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        out.append((nm, base + va, vs, rs, pr))
        off += 40
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default=os.path.join(KP.DB, "_types", "types.tsv"))
    ap.add_argument("--fields", default=os.path.join(KP.DB, "_types", "fields.tsv"))
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    secs = sections(raw)
    tva, tvs = [(v, vs) for n, v, vs, rs, pr in secs if n == ".text"][0]

    def fo(va):
        for n, v, vs, rs, pr in secs:
            if v <= va < v + vs:
                return pr + (va - v) if (va - v) < rs else None
        return None

    def is_data(x):
        return any(n in (".data", ".rdata") and v <= x < v + vs
                   for n, v, vs, rs, pr in secs)

    anchors, ineligible = {}, []
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            got = None
            for alt in f[12].split("|"):
                alt = alt.strip()
                m = R_STATIC.match(alt)
                if m:
                    got = (int(m.group(1), 0), None, 1)
                    break
                m = R_ARRAY.match(alt)
                if m:
                    got = (int(m.group(1), 0) + (int(m.group(2), 0) if m.group(2) else 0),
                           int(m.group(3), 0), int(m.group(4)))
                    break
            if got and fo(got[0]) is not None:
                anchors[f[0]] = got
            elif f[12].strip():
                ineligible.append(f[0])

    fields = collections.defaultdict(list)
    with io.open(a.fields, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9 or not f[0]:
                continue
            try:
                fields[f[0]].append((int(f[1], 0), int(f[2], 0), f[3], f[5]))
            except ValueError:
                pass

    print("types with bytes in the shipped image (STATIC/ARRAY, inside raw data): %d" % len(anchors))
    print("types whose route reaches runtime storage (.bss / PTR / PARRAY / ...): %d" % len(ineligible))
    print()
    hits = []
    spans = 0
    for tname, (base, stride, count) in sorted(anchors.items()):
        for off, size, name, meaning in sorted(fields.get(tname, [])):
            if not UNREAD.match(name or ""):
                continue
            spans += 1
            ptr = dat = nz = tot = 0
            for i in range(count):
                a0 = base + i * (stride or 0) + off
                o = fo(a0)
                if o is None:
                    continue
                for k in range(size // 8):
                    v = struct.unpack_from("<Q", raw, o + k * 8)[0]
                    tot += 1
                    if v:
                        nz += 1
                    if tva <= v < tva + tvs:
                        ptr += 1
                    elif is_data(v):
                        dat += 1
            if tot and (ptr or dat or nz):
                hits.append((tname, off, size, name, ptr, dat, nz, tot, count))

    print("unread spans examined : %d" % spans)
    print("spans with ANY content in the image : %d" % len(hits))
    print()
    print("  %-30s %-8s %-5s %-22s %5s %5s %5s %6s" % (
        "type", "offset", "size", "name", "ptr", "data", "nz", "slots"))
    for t, off, size, name, ptr, dat, nz, tot, cnt in sorted(hits, key=lambda x: (-x[4], -x[6])):
        mark = "  <-- .text pointers" if ptr else ""
        print("  %-30s %-8s %-5d %-22s %5d %5d %5d %6d%s"
              % (t[:30], hex(off), size, name[:22], ptr, dat, nz, tot, mark))
    print()
    print("`ptr` is the column that interprets itself: a span holding a .text pointer is a function")
    print("pointer field whatever the access census says. `nz` alone is not a finding - it can be")
    print("compiler padding, an inline array, or a field - and is printed to be read, not counted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
