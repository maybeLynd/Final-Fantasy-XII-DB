"""S-04: classes 3, 4, 11 and 12 over real data, and I6's text pointers (OPUS, 2026-09-26) - the two items AUDIT-SEM's S-04 cell
still names. Over block 328's world, imported through i1_i6.py (block 328's four cases and i1_i6's five run first, unchanged).

CORRECTION TO MY OWN EARLIER TEXT: i1_i6's README said I6's text pointers were not covered because "the text banks behind 02EBF170
are not bound in this world". That was wrong: 00236C30 binds 02EBF170 itself (00236FD6: 003846F0(02EBF170, dir+0xF8, 1)), and
block 328 re-makes that call. The text half of I6 is executed here.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED += the static closure of the area binder
003EA710. Data bound by shipped code only:
 - the shipped area file ps2data/plan_master/in/plan_map/rsn_b/area/rsn_b.ard, bound by the game's own binder 003EA710 (as
   block 343 binds it) - this is what fills the class-3 and class-4 slots 02EBF120 / 02EBF150;
 - the gambit table slot 02EBF0D8 (class 11), bound by 00238880's FIRST call, 003845F0(02EBF0D8, dir entry) with the entry
   00236C30 passes it - the call block 328 skipped because the rest of 00238880 allocates from heap 6 (the same treatment block
   328 gives 00237FC0's first call).
Cases:
 T   I6's text pointers: for classes 2, 8, 9, 13, 17, 18, 20, 21, 24..29 the fill's +0x18 points INSIDE the relocated battle_pack
     (resolved storage, not a copy in the record). Observed, not asserted: the storage is shared - class 25 ids 0 and 1
     return the SAME pointer, and class 8 id 0x3000 and class 20 id 0 point at the same bytes.
 C3  class 3 over the area table [02EBF120]: the validator accepts exactly 0 .. count-1 (probed at -1, 0, count-1, count).
 C4  class 4 over [02EBF150]: the same.
 C11 class 11 over the bound gambit table: the validator accepts exactly 0x6000 .. 0x6000+count-1.
 C12 class 12: its slot 02EBF0D0 has exactly one reference in .text (the validator's own read) and no copy as data - nothing in
     the image binds it; the validator therefore refuses every class-12 id over the image's null (0x7000, 0x7001 probed), and
     the fill returns -2 without a lane read (I1).
Writes c3_4_11_12_text_result.json.
"""
import json
import os
import struct

import i1_i6 as T

HERE = os.path.dirname(os.path.abspath(__file__))
C, W, uc, S = T.C, T.W, T.uc, T.S
BINDER, VALIDATE = 0x3EA710, 0x322C50
W.ALLOWED |= W.closure(BINDER) | {BINDER}
ARD = open(r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard", "rb").read()
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]


def valid(cls, v):
    S.call(VALIDATE, cls, v)
    return uc.reg_read(T.UC_X86_REG_RAX) & 0xFFFFFFFF


# ---- T ----
text = {}
PACK_LO, PACK_HI = C.B, C.B + len(C.pack)
for cls, ids in ((2, (0, 5)), (8, (0x3000, 0x3001)), (9, (0x4000, 0x4001)), (13, (0x8000, 0x8001)), (17, (0xC000, 0xC001)),
                 (18, (0xD000, 0xD001)), (20, (0, 1)), (21, (0, 1)), (24, (0, 1)), (25, (0, 1)), (26, (0, 1)), (27, (0, 1)),
                 (28, (0, 1)), (29, (0, 1))):
    fn, rec = (T.WWORD, T.REC_W) if cls in T.WORD_CLASSES else (T.WDWORD, T.REC_D)
    ps = []
    for v in ids:
        ok = S.call(fn, cls, v)
        ps.append((ok, q(rec + 0x18)))
    text[cls] = {"ok": all(p[0] for p in ps), "p18": ["%X" % p[1] for p in ps],
                 "inside_pack": all(PACK_LO <= p[1] < PACK_HI for p in ps), "distinct": ps[0][1] != ps[1][1],
                 "not_in_record": all(not (rec <= p[1] < rec + 0x98) for p in ps),
                 "bytes_at_first": bytes(uc.mem_read(ps[0][1], 12)).hex() if ps[0][1] else None}
