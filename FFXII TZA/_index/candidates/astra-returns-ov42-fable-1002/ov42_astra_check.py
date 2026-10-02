"""ov42_astra_check.py - FABLE, 2026-10-02: re-reads every image fact that README.md (astra-returns-ov42-fable-1002)
cites for the four ASTRA OV-42 returns accepted by SWE2-AUDIT-SPEC (reviews committed at 2e88eceef). Read-only.

Instructions are decoded by the analysis kit's disasm_fn.py (Database/Tools/analysis-kit/gfz-scripts/disasm_fn.py
ADDR LEN, which prints address, bytes, mnemonic and resolves every rip target); each span is decoded linearly from a
function entry (or from the cited instruction when only its own bytes are claimed), and each cited instruction is
compared with its exact decoded text and, for a rip operand, its resolved target. Data facts (two jump tables, one
file value) are read with disasm_fn's own section-aware Image reader. Table facts are read from ASTRA's retained
action tables (nine languages, archive-matched by ASTRA and re-matched by SPEC); the remap arithmetic is a static
model of the cited instructions over all 65536 words, labelled as such.

Groups: P = preconditions packet (318e510c6), C = class20 packet (1cf5316d0), R = remap packet (1f6569546),
X = selector-exclusions packet (7f625ac43), T = retained tables, M = arithmetic model.
Controls (sensitive to the defects they name):
 K1 a width-changed expectation at 003092C5 (byte instead of word, SPEC's own refusal case) must be reported as a
    mismatch by the same comparator - so a PASS is not produced by a comparator that accepts anything;
 K2 the table predicate with the wrong kind mapping (3w+1, kind 5) must find 39 counterexamples per table, as SPEC
    measured - so "0 negative" is not produced by a predicate that cannot see one.
Prints PASS/FAIL per check and FAILS n."""
import hashlib, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))                 # Database/
KIT = os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts")
DISASM = os.path.join(KIT, "disasm_fn.py")
TABLES = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence",
                                       "ov42-special-action-preconditions", "action-selectors-01", "tables"))
LANGS = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

sys.dont_write_bytecode = True                                   # leave no __pycache__ in the kit or the record
sys.path.insert(0, KIT)
import disasm_fn  # noqa: E402  (the same module the subprocess runs; used here only for its Image reader)

fails = 0
def check(name, ok, got=""):
    global fails
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, ("" if ok else "  -> " + str(got))))
    if not ok: fails += 1

LINE = re.compile(r"^([0-9A-F]{8})  ([0-9a-f]+)\s+(.*?)(?:  ; (.*))?$")
_cache = {}
def span(addr, length):
    key = (addr, length)
    if key not in _cache:
        out = subprocess.run([sys.executable, DISASM, "%08X" % addr, hex(length)], capture_output=True, text=True)
        if out.returncode != 0: raise SystemExit("disasm_fn failed at %08X: %s" % (addr, out.stderr))
        d = {}
        for ln in out.stdout.splitlines():
            m = LINE.match(ln)
            if m: d[int(m.group(1), 16)] = (m.group(3).strip(), m.group(4) or "", m.group(2))
        _cache[key] = d
    return _cache[key]

def same(d, a, text, target=None):
    x = d.get(a)
    if x is None: return False, "no instruction boundary at %08X" % a
    ok = x[0] == text and (target is None or x[1].startswith("%08X" % target))
    return ok, "%08X %s ; %s" % (a, x[0], x[1])

def expect(group, d, items):
    for it in items:
        a, text = it[0], it[1]
        tgt = it[2] if len(it) > 2 else None
        ok, got = same(d, a, text, tgt)
        check("%s %08X %s%s" % (group, a, text, (" -> %08X" % tgt) if tgt else ""), ok, got)

img = disasm_fn.Image(disasm_fn.DEFAULT_EXE)
check("image sha256", hashlib.sha256(img.d).hexdigest() == EXE_SHA and img.base == 0x120000, hex(img.base))

# ---- P: ov42-special-action-preconditions (318e510c6), ACCEPT-WITH-NARROWING -------------------------------------
CBE0 = span(0x0030CBE0, 0x22C)                                   # 0030CBE0 entry, 556 B
expect("P", CBE0, [(0x0030CD93, "mov rdx, rsi"), (0x0030CD99, "call 0x30ce10")])
CE10 = span(0x0030CE10, 0x110)
expect("P", CE10, [
    (0x0030CE93, "test dword ptr [rax + 0xc], 0x40000000"), (0x0030CE9A, "je 0x30cf31"),
    (0x0030CEC2, "cmp eax, 0xd0"), (0x0030CEC7, "jb 0x30cf00"), (0x0030CEEB, "cmp eax, 0xf1"), (0x0030CEF0, "ja 0x30cf00"),
    (0x0030CEF2, "mov eax, dword ptr [rip + 0x1fb5268]", 0x022C2160), (0x0030CEF8, "add eax, -5"),
    (0x0030CEFB, "cmp eax, 1"), (0x0030CEFE, "jbe 0x30cf31"), (0x0030CF0D, "call 0x306bd0")])
