"""DD residue batch 9 (SWE2-CONTRACT, 2026-09-30): checks behind the reconciled residue of two VBF pages.

Run: python -B b9_vbf_nmb.py   (FAILS 0)      archive: $FF12_VBF, else the Steam install path below

Page 1 - how-the-bigfile-index-loads-and-is-verified.md (the per-entry record layout)
  V1  the opener 001F4340 parses the index from the verified buffer: a u32 count at +8, count x 16-byte keys at +0x10,
      count x 32-byte records after them, a u32 string-table length that counts itself, then the u16 block table
  V2  the block count: the last record's first block (+0) plus its size (+8) in 64 KiB blocks, rounded up
  V3  the per-block "compressed" byte array: 0 when the stored block size is 0, or when an entry's last block stores
      exactly size mod 64 KiB; 1 otherwise
  V4  per record: the name offset (+0x18) is rebased in place to a char*; key i and record i go into a red-black
      tree node {links, key +0x18/+0x20, record +0x28}
  V5  the lookup 001F47D0 compares the two key halves as signed qwords and returns node +0x28; 0019AEE0 builds the
      key with CALG_MD5 over the caller's string
  V6  the read path: 0019A770 reads record +0 (first block) and +0x10 (archive offset), walks the u16 table (0 = 64 KiB);
      the stream handle clamps reads to +8 (size)
  V7  0019AA20 inflates a block whose flag is 1 with zlib's uncompress 0080C5A0 (zlib 1.2.11) and copies it raw
      otherwise
  V8  structflow from every load of the handle's record pointer: the record is read at +0, +8 and +0x10 only; the one
      escape (request +0x60) has no reader in the request's life cycle
  V9  15 reader handles of 0x30 bytes are fopen'd on the archive path at open; a 16th is made on demand
  A1-A9  the installed archive, header only, plus a three-entry payload sample decoded by the engine's rule

Page 2 - St2e-Carriers/area-nmb-index.md (the five requests, kind 26, where the arrays end)
  N1  002ED6F0 decodes a packed id: letter = bits 16..23, jump table over 'C'..'w'; the kind set it can emit
  N2  002E98F0 wraps it and adds 0x33 to a kind-1 index
  N3  four of the five sites take (kind, index) from these decoders, so none can ask for 26
  N4  001DA31B takes them from 0032F170 with manager 0, i.e. kind 5 at id*3
  N5  the eleven ResourcePath_Get sites are exactly the page's; ResourcePath_Copy's one site passes kind 4
  N6  kind 26 does resolve to a path, through the request machine: 0032E620 -> 0032E870 -> 0032E070 -> 0046E030 ->
      002DF780 (size test, then g_pathTables[kind][index]); 00324510 is the one literal-0x1A issuer, bounded at 301 ids
  N7  where the kind-37 arrays end: both end 2,964 slots after their base (next base), and every .fst sizes kind 37
      only at ids 120..2,963; kind 26: the .fst sizes ids up to 320 (321 entries)
  N8  the ch .nmb array is installed for regions 7, 8 and 11, which index KR, CH and CN in the language-name table
"""
import collections, hashlib, os, re, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
FSTDIR = os.path.join(os.path.dirname(VBF), "FileSizeTables")
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


def body(f):
    return list(T.R.md.disasm(T.R.at(f, T.sizes()[f]), f))


def q(a):
    return struct.unpack("<Q", T.R.at(a, 8))[0]


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
sc = T.scan()

