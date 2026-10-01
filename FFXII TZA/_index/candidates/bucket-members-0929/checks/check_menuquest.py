"""check_menuquest.py - A3 ps2data/image/ff12/myoshiok/<lang>/quest/menuquest00..02.bin.
Corpus layout check over every shipped copy (27 files), the join to menuquest.dat (qstd) groups and to
menuquest.h, .fst sizes, the static-image checks of the loader 003800D0 and the readers 0037E8D0 / 0037EE10 /
0037EF70 / 0037FEA0 / 00473D50 / 00473DB0 / 00473B70 / 00473BB0 / 00473CC0, and the id sweep with its control.
Read-only; prints FAILS."""
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

def chunk(b, o, magic):
    """{magic, u32 count (bit31 = relocated at run time; 0 on disk), u32 off[count] relative to chunk}"""
    if b[o:o + 4] != magic:
        return None
    n = I(b, o + 4)
    return n, [I(b, o + 8 + 4 * i) for i in range(n & 0x7FFFFFFF)]

print("=== 1. corpus: every shipped copy")
files = {}
for lang in LANGS:
    for g in range(16):
        p = f"{EXTRACT}/{lang}/quest/menuquest{g:02d}.bin"
        if os.path.exists(p):
            files[(lang, g)] = open(p, "rb").read()
print("files:", len(files), dict(collections.Counter(l for l, g in files)))
check(len(files) == 27 and max(g for l, g in files) == 2, "27 files = 9 locales x menuquest00..02 (none past 02)")
hdr = {}
for (lang, g), b in sorted(files.items()):
    tag = f"{lang}/menuquest{g:02d} ({len(b)} B)"
    off = [H(b, 2 * i) for i in range(6)]; c = H(b, 0xC); n = H(b, 0xE)
    hdr[(lang, g)] = n
    recs = [struct.unpack_from("<10H", b, 16 + 20 * k) for k in range(n)]
    ok = c == 0xFFFF and off[0] == 16 + 20 * n and off == sorted(off) and off[5] + 28 * n == len(b)
    check(ok, f"{tag}: header u16 off[6] = {[hex(x) for x in off]}, +0xC = {c:#x}, N = {n}; "
              f"16 + 20*N = {16 + 20 * n} == off[0]; off[5] + 28*N = {off[5] + 28 * n} == size")
    check(all(r[6:] == (0xFFF,) * 4 for r in recs), f"{tag}: record +12..+19 = four 0x0FFF in all {n}")
    check(all(r[5] == 0 for r in recs), f"{tag}: record +10 (section-5 rel) == 0 in all {n} (readers use 28*k instead)")
    # sections 0..2: zero-terminated strings
    sok, s0 = True, []
    for k, r in enumerate(recs):
        for i in range(3):
            if r[i] == 0xFFFF:
                continue
            o = off[i] + r[i]
            if not (off[i] <= o < off[i + 1]):
                sok = False; continue
            s, e = text(b, o)
            if e >= off[i + 1]:
                sok = False
            if i == 0:
                s0.append(s)
    none = sum(r[i] == 0xFFFF for r in recs for i in range(3))
    check(sok, f"{tag}: sections 0-2 string refs land in their section and terminate inside it ({none} of {3 * n} are 0xFFFF)")
    print(f"      section-0 strings: {collections.Counter(s0).most_common(3)}")
    # sections 3 and 4: QHD0 / QHT0 chunks
    for i, magic in ((3, b"QHD0"), (4, b"QHT0")):
        starts = sorted({off[i] + r[i] for r in recs if r[i] != 0xFFFF})
        good = [chunk(b, s, magic) for s in starts]
        cnts = collections.Counter(x[0] for x in good if x)
        inside = all(x and all(8 + 4 * (x[0]) <= o_ < (starts[j + 1] if j + 1 < len(starts) else off[i + 1]) - starts[j]
                               for o_ in x[1]) for j, x in enumerate(good))
        check(all(good) and all(x[0] < 0x80000000 for x in good) and inside,
              f"{tag}: section {i}: {len(starts)} distinct {magic.decode()} chunks, counts {dict(cnts)} (bit31 clear on "
              f"disk), every sub-offset inside its own chunk")
    # section 5: 28-byte nibble rows
    print(f"      section 5: {n} x 28 B; distinct rows {len({b[off[5] + 28 * k: off[5] + 28 * k + 28] for k in range(n)})}; "
          f"bytes 26-27 always zero: {all(b[off[5] + 28 * k + 26:off[5] + 28 * k + 28] == bytes(2) for k in range(n))}")