BD0 = span(0x00306BD0, 284)
expect("P", BD0, [
    (0x00306BDA, "mov eax, dword ptr [rip + 0x1fbb580]", 0x022C2160), (0x00306BE8, "je 0x306c05"),
    (0x00306BEA, "cmp eax, 1"), (0x00306BED, "je 0x306bfc"), (0x00306BEF, "xor eax, eax"),
    (0x00306BFC, "cmp rdi, qword ptr [rip + 0x1fbb565]", 0x022C2168), (0x00306C03, "jne 0x306bef"),
    (0x00306C0A, "mov ebx, 3"), (0x00306C22, "call 0x32f6e0"), (0x00306C29, "je 0x306c3d"),
    (0x00306C4D, "call 0x309230"), (0x00306C52, "mov edx, eax"), (0x00306C54, "mov ecx, ebx"), (0x00306C56, "call 0x32fc30")])
F6E0 = span(0x0032F6E0, 0x0F)
expect("P", F6E0, [(0x0032F6E0, "movsxd rax, ecx"), (0x0032F6E3, "lea rcx, [rip + 0x1f97636]", 0x022C6D20),
                   (0x0032F6EA, "movsx eax, byte ptr [rax + rcx]"), (0x0032F6EE, "ret")])
P9230 = span(0x00309230, 199)
expect("P", P9230, [
    (0x003092B4, "imul ecx, edx, 0x113"), (0x003092C0, "cmp rbx, rcx"), (0x003092C3, "je 0x3092cb"),
    (0x003092C5, "movzx eax, word ptr [rbx + 0x24]"), (0x003092CB, "mov rax, qword ptr [rdi + 0x698]"),
    (0x003092D2, "movzx eax, byte ptr [rax + 4]"), (0x003092D6, "sub eax, 0x1b"), (0x003092D9, "cdqe"),
    (0x003092DB, "mov eax, dword ptr [rsp + rax*4 + 0x20]")])

# ---- C: ov42-class20-action-admission (1cf5316d0), ACCEPT ---------------------------------------------------------
expect("C", CBE0, [(0x0030CC25, "movzx edx, word ptr [rbx + 0x1c]"), (0x0030CC29, "mov ecx, 0x14"),
                   (0x0030CC32, "call 0x322c50"), (0x0030CC7A, "movzx ecx, word ptr [rbx + 0x1c]"),
                   (0x0030CC7E, "imul esi, ecx"), (0x0030CC81, "add esi, eax")])
C2C50 = span(0x00322C50, 0x20)
expect("C", C2C50, [(0x00322C5A, "lea eax, [rcx - 1]"), (0x00322C5D, "mov ebx, edx"), (0x00322C5F, "cmp eax, 0x1f"),
                    (0x00322C62, "ja 0x322c8d"), (0x00322C64, "lea rdi, [rip - 0x202c6b]", 0x00120000)])
ARM19 = span(0x00322F72, 0x1A)
expect("C", ARM19, [(0x00322F72, "mov rcx, qword ptr [rip + 0x2b9c1bf]", 0x02EBF138), (0x00322F79, "xor eax, eax"),
                    (0x00322F7E, "je 0x32302a"), (0x00322F84, "mov ecx, dword ptr [rcx + 4]"), (0x00322F87, "jmp 0x32302c")])
TAIL = span(0x0032302A, 0x17)
expect("C", TAIL, [(0x0032302A, "mov ecx, eax"), (0x0032302C, "mov edx, eax"), (0x0032302E, "cmp ebx, edx"),
                   (0x00323030, "jl 0x322c8d"), (0x00323036, "lea eax, [rcx - 1]"), (0x00323039, "cmp ebx, eax"),
                   (0x0032303B, "jg 0x322c8d")])
check("C 0030CBE0 calls the readiness helper 0030C890",
      any(x[0] == "call 0x30c890" for x in CBE0.values()))
I45F0 = span(0x003845F0, 0xFC)                                   # to its ret at 003846EB
st = sorted(re.search(r"\+ (0x[0-9a-f]+)\]", x[0]).group(1) for a, x in I45F0.items()
            if x[0].startswith("mov dword ptr [") and x[0].endswith("], eax"))
