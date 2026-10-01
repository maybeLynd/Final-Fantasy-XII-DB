"""Falsification pass 1 on three map-menu data-format pages (OPUS, 2026-09-29): amap-menumap-area-table,
gmap-menumap-guide-texts and menuquest-bin-quest-detail-tables. Every file is read from the INSTALLED ARCHIVE through
agent_flow/tools/vbfextract.py - not from the extracted tree SWE2-DATA's checks read - and every code clause from the
shipping image. SWE2-DATA's check_amap/check_gmap/check_menuquest are carried, not re-run.

amap (worldmap/menumap_area.bin)
  A1  all nine copies byte-identical, 396 B; header 'amap', 0xC9, offsets 0x10 / 0x38 / 0x74 / 0xEC; the four counted
      sections close back to back at 396
  A2  P: 39 bytes in 0..5; Q: 59 area indices < 39; R: 59 words, each 0xFFFF or 0x8000..0x803F; S: 39 dwords, S[0] = -1,
      S[i] = 60099 + i
  A3  the loader requests kind 7 id 0xA5 (00253917, call 00253928) and stores 020927D0 (00253930); a raw rip sweep of
      020927D0 finds 7 references - the loader's and one in each of the four accessors - against a control of 158 for the
      world-map widget 02B457E0
  A4  the accessors: Q +0x0A, S +0x0E, P +0x08, R +0x0C; unsigned bounds (jb / jae); S index 0 -> 01CEB638; R 0xFFFF -> 0,
      else the key-item query 00309EC0 with mode 0; each forms the section address as offset + the low 32 bits of the blob
gmap (worldmap/menumap_guide00..04.bin)
  G1  35 copies (9 + 8 + 6 + 6 + 6); header 'gmap', 0x64, textOff = 0x10 + 8 * count; textRel ascending or 0xFFFF; a
      TIM2 starts at align16(text end) and 'TIM2' + 16 + the picture sizes ends at EOF in 30; the five Latin guide00 copies
      carry none and their tim2Off is at or past EOF
  G2  the request is kind 7 id 0x496 + the selection record's byte +4 (003C1EA7 / 003C1EB1 / 003C1EBC) into widget +0xF8;
      byte +4 of all 77 section-3 records of menumap_common.bin is 0 in all nine locales
  G3  the readers: count +0x0E with unsigned bounds, textRel at entry +4 (0xFFFF -> null), textOff +0x08, tim2Off +0x0A
      (0xFFFF -> null)
menuquest (quest/menuquest00..02.bin)
  M1  27 copies; off[0] = 16 + 20 N and off[5] + 28 N = size; N = 19 / 45 / 2 by group in all nine locales; pad 0xFFFF;
      every record's rel[5] = 0 and fill words 0x0FFF; sections 3 and 4 start 'QHD0' / 'QHT0'; section-5 bytes 26-27 zero
  M2  the request is kind 7 id 0x12A + group (0038011C / 00380120, call 00380145) or 0x129 on the other arm (00380112);
      00473D50 publishes the chunk at 02CA6C68, adds the chunk's low 32 bits to each offset from +8, and sets bit 31 of
      the count (00473D9E)
"""
import collections, io, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "agent_flow", "tools"))
import vbfextract as V  # noqa: E402
VBF = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass


def body(fa, n=None):
    return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa)}


def rip_to(a, target):
    x = next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
    m = re.search(r"rip ([+-]) 0x([0-9a-f]+)", x.op_str)
    return m is not None and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == target


tx = [s for s in SECS if s[0] == ".text"][0]
T0, TR, TN = tx[1], tx[3], tx[4]


