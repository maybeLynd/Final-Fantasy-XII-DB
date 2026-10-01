"""sn1_q3_pagemap.py - SN-1: what the .dbg q3 table holds (FABLE, Claude Opus 5.5, 2026-09-28). DATA from the archive.

q3 is {u32 X; u32 map[E]; zero pad to the next table}. map[k] is the index of the last instruction that starts before
byte 32k of the scope's code: -1 (0xFFFFFFFF) for k = 0, then one entry per 32-byte boundary strictly inside the code,
so E = 1 + floor((q0len - 1) / 32). It is the byte -> instruction page map, the inverse of q2 (q2 = {count;
byte offset of instruction 32j}). The instruction starts come from q0's flag byte, which DATA verified against the
opcode length table bit for bit.

  M1 every scope's map equals that formula, and every word after it up to the next table is zero (all 50 scopes)
  M2 q2, read the same way, is {ceil(instructions / 32); byte offset of instruction 32j} (the mirror, all 50)
  X  the head word X is reported, not explained: btlctrl scopes 18 and 19 carry byte-identical maps {-1, 0x0B} and
     X = 1 and 2, so X is not a count over the map. It is about half of E (the ratio is printed)
  C  controls: the formula without the -1 (instructions before byte 32k) matches no scope's map; the old two-list reading
     (listA = the first X words after the -1) needs a pad zero inside listA on exactly the scopes where X > E - 1 -
     the published "btlctrl sc19 exception" and two more - so its exceptions are this padding, predicted

Usage: python sn1_q3_pagemap.py [dir]
"""
import bisect, os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
scopes = []
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        q0, q1, q2, q3 = offs[4 * i:4 * i + 4]; end = offs[4 * i + 4] if i < ns - 1 else o0
        n0 = (q1 - q0) // 4
        starts = [k for k in range(n0) if b[q0 + 4 * k + 3] == 1]
        w3 = list(struct.unpack_from("<%dI" % ((end - q3) // 4), b, q3))
        w2 = list(struct.unpack_from("<%dI" % ((q3 - q2) // 4), b, q2))
        scopes.append((m, i, n0, starts, w2, w3))
m1 = []; m2 = []; ratios = []; shifted = 0; pad_in_listA = []
for m, i, n0, starts, w2, w3 in scopes:
    E = 1 + (n0 - 1) // 32
    want = [(bisect.bisect_left(starts, 32 * k) - 1) & 0xFFFFFFFF for k in range(E)]
    X, body = w3[0], w3[1:]
    ok = body[:E] == want and not any(body[E:])
    if not ok: m1.append((m, i))
    alt = [bisect.bisect_left(starts, 32 * k) for k in range(E)]
    shifted += body[:E] == alt
    ic = len(starts)
    if w2 != [(ic + 31) // 32] + [starts[32 * j] for j in range((ic + 31) // 32)][:len(w2) - 1] or len(w2) - 1 != (ic + 31) // 32:
        m2.append((m, i))
    ratios.append(X / E)
    if X > E - 1: pad_in_listA.append("%s sc%d (X %d, entries %d)" % (m, i, X, E - 1))
check("M1", not m1 and len(scopes) == 50, "%d scopes; map = last instruction before byte 32k, rest zero; mismatches %s" % (len(scopes), m1))
check("M2", not m2, "q2 = {ceil(instructions/32); byte of instruction 32j}; mismatches %s" % m2)
s18 = [s for s in scopes if s[:2] == ("btlctrl", 18)][0]; s19 = [s for s in scopes if s[:2] == ("btlctrl", 19)][0]
check("X", s18[5][1:] == s19[5][1:] and (s18[5][0], s19[5][0]) == (1, 2),
      "btlctrl sc18 / sc19 maps identical %s, X = %d / %d; X / E over 50 scopes %.2f..%.2f"
      % ([hex(v) for v in s18[5][1:3]], s18[5][0], s19[5][0], min(ratios), max(ratios)))
check("C", shifted == 0 and len(pad_in_listA) == 3 and any("btlctrl sc19" in p for p in pad_in_listA),
      "formula without the -1 matches %d scopes; old listA reading pulls a pad zero into listA on %s" % (shifted, pad_in_listA))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
