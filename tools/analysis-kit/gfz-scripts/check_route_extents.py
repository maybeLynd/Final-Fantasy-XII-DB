#!/usr/bin/env python3
"""check_route_extents.py - does a declared `count=` match where the data actually stops?

`check_route_counts.py` compares a route's count with the numbers in its document. That catches a
route whose prose disagrees, and it cannot catch a route whose prose agrees and is also wrong.
**This asks the image instead.**

The idea is the one that settled the dispatch table: an authored table of records looks like records
for `count` elements and then stops looking like them. So for
`ARRAY 0xADDR stride=0xS count=N` the elements `[0, N)` are scored for record-likeness and compared
against the `N` elements that follow. Three outcomes, and only the third is a finding:

    the band after the table is empty or unlike it   the count is CORROBORATED
    the table itself scores near zero               nothing to compare; reported as UNINFORMATIVE
    the band after scores like the table            the count may be SHORT - read it

SCORE. Per element, the fraction of its qword slots that are non-zero, plus the fraction that land
in `.text` (a callback table) or in a data section (a pointer table). Authored record tables in this
image are overwhelmingly one of those; a table of small integers scores low on all three and is
reported uninformative rather than judged, because a low score there says nothing.

**NO VERDICT IS ISSUED.** Every automated verdict this kit has attempted on a shape rather than a
reading has over-reported - 90, 56, 39, 16, 1461 - and the two `count=` defects found so far went in
opposite directions, one with the prose right and one with the column right. This prints the two
scores and the reader decides.

    python check_route_extents.py
"""
import argparse
import csv
import io
import os
import re
import struct
import sys

import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was a path relative to the CURRENT DIRECTORY, so the check only
# ran when invoked from inside gfz-scripts and raised FileNotFoundError everywhere else - a gate
# that crashes reports nothing, which is worse than a gate that reports a defect. Anchored on
# kit_paths, which is already imported above, the same way disasm_fn.py resolves the image.
EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
R_ARRAY = re.compile(r"^(ARRAY)\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s+"
                     r"stride=(0x[0-9A-Fa-f]+|\d+)\s+count=(\d+)")


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
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    secs = sections(raw)
    tva, tvs = [(v, vs) for n, v, vs, rs, pr in secs if n == ".text"][0]

    def fo(va):
        for n, v, vs, rs, pr in secs:
            if v <= va < v + vs:
                o = pr + (va - v)
                # past the section's RAW data is .bss - reads as zero, not file content
                return o if (va - v) < rs else None
        return None

    def is_data(x):
        for n, v, vs, rs, pr in secs:
            if n in (".data", ".rdata") and v <= x < v + vs:
                return True
        return False

    def score(addr, stride, n):
        """(nonzero, text-ptr, data-ptr) fractions over n elements of `stride` bytes."""
        nz = tp = dp = tot = 0
        for i in range(n):
            o = fo(addr + i * stride)
            if o is None or o + stride > len(raw):
                continue
            for k in range(stride // 8):
                v = struct.unpack_from("<Q", raw, o + k * 8)[0]
                tot += 1
                if v:
                    nz += 1
                if tva <= v < tva + tvs:
                    tp += 1
                elif is_data(v):
                    dp += 1
        if not tot:
            return None
        return (nz / tot, tp / tot, dp / tot, tot)

    rows = []
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            for alt in f[12].split("|"):
                m = R_ARRAY.match(alt.strip())
                if m:
                    lo = int(m.group(2), 0) + (int(m.group(3), 0) if m.group(3) else 0)
                    rows.append((f[0], lo, int(m.group(4), 0), int(m.group(5))))

    print("ARRAY routes with a numeric count and stride: %d" % len(rows))
    print()
    print("  %-30s %-10s %-7s %-6s  %-22s %-22s" % (
        "type", "base", "stride", "count", "inside (nz/text/data)", "after  (nz/text/data)"))
    short, corro, uninf = [], [], []
    for t, lo, stride, n in sorted(rows):
        if stride % 8:
            uninf.append((t, "stride not a qword multiple"))
            continue
        a_in = score(lo, stride, n)
        a_out = score(lo + n * stride, stride, min(n, 32))
        if not a_in or not a_out:
            uninf.append((t, "outside the file image (.bss or unmapped)"))
            continue
        fmt = lambda s: "%.2f/%.2f/%.2f" % (s[0], s[1], s[2])
        flag = ""
        # THE CATEGORIES MUST BE COMPARED SEPARATELY. The first version summed the text and data
        # pointer fractions, so `ScriptNativeDispatchRecord` -- a CALLBACK table (0.29 text, 0.00
        # data) followed by a region of DATA pointers (0.00 text, 0.39 data) -- scored as "the band
        # after looks like the table". It is the opposite: zero text pointers after 1,496 records
        # of them is the table ending exactly where the count says. Summing let a different kind of
        # table impersonate a continuation, and flagged 4 of 4 scorable rows with 0 corroborated.
        if a_in[1] >= 0.05:
            kindname, inside_f, after_f = "text", a_in[1], a_out[1]
        elif a_in[2] >= 0.05:
            kindname, inside_f, after_f = "data", a_in[2], a_out[2]
        else:
            uninf.append((t, "no pointer slots in the table - non-zero alone cannot discriminate"))
            print("  %-30s %08X   0x%-5X %-6d  %-22s %-22s  (uninformative)"
                  % (t[:30], lo, stride, n, fmt(a_in), fmt(a_out)))
            continue
        if after_f >= inside_f * 0.6:
            short.append((t, kindname, inside_f, after_f))
            flag = "  <-- band AFTER carries %s pointers too (%.2f vs %.2f): read it" % (
                kindname, after_f, inside_f)
        else:
            corro.append((t, kindname, inside_f, after_f))
            flag = "  ok: %s pointers stop (%.2f -> %.2f)" % (kindname, inside_f, after_f)
        print("  %-30s %08X   0x%-5X %-6d  %-22s %-22s%s"
              % (t[:30], lo, stride, n, fmt(a_in), fmt(a_out), flag))
    print()
    print("corroborated (the pointers stop where the count says) : %d" % len(corro))
    for x in corro:
        print("    %-30s %s %.2f -> %.2f" % (x[0][:30], x[1], x[2], x[3]))
    print("uninformative (nothing to score)               : %d" % len(uninf))
    for t, why in uninf:
        print("    %-30s %s" % (t[:30], why))
    print("worth reading (band after resembles the table) : %d" % len(short))
    for x in short:
        print("    %-30s %s %.2f -> %.2f" % (x[0][:30], x[1], x[2], x[3]))
    print()
    print("NO VERDICT IS ISSUED. A table can legitimately be followed by another of the same shape,")
    print("and a count can legitimately name a populated subset. These are two measurements.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
