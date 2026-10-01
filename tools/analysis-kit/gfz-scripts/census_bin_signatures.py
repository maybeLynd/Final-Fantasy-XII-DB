#!/usr/bin/env python3
"""census_bin_signatures.py - how many formats actually share the `.bin` extension?

The weakness this closes
------------------------
`formats_explained` scores `bin` as ONE row standing for 1,439 archive entries. The magic census
(`census_format_magics.py`, sample=12) already found `sloc`, `st2e`, `FLAG`, `gmap`, `CCdd`, `hctg`
and a bare dword in twelve samples, which makes `bin` a row that **cannot be closed by one sheet**.
Before anyone writes a sheet, the split has to be measured over the whole population.

Two things this does that a naive signature count does not
---------------------------------------------------------
1. **It reports a logical-unit count as well as a file count.** `.bin` ships per locale. The `.ard`
   census already found the same shape (332 files / 166 areas, byte-identical copies) and the
   README records that "the file count double-counts". A denominator that inherits the duplication
   flatters itself, so this keys by the path with locale segments removed and *proves* the
   duplication by content hash rather than assuming it.

2. **The signature discriminator has five verdicts, not two.** `MAGIC`, `MAGIC_TAG_VERSION`,
   `EBP_SECTION_BODY`, `NOT_A_MAGIC` and `UNDETERMINED`. Many `.bin` files begin with content, not a tag - `face_guest10.bin` starts
   `d1 d1 f4 f4` - and a two-valued classifier would silently report those as 30-odd extra
   "formats". EVIDENCE-STANDARD.md: *a discriminator must be able to return "I don't know"*, and
   the size of the UNDETERMINED bucket is a reported result, not a failure.

Method
------
Read only the FIRST archive block of each entry (64 KB decompressed), which is enough for a
signature and for a content hash, and never decompresses a 11 MB file to look at four bytes.

For an entry whose whole payload fits in that first block, the hash is the hash of the complete
file and byte-identity between copies is PROVEN. For a larger entry the hash covers the first
64 KB only, and the two populations are counted separately and reported separately - a partial
check reported as a partial check.

Positive control
----------------
EVIDENCE-STANDARD.md requires one on any absence claim. `--self-test` asserts the classifier
returns MAGIC for a known-present tag (`st2e`), NOT_A_MAGIC for known binary content, and
UNDETERMINED for the ambiguous shapes - so a run that reports "no file has signature X" is
distinguishable from a run where the classifier never fired.

Usage
-----
    python census_bin_signatures.py --vbf <archive> --out <tsv>
    python census_bin_signatures.py --self-test
"""
import argparse
import collections
import hashlib
import io
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))

BLOCK = 0x10000

# Locale segments, derived from the archive's own path vocabulary rather than assumed.
# Verified against the .bin tree 2026-09-04: every one of these appears as a whole path segment
# at more than one depth, and no other segment does.
LOCALES = {"us", "jp", "cn", "kr", "ch", "in", "de", "es", "fr", "it", "gb"}

# A tag is ASCII letters/digits, the alphabet every confirmed magic in this archive uses
# (`st2e`, `sloc`, `gmap`, `FLAG`, `CCdd`, `hctg`, `QST1`, `NPC0`, `FF12`, `EBP2`, `SHK1`).
def _tagish(b):
    return all((48 <= c <= 57) or (65 <= c <= 90) or (97 <= c <= 122) for c in b)


def _byte_doubled(blob, n=32):
    """Every byte repeated: D1 D1 F4 F4 F0 F0 ... - a 16-bit-expanded palette or image row.

    Written against the actual bytes of face_guest10.bin, NOT guessed. The first draft of this
    test asked whether the two 16-bit halves of the leading dword were equal, which is a
    different property and which `--self-test` rejected before it reached a result.
    """
    w = blob[:n]
    if len(w) < 8 or len(w) % 2:
        return False
    return w[0::2] == w[1::2]


