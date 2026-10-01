"""The motion-control commands 0x00, 0x03 and 0x2C, tallied as their invokers read them.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under
ps2data/obj_finish. Block and command format as in ../authored-command-census/census.py.
What the code reads (FABLE, 2026-09-20):
  0x00  i16 +2  the motion's length in frames; negative = endless                     (00417810)
  0x03  i16 +2  a hold count; -1 = hold once per rate tick                            (00417A80)
  0x2C  u16 +2  the motion being LEFT, matched against the entry's previous motion number & 0xFFF; 0xFFFF = any;
        u8 +4 blend frames (0 = cut, 0xFF = the no-blend flag); u8 +5 bit 7 a flag, low 7 bits a signed start offset;
        i8 +6; u8 +7 the number of (a, b) byte pairs that follow from +8                                  (00417DE0)
Predictions that could fail:
  P1  exactly one 0x00 per block, and it is the first command of the block's first track
  P2  every 0x2C 'from' word is 0xFFFF or fits in 12 bits
  P3  every 0x2C is long enough for its pair count: length >= 8 + 2 x count
"""
import os, struct, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]; u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
blocks = first_ok = 0; per_block = collections.Counter(); length = collections.Counter(); hold = collections.Counter()
frm_bad = short = n2c = 0; blend = collections.Counter(); pairs = collections.Counter(); anyfrom = 0
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data", "obj_finish")):
    for f in fn:
        if not f.endswith(".ca"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP":
            continue
        ver = u32(d, 4); base = 0x30 if ver == 0 else 0x40
        for i in range(u32(d, 0xC)):
            o = u32(d, base + 4 * i)
            if ver == 1 and not o:
                continue
            b = base + o
            if d[b:b + 4] != b"@FMC":
                continue
            blocks += 1; n00 = 0; h = b + 0x30; first = True
            for t in range(u32(d, b + 0xC)):
                ng, dist = d[h + 3], u16(d, h + 4); g = h + 6
                for _ in range(ng):
                    w = u16(d, g + 2); c = g + 4
                    for _ in range(w & 0x3F):
                        w0 = u16(d, c); cid, clen = w0 & 0x7F, w0 >> 7
                        if first:
                            first_ok += (cid == 0); first = False
                        if cid == 0:
                            n00 += 1; v = struct.unpack_from("<h", d, c + 2)[0]
                            length["endless" if v < 0 else ("1-30" if v <= 30 else "31-120" if v <= 120 else "121+")] += 1
                        elif cid == 3:
                            hold[struct.unpack_from("<h", d, c + 2)[0]] += 1
                        elif cid == 0x2C:
                            n2c += 1; fr = u16(d, c + 2)
                            anyfrom += (fr == 0xFFFF)
                            frm_bad += (fr != 0xFFFF and fr > 0xFFF)
                            cnt = struct.unpack_from("<b", d, c + 7)[0]
                            short += (clen < 8 + 2 * max(cnt, 0))
                            blend[d[c + 4]] += 1; pairs[cnt] += 1
                        if not clen:
                            break
                        c += clen
                    g += (w >> 6) or 4
                if not dist:
                    break
                h += dist
            per_block[n00] += 1
print("blocks:", blocks, "(authored-command census, .ca only: 31,942)")
print("P1  0x00 per block (count -> blocks):", sorted(per_block.items()), "; blocks whose first command is 0x00:", first_ok)
print("    0x00 length word:", sorted(length.items()))
print("    0x03 hold word (value -> commands):", sorted(hold.items(), key=lambda kv: -kv[1])[:8])
print("0x2C commands:", n2c, "; with 'from' = 0xFFFF (any):", anyfrom)
print("P2  0x2C 'from' words that are neither 0xFFFF nor 12-bit:", frm_bad)
print("P3  0x2C commands shorter than 8 + 2 x pairs:", short)
print("    0x2C blend byte +4 (value -> commands):", sorted(blend.items(), key=lambda kv: -kv[1])[:10])
print("    0x2C pair count byte +7 (value -> commands):", sorted(pairs.items(), key=lambda kv: -kv[1])[:8])
