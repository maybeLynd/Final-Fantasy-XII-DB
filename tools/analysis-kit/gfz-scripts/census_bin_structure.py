#!/usr/bin/env python3
"""census_bin_structure.py - what SHAPE is each `.bin` signature?

The companion to `census_bin_signatures.py`. That one answered *how many formats share the `.bin`
extension* (28, over 236 logical units). This one asks the next question a sheet-writer needs:
**for each signature, is the file a flat `header + count * record` table, and if so which?**

Why the grading matters more than the answer
--------------------------------------------
`size == hdr + count*rec` is three unknowns. Against ONE file that is one equation, and a fit is
weak however tidy it looks. Against eight files of the same signature it is eight simultaneous
equations and a surviving fit is strong.

So every law is reported with the number of units it had to satisfy, and graded:

    STRONG      a single law, and it holds across 2+ units
    LEAD        a single law, but only one unit exists - one equation, three unknowns
    AMBIGUOUS   more than one law fits; not reportable
    NO-LAW      nothing in THIS SEARCH SPACE fits

**NO-LAW is a statement about the search, not about the file.** The space searched is a
CONSTANT header size, a CONSTANT record size, and a u32 count in the first 16 bytes. Two
signatures this project has already documented come back NO-LAW and are perfectly regular
tables:

  * `licd` is `8 + width*height*2`, its geometry being u16 fields at +4/+6, not a u32 count;
  * `st2e` is `headerSize + count*recordSize`, where **all three are fields in the file**.

So NO-LAW means "not a flat table with constant geometry", and the honest reading is that
the signature needs a human - never that the file has no structure.

**A LEAD is not a finding and this script will not let it be printed as one.** That distinction is
the whole point of the grading column, and it exists because `_index/EVIDENCE-STANDARD.md` requires
a scan's noise floor to be computed before its hits are believed - which for a structural search
means counting how many models fit, not just finding one.

Usage
-----
    python census_bin_structure.py --vbf <archive> --sig-census <tsv> --out <tsv>
    python census_bin_structure.py --self-test
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

HDRS = (8, 12, 16, 20, 24, 32)
COUNT_OFFSETS = (4, 8, 12, 16)
RECS = (2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 48, 64, 80, 96, 128)


def laws_for(sizes_and_counts):
    """[(size, blob)] -> every (hdr, countOffset, recSize) satisfying ALL of them."""
    out = []
    for hdr in HDRS:
        for co in COUNT_OFFSETS:
            for rec in RECS:
                ok = True
                for size, blob in sizes_and_counts:
                    if co + 4 > len(blob):
                        ok = False
                        break
                    c = struct.unpack_from("<I", blob, co)[0]
                    if hdr + c * rec != size:
                        ok = False
                        break
                if ok:
                    out.append((hdr, co, rec))
    return out


def grade(laws, n_units):
    if not laws:
        return "NO-LAW", None
    if len(laws) > 1:
        return "AMBIGUOUS", None
    return ("STRONG" if n_units >= 2 else "LEAD"), laws[0]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--sig-census")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not (a.vbf and a.sig_census):
        return ap.error("--vbf and --sig-census, or --self-test")

    import vbfextract as V
    rows = [l.rstrip("\n").split("\t") for l in io.open(a.sig_census, encoding="utf-8")
            if not l.startswith("#")]
    head = rows[0]
    recs = [dict(zip(head, x)) for x in rows[1:]]
    units = collections.defaultdict(dict)
    for r in recs:
        if r["verdict"] in ("MAGIC", "MAGIC_TAG_VERSION"):
            units[r["sig_ascii"]].setdefault(r["unit"], r["path"])
    if not units:
        raise SystemExit("no MAGIC rows in the signature census - refusing to report an "
                         "empty scan as a result")

    f = io.open(a.vbf, "rb")
    names, blocks = V.load_index(f)
    out = []
    for tag in sorted(units):
        blobs = []
        for u, p in sorted(units[tag].items()):
            d = V.read_entry(f, names, blocks, p)
            blobs.append((len(d), d))
        laws = laws_for(blobs)
        g, law = grade(laws, len(blobs))
        hdr_dwords = " ".join("%08X" % struct.unpack_from("<I", blobs[0][1], o)[0]
                              for o in (4, 8, 12) if o + 4 <= blobs[0][0])
        out.append({
            "signature": tag,
            "units": len(blobs),
            "grade": g,
            "law": ("size = %d + cnt@0x%02X * %d" % law) if law else "",
            "n_laws": len(laws),
            "size_min": min(s for s, _ in blobs),
            "size_max": max(s for s, _ in blobs),
            "hdr_dwords_first_unit": hdr_dwords,
        })

    print("`.bin` STRUCTURE CENSUS - %d signatures" % len(out))
    tally = collections.Counter(r["grade"] for r in out)
    print("  grades: %s" % dict(tally))
    print("\n%-6s %5s %-10s %-34s %s" % ("tag", "units", "grade", "law", "fits"))
    for r in out:
        print("%-6s %5d %-10s %-34s %d"
              % (r["signature"], r["units"], r["grade"], r["law"], r["n_laws"]))
    print("\n  A LEAD is one equation in three unknowns. It is not a finding.")
    print("  NO-LAW = no CONSTANT-geometry table fits. It describes the search, not the")
    print("  file: `licd` and `st2e` are documented tables and both land there, because")
    print("  their header and record sizes are fields rather than constants.")

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# `.bin` structure census - census_bin_structure.py\n")
            o.write("# grade: STRONG (one law over 2+ units) | LEAD (one law, ONE unit - one\n")
            o.write("#        equation, not a finding) | AMBIGUOUS | NO-LAW\n")
            o.write("# NO-LAW = no CONSTANT-geometry table fits; a statement about the\n")
            o.write("# search, not the file. `licd` and `st2e` are documented tables and\n")
            o.write("# both land here because their geometry is stored in the file.\n")
            cols = ("signature", "units", "grade", "law", "n_laws",
                    "size_min", "size_max", "hdr_dwords_first_unit")
            o.write("\t".join(cols) + "\n")
            for r in out:
                o.write("\t".join(str(r[c]) for c in cols) + "\n")
        print("\n  wrote %s" % a.out)
    return 0


def self_test():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("  FAIL %-56s got %s want %s" % (name, got, want))
        else:
            print("  ok   %-56s %s" % (name, got))

    # a flat table: 16 + 3*16 = 64 bytes, count 3 at +8
    b = bytearray(64)
    struct.pack_into("<I", b, 8, 3)
    laws = laws_for([(64, bytes(b))])
    chk("a real flat table yields at least one law", len(laws) >= 1, True)

    # two units of the same shape must NARROW the law set, never widen it
    b2 = bytearray(96)
    struct.pack_into("<I", b2, 8, 5)
    two = laws_for([(64, bytes(b)), (96, bytes(b2))])
    chk("two units narrow the law set", len(two) <= len(laws), True)
    chk("the surviving law is the right one", (16, 8, 16) in two, True)

    chk("one unit + one law grades LEAD, not a finding",
        grade([(16, 8, 16)], 1)[0], "LEAD")
    chk("two units + one law grades STRONG", grade([(16, 8, 16)], 2)[0], "STRONG")
    chk("several laws grade AMBIGUOUS",
        grade([(16, 8, 16), (8, 4, 4)], 5)[0], "AMBIGUOUS")
    chk("no law grades NO-LAW", grade([], 9)[0], "NO-LAW")
    print("SELF_TEST_%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