def _repeating_unit(blob, n=16):
    """The first n bytes are one 2- or 4-byte unit repeated: 94 03 94 03 94 03 ..."""
    w = blob[:n]
    if len(w) < n:
        return 0
    for u in (2, 4):
        if w == w[:u] * (n // u):
            return u
    return 0


EBP_SECTION_MARKER = 0x8000000B


def classify(sig4, blob, size=None):
    """Five verdicts. Returns (verdict, reason).

    MAGIC             - four ASCII tag bytes at offset 0.
    MAGIC_TAG_VERSION - three ASCII letters plus a small version byte (`NAV\\x02`, `MRF\\x02`).
    EBP_SECTION_BODY  - not a `.bin` format at all: a bare EBP `section_000` bytecode body
                        wearing a `.bin` name. Requires BOTH the 0x8000000B section marker AND
                        `+0x04` equal to the whole file size, so the marker alone cannot carry it.
    NOT_A_MAGIC       - POSITIVELY disqualified by a named structural property, never by "it
                        doesn't look like a tag to me".
    UNDETERMINED      - no test fires either way. Counted and reported; never silently folded
                        into either side, because that is how 30 palettes become 30 "formats".

    The two positive-identification verdicts were added AFTER the first run, by reading the
    UNDETERMINED bucket. That is what the bucket is for: it shrank from 15 units to 9, and
    every unit that left it did so by being identified, not by being reclassified as noise.
    """
    # Byte-doubling is tested BEFORE the ASCII test, and the order is load-bearing.
    # face_guest08.bin begins 43 43 64 64 6C 6C 5C 5C ... - byte-doubled image data whose first
    # four bytes happen to spell "CCdd". Tested ASCII-first it was reported as a 28th format.
    # This is exactly the false positive the noise floor predicted (~0.8 expected over 236
    # units) and it was found by going to look for it. Doubling over a 32-byte window is a far
    # stronger structural signal than four ASCII bytes, and no confirmed magic in this archive
    # is byte-doubled.
    if _byte_doubled(blob):
        return "NOT_A_MAGIC", "every byte doubled over the first 32 (expanded image/palette)"
    if _tagish(sig4):
        return "MAGIC", "four ASCII tag bytes"
    v = struct.unpack("<I", sig4)[0]
    if v == EBP_SECTION_MARKER and size is not None and len(blob) >= 8:
        if struct.unpack_from("<I", blob, 4)[0] == size:
            return ("EBP_SECTION_BODY",
                    "0x8000000B section marker and +0x04 == whole file size")
    if _tagish(sig4[:3]) and sig4[3] < 0x20:
        return "MAGIC_TAG_VERSION", "three ASCII tag bytes plus version byte %d" % sig4[3]
    u = _repeating_unit(blob)
    if u:
        return "NOT_A_MAGIC", "first 16 bytes are one %d-byte unit repeated" % u
    if v == 0:
        return "NOT_A_MAGIC", "leading dword is zero"
    if v < 0x10000 and len(blob) >= 8:
        # a small leading integer is a count or a first-entry offset, not a tag
        return "NOT_A_MAGIC", "leading dword is a small integer (%d)" % v
    return "UNDETERMINED", "non-ASCII, not positively disqualified"


def read_first_block(f, names, blocks, path):
    """(prefix_bytes, declared_size, is_whole_file). Decompresses one block, never the file."""
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
            pass
    return data, size, nblocks == 1


def logical_unit(path):
    """Path with locale segments removed - the unit a sheet actually has to explain."""
    return "/".join(s for s in path.split("/") if s not in LOCALES)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--out")
    ap.add_argument("--ext", default=".bin")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.vbf:
        return ap.error("--vbf or --self-test required")

    import vbfextract as V
    f = io.open(a.vbf, "rb")
    names, blocks = V.load_index(f)
    paths = sorted(n for n in names if n.lower().endswith(a.ext))

    rows = []
    for p in paths:
        blob, size, whole = read_first_block(f, names, blocks, p)
        sig = bytes(blob[:4]) if len(blob) >= 4 else bytes(blob).ljust(4, b"\0")
        verdict, reason = classify(sig, blob, size)
        rows.append({
            "path": p, "unit": logical_unit(p), "size": size,
            "sig_hex": sig.hex(),
            # printed in full, never through a fixed-width field: a census that prints an
            # identifier must not truncate it.
            "sig_ascii": "".join(chr(c) if 32 <= c < 127 else "." for c in sig),
            "verdict": verdict, "reason": reason,
            "hash": hashlib.sha256(blob).hexdigest(),
            "hash_covers": "whole-file" if whole else "first-64KB",
        })

    print("`%s` SIGNATURE CENSUS - %d archive entries" % (a.ext, len(rows)))

    units = collections.defaultdict(list)
    for r in rows:
        units[r["unit"]].append(r)
    print("  logical units after removing locale segments: %d" % len(units))
    print("  copies per unit: %s"
          % dict(sorted(collections.Counter(len(v) for v in units.values()).items())))

    ident = same = diff = 0
    partial = 0
    for u, rs in units.items():
        if len(rs) < 2:
            continue
        same += 1
        keys = {(r["size"], r["hash"]) for r in rs}
        if len(keys) == 1:
            ident += 1
            if any(r["hash_covers"] != "whole-file" for r in rs):
                partial += 1
        else:
            diff += 1
    print("  multi-copy units: %d, of which copies agree: %d, differ: %d" % (same, ident, diff))
    print("    (%d of the %d agreements are first-64KB only, not whole-file)" % (partial, ident))

    ver = collections.Counter(r["verdict"] for r in rows)
    print("\n  verdicts over files: %s" % dict(ver))
    # A unit whose locale copies disagreed about their verdict would make "verdicts over units"
    # meaningless, so the count is reported rather than assumed to be zero.
    mixed = [u for u, rs in units.items() if len({r["verdict"] for r in rs}) > 1]
    uver = collections.Counter(rs[0]["verdict"] for rs in units.values())
    print("  verdicts over units: %s" % dict(uver))
    print("  units whose copies disagree about the verdict: %d%s"
          % (len(mixed), (" -- " + ", ".join(mixed[:3])) if mixed else " (so the above is well-defined)"))

    # VERDICT AGREEMENT IS THE COARSER QUESTION AND IT HIDES THE FINER ONE. `hdat` and `himg`
    # are both MAGIC, so a unit split between them agrees on the verdict and disagrees on the
    # FORMAT, and the line above reports zero. Measured 2026-09-19 (OPUS): seven `.dat` units
    # are exactly that - menuhandbook_monster004..010, hdat in some locales and himg in others.
    # Their per-magic attribution is therefore a range, not a point, so it is printed here
    # instead of being absorbed silently into whichever copy is enumerated first.
    sigsplit = [(u, sorted({r["sig_ascii"] for r in rs}))
                for u, rs in units.items() if len({r["sig_hex"] for r in rs}) > 1]
    print("  units whose copies carry DIFFERENT SIGNATURES: %d%s"
          % (len(sigsplit), "" if not sigsplit else
             " -- the magic counts below are ambiguous for these"))
    for u, ss in sigsplit[:6]:
        print("      %-58s %s" % (u[-58:], "/".join(ss)))
    if len(sigsplit) > 6:
        print("      ... %d more" % (len(sigsplit) - 6))

    bysig = collections.defaultdict(set)
    sigver = {}
    for r in rows:
        bysig[r["sig_hex"]].add(r["unit"])
        sigver[r["sig_hex"]] = (r["verdict"], r["sig_ascii"])
    mags = [(s, u) for s, u in bysig.items() if sigver[s][0] == "MAGIC"]
    print("\n  DISTINCT MAGICS: %d, covering %d units"
          % (len(mags), len(set().union(*[u for _, u in mags])) if mags else 0))
    for s, u in sorted(mags, key=lambda x: -len(x[1])):
        print("    %-8s '%s'  %3d unit(s)" % (s, sigver[s][1], len(u)))
    others = [(s, u) for s, u in bysig.items() if sigver[s][0] != "MAGIC"]
    print("\n  non-magic leading dwords: %d distinct, covering %d units"
          % (len(others), len(set().union(*[u for _, u in others])) if others else 0))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# `%s` signature census - census_bin_signatures.py over %d entries\n"
                    % (a.ext, len(rows)))
            o.write("# verdicts: MAGIC / NOT_A_MAGIC / UNDETERMINED. The UNDETERMINED count is a\n")
            o.write("# reported result, not a failure - see the module docstring.\n")
            o.write("path\tunit\tsize\tsig_hex\tsig_ascii\tverdict\treason\thash\thash_covers\n")
            for r in rows:
                o.write("\t".join(str(r[k]) for k in
                                  ("path", "unit", "size", "sig_hex", "sig_ascii",
                                   "verdict", "reason", "hash", "hash_covers")) + "\n")
        print("\n  wrote %s" % a.out)
    return 0