check("C installer 003845F0 rebases +0xC/+0x10/+0x14/+0x18/+0x1C and stores nothing at +4 or +8",
      sorted(st, key=lambda s: int(s, 16)) == ["0xc", "0x10", "0x14", "0x18", "0x1c"]
      and I45F0.get(0x003846EB, ("",))[0] == "ret", st)
jt = struct.unpack("<32I", img.read(0x00323054, 128))
check("C class table 00323054: 32 image-relative entries, entry 19 (class 0x14) = 00322F72",
      img.base + jt[19] == 0x00322F72, hex(img.base + jt[19]))

# ---- R: spattack-native-word-remap (1f6569546), ACCEPT ------------------------------------------------------------
DB70 = span(0x0030DB70, 0x134)
expect("R", DB70, [
    (0x0030DB9D, "movzx r8d, word ptr [rbx + 4]"), (0x0030DBCB, "mov eax, 0xffff"), (0x0030DBD2, "cmp cx, ax"),
    (0x0030DBD5, "je 0x30dbea"), (0x0030DBD7, "movzx eax, cx"), (0x0030DBDA, "sub eax, 0xd0"),
    (0x0030DBEA, "or eax, 0xffffffff"), (0x0030DC7B, "lea eax, [rbx - 0xd0]"), (0x0030DC83, "or eax, 0xffffffff"),
    (0x0030DC98, "mov dword ptr [rip + 0x1fb44da], eax", 0x022C2178)])
D6760 = span(0x003067AA, 0x136)
expect("R", D6760, [(0x003068C7, "movzx eax, ax"), (0x003068CA, "sub eax, 0xd0"), (0x003068D1, "or eax, 0xffffffff"),
                    (0x003068D4, "mov dword ptr [rip + 0x1fbb89e], eax", 0x022C2178)])
Q9C00 = span(0x00309C00, 0x2C)
expect("R", Q9C00, [(0x00309C00, "mov eax, dword ptr [rip + 0x1fb8572]", 0x022C2178), (0x00309C06, "cmp eax, -1"),
                    (0x00309C09, "jne 0x309c0e"), (0x00309C0B, "xor eax, eax"), (0x00309C0D, "ret"),
                    (0x00309C13, "mov dword ptr [rdx], eax"),
                    (0x00309C22, "mov dword ptr [rip + 0x1fb854c], 0xffffffff", 0x022C2178)])
D720 = span(0x0030D720, 0x0C)
expect("R", D720, [(0x0030D722, "mov dword ptr [rip + 0x1fb4a4c], 0xffffffff", 0x022C2178)])
expect("R", span(0x0034838A, 5), [(0x0034838A, "call 0x309c00")])
expect("R", span(0x002D6175, 5), [(0x002D6175, "call 0x309c00")])
A8870 = span(0x00348870, 0x28)
expect("R", A8870, [(0x00348880, "call 0x267e10"), (0x00348888, "mov ebx, eax"), (0x0034888A, "call 0x267e10"),
                    (0x0034888F, "mov edx, ebx"), (0x00348891, "mov ecx, eax"), (0x00348893, "call 0x30eea0")])
EEA0 = span(0x0030EEA0, 0x65)
expect("R", EEA0, [(0x0030EEA6, "mov ebx, edx"), (0x0030EEA8, "cmp edx, -1"), (0x0030EEAB, "je 0x30eeb7"),
                   (0x0030EEAD, "mov eax, 0xd0"), (0x0030EEB2, "add bx, ax"), (0x0030EEB7, "mov ebx, 0xffff"),
                   (0x0030EEBC, "call 0x31b7e0"), (0x0030EEC6, "or eax, 0xffffffff"),
                   (0x0030EECF, "cmp dword ptr [rip + 0x1fb329a], 4", 0x022C2170), (0x0030EED8, "mov eax, 0xfffffffe"),
                   (0x0030EEF5, "movzx r8d, bx"), (0x0030EF00, "call 0x30cfb0")])
CFB0 = span(0x0030CFB0, 0x18)
expect("R", CFB0, [(0x0030CFC3, "movzx ebx, r8w")])
expect("R", span(0x00304E12, 0x17), [(0x00304E12, "call 0x387090"), (0x00304E1A, "movzx r8d, ax"),
                                     (0x00304E24, "call 0x30cfb0")])          # the effective-id leg into 0030CFB0
