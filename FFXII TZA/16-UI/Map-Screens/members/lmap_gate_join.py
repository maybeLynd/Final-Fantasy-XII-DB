"""Checked join: do the persistent gate ids in menumap_location.bin's point entries appear among the ids the
shipped scripts pass to the map-jump-group flag verbs?

Layout (lmap page section 10, native offsets): header byte +9 = record count, word[+0xA + 2*i] = record offset;
record = {u8 countA, u8 countB, u8 countC, u8 ?} then countA + countB 24-byte point entries. A point's persistent
gate words are +0xE, +0x12, +0x14 (0xFFFF or 0 = none); +0x16 is an encoded id and is not a flag.
Control: the totals must reproduce the page's 384 A entries and 111 B entries.
"""
import struct, sys, collections

LMAP = r"D:\FFXII_TZA_extract\ps2data\image\ff12\myoshiok\us\worldmap\menumap_location.bin"
TSV = sys.argv[1]
b = open(LMAP, "rb").read()
nrec = b[9]
script_ids = {}
for line in open(TSV, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 6 and p[0].startswith("0x"):
        script_ids[int(p[0], 16)] = p
totA = totB = 0
gates = collections.Counter()
where = collections.defaultdict(list)
for i in range(nrec):
    ro = struct.unpack_from("<H", b, 0xA + 2 * i)[0]
    cA, cB = b[ro], b[ro + 1]
    totA += cA
    totB += cB
    for k in range(cA + cB):
        e = ro + 4 + 24 * k
        for fo in (0xE, 0x12, 0x14):
            g = struct.unpack_from("<H", b, e + fo)[0]
            if g not in (0, 0xFFFF):
                gates[g] += 1
                where[g].append((i, "A" if k < cA else "B", fo))
print("# records %d; A entries %d, B entries %d (page: 384 and 111)" % (nrec, totA, totB))
flagish = sorted(g for g in gates if g < 0x4000)
thr = sorted(g for g in gates if g >= 0x4000)
hit = [g for g in flagish if g in script_ids]
print("# distinct persistent gate ids %d (plain %d, threshold-form %d); plain ids also flipped or tested by a script: %d of %d"
      % (len(gates), len(flagish), len(thr), len(hit), len(flagish)))
print("# plain gate ids no script names: " + " ".join("0x%X" % g for g in flagish if g not in script_ids))
print("gate_id\tuses_in_map_data\tfields\tscript_set\tscript_release\tscript_is\tpreset")
for g in flagish + thr:
    p = script_ids.get(g)
    fields = ",".join(sorted({"+0x%X" % w[2] for w in where[g]}))
    print("0x%X\t%d\t%s\t%s\t%s\t%s\t%s" % (g, gates[g], fields, p[2] if p else "-", p[3] if p else "-", p[4] if p else "-",
                                          (p[1] or "no") if p else "-"))
