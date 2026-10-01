#!/usr/bin/env python3
"""ext_string_probe.py - does the shipping binary mention a file extension at all?

Purpose, and its single hard limit
----------------------------------
`_index/ASSET-FORMATS.md` assigns an owning subsystem to each shipped format **from where the file
sits in the archive**.  That is a location, not a proof.  This probe supplies a second, independent
signal: whether `FFXII_TZA.exe` contains the extension as a literal string, and what other strings
sit beside it.

**PRESENCE IS EVIDENCE. ABSENCE IS NOT.**  This database already established the point the hard way:
`PClusterHeaderBase` has eighteen recovered field records and **zero** name strings in the image, so
a class can be fully implemented and carry no string at all.  A format whose extension never appears
may still be loaded -- by a name built at run time, by a table of extensions stored as one blob, by
a hash, or by a caller that already holds the full path.

So a hit here is worth following.  A miss here is worth nothing and must never be written down as
*"the engine does not load X"*.

Method
------
ASCII scan for the extension with a leading dot, case-insensitively, as a NUL- or
quote-terminated fragment of a longer printable run.  The surrounding run is printed because
`.sab` inside `sound/%s.sab` is a format-string for a loader and `.sab` inside a help message is
not -- and only the neighbourhood distinguishes them.

Usage
-----
    python ext_string_probe.py --exe Tools/work/exe/FFXII_TZA.exe --census <census.tsv>
    python ext_string_probe.py --exe <exe> --ext sab --ext efx
    python ext_string_probe.py --self-test
"""
import argparse
import io
import os
import re
import sys

PRINTABLE = re.compile(rb"[\x20-\x7e]{4,200}")


def sections(blob):
    """[(name, file_off, raw_size, va)] from the PE headers.

    A file offset is useless to this database -- every address it cites is a canonical virtual
    address with image base 0x00120000 already included.  Reporting raw offsets would produce
    citations that resolve to nothing, which `audit_crossrefs.py` reports as GHOST ADDRESS.
    """
    pe = int.from_bytes(blob[0x3C:0x40], "little")
    if blob[pe:pe + 4] != b"PE\x00\x00":
        return []
    nsec = int.from_bytes(blob[pe + 6:pe + 8], "little")
    opt = int.from_bytes(blob[pe + 20:pe + 22], "little")
    magic = int.from_bytes(blob[pe + 24:pe + 26], "little")
    base = (int.from_bytes(blob[pe + 24 + 24:pe + 24 + 32], "little") if magic == 0x20B
            else int.from_bytes(blob[pe + 24 + 28:pe + 24 + 32], "little"))
    out = []
    t = pe + 24 + opt
    for i in range(nsec):
        e = t + i * 40
        name = blob[e:e + 8].rstrip(b"\x00").decode("ascii", "replace")
        va = int.from_bytes(blob[e + 12:e + 16], "little")
        raw_sz = int.from_bytes(blob[e + 16:e + 20], "little")
        raw_off = int.from_bytes(blob[e + 20:e + 24], "little")
        out.append((name, raw_off, raw_sz, base + va))
    return out


def to_va(secs, off):
    """file offset -> virtual address, or None if it lies outside every section's raw data."""
    for _n, raw_off, raw_sz, va in secs:
        if raw_off <= off < raw_off + raw_sz:
            return va + (off - raw_off)
    return None


def sec_of(secs, off):
    for n, raw_off, raw_sz, _va in secs:
        if raw_off <= off < raw_off + raw_sz:
            return n
    return "?"


def runs(blob):
    """(offset, text) for every printable ASCII run in the image."""
    for m in PRINTABLE.finditer(blob):
        yield m.start(), m.group(0).decode("ascii", "replace")


def probe(blob, exts):
    """ext -> [(offset, containing run)] for runs mentioning `.ext`."""
    want = {e.lower(): re.compile(r"\.%s(?![A-Za-z0-9])" % re.escape(e), re.I) for e in exts}
    hits = {e: [] for e in want}
    for off, text in runs(blob):
        for e, rx in want.items():
            if rx.search(text):
                hits[e].append((off, text))
    return hits


def load_exts(census):
    out = []
    for line in io.open(census, encoding="utf-8", errors="replace"):
        if line.startswith("#") or line.startswith("ext\t") or not line.strip():
            continue
        e = line.split("\t")[0]
        if e != "(none)":
            out.append(e)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe")
    ap.add_argument("--census")
    ap.add_argument("--ext", action="append", default=[])
    ap.add_argument("--max-show", type=int, default=3)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if not a.exe:
        return ap.error("--exe required")

    exts = a.ext or (load_exts(a.census) if a.census else [])
    if not exts:
        return ap.error("--ext or --census required")

    blob = io.open(a.exe, "rb").read()
    secs = sections(blob)
    hits = probe(blob, exts)

    print("EXTENSION STRING PROBE - %s (%d bytes)" % (os.path.basename(a.exe), len(blob)))
    print("PRESENCE IS EVIDENCE; ABSENCE IS NOT. A miss never means 'not loaded'.")
    print("Addresses are canonical VAs (image base already included).\n")
    found = [e for e in exts if hits[e]]
    missing = [e for e in exts if not hits[e]]
    print("  mentioned: %d of %d\n" % (len(found), len(exts)))
    for e in exts:
        if not hits[e]:
            continue
        # A run in `.text` is code bytes that happen to be printable, not a string. `.h` matches
        # `~.H+` and `D$.H` this way -- 36 "hits", none of them a filename. Counted separately so
        # a noisy extension cannot pass itself off as a well-attested one.
        noise = sum(1 for off, _t in hits[e] if sec_of(secs, off) == ".text")
        tag = "" if not noise else "   (%d in .text - code bytes, not strings)" % noise
        print("  .%-8s %d run(s)%s" % (e, len(hits[e]), tag))
        for off, text in hits[e][:a.max_show]:
            va = to_va(secs, off)
            print("      %s [%-7s] %s"
                  % ("%08X" % va if va else "  --  ", sec_of(secs, off), text[:100]))
    if missing:
        print("\n  NO STRING FOUND (says nothing about whether the engine loads them):")
        print("    " + " ".join("." + e for e in missing))
    return 0


SELF = (b"\x00junk\x00sound/%s.sab\x00" + b"\x00" * 8 +
        b"unrelated .sabotage text here\x00" + b"data/%s.EFX\x00")


def self_test():
    h = probe(SELF, ["sab", "efx", "zzz"])
    ok = True
    texts = [t for _o, t in h["sab"]]
    if not any("sound/%s.sab" in t for t in texts):
        print("SELF-TEST FAILED: format-string hit missed"); ok = False
    if any("sabotage" in t for t in texts):
        print("SELF-TEST FAILED: `.sabotage` matched as `.sab`"); ok = False
    if not h["efx"]:
        print("SELF-TEST FAILED: case-insensitive match missed .EFX"); ok = False
    if h["zzz"]:
        print("SELF-TEST FAILED: absent extension reported a hit"); ok = False
    if not ok:
        return 1
    print("self-test ok: `.sabotage` does not match `.sab`, case-insensitive hit found, "
          "absent extension reports nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