# ---------------------------------------------------------------- page 1: the index record layout, from the code
pin("V1 index base", 0x0019B0E5, "call 0x1f4340")
pin("V1 r15 = the verified index buffer", 0x001F453B, "mov r15, qword ptr [rbx]")
pin("V1 keys start at +0x10", 0x001F453E, "lea rdx, [r15 + 0x10]")
pin("V1 count is the u32 at +8", 0x001F4542, "mov ecx, dword ptr [r15 + 8]")
pin("V1 16 bytes per key", 0x001F4549, "shl r12d, 4")
pin("V1 records follow the keys", 0x001F454D, "add r12, rdx")
pin("V1 32 bytes per record", 0x001F4550, "shl rcx, 5")
pin("V1 string table starts 4 bytes past the records", 0x001F4554, "lea r13, [rcx + 4]")
pin("V1 its u32 length sits just before", 0x001F455B, "mov ecx, dword ptr [r13 - 4]")
pin("V1 the length counts itself", 0x001F455F, "add rcx, -4")
pin("V1 block table = string table end", 0x001F4566, "mov qword ptr [rbx + 0x68], rcx")
pin("V2 last record's size", 0x001F4574, "mov r8, qword ptr [rcx + r12 + 8]")
pin("V2 in 64 KiB blocks", 0x001F4579, "shr r8, 0x10")
pin("V2 plus its first block (+0)", 0x001F457D, "add r8d, dword ptr [rcx + r12]")
pin("V2 block count stored", 0x001F4581, "mov dword ptr [rbx + 0x60], r8d")
pin("V2 a partial tail adds one", 0x001F458F, "movzx eax, word ptr [rcx + r12 + 8]")
pin("V3 flag array sized by the block count", 0x001F45A9, "mov qword ptr [rbx + 0x70], rax")
pin("V3 stored size 0?", 0x001F45C4, "cmp word ptr [rax + rcx*2], di")
pin("V3 -> flag 0", 0x001F45CE, "mov byte ptr [rcx + rax], dil")
pin("V3 else flag 1", 0x001F45D4, "mov byte ptr [rcx + rax], 1")
pin("V3 per record: size mod 64 KiB", 0x001F463C, "movzx r8d, ax")
pin("V3 last block = first + blocks - 1", 0x001F464B, "add ecx, dword ptr [r10]")
pin("V3 stored size == size mod 64 KiB?", 0x001F4658, "cmp rcx, r8")
pin("V3 -> that tail's flag 0", 0x001F4661, "mov byte ptr [rdx + rax], 0")
pin("V4 name offset rebased to a pointer", 0x001F462D, "add qword ptr [r10 + 0x18], r13")
pin("V4 key i (r9 = 2i, 8-byte scale)", 0x001F466C, "lea rdx, [rdi + r9*8]")
pin("V4 insert", 0x001F4677, "call 0x1f4720")
pin("V4 node key copied to +0x18", 0x001F477E, "movups xmmword ptr [rbx + 0x18], xmm0")
pin("V4 node value = the record", 0x001F4785, "mov qword ptr [rbx + 0x28], rax")
pin("V4 insert compares +0x18 signed", 0x001F4008, "cmp rcx, rdx")
pin("V4 then +0x20", 0x001F4013, "cmp qword ptr [r8 + 0x20], rax")
pin("V5 lookup: high half first", 0x001F47E7, "mov rax, qword ptr [rdx + 0x18]")
pin("V5 lookup: signed", 0x001F47EE, "jl 0x1f480c")
pin("V5 lookup: second half", 0x001F47F2, "cmp qword ptr [rdx + 0x20], r9")
pin("V5 hit -> node +0x28", 0x001F4824, "lea rax, [rdx + 0x28]")
pin("V5 then opens a handle on it", 0x001F4834, "jmp 0x1f4250")
pin("V5 key = CALG_MD5", 0x0019AF2B, "mov edx, 0x8003")
pin("V5 over the caller's string", 0x0019AF5B, "call qword ptr [rip + 0x7270df]")
pin("V5 the only lookup call", 0x0019AF92, "call 0x1f47d0")
check("V5 001F47D0 has one caller (0019AEE0)", sorted(sc["calls"].get(0x001F47D0, ())) == [(0x0019AEE0, 0x0019AF92)],
      str(sorted(sc["calls"].get(0x001F47D0, ()))))
