"""B3 test_area_ref.bin (kind 9 idx 2) and test_map_ref.bin (kind 9 idx 1) against their sibling map_ref.bin (MRF).
Claims: test_area_ref = u16[321], strictly ascending; entry k == index of the first map_ref field row whose word +4
(the value MapRef_GetAreaArdFieldResourceIndex returns) equals k. test_map_ref = 274 headerless 8-byte rows of the
map_ref row shape {u16 +0, i16 +2, u16 +4, u16 +6}. Loader/reader instruction sites are decoded."""
import struct
from common import *
header()
print("== static")
check("kind 9 idx 1 = test_map_ref", (kind_path(9, 1) or "").endswith(r"common\test_map_ref.bin"), kind_path(9, 1))
check("kind 9 idx 2 = test_area_ref", (kind_path(9, 2) or "").endswith(r"in\common\test_area_ref.bin"), kind_path(9, 2))
expect_ins(0x26880E, "lea edx, [rdi + 2]"); expect_ins(0x268811, "lea ecx, [rdi + 9]"); expect_ins(0x268814, "call 0x32e400")
expect_ins(0x268821, "call 0x267930")
check("00268829 stores the buffer to 02099D98", rip_target(0x268829) == 0x2099D98 and ins_at(0x268829).startswith("mov qword ptr"))
expect_ins(0x268838, "lea edx, [rdi + 2]"); expect_ins(0x26883E, "call 0x32e620")
check("0026876B/00268772 zero the MapRef globals first (02099D98 among them)", rip_target(0x268772) == 0x2099D98)
expect_ins(0x264EE9, "movsxd rcx, dword ptr [r8 + 4]"); expect_ins(0x264EF9, "movzx eax, word ptr [rax + 4]")
check("MapRef_GetAreaArdFieldResourceIndex reads map_ref (02099D88)", rip_target(0x264ED0) == 0x2099D88)
sw = open("b3_refsweep_02099D98.txt").read()
check("raw sweep of 02099D98: exactly the two stores in MapRef_BeginLoadResources, no dword/qword hit",
      "(a) rip-relative confirmed: 2" in sw and "(b) dword hits: 0" in sw and "(c) qword pointer hits: 0" in sw and "CONTROL 00268829: PASS" in sw)
wide = open("b3_refsweep_02099D00_E00.txt").read()
lea_bases = [l for l in wide.splitlines() if " lea " in l and any(t in l for t in ("02099D80", "02099D88", "02099D90", "02099D98"))]
check("no lea of a base at 02099D80..02099D98 anywhere (no base+disp route to the slot)", not lea_bases, str(lea_bases))
cp = open("callpairs_run1.txt").read()
k91 = [l for l in cp.splitlines() if "(rcx=0x9, next=0x1)" in l or "(rdx=0x9, next=0x1)" in l]
check("(9,1) constant pairs reach only 00252B40 and 003E12A0, neither a request API", sorted(l.split("call ")[1] for l in k91) == ["0x252b40", "0x3e12a0"], str(k91))
expect_ins(0x252B40, "and ecx, 0x7fff")
print("== corpus")
mr_files = copies("ps2data/image/ff12/*/common/map_ref.bin")
ta_files = copies("ps2data/image/ff12/*/common/test_area_ref.bin")
tm_files = copies("ps2data/image/ff12/**/test_map_ref.bin")
check("2 map_ref, 2 test_area_ref, 1 test_map_ref copy", (len(mr_files), len(ta_files), len(tm_files)) == (2, 2, 1), f"{len(mr_files)},{len(ta_files)},{len(tm_files)}")
for ta_f in ta_files:
    lang = ta_f.replace("\\", "/").split("/")[-3]
    m = open([f for f in mr_files if f.replace("\\", "/").split("/")[-3] == lang][0], "rb").read()
    t = open(ta_f, "rb").read()
    h = struct.unpack_from("<8I", m, 0)
    rows = [struct.unpack_from("<4H", m, h[1] + 8 * i) for i in range((h[2] - h[1]) // 8)]
    ta = struct.unpack_from("<%dH" % (len(t) // 2), t)
    first = {}
    for i, r in enumerate(rows): first.setdefault(r[2], i)
    check(f"{lang}: test_area_ref {len(t)} B = u16[{len(ta)}], even size, strictly ascending", len(t) % 2 == 0 and all(ta[i] < ta[i + 1] for i in range(len(ta) - 1)))
    check(f"{lang}: map_ref MRF header, {len(rows)} rows, row word +4 nondecreasing, {len(first)} distinct values 0..{max(first)}",
          m[:3] == b"MRF" and all(rows[i][2] <= rows[i + 1][2] for i in range(len(rows) - 1)) and sorted(first) == list(range(len(first))))
    check(f"{lang}: test_area_ref[k] == first map_ref row with word+4 == k for all {len(ta)} k (count equal: {len(ta)} == {len(first)})",
          len(ta) == len(first) and all(first[k] == ta[k] for k in range(len(ta))))
    check(f"{lang}: test_area_ref does not occur inside map_ref (not a copied section)", m.find(t[:64]) < 0)
tm = open(tm_files[0], "rb").read()
trs = [struct.unpack_from("<4H", tm, 8 * i) for i in range(len(tm) // 8)]
check(f"test_map_ref {len(tm)} B = {len(trs)} rows x 8, no header (starts with a row, not 'MRF')", len(tm) % 8 == 0 and tm[:3] != b"MRF")
check("test_map_ref row word +4 nondecreasing (the map_ref row invariant)", all(trs[i][2] <= trs[i + 1][2] for i in range(len(trs) - 1)))
m = open(mr_files[0], "rb").read(); h = struct.unpack_from("<8I", m, 0)
rows = [struct.unpack_from("<4H", m, h[1] + 8 * i) for i in range((h[2] - h[1]) // 8)]
print(f"  test_map_ref: word+4 max {max(r[2] for r in trs)} (map_ref {max(r[2] for r in rows)}); word+6 max {max(r[3] for r in trs)} (map_ref {max(r[3] for r in rows)})")
print(f"  rows equal to map_ref's same-index row: {sum(1 for i in range(len(trs)) if trs[i] == rows[i])}/{len(trs)} (an older/other build, not a prefix)")
check("test_map_ref is not a byte prefix/section of map_ref", m.find(tm[:64]) < 0)
finish()