print("\n=== 2. joins: menuquest.dat groups, menuquest.h")
for lang in sorted({l for l, g in files}):
    q = open(f"{EXTRACT}/{lang}/quest/menuquest.dat", "rb").read()
    n = H(q, 0xA); groups = collections.Counter(I(q, 0xC + 8 * i + 4) & 0xFF for i in range(n))
    want = [hdr[(lang, g)] for g in range(3)]
    check(q[:4] == b"qstd" and H(q, 8) == 3 and [groups[g] for g in range(3)] == want and sum(want) == n,
          f"{lang}: qstd +8 = {H(q, 8)} groups, +0xA = {n} quests; per-group counts {[groups[g] for g in range(3)]} "
          f"== menuquest00/01/02 N {want}")
    shifted = [groups[(g + 1) % 3] for g in range(3)]
    print(f"      control (group+1): {shifted} vs {want}")
for lang in ("us", "cn", "kr"):
    h = open(f"{EXTRACT}/{lang}/quest/menuquest.h", "rb").read().decode("utf-8-sig")
    num = int(re.search(r"menuquest_NUM\s+(\d+)", h).group(1)); gn = int(re.search(r"menuquest_group_NUM\s+(\d+)", h).group(1))
    check(num == sum(hdr[(lang, g)] for g in range(3)) and gn == 3,
          f"menuquest.h ({lang}): menuquest_NUM {num} == sum of N over the 3 files; menuquest_group_NUM {gn} == 3 files")

print("\n=== 3. .fst sizes, kind 7 ids 0x12A..0x139, and path slots")
for lang, tag in FSTTAG.items():
    fst = open(FST % tag, "rb").read()
    sz = [struct.unpack_from("<i", fst, 4 * (7 * 5000 + 0x12A + g))[0] for g in range(16)]
    want = [len(files[(lang, g)]) if (lang, g) in files else -1 for g in range(16)]
    check(sz == want, f"FileSizeTable_{tag}: ids 0x12A..0x12C = {sz[:3]}, 0x12D..0x139 all -1: {sz == want}")
check(all(cstr(u64(0x01E0E530 + (0x12A + g) * 8)).endswith(f"menuquest{g:02d}.bin") for g in range(16)),
      "kind-7 path slots 01E0E530[0x12A+g] name menuquest{g:02d}.bin, g = 0..15; 0x129 = "
      + cstr(u64(0x01E0E530 + 0x129 * 8)).split("\\")[-1] + ", 0x128 = " + cstr(u64(0x01E0E530 + 0x128 * 8)).split("\\")[-1])

print("\n=== 4. static image")
def ins(a, mn, frag):
    x = ins_at(a)
    check(x is not None and x.mnemonic == mn and frag in x.op_str, f"{a:08X}: expect `{mn} ..{frag}..` got `{x.mnemonic} {x.op_str}`")
