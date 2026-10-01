"""DD prose-residue batch 16 (SWE2-CONTRACT for OPUS, 2026-10-01): 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md.

Run: python -B b16_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...) and the kit's structflow.py; the shipped archive
D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf through agent_flow/tools/vbfextract.py (the 166 `in` and 166 `ch`
area files, the us battle_pack.bin); the register _index/OPEN-QUESTIONS.md and the page, for the pointer checks.

The one residue (RESIDUE, answered): order-record flag bit 0x04, "no reader found / authored but unread" on the page.
N1  the shipped census is reproduced: 166 area files, 1,422 sets, 50,050 records in `in` and in `ch`; bit 0x04 on 256
    records, and every other bit count of section 8g's table (positive control)
N2  the 256 records do not use 0x04 as a fourth chain bit: 200 carry no chain bit 0x08/0x10/0x20, 194 have only entry 0
N3  the evaluator's chain test 0x20 >> i, 0x20 >> (i + 1) runs only for entries 0 and 1 (cmp ebx, 2 / jge before it,
    three entries), so it tests 0x20, 0x10 and 0x08 only - the page's "the shifted test stops at entry 2" holds
N4  a record-pointer taint (structflow, stride 0x18) seeded at every qword load of [unit + 0x708] in the image and at
    the record argument (rdx) of 003014C0, 00301AD0 and 0030F760 finds exactly eleven accesses covering record +4,
    none unknown; positive controls: the seven Z-19 reader sites are among them
N5  the mask each of them applies; the only one testing bit 2 is 00325DF4 `test byte ptr [rax + 4], 4`; the walk's own
    record tests (rbx, outside the seeds) are 0x40 and 0x80
N6  00325DF4 is in BattleUnit_CanAdvanceCombatNavigation (00325D90): the current order (+0x708) with bit 0x04 makes it
    return 0; its one caller, BattleUnit_UpdateCombatNavigationStep (00325BB0, at 00325BD0), then only calls 0033C9B0
    on the locomotion block unit + 0x80 and leaves, skipping the route and step calls; 0033C9B0 calls 00336710 and
    0033E1F0
N7  no player gambit carries any flag: the 256 gambit condition rows (st2e at battle_pack +0x20) have +0xE = 0, the
    word the rebuild copies to record +4 (control: relation bytes 137 / 68 / 51)
N8  bit 0x8000 is read by three sign tests on the current order, and is set by no shipped record and by none of the
    engine's static order sets (which carry no 0x04 either)
P1-P3  the pointer notes' sources: the register rows they cite are ANSWERED / CLOSED; the threshold word, the Z-16
    category decode and 0033F020's targets are where the notes say
Z1-Z4  the page keeps the struck sentences verbatim, carries the corrections and pointers, and is CRLF on every line
"""
import collections, io, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.abspath(os.path.join(TZA, ".."))
REPO = os.path.abspath(os.path.join(DB, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(REPO, "agent_flow", "tools"))
import retool as T  # noqa: E402
import structflow as S  # noqa: E402
import vbfextract as V  # noqa: E402

VBF = os.environ.get("FF12_VBF", r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf")
PAGE = os.path.join(TZA, "09-Combat-AI-And-Gambits", "gambit-evaluation-and-enmity.md")
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
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def pin(name, a, text):
    t = ins(a)
    check(name, t == text, "%08X  %s" % (a, t))


def body(f):
    return list(T.R.md.disasm(T.R.at(f, T.sizes()[f]), f))


u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]

# ============================================================ N1-N2: the shipped order sets
fh = io.open(VBF, "rb")
names, blocks = V.load_index(fh)
census = {}
for lang in ("in", "ch"):
    ards = sorted(p for p in names if p.lower().endswith(".ard") and "/%s/" % lang in p)
    c = {"files": len(ards), "sets": 0, "records": 0, "bits": collections.Counter(), "chain": collections.Counter(),
         "entries": collections.Counter()}
    for p in ards:
        b = V.read_entry(fh, names, blocks, p)
        s1 = u32(b, 0x14)
        if not s1:
            continue
        cnt = u16(b, s1)
        so = [u32(b, s1 + 4 + 4 * i) for i in range(cnt + 1)]
        for k in range(cnt):
            base = s1 + so[k]
            n = sum(b[base:base + 12])
            c["sets"] += 1
            for r in range(n):
                o = base + 0x20 + 24 * r
                fl = u16(b, o + 4)
                c["records"] += 1
                for bit in range(16):
                    if fl >> bit & 1:
                        c["bits"][1 << bit] += 1
                if fl & 4:
                    c["chain"][fl & 0x38] += 1
                    c["entries"][tuple(u16(b, o + 6 + 6 * e) != 0 for e in range(3))] += 1
    census[lang] = c
PAGE_BITS = {0x04: 256, 0x08: 2118, 0x10: 8082, 0x20: 8076, 0x40: 3339, 0x80: 6528, 0x100: 369, 0x200: 1912,
             0x400: 99, 0x800: 15084, 0x1000: 82, 0x2000: 283, 0x4000: 11929}
for lang, c in census.items():
    check("N1 %s: 166 area files, 1,422 order sets, 50,050 records (the loader page's counts)" % lang,
          (c["files"], c["sets"], c["records"]) == (166, 1422, 50050), (c["files"], c["sets"], c["records"]))
    check("N1 %s: bit 0x04 is set on 256 records" % lang, c["bits"][4] == 256, c["bits"][4])
    check("N1 %s control: every bit count of section 8g's table is reproduced, and 0x0001 / 0x0002 / 0x8000 are never set" % lang,
          dict(c["bits"]) == PAGE_BITS, {hex(k): v for k, v in sorted(c["bits"].items())})
    check("N2 %s: 200 of the 256 carry no chain bit (0x08 / 0x10 / 0x20), so 0x04 is not used as a fourth chain bit" % lang,
          c["chain"][0] == 200 and sum(c["chain"].values()) == 256, {hex(k): v for k, v in c["chain"].items()})
    check("N2 %s: 194 of the 256 have only selector entry 0 (60 have entries 0-1, 2 all three)" % lang,
          c["entries"] == collections.Counter({(True, False, False): 194, (True, True, False): 60, (True, True, True): 2}),
          dict(c["entries"]))

# ============================================================ N3: the evaluator's chain test
pin("N3 the chain test runs only while ebx < 2", 0x003016B5, "cmp ebx, 2")
pin("N3 ... (else the unchained arm)", 0x003016B8, "jge 0x301750")
pin("N3 it loads record +4", 0x003016BE, "movzx edx, word ptr [r14 + 4]")
pin("N3 bit 0x20 >> i", 0x003016CA, "sar eax, cl")
pin("N3 ... and 0x20 >> (i + 1)", 0x003016D4, "lea ecx, [rbx + 1]")
pin("N3 ... tested", 0x003016DE, "test edx, eax")
pin("N3 three selector entries", 0x00301771, "cmp ebx, 3")
tested = sorted({(0x20 >> i) for i in range(2)} | {(0x20 >> (i + 1)) for i in range(2)})
check("N3 so the shifted test reaches 0x08, 0x10 and 0x20 only, never 0x04", tested == [0x08, 0x10, 0x20], [hex(x) for x in tested])

# ============================================================ N4-N5: every reader of record +4
seed_sites = []
pat = re.compile(r"^mov r\w+, qword ptr \[(r\w+) \+ 0x708\]$")
for f, n in sorted(T.sizes().items()):
    d = T.R.at(f, n)
    if not d:
        continue
    for i in T.R.md.disasm(d, f):
        m = pat.match("%s %s" % (i.mnemonic, i.op_str))
        if m and m.group(1) not in ("rip", "rsp"):
            seed_sites.append((f, i.address))
check("N4 the image has 20 qword loads of [reg + 0x708] (the unit's current order) in 19 functions",
      len(seed_sites) == 20 and len({f for f, _ in seed_sites}) == 19, len(seed_sites))
F = S.Flow(fields=[4], depth=3, stride=0x18, slot=0, seed_loads={(f, 0x708) for f, _ in seed_sites})
for f in sorted({f for f, _ in seed_sites}):
    F.enqueue(f, {}, 3)
for f in (0x003014C0, 0x00301AD0, 0x0030F760):   # the evaluator, the selector, CommitAction: rdx = the record
    F.enqueue(f, {"rdx": {"B"}}, 3)
while F.q:
    f = F.q.pop()
    d, e = F.entry[f]
    F.walk(f, e, d)
hits = {a: (f, t) for f, a, kind, form, off, w, t in F.hits}
EXPECT = {0x002FFCB1, 0x003015A6, 0x003016BE, 0x00301B3D, 0x00305D7F, 0x00308736, 0x0030AF49, 0x00325C83,
          0x00325CAA, 0x00325DF4, 0x00328604}
check("N4 exactly eleven accesses cover record +4", set(hits) == EXPECT, " ".join("%08X" % a for a in sorted(hits)))
check("N4 no access through a record pointer has an unknown offset", not F.unk, len(F.unk))
check("N4 the one escape is CommitAction storing the record as the current order (+0x708)",
      {(f, a) for f, a, t, x in F.esc} == {(0x0030F760, 0x0030F7F9)}, sorted((hex(f), hex(a)) for f, a, t, x in F.esc))
Z19 = {0x002FFCB1: 0x2000, 0x003015A6: 0x800, 0x003016BE: None, 0x00301B3D: None, 0x00305D7F: 0x4000,
       0x00325C83: 0x200, 0x00325CAA: 0x100}
check("N4 control: the seven Z-19 reader sites are found", set(Z19) <= set(hits))


def mask_before(f, a):
    """the immediate a register-operand test at `a` uses: the nearest `mov <that reg>, imm` before it in the body"""
    b = body(f)
    k = next(j for j, i in enumerate(b) if i.address == a)
    reg = b[k].op_str.split(", ")[-1]
    full = {"cx": "ecx", "ax": "eax"}.get(reg, reg)
    for i in reversed(b[max(0, k - 8):k]):
        if i.mnemonic == "mov" and i.op_str.startswith(full + ", 0x"):
            return int(i.op_str.split(", ")[1], 16)
    return None


masks = {}
for a, (f, t) in sorted(hits.items()):
    m = re.match(r"test (byte|word) ptr \[\w+ \+ 4\], (0x[0-9a-f]+|\d+)$", t)
    if m:
        masks[a] = int(m.group(2), 0)
    elif re.match(r"test word ptr \[\w+ \+ 4\], (cx|ax)$", t):
        masks[a] = mask_before(f, a)
    elif re.match(r"cmp word ptr \[\w+ \+ 4\], 0$", t):
        masks[a] = 0x8000       # a signed compare with 0 followed by jl / jge: bit 15 (N8)
    else:
        masks[a] = "load"
for a, want in ((0x002FFCB1, 0x2000), (0x003015A6, 0x800), (0x00305D7F, 0x4000), (0x00325C83, 0x200), (0x00325CAA, 0x100),
                (0x00325DF4, 0x4)):
    check("N5 %08X tests %#x" % (a, want), masks.get(a) == want, "%s ; mask %s" % (hits[a][1], masks.get(a)))
check("N5 the two loads are the evaluator's chain test (003016BE, N3) and the selector's word at 00301B3D",
      [a for a, m in masks.items() if m == "load"] == [0x003016BE, 0x00301B3D])
pin("N5 ... whose value is tested against 0x1000", 0x00301B47, "mov ecx, 0x1000")
pin("N5 ... ", 0x00301B59, "test cx, ax")
pin("N5 ... and 0x400", 0x00301B79, "mov ecx, 0x400")
pin("N5 ... ", 0x00301B7E, "test cx, ax")
sel = body(0x00301AD0)
k = next(j for j, i in enumerate(sel) if i.address == 0x00301B3D)
eax_written = [i.address for i in sel[k + 1:] if i.address <= 0x00301B7E and "eax" == i.op_str.split(",")[0].strip()]
check("N5 ... eax still holds the flags word at both tests (no write to eax between 00301B3D and 00301B7E)", eax_written == [], eax_written)
bit2 = sorted(a for a, m in masks.items() if isinstance(m, int) and m & 4)
check("N5 the only access testing bit 2 (0x04) of record +4 is 00325DF4", bit2 == [0x00325DF4], bit2)
walk = [i for i in body(0x00305CC0) if any(op.type == 3 and op.mem.disp in (4, 5) and op.mem.base != T.RIP for op in i.operands)]
wtexts = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in walk]
check("N5 the walk's own record tests (00305CC0) are the 0x4000 context test and the 0x40 / 0x80 resume bits",
      wtexts == ["00305D7F test word ptr [r14 + 4], ax", "00305DB2 test byte ptr [rbx + 4], 0x40", "00305DBC test byte ptr [rbx + 4], 0x80"], wtexts)

