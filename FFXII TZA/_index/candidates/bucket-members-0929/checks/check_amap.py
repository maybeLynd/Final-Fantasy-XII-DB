"""check_amap.py - A2 `amap` = ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_area.bin.
Corpus layout check over every shipped copy, joins against sibling files, and the static-image checks of the
loader and the four accessors. Read-only. Prints each check and a final FAILS count."""
import os, struct, collections
from pe import *

FAILS = 0
def check(ok, msg):
    global FAILS
    if not ok:
        FAILS += 1
    print(("PASS " if ok else "FAIL ") + msg)

H = lambda b, o: struct.unpack_from("<H", b, o)[0]
I = lambda b, o: struct.unpack_from("<I", b, o)[0]
ROOT = "D:/FFXII_TZA_extract/ps2data/image/ff12"
FST = "D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_%s.fst"

def parse_amap(b):
    """returns dict of the four sections; raises on any closure failure"""
    assert b[:4] == b"amap"
    o8, oA, oC, oE = H(b, 8), H(b, 0xA), H(b, 0xC), H(b, 0xE)
    nP = b[o8]; P = list(b[o8 + 1:o8 + 1 + nP])
    nQ = b[oA]; Q = list(b[oA + 1:oA + 1 + nQ])
    nR = H(b, oC); R = [H(b, oC + 2 + 2 * i) for i in range(nR)]
    nS = I(b, oE); S = [I(b, oE + 4 + 4 * i) for i in range(nS)]
    return dict(fid=I(b, 4), off=(o8, oA, oC, oE), P=P, Q=Q, R=R, S=S,
                ends=(o8 + 1 + nP, oA + 1 + nQ, oC + 2 + 2 * nR, oE + 4 + 4 * nS))

def st2e_ids(b):
    assert b[:4] == b"st2e"
    n = I(b, 4); rs = I(b, 8); hs = I(b, 0xC)
    return set(I(b, hs + rs * i) for i in range(n))

print("=== 1. corpus: every shipped copy")
files = {}
for lang in LANGS:
    p = f"{EXTRACT}/{lang}/worldmap/menumap_area.bin"
    if os.path.exists(p):
        files[lang] = open(p, "rb").read()
print("copies found:", len(files), sorted(files), "(in_sdver has no worldmap folder)" if "in_sdver" not in files else "")
check(len(files) == 9, "9 locale copies of menumap_area.bin")
digests = collections.Counter(hashlib.sha256(b).hexdigest()[:16] for b in files.values())
print("distinct contents:", dict(digests))
for lang, b in sorted(files.items()):
    a = parse_amap(b)
    o8, oA, oC, oE = a["off"]; e = a["ends"]
    check(a["fid"] == 0xC9, f"{lang}: +4 file id == 0xC9 (got {a['fid']:#x})")
    check((o8, oA, oC, oE) == (0x10, e[0], e[1], e[2]) and e[3] == len(b),
          f"{lang}: size arithmetic 0x10 +1+{len(a['P'])} | +1+{len(a['Q'])} | +2+2*{len(a['R'])} | +4+4*{len(a['S'])} "
          f"= {e[3]} == file size {len(b)}; sections abut (offs {o8:#x},{oA:#x},{oC:#x},{oE:#x})")
    check(len(a["P"]) == len(a["S"]) == 39, f"{lang}: P count == S count == 39 (area space)")
    check(len(a["Q"]) == len(a["R"]) == 59, f"{lang}: Q count == R count == 59 (persistence-group space)")
    check(all(q < len(a["P"]) for q in a["Q"]), f"{lang}: every Q value < 39 (Q maps group -> area index); max {max(a['Q'])}")
    check(max(a["P"]) < 0x80, f"{lang}: P values < 0x80, so 0x80|P stays a distinct payload byte; distribution "
                              f"{dict(sorted(collections.Counter(a['P']).items()))}")
    badR = [r for r in a["R"] if r != 0xFFFF and not (0x8000 <= r < 0x8040)]
    check(not badR, f"{lang}: R values are 0xFFFF or 0x8000..0x803F (class-13 sub-table 1, the 64 area-map key items); "
                    f"{sum(r != 0xFFFF for r in a['R'])} set, {a['R'].count(0xFFFF)} none")
    check(a["S"][0] == 0xFFFFFFFF and all(a["S"][i] == 60099 + i for i in range(1, 39)),
          f"{lang}: S[0] = -1, S[i] = 60099+i for i=1..38")

print("\n=== 2. joins against sibling files")
for lang, b in sorted(files.items()):
    a = parse_amap(b)
    mn = f"{ROOT}/test_battle/{lang}/binaryfile/menu_mapname.bin"
    ids = st2e_ids(open(mn, "rb").read())
    hit = sum(s in ids for s in a["S"][1:])
    ctl = sum((s + 1000) in ids for s in a["S"][1:])
    check(hit == 38 and ctl == 0, f"{lang}: S[1..38] in menu_mapname.bin id table {hit}/38 (control S+1000: {ctl}/38)")
    w = open(f"{EXTRACT}/{lang}/worldmap/menumap_world.bin", "rb").read()
    wa = H(w, 0xA); wn = I(w, wa)
    names = [I(w, wa + 4 + 0x1C * i + 16) for i in range(wn)]
    same = sum(names[i] == a["S"][i] for i in range(39))
    shifted = sum(names[(i + 1) % 39] == a["S"][i] for i in range(39))
    check(wn == 39 and same == 39 and shifted == 0,
          f"{lang}: wmap area record i +16 nameId == amap S[i] for {same}/39 (control, i+1: {shifted}/39)")
