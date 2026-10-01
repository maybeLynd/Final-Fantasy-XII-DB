"""check_gmap.py - A1 `gmap` = ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_guide00..04.bin.
Corpus layout check over every shipped copy (35 files), the join to menumap_common.bin section 3, .fst sizes,
the static-image checks of the loader 003C1DF0 and the readers 003BD890 / 003BD8F0 / 003BD860, and the
id sweep (with its positive control) behind "only guide00 is ever requested". Read-only; prints FAILS."""
import os, struct, collections, re
from pe import *
import pe

FAILS = 0
def check(ok, msg):
    global FAILS
    if not ok:
        FAILS += 1
    print(("PASS " if ok else "FAIL ") + msg)

H = lambda b, o: struct.unpack_from("<H", b, o)[0]
I = lambda b, o: struct.unpack_from("<I", b, o)[0]
FST = "D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_%s.fst"
FSTTAG = dict(us="US", de="DE", es="ES", fr="FR", it="IT", ch="CH", cn="CN", kr="KR", **{"in": "IN"})
CH = {**{0x20 + i: chr(65 + i) for i in range(26)}, **{0x3A + i: chr(97 + i) for i in range(26)}, 0x04: " "}

def text(b, o):
    e = b.index(0, o)
    return "".join(CH.get(c, ".") for c in b[o:e]), e

def cmap_sec3(b):
    o = H(b, 0xA); n = H(b, o); p = o + 2 + 2 * n; p = (p + 3) & ~3
    cnt = I(b, p)
    return [struct.unpack_from("<HHBBH", b, p + 4 + 8 * i) for i in range(cnt)], p

def tim2_len(b, o):
    """TIM2 file header 16 bytes + sum of picture TotalSize (u32 at picture+0)"""
    n = H(b, o + 6); p = o + 16
    for _ in range(n):
        p += I(b, p)
    return p - o, n

print("=== 1. corpus: every shipped copy")
files = {}
for lang in LANGS:
    for k in range(16):
        p = f"{EXTRACT}/{lang}/worldmap/menumap_guide{k:02d}.bin"
        if os.path.exists(p):
            files[(lang, k)] = open(p, "rb").read()
print("files:", len(files), dict(collections.Counter(l for l, k in files)))
check(len(files) == 35, "35 menumap_guide##.bin copies (us/cn/es/fr/it/kr 00-04, ch 00-01, in 00-01, de 00)")
check(max(k for l, k in files) == 4, "no guide05..15 ships although the image carries paths for 00..15")
tim2_count = 0
for (lang, k), b in sorted(files.items()):
    tag = f"{lang}/guide{k:02d} ({len(b)} B)"
    offT, offP, z, n = H(b, 8), H(b, 0xA), H(b, 0xC), H(b, 0xE)
    ok = b[:4] == b"gmap" and I(b, 4) == 0x64 and z == 0 and offT == 0x10 + 8 * n
    check(ok, f"{tag}: 'gmap', +4 == 0x64, +0xC == 0, text section +8 = {offT:#x} == 0x10 + 8*count({n})")
    ents = [struct.unpack_from("<HHHH", b, 0x10 + 8 * i) for i in range(n)]
    offs = [e[2] for e in ents]
    check(all(e[3] == 0 for e in ents) and offs == sorted(offs) and len(set(offs)) == n,
          f"{tag}: entry +6 == 0 in all {n}; text offsets strictly ascending")
    ends, strs = [], []
    for i, e in enumerate(ents):
        s, end = text(b, offT + e[2]); strs.append(s); ends.append(end)
        nxt = offT + offs[i + 1] if i + 1 < n else None
        if nxt is not None and end != nxt - 1:
            break
    closed = all((ends[i] == offT + offs[i + 1] - 1) for i in range(n - 1))
    check(closed, f"{tag}: each string's 00 terminator is the byte before the next entry's text")
    tend = ends[-1] + 1
    al16 = (tend + 15) & ~15
    if offP == 0xFFFF:
        check(False, f"{tag}: +0xA is 0xFFFF (no TIM2 offset)")
    elif offP >= len(b):
        al4 = (tend + 3) & ~3
        check(offP == al16 and len(b) == al4 and not any(b[tend:]),
              f"{tag}: +0xA = {offP:#x} lies at/after EOF {len(b):#x}; == align16(text end {tend:#x}); file ends at "
              f"align4(text end) with zero pad -> no embedded TIM2; the pointer 003BD915-003BD92D forms is past the data")
    else:
        L, pics = tim2_len(b, offP)
        tim2_count += 1
        check(offP == al16 and b[offP:offP + 4] == b"TIM2" and offP + L == len(b) and (b[offP + 0x40] & 0xF) == 1,
              f"{tag}: +0xA = {offP:#x} == align16(text end); 'TIM2' there, {pics} picture(s), 16+sum(TotalSize) = {L} "
              f"closes at EOF; byte TIM2+0x40 low nibble == 1 (the 0039BEC0 gate)")
    print(f"      first text: {strs[0][:70]!r}")