def rip_refs(target):
    """{displacement address: every decodable instruction start} for rip-relative references to `target` in .text: a disp32
    candidate for each immediate width, confirmed by an instruction that starts 2-7 bytes earlier and ends where that width
    says. One reference is one displacement; its start is ambiguous only by a REX byte, so all starts are kept."""
    text = blob[TR:TR + TN]; out = {}
    for k in (0, 1, 2, 4):
        for p in range(0, TN - 4 - k):
            if T0 + p + 4 + k + struct.unpack_from("<i", text, p)[0] != target:
                continue
            for back in range(2, 8):
                s = p - back
                if s < 0:
                    continue
                ins = next(md.disasm(text[s:s + 16], T0 + s), None)
                if ins is not None and ins.size == back + 4 + k and "rip" in ins.op_str:
                    out.setdefault(T0 + p, set()).add(ins.address)
    return out


f = open(VBF, "rb"); NAMES, BLOCKS = V.load_index(f)
member = lambda path: V.read_entry(f, NAMES, BLOCKS, path)
MY = "ps2data/image/ff12/myoshiok/"
LOC = sorted({k[len(MY):].split("/")[0] for k in NAMES if k.startswith(MY) and k.endswith("/worldmap/menumap_area.bin")})
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

# ---------------------------------------------------------------- amap
A = {l: member(MY + l + "/worldmap/menumap_area.bin") for l in LOC}
a = A[LOC[0]]
offs = struct.unpack_from("<4H", a, 8)
pn, qn, rn, sn = a[0x10], a[0x38], u16(a, 0x74), u32(a, 0xEC)
check("A1", len(LOC) == 9 and len(set(A.values())) == 1 and len(a) == 396 and a[:4] == b"amap" and u32(a, 4) == 0xC9
      and offs == (0x10, 0x38, 0x74, 0xEC) and 0x10 + 1 + pn == 0x38 and 0x38 + 1 + qn == 0x74 and 0x74 + 2 + 2 * rn == 0xEC
      and 0xEC + 4 + 4 * sn == 396, "%d locales, one content, %d B, offsets %s, counts %d/%d/%d/%d" % (len(LOC), len(a), [hex(x) for x in offs], pn, qn, rn, sn))
P = list(a[0x11:0x11 + pn]); Q = list(a[0x39:0x39 + qn]); R = struct.unpack_from("<%dH" % rn, a, 0x76); S = struct.unpack_from("<%di" % sn, a, 0xF0)
check("A2", pn == 39 and set(P) <= set(range(6)) and qn == 59 and max(Q) < 39 and rn == 59
      and all(r == 0xFFFF or 0x8000 <= r <= 0x803F for r in R) and sn == 39 and S[0] == -1 and all(S[i] == 60099 + i for i in range(1, 39)),
      "P values %s; Q max %d; R %d set / %d none; S[1..38] = 60099 + i" % (sorted(set(P)), max(Q), sum(r != 0xFFFF for r in R), sum(r == 0xFFFF for r in R)))
L = body(0x00253780)
refs, ctl = rip_refs(0x020927D0), rip_refs(0x02B457E0)
acc = {0x00254380: 0x00254380, 0x002543A0: 0x002543A0, 0x002543D0: 0x002543D0, 0x002543F0: 0x002543F4}
starts = set().union(*refs.values()) if refs else set()
in_loader = [d for d in refs if 0x00253780 <= d < 0x00253780 + sizes[0x00253780]]
check("A3", L.get(0x00253917) == "mov r8d, 0xa5" and L.get(0x0025390D) == "mov edx, 7" and L.get(0x00253928) == "call 0x249180"
      and rip_to(0x00253930, 0x020927D0) and L[0x00253930].startswith("mov qword ptr [rip")
      and len(refs) == 7 and len(in_loader) == 3 and all(v in starts for v in acc.values()) and len(ctl) == 158,
      "020927D0: %d rip references (loader %d, accessors %d); control 02B457E0: %d" % (len(refs), len(in_loader), sum(v in starts for v in acc.values()), len(ctl)))