# ============================================================ N6: the reader, and what it gates
pin("N6 BattleUnit_CanAdvanceCombatNavigation loads the unit's current order", 0x00325DE8, "mov rax, qword ptr [rdi + 0x708]")
pin("N6 ... (none: skip the test)", 0x00325DF2, "je 0x325dfa")
pin("N6 ... tests its flags bit 0x04", 0x00325DF4, "test byte ptr [rax + 4], 4")
pin("N6 ... and on it leaves with 0", 0x00325DF8, "jne 0x325da5")
pin("N6 ... ", 0x00325DA5, "xor eax, eax")
pin("N6 ... ", 0x00325DAC, "ret")
check("N6 the gate is 00325D90..00325E5B (one body) and its name is the battle-unit census's",
      T.func_of(0x00325DF4) == 0x00325D90 and "00325D90\tBattleUnit_CanAdvanceCombatNavigation" in
      open(os.path.join(TZA, "04-Actor-Entity", "Battle-Unit", "battle-unit-accesses.tsv"), encoding="utf-8").read())
cs = sorted(T.scan()["calls"].get(0x00325D90, ()))
check("N6 its one caller is BattleUnit_UpdateCombatNavigationStep 00325BB0, at 00325BD0", cs == [(0x00325BB0, 0x00325BD0)], cs)
pin("N6 the step's locomotion block is unit + 0x80", 0x00325BC4, "lea rbx, [rcx + 0x80]")
pin("N6 ... a 0 from the gate", 0x00325BD7, "jne 0x325be6")
pin("N6 ... calls 0033C9B0 on that block", 0x00325BD9, "mov rcx, rbx")
pin("N6 ... ", 0x00325BDC, "call 0x33c9b0")
pin("N6 ... and jumps to the epilogue", 0x00325BE1, "jmp 0x325d66")
step = [i for i in body(0x00325BB0) if i.mnemonic == "call"]
skipped = [i.op_str for i in step if 0x00325BE6 <= i.address < 0x00325D66]
check("N6 ... skipping the route and step calls of the open path (0030A130, 00383620, 00383670, 003003F0)",
      {"0x30a130", "0x383620", "0x383670", "0x3003f0"} <= set(skipped), skipped)
