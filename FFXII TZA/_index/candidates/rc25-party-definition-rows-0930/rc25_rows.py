"""rc25_rows.py - RC-25 residue: which definitionRowIndex (BattleStatsRecord +0x04) values the party stats records carry,
and so which char_silhouette blocks the menu can show. ORACLE, 2026-09-30. Static, shipping image.

Chain (each link asserted from the image bytes):
  L1  BattleStats_InitializeDefinitionRecord 0023AC80(rec, id): memset 0x1C8, then word [rec+4] = id (0023AD8E);
      id low byte = row, high byte = table (0 -> 02EBF130 party table, 1 -> 02EBF120 enemy table).
  L2  its three callers: 00237E26 (in 00237DF0) and 00239AC4 (in 00239960) loop k = 0..0x27 over
      rec = [02EBF190] + 8 + k*0x1C8 with id = k (cmp k, 0xFF / cmovne never selects 0xFFFF for k < 0x28) - the
      class-0 party records; 0023A7A9 (in 0023A570) initialises a SpawnRecord's embedded record, not a party record.
  L3  the published BattleStatsRecord access census (08-Combat-Formula/Battle-Stats-Record/battle-stats-record-accesses.tsv)
      lists exactly one write to +0x04: 0023AD8E. Re-read here: its w/rw rows at disp 0x0..0x5.
  L4  the menu member id word +0x60 = byte [stats + 4] (00329220: 0032946C/00329471), the stats record being
      00320040's resolution of party slot map 3 (0031B9F0 -> row <= 0x27, else none; 00320058 cmp al, 0x27).
  L5  the silhouette: 002CEE00 takes ch = +0x60 and drops ids > 5 (unsigned); 002CEFD0 shows block T[ch],
      T = {0,1,3,2,4,5}; the menu's main-member rule counts id <= 5 and not guest (002833B5..002833D2).
  L6  the party table (battle_pack.bin +0x44, 40 rows) row names are published (battle-record-kind-byte.md AL-2):
      rows 0-5 Vaan, Ashe, Fran, Balthier, Basch, Penelo; 6-16 guests; 17-25 "No name"; 26 Chocobo; 27-39 Espers.
"""
import csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def ops(f):
    return {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(f)}


i0 = ops(0x0023AC80)
check(i0.get(0x0023AC9E) == ("mov", "r15d, edx") and i0.get(0x0023ACA1) == ("sar", "eax, 8") and i0.get(0x0023ACAA) == ("movzx", "esi, dl")
      and i0.get(0x0023AD8E) == ("mov", "word ptr [rdi + 4], r15w") and i0.get(0x0023AD41) == ("mov", "rax, qword ptr [rip + 0x2c843e8]"),
      "L1 0023AC80 stores the whole id word at +4 (row = low byte, table = high byte; table 0 reads 02EBF130)")
calls = sorted((a, img.owner(a)) for a, _k in img.calls_to(0x0023AC80))
check(calls == [(0x00237E26, 0x00237DF0), (0x00239AC4, 0x00239960), (0x0023A7A9, 0x0023A570)], "L2a three call sites %s" %
      ["%08X in %08X" % c for c in calls])
for f, cmpa, ima in ((0x00237DF0, 0x00237E2D, 0x00237E11), (0x00239960, 0x00239ACB, 0x00239AAF)):
    o = ops(f)
    check(o.get(cmpa) == ("cmp", "ebx, 0x28") and o.get(ima, ("", ""))[1].endswith(", 0x1c8")
          and any(v == ("cmovne", "edx, ebx") for v in o.values()),
          "L2b %08X: loop k = 0..0x27, rec = [02EBF190] + 8 + k*0x1C8, id = k" % f)
rows = list(csv.reader(io.open(os.path.join(DB, "08-Combat-Formula", "Battle-Stats-Record", "battle-stats-record-accesses.tsv"),
                               encoding="utf-8"), delimiter="\t"))
w = [r for r in rows[1:] if r[4] in ("w", "rw") and int(r[3], 16) <= 4 < int(r[3], 16) + 8
     and ("word" in r[5] or "byte" in r[5] and r[3] == "0x4" or "dword" in r[5] and int(r[3], 16) + 4 > 4 or "qword" in r[5])]
w4 = [r for r in w if r[3] == "0x4" or ("dword" in r[5] and r[3] in ("0x1", "0x2", "0x3")) or ("qword" in r[5] and int(r[3], 16) <= 4)]
print("L3 census writes that can cover +0x04: %s" % [(r[2], r[5]) for r in w4])
check([r[2] for r in w4] == ["0023AD8E"], "L3 the stats-record census has exactly one writer of +0x04: 0023AD8E")
m = {x.address: (x.mnemonic, x.op_str) for x in img.dis(0x00320053, 0x10)}
p = ops(0x00329220)
check(m.get(0x00320058) == ("cmp", "al, 0x27") and p.get(0x0032925D) == ("mov", "word ptr [rdi + 0x60], ax")
      and p.get(0x0032946C) == ("movzx", "eax, byte ptr [r14 + 4]") and p.get(0x00329471) == ("mov", "word ptr [rdi + 0x60], ax"),
      "L4 member +0x60 = -1, then byte [stats + 4] of the party-slot-map-3 record (row <= 0x27)")
s = {x.address: (x.mnemonic, x.op_str) for x in img.dis(0x002CEE00, 0x50)}
T = list(struct.unpack("<4i", img.rd(0x00917160, 16))) + [4, 5]
check(s.get(0x002CEE21) == ("cmp", "ecx, 5") and T == [0, 1, 3, 2, 4, 5], "L5 ids > 5 show nothing; block = T[id], T = %s" % T)
NAMES = ["Vaan", "Ashe", "Fran", "Balthier", "Basch", "Penelo"]
print("\nparty record -> definitionRowIndex -> silhouette block (pages):")
for k in range(0x28):
    blk = ("block %d (pages %d-%d)" % (T[k], 0x204 * T[k], 0x204 * T[k] + 0x203)) if k <= 5 else "none (id > 5)"
    who = NAMES[k] if k < 6 else ("guest row" if k <= 16 else ("'No name'" if k <= 25 else ("Chocobo" if k == 26 else "Esper")))
    print("  record %2d  row %2d  %-10s %s" % (k, k, who, blk))
blocks = sorted(T[k] for k in range(6))
check(blocks == [0, 1, 2, 3, 4, 5], "L6 the six main-character records (rows 0-5) select all six blocks: every one of the 3,096 pages")
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
