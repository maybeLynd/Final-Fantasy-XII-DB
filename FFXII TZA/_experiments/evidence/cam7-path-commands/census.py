"""CAM7 (EBP section_009) record payload census, against the interpreter's own reading.

Walks every us .ebp container (set FF12_EBP_DIR) as the engine does:
  * record +0x20 u32 attachment bitfield           -- read by 002572E0
  * record +0x28 command stream: type byte 1 = key (0x40 B), 2 = segment (0x2C B), 0xFF = end
                                                    -- 00258350 (dispatch at 00258567..00258582)
  * segment +0x04 u16[13] timing words (bit 15 = array-B curve index & 0x7FFF)      -- 00255410
  * segment +0x1E u16[2]  path words   (bit 15 = array-C path index & 0x3FFF, bit 14 = unscaled) -- 002554E0
  * array B record: u32 length, u32 n, f32 start, startValue, end, endValue, n x 0x24 keys -- 003CC5F0
  * array C record: u16 length, u16 ?, u16 n, u16 m, vec3 start, vec3 end, n x 0x38 cubic segments,
                    m x 8 arc-length pairs      -- 003CC740 / 003CC890
Positive control: the published totals (section-009 section 5) must come back -- 423 files,
3,942 records, 15,350 array-B records, 1,682 array-C records.
FABLE, 2026-09-12.
"""
import os, struct, collections

EBP = os.environ["FF12_EBP_DIR"]
U = lambda b, o: struct.unpack_from("<I", b, o)[0]
H = lambda b, o: struct.unpack_from("<H", b, o)[0]
F = lambda b, o: struct.unpack_from("<f", b, o)[0]


def sections(b):
    if b[:4] != b"EBP2":
        return None
    n = U(b, 4); offs = list(struct.unpack_from("<%dI" % n, b, 0x10))
    pres = sorted((o, i) for i, o in enumerate(offs) if o); out = {}
    for k, (o, i) in enumerate(pres):
        out[i] = (o, (pres[k + 1][0] if k + 1 < len(pres) else len(b)) - o)
    return out


def mc(c, n=None):
    """most_common with a deterministic tie-break (count descending, then key text)."""
    items = sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))
    return items if n is None else items[:n]


def sd(d):
    """a plain dict printed in key order."""
    return dict(sorted(d.items(), key=lambda kv: str(kv[0])))


C = collections.Counter
files = recs = nB_tot = nC_tot = 0
grammar_bad = []; seqs = C(); tail = C(); kinds = C(); absflag = C(); seg_pad = C(); dur_zero = 0
timing = C(); timing_by_slot = [C() for _ in range(13)]; paths = C(); path_by_slot = [C() for _ in range(2)]
refB = C(); refC = C(); idx_out = 0; zero_arc_flags = C(); arc_first = C(); arc_last_param = C()
key = {o: C() for o in (0x10, 0x20, 0x24, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C)}
att = C(); att_eye_id = C(); att_tgt_id = C(); att_eye_mode = C(); att_tgt_mode = C(); att_bits = C()
Bsize_ok = Bsize_bad = 0; Bcount = C(); Bend = C()
Csize_ok = Csize_bad = 0; Cfield2 = C(); Cnm = C(); first_seg = []
for dp, _d, fs in sorted(os.walk(EBP)):
    _d.sort()
    for f in sorted(fs):
        if not f.lower().endswith(".ebp"):
            continue
        b = open(os.path.join(dp, f), "rb").read(); s = sections(b)
        if not s or 9 not in s:
            continue
        o9, l9 = s[9]; files += 1
        n = U(b, o9 + 4); nB = U(b, o9 + 8); nC = U(b, o9 + 12); nB_tot += nB; nC_tot += nC
        cur = o9 + U(b, o9 + 0x1C); useB = C(); useC = C(); flagC = {}
        for i in range(n):
            ln = U(b, cur + 4); end = cur + ln; recs += 1
            w = U(b, cur + 0x20); att[w] += 1
            att_eye_id[(w & 0x1FF) != 0] += 1; att_tgt_id[((w >> 16) & 0x1FF) != 0] += 1
            att_eye_mode[(w >> 13) & 3] += 1; att_tgt_mode[(w >> 29) & 3] += 1
            for bit in range(32):
                if w >> bit & 1:
                    att_bits[bit] += 1
            p = cur + 0x28; toks = []; ok = True
            while True:
                if p >= end:
                    ok = False; break
                t = b[p]
                if t == 1:
                    toks.append("K")
                    for o in key:
                        key[o][round(F(b, p + o), 2)] += 1
                    p += 0x40
                elif t == 2:
                    if not toks:
                        first_seg.append((f, i))
                    toks.append("S")
                    seg_pad[bytes(b[p + 1:p + 4]) + bytes(b[p + 0x26:p + 0x2C])] += 1
                    for j in range(13):
                        tw = H(b, p + 4 + 2 * j)
                        if tw & 0x8000:
                            timing["curve"] += 1; timing_by_slot[j]["curve"] += 1; useB[tw & 0x7FFF] += 1
                            idx_out += (tw & 0x7FFF) >= nB
                        else:
                            timing["frames"] += 1; timing_by_slot[j]["frames"] += 1
                    for j in range(2):
                        pw = H(b, p + 0x1E + 2 * j)
                        if pw & 0x8000:
                            k2 = "path-unscaled" if pw & 0x4000 else "path"
                            paths[k2] += 1; path_by_slot[j][k2] += 1; useC[pw & 0x3FFF] += 1; flagC[pw & 0x3FFF] = k2
                            idx_out += (pw & 0x3FFF) >= nC
                        else:
                            paths["none"] += 1; path_by_slot[j]["none"] += 1
                    dur_zero += H(b, p + 0x22) == 0
                    kinds[b[p + 0x24]] += 1; absflag[b[p + 0x25]] += 1
                    p += 0x2C
                elif t == 0xFF:
                    toks.append("E"); p += 1; break
                else:
                    ok = False; toks.append("?%02X" % t); break
            if ok:
                tail[end - p] += 1
            else:
                grammar_bad.append((f, i, "".join(toks)))
            sq = "".join(toks); seqs[sq] += 1
            cur = end
        for k in range(nB):
            L = U(b, cur); m = U(b, cur + 4); Bcount[m] += 1
            if L == 0x18 + 0x24 * m:
                Bsize_ok += 1
            else:
                Bsize_bad += 1
            if m:
                Bend[round(sum(F(b, cur + 0x18 + 0x24 * q + 0x20) for q in range(m)), 3)] += 1
            refB[useB[k]] += 1
            cur += L
        for k in range(nC):
            L = H(b, cur); f2 = H(b, cur + 2); nseg = H(b, cur + 4); marc = H(b, cur + 6)
            Cfield2[f2] += 1; Cnm[(nseg, marc)] += 1
            if L == 0x20 + 0x38 * nseg + 8 * marc:
                Csize_ok += 1
            else:
                Csize_bad += 1
            refC[useC[k]] += 1
            if marc == 0:
                zero_arc_flags[flagC.get(k)] += 1
            else:
                t0 = cur + 0x20 + 0x38 * nseg
                arc_first[(round(F(b, t0), 3), round(F(b, t0 + 4), 3))] += 1
                arc_last_param[round(F(b, t0 + 8 * (marc - 1) + 4), 3)] += 1
            cur += L

