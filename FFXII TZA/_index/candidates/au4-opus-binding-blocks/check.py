"""AU-4 (OPUS, 2026-09-26): the live binding region 01F80130..01F80C68 is three 0x420-stride blocks of three InputBindingRecords
(0x15C) each; the stated end is the last record's digital-code table, not a short third block. STATIC, from the shipping image.
 A1  the three C++ static initialisers 0015BD30 / 0015C0D0 / 0015BF20 each write their own block's three records: twelve
     16-byte rip-relative stores at +0x000..+0x030, +0x15C.., +0x2B8.. (the 64-byte digital-code table of records 0, 1, 2), and
     three `lea` of record+0x40 (block +0x040, +0x19C, +0x2F8; rax, or rcx for block 1's third) that seed a register loop copying 2 x 0x80 bytes (r8d = 2) -
     the 256-byte axis table of each record, written through rax, which a rip-relative census cannot see.
 A2  blocks at 01F80130 / 01F80550 / 01F80970 (stride 0x420 = 3 x 0x15C + 0xC); the third initialiser's last store ends at
     01F80C68 (= 01F80970 + 0x2B8 + 0x40), which is where the row's region stops.
 A3  the only rip-relative reference in 01F80C68..01F80D90 is that lea of 01F80C68 (record 2's axis table in block 3); record 2
     ends at 01F80D84 (+0x2B8 + 0x15C) and the next referenced global is 01F80D90 = 01F80970 + 0x420 (the keymap path:
     InputManager_BuildKeymapPath / InputManager_LoadKeymapIni). The record's +0x140..+0x15C tail is not written here.
Writes result.json."""
import json, os, re, sys
import capstone, pefile
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
IB = 0x120000
img = pefile.PE(EXE, fast_load=True).get_memory_mapped_image()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
rows = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    c = l.split("\t")
    try:
        rows[int(c[0], 16)] = (c[1], int(c[2]))
    except (ValueError, IndexError):
        pass
R = {"blocks": {}}
for f, base in ((0x15BD30, 0x1F80130), (0x15C0D0, 0x1F80550), (0x15BF20, 0x1F80970)):
    offs, leas, loop = [], [], []
    for i in md.disasm(img[f - IB:f - IB + rows[f][1]], f):
        m = re.search(r"(\w+) ptr \[rip \+ (0x[0-9a-f]+)\], ", i.op_str)
        if m and i.mnemonic.startswith("mov"):
            offs.append((i.address + i.size + int(m.group(2), 16) - base, m.group(1)))
        m2 = re.match(r"r[a-z0-9]+, \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
        if i.mnemonic == "lea" and m2:
            t = i.address + i.size + int(m2.group(1), 16)
            if base <= t < base + 0x420:
                leas.append(t - base)
        if (i.mnemonic, i.op_str) in (("mov", "r8d, 2"), ("lea", "rax, [rax + 0x80]"), ("sub", "r8, 1")):
            loop.append("%s %s" % (i.mnemonic, i.op_str))
    R["blocks"]["%08X" % base] = {"init": "%08X" % f, "stores": ["+%03X %s" % o for o in offs], "axis_leas": ["+%03X" % x for x in leas],
                                  "loop": loop}
refs = {}
for a, (nm, sz) in rows.items():
    if not 0x121000 <= a < 0x8C0000:
        continue
    for i in md.disasm(img[a - IB:a - IB + sz], a):
        m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", i.op_str)
        if m:
            t = i.address + i.size + int(m.group(1), 16)
            if 0x1F80C68 <= t < 0x1F80DA0:
                refs.setdefault("%08X" % t, set()).add("%08X %s" % (a, nm[:32]))
R["refs_1F80C68_1F80DA0"] = {k: sorted(v) for k, v in sorted(refs.items())}
want = ["+000 xmmword", "+010 xmmword", "+020 xmmword", "+030 xmmword", "+15C xmmword", "+16C xmmword", "+17C xmmword", "+18C xmmword",
        "+2B8 xmmword", "+2C8 xmmword", "+2D8 xmmword", "+2E8 xmmword"]
cases = {
    "A1_each_initialiser_writes_three_records_codes_and_axis_tables": all(b["stores"] == want and b["axis_leas"] == ["+040", "+19C", "+2F8"]
        for b in R["blocks"].values()) and "mov r8d, 2" in R["blocks"]["01F80970"]["loop"] and "sub r8, 1" in R["blocks"]["01F80970"]["loop"],
    "A2_stride_0x420_and_the_stated_end_is_record_2s_table": 0x1F80550 - 0x1F80130 == 0x420 and 0x1F80970 - 0x1F80550 == 0x420
        and 0x420 == 3 * 0x15C + 0xC and 0x1F80970 + 0x2B8 + 0x40 == 0x1F80C68,
    "A3_next_global_is_block3_plus_0x420": sorted(R["refs_1F80C68_1F80DA0"]) == ["01F80C68", "01F80D90"]
        and R["refs_1F80C68_1F80DA0"]["01F80C68"] == ["0015BF20 FUN_0015bf20"] and 0x1F80970 + 0x2B8 + 0x15C == 0x1F80D84
        and any("InputManager_BuildKeymapPath" in s for s in R["refs_1F80C68_1F80DA0"]["01F80D90"]),
}
res = {"evidence_class": "STATIC", "live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-58s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
