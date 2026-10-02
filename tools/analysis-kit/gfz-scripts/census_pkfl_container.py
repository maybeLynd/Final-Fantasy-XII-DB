#!/usr/bin/env python3
"""census_pkfl_container.py - the PKFL package directory, over all 10,314 shipped files.

Why this exists
---------------
`PKFL` is the second EBP and slightly larger: **10,314 files** against EBP's 10,045, and like EBP it
is **one container wearing four extensions** -- `.mot`, `.snd`, `.vpc`, `.vpcjp`. A 160-file sample
found 160/160 carrying the magic, two directory sizes (16 and 64 slots) and 28 occupied indices.

**A sample is not a denominator.** EBP's 14 units are trustworthy for exactly one reason: they were
censused over the whole corpus before anyone wrote a sheet, and a second independent route
reproduced them. This does the same for PKFL so that `26-PKFL-Package-Container` can be scored
without inventing its population.

What it refuses to do
---------------------
**It decides nothing about what a slot HOLDS.** Occupancy, sizes and co-occurrence only. The
temptation with `.mot` is to read slot meanings off the extension -- and the extension is exactly
what the magic census already proved unreliable, since one layout ships under four of them.

A structural warning carried from the sample: **EBP's directory is sparse and PKFL's is dense.**
EBP's seven permanently-zero slots are *how* its census learned they existed; if PKFL indices are
all occupied, **absence carries no information here** and occupancy frequency has to do the work.

Usage
-----
    python census_pkfl_container.py --vbf "<...>\\FFXII_TZA.vbf" \
        --out Tools/work/formats/pkfl-container-census.tsv
    python census_pkfl_container.py --self-test
"""
import argparse
import collections
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))
MAGIC = b"PKFL"
EXTS = ("mot", "snd", "vpc", "vpcjp")


def read_dir(blob):
    """-> (slotCount, [(offset, size)]) or None. Directory begins at +0x08, after magic and count.

    Corrected 2026-10-02 (OPUS, opus-pkfl-readiness-fixes-1002): each slot is a {u32 offset, u32 size} PAIR, so the
    directory is 8 + 8 * slotCount bytes (0x88 for 16 slots, 0x208 for 64 - the sizes the walker 0032FCA0 requests).
    This used to read slotCount single dwords, i.e. the first half of the directory with every size taken for an
    offset. The engine reads slot k's offset at +8+8k and its size at +0xC+8k (0032F360+0x2E). Over all 10,314
    shipped packages the pair reading has no lone zero, every pair in bounds, offsets ascending in slot order and the
    first payload at 0x800.
    """
    if len(blob) < 12 or blob[:4] != MAGIC:
        return None
    n = struct.unpack_from("<I", blob, 4)[0]
    if not (1 <= n <= 4096) or 8 + 8 * n > len(blob):
        return None
    w = struct.unpack_from("<%dI" % (2 * n), blob, 8)
    return n, [(w[2 * k], w[2 * k + 1]) for k in range(n)]


