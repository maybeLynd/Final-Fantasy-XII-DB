"""sd101_indep.py - SWE2-AUDIT-SPEC's independent check of SD-101 (2026-09-30).
1. Every write shape of widget +0x40 bit 24 (any width at +0x40..+0x43, bts/btr, register read-modify-write), over every
   listed function and unlisted .pdata range (../auditspec-review-sd4-0930/bitsweep.py).
2. Raw E8/E9/0F8x rel32 references to 00247730 over ALL .text bytes, each verified by decoding at the site, classed by
   the edx/rdx/dl value set in the 10 instructions before the site.
Control C: the sweep finds the author's five setters and the subtree setter's own clear 0024773A (a sweep blind to the
bit would miss them).
"""
import os, re, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd4-0930"))
import bitsweep as BS  # noqa: E402
tk = BS.tk

hits = BS.sweep(0x40, 24)
print("sweep: ranges %d, hits %d" % (len(BS.ranges()), len(hits)))
for h in sorted(hits):
    if h[4] != "clear" or h[2] != "M":
        print("  %08X %08X %-2s %-58s %s" % h)
ncl = sum(1 for h in hits if h[4] == "clear" and h[2] == "M")
print("  (+ %d memory-form clears not listed)" % ncl)
addrs = {h[1] for h in hits}
want = {0x005728E6, 0x00573AF5, 0x00247754, 0x0057390E, 0x00573952, 0x0024773A}
print("%s  C the author's five setters and 0024773A are found" % ("PASS" if want <= addrs else "FAIL: missing %s" % sorted("%08X" % a for a in want - addrs)))

# raw rel32 references to 00247730
T = 0x00247730
TVA, TVS, TRS, TRO = tk.TVA, tk.TVS, tk.TRS, tk.TRO
text = tk.d[TRO:TRO + TRS]
sites = []
for p in range(len(text) - 5):
    b = text[p]
    if b in (0xE8, 0xE9):
        L, rel = 5, struct.unpack_from("<i", text, p + 1)[0]
    elif b == 0x0F and 0x80 <= text[p + 1] <= 0x8F and p + 6 <= len(text):
        L, rel = 6, struct.unpack_from("<i", text, p + 2)[0]
    else:
        continue
    a = TVA + p
    if a + L + rel != T:
        continue
    x = tk._decode_at(a)
    if x is None or x.size != L:
        continue
    sites.append((a, x.mnemonic))
kinds = collections.Counter()
rows = []
for a, mn in sites:
    o, how = tk.owner(a)
    if o == T:
        rows.append((a, mn, "self", tk.fname(a))); continue
    n = tk.fsize(o) if how == "listed" else next(e - b for b, e in tk.pdata if b == o)
    xs = [x for x in tk.dis(o, o + n) if x.address < a][-10:]
    e = next(("%s %s" % (x.mnemonic, x.op_str) for x in reversed(xs) if re.match(r"(edx|rdx|dl)\b", x.op_str)), "?")
    k = "1" if e == "mov edx, 1" else "0" if e == "xor edx, edx" else "var"
    kinds[k] += 1
    rows.append((a, mn, k, tk.fname(a)))
print("raw rel32 references to 00247730: %d (%s)" % (len(sites), dict(collections.Counter(m for _, m in sites))))
for r in sorted(rows):
    print("  %08X %-4s %-4s %s" % r)
print("outside callers by edx: %s" % dict(kinds))