mr = open(f"{ROOT}/in/common/map_ref.bin", "rb").read()
base = I(mr, 4); rows = (len(mr) - base) // 8
groups = [H(mr, base + 8 * i + 6) for i in range(rows)]
print(f"map_ref.bin (in): {rows} rows, persistence groups used {len(set(groups))}, max {max(groups)}")
big = [(i, g_) for i, g_ in enumerate(groups) if g_ > 58]
check(max(g_ for g_ in groups if g_ <= 58) == 58 and len(big) == 1,
      f"map_ref.bin groups are 0..58 (= 59 = Q/R count) except {len(big)} row(s) {big}; a group >= 59 fails the "
      f"accessor bounds test (00254390 cmp ecx,eax / jb) and reads as area 0 / R none")
cm = open(f"{EXTRACT}/us/worldmap/menumap_common.bin", "rb").read()
cd = H(cm, 8); cgroups = [cm[cd + 4 + 8 * i] for i in range(I(cm, cd))]
check(max(cgroups) < 59, f"menumap_common directory groups all < 59 (max {max(cgroups)})")

print("\n=== 3. .fst sizes and the kind-7 path slot")
for lang, tag in [("us", "US"), ("de", "DE"), ("es", "ES"), ("fr", "FR"), ("it", "IT"), ("ch", "CH"), ("cn", "CN"), ("kr", "KR"), ("in", "IN")]:
    fst = open(FST % tag, "rb").read()
    sz = struct.unpack_from("<i", fst, 4 * (7 * 5000 + 0xA5))[0]
    check(sz == len(files[lang]), f"FileSizeTable_{tag}.fst kind 7 id 0xA5 = {sz} == {lang} file size {len(files[lang])}")
slot = u64(0x01E0E530 + 0xA5 * 8)
check(cstr(slot).endswith("WorldMap\\menumap_area.bin"), f"kind-7 path slot 01E0E530[0xA5] -> {cstr(slot)}")

print("\n=== 4. static image: loader and accessors")
def ins(a, mn, frag):
    x = ins_at(a)
    ok = x is not None and x.mnemonic == mn and frag in x.op_str
    check(ok, f"{a:08X}: expect `{mn} ..{frag}..` got `{x.mnemonic} {x.op_str}`" if x else f"{a:08X}: no decode")
ins(0x0025390D, "mov", "edx, 7")
ins(0x00253917, "mov", "r8d, 0xa5")
ins(0x00253924, "lea", "r9d, [rdx - 4]")
ins(0x00253928, "call", "0x249180")
ins(0x00253930, "mov", "qword ptr [rip + 0x1e3ee99], rax")   # -> 020927D0 (00249180 returns obj+8, the blob)
ins(0x0024919A, "mov", "rax, qword ptr [rax + 8]")
ins(0x002543D7, "movzx", "edx, word ptr [rax + 8]")        # P
ins(0x002543E9, "movzx", "eax, byte ptr [rax + rdx + 1]")
ins(0x00254387, "movzx", "edx, word ptr [rax + 0xa]")      # Q
ins(0x00254399, "movzx", "eax, byte ptr [rax + rdx + 1]")
ins(0x002543FB, "movzx", "edx, word ptr [rax + 0xc]")      # R
ins(0x00254413, "movzx", "ecx, word ptr [rdx + rax*2 + 2]")
ins(0x00254424, "call", "0x309ec0")
ins(0x002543A7, "movzx", "edx, word ptr [rax + 0xe]")      # S
ins(0x002543BF, "mov", "ecx, dword ptr [rdx + rax*4 + 4]")
ins(0x002543C3, "jmp", "0x2f9920")
ins(0x00583F3F, "call", "0x264f90")                        # save header: field -> group -> Q
ins(0x00583F46, "call", "0x254380")
ins(0x00583F4B, "mov", "dword ptr [rdi + 0x48], eax")
ins(0x003F92EC, "call", "0x254380")                        # group -> area -> P -> glyph escape
ins(0x003F92F3, "call", "0x2543d0")
ins(0x003F92FA, "call", "0x2ac2c0")
g = d[off(0x01E0CDFC):off(0x01E0CDFC) + 5]
check(g == bytes([0x0F, 0x3F, 0x81, 0x80, 0x00]),
      f"01E0CDFC escape template bytes {g.hex(' ')} = 0F '?' 81 80|P 00 (002AC2C0 ORs P|0x80 into byte 3)")

print("\n=== 5. raw rip sweep of the blob slot 020927D0 (function-list independent)")
refs = raw_rip_refs(0x020927D0, 0x020927D8)
for a_, mn, op, t in refs:
    print(f"   {a_:08X} {mn} {op}   fn {owner(a_) or 0:08X}")
check(len(refs) == 7 and {owner(r[0]) for r in refs} == {0x253780, 0x254380, 0x2543A0, 0x2543D0, 0x2543F0},
      "7 references: loader 00253780 (1 read, 2 writes) + the four accessors; no other code touches the slot")
ctl = raw_rip_refs(0x02B457E0, 0x02B457E8)
check(len(ctl) >= 100, f"positive control: the same sweep finds {len(ctl)} refs to the world-map widget singleton 02B457E0 "
                       f"(FABLE ripscan lists 158 lines incl. the ones this build's functions list covers)")
print(f"\nFAILS {FAILS}")
