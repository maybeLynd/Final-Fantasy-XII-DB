# section012_ordinal_test.py (FABLE, Claude Opus 5.5, 2026-09-25) - UQ-333: are the C / N / S ids (and the lowercase n ids
# 0-8) ordinals into the script's own entry list? Tests each id against its container's section_000 entry count.
import os, sys, struct, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
f = open(r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf", "rb")
names, blocks = V.load_index(f)
stat = collections.defaultdict(lambda: [0, 0, 0])   # letter -> [ids, ids < entrycount, containers]
ex = collections.defaultdict(list)
for path in sorted(p for p in names if p.lower().endswith(".ebp") and "/us/" in p.lower()):
    b = V.read_entry(f, names, blocks, path)
    if len(b) < 0x80 or b[:4] != b"EBP2":
        continue
    s12 = U32(b, 0x40)
    s0 = U32(b, 0x10)
    if not s12 or not s0:
        continue
    sec = b[s0:]
    diroff = U32(sec, 0x18)
    ecount = U32(sec, diroff)
    per = collections.defaultdict(list)
    for k in range(U32(b, s12)):
        per[chr(U16(b, s12 + 6 + 4 * k))].append(U16(b, s12 + 4 + 4 * k))
    for L, vals in per.items():
        if L in "CNS" or L == "n":
            use = [v for v in vals if L != "n" or v <= 8]
            if not use:
                continue
            st = stat[L]
            st[0] += len(use); st[1] += sum(1 for v in use if v < ecount); st[2] += 1
            if any(v >= ecount for v in use) and len(ex[L]) < 5:
                ex[L].append((path.split("/")[-1], ecount, sorted(use)[-3:]))
for L, (n, ok, c) in sorted(stat.items()):
    print("%s: ids %d in %d containers; below the container's entry count: %d (%.1f%%)" % (L, n, c, ok, 100.0 * ok / n))
    if ex[L]:
        print("   counter-examples:", ex[L])
