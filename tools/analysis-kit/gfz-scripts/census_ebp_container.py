#!/usr/bin/env python3
"""census_ebp_container.py - the EBP2 container header, read across the whole corpus.

What it reads
-------------
    +0x00  u32   magic        'EBP2'
    +0x04  u32   slotCount    0x14 = 20 -- the length of the directory that follows
    +0x08  u32   ?
    +0x0C  u32   ?
    +0x10  u32[slotCount]     section offsets, INDEXED BY SECTION NUMBER, 0 = absent

**The directory is indexed, not packed**, which is the whole reason the section numbering is sparse:
`001`, `005`, `007`, `013`, `015`, `017` and `018` never occur in 1,115 files because their slots are
simply always zero. A packed list would have made those indices unobservable.

Why this exists
---------------
`check_ebp.py` scores `ebp_explained` against a **frozen** population of 13 section types, censused
by unpacking the corpus with an external tool. That denominator has never been re-derived from the
container's own directory. This does it independently, and **disagreement would be a finding about a
scored denominator**, which is the kind of thing that must not be discovered late.

Every invariant printed here is checked over the whole corpus, never over the file that was opened
first -- a format claim without a file count is a guess about one file.

Usage
-----
    python census_ebp_container.py --corpus Tools/work/repos-d2/ebp
    python census_ebp_container.py --corpus <dir> --out Tools/work/formats/ebp-container-census.tsv
    python census_ebp_container.py --self-test
"""
import argparse
import collections
import io
import os
import struct
import sys

MAGIC = b"EBP2"
HDR = 0x10          # the directory begins here


def read_header(blob):
    """-> (slot_count, w2, w3, [offsets]) or None if the magic is wrong."""
    if len(blob) < HDR + 4 or blob[:4] != MAGIC:
        return None
    n, w2, w3 = struct.unpack_from("<III", blob, 4)
    if n == 0 or HDR + 4 * n > len(blob):
        return None
    offs = list(struct.unpack_from("<%dI" % n, blob, HDR))
    return n, w2, w3, offs


def sections(offs, size):
    """-> {index: (offset, length)} for present slots, length from the next present offset."""
    present = sorted((o, i) for i, o in enumerate(offs) if o)
    out = {}
    for k, (o, i) in enumerate(present):
        end = present[k + 1][0] if k + 1 < len(present) else size
        out[i] = (o, end - o)
    return out