q, s_, p_, r_ = body(0x00254380), body(0x002543A0), body(0x002543D0), body(0x002543F0)
check("A4", q.get(0x00254387) == "movzx edx, word ptr [rax + 0xa]" and q.get(0x0025438B) == "add edx, eax" and q.get(0x00254392) == "jb 0x254397"
      and s_.get(0x002543A7) == "movzx edx, word ptr [rax + 0xe]" and s_.get(0x002543AF) == "jne 0x2543b9" and rip_to(0x002543B1, 0x01CEB638)
      and s_.get(0x002543BB) == "jae 0x2543b1" and s_.get(0x002543C3) == "jmp 0x2f9920"
      and p_.get(0x002543D7) == "movzx edx, word ptr [rax + 8]" and p_.get(0x002543E2) == "jb 0x2543e7"
      and r_.get(0x002543FB) == "movzx edx, word ptr [rax + 0xc]" and r_.get(0x0025440F) == "jae 0x254403"
      and r_.get(0x00254418) == "mov eax, 0xffff" and r_.get(0x00254420) == "je 0x254403" and r_.get(0x00254422) == "xor edx, edx"
      and r_.get(0x00254424) == "call 0x309ec0" and r_.get(0x0025442D) == "setne cl",
      "Q +0x0A, S +0x0E, P +0x08, R +0x0C; unsigned bounds; S 0 -> 01CEB638; R 0xFFFF -> 0, else 00309EC0(R, 0) as a bool")

# ---------------------------------------------------------------- gmap
G = {(l, n): member(MY + l + "/worldmap/menumap_guide%02d.bin" % n) for l in LOC for n in range(5)
     if (MY + l + "/worldmap/menumap_guide%02d.bin" % n) in NAMES}
per = collections.Counter(n for _l, n in G)
bad, tim, notim = [], 0, []
for (l, n), b in G.items():
    cnt, toff, tim2 = u16(b, 0xE), u16(b, 8), u16(b, 0xA)
    rel = [u16(b, 0x10 + 8 * i + 4) for i in range(cnt)]
    live = [x for x in rel if x != 0xFFFF]
    ok = b[:4] == b"gmap" and u32(b, 4) == 0x64 and toff == 0x10 + 8 * cnt and live == sorted(live)
    end = toff + (max(live) if live else 0)
    end = b.index(b"\0", end) + 1 if live else toff
    if tim2 != 0xFFFF and tim2 + 16 <= len(b) and b[tim2:tim2 + 4] == b"TIM2":
        np_ = u16(b, tim2 + 6); o = tim2 + 16
        for _ in range(np_):
            o += u32(b, o)
        ok = ok and tim2 == (end + 15) // 16 * 16 and o == len(b); tim += 1
    else:
        notim.append((l, n, tim2 >= len(b)))
    if not ok:
        bad.append((l, n))
check("G1", len(G) == 35 and [per[n] for n in range(5)] == [9, 8, 6, 6, 6] and not bad and tim == 30
      and sorted((l, n) for l, n, _ in notim) == sorted((l, 0) for l in ("us", "de", "es", "fr", "it")) and all(past for _l, _n, past in notim),
      "%d copies %s; closure failures %s; TIM2 in %d; none in %s (offset at or past EOF: %s)"
      % (len(G), [per[n] for n in range(5)], bad or "none", tim, sorted("%s%d" % (l, n) for l, n, _ in notim), all(p for *_x, p in notim)))
C = body(0x003C1DF0)
cm = {l: member(MY + l + "/worldmap/menumap_common.bin") for l in LOC}
b4 = collections.Counter()
for l, b in cm.items():
    n = u32(b, 0x474)
    b4.update(b[0x478 + 8 * i + 4] for i in range(n))
nrec = {u32(b, 0x474) for b in cm.values()}
check("G2", C.get(0x003C1EA7) == "movzx r8d, byte ptr [rdx + 4]" and C.get(0x003C1EB1) == "add r8d, 0x496" and C.get(0x003C1EBC) == "call 0x249210"
      and C.get(0x003C1ECC) == "mov qword ptr [rcx + 0xf8], rdx" and C.get(0x003C1E9D) == "mov rdx, qword ptr [rcx + 0xf0]"
      and nrec == {77} and all(0x478 + 8 * 77 == len(b) for b in cm.values()) and set(b4) == {0},
      "id 0x496 + record byte +4; section 3 holds %s records closing at EOF in all %d locales; byte +4 values %s" % (sorted(nrec), len(cm), dict(b4)))
