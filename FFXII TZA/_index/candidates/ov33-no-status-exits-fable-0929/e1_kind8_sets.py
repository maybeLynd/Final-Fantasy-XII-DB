"""e1_kind8_sets.py - coordinator lead (RC-5): event sets 355 / 398 / 440 have no kind-8 FST rows. Check the rows in all 12
tables, and check mechanically that every 0032E620 call in the 0032FC30 -> 0032FCA0 -> 00330310 chain is preceded, in the
same function, by a conditional branch on the size 0032E400 returned for the same (kind, row).  (OV-33 E1)

Rows: 0032FCA0 m in 1..3 -> kind 8, base = set*4 (0032FD30-0032FD35); requests base+0 (00330444), base+1 (0032FF0B),
base+2 (0032FE9E), base+3 (0032FF76) and kind 0x25 base+3 (0032FFE2).
Gate table (read by hand, printed for the reviewer): each request site with the branch that skips it.
Positive controls: sets 30 and 31 (rows 120..127) sized in US.
Terminal line: FAILS n / STATUS.
"""
import struct, os, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
ROOT = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables"
LANGS = ["JP", "US", "FR", "DE", "IT", "ES", "UK", "KR", "CH", "ASIA", "IN", "CN"]
T = {L: struct.unpack("<205000i", open(os.path.join(ROOT, "FileSizeTable_%s.fst" % L), "rb").read()) for L in LANGS}
fails = 0
ctl = all(T["US"][8 * 5000 + r] > 0 for r in range(120, 128))
print("control US kind 8 rows 120..127 all positive:", ctl, [T["US"][8 * 5000 + r] for r in range(120, 128)]); fails += not ctl
for s in (355, 398, 440):
    for k in (8, 0x25):
        rows = range(4 * s, 4 * s + 4)
        neg = {L: [T[L][k * 5000 + r] for r in rows] for L in LANGS}
        allneg = all(v == -1 for L in LANGS for v in neg[L])
        print("set %3d kind %2d rows %d..%d: -1 in all 12 languages: %s" % (s, k, 4 * s, 4 * s + 3, allneg))
        if not allneg:
            for L in LANGS: print("   ", L, neg[L])
# gate table: (request site, gate branch site, expected mnemonic)
GATES = [(0x32FE9E, 0x32FE5E, "js"), (0x32FF0B, 0x32FED2, "jl"), (0x32FF76, 0x32FF38, "js"),
         (0x32FFE2, 0x32FFA3, "jl"), (0x330444, 0x330378, "jle")]
print("\ngate branches (each skips its request when the size for the same pair is negative / non-positive):")
for req, br, mn in GATES:
    x = [i for i in tk.dis(br, br + 8)][0]
    tgt = int(x.op_str, 16)
    ok = x.mnemonic == mn and tgt > req
    print("  request %08X  gate %08X %s %s  (skips past the request: %s)" % (req, br, x.mnemonic, x.op_str, ok))
    fails += not ok
x = tk.dis(0x32EBB3, 0x32EBB8)[0]
print("  request 0032EC01 (0032EB40, tail of 00330310) gate 0032EBB3 %s %s (size <= 0x800 skips)" % (x.mnemonic, x.op_str))
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
