#!/usr/bin/env python3
"""Compare two same-size functions and say WHICH call sites differ.

A body-bytes hash can only say "different". Any two copies of the same source at
different addresses hash differently, because every relative call and RIP-relative
reference encodes the distance to its target -- so the hash is useless for deciding
whether two generated functions are the same code.

This is the constructive counterpart. For a differing displacement field:

    delta == -(addr_b - addr_a)   ->  both reference the SAME absolute target
    delta != -(addr_b - addr_a)   ->  this site DIVERGES; the two functions differ here

Found twice on 2026-09-02 and made a tool on the strength of that:

  * 005847E0 / 00584950 / 00584A40 -- three 92-byte PhyreEngine descriptor destructors.
    The first two are true clones; the third shifts three displacements by its full
    distance but a fourth by a different amount, so exactly one callee differs.
  * 004EDB50 / 004F5360 -- two 7,440-byte residual functions, 1,228 differing bytes.
    1,184 are displacement fields shifted by the exact distance; the 44 that are not
    are the entire semantic difference between them.

Usage:
  clone_diff.py <addrA> <addrB> [--size N] [--exe PATH] [--width 2|4]
  clone_diff.py --family <addr> [<addr> ...]     # pairwise against the first

Addresses are canonical VAs (image base already included).
"""
import argparse
import collections
import io
import struct
import sys
import kit_paths as KP  # noqa: E402
import os

DEFAULT_EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
DEFAULT_FN = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")


def load_pe(path):
    d = io.open(path, "rb").read()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    optsz = struct.unpack_from("<H", d, e + 20)[0]
    ib = struct.unpack_from("<Q", d, e + 24 + 24)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    base = e + 24 + optsz
    secs = []
    for i in range(nsec):
        o = base + 40 * i
        vs, va, rs, pr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((ib + va, ib + va + max(vs, rs), pr))
    return d, secs


def off(secs, va):
    for lo, hi, pr in secs:
        if lo <= va < hi:
            return pr + (va - lo)
    raise SystemExit("VA 0x%X is not inside any section" % va)


def sizes_from_tsv(path):
    import csv
    try:
        return {r["entry"].upper(): int(r["body_bytes"])
                for r in csv.DictReader(io.open(path, encoding="utf-8"), delimiter="\t")}
    except OSError:
        return {}


def compare(d, secs, a, b, n, width):
    A = d[off(secs, a):off(secs, a) + n]
    B = d[off(secs, b):off(secs, b) + n]
    dist = b - a
    diffs = [i for i in range(n) if A[i] != B[i]]

    # group consecutive differing bytes into runs; a shifted disp32 usually shows as
    # a 2- or 3-byte run because its high bytes are unchanged
    runs, cur = [], []
    for i in diffs:
        if cur and i == cur[-1] + 1:
            cur.append(i)
        else:
            if cur:
                runs.append(cur)
            cur = [i]
    if cur:
        runs.append(cur)

    same, diverge, other = [], [], []
    for r in runs:
        st = r[0]
        if st + width <= n:
            va = struct.unpack_from("<H" if width == 2 else "<I", A, st)[0]
            vb = struct.unpack_from("<H" if width == 2 else "<I", B, st)[0]
            mask = (1 << (8 * width)) - 1
            delta = (vb - va) & mask
            signed = delta - (mask + 1) if delta > mask // 2 else delta
            if signed == -dist:
                same.append((st, va, vb, signed))
                continue
            other.append((st, va, vb, signed))
        else:
            other.append((st, None, None, None))

    print("=" * 72)
    print("A 0x%08X   B 0x%08X   distance 0x%X (%d)   size %d" % (a, b, dist, dist, n))
    print("differing bytes: %d in %d run(s)" % (len(diffs), len(runs)))
    print("  same-target displacement fields : %d  (delta == -0x%X)" % (len(same), dist))
    print("  DIVERGENT / other               : %d" % len(other))
    if other:
        print("\n  sites where the two functions differ")
        print("  (a different callee, or a different immediate -- this cannot tell you which):")
        for st, va, vb, sg in other:
            if va is None:
                print("     +0x%04X   (run too short to read as a %d-byte field)" % (st, width))
            else:
                # NOT necessarily a call target. A site whose delta is not the address
                # distance may be a different callee OR a different immediate/index --
                # in the residual twins the 44 divergent sites are index constants, not
                # calls. This tool can say the two functions differ here, never why.
                print("     +0x%04X   0x%0*X -> 0x%0*X   delta %+d"
                      % (st, width * 2, va, width * 2, vb, sg))
    verdict = ("TRUE CLONE - every difference is a displacement to the same targets"
               if not other else
               "NEAR-CLONE - %d site(s) diverge" % len(other))
    print("\n  verdict: %s" % verdict)
    return len(other) == 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("addrs", nargs="+")
    ap.add_argument("--size", type=int)
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--functions", default=DEFAULT_FN)
    ap.add_argument("--width", type=int, default=2, choices=(2, 4),
                    help="field width to read a displacement as; 2 catches the common "
                         "case where only the low half of a rel32 changed")
    a = ap.parse_args(argv)

    d, secs = load_pe(a.exe)
    sizes = sizes_from_tsv(a.functions)
    vas = [int(x, 16) for x in a.addrs]
    n = a.size or sizes.get("%08X" % vas[0])
    if not n:
        raise SystemExit("give --size (no body_bytes found for %08X)" % vas[0])

    ok = True
    for other in vas[1:]:
        m = min(n, sizes.get("%08X" % other, n))
        ok &= compare(d, secs, vas[0], other, m, a.width)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