R1, R2 = body(0x003BD890), body(0x003BD8F0)
check("G3", R1.get(0x003BD8BD) == "movzx r8d, word ptr [rdx + 6]" and R1.get(0x003BD8C2) == "movzx eax, word ptr [rcx + 0xe]"
      and R1.get(0x003BD8C9) == "jb 0x3bd8ce" and R1.get(0x003BD8CE) == "movzx edx, word ptr [rcx + r8*8 + 0x14]" and R1.get(0x003BD8DC) == "je 0x3bd8cb"
      and R1.get(0x003BD8DE) == "movzx eax, word ptr [rcx + 8]" and R1.get(0x003BD89C) == "test byte ptr [rax + 0xd0], 0x40"
      and R2.get(0x003BD8F8) == "movzx eax, word ptr [rcx + 0xe]" and R2.get(0x003BD8FE) == "jae 0x3bd8f5"
      and R2.get(0x003BD915) == "movzx eax, word ptr [rcx + 0xa]" and R2.get(0x003BD91F) == "mov qword ptr [r8], 0"
      and R2.get(0x003BD930) == "movzx edx, word ptr [rdx + 4]" and R2.get(0x003BD938) == "je 0x3bd8f5" and R2.get(0x003BD93A) == "movzx eax, word ptr [rcx + 8]",
      "count +0x0E unsigned; entry +4 textRel (0xFFFF -> null); textOff +0x08; tim2Off +0x0A (0xFFFF -> null); widget +0xD0 bit 0x40 gate")

# ---------------------------------------------------------------- menuquest
M = {(l, g): member(MY + l + "/quest/menuquest%02d.bin" % g) for l in LOC for g in range(3)}
badm, Ns = [], collections.defaultdict(set)
for (l, g), b in M.items():
    off = struct.unpack_from("<6H", b, 0); pad, n = u16(b, 0xC), u16(b, 0xE); Ns[g].add(n)
    recs = [struct.unpack_from("<10H", b, 0x10 + 20 * k) for k in range(n)]
    ok = (off[0] == 16 + 20 * n and off[5] + 28 * n == len(b) and pad == 0xFFFF and all(r[5] == 0 and r[6:] == (0x0FFF,) * 4 for r in recs)
          and b[off[3]:off[3] + 4] == b"QHD0" and b[off[4]:off[4] + 4] == b"QHT0"
          and all(b[off[5] + 28 * k + 26:off[5] + 28 * k + 28] == b"\0\0" for k in range(n)))
    if not ok:
        badm.append((l, g))
check("M1", len(M) == 27 and not badm and [sorted(Ns[g]) for g in range(3)] == [[19], [45], [2]],
      "27 copies; closure/record/chunk failures %s; N by group %s" % (badm or "none", [sorted(Ns[g]) for g in range(3)]))
Q_, K_ = body(0x003800D0), body(0x00473D50)
check("M2", Q_.get(0x0038011C) == "movzx ebx, byte ptr [rdx + 2]" and Q_.get(0x00380120) == "add ebx, 0x12a" and Q_.get(0x00380112) == "mov ebx, 0x129"
      and Q_.get(0x00380137) == "mov r8d, ebx" and Q_.get(0x0038013A) == "mov edx, 7" and Q_.get(0x00380145) == "call 0x249210"
      and rip_to(0x00473D50, 0x02CA6C68) and K_.get(0x00473D6D) == "mov ecx, 8" and K_.get(0x00473D80) == "add dword ptr [rcx + rdx], r9d"
      and K_.get(0x00473D57) == "mov r9, rcx" and K_.get(0x00473D9E) == "or dword ptr [rdx + 4], 0x80000000",
      "kind 7 id 0x12A + group (0x129 on the other arm); chunk at 02CA6C68, offsets from +8 rebased by its low 32 bits, bit 31 set")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