pin("V6 handle +0x18 = the record", 0x002150B4, "mov qword ptr [rcx + 0x18], rdx")
pin("V6 read planner takes the record", 0x0019A791, "mov r14, qword ptr [r9 + 0x18]")
pin("V6 +0 = first block index", 0x0019A7AB, "mov ebx, dword ptr [r14]")
pin("V6 +0x10 = archive offset of that block", 0x0019A7AE, "mov rdi, qword ptr [r14 + 0x10]")
pin("V6 block table", 0x0019A7BB, "mov r9, qword ptr [r13 + 0x68]")
pin("V6 stored u16 size", 0x0019A7D9, "movzx ecx, word ptr [r9 + rax*2]")
pin("V6 0 means 64 KiB", 0x0019A7E6, "mov eax, 0x10000")
pin("V6 read clamped to +8 (size)", 0x00215143, "cmp rax, qword ptr [rcx + 8]")
pin("V6 SEEK_END from +8", 0x0021523E, "mov rcx, qword ptr [rax + 8]")
pin("V6 size getter", 0x00215284, "mov rax, qword ptr [rax + 8]")
pin("V7 flags", 0x0019AA5E, "mov r8, qword ptr [rax + 0x70]")
pin("V7 flag test", 0x0019AA93, "cmp byte ptr [rbp + r8], bl")
pin("V7 compressed -> uncompress", 0x0019AAAE, "call 0x80c5a0")
pin("V7 raw -> 0x200 x 0x80 copy", 0x0019AA7D, "mov r12d, 0x200")
pin("V7 0080C5A0 is the uncompress shim", 0x0080C5AE, "call 0x80c5c0")
pin("V7 which inits inflate with version", 0x0080C5FD, "lea rdx, [rip + 0x14bada0]")
check("V7 version string", T.cstr(0x01CC73A4) == "1.2.11", repr(T.cstr(0x01CC73A4)))
# V8: every access through the record pointer, from each load of it
import structflow as S  # noqa: E402
g = S.Flow([0, 4, 8, 0x10, 0x18], 3, stride=0x20, slot=0,
           seed_loads={(0x0019A770, 0x18), (0x00215110, 0x18), (0x00215220, 0x18), (0x00215280, 0x18)})
g.run([0x0019A770, 0x00215110, 0x00215220, 0x00215280])
offs = collections.Counter(h[4] for h in g.hits)
check("V8 record reads: +0 x1, +8 x5, +0x10 x1, nothing at +4 or +0x18", dict(offs) == {0: 1, 8: 5, 16: 1} and not g.unk,
      str(sorted(("%08X" % h[1], h[4]) for h in g.hits)))
check("V8 the one escape is the request's +0x60", [(e[1], e[3]) for e in g.esc] == [(0x0019A834, "mov qword ptr [rax + 0x60], r14")],
      str(sorted(g.esc)))
g2 = S.Flow([0x60], 3, stride=0x1000, slot=0, seed_calls={(0x0019AFE0, 0x0019A770)})
g2.run([0x0019AFE0])
check("V8 request +0x60 is read nowhere in its life cycle", not g2.hits and not g2.unk and
      sorted(g2.entry) == [0x0019A860, 0x0019A9B0, 0x0019AA20, 0x0019AFE0, 0x0019B130],
      "walked " + " ".join("%08X" % f for f in sorted(g2.entry)))
pin("V9 handle pool 0x2D8 = 8 + 15 x 0x30", 0x001F4687, "mov ecx, 0x2d8")
pin("V9 fifteen", 0x001F4695, "mov esi, 0xf")
pin("V9 each opened on the archive path", 0x001F46F2, "call 0x215290")
pin("V9 with fopen", 0x002152AD, "call qword ptr [rip + 0x6adc45]")
pin("V9 a 16th on demand when all are busy", 0x001F42DC, "lea ecx, [rbx + 0x30]")
pin("V9 and opened the same way", 0x001F4308, "call 0x215290")
pin("V9 a lookup takes the first handle whose in-use byte is 0", 0x001F4290, "cmp byte ptr [rax], bl")
pin("V9 of fifteen", 0x001F429E, "cmp r8, 0xf")
pin("V9 blocks arrive through CRT fread (the opener's import)", 0x0019A8D1, "call qword ptr [rip + 0x728619]")
check("V9 that slot is the opener's fread slot 008C2EF0", 0x0019A8D1 + 6 + 0x728619 == 0x008C2EF0 == 0x001F43D1 + 6 + 0x6ceb19)

# ---------------------------------------------------------------- page 1: the installed archive
f = open(VBF, "rb")
magic, hl, cnt, hi32 = struct.unpack("<4sIII", f.read(16))
f.seek(0)
H = f.read(hl)
fsize = os.path.getsize(VBF)
check("A1 header: SRYK, u32 index length, u32 count, u32 zero", (magic, hi32) == (b"SRYK", 0), "%d B, %d entries" % (hl, cnt))
ent = 16 + cnt * 16
st = ent + cnt * 32
slen = struct.unpack_from("<I", H, st)[0]
bl = st + slen
nblk = (hl - bl) // 2
E = [struct.unpack_from("<IIQQQ", H, ent + i * 32) for i in range(cnt)]
B = struct.unpack_from("<%dH" % nblk, H, bl)
strs = H[st + 4:st + slen]
nb = lambda s: (s >> 16) + (1 if s & 0xFFFF else 0)
check("A2 block table fills the header exactly", (hl - bl) % 2 == 0 and E[-1][0] + nb(E[-1][2]) == nblk,
      "%d blocks = last first-block %d + %d" % (nblk, E[-1][0], nb(E[-1][2])))
