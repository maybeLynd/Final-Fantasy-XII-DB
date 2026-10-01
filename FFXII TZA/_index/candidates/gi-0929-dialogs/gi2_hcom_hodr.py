#!/usr/bin/env python3
"""gi2_hcom_hodr.py - GI-2 (FABLE, 2026-09-29): menuhandbook.bin (hcom) and menuhandbook_order.bin (hodr) decoded
against the code that reads them.

Checks:
  A. hcom, all nine locales: the file is a chain of five length-prefixed sections {u16 len, u16 count, ...} reached by
     p += u16[p] from +8, ending exactly at the file size; each section's content; each consumer's hop count read from
     its instructions. REGRESSION against the "u16 self-relative node web / 0xFFFF dead ends / de adds 0x800661FF"
     reading: the 0xFFFF words lie inside section 0's bitmap, the mask 0x800661FF is in all nine locales, and the
     locale size deltas are the section-1 and section-4 length changes.
  B. hodr: 00572E10 (its only reader of the blob) is installed only for handbook page kind 7, the Sky Pirate's Den;
     +0x16 / +0x17 are only ever the effect-id argument of 003B2D80; +1 is a draw depth; records 30/31 anchor through
     003165C0 (checked against their positions); statue titles, and hcom section 3 = the statues of achievements 20-29.
Names: the monster hctg textId resolved through battle_pack.bin's word banks (battle-text-banks.md), with that page's
control (bank 5 entry 2 = Petrify). Exit status is 1 when any check fails.
"""
import struct, sys, os, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
FST = r"D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_US.fst"
FF = r"D:/FFXII_TZA_extract/ps2data/image/ff12"
LANGS = ["us", "de", "es", "fr", "it", "in", "kr", "cn", "ch"]
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0], d[o:o + 8].rstrip(b"\0")))
def off(a):
    r = a - BASE
    for va, vs, ro, _ in secs:
        if va <= r < va + vs: return ro + (r - va)
funcs = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(fn): return list(md.disasm(d[off(fn):off(fn) + funcs[fn]], fn))
def ins(a): x = list(md.disasm(d[off(a):off(a) + 16], a))[0]; return f"{x.mnemonic} {x.op_str}"
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail != "" else ""))
    if not ok: fails += 1
def dec(s):
    o = ""
    for c in s:
        if 0x20 <= c <= 0x39: o += chr(65 + c - 0x20)
        elif 0x3A <= c <= 0x53: o += chr(97 + c - 0x3A)
        elif 0x54 <= c <= 0x5D: o += chr(48 + c - 0x54)
        elif c == 4: o += " "
        elif c == 0xAC: o += "'"
        elif c == 0xA7: o += ","
        elif c == 0xA8: o += "."
        else: o += "{%02X}" % c
    return o
# battle text banks (battle_pack.bin section at +0x2BBA8 in us, battle-text-banks.md)
bp = open(f"{FF}/test_battle/us/binaryfile/battle_pack.bin", "rb").read(); SEC = 0x2BBA8
def bank(word):
    b, i = word >> 11, word & 0x7FF
    bo = SEC + struct.unpack_from("<I", bp, SEC + 4 + 4 * b)[0]
    blk = bo + struct.unpack_from("<I", bp, bo + 4 + 4 * i)[0]
    p = blk + 2 if bp[blk] == 0 and bp[blk + 1] == 0 else blk
    return dec(bp[p:bp.index(b"\0", p)])
check("battle-text control: bank 5 entry 2 is 'Petrify'", bank((5 << 11) | 2) == "Petrify", bank((5 << 11) | 2))
mon = open(f"{FF}/myoshiok/us/handbook/menuhandbook_monster.bin", "rb").read(); RT = struct.unpack_from("<H", mon, 0x0A)[0]
def beast(k): return bank(struct.unpack_from("<I", mon, RT + 12 * k)[0])
# menu text (002F9860 path)
fst = open(FST, "rb").read(); _sz = {}
def text(tid):
    g, row = divmod(tid, 1000)
    lid = struct.unpack_from("<b", d, off(0x01E09F68 + g))[0]; size = struct.unpack_from("<i", fst, 4 * (2 * 5000 + lid))[0]
    b = f"{FF}/test_battle/us/binaryfile"
    if not _sz:
        for f in os.listdir(b): _sz.setdefault(os.path.getsize(os.path.join(b, f)), []).append(f)
    t = open(os.path.join(b, _sz[size][0]), "rb").read(); tab = struct.unpack_from("<I", t, 0x14)[0]
    st = tab + 12 + struct.unpack_from("<I", t, tab + 16 + 4 * row)[0]
    return dec(t[st:t.index(b"\0", st)])

