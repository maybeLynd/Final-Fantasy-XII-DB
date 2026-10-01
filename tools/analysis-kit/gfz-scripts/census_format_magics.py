#!/usr/bin/env python3
"""census_format_magics.py - does one extension mean one format?

The weakness this closes
------------------------
`formats_explained` counts EXTENSIONS, and `_index/COVERAGE.md` recorded the obvious objection
against itself before anyone else could raise it:

    `.dat` has 2,948 entries across two different trees -- exactly the shape of several unrelated
    formats sharing a name. If that is what it proves to be, this denominator is wrong in the
    direction that flatters it.

**An extension is a filename convention; a format is a byte layout.** Only the bytes decide, so this
samples real archive entries and groups them by their leading signature.

Method
------
For each extension, take up to `--sample` entries spread evenly across the archive's own ordering
(a deterministic stride, not the first N -- the first N of `ps2data/image` are all one menu folder,
and sampling them would prove only that a folder is homogeneous). Decompress **only the first
block** of each and read its first 16 bytes.

A signature is the leading 4 bytes, printable ASCII where it is printable and hex otherwise.

Reading the result
------------------
    1 signature      the extension names one format. The census row is sound.
    n signatures     either one format with a version/variant field in the first four bytes, or
                     several formats sharing a name. **This script cannot tell those apart** -- it
                     reports the split and the paths, and a human decides. A number of distinct
                     signatures is a lead, never a verdict.

**Sampling caveat, stated because the result is worthless without it:** a format present in 1 % of
an extension's files will usually be missed by a 12-file sample. Absence of a second signature here
is NOT proof that an extension is homogeneous.

Usage
-----
    python census_format_magics.py --vbf "<path>\\FFXII_TZA.vbf" \
        --census Tools/work/formats/archive-extension-census.tsv \
        --out Tools/work/formats/format-magic-census.tsv
    python census_format_magics.py --self-test
"""
import argparse
import collections
import io
import os
import struct
import sys
import zlib

BLOCK = 0x10000


def load_index(f):
    """path -> (start_block, size, offset), plus the block-size table. Mirrors vbfextract.py."""
    magic, header_len = struct.unpack("<4sI", f.read(8))
    if magic != b"SRYK":
        raise ValueError("not a SRYK bigfile: %r" % magic)
    (num,) = struct.unpack("<Q", f.read(8))
    entries_off = 0x10 + num * 16
    f.seek(entries_off)
    raw = f.read(0x20 * num)
    entries = [struct.unpack_from("<IIQQQ", raw, i * 0x20) for i in range(num)]
    strtab_off = entries_off + 0x20 * num
    f.seek(strtab_off)
    (strlen,) = struct.unpack("<I", f.read(4))
    strtab = f.read(strlen)
    f.seek(strtab_off + strlen)
    bl = f.read(header_len - (strtab_off + strlen))
    blocks = struct.unpack("<%dH" % (len(bl) // 2), bl)
    names = collections.OrderedDict()
    for sb, _sb2, size, off, noff in entries:
        end = strtab.index(b"\0", noff)
        names[strtab[noff:end].decode()] = (sb, size, off)
    return names, blocks


def read_head(f, names, blocks, path, want=16):
    """First `want` bytes of an entry, decompressing only its first block."""
    sb, size, off = names[path]
    nblocks = (size + BLOCK - 1) // BLOCK
    csize = blocks[sb] or BLOCK
    expected = BLOCK if nblocks > 1 else size
    f.seek(off)
    data = f.read(csize)
    if csize != expected:
        try:
            data = zlib.decompress(data)
        except zlib.error:
            pass                       # stored raw, or a variant this does not know
    return data[:want]


def signature(head):
    """Leading 4 bytes as ASCII when printable, else hex. Empty entries report EMPTY."""
    if not head:
        return "EMPTY"
    b = head[:4]
    if all(0x20 <= c < 0x7F for c in b) and len(b) == 4:
        return "'%s'" % b.decode("ascii")
    return " ".join("%02X" % c for c in b)


def sample(paths, n):
    """Up to n paths spread evenly across the list, deterministically."""
    if len(paths) <= n:
        return list(paths)
    stride = len(paths) / float(n)
    return [paths[int(i * stride)] for i in range(n)]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--census")
    ap.add_argument("--out")
    ap.add_argument("--sample", type=int, default=12)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if not a.vbf:
        return ap.error("--vbf required")

    f = io.open(a.vbf, "rb")
    names, blocks = load_index(f)
    by_ext = collections.defaultdict(list)
    for p in names:
        n = p.replace("\\", "/").split("/")[-1]
        e = n.rsplit(".", 1)[1].lower() if "." in n else "(none)"
        by_ext[e].append(p)

    rows = []
    print("FORMAT MAGIC CENSUS - %d entries, %d extensions, up to %d samples each"
          % (len(names), len(by_ext), a.sample))
    print("One signature = one format. Several = a lead, not a verdict.\n")
    for ext in sorted(by_ext, key=lambda e: -len(by_ext[e])):
        sigs = collections.Counter()
        example = {}
        for p in sample(by_ext[ext], a.sample):
            try:
                s = signature(read_head(f, names, blocks, p))
            except Exception as exc:
                s = "ERROR:%s" % type(exc).__name__
            sigs[s] += 1
            example.setdefault(s, p)
        flag = "" if len(sigs) == 1 else "   <-- %d signatures" % len(sigs)
        print("  .%-8s %6d files  %s%s"
              % (ext, len(by_ext[ext]), ", ".join("%s x%d" % (s, c) for s, c in sigs.most_common()),
                 flag))
        for s, c in sigs.most_common():
            rows.append((ext, len(by_ext[ext]), s, c, example[s]))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# leading-signature census - census_format_magics.py, sample=%d\n" % a.sample)
            o.write("# One signature per extension supports the `formats_explained` denominator.\n")
            o.write("# Several is a LEAD, not a verdict: it is equally the shape of a version\n")
            o.write("# field in the first four bytes. A human decides, and writes up which.\n")
            o.write("ext\tfiles\tsignature\tin_sample\texample\n")
            for r in rows:
                o.write("%s\t%d\t%s\t%d\t%s\n" % r)
        print("\nwrote %s" % a.out)
    return 0


def self_test():
    ok = True
    if signature(b"EBP2\x00\x00") != "'EBP2'":
        print("SELF-TEST FAILED: printable signature"); ok = False
    if signature(b"\x00\x01\x02\x03") != "00 01 02 03":
        print("SELF-TEST FAILED: hex signature"); ok = False
    if signature(b"") != "EMPTY":
        print("SELF-TEST FAILED: empty entry"); ok = False
    s = sample(list(range(100)), 5)
    if s != [0, 20, 40, 60, 80]:
        print("SELF-TEST FAILED: stride sample %s" % s); ok = False
    if sample([1, 2], 5) != [1, 2]:
        print("SELF-TEST FAILED: short list"); ok = False
    if not ok:
        return 1
    print("self-test ok: printable and hex signatures, empty entry named, sampling strides across "
          "the whole list rather than taking the first N")
    return 0


if __name__ == "__main__":
    sys.exit(main())