names = [strs[e[4]:strs.index(b"\0", e[4])] for e in E]
check("A3 key i = MD5(name i)", all(hashlib.md5(names[i]).digest() == H[16 + i * 16:32 + i * 16] for i in range(cnt)), "%d of %d" % (cnt, cnt))
check("A3 the 16-byte keys are unique", len({H[16 + i * 16:32 + i * 16] for i in range(cnt)}) == cnt)
tk = [struct.unpack_from("<qq", H, 16 + i * 16) for i in range(cnt)]
check("A3 the key array is not in tree order (the tree is the only index)", any(tk[i] > tk[i + 1] for i in range(cnt - 1)))
live = [e for e in E if e[2]]
dead = [i for i, e in enumerate(E) if not e[2]]
check("A4 the 26 zero-size entries: +4 = 1,703,388, all jsondata/cutscenes/*.json",
      len(dead) == 26 and {E[i][1] for i in dead} == {1703388} and all(names[i].startswith(b"jsondata/cutscenes/") and names[i].endswith(b".json") for i in dead))
check("A4 +4 equals +0 in every entry with bytes", all(e[1] == e[0] for e in live) and len(live) == cnt - 26,
      "%d of %d; the other %d have size 0" % (sum(e[1] == e[0] for e in E), cnt, cnt - len(live)))
cs = [0]
for b in B:
    cs.append(cs[-1] + (b or 0x10000))
check("A5 +0x10 = index length + stored sizes of all earlier blocks", all(e[3] == hl + cs[e[0]] for e in live),
      "%d entries" % len(live))
check("A5 payload runs from the index end to the digest", hl + cs[-1] == fsize - 16, "%d + %d = %d - 16" % (hl, cs[-1], fsize))
check("A6 blocks are contiguous in record order", all(E[i][0] + nb(E[i][2]) == E[i + 1][0] for i in range(cnt - 1) if E[i][2]))
check("A7 name offsets ascend and index a lower-case table", all(E[i][4] < E[i + 1][4] for i in range(cnt - 1)) and
      not any(c in range(65, 91) for c in strs), "first %r" % names[0].decode())
rawtail = sum(1 for e in live if e[2] & 0xFFFF and B[e[0] + nb(e[2]) - 1] == e[2] & 0xFFFF)
zeroes = sum(1 for b in B if b == 0)
check("A8 raw blocks: %d full (stored 0), %d tails (stored == size mod 64 KiB)" % (zeroes, rawtail), rawtail > 0 and zeroes > 0)


def decode(e):
    out, pos = bytearray(), e[3]
    n = nb(e[2])
    for k in range(n):
        s = B[e[0] + k]
        last = k == n - 1
        flag = 0 if (s == 0 or (last and e[2] & 0xFFFF and s == e[2] & 0xFFFF)) else 1
        f.seek(pos)
        d = f.read(s or 0x10000)
        blk = zlib.decompress(d) if flag else d
        want = (e[2] & 0xFFFF or 0x10000) if last else 0x10000
        if len(blk) != want:
            return None
        out += blk
        pos += s or 0x10000
    return bytes(out)


pick = {}
for i, e in enumerate(E):
    if not e[2] or e[2] > 0x40000:
        continue
    blks = [B[e[0] + k] for k in range(nb(e[2]))]
    last_raw = e[2] & 0xFFFF and blks[-1] == e[2] & 0xFFFF
    if 0 in blks and "full-raw" not in pick:
        pick["full-raw"] = i
    if last_raw and "tail-raw" not in pick:
        pick["tail-raw"] = i
    if not last_raw and 0 not in blks and len(blks) > 1 and "all-zlib" not in pick:
        pick["all-zlib"] = i
    if len(pick) == 3:
        break
res = {k: decode(E[i]) for k, i in pick.items()}
check("A9 engine-rule decode of three entries gives their sizes", len(pick) == 3 and all(res[k] is not None and len(res[k]) == E[pick[k]][2] for k in pick),
      "; ".join("%s %s %d B" % (k, names[i].decode(), E[i][2]) for k, i in pick.items()))

