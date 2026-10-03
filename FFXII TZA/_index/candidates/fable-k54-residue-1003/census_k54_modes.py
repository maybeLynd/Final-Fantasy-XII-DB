"""census_k54_modes.py - FABLE 2026-10-03. Which per-pass UV modes shipped effects author.

The walks that fill the draw-parameter block copy each pass's mode byte (param + 0x1B0 + p) from byte +7 of a 0xF0-byte
pass slot of the element DEFINITION, and the axis byte (param + 0x1B4 + p) from bit 0 of slot byte +0xB; a slot is
skipped when its byte +0 is 0 (k54_residue.py, section C, proves this by execution for all four walks). The slot
arrays start at:
    type 0x05 (kind-0x54 mesh, walk 00449AB0, draw 004355D0 family)   definition + 0x250
    type 0x04 (ring band, walk 004453D0, draw 004434D0 / 00444340)     definition + 0x350
    type 0x06 (column, walk 00447020, same draw pair)                  definition + 0x3B0
    type 0x07 (dome, walk 00447ED0, same draw pair)                    definition + 0x3B0
The definition is the 0xA00 chunk's payload at chunk + 0x10 (effect-mesh-records-kind-54.md s5; census_mesh54.py reads
+0x570 / +0x590 there). Streams: every EFX stream of the full extract, walked exactly as members/type_census.py
(3,288 .efx, the EFX blobs inside the 410 .efb, and the 531 embedded streams in .cm / .mpk files), imported from it.

Also recorded: the path each element takes - for type 0x05 from definition byte +0x590 through 004355D0's rule
(+0x1F1 >= 0x80 -> 00438860, else bit 3 -> 00437130, else inline; the +0x1F1 bits are the ones k54_residue.py's
emulation of 00449AB0 derives: bit 7 = +0x590 bit 5, bit 3 = +0x590 bit 0 OR bit 5); for the grid types from
+0x672 / +0x6D2 bit 0 (set -> 00444340, else 004434D0).

Checks (exit 1 on failure):
  N1 type 0x04 / 0x05 / 0x06 / 0x07 chunk counts equal type_census.tsv's (173 / 5,204 / 25 / 0);
  N2 every definition is long enough for its four slots and its path byte;
  N3 the type-0x05 path census over the .efx/.efb-first-blob population reproduces the page's s5 figures
     (VU0 514, alternative 1,791, inline 2,859 over 5,164 elements) - so the path rule matches the page's.
The +0x1D8 + 4p scalar of a pass is 004309C0 evaluated on the 16-byte track 0x10 bytes before the slot (its kind bytes
+0xC / +0xD: 0 = 0.0, 1 = a resource's float, other = a keyed curve, 004309C0+0xA..+0x3F); for mode-2 slots the two
kind bytes are tallied.
Output: k54_modes.tsv (one row per active slot) and the summary printed to stdout.
"""
import collections
import csv
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.abspath(os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Effect-File-Formats", "members"))
sys.path.insert(0, MEM)
import type_census as TC  # noqa: E402

SLOTS = {0x05: 0x250, 0x04: 0x350, 0x06: 0x3B0, 0x07: 0x3B0}
PATHBYTE = {0x05: 0x590, 0x04: 0x672, 0x06: 0x6D2, 0x07: 0x6D2}


def path_of(t, rec):
    b = rec[PATHBYTE[t]]
    if t == 0x05:
        f1 = (((b >> 5) & 1) << 7) | ((((b >> 0) | (b >> 5)) & 1) << 3)
        if f1 >= 0x80:
            return "00438860"
        return "00437130" if f1 & 8 else "inline"
    return "00444340" if b & 1 else "004434D0"


def main():
    fails = []
    std = []
    for dp, dn, fn in os.walk(os.path.join(TC.ROOT, "ps2data")):
        std += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
    std.sort()
    emb = [os.path.join(TC.ROOT, l.strip()) for l in open(TC.EMB) if l.strip()]
    n_el = collections.Counter()
    short = []
    rows = []
    for src, paths in (("std", std), ("emb", emb)):
        for p in paths:
            b = open(p, "rb").read()
            rel = os.path.relpath(p, TC.ROOT).replace("\\", "/")
            for ch, exact in TC.streams(b):
                for ty, o in ch:
                    if ty != 0xA00:
                        continue
                    t = b[o + 0xE]
                    if t not in SLOTS:
                        continue
                    ln = struct.unpack_from("<I", b, o)[0]
                    rec = b[o + 0x10:o + ln]
                    n_el[t] += 1
                    need = max(SLOTS[t] + 3 * 0xF0 + 0xC, PATHBYTE[t] + 1)
                    if len(rec) < need:
                        short.append((rel, o, t, len(rec)))
                        continue
                    path = path_of(t, rec)
                    p_idx = 0
                    for i in range(4):
                        s = rec[SLOTS[t] + 0xF0 * i:SLOTS[t] + 0xF0 * (i + 1)]
                        if s[0] == 0:
                            continue
                        trk = rec[SLOTS[t] + 0xF0 * i - 0x10:SLOTS[t] + 0xF0 * i]   # the +0x1D8 scalar's track
                        rows.append((rel, src, "0x%X" % o, "0x%02X" % t, path, i, p_idx, s[0], s[7], s[0xB] & 1,
                                     s[0xB], s[0xA], trk[0xC], trk[0xD]))
                        p_idx += 1
    # N1
    tc = {}
    for r in csv.DictReader(open(os.path.join(MEM, "type_census.tsv")), delimiter="\t"):
        tc[int(r["type"], 16)] = int(r["chunks"])
    want = {t: tc.get(t, 0) for t in SLOTS}
    got = {t: n_el[t] for t in SLOTS}
    ok1 = want == got
    print("N1 element chunks by type %s, type_census.tsv %s: %s" % (
        {"0x%02X" % k: v for k, v in sorted(got.items())}, {"0x%02X" % k: v for k, v in sorted(want.items())},
        "PASS" if ok1 else "FAIL"))
    if not ok1:
        fails.append("N1")
    print("N2 definitions too short for their slots: %d %s" % (len(short), "PASS" if not short else "FAIL"))
    if short:
        fails.append("N2 %s" % short[:3])
    # N3: compare with the page's own TSV (effect-mesh-54-element05.tsv) row by row on the .efx population
    tsv = list(csv.DictReader(open(os.path.join(MEM, "effect-mesh-54-element05.tsv")), delimiter="\t"))
    page_path = collections.Counter()
    for r in tsv:
        page_path[path_of(0x05, bytes(0x590) + bytes([int(r["mode_0x590"], 16)]))] += 1
    print("N3 page TSV (%d type-0x05 rows) path census through this script's rule: %s" % (len(tsv), dict(page_path)))
    ok3 = (len(tsv) == 5164 and page_path == collections.Counter({"00438860": 514, "00437130": 1791, "inline": 2859}))
    print("N3 reproduces the page's s5 'VU0 514, alternative 1,791, inline 2,859': %s" % ("PASS" if ok3 else "FAIL"))
    if not ok3:
        fails.append("N3")

    with open(os.path.join(HERE, "k54_modes.tsv"), "w", newline="\n") as fo:
        fo.write("file\tsource\tchunk_off\ttype\tpath\tslot\tpass\tbyte0\tmode_b7\taxis_bB0\tbyteB\tbyteA\t"
                 "s_track_kindC\ts_track_kindD\n")
        for r in rows:
            fo.write("\t".join(str(x) for x in r) + "\n")

    # summaries
    print()
    print("SUMMARY active pass slots (byte +0 != 0) by type: %s" % dict(collections.Counter(r[3] for r in rows)))
    for t in ("0x05", "0x04", "0x06", "0x07"):
        R = [r for r in rows if r[3] == t]
        if not R:
            print("type %s: no active slots" % t)
            continue
        print("type %s: %d active slots in %d elements" % (t, len(R), len({(r[0], r[2]) for r in R})))
        print("   byte +0 (texture mode) histogram: %s" % sorted(collections.Counter(r[7] for r in R).items()))
        print("   mode byte +7 histogram:           %s" % sorted(collections.Counter(r[8] for r in R).items()))
        for mval in sorted(set(r[8] for r in R)):
            M = [r for r in R if r[8] == mval]
            print("     mode %d: %d slots, %d elements, %d files, %d distinct assets; axis (+0xB bit 0) %s; by path %s; "
                  "by pass index %s" % (
                mval, len(M), len({(r[0], r[2]) for r in M}), len({r[0] for r in M}),
                len({TC.asset_key(r[0]) for r in M}),
                sorted(collections.Counter(r[9] for r in M).items()),
                sorted(collections.Counter(r[4] for r in M).items()),
                sorted(collections.Counter(r[6] for r in M).items())))
            if mval == 2:
                print("       mode 2 planar-scalar track (slot - 0x10, read by 004309C0) kind bytes (+0xC, +0xD): %s" % (
                    sorted(collections.Counter((r[12], r[13]) for r in M).items())))
    el, el_lit = {}, {}
    for r in rows:
        el[(r[0], r[2], r[3])] = r[4]
        if r[8] != 0:
            el_lit[(r[0], r[2], r[3])] = r[4]
    print("elements with an active slot, by (type, draw path): %s" % sorted(collections.Counter(
        (k[2], v) for k, v in el.items()).items()))
    print("elements with a slot of mode 1..255, by (type, draw path): %s" % sorted(collections.Counter(
        (k[2], v) for k, v in el_lit.items()).items()))
    lit = [r for r in rows if r[8] != 0]
    print("TOTALS active slots %d; slots with mode != 0: %d; modes above 4: %d; modes 1/3 (matrix of modes 1 and 3): %d; "
          "modes 2/4: %d" % (len(rows), len(lit), sum(1 for r in lit if r[8] > 4),
                             sum(1 for r in lit if r[8] in (1, 3)), sum(1 for r in lit if r[8] in (2, 4))))
    m2 = [r for r in rows if r[3] == "0x05" and r[8] == 2]
    print("type 0x05 mode-2 slots %d: scalar track kinds 0/0 (constant 0.0) %d, 1/0 %d, other %d" % (
        len(m2), sum(1 for r in m2 if (r[12], r[13]) == (0, 0)), sum(1 for r in m2 if (r[12], r[13]) == (1, 0)),
        sum(1 for r in m2 if (r[12], r[13]) not in ((0, 0), (1, 0)))))
    print("(type, mode, slot byte +0) for modes != 0: %s" % sorted(collections.Counter(
        (r[3], r[8], r[7]) for r in rows if r[8] != 0).items()))
    print("FAILS %d" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