D070 = span(0x0030D070, 0xE4)
expect("R", D070, [(0x0030D14F, "mov word ptr [rcx + 0x1c], r10w")])

# ---- X: action-selector-local-exclusions (7f625ac43), ACCEPT -------------------------------------------------------
G60E0 = span(0x003060E0, 595)
expect("X", G60E0, [
    (0x0030610D, "call 0x322c50"), (0x00306116, "mov eax, 4"), (0x00306120, "test rdi, rdi"), (0x00306123, "je 0x30632c"),
    (0x00306129, "movzx eax, byte ptr [rdi + 5]"), (0x0030612F, "jne 0x30632c"),
    (0x00306181, "movzx eax, byte ptr [rcx + 0x1e]"), (0x00306185, "cmp eax, 6"), (0x00306188, "ja 0x3062f4"),
    (0x003062F4, "cmp eax, 9"), (0x003062F7, "je 0x306311"), (0x003062F9, "cmp eax, 0xff"), (0x003062FE, "je 0x30630a"),
    (0x00306300, "mov eax, 5"), (0x0030632C, "xor eax, eax")])
W6480 = span(0x00306480, 99)
expect("X", W6480, [(0x00306493, "jne 0x3064a3"), (0x00306495, "lea eax, [rdx + 0x2c]"), (0x003064A6, "call 0x3060e0"),
                    (0x003064AD, "je 0x3064bf"), (0x003064AF, "mov eax, 0xf"), (0x003064C5, "call 0x323ec0")])
FCF0 = span(0x002FFCF0, 479)
expect("X", FCF0, [(0x002FFD05, "mov rdi, qword ptr [rdx + 0x698]"), (0x002FFD15, "test rdi, rdi"),
                   (0x002FFE97, "mov rdx, rdi"), (0x002FFE9D, "call 0x306480"), (0x002FFEA4, "jne 0x2ffd99")])
expect("X", DB70, [(0x0030DBBE, "call 0x2ffcf0"), (0x0030DBC5, "jne 0x30dc24"),
                   (0x0030DBDF, "mov dword ptr [rip + 0x1fb45a7], edx", 0x022C218C),
                   (0x0030DC24, "mov eax, 1"), (0x0030DC33, "ret"),
                   (0x0030DC34, "movzx eax, word ptr [rip + 0x1fb4555]", 0x022C2190), (0x0030DC3B, "mov ecx, 0xe2"),
                   (0x0030DC48, "cmp ax, 0xf"), (0x0030DC4C, "jbe 0x30dc83"), (0x0030DC55, "call 0x2f8d60"),
                   (0x0030DC5A, "movzx edi, ax"), (0x0030DC64, "lea ecx, [r8 + 0x14]"), (0x0030DC68, "call 0x322c50"),
                   (0x0030DC6F, "je 0x30dc83"), (0x0030DC76, "cmp di, ax"), (0x0030DC79, "je 0x30dc83"),
                   (0x0030DC8B, "movss dword ptr [rip + 0x1fb44f1], xmm6", 0x022C2184)])
M8D60 = span(0x002F8D60, 0xEA)
expect("X", M8D60, [(0x002F8D66, "movsxd rax, dword ptr [rip + 0x1bf2d83]", 0x01EEBAF0), (0x002F8D72, "js 0x2f8d85"),
                    (0x002F8D74, "lea rcx, [rip + 0x1fc5bb5]", 0x022BE930), (0x002F8D7B, "movzx eax, word ptr [rcx + rax*2]"),
                    (0x002F8D84, "ret"), (0x002F8E28, "or eax, 0xffffffff"), (0x002F8E35, "ret"),
                    (0x002F8E36, "movzx eax, byte ptr [r10]"), (0x002F8E49, "ret")])
rets = sorted(a for a, x in M8D60.items() if x[0] == "ret" and a < 0x002F8E4A)
check("X 002F8D60 has exactly three ret exits (002F8D84, 002F8E35, 002F8E49)",
      rets == [0x002F8D84, 0x002F8E35, 0x002F8E49], [hex(a) for a in rets])
fv = struct.unpack("<i", img.read(0x01EEBAF0, 4))[0]
check("X 01EEBAF0 file value is -1", fv == -1, fv)
expect("X", D6760, [(0x003067AA, "mov eax, dword ptr [rip + 0x1fbb9ac]", 0x022C215C), (0x003067B0, "dec eax"),
                    (0x003067B7, "cmp eax, 5"), (0x003067BA, "ja 0x306a9a")])