print(f"embedded TIM2 present in {tim2_count} of 35 files")

print("\n=== 2. join to menumap_common.bin section 3 (the selection table 003BD950 walks)")
for lang in sorted({l for l, k in files}):
    cm = open(f"{EXTRACT}/{lang}/worldmap/menumap_common.bin", "rb").read()
    recs, p = cmap_sec3(cm)
    check(all(r[3] == 0 for r in recs), f"{lang}: cmap sec3 @ {p:#x}: {len(recs)} recs, byte +4 (guide selector read at "
                                        f"003C1EA7) == 0 in all -> 003C1DF0 only ever requests id 0x496 (guide00)")
    b = files[(lang, 0)]
    n = H(b, 0xE); ents = [struct.unpack_from("<HHHH", b, 0x10 + 8 * i) for i in range(n)]
    same = sum((ents[i][0], ents[i][1]) == (recs[i][0], recs[i][1]) for i in range(min(n, len(recs))))
    shifted = sum((ents[i][0], ents[i][1]) == (recs[(i + 1) % len(recs)][0], recs[(i + 1) % len(recs)][1]) for i in range(n))
    seq = all(recs[i][4] == i for i in range(len(recs)))
    check(n == len(recs) == 77 and same == 77 and shifted == 0 and seq,
          f"{lang}: guide00 count {n} == cmap sec3 count {len(recs)}; (gate,key) equal at the same index {same}/77 "
          f"(control, index+1: {shifted}/77); cmap +6 seq == index (003BD8BD uses it to index guide00)")
    pairs = {(r[0], r[1]) for r in recs}
    for k in range(1, 5):
        if (lang, k) in files:
            g = files[(lang, k)]; m = H(g, 0xE)
            e = [struct.unpack_from("<HH", g, 0x10 + 8 * i) for i in range(m)]
            inset = sum(x in pairs for x in e); gates = sum(any(x[0] == r[0] for r in recs) for x in e)
            print(f"      {lang}/guide{k:02d}: {m} entries, (gate,key) found in cmap sec3 {inset}/{m}, gate value found {gates}/{m}, "
                  f"keys {[hex(x[1]) for x in e]}")

print("\n=== 3. .fst sizes for kind 7 ids 0x496..0x4A5")
for lang, tag in FSTTAG.items():
    fst = open(FST % tag, "rb").read()
    sz = [struct.unpack_from("<i", fst, 4 * (7 * 5000 + 0x496 + k))[0] for k in range(16)]
    want = [len(files[(lang, k)]) if (lang, k) in files else -1 for k in range(16)]
    check(sz == want, f"FileSizeTable_{tag}: ids 0x496..0x4A5 sizes {sz[:6]}... == extracted sizes / -1 for absent")
for k in range(16):
    s = cstr(u64(0x01E0E530 + (0x496 + k) * 8))
    if not s.endswith(f"menumap_guide{k:02d}.bin"):
        check(False, f"kind-7 slot 0x{0x496 + k:X} -> {s}")
check(True, "kind-7 path slots 01E0E530[0x496+k] name menumap_guide{k:02d}.bin for k = 0..15")

print("\n=== 4. static image")
def ins(a, mn, frag):
    x = ins_at(a)
    check(x is not None and x.mnemonic == mn and frag in x.op_str, f"{a:08X}: expect `{mn} ..{frag}..` got `{x.mnemonic} {x.op_str}`")