ins(0x003800DF, "movzx", "eax, byte ptr [rdx + 1]")   # request type
ins(0x003800EA, "cmp", "al, 2")
ins(0x0038011C, "movzx", "ebx, byte ptr [rdx + 2]")   # group
ins(0x00380120, "add", "ebx, 0x12a")
ins(0x00380112, "mov", "ebx, 0x129")                  # type 4: menuquest.nfs
ins(0x00380137, "mov", "r8d, ebx")
ins(0x0038013A, "mov", "edx, 7")
ins(0x00380145, "call", "0x249210")
ins(0x00380155, "mov", "rax, qword ptr [rbx + 8]")
ins(0x0038005D, "mov", "qword ptr [rsi + 0x10], rax")  # slot +0x10 = blob
ins(0x0037FD93, "movzx", "r9d, byte ptr [r11 + r10*8 + 0x10]")   # qstd payload low byte = group
ins(0x0037FDE9, "mov", "byte ptr [rbx + 0xe7], r8b")             # ordinal within group
ins(0x0037FE13, "mov", "byte ptr [rsp + 0x22], r9b")
ins(0x0037E96C, "lea", "rbp, [rax + 1]")                          # rec = blob + 16 + 20*k
ins(0x0037E970, "lea", "rbp, [rax + rbp*4]")
ins(0x0037E974, "lea", "rbp, [rdi + rbp*4]")
ins(0x0037E9D3, "movzx", "ecx, word ptr [rdi + 0xa]")            # section 5
ins(0x0037E9E0, "imul", "rax, rdx, 0x1c")
ins(0x0037E9FE, "movzx", "edx, word ptr [rdi]")                   # section 0
ins(0x0037EA01, "movzx", "eax, word ptr [rbp]")
ins(0x0037EA27, "movzx", "edx, word ptr [rdi + 2]")               # section 1
ins(0x0037EA2B, "movzx", "eax, word ptr [rbp + 2]")
ins(0x0037EA51, "movzx", "edx, word ptr [rdi + 4]")               # section 2
ins(0x0037EA55, "movzx", "eax, word ptr [rbp + 4]")
ins(0x0037EF01, "movzx", "ebx, word ptr [rcx + 0xa]")             # section 5 again
ins(0x0037EF0A, "imul", "rcx, rax, 0x1c")
ins(0x0037EFAA, "movzx", "eax, byte ptr [rax + rbx]")             # nibble fetch
ins(0x0037FEC4, "movzx", "ecx, word ptr [rcx + 6]")               # section 3 (header)
ins(0x0037FECD, "movzx", "eax, word ptr [rdx + 6]")               # section 3 (record)
ins(0x0037FEE2, "call", "0x473d50")
ins(0x0037FF1B, "movzx", "ecx, word ptr [rbx + 8]")               # section 4
ins(0x0037FF24, "movzx", "eax, word ptr [rdi + 8]")
ins(0x0037FF39, "call", "0x473db0")
ins(0x00473D5A, "mov", "eax, dword ptr [rcx + 4]")                # QHD0 count
ins(0x00473D80, "add", "dword ptr [rcx + rdx], r9d")              # in-place 32-bit relocation
ins(0x00473D9E, "or", "dword ptr [rdx + 4], 0x80000000")
ins(0x00473DE0, "add", "dword ptr [rcx + rdx], r9d")
ins(0x00473B7A, "movsxd", "rcx, dword ptr [rax + rdx*4 + 8]")     # sign-extended 32-bit pointer
ins(0x00473BDB, "movzx", "eax, byte ptr [r11 + 1]")
ins(0x00473CDF, "movzx", "eax, word ptr [rcx + rax*4 + 4]")

print("\n=== 5. raw rip sweep of the QHD/QHT pointer globals")
refs = raw_rip_refs(0x02CA6C68, 0x02CA6C78)
fns = collections.Counter(owner(r[0]) for r in refs)
for a_, mn, op, t in refs:
    print(f"   {a_:08X} {mn} {op} -> {t:08X}  fn {owner(a_) or 0:08X}")
check(set(fns) == {0x473B50, 0x473B60, 0x473B70, 0x473BB0, 0x473CC0, 0x473D50, 0x473DB0},
      "02CA6C68 (QHD) / 02CA6C70 (QHT) are touched only by 00473B50/60 (clear), 00473D50/DB0 (install), "
      "00473B70/BB0 (QHD read), 00473CC0 (QHT read)")

print("\n=== 6. id sweep with control")
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
ctl = [f for f in sweep(0x128, 0x128) if f[2]]
print("   control 0x128 (menuquest.dat, documented at 0037F740 and 00577057):", [(f"{f[0]:08X}", f[1]) for f in ctl])
check({f[2] for f in ctl} >= {0x0037F740, 0x00577057}, "positive control: sweep finds both documented menuquest.dat requests")
hits = [f for f in sweep(0x129, 0x139) if f[2]]
for f in hits:
    print(f"   {f[0]:08X} {f[1]:30s} -> request call {f[2]:08X}  fn {owner(f[0]) or 0:08X}")
check([f[0] for f in hits] == [0x00380112, 0x00380120],
      "only 003800D0 forms a kind-7 request id in 0x129..0x139 (0x129 .nfs, and 0x12A + group)")
print(f"\nFAILS {FAILS}")
