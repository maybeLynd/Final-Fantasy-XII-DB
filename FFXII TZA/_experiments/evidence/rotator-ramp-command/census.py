"""Authored command 0x24 - the rotator speed ramp - tallied as its handler 005201B0 reads it.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under
ps2data/obj_finish. Block and command format as in ../authored-command-census/census.py.
What the code reads (FABLE, 2026-09-20): word +6 - 0 = word +2 is a rotator INDEX; non-zero with bit 7 clear = word +2
is looked up (00519100) to an index; bits 7 and 6 both set = the call goes to rig controller 5 instead; bit 7 alone =
nothing. word +4 = ramp length in frames (0 = set at once). float +8 = target angular speed.
Prediction that could fail: no command has bit 7 of word +6 without bit 6 (that arm does nothing).
Control: 1,493 commands (authored-command census).
"""
import os, struct, collections
ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]; u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
k24 = collections.Counter(); fr24 = collections.Counter(); sp24 = collections.Counter(); c05 = collections.Counter(); n05 = collections.defaultdict(collections.Counter); c29 = collections.Counter(); n29 = collections.defaultdict(collections.Counter)
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
                        if cid == 0x24:
                            w6 = u16(d, c+6); k24[('ctrl5' if (w6 & 0xC0) == 0xC0 else 'bit7only' if w6 & 0x80 else 'byname' if w6 else 'byindex')] += 1; fr24[u16(d, c+4)] += 1; sp24[round(struct.unpack_from('<f', d, c+8)[0], 2)] += 1
                        if cid == 5:
                            v = u16(d, c+2); k = (v >> 12, v & 0xFFF); c05[k] += 1; n05[k][name] += 1
                        if cid == 0x29:
                            v = struct.unpack_from("<h", d, c+2)[0]; c29[v] += 1; n29[v][name] += 1
                        if not clen: break
                        c += clen
                    g += (w >> 6) or 4
                if not dist: break
                h += dist
print("0x24 addressing:", sorted(k24.items()))
print("0x24 frames word +4:", fr24.most_common(8))
print("0x24 target float +8:", sp24.most_common(10))
print("control: total", sum(k24.values()), "(census 1,493); bit-7-only commands:", k24.get("bit7only", 0))
