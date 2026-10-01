"""eq_slot5_census.py - does any shipped ENEMY order record author the equipment-slot selector (0x1A occupied / 0x1B
empty, AiOrder_EvaluateTargetSelector 00301AD0: switch byte = entry +3 at 00301B14 / 00301EA3, slot N = entry +2 at
00301B1A, bound cmp edi,5 at 00302416) with N = 5?

Corpus: the 166 `in` .ard files. Slot 1 (file +0x14) = order-set directory: u16 count, u16 100, u32 offset[count+1]
(section-relative). Order set: u8[12] per-subgroup counts, u8[20] zero, then 24-byte records. Record: three 6-byte
selector entries at +6/+0xC/+0x12, {u16 first word (0 = empty, skipped at 00301685), u8 operand, u8 selector, s16}.
Controls: 1,422 sets and 50,050 records (the loader page, section 7a); first-entry first-word histogram must give 18,206
records with value 1 (gambit page, Z-15B)."""
import glob, os, struct, collections

files = sorted(glob.glob(r"D:/FFXII_TZA_extract/ps2data/plan_master/in/plan_map/*/area/*.ard"))
sets = recs = 0
first = collections.Counter()
sel = collections.Counter()           # (selector, operand) over non-empty entries with selector 0x1A/0x1B
where5 = []
for f in files:
    b = open(f, "rb").read()
    s1 = struct.unpack_from("<I", b, 0x14)[0]
    cnt = struct.unpack_from("<H", b, s1)[0]
    offs = struct.unpack_from("<%dI" % (cnt + 1), b, s1 + 4)
    for i in range(cnt):
        o = s1 + offs[i]
        n = sum(b[o:o + 12])
        sets += 1
        for r in range(n):
            ro = o + 0x20 + 24 * r
            recs += 1
            for e in range(3):
                eo = ro + 6 + 6 * e
                w0, opnd, selr = struct.unpack_from("<HBB", b, eo)
                if e == 0:
                    first[w0] += 1
                if w0 == 0:
                    continue
                if selr in (0x1A, 0x1B):
                    sel[(selr, opnd)] += 1
                    if opnd == 5:
                        where5.append((os.path.basename(f), i, r, e))
print("files", len(files), "sets", sets, "records", recs)
print("control: first-entry first word == 1:", first[1], " == 0:", first[0])
print("selector 0x1A/0x1B entries (non-empty) by (selector, slot operand):", sorted(sel.items()))
print("entries with slot operand 5:", len(where5), where5[:10])
