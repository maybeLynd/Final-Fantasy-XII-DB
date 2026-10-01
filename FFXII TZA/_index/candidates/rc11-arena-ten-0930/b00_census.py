"""b00_census.py - which record kinds the shipped effect data store through chunk type 0xB00, the only route to the
0x59 record loader 00504350 (ORACLE, 2026-09-30, RC-11). Static, authored data. Reads only.

Route (read from the image, see README): 00504350 has two direct callers, 003AA109 in 003A9EF0 (miss path) and
00500A20 in 00500980 (hit path; 00500980's only caller is 003A9F42 in 003A9EF0). 003A9EF0's only caller is 003EDAA0 in
003ED8A0, the arm for chunk type 0xB00 (003EDA81), called with rbx = its own rcx + 8 (003ED8BD); 003EE2D0 passes rcx = chunk + 4 (003EE1EC-003EE1F2 in the parse 003EDAD0), so the record is chunk + 0xC. 003ED8A0's only caller is 003EE39B in
003EE2D0, the arm for chunk flag word 0x100. The record's kind byte is stream + 2 (the dispatch page s2.7), so chunk +0xE.

Walker: the one of 17-Presentation-Rendering/Effect-File-Formats/members/type_census.py (imported, unchanged): every
.efx, every .efb blob, and the 531 EFX streams embedded in .cm / .mpk files; chunks {u32 length, u16 flag, u16 type}.

Checks (exit 1 on failure):
  C1 every stream walk ends exactly at its declared size (so every shipped chunk carries flag 0x100: the walker stops
     at any other flag, and 003EE2D0's 0x101 / 0x102 / 0x103 arms are never taken by shipped data);
  C2 POSITIVE CONTROL: 0xB00 chunks exist and their kind bytes lie in 0x50..0x59 (the store's dispatch range,
     00500984-0050098E); a misread offset fails this;
  C3 POSITIVE CONTROL: the 0xA00 record total equals the published census total, 48,868.
Prints the per-kind count of 0xB00 records and every file carrying kind 0x59.
"""
import collections, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Effect-File-Formats", "members"))
import type_census as tc  # noqa: E402


def main():
    std = []
    for dp, dn, fn in os.walk(os.path.join(tc.ROOT, "ps2data")):
        std += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
    emb = [os.path.join(tc.ROOT, l.strip()) for l in open(tc.EMB) if l.strip()]
    kinds, files59, inexact, a00 = collections.Counter(), collections.defaultdict(int), 0, 0
    flags = collections.Counter()
    nstreams = 0
    for p in std + emb:
        b = open(p, "rb").read()
        for ch, exact in tc.streams(b):
            nstreams += 1
            inexact += not exact
            for ty, o in ch:
                flags[struct.unpack_from("<H", b, o + 4)[0]] += 1
                if ty == 0xA00:
                    a00 += 1
                if ty == 0xB00:
                    k = b[o + 0xE]
                    kinds[k] += 1
                    if k == 0x59:
                        files59[os.path.relpath(p, tc.ROOT).replace("\\", "/")] += 1
    fails = 0
    ok1 = inexact == 0
    print("%s  C1 %d streams, %d walks not ending at the declared size; chunk flag words seen: %s"
          % ("PASS" if ok1 else "FAIL", nstreams, inexact, dict(flags)))
    ok2 = bool(kinds) and min(kinds) >= 0x50 and max(kinds) <= 0x59
    print("%s  C2 0xB00 records %d, kinds within 0x50..0x59" % ("PASS" if ok2 else "FAIL", sum(kinds.values())))
    ok3 = a00 == 48868
    print("%s  C3 0xA00 records %d (published 48,868)" % ("PASS" if ok3 else "FAIL", a00))
    fails = (not ok1) + (not ok2) + (not ok3)
    print("0xB00 records by kind: %s" % ", ".join("0x%02X %d" % kv for kv in sorted(kinds.items())))
    print("kind 0x59 records: %d in %d files" % (kinds[0x59], len(files59)))
    by_dir = collections.Counter("/".join(f.split("/")[:3]) for f in files59)
    print("kind 0x59 files by top directory: %s" % dict(sorted(by_dir.items())))
    by_ext = collections.Counter(os.path.splitext(f)[1] for f in files59)
    print("kind 0x59 files by extension: %s" % dict(by_ext))
    for f in sorted(files59)[:40]:
        print("  %s  %d" % (f, files59[f]))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