print("== A. hcom")
def sections(t):
    out = []; p = 8
    while p + 4 <= len(t):
        n = struct.unpack_from("<H", t, p)[0]
        if n == 0: break
        out.append((p, n)); p += n
    return out, p
H = {}
for lang in LANGS:
    t = open(f"{FF}/myoshiok/{lang}/handbook/menuhandbook.bin", "rb").read(); H[lang] = t
    ss, end = sections(t)
    check(f"[{lang}] 'hcom' tag 103, five sections, chain ends at the file size {len(t)}",
          t[:4] == b"hcom" and struct.unpack_from("<I", t, 4)[0] == 103 and len(ss) == 5 and end == len(t), [f"+{p:#x}:{n:#x}" for p, n in ss])
    sec4 = t[ss[4][0]:ss[4][0] + ss[4][1]]
    check(f"[{lang}] section-4 mask carries 0x800661FF's bits", struct.unpack_from("<I", sec4, 4)[0] & 0x800661FF == 0x800661FF, hex(struct.unpack_from("<I", sec4, 4)[0]))
t = H["us"]; ss, _ = sections(t); S = [t[p:p + n] for p, n in ss]
cnt0 = struct.unpack_from("<H", S[0], 2)[0]
check("S0 count 369 = the navigation-map id space; bitmap fills the section", cnt0 == 369 and (cnt0 + 7) // 8 <= len(S[0]) - 4)
ff = [i for i in range(8, len(t) - 1, 2) if struct.unpack_from("<H", t, i)[0] == 0xFFFF]
check("REGRESSION: every 0xFFFF word the 'dead end' reading saw lies inside section 0's bitmap", ff and all(0x0C <= i < 0x3C for i in ff), [hex(i) for i in ff])
tot, w4, nrec = struct.unpack_from("<HHH", S[1], 2)
check("S1: bestiary count 384 (= the monster hctg family's 384 records, hctg word +0x0E), 14 keyed records",
      tot == 384 and nrec == 14 and struct.unpack_from("<H", mon, 0x0E)[0] == 384, (tot, nrec, struct.unpack_from("<H", mon, 0x0E)[0]))
keyed = {}
for r in range(nrec):
    k, v = struct.unpack_from("<HH", S[1], 8 + 4 * r); keyed[k & 0xFFF] = (k >> 12, v)
    print(f"      S1 #{k & 0xFFF:#05x} {beast(k & 0xFFF):28s} type {k >> 12} value {v}" + (f" ({beast(v)})" if k >> 12 == 1 else ""))
check("S1: Enkidu (#0xFC) counts once Gilgamesh (#0xFB) is defeated", beast(0xFC) == "Enkidu" and keyed[0xFC] == (1, 0xFB) and beast(0xFB) == "Gilgamesh")
check("S1: Judge Gabranth (#0x17E) counts at story progress 5500", beast(0x17E) == "Judge Gabranth" and keyed[0x17E] == (0, 5500))
cnt2 = struct.unpack_from("<H", S[2], 2)[0]; pairs = [(S[2][4 + 2 * i], S[2][5 + 2 * i]) for i in range(cnt2)]
check("S2: 45 {quest, threshold} pairs over quest ids 0x80..0xAC", cnt2 == 45 and sorted(a for a, _ in pairs) == list(range(0x80, 0xAD)), cnt2)
cnt3 = struct.unpack_from("<H", S[3], 2)[0]; ids3 = [struct.unpack_from("<H", S[3], 4 + 2 * i)[0] for i in range(cnt3)]
names3 = [beast(i) for i in ids3]
check("S3: 11 monsters", cnt3 == 11, names3)
cnt4, mask = struct.unpack_from("<H", S[4], 2)[0], struct.unpack_from("<I", S[4], 4)[0]
vals = [struct.unpack_from("<I", S[4], 8 + 4 * i)[0] for i in range(cnt4)]
check("S4: us mask 0x800661FF with 14 values 300..16", mask == 0x800661FF and vals == [300, 200, 100, 50, 500, 50000, 100000, 1000000, 50, 8, 1000, 500000, 50, 16])
def secs_of(lang): tt = H[lang]; s2, _ = sections(tt); return [tt[p:p + n] for p, n in s2]
for lang in LANGS[1:]:
    L = secs_of(lang)
    extra = sorted(set(struct.unpack_from("<HH", L[1], 8 + 4 * r) for r in range(struct.unpack_from("<H", L[1], 6)[0])) -
                   set(struct.unpack_from("<HH", S[1], 8 + 4 * r) for r in range(nrec)))
    check(f"[{lang}] the section-1 difference is one Rogue Tomato rule (#0xD3, story >= 78)", extra == [(0xD3, 78)] and beast(0xD3) == "Rogue Tomato", extra)
    m = struct.unpack_from("<I", L[4], 4)[0]
    exp = 0x800669FF if lang in ("in", "kr", "cn", "ch") else 0x800661FF
    check(f"[{lang}] section-4 mask {exp:#x}" + (" (counter 11 override 48000)" if exp != 0x800661FF else ""), m == exp and
          (exp == 0x800661FF or struct.unpack_from("<I", L[4], 8 + 4 * 9)[0] == 48000), hex(m))
# consumer hop counts
hops = {0x315D50: ([0x315D65, 0x315D6E, 0x315D77], 0x315D80, "movzx r8d, word ptr [rax + 2]"),
        0x3154B0: ([0x315554], 0x31555E, "movzx r9d, word ptr [rax + 6]"),
        0x3161A0: ([0x3161C3], 0x3161E3, "cmp bp, word ptr [rax + 2]"),
        0x316480: ([0x3164AD, 0x3164BA], 0x3164D7, "cmp r14w, word ptr [rax + 2]"),
        0x315DC0: ([0x315E00, 0x315E09], 0x315E12, "movzx r8d, word ptr [rax + 2]"),
        0x3160C0: ([], 0x316103, "cmp bx, word ptr [rdi + 2]")}
for fn, (hs, cntsite, s) in hops.items():
    ok = all(re.match(r"movzx eax, word ptr \[r[a-z0-9]+\]$", ins(h)) for h in hs) and ins(cntsite) == s
    check(f"{fn:08X} hops {len(hs)} time(s) from +8, then reads the section count ({cntsite:08X})", ok, [ins(h) for h in hs] + [ins(cntsite)])
check("003165C0 hops four times (003165DA/E3/EC/F5)", all(ins(a).startswith("movzx") and "word ptr" in ins(a) for a in (0x3165DA, 0x3165E3, 0x3165EC, 0x3165F5)),
      [ins(a) for a in (0x3165DA, 0x3165E3, 0x3165EC, 0x3165F5)])
check("section-1 type nibble: shr ecx,0xc in 003161A0 (00316287) and 003154B0 (003155BE)", ins(0x316287) == "shr ecx, 0xc" and ins(0x3155BE) == "shr ecx, 0xc")
check("section-2 predicates: cleared bitset +0x1020 (0046B1A0), ordered bitset +0x1000 (0046B240), progress byte +0x1064 (0046B180)",
      ins(0x46B1D4) == "test byte ptr [rax + rdi + 0x1020], dl" and ins(0x46B274) == "test byte ptr [rax + rdi + 0x1000], dl" and ins(0x46B18E) == "movzx eax, byte ptr [rax + rbx + 0x1064]")

print("== B. hodr - the Sky Pirate's Den")
check("0056EE10 installs 00572E10 only for page kind 7", ins(0x56EE3F) == "cmp al, 7" and ins(0x56EE7A) == "lea rdx, [rip + 0x3f8f]"
      and 0x56EE7A + 7 + 0x3F8F == 0x572E10)
refs = []
for fn in sorted(funcs):
    if not (0x121000 <= fn < 0x8C2000): continue
    try: xs = dis(fn)
    except Exception: continue
    for x in xs:
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
        if m and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == 0x572E10: refs.append(x.address)
check("00572E10's only rip reference is 0056EE7A", refs == [0x56EE7A], [f"{a:08X}" for a in refs])
o = open(f"{FF}/myoshiok/us/handbook/menuhandbook_order.bin", "rb").read()
n = struct.unpack_from("<I", o, 8)[0]
check("hodr: tag 101, 33 records, 12 + 33*32 = file size", o[:4] == b"hodr" and struct.unpack_from("<I", o, 4)[0] == 101 and n == 33 and 12 + 32 * n == len(o))
R = [o[12 + 32 * i:44 + 32 * i] for i in range(n)]
check("+0 of records 0..29 is a permutation of 0..29; 30/31 are 0xFF, 32 is 0xFE", sorted(r[0] for r in R[:30]) == list(range(30)) and [R[30][0], R[31][0], R[32][0]] == [0xFF, 0xFF, 0xFE])
check("REGRESSION: +1 is a depth (all 33 values 0..32 distinct) and is used as (0xFF - v) * 10000 (00572A8B / 00572A8F)",
      sorted(r[1] for r in R) == list(range(33)) and ins(0x572A8B) == "sub edx, ecx" and ins(0x572A8F) == "imul edx, edx, 0x2710")
b16 = []
for fn in sorted(funcs):
    if not (0x570000 <= fn < 0x578000): continue
    xs = dis(fn)
    for i, x in enumerate(xs):
        if re.search(r"byte ptr \[r[a-z0-9]+ \+ 0x1[67]\]", x.op_str):
            nxt = [y for y in xs[i + 1:i + 6] if y.mnemonic == "call"]
            b16.append((x.address, x.op_str.split(",")[0], nxt[0].op_str if nxt else None))
check("positive control: the +0x16/+0x17 sweep over 0x570000..0x578000 finds 11 byte reads", len(b16) == 11, len(b16))
check("REGRESSION: every +0x16/+0x17 read is the r9d effect id of the next call, 003B2D80 (no index use)",
      all(r == "r9d" and c == "0x3b2d80" for _, r, c in b16), [(f"{a:08X}", r, c) for a, r, c in b16])
check("005734C0 draws the new selection with +0x17 and the old one with +0x16",
      ins(0x57351C) == "movzx r9d, byte ptr [rbx + 0x16]" and ins(0x5735F5) == "movzx r9d, byte ptr [rbx + 0x17]")
check("groups are gated by 00576E10 = 003154B0(7, i), the award bit at +0x3844",
      ins(0x576E17) == "mov cl, 7" and ins(0x3155F4) == "cmp cl, 7" and ins(0x315612) == "movzx edx, byte ptr [rax + rcx + 0x3844]")
check("children anchor through 003165B0 = jmp 003165C0 (called with the record index at 005729BE)",
      ins(0x3165B0) == "jmp 0x3165c0" and ins(0x5729BB) == "movzx ecx, bl" and ins(0x5729BE) == "call 0x3165b0")
def ov(i):
    if i >= 0x20 or not (mask >> i) & 1: return 0
    return vals[bin(mask & ((1 << i) - 1)).count("1")]
key = {r[0]: i for i, r in enumerate(R[:30])}
pos = [struct.unpack_from("<hh", r, 2) for r in R]
a30, a31 = key[ov(30)], key[ov(31)]
check("record 30 anchors to record 0 and sits on its exact position", a30 == 0 and pos[30] == pos[0], (a30, pos[30], pos[0]))
check("record 31 anchors to record 16 (id-31 override 16) and sits beside it", a31 == 16 and abs(pos[31][0] - pos[16][0]) <= 40 and abs(pos[31][1] - pos[16][1]) <= 40, (a31, pos[31], pos[16]))
titles = [text(0x1B68 + i) for i in range(30)]
print("      statues: " + ", ".join(f"{i}:{s}" for i, s in enumerate(titles)))
check("statue 0 is 'Balthier' and its description names Assault Striker", titles[0] == "Balthier" and "Assault Striker" in text(0x5DDE))
check("hcom section 3 entries 0..9 are the statues of achievements 20..29, in order", [x.split(",")[0] for x in names3[:10]] == titles[20:30], (names3[:10], titles[20:30]))
check("popup reads +0xA / +0xC as the window position (005727BF / 005727BB)", ins(0x5727BF) == "movzx eax, word ptr [rax + 0xa]" and ins(0x5727BB) == "movsx ecx, word ptr [rax + 0xc]")
check("pointer at (+2 + +6, +4 + +8) (0057346B / 00573479)", ins(0x57346B) == "add dx, word ptr [rbx + 6]" and ins(0x573479) == "add ax, word ptr [rbx + 8]")
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