ins(0x003C1E15, "mov", "rcx, qword ptr [rax + 0xe8]")     # cmap blob
ins(0x003C1E21, "movzx", "eax, word ptr [rcx + 0xa]")     # cmap sec2 offset
ins(0x003C1E48, "call", "0x3bd950")                       # sec3 walk -> record
ins(0x003C1E59, "mov", "qword ptr [rcx + 0xf0], rax")
ins(0x003C1EA7, "movzx", "r8d, byte ptr [rdx + 4]")
ins(0x003C1EAC, "mov", "edx, 7")
ins(0x003C1EB1, "add", "r8d, 0x496")
ins(0x003C1EB8, "lea", "r9d, [rdx - 4]")
ins(0x003C1EBC, "call", "0x249210")
ins(0x003C1EC8, "mov", "rdx, qword ptr [rax + 8]")
ins(0x003C1ECC, "mov", "qword ptr [rcx + 0xf8], rdx")
ins(0x003BD8BD, "movzx", "r8d, word ptr [rdx + 6]")       # selected cmap record seq
ins(0x003BD8C2, "movzx", "eax, word ptr [rcx + 0xe]")     # gmap count
ins(0x003BD8CE, "movzx", "edx, word ptr [rcx + r8*8 + 0x14]")  # entry +4 text offset
ins(0x003BD8DE, "movzx", "eax, word ptr [rcx + 8]")       # text section
ins(0x003BD8F8, "movzx", "eax, word ptr [rcx + 0xe]")
ins(0x003BD915, "movzx", "eax, word ptr [rcx + 0xa]")     # TIM2 offset -> widget +0x108
ins(0x003BD930, "movzx", "edx, word ptr [rdx + 4]")
ins(0x003BD93A, "movzx", "eax, word ptr [rcx + 8]")
ins(0x003BC7A7, "call", "0x3bd8f0")
ins(0x003BC7B3, "mov", "qword ptr [rbx + 0x100], rax")
ins(0x003BC7C3, "call", "0x39bec0")                       # TIM2 validator / slot registry
ins(0x0039BEDC, "lea", "rdx, [rip + 0x97558d]")           # "TIM2"
ins(0x0039BEED, "mov", "eax, dword ptr [rdi + 0x40]")
ins(0x002BA9DE, "call", "0x28fd00")                       # (text, TIM2) consumer
check(d[off(0x00D11470):off(0x00D11470) + 4] == b"TIM2", "00D11470 holds 'TIM2' (0039BEC0 memcmp operand)")

print("\n=== 5. id sweep: who else could request 0x497..0x4A5 (function-list independent byte sweep)")
REQ = {0x249210, 0x249180, 0x32E400, 0x32EB40}
def sweep(lo, hi):
    t0, t1, ro = text_range(); blob = d[ro:ro + (t1 - t0)]
    found = []
    for i in range(len(blob) - 3):
        v = struct.unpack_from("<I", blob, i)[0]
        if not (lo <= v <= hi):
            continue
        a = t0 + i
        x, how = containing_ins(a)
        if x is None or x.address + x.size < a + 4:
            continue
        if "[" in x.op_str.split(",")[-1] or x.mnemonic not in ("mov", "lea", "add", "sub", "or"):
            continue
        if not re.match(r"(r8d?|r8w|edx|rdx|r9d|ecx|eax|ebx|esi|edi|ebp|r1[0-5]d|r[0-9]d),", x.op_str):
            continue
        nxt = list(md.disasm(d[pe.off(x.address):pe.off(x.address) + 90], x.address))[:14]
        calls = [y for y in nxt if y.mnemonic == "call" and y.op_str.startswith("0x") and int(y.op_str, 16) in REQ]
        found.append((x.address, f"{x.mnemonic} {x.op_str} [{how}]", calls[0].address if calls else None))
    return found
ctl = sweep(0xA2, 0xA4)
ctl_req = [f for f in ctl if f[2]]
for f in ctl_req:
    print(f"   control hit {f[0]:08X} {f[1]} -> request call {f[2]:08X}")
check({f[0] for f in ctl_req} >= {0x003BC305, 0x003BC333, 0x003BC35D},
      "positive control: sweeping 0xA2..0xA4 finds the three documented 003BC2D0 requests (wmap/lmap/cmap)")
hits = sweep(0x496, 0x4A5)
req = [f for f in hits if f[2]]
for f in hits:
    print(f"   {f[0]:08X} {f[1]:40s} request-call-within-12: {'%08X' % f[2] if f[2] else '-'}  fn {owner(f[0]) or 0:08X}")
check([f[0] for f in req] == [0x003C1EB1], "only register-immediate use of 0x496..0x4A5 followed by a kind-7 request "
                                             "call is 003C1EB1 add r8d, 0x496")
print(f"\nFAILS {FAILS}")
