"""DD prose-residue batch 20 (SWE2-CONTRACT for OPUS, 2026-10-01): the map-screens page and the request-router page.

  16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md   (CRLF on every line)
  16-UI/Request-Router/ui-request-router.md                         (LF on every line)

Run: python -B b20_checks.py   (from anywhere; paths resolve from this file. Last line FAILS n; must be FAILS 0)
Inputs: the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py (sha 73461d08...), its import
table (pefile), the register _index/OPEN-QUESTIONS.md, the key-slot table
16-UI/Layout-Parameter-System/members/layout-key-slots.tsv, and the two pages.
Static only; nothing is executed and nothing is live. No check reads either page's status line.

A1-A5  the track container is zeroed at birth and its +0x179DC..+0x179DF are never stored (map page, 1054):
       A1 002B6394 mov ecx, 0x179e0 / 002B63A0 call 00244F50 (the factory); A2 both factory paths reach 002465F0 with
       edx = the size (00244FCB mov edx, edi; the pool path jumps back to 00244FC5); A3 002465F0 calls 00861EC0 with
       edx = 0 and r8 = the size (00246626); A4 00861EC0 is `jmp [008C2A60]` and that slot imports memset
       (control: 0028CA30's known 0x80-byte memset tail-jumps to the same thunk); A5 image-wide, every instruction with
       a memory displacement in 0x179DC..0x179DF: the stores are exactly the location page's (002BAF80) - two stores,
       four reads (the page's own count). Positive control: the same census finds 109 sites / 49 stores at 0x179D2,
       the page's figures.
B1-B4  the track closer 002B6260's callers (map page, 1018): B1 direct callers exactly 00252DE0@00252DE4,
       00253C70@00253C92 and @00253EA4, 002B6140@002B6194 (jmp), 002B7B80@002B8325; B2 00252DE0's only caller is
       the area unload 002628B0@00262DCE and 002B6260 is its first call; 002B6140's callers are 00251F40, 00254AC0,
       00255330, and it calls 00247870 before the tail jump; B3 00253C89 `cmp byte [02092750], 3 / je` skips only the
       00253C92 call; B4 002B6260 returns at once when 0209E5C0 is null (002B626E). Control: callers() finds
       002B6220's known caller 00253C70@00253DE2.
C1-C5  the two drawers differ only as the note says (map page, 835): C1 callee multisets; C2 rip-referenced globals;
       C3 the globals' layout keys from layout-key-slots.tsv (TrackMapColorR..A, ExtraTrackMapJumpIconOffsetX/Y,
       BaseMapJumpIconScale, ExtraLocaMapJumpIconOffsetX/Y) and no key for 01E0CE78 / 01E0CE7C; C4 the cited sites
       (002B93B6, 002B9502 colour reads; 002B9547 / 002B9560 cvttss2si; 002BCC0C imul); C5 002DD2F0 calls 00249EE0
       then 00249FD0.
D1-D2  the single-node substitution (map page, 824): the compared stack argument is page +0xBBC8 and the substituted
       value is the byte +0xBBE4, on both walkers (stack offsets checked against each walker's frame size).
E1-E7  003BC160 (map page, 1294-1295): E1 the three gates; E2 the loop calls 00473BB0(0, i, 003BC260(widget), &out);
       E3 the hit test is out[+0] == 1 and out[+0x14] != 0 (ebp = 0); E4 the store at 003BC247 is a dword at
       02B457D8 (bytes 89 2D), setne bpl on ebx; E5 the writers of 02B457D8..02B457DF are exactly 002BAD7F and
       003BC247 (rip census, which also finds the second one as a positive control); E6 00473B70 reads 02CA6C68;
       E7 00473BB0's out[+0x14] comes from the record's byte +6 (00473C6C .. 00473C75).
F1-F3  the request-24 callees (router page, 216): F1 00290450 forwards to 003F80E0 on [0209BE80]+0xA0D0;
       F2 00428F30 walks 0x740-byte records of 022C6F28 from +0x48800 through word +4, calling 0046D0A0 on +0x5F0;
       F3 the battle-mode ladder page carries the `0035BC50` opened section and names 0028FD70 and 00290500.
P1-P3  pointer sources: P1 the register rows cited are ANSWERED (UQ-156, UQ-157, UQ-158, UQ-162, UQ-163, MS-1..MS-4);
       P2 the map page's section 4 row for 003C2210 and the router's section 7c P1 / 7b R5 / R7 / R13 are present;
       P3 the MS-4 record exists.
Z1-Z5  the pages: every batch-20 note is on the line the README names; exactly two batch-20 strikes (the 003BC160
       corrections on map lines 333 and 1294, with consumer-check.md beside this file); the map page is CRLF and the router page LF on every
       line; the line counts are unchanged from HEAD.
"""
import collections, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.abspath(os.path.join(TZA, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

R, SC, SZ = T.R, T.scan(), T.sizes()
CAND = os.path.join(TZA, "_index", "candidates")
REG = os.path.join(TZA, "_index", "OPEN-QUESTIONS.md")
MAP = os.path.join(TZA, "16-UI", "Map-Screens", "the-map-screens-and-their-shared-map-data.md")
RTR = os.path.join(TZA, "16-UI", "Request-Router", "ui-request-router.md")
KEYS = os.path.join(TZA, "16-UI", "Layout-Parameter-System", "members", "layout-key-slots.tsv")
LADDER = os.path.join(TZA, "00-Engine-Core-Runtime", "Battle-Runtime-Mode", "battle-runtime-mode-ladder.md")
TAG = "DD batch 20"
FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + str(detail) if detail != "" else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def callers(a):
    return sorted(SC["calls"].get(a, ()))


def fmtc(c):
    return [("%08X" % f, "%08X" % s) for f, s in c]


# ============================================================ A: the track container's zeroing
check("A1 002B6394 mov ecx, 0x179e0 then 002B63A0 call 0x244f50 (the widget factory), stored to 0209E5C0 at 002B63A8",
      ins(0x002B6394) == "mov ecx, 0x179e0" and ins(0x002B63A0) == "call 0x244f50"
      and ins(0x002B63A8) == "mov qword ptr [rip + 0x1de8211], rax" and 0x002B63A8 + 7 + 0x1DE8211 == 0x0209E5C0)
check("A2 the factory hands every object to 002465F0 with edx = the size (00244F6A mov edi, ecx; 00244FCB mov edx, edi; "
      "00244FCD call; the pool path 00244FFD jumps back to 00244FC5)",
      ins(0x00244F6A) == "mov edi, ecx" and ins(0x00244FCB) == "mov edx, edi" and ins(0x00244FCD) == "call 0x2465f0"
      and ins(0x00244FFD) == "jmp 0x244fc5" and ins(0x00244FB2) == "call 0x2497b0")
check("A3 002465F0 zeroes the object first: movsxd r8, edx / xor edx, edx / mov rdi, rcx / call 00861EC0 at 00246626",
      ins(0x00246612) == "movsxd r8, edx" and ins(0x00246618) == "xor edx, edx" and ins(0x0024661D) == "mov rdi, rcx"
      and ins(0x00246626) == "call 0x861ec0" and ins(0x00246641) == "mov qword ptr [rdi], rbx")
imp = None
try:
    import pefile
    pe = pefile.PE(R.b.EXE, fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
    imp = {i.address: (d.dll, i.name) for d in pe.DIRECTORY_ENTRY_IMPORT for i in d.imports}
except Exception as e:  # pragma: no cover
    print("INFO pefile unavailable: %r" % e)
ok4 = (ins(0x00861EC0) == "jmp qword ptr [rip + 0x60b9a]" and 0x00861EC0 + 6 + 0x60B9A == 0x008C2A60
       and imp is not None and imp.get(0x008C2A60) == (b"VCRUNTIME140.dll", b"memset"))
check("A4 00861EC0 is jmp [008C2A60] and that IAT slot imports VCRUNTIME140!memset; control: 0028CA30 "
      "(xor edx, edx / mov r8d, 0x80 / jmp 00861EC0) is the router page's known 0x80-byte clear",
      ok4 and ins(0x0028CA30) == "xor edx, edx" and ins(0x0028CA32) == "mov r8d, 0x80" and ins(0x0028CA38) == "jmp 0x861ec0",
      imp.get(0x008C2A60) if imp else None)
sites = collections.defaultdict(list)          # disp -> [(addr, func, is_store)]
for f, n in SZ.items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        for k, op in enumerate(i.operands):
            if op.type == 3 and op.mem.base != T.RIP and 0x179D2 <= op.mem.disp <= 0x179DF:
                store = (k == 0 and i.mnemonic not in ("cmp", "test", "bt", "push")
                         and not i.mnemonic.startswith("j") and len(i.operands) >= 1)
                sites[op.mem.disp].append((i.address, f, store))
dc = [s for k in range(0x179DC, 0x179E0) for s in sites.get(k, [])]
st = [(a, f) for a, f, s in dc if s]
rd = [(a, f) for a, f, s in dc if not s]
check("A5 every instruction with displacement 0x179DC..0x179DF: 2 stores, both in the location page 002BAF80; 4 reads, "
      "all in the two map pages 002B7B80 / 002BAF80",
      len(st) == 2 and all(f == 0x002BAF80 for _, f in st) and len(rd) == 4
      and all(f in (0x002B7B80, 0x002BAF80) for _, f in rd),
      {"stores": ["%08X" % a for a, _ in st], "reads": ["%08X in %08X" % (a, f) for a, f in rd]})
d2 = sites.get(0x179D2, [])
check("A5c control: the same census finds the page's 109 sites / 49 stores at displacement 0x179D2",
      len(d2) == 109 and sum(1 for *_, s in d2 if s) == 49, (len(d2), sum(1 for *_, s in d2 if s)))

# ============================================================ B: the track closer's callers
c = callers(0x002B6260)
check("B1 002B6260's direct callers are exactly 00252DE0@00252DE4, 00253C70@00253C92 and @00253EA4, "
      "002B6140@002B6194, 002B7B80@002B8325; no rip reference",
      c == [(0x00252DE0, 0x00252DE4), (0x00253C70, 0x00253C92), (0x00253C70, 0x00253EA4), (0x002B6140, 0x002B6194),
            (0x002B7B80, 0x002B8325)] and not SC["refs"].get(0x002B6260), fmtc(c))
check("B2 00252DE0 (the request reset) is called only by the area unload 002628B0 (00262DCE) and calls 002B6260 first; "
      "002B6140 is called by 00251F40, 00254AC0, 00255330, calls 00247870 and tail-jumps 002B6260",
      callers(0x00252DE0) == [(0x002628B0, 0x00262DCE)] and ins(0x00252DE4) == "call 0x2b6260"
      and [f for f, _ in callers(0x002B6140)] == [0x00251F40, 0x00254AC0, 0x00255330]
      and ins(0x002B6186) == "call 0x247870" and ins(0x002B6194) == "jmp 0x2b6260",
      (fmtc(callers(0x00252DE0)), fmtc(callers(0x002B6140))))
check("B3 00253C89 `cmp byte ptr [rip + 0x1e3eac0], 3` (02092750) / `je 0x253c97` skips only the 00253C92 call",
      ins(0x00253C89) == "cmp byte ptr [rip + 0x1e3eac0], 3" and 0x00253C89 + 7 + 0x1E3EAC0 == 0x02092750
      and ins(0x00253C90) == "je 0x253c97" and ins(0x00253C92) == "call 0x2b6260" and ins(0x00253C97) == "call 0x35c740")
check("B4 002B6260 returns at once when 0209E5C0 is null (002B6264 load, 002B626E je 0x2b6305)",
      ins(0x002B6264) == "mov rcx, qword ptr [rip + 0x1de8355]" and 0x002B6264 + 7 + 0x1DE8355 == 0x0209E5C0
      and ins(0x002B626E) == "je 0x2b6305")
check("B5 control: callers() finds 002B6220's known caller 00253C70@00253DE2", callers(0x002B6220) == [(0x00253C70, 0x00253DE2)])

# ============================================================ C: the two drawers
def census(f):
    L = body(f)
    calls = collections.Counter(i.op_str for i in L if i.mnemonic == "call")
    g = collections.Counter()
    for i in L:
        for op in i.operands:
            if op.type == 3 and op.mem.base == T.RIP:
                g[i.address + i.size + op.mem.disp] += 1
    return calls, g


tc, tg = census(0x002B8EE0)
lc, lg = census(0x002BCB00)
only_t = dict(tc - lc)
only_l = dict(lc - tc)
check("C1 callee multisets: track-only 00249FD0 x4, 002B6B50 x1, one more 002D8530; location-only 002DD2F0 x3, 00249EE0 x1; "
      "both call 003BC160, 003BDCD0, 003BDB30",
      only_t == {"0x249fd0": 4, "0x2b6b50": 1, "0x2d8530": 1} and only_l == {"0x2dd2f0": 3, "0x249ee0": 1}
      and all(tc[x] == lc[x] == 1 for x in ("0x3bc160", "0x3bdcd0", "0x3bdb30")), (only_t, only_l))
gt = set(tg) - set(lg)
gl = set(lg) - set(tg)
want_t = {0x0209E5A8, 0x0209E5AC, 0x01E0CE60, 0x01E0CE64, 0x01E0CE68, 0x01E0CE6C, 0x01E0CE78, 0x01E0CE7C,
          0x01E0C1DC, 0x01E0C1D8, 0x01E0CE54, 0x00900384, 0x01CEBB70, 0x008C5B34}
want_l = {0x01E0CE80, 0x0209E5D8, 0x0209E5DC, 0x01CEBBA8}
check("C2 rip globals: track-only = the TrackMap colour / offset keys, 01E0CE78/7C, the screen size 01E0C1DC/D8, 01E0CE54, "
      "00900384 and two constants; location-only = 01E0CE80, 0209E5D8/DC, 01CEBBA8",
      gt == want_t and gl == want_l, (sorted("%08X" % x for x in gt), sorted("%08X" % x for x in gl)))
keys = {}
for ln in open(KEYS, encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 3 and re.match(r"^[0-9A-F]{8}$", p[2]):
        keys[int(p[2], 16)] = p[0]
kw = {0x01E0CE60: "TrackMapColorR", 0x01E0CE64: "TrackMapColorG", 0x01E0CE68: "TrackMapColorB",
      0x01E0CE6C: "TrackMapColorA", 0x0209E5A8: "ExtraTrackMapJumpIconOffsetX", 0x0209E5AC: "ExtraTrackMapJumpIconOffsetY",
      0x01E0CE80: "BaseMapJumpIconScale", 0x0209E5D8: "ExtraLocaMapJumpIconOffsetX",
      0x0209E5DC: "ExtraLocaMapJumpIconOffsetY"}
check("C3 layout-key-slots.tsv names the drawers' key globals as the note says, and has no key at 01E0CE78 / 01E0CE7C "
      "(control: %d keys loaded)" % len(keys),
      all(keys.get(a) == k for a, k in kw.items()) and 0x01E0CE78 not in keys and 0x01E0CE7C not in keys and len(keys) > 200)
check("C4 the cited sites: 002B93B6 / 002B9502 read 01E0CE60; 002B9547 / 002B9560 cvttss2si 01E0CE78 / 01E0CE7C; "
      "002BCC0C imul 01E0CE80",
      ins(0x002B93B6) == "movzx eax, byte ptr [rip + 0x1b53aa3]" and 0x002B93B6 + 7 + 0x1B53AA3 == 0x01E0CE60
      and ins(0x002B9502) == "movzx eax, byte ptr [rip + 0x1b53957]" and 0x002B9502 + 7 + 0x1B53957 == 0x01E0CE60
      and ins(0x002B9547).startswith("cvttss2si eax, dword ptr [rip + 0x1b53929]") and 0x002B9547 + 8 + 0x1B53929 == 0x01E0CE78
      and ins(0x002B9560).startswith("cvttss2si eax, dword ptr [rip + 0x1b53914]") and 0x002B9560 + 8 + 0x1B53914 == 0x01E0CE7C
      and ins(0x002BCC0C) == "imul dword ptr [rip + 0x1b5026e]" and 0x002BCC0C + 6 + 0x1B5026E == 0x01E0CE80)
dd = [i for i in body(0x002DD2F0) if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")]
check("C5 002DD2F0 calls 00249EE0 and then reaches 00249FD0",
      [i.op_str for i in dd][:2] == ["0x249ee0", "0x249fd0"], [(hex(i.address), i.mnemonic, i.op_str) for i in dd])


# ============================================================ D: the single-node substitution
def no_write(reg, lo, hi, f):
    bad = []
    for i in body(f):
        if lo < i.address < hi and i.op_str.split(",")[0].strip() in (reg, reg + "d", reg + "w", reg + "b") \
                and i.mnemonic not in ("cmp", "test", "push"):
            bad.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
    return bad


# track: walker frame = 4 pushes (0x20) + sub 0x88 + ret 8 = 0xB0
okd1 = (ins(0x002B88F2) == "mov r9, qword ptr [r14 + 0xbbc8]" and ins(0x002B89C9) == "mov qword ptr [rsp + 0x20], r9"
        and ins(0x002B899F) == "movsx edx, byte ptr [r14 + 0xbbe4]" and ins(0x002B89A7) == "mov dword ptr [rsp + 0x48], edx"
        and ins(0x002B89D5) == "call 0x2b9a20" and ins(0x002B9A30) == "sub rsp, 0x88"
        and ins(0x002B9A4F) == "mov r13d, dword ptr [rsp + 0xf8]" and ins(0x002B9A98) == "cmp qword ptr [rsp + 0xd0], rbx"
        and ins(0x002B9AB0) == "cmove eax, r13d" and 0xD0 - 0xB0 == 0x20 and 0xF8 - 0xB0 == 0x48)
w1 = no_write("r9", 0x002B88F2, 0x002B89C9, 0x002B7B80) + no_write("edx", 0x002B89A7, 0x002B89A7 + 1, 0x002B7B80)
check("D1 track: the compared argument is page +0xBBC8 (002B88F2 -> [rsp+0x20] at 002B89C9 = walker [rsp+0xd0]) and the "
      "substituted value is byte +0xBBE4 (002B899F -> [rsp+0x48] = walker [rsp+0xf8] -> r13d -> cmove at 002B9AB0); "
      "r9 not rewritten in between", okd1 and not w1, w1)
okd2 = (ins(0x002BBD80) == "mov r9, qword ptr [r14 + 0xbbc8]" and ins(0x002BBE52) == "mov qword ptr [rsp + 0x20], r9"
        and ins(0x002BBE2C) == "movsx edx, byte ptr [r14 + 0xbbe4]" and ins(0x002BBE34) == "mov dword ptr [rsp + 0x40], edx"
        and ins(0x002BBE5E) == "call 0x2bd590" and ins(0x002BD5A0) == "sub rsp, 0x78"
        and ins(0x002BD5BC) == "mov r13d, dword ptr [rsp + 0xe0]" and ins(0x002BD5F8) == "cmp qword ptr [rsp + 0xc0], rbx"
        and ins(0x002BD60B) == "cmove eax, r13d" and 0xC0 - 0xA0 == 0x20 and 0xE0 - 0xA0 == 0x40)
w2 = no_write("r9", 0x002BBD80, 0x002BBE52, 0x002BAF80)
check("D2 location: the same pair (002BBD80 / 002BBE52 -> walker [rsp+0xc0]; 002BBE2C / 002BBE34 -> walker [rsp+0xe0]; "
      "frame 0xA0); r9 not rewritten in between", okd2 and not w2, w2)

# ============================================================ E: 003BC160
check("E1 003BC160's gates: [02B457E0] non-null, byte +0xC8 == 1, dword +0xD0 & 0x100, 0037ED80() == 1",
      ins(0x003BC194) == "cmp byte ptr [rax + 0xc8], 1" and ins(0x003BC19D) == "test dword ptr [rax + 0xd0], 0x100"
      and ins(0x003BC1A9) == "call 0x37ed80" and ins(0x003BC1AE) == "cmp eax, 1")
check("E2 the loop: 00473B70(0) count (003BC1B8/003BC1C9), esi = 003BC260(widget) (003BC1D7/003BC1DE), "
      "00473BB0(ecx=0, edx=i, r8d=esi, r9=&out) at 003BC1FC",
      ins(0x003BC1B8) == "xor ecx, ecx" and ins(0x003BC1C9) == "call 0x473b70" and ins(0x003BC1D7) == "call 0x3bc260"
      and ins(0x003BC1DE) == "mov esi, eax" and ins(0x003BC1F5) == "mov r8d, esi" and ins(0x003BC1F8) == "mov edx, ebx"
      and ins(0x003BC1FA) == "xor ecx, ecx" and ins(0x003BC1FC) == "call 0x473bb0" and ins(0x003BC1F0) == "lea r9, [rsp + 0x20]")
check("E3 the hit test is out[+0] == 1 and out[+0x14] != 0: ebp = 0 (003BC1DC xor ebp, ebp), 003BC201 cmp [rsp+0x20], 1 / "
      "jne next; 003BC208 cmp [rsp+0x34], ebp / jne hit 003BC23D",
      ins(0x003BC1DC) == "xor ebp, ebp" and ins(0x003BC201) == "cmp dword ptr [rsp + 0x20], 1"
      and ins(0x003BC206) == "jne 0x3bc20e" and ins(0x003BC208) == "cmp dword ptr [rsp + 0x34], ebp"
      and ins(0x003BC20C) == "jne 0x3bc23d" and 0x34 - 0x20 == 0x14)
raw = R.at(0x003BC247, 6)
check("E4 003BC247 stores a DWORD at 02B457D8 (bytes 89 2D, mov dword ptr [rip + 0x278958b], ebp), after setne bpl on "
      "test ebx, ebx; the hit's out[+0xC] goes to 003C0380 (rejects the old 'byte 02B457D9' reading)",
      raw[:2] == b"\x89\x2d" and ins(0x003BC247) == "mov dword ptr [rip + 0x278958b], ebp"
      and 0x003BC247 + 6 + 0x278958B == 0x02B457D8 and ins(0x003BC241) == "test ebx, ebx"
      and ins(0x003BC243) == "setne bpl" and ins(0x003BC23D) == "mov ecx, dword ptr [rsp + 0x2c]"
      and ins(0x003BC24D) == "call 0x3c0380" and 0x2C - 0x20 == 0xC, raw[:2].hex())
allr = [(t, sorted(SC["refs"].get(t, ()))) for t in range(0x02B457D8, 0x02B457E0)]
stores = []
for t, lst in allr:
    for f, a, k in lst:
        i = next(R.md.disasm(R.at(a, 16), a, 1))
        if i.mnemonic.startswith("mov") and i.operands[0].type == 3:
            stores.append(("%08X" % t, "%08X" % a, "%08X" % f))
check("E5 the stores to 02B457D8..02B457DF are exactly 002BAD7F (002BA700) and 003BC247 (003BC160), both at 02B457D8; "
      "nothing stores at 02B457D9 or 02B457DC (positive control: the census finds 003BC247)",
      sorted(stores) == [("02B457D8", "002BAD7F", "002BA700"), ("02B457D8", "003BC247", "003BC160")], stores)
check("E6 00473B70 reads the chunk pointer 02CA6C68 and returns the row's count byte",
      ins(0x00473B70) == "mov rax, qword ptr [rip + 0x28330f1]" and 0x00473B70 + 7 + 0x28330F1 == 0x02CA6C68
      and ins(0x00473B7F) == "movzx eax, byte ptr [rcx]")
check("E7 00473BB0's out[+0x14] is taken from the record's byte +6 bitfield (00473C6C movzx [r8+6] ... 00473C75 store)",
      ins(0x00473C6C) == "movzx eax, byte ptr [r8 + 6]" and ins(0x00473C75) == "mov dword ptr [r10 + 0x14], eax")

# ============================================================ F: the request-24 callees
check("F1 00290450 forwards edx = ecx to 003F80E0 on [0209BE80] + 0xA0D0 when the singleton is non-null",
      ins(0x00290450) == "mov edx, ecx" and ins(0x00290452) == "mov rcx, qword ptr [rip + 0x1e0ba27]"
      and 0x00290452 + 7 + 0x1E0BA27 == 0x0209BE80 and ins(0x0029045C) == "je 0x29046a"
      and ins(0x0029045E) == "add rcx, 0xa0d0" and ins(0x00290465) == "jmp 0x3f80e0")
check("F2 00428F30 walks 0x740-byte records of [022C6F28] from index +0x48800 through word +4 (-1 ends), calling "
      "0046D0A0 on each record's +0x5F0",
      ins(0x00428F3A) == "mov rdi, qword ptr [rip + 0x1e9dfe7]" and 0x00428F3A + 7 + 0x1E9DFE7 == 0x022C6F28
      and ins(0x00428F41) == "mov ebx, dword ptr [rdi + 0x48800]" and ins(0x00428F53) == "imul rcx, rax, 0x740"
      and ins(0x00428F5D) == "movsx ebx, word ptr [rcx + 4]" and ins(0x00428F61) == "add rcx, 0x5f0"
      and ins(0x00428F68) == "call 0x46d0a0" and ins(0x00428F6D) == "cmp ebx, -1")
lad = open(LADDER, encoding="utf-8").read()
check("F3 the battle-mode ladder page carries '## `0035BC50` opened' and names 0028FD70 and measures 00290500",
      "## `0035BC50` opened" in lad and "`0028FD70`" in lad and "`00290500` (26 B)" in lad)

# ============================================================ P: pointer sources
reg = {}
for ln in open(REG, encoding="utf-8").read().splitlines():
    m = re.match(r"^\|\s*([A-Z]{1,3}-\d+)\s*\|", ln)
    if m:
        reg.setdefault(m.group(1), ln)
cited = ["UQ-156", "UQ-157", "UQ-158", "UQ-162", "UQ-163", "MS-1", "MS-2", "MS-3", "MS-4"]
bad = [k for k in cited if k not in reg or "ANSWERED" not in reg[k]]
check("P1 the register rows the notes cite are ANSWERED: " + ", ".join(cited), not bad, bad)
mp = open(MAP, encoding="utf-8").read()
rt = open(RTR, encoding="utf-8").read()
check("P2 the cited page sections exist: map section 4 row `003C2210` (releases both slots); router 7c P1 (gameover_c.tm2), "
      "7b R5 / R7 / R13",
      "| `003C2210` | releases both" in mp and "- **P1. The game-over screen shows the words GAME OVER" in rt
      and "- **R5. World-map kind 7" in rt and "- **R7. Request 2's parameter.**" in rt
      and "- **R13. No native producer of 15, 18 or 19.**" in rt)
check("P3 the MS-4 record exists (_index/candidates/swe2struct-residue3-0930/README.md)",
      os.path.isfile(os.path.join(CAND, "swe2struct-residue3-0930", "README.md")))


# ============================================================ Z: the pages
def lines(p):
    return open(p, "rb").read().decode("utf-8").split("\n")


expect = {MAP: [32, 46, 144, 208, 333, 813, 820, 824, 835, 836, 855, 881, 974, 996, 1018, 1037, 1054, 1056, 1077, 1149,
                1211, 1294, 1295],
          RTR: [37, 194, 216, 344, 488, 519, 543, 620, 885]}
for p, want in expect.items():
    got = [n + 1 for n, t in enumerate(lines(p)) if TAG in t]
    check("Z1 %s: batch-20 notes on exactly the README's lines" % os.path.basename(p), got == want, got)
strikes = []
for p in (MAP, RTR):
    for n, t in enumerate(lines(p)):
        if TAG in t:
            # a batch-20 strike is the struck 02B457D9 text on a batch-20 line
            for m in re.finditer(r"~~(.+?)~~", t):
                if "02B457D9" in m.group(1) or "02B457DC" in m.group(1):
                    strikes.append((os.path.basename(p), n + 1, m.group(1)))
check("Z2 exactly two batch-20 strikes (map line 333, the section-4 row; map line 1294, the interior citation) and "
      "consumer-check.md exists",
      strikes == [("the-map-screens-and-their-shared-map-data.md", 333, "`[+0x34]`==0, writes `02B457DC`=(index≠" "0)"),
                  ("the-map-screens-and-their-shared-map-data.md", 1294, "byte `02B457D9 = (ebx != 0)`")]
      and os.path.isfile(os.path.join(HERE, "consumer-check.md")), strikes)
other = [(os.path.basename(p), n + 1) for p in (MAP, RTR) for n, t in enumerate(lines(p))
         if TAG in t and re.search(r"~~", t[t.find(TAG):]) and not (p == MAP and n + 1 in (333, 1294))]
check("Z3 no other batch-20 note carries a strike", not other, other)
eol = {os.path.basename(p): (open(p, "rb").read().count(b"\n"), open(p, "rb").read().count(b"\r\n")) for p in (MAP, RTR)}
check("Z4 the map page is CRLF on every line (1338 / 1338) and the router page LF on every line (961 / 0)",
      eol == {"the-map-screens-and-their-shared-map-data.md": (1338, 1338), "ui-request-router.md": (961, 0)}, eol)
head = {}
for p in (MAP, RTR):
    rel = os.path.relpath(p, TZA).replace(os.sep, "/")
    r = subprocess.run(["git", "-C", TZA, "show", "HEAD:./" + rel], capture_output=True)
    head[os.path.basename(p)] = r.stdout.count(b"\n")
check("Z5 line counts equal HEAD's (notes are appended in place)", head == {k: v[0] for k, v in eol.items()}, head)

print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