pin("N6 ... the open path first clears unit flag bit 18", 0x00325BE6, "and qword ptr [rdi], 0xfffffffffffbffff")
cc = [i.op_str for i in body(0x0033C9B0) if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")]
check("N6 0033C9B0 calls BuildSolverContext 00336710 and 0033E1F0 (the steering page's ResetAvoidanceStateRandomized)",
      "0x336710" in cc and "0x33e1f0" in cc, cc)

# ============================================================ N7: the player's gambit conditions
pk = [p for p in names if p.endswith("battle_pack.bin") and "/us/" in p][0]
b = V.read_entry(fh, names, blocks, pk)
sec = u32(b, 0x20)
cnt, stride, off = u16(b, sec + 4), u32(b, sec + 8), u32(b, sec + 0xC)
check("N7 battle_pack +0x20 is an st2e table of 256 rows of 32 bytes", b[sec:sec + 4] == b"st2e" and (cnt, stride) == (256, 32), (b[sec:sec + 4], cnt, stride))
fw = collections.Counter(u16(b, sec + off + r * stride + 0xE) for r in range(cnt))
check("N7 every row's +0xE (copied to record +4 by the rebuild) is 0", fw == collections.Counter({0: 256}), dict(fw))
rel = collections.Counter(b[sec + off + r * stride + 0x10] for r in range(cnt))
check("N7 control: the rows' relation bytes +0x10 are 1 / 2 / 4 on 137 / 68 / 51 rows (section 8i)", rel == collections.Counter({1: 137, 2: 68, 4: 51}), dict(rel))
fe = [i for i in body(0x00328140) if "+ 0xe]" in i.op_str]
check("N7 control: 00328140 reads a word at row +0xE", any(i.mnemonic == "movzx" and "word ptr" in i.op_str for i in fe),
      ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in fe])