# ---------------------------------------------------------------- page 2: the five sites and kind 26
pin("N1 packed id: number = low 16 bits", 0x002ED6F0, "movzx r10d, cx")
pin("N1 letter = bits 16..23", 0x002ED6FA, "movzx eax, cl")
pin("N1 from 'C'", 0x002ED6FD, "add eax, -0x43")
pin("N1 to 'w'", 0x002ED700, "cmp eax, 0x34")
pin("N1 else the default", 0x002ED703, "ja 0x2ed840")
pin("N1 default kind 1", 0x002ED840, "mov eax, 1")
bm = T.R.at(0x002ED888, 0x35)
dw = struct.unpack("<13I", T.R.at(0x002ED854, 52))
kinds = {}
for k in range(0x35):
    tgt = 0x00120000 + dw[bm[k]]
    head = list(T.R.md.disasm(T.R.at(tgt, 40), tgt))[:6]
    kd = [i for i in head if i.mnemonic == "mov" and i.op_str.startswith("edx, 0x")]
    kinds[chr(0x43 + k)] = int(kd[0].op_str.split(",")[1], 16) if kd else (1 if tgt == 0x002ED840 else None)
emit = set(kinds.values())
check("N1 the kinds 002ED6F0 can emit", emit == {1, 13, 14, 15, 16, 18, 19, 20, 22, 23, 24, 25, 34} and max(bm) < 13,
      " ".join("%s:%d" % (c, v) for c, v in kinds.items() if v != 1) + " others:1")
check("N1 26 is not among them", 26 not in emit)
pin("N2 002E98F0 calls it", 0x002E9900, "call 0x2ed6f0")
pin("N2 kind 1?", 0x002E9905, "cmp dword ptr [rbx], 1")
pin("N2 then index + 0x33", 0x002E990A, "add dword ptr [rdi], 0x33")
for site, dec, kslot, islot in ((0x001BB397, (0x001BB38A, "call 0x2e98f0"), (0x001BB393, "mov ecx, dword ptr [rsp + 0x68]"), (0x001BB382, "lea rdx, [rsp + 0x68]")),
                                (0x001F5E64, (0x001F5E59, "call 0x2e98f0"), (0x001F5E61, "mov ecx, dword ptr [rbp + 4]"), (0x001F5E55, "lea rdx, [rbp + 4]")),
                                (0x00863144, (0x00863137, "call 0x2e98f0"), (0x00863140, "mov ecx, dword ptr [rsp + 0x24]"), (0x00863132, "lea rdx, [rsp + 0x24]")),
                                (0x002EEF70, (0x002EEF63, "call 0x2ed6f0"), (0x002EEF6C, "mov ecx, dword ptr [rsp + 0x58]"), (0x002EEF5A, "lea rdx, [rsp + 0x58]"))):
    pin("N3 %08X decoder" % site, *dec)
    pin("N3 %08X kind out-slot (rdx)" % site, *islot)
    pin("N3 %08X kind in ecx" % site, *kslot)
    pin("N3 %08X the call" % site, site, "call 0x2df980")
pin("N4 manager 0", 0x001DA2FB, "xor ecx, ecx")
pin("N4 0032F170", 0x001DA2FD, "call 0x32f170")
pin("N4 kind slot r8", 0x001DA2F7, "lea r8, [rbp + 0x50]")
pin("N4 kind in ecx", 0x001DA318, "mov ecx, dword ptr [rbp + 0x50]")
pin("N4 0032F170: manager <= 0", 0x0032F172, "jle 0x32f19e")
pin("N4 -> index id*3", 0x0032F19E, "lea eax, [rdx + rdx*2]")
pin("N4 -> kind 5", 0x0032F1A1, "mov dword ptr [r8], 5")
page_sites = [0x001B7F93, 0x001BB397, 0x001DA31B, 0x001F5E64, 0x002EEF70, 0x002FC599, 0x0032FD5A, 0x003322C8, 0x0035B8AE,
              0x00379A5A, 0x00863144]
