"""ashd_lzss_sweep.py - FABLE (Claude Opus 5.5), 2026-09-27, for the non-author review of OPUS's proposed NAS on UQ-70's
ashd residue. DATA: tries 120 stock LZSS configurations (3 stream starts x 2 flag-bit orders x 2 literal polarities x
5 reference encodings x 2 minimum lengths) on katano/event.bin and reports how close each output comes to the header's
0x2509. 96 stop at an out-of-range back-reference; the 24 that run to the end miss by 1,454 bytes or more, so the stream is not a stock LZSS - which says the scheme is bespoke, not that
it cannot be recovered. Skips without the local extract; exit 0 either way (a measurement, not a gate)."""
import itertools
import os, sys
P = r"D:/FFXII_TZA_extract/ps2data/image/ff12/katano/event.bin"
if not os.path.exists(P): print("SKIP no extract"); sys.exit(0)
b = open(P, "rb").read()
TARGET = 0x2509

def lzss(data, start, msb, lit_is_one, refkind, minlen, init=0x00):
    out = bytearray(); i = start; ring = bytearray([init]) * 4096; r = 0xFEE
    try:
        while i < len(data) and len(out) < TARGET * 2:
            flags = data[i]; i += 1
            for k in range(8):
                bit = (flags >> (7 - k)) & 1 if msb else (flags >> k) & 1
                if i >= len(data): break
                if bit == lit_is_one:
                    c = data[i]; i += 1; out.append(c); ring[r] = c; r = (r + 1) & 0xFFF
                else:
                    b1, b2 = data[i], data[i + 1]; i += 2
                    if refkind == "okumura":
                        pos = b1 | ((b2 & 0xF0) << 4); ln = (b2 & 0x0F) + minlen
                        for j in range(ln):
                            c = ring[(pos + j) & 0xFFF]; out.append(c); ring[r] = c; r = (r + 1) & 0xFFF
                    else:
                        if refkind == "hi12": dist = ((b1 << 4) | (b2 >> 4)) + 1; ln = (b2 & 0xF) + minlen
                        elif refkind == "lo12": dist = (((b2 & 0xF0) << 4) | b1) + 1; ln = (b2 & 0xF) + minlen
                        elif refkind == "be_len_hi": dist = (((b1 & 0x0F) << 8) | b2) + 1; ln = (b1 >> 4) + minlen
                        elif refkind == "le_len_hi": dist = (((b2 & 0x0F) << 8) | b1) + 1; ln = (b2 >> 4) + minlen
                        if dist > len(out): return None
                        for j in range(ln):
                            c = out[-dist]; out.append(c); ring[r] = c; r = (r + 1) & 0xFFF
        return bytes(out)
    except IndexError:
        return bytes(out)

res = []
for start, msb, lit, kind, ml in itertools.product((0x0C, 0x08, 0x10), (False, True), (0, 1), ("okumura", "hi12", "lo12", "be_len_hi", "le_len_hi"), (2, 3)):
    o = lzss(b, start, msb, lit, kind, ml)
    if not o: continue
    pr = sum(32 <= c < 127 for c in o) / max(1, len(o))
    res.append((abs(len(o) - TARGET), start, msb, lit, kind, ml, len(o), round(pr, 3), o[:48]))
res.sort()
for r in res[:5]: print(r[:8])
print("configurations tried 120, ran to the end", len(res), "best miss", res[0][0], "bytes; within 256:", sum(r[0] <= 256 for r in res))