case_t = all(v["ok"] and v["inside_pack"] and v["not_in_record"] for v in text.values())
shared = sorted({p for v in text.values() for p in v["p18"] if sum(p in w["p18"] for w in text.values()) > 1 or v["p18"].count(p) > 1})

# ---- C11: the gambit slot, 00238880's first call ----
gcall = [c for c in C.calls if c[0] == 0x238880]
dirent = gcall[0][2] if gcall else None
okb = S.call(C.BIND, 0x2EBF0D8, C.d(dirent)) if dirent is not None else False
g_tab = q(0x2EBF0D8)
g_cnt = d4(g_tab + 4) if g_tab else 0
c11 = {"bound": okb, "dirent": "%X" % dirent if dirent is not None else None, "table": "%X" % g_tab, "count": g_cnt}
if g_cnt:
    c11["edges"] = {"%X" % v: valid(11, v) for v in (0x5FFF, 0x6000, 0x6000 + g_cnt - 1, 0x6000 + g_cnt)}
case_c11 = okb and g_cnt > 0 and [c11["edges"][k] != 0 for k in c11["edges"]] == [False, True, True, False]

# ---- C3 / C4: the shipped area file, bound by its own binder ----
REGION = 0x76C00000
uc.mem_map(REGION, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(REGION + 0x1000, ARD)
oka = S.call(BINDER, REGION + 0x1000)
area = {}
for cls, slot in ((3, 0x2EBF120), (4, 0x2EBF150)):
    tab = q(slot)
    cnt = d4(tab + 4) if tab else 0
    edges = {"%X" % (v & 0xFFFFFFFF): valid(cls, v & 0xFFFFFFFF) for v in (-1, 0, cnt - 1, cnt)} if cnt else {}
    area[cls] = {"table": "%X" % tab, "count": cnt, "edges": edges}
edge_ok = lambda e: [x != 0 for x in e.values()] == [False, True, True, False]
case_c3 = oka and area[3]["count"] > 0 and edge_ok(area[3]["edges"])
case_c4 = oka and area[4]["count"] > 0 and edge_ok(area[4]["edges"])

# ---- C12: no writer in the image ----
raw = W.raw
slot12 = 0x2EBF0D0
data_copies = sum(raw.count(p) for p in (struct.pack("<Q", slot12), struct.pack("<I", slot12), struct.pack("<I", slot12 - 0x120000)))
refs = []
pe = struct.unpack_from("<I", raw, 0x3C)[0]
n, o = struct.unpack_from("<H", raw, pe + 6)[0], struct.unpack_from("<H", raw, pe + 20)[0]
off = pe + 24 + o
for _ in range(n):
    nm = raw[off:off + 8].rstrip(b"\0")
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    off += 40
    if nm != b".text":
        continue
    base, data = va + 0x120000, raw[ra:ra + rs]
    for i in range(len(data) - 7):
        if data[i] in (0x48, 0x4C) and (data[i + 2] & 0xC7) == 0x05:
            if base + i + 7 + struct.unpack_from("<i", data, i + 3)[0] == slot12:
                refs.append("%08X" % (base + i))
c12 = {"slot_value": "%X" % q(slot12), "text_refs": refs, "data_copies": data_copies,
       "validator": {"%X" % v: valid(12, v) for v in (0x7000, 0x7001)}, "fill": T.fill(12)}
case_c12 = q(slot12) == 0 and len(refs) == 1 and data_copies == 0 and all(v == 0 for v in c12["validator"].values()) \
    and c12["fill"]["ret"] == 0xFFFFFFFE and c12["fill"]["lane_reads"] == 0

cases = {"T_I6_text_pointers_resolve_into_the_bound_pack": case_t, "C3_class3_over_the_shipped_area_table": case_c3,
         "C4_class4_over_the_shipped_area_table": case_c4, "C11_class11_over_the_bound_gambit_table": case_c11,
         "C12_class12_slot_has_no_writer_in_the_image": case_c12}
res = {"ok": all(cases.values()), "cases": cases, "shared_text_pointers": shared, "text": {str(k): v for k, v in text.items()}, "area_bound": oka, "area": {str(k): v for k, v in area.items()},
       "class11": c11, "class12": c12, "pack": ["%X" % PACK_LO, "%X" % PACK_HI]}
json.dump(res, open(os.path.join(HERE, "c3_4_11_12_text_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-52s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps({"area": res["area"], "c11": c11, "c12": {k: v for k, v in c12.items() if k != "fill"}})[:1400])