# ============================================================ N8: bit 0x8000
for a, nxt in ((0x00308736, (0x0030873B, "jl 0x308751")), (0x0030AF49, (0x0030AF4E, "jge 0x30af77")), (0x00328604, (0x00328609, "jl 0x328612"))):
    check("N8 %08X is a sign test of the current order's flags word" % a, hits.get(a, (0, ""))[1] == "cmp word ptr [rax + 4], 0", hits.get(a))
    pin("N8 ... followed by a signed branch", nxt[0], nxt[1])
pin("N8 00308736's skip passes over the resume walk 00305AB0(unit, 1)", 0x0030874C, "call 0x305ab0")
static = {}
for s_ in (0x01EEC2D0, 0x01EEC320, 0x01EEC370, 0x01EEC3C0, 0x01EEC410):
    h = T.R.at(s_, 0x20)
    static[s_] = [u16(T.R.at(s_ + 0x20 + 24 * k_, 6), 4) for k_ in range(sum(h[:12]))]
static[0x01EEC298] = [u16(T.R.at(0x01EEC298, 6), 4)]
check("N8 the engine's static order sets (01EEC2D0, 01EEC320, 01EEC370, 01EEC3C0, 01EEC410) and record 01EEC298 carry neither 0x04 nor 0x8000",
      all(not (w & 0x8004) for v in static.values() for w in v), {"%08X" % k: ["%04X" % w for w in v] for k, v in static.items()})
