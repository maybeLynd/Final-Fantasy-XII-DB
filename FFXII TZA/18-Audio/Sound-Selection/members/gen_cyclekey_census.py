#!/usr/bin/env python3
"""Census of the SabFile::Sequence key byte (007CF9A0: +5 at version <= 2,
+0x11 from version 3) over every shipped `.sab` bank in FFXII_TZA.vbf, for
FABLE-REQ-SWE2-DATA-CYCLESOUND-KEY-BYTE-CENSUS / sound-trigger.md UQ-259.

The five selection walkers group a list's entries by this byte; CycleSound
(007E6360) and SwitchSound (007E67C0) are two of the policies, and the owning
class is chosen by the sound record's byte +4 (factory 007B2F70).  Because the
snd-class census found +4 in {0,1} only, no shipped bank builds a CycleSound
or SwitchSound object at all - but the Sequence records that do ship still
carry the key byte, so its authored values and run structure are measurable.

Layout (verified against the first bank's records):
    'seq ' chunk = { u16 0, u16 0x10, u32 count, u32[3] pad,
                     u32 offsets[count] } at +0x10, chunk-relative offsets.

    SabFile::Sequence record (shipped version 4):
        +0    u8   version            4 in all shipped records
        +4    u16  seq-record id      dense in the family/bank seq namespace:
                                      multi-record banks 0..n-1 (se200/se208
                                      0..31); one-record banks dense across
                                      the family (se001001=1, se010 0..263,
                                      byte +5 non-zero on 428 records);
                                      4,078 of 4,097 single-sound banks
                                      carry +4 != 0.  NOT the owning sound's
                                      in-bank u8 index (corrected
                                      2026-09-20).
        +0x10 f32  weight / rangeMin  shared storage (UQ-261); byte +0x11 is
                                     its second byte
        +0x11 u8   group key          what 007CF9A0 returns at version >= 3
        +0x14 f32  rangeMax           SwitchSound half-open range top

`.mab` banks ship chunks musc/inst/mtrl only - verified: no `seq ` chunk in
any of the 116 shipped .mab files, so the census is .sab-only.

Per-list run structure: a sound's candidate list length is the sound record's
+5; the snd-class census measured +5 == 1 for every class-1 sound and 0 for
every class-0 sound, so each shipped list is a single entry.  The census still
reports consecutive-equal-key runs across each bank's seq table and distinct
keys per bank, since that is what "cycle steps" would look like if they
shipped.

Usage: gen_cyclekey_census.py [vbf-path]
    -> writes cyclekey-census.tsv beside this script and prints the summary.
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


def chunk(blob, want):
    """Return the byte slice of chunk `want`, or None."""
    o = 0x20
    while o + 16 <= len(blob):
        tag = blob[o:o + 4]
        if not all(32 <= c < 127 for c in tag):
            break
        off = U32(blob, o + 8)
        if off == 0 or off >= len(blob):
            break
        if tag == want:
            return blob[off:]
        o += 16
    return None


def records(c):
    """Yield record slices from a {u16 0,u16 0x10,u32 count,...,offsets[]}
    chunk directory."""
    if c is None or U16(c, 0) != 0 or U16(c, 2) != 0x10:
        return
    n = U32(c, 4)
    if 0x10 + 4 * n > len(c):
        return
    for i in range(n):
        yield i, U32(c, 0x10 + 4 * i), c


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    sabs = sorted(p for p in names if p.lower().endswith(".sab"))
    mabs = sorted(p for p in names if p.lower().endswith(".mab"))

    ver_dist = collections.Counter()      # sequence record version
    key_dist = collections.Counter()      # key byte value -> records
    w_dist = collections.Counter()        # u32 @+0x10 (weight / rangeMin)
    rmax_dist = collections.Counter()     # u32 @+0x14 (rangeMax)
    idx_match = 0                          # +4 == record index in chunk
    total = 0
    cls45 = 0                              # snd records with class 4 or 5
    mab_seq = 0                            # .mab files carrying a seq chunk

    run_rows = []                          # per-bank run summaries
    tsv = io.open(os.path.join(HERE, "cyclekey-census.tsv"), "w",
                  encoding="utf-8", newline="\n")
    tsv.write("# SabFile::Sequence key-byte census - 007CF9A0's +0x11 (v>=3) "
              "over all shipped .sab banks\n")
    tsv.write("# u32_10 = the +0x10 field the key byte overlays (UQ-261); "
              "u32_14 = rangeMax\n")
    tsv.write("bank\tseq_index\tversion\tkey(+0x11)\tu32_10\tu32_14\n")

    for p in sabs:
        blob = V.read_entry(f, names, blocks, p)
        snd = chunk(blob, b"snd ")
        for _, ro, c in (records(snd) or ()):
            if len(c) - ro >= 0x1A and c[ro + 4] in (4, 5):
                cls45 += 1
        c = chunk(blob, b"seq ")
        keys = []
        for i, ro, cc in (records(c) or ()):
            if len(cc) - ro < 0x18:
                continue
            ver = cc[ro]
            key = cc[ro + 0x11] if ver >= 3 else cc[ro + 5]
            w = U32(cc, ro + 0x10)
            rmax = U32(cc, ro + 0x14)
            ver_dist[ver] += 1
            key_dist[key] += 1
            w_dist[w] += 1
            rmax_dist[rmax] += 1
            if U16(cc, ro + 4) == i:
                idx_match += 1
            keys.append(key)
            total += 1
            tsv.write("%s\t%d\t%d\t%d\t0x%08x\t0x%08x\n"
                      % (p, i, ver, key, w, rmax))
        # consecutive-equal-key runs across the bank's seq table
        runs = []
        for k in keys:
            if runs and runs[-1][0] == k:
                runs[-1][1] += 1
            else:
                runs.append([k, 1])
        run_rows.append((p, len(keys), len(set(keys)), len(runs),
                         max((r[1] for r in runs), default=0)))
    tsv.close()

    for p in mabs:
        blob = V.read_entry(f, names, blocks, p)
        if chunk(blob, b"seq ") is not None:
            mab_seq += 1

    print("banks", len(sabs), "mabs", len(mabs), "mab with seq chunk:", mab_seq)
    print("seq records", total, "u16(+4) seq-id == chunk position:", idx_match)
    print("version dist:", dict(ver_dist))
    print("key byte dist:", dict(sorted(key_dist.items())))
    print("u32@+0x10 dist:", {hex(k): v for k, v in w_dist.most_common(8)})
    print("u32@+0x14 dist:", {hex(k): v for k, v in rmax_dist.most_common(8)})
    print("snd records class 4/5 (Cycle/Switch):", cls45)
    multi = [r for r in run_rows if r[4] > 1]
    print("banks with a run>1 of equal keys:", len(multi))
    for r in multi[:10]:
        print("  ", r)


if __name__ == "__main__":
    main()