check("N5 ResourcePath_Get's eleven sites", sorted(s for _, s in sc["calls"].get(0x002DF980, ())) == page_sites)
check("N5 ResourcePath_Copy has one site", sorted(sc["calls"].get(0x002DF880, ())) == [(0x00377DC0, 0x00377E09)])
check("N5 its function has one caller", sorted(sc["calls"].get(0x00377DC0, ())) == [(0x00378A60, 0x00378B2B)])
pin("N5 that caller passes 4 in r9d", 0x00378B1A, "mov r9d, 4")
pin("N5 r9d -> eax", 0x00377DED, "mov eax, r9d")
pin("N5 eax -> ecx (kind)", 0x00377DFD, "mov ecx, eax")
pin("N6 0032E620 hands the kind on", 0x0032E6DB, "mov ecx, edi")
pin("N6 to the slot filler", 0x0032E6DD, "call 0x32e870")
pin("N6 slot +0x21 = kind", 0x0032E943, "mov byte ptr [r10 + 0x21], r14b")
pin("N6 slot +0x24 = index", 0x0032E902, "mov dword ptr [r10 + 0x24], ebp")
check("N6 state 1 of 0032E070 is 0032E0BD", 0x00120000 + struct.unpack("<I", T.R.at(0x0032E2D0, 4))[0] == 0x0032E0BD)
pin("N6 which reads the kind", 0x0032E0D3, "movzx eax, byte ptr [rbx + 0x21]")
pin("N6 and the index", 0x0032E0DB, "mov edx, dword ptr [rbx + 0x24]")
pin("N6 into 0046E030", 0x0032E0F1, "call 0x46e030")
pin("N6 which calls the third consumer", 0x0046E03E, "call 0x2df780")
pin("N6 size test first (-1 refuses)", 0x002DF7B0, "cmp dword ptr [r15 + rax*4 + 0x2da3ee0], -1")
pin("N6 then g_pathTables[kind]", 0x002DF7BF, "mov rax, qword ptr [r15 + rbx*8 + 0x203f000]")
pin("N6 [index]", 0x002DF7CC, "mov rdi, qword ptr [rax + r14*8]")
lits = {}
for fn, site in sorted(sc["calls"].get(0x0032E620, ())):
    prior = [i for i in body(fn) if i.address < site][-14:]
    w = [i for i in prior if re.match(r"(mov|lea|movsx|movzx|xor) ecx", "%s %s" % (i.mnemonic, i.op_str))]
    m = re.match(r"mov ecx, (0x[0-9a-f]+|\d+)$", "%s %s" % (w[-1].mnemonic, w[-1].op_str)) if w else None
    lits[site] = int(m.group(1), 0) if m else None
c26 = [s for s, v in lits.items() if v == 26]
check("N6 of 0032E620's %d sites, %d pass an immediate kind and one is 0x1A (00324637)" % (len(lits), sum(v is not None for v in lits.values())),
      c26 == [0x00324637], " ".join("%08X" % s for s in c26))