dt = struct.unpack("<8I", img.read(0x00306AF0, 32))
want6 = [0x00306931, 0x00306A3D, 0x003067DB, 0x00306848, 0x003069F8, 0x00306A8E]
check("X 00306AF0 six entries then int3 padding", [img.base + x for x in dt[:6]] == want6
      and dt[6] == dt[7] == 0xCCCCCCCC, [hex(x) for x in dt])

# ---- T: retained action tables (nine languages) ----------------------------------------------------------------
def rows_of(path):
    b = open(path, "rb").read()
    n = struct.unpack_from("<I", b, 4)[0]; s = struct.unpack_from("<H", b, 8)[0]
    return b, n, s, [b[32 + i * s:32 + (i + 1) * s] for i in range(n)]
shas, k2 = set(), []
for lg in LANGS:
    b, n, s, R = rows_of(os.path.join(TABLES, "action_data_%s.st2e" % lg))
    shas.add(hashlib.sha256(b).hexdigest())
    w = [struct.unpack_from("<H", r, 0x24)[0] for r in R]
    f = [struct.unpack_from("<I", r, 0x0C)[0] for r in R]
    c = [r[0x1E] for r in R]
    ff = [i for i in range(n) if w[i] == 0xFFFF]
    neg4 = [i for i in range(n) if w[i] != 0xFFFF and ((4 * w[i] + 1) & 0xFFFF) >= 0x8000]
    k2.append(len([i for i in range(n) if w[i] != 0xFFFF and ((3 * w[i] + 1) & 0xFFFF) >= 0x8000]))
    b30ff = [i for i in ff if f[i] & (1 << 30)]
    hi = [i for i in range(n) if w[i] != 0xFFFF and w[i] >= 0x8000]
    hirows = list(range(111, 124)) + list(range(246, 262)) + list(range(427, 436)) + [440]
    ok = (n == 543 and s == 60 and len(ff) == 68 and not neg4 and b30ff == [0x113] + list(range(511, 535))
          and len(set(f[i] for i in range(511, 535))) == 1 and all(f[i] & (1 << 30) for i in range(511, 535))
          and all(c[i] == 7 for i in range(511, 535)) and sum(1 for x in c if x == 7) == 235
          and hi == hirows and sorted(set(w[i] for i in hi)) [0] == 32775 and max(w[i] for i in hi) == 32907
          and len(set(w[i] for i in hi)) == 10 and not any(f[i] & (1 << 30) for i in hi)
          and w[113] == 0x808B and not f[113] & (1 << 30))
    check("T %s: 543 x 60; 68 FFFF; 0 non-FFFF negative 4w+1 WORD; FFFF+bit30 = 0x113 and 511..534; "
          "511..534 +0x1E = 7 (235 such rows); 10 bit-15 words 32775..32907, no bit30; row 113 = 0x808B" % lg,
          ok, (n, s, len(ff), neg4[:5], b30ff[:3], len(hi)))
check("T the nine tables are one distinct table", len(shas) == 1, len(shas))

# ---- M: remap arithmetic (static model of 0030DBDA / 0030DC7B / 003068CA encode, 00309C06 reader, 0030EEB2 decode)
def enc(w): return -1 if w == 0xFFFF else w - 0xD0               # movzx; sub eax,0xd0 / or eax,-1 (dword)
def dec(v): return 0xFFFF if v == -1 else (v + 0xD0) & 0xFFFF     # cmp edx,-1 / mov ebx,0xffff; else add bx,ax
unavail = [w for w in range(65536) if enc(w) == -1]
roundtrip_bad = [w for w in range(65536) if enc(w) != -1 and dec(enc(w)) != w]
check("M unavailable words are exactly CF and FFFF; every other word decodes unchanged",
      unavail == [0xCF, 0xFFFF] and not roundtrip_bad, (unavail, roundtrip_bad[:3]))
check("M 511..534 queue as 303..326 and decode unchanged; word 0 queues -208",
      [enc(w) for w in range(511, 535)] == list(range(303, 327)) and all(dec(enc(w)) == w for w in range(511, 535))
      and enc(0) == -208)
check("M a byte fallback (0..255) queues -208..47, disjoint from 303..326",
      min(enc(b) for b in range(256)) == -208 and max(enc(b) for b in range(256)) == 47)

# ---- controls ----------------------------------------------------------------------------------------------------
ok, got = same(P9230, 0x003092C5, "movzx eax, byte ptr [rbx + 0x24]")
check("K1 control: a width-changed expectation at 003092C5 is reported as a mismatch", not ok, got)
check("K2 control: the wrong kind mapping 3w+1 finds 39 counterexamples in each table", k2 == [39] * 9, k2)
print("FAILS", fails)
