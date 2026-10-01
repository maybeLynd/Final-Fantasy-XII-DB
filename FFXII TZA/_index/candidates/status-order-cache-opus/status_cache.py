"""status_cache.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
The status order cache at 022C8B08: its extent, its two types, its builder, its readers and its lifetime. FABLE's GA-1
(_index/candidates/ga1-status-open-bytes/kinds.md) and the 00329220 page describe it in prose; the type store had no row.

  B  BUILDER 00273BA0 (rcx = the cache): for i = 0..31, 0035D330(0x1A, i) and a copy of its 0x98-byte record into
     cache + 0xA8*i (six movups + one movsd, 00273BE6..00273C46), then the dword i at entry +0x98 (00273C41). Four passes
     of 002D02C0 (r9d = kind 1..4) and 002D03B0 fill 32 qwords each at +0x1500 / +0x1600 / +0x1700 / +0x1800 (lea r8 or rdx,
     [rbx + base + 8], then stores at -0x18 / -0x10 after +0x10): each qword = cache + 0xA8 * (signed byte from the
     enumeration's dword slots). Nothing is written at entry +0x9C..+0xA7 or at +0x1900 or above
  G  LIFETIME: 0035D490 (returns the cache) and 0035D5C0 (builds only) test dword 022C83E8 bit 0x200, run 00273BA0 when it
     is clear and set it (0035D4B1, 0035D5DC). Every rip-relative write to 022C83E8 in .text is listed and none clears bit
     0x200: the ands use 0xFFFC02EC, 0xFFFFFFBF, 0xFFFFFFEF, 0xFFFFFFEE; the xor-merges touch bits 0, 3, 4, 5; btr bit 7;
     the rest are ors. So on these paths the cache is built once and never rebuilt or released. The cache lies in .data's
     zero-filled tail. A block write over 022C83E8 through another base is not ruled out
  R  READERS: 00271FB0 selects the table by listing L (1 -> +0x1700, 2 -> +0x1600, 3 -> +0x1800, else +0x1500), walks 32
     qwords, reads entry +0x98 (00272013) as a bit index (bt edi, eax) and the L's order key at +0x23 / +0x22 / +0x24 /
     +0x21, then +0x25; 00273160 reads +0x1700 directly and entry +0x98 (002731B8); 00273380 reads entry +0x98 (002733D3);
     00273410 returns the selected table's address
  X  EXTENT: the four tables end at +0x1900 = 022CA408, where GA-1 places the next object; 022CA408 is referenced as its own
     base (rip-relative) and the cache's own references stop below it
  W  REGRESSION (FAILS before): StatusOrderCache022C8B08 (0x1900) and StatusOrderCacheEntryA8 (0xA8) in the store, tiled;
     EncodedIdQueryRecord's instance cell names the 32 embedded copies
Not claimed: what the unwritten entry bytes +0x9C..+0xA7 are for; what a -1 enumeration byte would give; the listings'
screen meaning (GA-1 has it); the enumeration's order rule.
Usage: python status_cache.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)]
def has(lo, hi, pairs):
    A = {a: (m, o) for a, m, o in dis(lo, hi)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
CACHE, FLAGS = 0x22C8B08, 0x22C83E8
bld = dis(0x273BA0, 0x273E23)
copies = [(m, o) for a, m, o in bld if 0x273BE6 <= a <= 0x273C46 and "[rax" in o]
tables = [(a, o) for a, m, o in bld if m == "lea" and re.match(r"r(8|dx|10), \[rbx \+ 0x1[5-8]08\]", o)]
kinds = [o for a, m, o in bld if m == "mov" and o.startswith("r9d, ")]
stores = [(a, o) for a, m, o in bld if m == "mov" and o.startswith("qword ptr [r") and ("- 0x18]" in o or "- 0x10]" in o)]
check("B", has(0x273BD3, 0x273C50, [(0x273BD5, ("mov", "ecx, 0x1a")), (0x273BDA, ("call", "0x35d330")), (0x273BDF, ("lea", "rsi, [rsi + 0xa8]")),
                                     (0x273C39, ("movsd", "xmm1, qword ptr [rax + 0x90]")), (0x273C41, ("mov", "dword ptr [rsi - 0x10], ebp")),
                                     (0x273C46, ("movsd", "qword ptr [rsi - 0x18], xmm1")), (0x273C4B, ("cmp", "ebp, 0x20"))])
      and [o.split(", ")[1] for m, o in copies] == ["xmmword ptr [rax]"] + ["xmmword ptr [rax + 0x%x]" % k for k in range(0x10, 0x90, 0x10)] + ["qword ptr [rax + 0x90]"]
      and [o for a, o in tables] == ["r8, [rbx + 0x1508]", "r8, [rbx + 0x1608]", "r10, [rbx + 0x1708]", "rdx, [rbx + 0x1808]"]
      and kinds == ["r9d, 1", "r9d, 2", "r9d, 3", "r9d, 4"] and len(stores) == 8
      and all(("imul", "rcx, rax, 0xa8") in [(m, o) for a, m, o in bld if t < a < t + 0x40] for t, _ in tables),
      "32 x (0x98-byte class-0x1A record + dword i at +0x98) at stride 0xA8; four 32-qword pointer tables at +0x1500/+0x1600/+0x1700/+0x1800 (kinds 1..4)")
# every rip-relative reference to FLAGS in .text, found by value, then decoded
text = [s for s in pe.sections if s.Name.startswith(b".text")][0]
tb = B + text.VirtualAddress; buf = d[text.PointerToRawData:text.PointerToRawData + text.SizeOfRawData]
refs = {}
for al in range(4):
    for j, (v,) in enumerate(struct.iter_unpack("<i", buf[al:al + (len(buf) - al) // 4 * 4])):
        i = al + 4 * j
        for tail in (0, 1, 4):
            if tb + i + 4 + tail + v == FLAGS:
                for back in range(7, 1, -1):
                    x = next(cs.disasm(buf[i - back:i - back + 16], tb + i - back, 1), None)
                    if x and x.address + x.size == tb + i + 4 + tail and "rip" in x.op_str: refs[x.address] = (x.mnemonic, x.op_str); break
writes = {a: v for a, v in refs.items() if v[1].startswith("dword ptr [rip") and v[0] in ("mov", "and", "or", "xor", "btr", "bts", "btc")}
# the stored-register sites are xor-merges of one bit, a btr of bit 7, or plain and/or masks; bind each one's modifying instruction
MERGES = {0x35C914: ("and", "ecx, 8"), 0x35C932: ("and", "edx, 0x10"), 0x35C94F: ("and", "eax, 1"), 0x35D620: ("and", "ecx, 0x20"),
          0x35D658: ("btr", "eax, 7"), 0x35D921: ("or", "eax, 0x10"), 0x35D93E: ("or", "eax, 1"), 0x35D952: ("and", "eax, 0xffffffef"),
          0x35D964: ("or", "eax, 2"), 0x35DA68: ("and", "eax, 0xffffffbf")}
movs = sorted(a for a, v in writes.items() if v[0] == "mov")
loads = sorted(a for a, v in refs.items() if v[0] == "mov" and v[1].startswith("e") and "dword ptr [rip" in v[1])
def load_of(a): return max(l for l in loads if l < a)
merge_ok = movs == sorted(MERGES) and all(MERGES[a] in [(m, o) for aa, m, o in dis(load_of(a), a)] and a - load_of(a) < 0x20 for a in movs)
ands = sorted(int(v[1].split(", ")[1], 16) for a, v in writes.items() if v[0] == "and")
setters = sorted(a for a, v in writes.items() if v == ("or", "dword ptr [rip + 0x%x], 0x200" % (FLAGS - a - 10)))
check("G", has(0x35D490, 0x35D4D1, [(0x35D496, ("test", "dword ptr [rip + 0x1f6af48], 0x200")), (0x35D4A2, ("lea", "rbx, [rip + 0x1f6b65f]")),
                                     (0x35D4AC, ("call", "0x273ba0")), (0x35D4B1, ("or", "dword ptr [rip + 0x1f6af2d], 0x200"))])
      and 0x35D4A0 + 0x1F6AF48 == FLAGS and 0x35D4A9 + 0x1F6B65F == CACHE
      and has(0x35D5C0, 0x35D5EB, [(0x35D5C4, ("test", "dword ptr [rip + 0x1f6ae1a], 0x200")), (0x35D5D0, ("lea", "rcx, [rip + 0x1f6b531]")),
                                   (0x35D5D7, ("call", "0x273ba0")), (0x35D5DC, ("or", "dword ptr [rip + 0x1f6ae02], 0x200"))])
      and 0x35D5D7 + 0x1F6B531 == CACHE and len(refs) == 48 and merge_ok and all(v & 0x200 for v in ands) and setters == [0x35D4B1, 0x35D5DC]
      and all(v[0] != "xor" and v[0] != "btr" for a, v in writes.items())
      and any(s.Name.startswith(b".data") and B + s.VirtualAddress + s.SizeOfRawData <= CACHE and CACHE + 0x1900 <= B + s.VirtualAddress + s.Misc_VirtualSize for s in pe.sections),
      "%d references to 022C83E8, %d writes; the and-masks %s all keep 0x200, the %d register stores are one-bit merges / btr 7 / or / and-masks "
      "that keep it; only 0035D4B1 and 0035D5DC touch 0x200, setting it; the cache sits in .data's zero-filled tail" % (len(refs), len(writes), [hex(v) for v in ands], len(movs)))
rd = dis(0x271FB0, 0x2720F0)
RA = {a: (m, o) for a, m, o in rd}
check("R", RA.get(0x271FFB) == ("mov", "eax, 0x1700") and RA.get(0x271FF4) == ("mov", "eax, 0x1600") and RA.get(0x271FED) == ("mov", "eax, 0x1800")
      and RA.get(0x271FE6) == ("mov", "eax, 0x1500") and RA.get(0x272004) == ("mov", "r11d, 0x20") and RA.get(0x272013) == ("mov", "eax, dword ptr [rdx + 0x98]")
      and RA.get(0x272019) == ("bt", "edi, eax") and RA.get(0x272044) == ("cmp", "byte ptr [rdx + 0x21], 0xff") and RA.get(0x27204A) == ("cmp", "byte ptr [rdx + 0x24], 0xff")
      and RA.get(0x272052) == ("cmp", "byte ptr [rdx + 0x22], 0xff") and RA.get(0x27205A) == ("cmp", "byte ptr [rdx + 0x23], 0xff")
      and RA.get(0x27205E) == ("movzx", "r9d, byte ptr [rdx + 0x25]")
      and has(0x273160, 0x273264, [(0x27319C, ("call", "0x35d490")), (0x2731B0, ("mov", "r9, qword ptr [rcx + rax + 0x1700]")),
                                   (0x2731B8, ("mov", "edx, dword ptr [r9 + 0x98]")), (0x2731BF, ("bt", "ebx, edx")), (0x2731E1, ("cmp", "byte ptr [r9 + 0x23], 0xff"))])
      and has(0x273380, 0x273407, [(0x273392, ("call", "0x35d490")), (0x2733D3, ("mov", "eax, dword ptr [r8 + 0x98]"))])
      and has(0x273410, 0x27345C, [(0x273418, ("call", "0x35d490")), (0x27342C, ("add", "rax, 0x1500")), (0x273438, ("add", "rax, 0x1800"))]),
      "00271FB0: L 1/2/3/else -> +0x1700/+0x1600/+0x1800/+0x1500, entry +0x98 as a bit index, keys +0x23/+0x22/+0x24/+0x21, then +0x25; "
      "00273160 (+0x1700, +0x98, +0x23), 00273380 (+0x98), 00273410 (table address)")
cache_refs, next_refs = [], []
for al in range(4):
    for j, (v,) in enumerate(struct.iter_unpack("<i", buf[al:al + (len(buf) - al) // 4 * 4])):
        i = al + 4 * j
        for tail in (0, 1, 4):
            t = tb + i + 4 + tail + v
            if CACHE <= t < CACHE + 0x1900 or t == CACHE + 0x1900:
                for back in range(7, 1, -1):
                    x = next(cs.disasm(buf[i - back:i - back + 16], tb + i - back, 1), None)
                    if x and x.address + x.size == tb + i + 4 + tail and "rip" in x.op_str: (cache_refs if t < CACHE + 0x1900 else next_refs).append((x.address, t)); break
check("X", sorted(set(t for a, t in cache_refs)) == [CACHE] and sorted(set(a for a, t in cache_refs)) == [0x35D4A2, 0x35D4C4, 0x35D5D0] and len(next_refs) > 0,
      "rip references inside [022C8B08, +0x1900) are only 0035D4A2 / 0035D4C4 / 0035D5D0 at the base; 022CA408 (+0x1900) has %d of its own" % len(next_refs))
REC = "_index/candidates/status-order-cache-opus/status_cache.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PV, DU = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
T1, T2 = "StatusOrderCache022C8B08", "StatusOrderCacheEntryA8"
ROWS = [(T1, 0x0000, 0x1500, "entries", "StatusOrderCacheEntryA8[32]", "the 32 status cache entries, entry i built from 0035D330(0x1A, i) (check B)", PV),
        (T1, 0x1500, 0x100, "orderListOther1500", "StatusOrderCacheEntryA8*[32]", "listing L other than 1..3 (0): built by 002D02C0 kind 1; readers test the entry's order key +0x21 (00272044)", PV),
        (T1, 0x1600, 0x100, "orderListL2_1600", "StatusOrderCacheEntryA8*[32]", "listing L = 2: built by 002D02C0 kind 2; readers test the entry's order key +0x22 (00272052)", PV),
        (T1, 0x1700, 0x100, "orderListL1_1700", "StatusOrderCacheEntryA8*[32]", "listing L = 1: built by 002D02C0 kind 3; readers test +0x23 (0027205A, 002731E1); 00273160 reads this table directly", PV),
        (T1, 0x1800, 0x100, "orderListL3_1800", "StatusOrderCacheEntryA8*[32]", "listing L = 3: built by 002D02C0 kind 4; readers test +0x24 (0027204A)", PV),
        (T2, 0x00, 0x98, "record", "EncodedIdQueryRecord", "a copy of the class-0x1A query record 0035D330(0x1A, i) returns, whole (00273BE6..00273C46); readers use its order keys +0x21..+0x24 and +0x25", PV),
        (T2, 0x98, 4, "rowIndex98", "uint32", "i, the status row the entry was built from (00273C41); readers use it as a bit index into their own mask (00272019 bt edi, eax; 002731BF)", PV),
        (T2, 0x9C, 0xC, "unwrittenSpan9C", "u8[12]", "not written by the builder and not read by the four readers; zero from .data's zero-filled tail", DU)]
TROWS = [[T1, "0x1900", "04-Actor-Entity", "one static object at 022C8B08, returned by 0035D490",
          "IMAGE - .data's zero-filled tail at 022C8B08; the next object starts at 022CA408 (+0x1900)",
          "00273BA0, once: 0035D490 / 0035D5C0 run it while dword 022C83E8 bit 0x200 is clear, then set the bit",
          "none - never released or rebuilt on the direct paths: no rip-relative write clears 022C83E8 bit 0x200 (check G)", PV[0], PV[1], "L1",
          "CARVED 2026-09-28 (OPUS, %s B G R X). Prose: _index/candidates/ga1-status-open-bytes/kinds.md (FABLE, GA-1) and the 00329220 page. %s" % (REC, EXE),
          "04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md", "STATIC - 0035D490's return value"],
         [T2, "0xA8", "04-Actor-Entity", "32 embedded in StatusOrderCache022C8B08 +0x0000, stride 0xA8",
          "EMBEDDED - StatusOrderCache022C8B08 +0x0000 + 0xA8 * i", "00273BA0 (a whole-record copy plus the index)", "none - lives with the cache", PV[0], PV[1], "L1",
          "CARVED 2026-09-28 (OPUS, %s B R). %s" % (REC, EXE), "04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md",
          "EMBEDDED - the cache's entries array; the order tables point at entries"]]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); e = fl[1][len(fl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] in (T1, T2) for l in fl):
        fl += ["\t".join([t, "0x%04X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s). %s" % (REC, EXE)]) + e for t, o, n, nm, ct, m, rd in ROWS]
    open(FI, "wb").write("".join(fl).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    for r in TROWS:
        if not any(cells(l)[0] == r[0] for l in tl): tl.append("\t".join(r) + te)
    for i_, l in enumerate(tl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == "EncodedIdQueryRecord" and T2 not in c[3]:
            c[3] += "; a fourth home: 32 whole copies of class-0x1A records embedded as StatusOrderCacheEntryA8 +0x00 in StatusOrderCache022C8B08 (00273BA0; OPUS 2026-09-28, %s)" % REC
            tl[i_] = "\t".join(c) + ee
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in (T1, T2)]
Tt = [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in (T1, T2)]
check("W", len(Tt) == 2 and sum(int(c[2]) for c in F if c[0] == T1) == 0x1900 and sum(int(c[2]) for c in F if c[0] == T2) == 0xA8 and len(F) == len(ROWS)
      and any(c[0] == "EncodedIdQueryRecord" and T2 in c[3] for c in [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()]),
      "StatusOrderCache022C8B08 (0x1900) and StatusOrderCacheEntryA8 (0xA8) are in the store and tile; EncodedIdQueryRecord lists the embedded copies")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