check("N8 control: those static records' flags are the ones their pages give (01EEC298 and 01EEC3C0 0x2000, the rest 0)",
      static[0x01EEC298] == [0x2000] and static[0x01EEC3C0] == [0x2000] and static[0x01EEC410] == [0], static)

# ============================================================ P: the pointer notes' sources
reg = {}
for line in open(os.path.join(TZA, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8"):
    m = re.match(r"\| ((?:Z|UQ|GR|DH)-\d+) \|", line)
    if m:
        reg[m.group(1)] = line.rstrip().split(" | ")[-1]
for rid, word in (("Z-1", "ANSWERED"), ("Z-2", "ANSWERED"), ("Z-3", "ANSWERED"), ("Z-10", "CLOSED"), ("Z-15", "ANSWERED"),
                  ("Z-16", "ANSWERED"), ("Z-19", "ANSWERED"), ("UQ-121", "ANSWERED"), ("GR-9", "ANSWERED"), ("DH-1", "ANSWERED"),
                  ("DH-2", "ANSWERED")):
    check("P1 register row %s's status cell reads %s" % (rid, word), reg.get(rid, "").startswith("**" + word), reg.get(rid, "")[:60])
pin("P2 the selector entry's +4 word (record +6 + 6i + 4) is the s16 threshold", 0x00301B1F, "movsx esi, word ptr [rdx + rdi*2 + 0xa]")
pin("P2 Z-16: 00301830 subtracts 0x4000 from the resolved id", 0x003018DD, "lea eax, [rdx - 0x4000]")
pin("P2 ... bounds it by 0x166", 0x003018E3, "cmp eax, 0x166")
check("P2 ... and indexes the order-handler table 01EEC460", "01EEC460" in T.fmt(next(T.R.md.disasm(T.R.at(0x003018F0, 16), 0x003018F0, 1))))
tg = {i.op_str for i in body(0x0033F020) if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")}
six = {"0x471100", "0x471330", "0x4715f0", "0x4718f0", "0x472580", "0x473210"}
check("P3 0033F020's seven targets include the six 60-fps table initialisers of the Presentation crossing", six <= tg and len(tg) == 7, sorted(tg))

# ============================================================ Z: the page
raw = open(PAGE, "rb").read()
pg = raw.decode("utf-8")
check("Z1 the page keeps the struck reader cell verbatim", "~~**no reader found** — the shifted test stops at entry 2~~" in pg)
check("Z1 ... and the struck meaning cell", "~~authored but unread~~ while current: **no combat" in pg)
check("Z2 the page keeps section 7's struck '`0x04` unread' verbatim", "~~`0x04` unread~~" in pg)
check("Z3 two corrections carry the batch's Corrected note", pg.count("*Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16)") == 2)
check("Z3 thirteen dated pointer notes and one added note", pg.count("Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16)") == 13
      and pg.count("*Added 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16)") == 1)
check("Z4 every line of the page ends CRLF", raw.count(b"\n") == raw.count(b"\r\n") and raw.endswith(b"\r\n"), (raw.count(b"\n"), raw.count(b"\r\n")))
# Z4 amended 2026-10-01 by OPUS: the lane moves no status word; after OPUS's owner re-status (opus-dd-restatus-09-0930)
# the line reads DOCUMENTED and names that re-status, which this check accepts as the only allowed change.
check("Z4 the status line is unchanged by the lane (PARTIAL as the lane left it, or OPUS's attributed owner re-status)",
      "status: PARTIAL — one registered residue, GR-9 (what enters the subgroups of 155 enemy order sets that no switch inside the set reaches)" in pg
      or "status: DOCUMENTED — every register row the page names is closed and its prose residue is answered (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's DD batch 16)" in pg)

print("PASSES", PASSES)
print("FAILS", FAILS)
