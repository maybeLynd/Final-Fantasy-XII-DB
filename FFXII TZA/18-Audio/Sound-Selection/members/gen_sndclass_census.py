#!/usr/bin/env python3
"""Census of SabFile::Sound record byte +4 (the 007B2F70 class selector) over
every shipped `.sab` sound bank in FFXII_TZA.vbf.

Layout, verified against sab-sound-bank-container.md and the first record of
each bank:
    .sab header 0x10 + 16-byte name, then a 16-byte-per-entry chunk directory;
    the 'snd ' chunk is  { u16 0, u16 0x10, u32 count, u32[3] pad,
                           u32 offsets[count] } at +0x10, each offset
    chunk-relative and pointing at a SabFile::Sound record (version 16).

    record +0    u8  version          16 in all shipped records
    record +4    u8  class selector   0/1 base Sound, 2 Random, 3 Order,
                                      4 Cycle, 5 Switch  (007B2F70 @ 007B30C7)
    record +5    u8  candidate count  read unversioned by the five walkers
    record +0x19 bit 5                allow-repeat flag (007E5459..007E55B5)

Usage: gen_sndclass_census.py [vbf-path]   -> writes sndclass-census.tsv beside
this script and prints the summary tables.
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "..", "agent_flow", "tools")))
import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]

CLASS_NAMES = {0: "Sound(base)", 1: "Sound(base)", 2: "RandomSound",
               3: "OrderSound", 4: "CycleSound", 5: "SwitchSound"}


def snd_chunk(blob):
    """Return the byte slice of the 'snd ' chunk, or None."""
    o = 0x20
    while o + 16 <= len(blob):
        tag = blob[o:o + 4]
        if not all(32 <= c < 127 for c in tag):
            break
        off = U32(blob, o + 8)
        if off == 0 or off >= len(blob):
            break
        if tag == b"snd ":
            return blob[off:]
        o += 16
    return None


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    sabs = sorted(p for p in names if p.lower().endswith(".sab"))

    cls_count = collections.Counter()      # +4 value -> records
    cand_dist = collections.Counter()      # (cls, +5) -> records, cls in 2..5
    rep_dist = collections.Counter()       # (cls, bit5) -> records, cls in 2..5
    ver_dist = collections.Counter()
    hdr_bad = off_bad = 0
    per_class_examples = collections.defaultdict(list)
    stride_hist = collections.Counter()
    total = 0

    rows = []
    for p in sabs:
        blob = V.read_entry(f, names, blocks, p)
        c = snd_chunk(blob)
        if c is None or U16(c, 0) != 0 or U16(c, 2) != 0x10:
            hdr_bad += 1
            continue
        n = U32(c, 4)
        if 0x10 + 4 * n > len(c):
            off_bad += 1
            continue
        bank = os.path.basename(p)
        prev = None
        for i in range(n):
            ro = U32(c, 0x10 + 4 * i)
            if ro + 0x1A > len(c):
                off_bad += 1
                continue
            if prev is not None:
                stride_hist[ro - prev] += 1
            prev = ro
            r = c[ro:]
            ver, cls, cand = r[0], r[4], r[5]
            rep = (r[0x19] >> 5) & 1
            ver_dist[ver] += 1
            cls_count[cls] += 1
            total += 1
            if cls in (2, 3, 4, 5):
                cand_dist[(cls, cand)] += 1
                rep_dist[(cls, rep)] += 1
                if len(per_class_examples[cls]) < 12:
                    per_class_examples[cls].append((bank, i))
            rows.append((bank, i, ver, cls, cand, rep))

    out = os.path.join(HERE, "sndclass-census.tsv")
    with io.open(out, "w", encoding="utf-8", newline="\n") as w:
        w.write("# SabFile::Sound record census - byte +4 class selector over "
                "every shipped .sab (FABLE-REQ-SWE2-DATA-SOUND-CLASS-BYTE-CENSUS)\n")
        w.write("# only records with +4 in 2..5 carry meaningful +5/+0x19 reads\n")
        w.write("bank\trecord_index\tversion\tclass(+4)\tcandidates(+5)\t"
                "allow_repeat(+0x19 bit5)\n")
        for row in rows:
            w.write("%s\t%d\t%d\t%d\t%d\t%d\n" % row)

    print("files", len(sabs), "records", total,
          "bad headers", hdr_bad, "bad offsets", off_bad)
    print("version dist:", dict(ver_dist))
    print("record stride dist:", dict(stride_hist))
    print("\nclass (+4) distribution:")
    for k in sorted(cls_count):
        print("  %d %-12s %d" % (k, CLASS_NAMES.get(k, "?"), cls_count[k]))
    print("\nfor classes 2..5 - candidates(+5):")
    for k in sorted(cand_dist):
        print("  cls %d cand %d -> %d" % (k[0], k[1], cand_dist[k]))
    print("for classes 2..5 - +0x19 bit5:")
    for k in sorted(rep_dist):
        print("  cls %d bit5 %d -> %d" % (k[0], k[1], rep_dist[k]))
    print("\nexamples per built class:")
    for cls in sorted(per_class_examples):
        print("  cls %d (%s):" % (cls, CLASS_NAMES[cls]),
              ", ".join("%s#%d" % e for e in per_class_examples[cls]))


if __name__ == "__main__":
    main()