pin("N6 the assembler passes its loop index as the index", 0x00324627, "mov edx, eax")
pin("N6 the assembler's bound: 301 ids", 0x00324597, "mov edi, 0x12d")
pin("N6 its {size, request id} pairs at 022C27B8, stride 8", 0x00324607, "lea rbx, [rsi + r9*8]")
pin("N6 loop test", 0x00324678, "cmp eax, edi")
# N7 array ends
fn = 0x002DF9A0
last, stores = {}, collections.defaultdict(list)
for i in body(fn):
    if i.mnemonic == "lea" and "rip +" in i.op_str:
        last[i.op_str.split(",")[0]] = i.address + i.size + i.operands[1].mem.disp
    if i.mnemonic == "mov" and i.op_str.startswith("qword ptr [rip"):
        gg, r = i.address + i.size + i.operands[0].mem.disp, i.op_str.split(", ")[1]
        if 0x0215F000 <= gg < 0x0215F148 and r in last:
            stores[(gg - 0x0215F000) // 8].append(last[r])
allb = sorted({b for v in stores.values() for b in v})
check("N7 ResourcePath_Init installs 94 array bases", len(allb) == 94)
check("N7 kind 37's two bases", stores[37] == [0x01ECBCF0, 0x01EA4D00], " ".join("%08X" % b for b in stores[37]))


def ext(p):
    s = T.cstr(p, 128) if p else None
    return "NULL" if not p else (s.rsplit(".", 1)[-1] if s and "." in s else "?")


for b in stores[37]:
    n = (min(x for x in allb if x > b) - b) // 8
    seq = [ext(q(b + 8 * i)) for i in range(n)]
    nn = [i for i in range(n) if seq[i] != "NULL"]
    per = collections.Counter(seq[i] for i in nn)
    ok = n == 2964 and len(nn) == 1316 and nn[0] == 120 and nn[-1] == 2963 and \
        all(seq[i] == ("ebp", "mot", "snd", "vpcjp")[i % 4] for i in nn)
    check("N7 kind 37 @%08X: next base after 2,964 slots; 1,316 paths at 120..2,963, stride 4" % b, ok,
          "slots %d paths %d first %s last %s %s" % (n, len(nn), nn[0] if nn else "-", nn[-1] if nn else "-", dict(per)))
fsts = sorted(x for x in os.listdir(FSTDIR) if x.lower().endswith(".fst"))
spans = set()
for x in fsts:
    t = struct.unpack("<205000I", open(os.path.join(FSTDIR, x), "rb").read())
    for k in (26, 37):
        ids = [i for i in range(5000) if t[k * 5000 + i] != 0xFFFFFFFF]
        spans.add((k, len(ids), min(ids), max(ids)))
t_us = struct.unpack("<205000I", open(os.path.join(FSTDIR, "FileSizeTable_US.fst"), "rb").read())
hi26 = [i for i in range(301, 5000) if t_us[26 * 5000 + i] != 0xFFFFFFFF]
stems = [T.cstr(q(0x01E4DC30 + 8 * i), 128).rsplit("\\", 1)[-1] for i in hi26]
check("N6 the sized kind-26 ids past the assembler's 301 are tri_a..tri_t", hi26 == list(range(301, 321)) and
      stems == ["tri_%s.nmb" % c for c in "abcdefghijklmnopqrst"], "%s .. %s" % (stems[:1], stems[-1:]))
heads = {}
for k in (22, 14, 34):
    b = stores[k][0]
    heads[k] = T.cstr(q(b), 128).rsplit("\\", 1)[-1]
check("N1 the letters agree with the tables: kind 22 b0001.cm, 14 c1004.cm, 34 m1002.cm",
      heads == {22: "b0001.cm", 14: "c1004.cm", 34: "m1002.cm"}, str(heads))
check("N7 all %d .fst files size kind 37 at ids 120..2,963 (1,080) and kind 26 at 48..320 (166)" % len(fsts),
      len(fsts) == 12 and spans == {(37, 1080, 120, 2963), (26, 166, 48, 320)}, str(sorted(spans)))
# N8 the ch region
jt = [0x00120000 + x for x in struct.unpack("<11I", T.R.at(0x002E04B0, 44))]
pin("N8 region - 1 indexes the switch", 0x002DFBAF, "lea eax, [r8 - 1]")
pin("N8 eleven arms", 0x002DFBB3, "cmp eax, 0xa")


def reaches(start, target=0x002DFE58, stop=0x002DFF7F):
    seen, todo = set(), [start]
    while todo:
        a = todo.pop()
        while a not in seen and a != stop:
            seen.add(a)
            if a == target:
                return True
            x = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
            if x.mnemonic == "jmp":
                a = x.operands[0].imm if x.operands[0].type == 2 else stop
                continue
            if x.mnemonic.startswith("j") and x.operands[0].type == 2:
                todo.append(x.operands[0].imm)
            if x.mnemonic == "ret":
                break
            a += x.size
    return False


ch = sorted(r for r in range(1, 12) if reaches(jt[r - 1]))
lang = [T.R.at(q(0x01E88B00 + 8 * i), 8).split(b"\0")[0].decode() for i in range(12)]
check("N8 regions whose arm installs the ch array (002DFE58)", ch == [7, 8, 11] and not reaches(0x002DFF32),
      "%s -> %s" % (ch, [lang[r] for r in ch]))
check("N8 the same argument names the .fst", [lang[r] for r in (7, 8, 11)] == ["KR", "CH", "CN"])
pin("N8 (the .fst name reads the language table by r8)", 0x002E03F5, "mov r9, qword ptr [r10 + r8*8 + 0x1d68b00]")
w8 = [i.address for i in body(fn) if i.address < 0x002E03F5 and re.match(r"r8[dwb]?\b", i.op_str.split(",")[0].strip() or "-")
      and i.mnemonic not in ("cmp", "test")]
check("N8 r8 is written once before, by the argument", w8 == [0x002DF9C2], " ".join("%08X" % a for a in w8))
check("N8 and no call before that use could clobber it", not [i for i in body(fn) if i.address < 0x002E03F5 and i.mnemonic == "call"])

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