def slots(pairs, size=None):
    """{index: (offset, size)} for present slots (offset or size non-zero). Lengths are stored, not inferred.

    *Withdrawn 2026-10-02 (OPUS): the text below described the four-byte reading. Its "aliasing" - odd slots
    pointing inside the directory, the repeated 0x40 - was the size words read as offsets. It is kept as history.*

    **LENGTH IS None WHEN SLOTS SHARE AN OFFSET, and that is the whole point of this function.**

    The first version returned `next_offset - offset` unconditionally. In PKFL **slots alias**:
    2,349 of 10,314 files have two or more slots pointing at the same place, and 2,385 of 2,403
    duplicate groups are entirely odd slots pointing *inside the directory itself* -- a canonical
    "this half is empty" marker, cheaper than a null.

    Under the old arithmetic an aliased slot got a length of **0**, and the last alias in a group
    got a spurious ~1,984 bytes spanning the gap to the first real payload. **Neither is a payload
    size.** The category README read those zeros as "the odd slot is a small companion", inferred a
    DAT/CTL mechanism from them, and proposed a 14-pair scored denominator on that basis. All of it
    rested on this arithmetic.

    **A census that emits a plausible number for a case it cannot measure is worse than one that
    refuses**, because the number gets read. So an aliased slot reports `None`.
    """
    return {i: (o, s) for i, (o, s) in enumerate(pairs) if o or s}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int, default=0, help="0 = the whole corpus")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.vbf:
        return ap.error("--vbf or --self-test required")

    import vbfextract as V
    f = io.open(a.vbf, "rb")
    names, blocks = V.load_index(f)
    want = [p for p in names if p.rsplit(".", 1)[-1].lower() in EXTS]
    if a.limit:
        want = want[::max(1, len(want) // a.limit)][:a.limit]

    occ = collections.Counter()
    slot_sizes = collections.defaultdict(list)
    counts = collections.Counter()
    by_ext_count = collections.defaultdict(collections.Counter)
    bad, rows = [], []
    aliased = collections.Counter()
    for p in want:
        try:
            b = V.read_entry(f, names, blocks, p)
        except Exception:
            continue
        d = read_dir(b)
        ext = p.rsplit(".", 1)[-1].lower()
        if not d:
            bad.append(p)
            continue
        n, offs = d
        counts[n] += 1
        by_ext_count[ext][n] += 1
        s = slots(offs)
        for i, (_o, ln) in s.items():
            occ[i] += 1
            slot_sizes[i].append(ln)
        rows.append((p, ext, n, ",".join("%02d" % i for i in sorted(s))))

    ok = len(rows)
    print("PKFL PACKAGE CENSUS - %d files read, %d parsed, %d without a PKFL directory"
          % (len(want), ok, len(bad)))
    print("  slot-count values: %s" % dict(counts))
    print("  by extension     : %s" % {e: dict(c) for e, c in by_ext_count.items()})
    print("")
    hi = max(occ) if occ else -1
    print("  slot occupancy over %d files (max index %d):" % (ok, hi))
    for i in range(hi + 1):
        c = occ.get(i, 0)
        if c:
            sz = slot_sizes[i]
            al = aliased.get(i, 0)
            tag = "" if not al else "   %d ALIASED (length unmeasurable)" % al
            if sz:
                print("    slot %02d  %6d  %5.1f %%   len %d - %d, median %d%s"
                      % (i, c, 100.0 * c / ok, min(sz), max(sz), sorted(sz)[len(sz) // 2], tag))
            else:
                print("    slot %02d  %6d  %5.1f %%   ALL %d occurrences aliased - NO LENGTH"
                      % (i, c, 100.0 * c / ok, al))
        else:
            print("    slot %02d  %6d          -- never present --" % (i, c))
    # BUG FIXED 2026-09-04: this used to range only to the highest OCCUPIED index and then
    # announce "0 never present -- a DENSE directory". That conclusion was false and produced by
    # construction: a range that stops at the last occupied slot cannot contain an empty one.
    # The directory declares its own size, so the range must come from slotCount.
    # In fact the 64-slot variant never uses anything above index 27 -- 36 permanently-zero slots,
    # exactly the EBP-style sparseness the summary had just denied.
    biggest = max(counts) if counts else 0
    empty = [i for i in range(biggest) if not occ.get(i)]
    print("")
    print("  **%d occupied indices out of a declared %d**; %d never present"
          % (len(occ), biggest, len(empty)))
    if empty:
        print("  Never present: %s%s"
              % (empty[:12], " ... (%d more)" % (len(empty) - 12) if len(empty) > 12 else ""))
        print("  Sparse, like EBP: the always-zero slots are how the population is BOUNDED.")

    pairs = sum(1 for i in occ if i % 2 == 0 and occ.get(i) == occ.get(i + 1))
    print("  even/odd slots with identical occupancy: %d pair(s)" % pairs)

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# PKFL package census - census_pkfl_container.py over %d files\n" % ok)
            o.write("# Occupancy only. Nothing here says what a slot HOLDS.\n")
            o.write("path\text\tslotCount\tpresent\n")
            for r in rows:
                o.write("%s\t%s\t%d\t%s\n" % r)
        print("\nwrote %s" % a.out)
    return 0


def self_test():
    body = MAGIC + struct.pack("<I", 4) + struct.pack("<8I", 0x800, 0x40, 0, 0, 0x1000, 0x30, 0, 0)
    body += b"\x00" * (0x100 - len(body))
    d = read_dir(body)
    ok = True
    if not d or d[0] != 4 or d[1] != [(0x800, 0x40), (0, 0), (0x1000, 0x30), (0, 0)]:
        print("SELF-TEST FAILED: dir %s" % (d,)); ok = False
    s = slots(d[1])
    if sorted(s) != [0, 2] or s[0] != (0x800, 0x40) or s[2] != (0x1000, 0x30):
        print("SELF-TEST FAILED: slots %s" % s); ok = False
    if read_dir(MAGIC + struct.pack("<I", 4) + b"\x00" * 16) is not None:
        print("SELF-TEST FAILED: a directory shorter than 8 + 8 * count accepted"); ok = False
    if read_dir(b"XXXX" + body[4:]) is not None:
        print("SELF-TEST FAILED: bad magic accepted"); ok = False
    if read_dir(MAGIC + struct.pack("<I", 99999)) is not None:
        print("SELF-TEST FAILED: oversized directory accepted"); ok = False
    if not ok:
        return 1
    print("self-test ok: {offset, size} pairs parsed at +0x08, zero pairs read as absent, sizes as stored, "
          "short directory, bad magic and oversized count refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