def walk(root):
    for dp, _d, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(".ebp"):
                yield os.path.join(dp, f)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.corpus:
        return ap.error("--corpus or --self-test required")

    files = sorted(walk(a.corpus))
    counts = collections.Counter()          # section index -> files containing it
    slot_counts = collections.Counter()
    w2v, w3v = collections.Counter(), collections.Counter()
    first_off = collections.Counter()
    align = collections.Counter()
    sizes = collections.defaultdict(list)
    bad_magic, out_of_order, past_eof = [], [], []
    rows = []

    for p in files:
        blob = io.open(p, "rb").read()
        h = read_header(blob)
        if not h:
            bad_magic.append(p)
            continue
        n, w2, w3, offs = h
        slot_counts[n] += 1
        w2v[w2] += 1
        w3v[w3] += 1
        present = sections(offs, len(blob))
        nz = [o for o in offs if o]
        if nz != sorted(nz):
            out_of_order.append(p)
        if nz and max(nz) > len(blob):
            past_eof.append(p)
        if nz:
            first_off[min(nz)] += 1
        for o in nz:
            align[o % 0x40] += 1
        for i, (o, ln) in present.items():
            counts[i] += 1
            sizes[i].append(ln)
        rows.append((p, n, sorted(present)))

    print("EBP2 CONTAINER CENSUS - %d files under %s" % (len(files), a.corpus))
    if bad_magic:
        print("  !! %d file(s) without an EBP2 magic, e.g. %s" % (len(bad_magic), bad_magic[0]))
    ok = len(files) - len(bad_magic)
    print("  parsed: %d\n" % ok)

    def inv(label, ctr, unit="files"):
        # The denominator differs per row: most invariants are one-per-file, but alignment is
        # one-per-OFFSET. Printing both against the file count read as `5419 / 1114`, which is
        # not a ratio at all -- a denominator has to be named, not assumed.
        top, n = ctr.most_common(1)[0] if ctr else ("-", 0)
        tag = "INVARIANT" if len(ctr) == 1 else "%d values" % len(ctr)
        val = ("0x%X" % top) if isinstance(top, int) else top
        print("  %-28s %-10s %-11s %d / %d %s" % (label, val, tag, n, sum(ctr.values()), unit))

    inv("+0x04 slot count", slot_counts)
    inv("+0x08", w2v)
    inv("+0x0C", w3v)
    inv("first section offset", first_off)
    inv("offset alignment (mod 0x40)", align, "section offsets")
    print("  offsets ascending:           %s"
          % ("yes, all files" if not out_of_order else "NO - %d file(s)" % len(out_of_order)))
    print("  offsets within the file:     %s"
          % ("yes, all files" if not past_eof else "NO - %d file(s)" % len(past_eof)))

    print("\n  section directory - occupancy by slot index:")
    n_slots = max(slot_counts) if slot_counts else 0
    for i in range(n_slots):
        c = counts.get(i, 0)
        if c:
            s = sizes[i]
            print("    slot %02d   %5d files  %5.1f %%   len %d - %d, median %d"
                  % (i, c, 100.0 * c / ok, min(s), max(s), sorted(s)[len(s) // 2]))
        else:
            print("    slot %02d   %5d files            -- never present --" % (i, c))

    # Cross-check against the frozen scored denominator.
    try:
        import check_ebp
        frozen = {int(s): v for s, v in check_ebp.CENSUS.items()}
        print("\n  CROSS-CHECK against check_ebp.py's frozen population (%d scripts):"
              % check_ebp.CORPUS_SIZE)
        drift = 0
        for i in sorted(set(frozen) | set(counts)):
            f, now = frozen.get(i), counts.get(i)
            if f != now:
                drift += 1
                print("    slot %02d  frozen %-6s  directory %-6s   <-- DISAGREES" % (i, f, now))
        if drift:
            print("    %d slot(s) disagree. A scored denominator that moved is a FINDING to write"
                  " up,\n    not a number to quietly change." % drift)
        else:
            print("    all %d section slots agree exactly. The frozen denominator is confirmed by"
                  "\n    a second, independent reading - the container's own directory." % len(frozen))
    except Exception as exc:
        print("  (cross-check unavailable: %s)" % exc)

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# EBP2 container census - census_ebp_container.py over %d files\n" % ok)
            o.write("file\tslots\tpresent\n")
            for p, n, pres in rows:
                o.write("%s\t%d\t%s\n" % (p.replace(os.sep, "/"), n,
                                          ",".join("%03d" % i for i in pres)))
        print("\nwrote %s" % a.out)
    return 0


def self_test():
    hdr = MAGIC + struct.pack("<III", 4, 0, 0) + struct.pack("<4I", 0x80, 0, 0x100, 0)
    body = hdr + b"\x00" * (0x200 - len(hdr))
    h = read_header(body)
    ok = True
    if not h or h[0] != 4 or h[3] != [0x80, 0, 0x100, 0]:
        print("SELF-TEST FAILED: header %s" % (h,)); ok = False
    s = sections(h[3], len(body))
    if sorted(s) != [0, 2]:
        print("SELF-TEST FAILED: present %s" % sorted(s)); ok = False
    if s[0] != (0x80, 0x80) or s[2] != (0x100, 0x100):
        print("SELF-TEST FAILED: lengths %s" % s); ok = False
    if read_header(b"XXXX" + body[4:]) is not None:
        print("SELF-TEST FAILED: bad magic accepted"); ok = False
    if read_header(MAGIC + struct.pack("<III", 999999, 0, 0)) is not None:
        print("SELF-TEST FAILED: directory longer than the file accepted"); ok = False
    if not ok:
        return 1
    print("self-test ok: indexed directory parsed, zero slots read as absent, lengths derived from "
          "the next present offset, bad magic and an oversized directory both refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
