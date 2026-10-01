"""e1_fst_census.py - per-kind census of the shipped FileSizeTables (OV-33 E1).

Reads all 12 install tables (D:/SteamLibrary/.../FileSizeTables), 41 x 5000 u32.
Per language and kind: count of -1 entries, count of sized entries, count of zero entries, count of negative
entries other than -1, and the max sized id. Also prints, for the US table, the explicit sized-id ranges of
chosen kinds used by the producer census (see README).
Positive controls: dword 0 == 57 (system.cnf); US has 10,521 sized entries and 31 populated kinds (page §9).
Terminal line: FAILS n / STATUS.
"""
import struct, os, sys, hashlib
ROOT = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables"
LANGS = ["JP", "US", "FR", "DE", "IT", "ES", "UK", "KR", "CH", "ASIA", "IN", "CN"]  # 01E88B00 order
fails = 0
T = {}
for L in LANGS:
    b = open(os.path.join(ROOT, "FileSizeTable_%s.fst" % L), "rb").read()
    if len(b) != 820000: print("BAD SIZE", L, len(b)); fails += 1; continue
    T[L] = struct.unpack("<205000i", b)
    print("%-4s sha256 %s" % (L, hashlib.sha256(b).hexdigest()))
us = T["US"]
print("control dword0 == 57:", us[0] == 57); fails += us[0] != 57
sized = sum(1 for v in us if v != -1)
kinds = sum(1 for k in range(41) if any(us[k * 5000 + i] != -1 for i in range(5000)))
print("control US sized entries == 10521:", sized, sized == 10521); fails += sized != 10521
print("control US populated kinds == 31:", kinds, kinds == 31); fails += kinds != 31
print()
print("kind | per language: sized/-1/zero/otherneg/maxid")
for k in range(41):
    row = []
    for L in LANGS:
        r = T[L][k * 5000:(k + 1) * 5000]
        s = [i for i, v in enumerate(r) if v != -1]
        m1 = sum(1 for v in r if v == -1)
        z = sum(1 for v in r if v == 0)
        on = sum(1 for v in r if v < 0 and v != -1)
        row.append("%s:%d/%d/%d/%d/%s" % (L, len(s), m1, z, on, max(s) if s else "-"))
    print("k%02d " % k + " ".join(row))
# totals of anomalous values over all languages
allz = sum(1 for L in LANGS for v in T[L] if v == 0)
alln = sum(1 for L in LANGS for v in T[L] if v < 0 and v != -1)
print("all languages: zero entries %d, negative-not--1 entries %d" % (allz, alln))
# kinds entirely -1 in ALL languages
empty_all = [k for k in range(41) if all(T[L][k * 5000 + i] == -1 for L in LANGS for i in range(5000))]
print("kinds with no sized entry in any language:", empty_all)
def ranges(ids):
    out = []; s = None
    for i in ids:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return ",".join("%d" % a if a == b else "%d-%d" % (a, b) for a, b in out)
print()
print("US sized-id ranges per kind:")
for k in range(41):
    ids = [i for i in range(5000) if us[k * 5000 + i] != -1]
    if ids: print("k%02d %s" % (k, ranges(ids)))
print()
print("ids whose sized/-1 status differs between languages, per kind (union of differences):")
for k in range(41):
    diff = [i for i in range(5000) if len(set(T[L][k * 5000 + i] == -1 for L in LANGS)) > 1]
    if diff: print("k%02d %s" % (k, ranges(diff)))
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
