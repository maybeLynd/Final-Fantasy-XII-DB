"""shk1_curve_check.py [EXTRACT_ROOT] - test the SHK1 curve reading of the evaluator 003CC5F0 against every
shipped SHK1 section (the nine language copies are deduplicated by section bytes).

The evaluator reads a curve as:
  header  +0x04 keyCount (0 -> return +0x14), +0x08 start (t <= start -> return +0x0C), +0x10 duration
          (t >= duration -> return +0x14), else u = t / duration;
  key i   (36 bytes at +0x18 + 36*i): the segment is found by accumulating float 8 (the weight) until it
          passes u; s = (u - start_of_segment) / weight; value = f4*s^3 + f5*s^2 + f6*s + f7.
Tests:
  1. continuity: key i+1's f7 == key i's f4+f5+f6+f7 (the value at s = 1), for every joint;
     CONTROL: the same equality over random key pairs from different curves must mostly FAIL.
  2. header: +0x0C == first key's f7 (value at the start); +0x14 == last key's f4+f5+f6+f7 (value at the end).
  3. the evaluator-unread floats: f3 == cumulative start frame; f2 == segment end frame (reported, not asserted).
FABLE (Claude Opus 5.5), 2026-09-26."""
import os, struct, sys, random
root = sys.argv[1] if len(sys.argv) > 1 else r"D:\FFXII_TZA_extract"
def close(x, y): return abs(x - y) <= 1e-3 * max(1.0, abs(y))
seen = set(); curves = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.lower().endswith(".ebp"): continue
        b = open(os.path.join(dp, f), "rb").read()
        i = b.find(b"SHK1")
        if i < 0: continue
        h = hash(b[i:i + 4096])
        if h in seen: continue
        seen.add(h)
        cc = struct.unpack_from("<H", b, i + 6)[0]; c = i + struct.unpack_from("<H", b, i + 8)[0]
        for k in range(cc):
            bl, kc = struct.unpack_from("<iI", b, c)
            hdr = struct.unpack_from("<4f", b, c + 8)
            keys = [struct.unpack_from("<9f", b, c + 24 + 36 * j) for j in range(kc)]
            curves.append((hdr, keys)); c += bl
nkeys = sum(len(k) for _, k in curves)
print("unique SHK1 sections %d, curves %d, keys %d" % (len(seen), len(curves), nkeys))
joints = cont = 0
for hdr, ks in curves:
    for j in range(len(ks) - 1):
        joints += 1; cont += close(sum(ks[j][4:8]), ks[j + 1][7])
allk = [k for _, ks in curves for k in ks]; random.seed(1)
ctl = sum(close(sum(random.choice(allk)[4:8]), random.choice(allk)[7]) for _ in range(joints))
print("1. continuity: %d of %d joints; CONTROL random pairs: %d of %d" % (cont, joints, ctl, joints))
s_ok = e_ok = 0; start_nz = start_big = 0
for (st, v0, dur, v1), ks in curves:
    if ks: s_ok += close(v0, ks[0][7]); e_ok += close(v1, sum(ks[-1][4:8]))
    start_nz += st != 0; start_big += abs(st) > 1e-3
print("2. header: +0x0C == first value %d, +0x14 == end value %d, of %d; +0x08 nonzero %d (|x| > 0.001: %d)"
      % (s_ok, e_ok, len(curves), start_nz, start_big))
f3 = f2 = 0
for (st, v0, dur, v1), ks in curves:
    cum = 0.0
    for k in ks:
        f3 += close(k[3], cum * dur); f2 += close(k[2], (cum + k[8]) * dur); cum += k[8]
print("3. unread floats: f3 == cumulative start frame %d of %d; f2 == segment end frame %d of %d" % (f3, nkeys, f2, nkeys))