def self_test():
    """Positive controls. A zero from a classifier that never fires looks like a real zero."""
    ok = True

    def chk(name, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("  FAIL %-46s got %s want %s" % (name, got, want))
        else:
            print("  ok   %-46s %s" % (name, got))

    body = b"\x00" * 64
    chk("st2e is a MAGIC (known present in this archive)",
        classify(b"st2e", b"st2e" + body)[0], "MAGIC")
    chk("sloc is a MAGIC", classify(b"sloc", b"sloc" + body)[0], "MAGIC")
    chk("QST1 is a MAGIC (digits allowed)", classify(b"QST1", b"QST1" + body)[0], "MAGIC")
    chk("all-zero dword is NOT_A_MAGIC",
        classify(b"\0\0\0\0", b"\0" * 68)[0], "NOT_A_MAGIC")
    chk("small leading integer 0x40 is NOT_A_MAGIC",
        classify(b"\x40\0\0\0", b"\x40" + body)[0], "NOT_A_MAGIC")
    # real leading bytes of face_guest10.bin, read from the archive 2026-09-04
    fg = bytes.fromhex("d1d1f4f4f0f092922323151521215e5ea0a0b8b8cecee2e2eeeef3f3f5f5f5f5")
    chk("byte-doubled image data is NOT_A_MAGIC",
        classify(fg[:4], fg)[0], "NOT_A_MAGIC")
    chk("a fully repeating 2-byte unit is NOT_A_MAGIC",
        classify(b"\x94\x03\x94\x03", b"\x94\x03" * 32)[0], "NOT_A_MAGIC")
    # real leading bytes of menuquest01.bin, read from the archive 2026-09-04.
    # 94 03 repeats three times and then stops, so NO structural rule fires and the honest
    # verdict is UNDETERMINED. Asserted deliberately: the instrument must be shown ABSTAINING
    # on a real file, not only disqualifying and accepting, or the bucket is untested.
    mq = bytes.fromhex("940394039403cc4bac54945cffff2d00ffffffff0000000000000000ff0fff0f")
    chk("menuquest01.bin real bytes -> abstain",
        classify(mq[:4], mq)[0], "UNDETERMINED")
    # real leading bytes of ctrl.bin (8352 B) and navimapdata.bin, read from the archive
    ctrl = bytes.fromhex("0b000080a02000009c000000a3000000") + bytes(48)
    cc = bytes.fromhex("43436464 6c6c5c5c 32324d4d 78788f8f 9e9ea7a7 ababb3b3 b3b3b3b3 a1a18181".replace(" ",""))
    chk("byte-doubled data spelling ASCII is NOT a magic (CCdd)",
        classify(cc[:4], cc, 12288)[0], "NOT_A_MAGIC")
    chk("EBP section body identified (marker AND length match)",
        classify(ctrl[:4], ctrl, 8352)[0], "EBP_SECTION_BODY")
    chk("section marker WITHOUT a length match does not qualify",
        classify(ctrl[:4], ctrl, 9999)[0], "UNDETERMINED")
    chk("NAV+version is MAGIC_TAG_VERSION",
        classify(b"NAV\x02", b"NAV\x02" + bytes(60), 3470)[0], "MAGIC_TAG_VERSION")
    chk("high non-ASCII dword with no structure abstains",
        classify(b"\x94\xa3\x17\x0f", b"\x94\xa3\x17\x0f" + bytes(range(60)))[0], "UNDETERMINED")
    chk("logical_unit strips a locale segment",
        logical_unit("ps2data/image/ff12/myoshiok/ch/worldmap/menumap_world.bin"),
        "ps2data/image/ff12/myoshiok/worldmap/menumap_world.bin")
    chk("logical_unit leaves a locale-free path alone",
        logical_unit("ps2data/image/ff12/common/behindcamera.bin"),
        "ps2data/image/ff12/common/behindcamera.bin")
    print("SELF_TEST_%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
