"""The two authored commands that make a character's sounds, tallied by parameter and by the animation block that authors them.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under
ps2data/obj_finish. Block and command format as in ../authored-command-census/census.py.
What the code reads (FABLE, 2026-09-20):
  command 0x05  u16 +2 = mode << 12 | type          (00520C50 -> 0046CC70(emitter, mode, type, volume 0 = full))
  command 0x29  i16 +2 = volume, 128 = full          (00520D00 -> 0046CC70(emitter, mode 0, type 1, volume))
  mode 0 types 1..12 are the twelve arms of the variation picker 0046C250; mode 4 carries an explicit sound number
Predictions that could fail:
  P1  every mode-0 type of command 0x05 is in 1..12 (the picker refuses anything else)
  P2  modes other than 0 and 4 are not authored
Control: command totals must equal the authored-command census (.ca only): 0x05 = 23,783, 0x29 = 47,472.
"""
import os, struct, collections
ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]; u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
c05 = collections.Counter(); n05 = collections.defaultdict(collections.Counter); c29 = collections.Counter(); n29 = collections.defaultdict(collections.Counter)
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
                        if cid == 5:
                            v = u16(d, c+2); k = (v >> 12, v & 0xFFF); c05[k] += 1; n05[k][name] += 1
                        if cid == 0x29:
                            v = struct.unpack_from("<h", d, c+2)[0]; c29[v] += 1; n29[v][name] += 1
                        if not clen: break
                        c += clen
                    g += (w >> 6) or 4
                if not dist: break
                h += dist
print("0x05 (mode, type) -> count ; commonest block names")
for k, n in c05.most_common(24): print("  ", k, n, ", ".join(x for x, _ in n05[k].most_common(5)))
print("0x29 word +2 -> count ; names")
for k, n in c29.most_common(12): print("  ", k, n, ", ".join(x for x, _ in n29[k].most_common(5)))

print("control: 0x05 total", sum(c05.values()), "(census 23,783) ; 0x29 total", sum(c29.values()), "(census 47,472)")
print("P1  mode-0 types outside 1..12:", sorted(k for k in c05 if k[0] == 0 and not 1 <= k[1] <= 12) or "none")
print("P2  modes authored:", sorted({k[0] for k in c05}))
