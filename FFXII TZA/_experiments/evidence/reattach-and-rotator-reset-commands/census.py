"""Authored commands 0x15 (re-attach the record's children) and 0x25 (rotator back to its default speed), tallied.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under
ps2data/obj_finish. Block and command format as in ../authored-command-census/census.py.
What the code reads (FABLE, 2026-09-20):
  0x15  byte +2 -> record +0x3D1 bits 0-2 (child +0x2C8: non-zero = attachment mode 1, zero = mode 0),
        byte +3 -> bits 3-5 (child +0x2CA likewise)                          (00520740 -> dirty pass -> 00429760)
  0x25  word +2 rotator index (word +6 non-zero = by name), word +4 ramp in frames back to the entry's default speed
Prediction that could fail: blocks named 'active' set field A and blocks named 'deact' clear it, never the reverse.
Controls: 1,218 and 740 commands (authored-command census, .ca only: 1,218 / 740).
"""
import os, struct, collections
ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]; u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
k15 = collections.Counter(); k25 = collections.Counter(); c05 = collections.Counter(); n05 = collections.defaultdict(collections.Counter); c29 = collections.Counter(); n29 = collections.defaultdict(collections.Counter)
for dp, dn, fn in os.walk(ROOT + "/ps2data/obj_finish"):
    for f in fn:
        if not f.endswith(".ca"): continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP": continue
        ver = u32(d, 4); base = 0x30 if ver == 0 else 0x40
        for i in range(u32(d, 0xC)):
            o = u32(d, base + 4 * i)
            if ver == 1 and not o: continue
            b = base + o
            if d[b:b+4] != b"@FMC": continue
            name = d[b+0x10:b+0x30].split(b"\0")[0].decode("latin1")
            h = b + 0x30
            for t in range(u32(d, b + 0xC)):
                ng, dist = d[h+3], u16(d, h+4); g = h + 6
                for _ in range(ng):
                    w = u16(d, g+2); c = g + 4
                    for _ in range(w & 0x3F):
                        w0 = u16(d, c); cid, clen = w0 & 0x7F, w0 >> 7
                        if cid == 0x15:
                            k15[(name, d[c+2], d[c+3])] += 1
                        if cid == 0x25:
                            k25[(u16(d, c+6) != 0, u16(d, c+4))] += 1
                        if cid == 5:
                            v = u16(d, c+2); k = (v >> 12, v & 0xFFF); c05[k] += 1; n05[k][name] += 1
                        if cid == 0x29:
                            v = struct.unpack_from("<h", d, c+2)[0]; c29[v] += 1; n29[v][name] += 1
                        if not clen: break
                        c += clen
                    g += (w >> 6) or 4
                if not dist: break
                h += dist
print("0x15 (block, byte+2, byte+3):", k15.most_common(10))
print("0x25 (byname, frames):", k25.most_common(8), sum(k25.values()))
print("controls: 0x15 total", sum(k15.values()), "; 0x25 total", sum(k25.values()))
print("prediction: active with A = 0:", sum(n for (b, a, _), n in k15.items() if b == "active" and a == 0), "; deact with A != 0:", sum(n for (b, a, _), n in k15.items() if b == "deact" and a != 0))