print("control: files %d records %d arrayB %d arrayC %d (published 423 / 3,942 / 15,350 / 1,682)" % (files, recs, nB_tot, nC_tot))
print("\n== command stream")
print("records whose stream parses as key/segment/end:", recs - len(grammar_bad), "of", recs, "; failures:", grammar_bad[:5])
print("bytes between the end byte and the record end:", sd(tail))
print("streams:", mc(seqs))
print("streams starting with a segment:", first_seg)
print("\n== key (type 1, 0x40 bytes): value histograms (top 6, distinct count)")
for o in key:
    print("  +0x%02X" % o, mc(key[o], 6), "distinct", len(key[o]))
print("\n== segment (type 2, 0x2C bytes)")
print("interpolation kind +0x24:", sorted(kinds.items()))
print("+0x25 (path offsets absolute when nonzero):", sorted(absflag.items()))
print("+0x01..+0x03 and +0x26..+0x2B all zero:", list(seg_pad.keys()) == [bytes(9)], sd(seg_pad) if len(seg_pad) > 1 else "")
print("duration +0x22 zero:", dur_zero)
print("timing words:", sd(timing))
print("timing words per slot (curve count):", [t["curve"] for t in timing_by_slot])
print("path words:", sd(paths), "per slot:", [sd(x) for x in path_by_slot])
print("curve/path index >= the section's count:", idx_out)
print("array-B records referenced k times:", sd(refB), "; array-C records referenced k times:", sd(refC))
print("\n== array B (timing curves)")
print("length == 0x18 + 0x24*n:", Bsize_ok, "mismatch:", Bsize_bad, "; n histogram:", sorted(Bcount.items()))
print("sum of key spans (+0x20 of each 0x24 key):", mc(Bend, 5))
print("\n== array C (paths)")
print("length == 0x20 + 0x38*n + 8*m:", Csize_ok, "mismatch:", Csize_bad)
print("paths with no arc table (m = 0), by the flag of the word that references them:", sd(zero_arc_flags))
print("first arc pair (distance, param):", mc(arc_first, 3), "; last pair param:", mc(arc_last_param, 3))
print("+0x02:", sd(Cfield2), "; (n, m) top:", mc(Cnm, 8))
print("\n== record +0x20 attachment bitfield")
print("eye actor id (bits 0-8) nonzero:", sd(att_eye_id), "; target actor id (bits 16-24) nonzero:", sd(att_tgt_id))
print("eye mode bits 13-14:", sd(att_eye_mode), "; target mode bits 29-30:", sd(att_tgt_mode))
print("records with each bit set:", dict(sorted(att_bits.items())))
print("most common words:", ["%08X:%d" % (k, v) for k, v in mc(att, 8)])
