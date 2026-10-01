"""DD residue batch 21 (SWE2-STRUCT for OPUS, 2026-10-01): the checks behind the residue answered on two pages,
12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md and
05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md.

Run: python -B b21_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...); the installed archive ($FF12_VBF, else the Steam path
below) for the nine battle_pack.bin packs; the register, the board (TEAM.json) and the owner pages, read only.

Shop page
  V1-V7  the shop table in all nine battle_pack.bin packs: each decodes to 57 rows / 267 entries / 2,512 references,
         and the nine decoded tables are identical. Positive control: the us figures are the page's own (57, 267,
         2,512; row 24 at +0x1338 with 39 entries). Discrimination controls: the nine files differ and the table offset
         differs; a one-id mutation of the decoded table changes its digest
  M1-M6  the map-marker widget: 002BA310 has one direct caller, 002BAF80 @ 002BB836, inside the confirm-on-marker range
         the map page gives (002BB7E1-002BB96B); 002BAF80 is the location map's page procedure on the map page;
         002BD8C0 and 002BA530 are reached only from 002BA310; 002B9C70 only from 002BD8C0; 0x3E0 widget size
  G1-G4  GR-13 / GR-14 / GR-15 are ANSWERED in the register; the page carries the six consumer corrections of
         gr13-15-shop-list-widget-0930 (statements 1-6); section 7 has no open box
Spawn page
  A1-A3  0023A520 is the handler of verb 0x3053 btlAtelSetupActorStart through the thunk 00510710 (a jmp)
  W1-W7  the L-12 word: 00235720 has one caller, 0050F520, reached only from .data 01F28510 (verb 0x301A); the
         adapter stores nothing but a push before the call; the word at 00235720's rsp+0x34 lies 0xBC below the
         adapter's rsp; inside 00235720 only the lea and the movss touch +0x34 (control: +0x30 / +0x38 are written)
  S1-S7  the child sort of 002479B0: records {movsx word +0x44, index, child}; comparator 00244610 = b.prio - a.prio,
         then a.idx - b.idx; 00249CE0 is the shared sort (8 call sites) and advances on a negative result
  E1-E3  00354E80 / 00354B20 are the dispatch-table handlers of eventplay (0x00EB) / eventplay_ec (0x00EC)
  R1-R5  the board and the register behind the pointers: L-12 / L-13 SUPERSEDED; FRONTIER-RT-RUNTIME-SURROGATE does
         not carry L-13; FABLE-REQ-ASTRA-L13-BANKS was DONE before the 2026-09-27 ruling; no open board item names the
         spawn page except SWE2STRUCT-DD-B21-1001; the section 11-29 review requests are DONE
  C1     the gambit page still says the restore helper "copies them back" (the routed disagreement stands)
  N1     every batch-21 note is on its page exactly once, and both pages stay pure CRLF
"""
import hashlib, io, json, os, re, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import retool as T  # noqa: E402

VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text == got, "%08X  %s" % (a, got))


SZ = T.sizes()


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def page(rel):
    return io.open(os.path.join(DB, rel), encoding="utf-8", newline="").read()


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
SC = T.scan()


def callers(f):
    return sorted(SC["calls"].get(f, ()))


def riprefs(f):
    return sorted(SC["refs"].get(f, ()))


SHOP = "12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md"
SPAWN = "05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md"
SH = page(SHOP)
SP = page(SPAWN)

# ============================================================ V: the shop table in every pack


def load_index(f):
    magic, hlen = struct.unpack("<4sI", f.read(8))
    assert magic == b"SRYK"
    (n,) = struct.unpack("<Q", f.read(8))
    eoff = 0x10 + n * 16
    f.seek(eoff)
    raw = f.read(0x20 * n)
    ents = [struct.unpack_from("<IIQQQ", raw, i * 0x20) for i in range(n)]
    f.seek(eoff + 0x20 * n)
    (slen,) = struct.unpack("<I", f.read(4))
    st = f.read(slen - 4)
    f.seek(eoff + 0x20 * n + slen)
    bl = f.read(hlen - (eoff + 0x20 * n + slen))
    blocks = struct.unpack("<%dH" % (len(bl) // 2), bl)
    out = {}
    for sb, _sb2, size, off, noff in ents:
        out[st[noff:st.index(b"\0", noff)].decode()] = (sb, size, off)
    return out, blocks


def read_entry(f, idx, blocks, path):
    sb, size, off = idx[path]
    nb = (size + 0xFFFF) // 0x10000
    out = bytearray()
    pos = off
    for i in range(nb):
        cs = blocks[sb + i] or 0x10000
        exp = 0x10000 if i < nb - 1 else size - 0x10000 * (nb - 1)
        f.seek(pos)
        d = f.read(cs)
        out += d if cs == exp else zlib.decompress(d)
        pos += cs
    assert len(out) == size
    return bytes(out)


def shop_table(b):
    """directory dword +0xA0 -> header {tag 0x64, stride, count, data}; every nested offset is section-relative"""
    s = struct.unpack_from("<I", b, 0xA0)[0]
    tag, st, cnt, data = struct.unpack_from("<IHHI", b, s)
    if tag != 0x64:
        return s, None, None
    rows, secs = [], []
    for i in range(cnt):
        name, sec = struct.unpack_from("<II", b, s + data + st * i)
        secs.append(sec)
        t2, st2, c2, d2 = struct.unpack_from("<IHHI", b, s + sec)
        if t2 != 0x164:
            return s, None, None
        ents = []
        for j in range(c2):
            gk, op, th, lst = struct.unpack_from("<BBHI", b, s + d2 + st2 * j)
            t3, _st3, c3, d3 = struct.unpack_from("<IHHI", b, s + lst)
            if t3 != 0x264:
                return s, None, None
            ents.append((gk, op, th, struct.unpack_from("<%dH" % c3, b, s + d3)))
        rows.append((name, tuple(ents)))
    return s, tuple(rows), secs


def digest(rows):
    return hashlib.sha256(repr(rows).encode()).hexdigest()


LANGS = ["us", "de", "fr", "es", "it", "in", "kr", "ch", "cn"]
tables, offs, fsha = {}, {}, {}
with open(VBF, "rb") as f:
    idx, blocks = load_index(f)
    found = sorted(k.split("/")[4] for k in idx if k.endswith("/binaryfile/battle_pack.bin"))
    check("V1 the archive holds exactly nine battle_pack.bin packs, the nine languages", found == sorted(LANGS), str(found))
    for lg in LANGS:
        b = read_entry(f, idx, blocks, "ps2data/image/ff12/test_battle/%s/binaryfile/battle_pack.bin" % lg)
        fsha[lg] = hashlib.sha256(b).hexdigest()
        s, rows, secs = shop_table(b)
        offs[lg] = s
        tables[lg] = rows
        ok = rows is not None
        ne = sum(len(e) for _, e in rows) if ok else -1
        nr = sum(len(x[3]) for _, e in rows for x in e) if ok else -1
        check("V2 %s: the shop table decodes to 57 rows, 267 entries, 2,512 references" % lg,
              ok and (len(rows), ne, nr) == (57, 267, 2512), "table at +0x%X: %s rows %d entries %d refs" %
              (s, len(rows) if ok else None, ne, nr))
        if lg == "us":
            check("V3 positive control (us): row 24's section at +0x1338 with 39 entries, name 0x1F9, all story gates",
                  ok and secs[24] == 0x1338 and len(rows[24][1]) == 39 and rows[24][0] == 0x1F9
                  and all(e[0] in (0, 2) for e in rows[24][1]), "sec +0x%X n %d" % (secs[24], len(rows[24][1])))
            check("V3 positive control (us): the page states these counts", "57 rows, 267 stock entries, 2,512 item references"
                  in SH and "row 24 at section `+0x1338`" in SH)
ref = digest(tables["us"])
check("V4 the nine decoded tables are identical, row for row and id for id",
      all(digest(tables[lg]) == ref for lg in LANGS), ref[:16])
check("V5 discrimination control: the nine files are not the same file", len(set(fsha.values())) == 9)
check("V6 discrimination control: the table sits at different offsets", len(set(offs.values())) >= 5,
      " ".join("%s:+0x%X" % (lg, offs[lg]) for lg in LANGS))
mut = list(tables["in"])
name, ents = mut[24]
e0 = list(ents[5])
e0[3] = (e0[3][0] ^ 1,) + tuple(e0[3][1:])
mut[24] = (name, ents[:5] + (tuple(e0),) + ents[6:])
check("V7 discrimination control: one flipped id bit in one list changes the digest", digest(tuple(mut)) != ref)

# ============================================================ M: which screen the marker widget is
c = callers(0x002BA310)
check("M1 002BA310 has exactly one direct caller, 002BAF80 @ 002BB836", c == [(0x002BAF80, 0x002BB836)], str(
    [("%08X" % a, "%08X" % b) for a, b in c]))
check("M1 ... and no rip reference or .data slot", riprefs(0x002BA310) == [] and T.qword_sites(0x002BA310) == [])
check("M2 002BB836 lies in the confirm-on-marker arm the map page gives (002BB7E1-002BB96B)",
      0x002BB7E1 <= 0x002BB836 <= 0x002BB96B and "Confirm on the current marker** (`002BB7E1`–`002BB96B`)"
      in page("16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md"))
check("M3 002BAF80 is the location map's page procedure on the map page",
      "| location map container | `0x179E0` | `0209E5F0` | `002BA700` | `002BAF80` |"
      in page("16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md"))
check("M4 002BD8C0: no direct caller, one rip reference, the lea in 002BA310",
      callers(0x002BD8C0) == [] and [(f, a, k) for f, a, k in riprefs(0x002BD8C0)] == [(0x002BA310, 0x002BA4D4, "lea")]
      and T.qword_sites(0x002BD8C0) == [])
check("M5 002BA530 is called only by 002BA310; 002B9C70 only by 002BD8C0",
      [f for f, _ in callers(0x002BA530)] == [0x002BA310] and riprefs(0x002BA530) == []
      and [f for f, _ in callers(0x002B9C70)] == [0x002BD8C0] and riprefs(0x002B9C70) == [])
m6 = [i for i in body(0x002BA310) if i.mnemonic == "mov" and i.op_str.endswith(", 0x3e0")]
check("M6 002BA310 sizes its widget 0x3E0", len(m6) >= 1, " ".join("%08X %s" % (i.address, i.op_str) for i in m6))
mc = callers(0x00249CE0)
check("M  control: the caller index returns several callers where they exist (00249CE0: 8 sites)", len(mc) == 8,
      str(len(mc)))

# ============================================================ G: GR-13..15 and their consumers
REG = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", newline="").read()


def lead(rid):
    m = re.search(r"^\|\s*%s\s*\|(.*)$" % re.escape(rid), REG, re.M)
    return m.group(1) if m else ""


for rid in ("GR-13", "GR-14", "GR-15"):
    check("G1 %s reads ANSWERED in the register" % rid, "ANSWERED" in lead(rid)[:4000])
for k in range(1, 7):
    check("G2 the page carries gr13-15-shop-list-widget-0930 statement %d" % k,
          ("gr13-15-shop-list-widget-0930/README.md) statement %d;" % k) in SH)
s7 = SH[SH.index("## 7. What is not known"):SH.index("## 8. Evidence")]
check("G3 section 7 has no open box", "- [ ]" not in s7 and "- [~]" not in s7 and s7.count("- [x]") >= 9,
      "%d ticked" % s7.count("- [x]"))
check("G4 the GR-14 and GR-15 boxes carry their answers",
      "Message 26 reaches only the inventory menu's lists; the shop's Buy, Sell and Bazaar lists never receive it" in s7
      and "the shop's Buy / Sell / Bazaar tabs (kinds 32, 19, 31)" in s7)

# ============================================================ A: the unnamed tunable reset
pin("A1 00510710 is a jmp to 0023A520", 0x00510710, "jmp 0x23a520")
check("A2 0023A520's only reference is that thunk", callers(0x0023A520) == [(0x00510710, 0x00510710)] and
      riprefs(0x0023A520) == [] and T.qword_sites(0x0023A520) == [])
VT = page("01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv")
check("A3 the verb table row 0x3053 btlAtelSetupActorStart -> 00510710, and the thunk sits in .data",
      re.search(r"^3053\t3\t053\tbtlAtelSetupActorStart\t.*\t00510710\tresult\t00510710\t", VT, re.M) is not None
      and len(T.qword_sites(0x00510710)) == 1)

# ============================================================ W: the L-12 word
check("W1 00235720 has one direct caller, 0050F520 @ 0050F52C, and no rip reference",
      callers(0x00235720) == [(0x0050F520, 0x0050F52C)] and riprefs(0x00235720) == [] and
      T.qword_sites(0x00235720) == [])
check("W2 0050F520 is reached only through .data 01F28510",
      callers(0x0050F520) == [] and riprefs(0x0050F520) == [] and T.qword_sites(0x0050F520) == [0x01F28510])
check("W2 ... the verb table row 0x301A btlAtelDecideEntryPointAuto -> 0050F520",
      re.search(r"^301A\t3\t01A\tbtlAtelDecideEntryPointAuto\t.*\t0050F520\tresult\t0050F520\t", VT, re.M) is not None)
ad = body(0x0050F520)
seq = ["%s %s" % (i.mnemonic, i.op_str) for i in ad]
check("W3 the adapter: push rbx; sub rsp, 0x20; two register moves; call 0x235720",
      seq[:5] == ["push rbx", "sub rsp, 0x20", "mov rbx, rcx", "mov rcx, rdx", "call 0x235720"], " / ".join(seq))
stores = [i for i in ad[:5] if i.operands and i.operands[0].type == 3]
check("W3 ... no memory store before the call", stores == [])
pro = ["%s %s" % (i.mnemonic, i.op_str) for i in body(0x00235720)[:3]]
check("W4 00235720's prologue: push rbx; push rdi; sub rsp, 0xd8", pro == ["push rbx", "push rdi", "sub rsp, 0xd8"],
      str(pro))
# adapter rsp after its sub = S. call pushes 8, two pushes 16, sub 0xD8: callee rsp = S - 0xF0; slot = S - 0xF0 + 0x34
check("W5 the slot is S - 0xBC, below the adapter's frame [S, S + 0x30)", -0x8 - 0x10 - 0xD8 + 0x34 == -0xBC)
acc = []
for i in body(0x00235720):
    for k, op in enumerate(i.operands):
        if op.type == 3 and T.R.md.reg_name(op.mem.base) == "rsp" and op.mem.index == 0:
            acc.append((i.address, i.mnemonic, op.mem.disp, k))
at34 = [(a, m) for a, m, d, k in acc if d == 0x34]
check("W6 inside 00235720 only the lea (00235930) and the movss read (00235959) touch rsp+0x34",
      sorted(at34) == [(0x00235930, "lea"), (0x00235959, "movss")], str([("%08X" % a, m) for a, m in at34]))
w30 = [a for a, m, d, k in acc if d == 0x30 and k == 0 and m.startswith("mov")]
w38 = [a for a, m, d, k in acc if d == 0x38 and k == 0 and m.startswith("mov")]
check("W7 control: the sweep sees writes to the neighbours +0x30 and +0x38", len(w30) >= 1 and len(w38) >= 1,
      "+0x30 %s; +0x38 %s" % (["%08X" % a for a in w30], ["%08X" % a for a in w38]))

# ============================================================ S: the child sort
pin("S1 records hold the sign-extended word +0x44", 0x00247A11, "movsx ecx, word ptr [rdx + 0x44]")
pin("S1 ... at record +0", 0x00247A1C, "mov dword ptr [rax - 8], ecx")
pin("S1 ... the index at record +4", 0x00247A15, "mov dword ptr [rax - 4], r8d")
pin("S1 ... counted from 0", 0x00247A03, "xor r8d, r8d")
pin("S1 ... the child at record +8", 0x00247A1F, "mov qword ptr [rax], rdx")
cmpb = ["%s %s" % (i.mnemonic, i.op_str) for i in T.R.md.disasm(T.R.at(0x00244610, 13), 0x00244610)]
check("S2 comparator 00244610: eax = b.prio - a.prio; if 0, a.idx - b.idx",
      cmpb[:6] == ["mov eax, dword ptr [rdx]", "sub eax, dword ptr [rcx]", "jne 0x24461c",
                   "mov eax, dword ptr [rcx + 4]", "sub eax, dword ptr [rdx + 4]", "ret "], " / ".join(cmpb))
check("S3 the priorities are i16, so b - a lies in [-65535, 65535] and cannot overflow", 32767 - (-32768) < 2 ** 31)
check("S4 002479B0 passes 00244610 as the sort's comparator (lea, stack argument)",
      [(f, a, k) for f, a, k in riprefs(0x00244610)] == [(0x002479B0, 0x00247A2F, "lea")]
      and ins(0x00247A3F) == "mov qword ptr [rsp + 0x20], rax" and ins(0x00247A4C) == "call 0x249ce0")
check("S5 00249CE0 is the shared sort: eight call sites", len(callers(0x00249CE0)) == 8 and
      (0x002479B0, 0x00247A4C) in callers(0x00249CE0))
pin("S6 00249CE0 takes the comparator from its fifth argument", 0x00249CFE, "mov r13, qword ptr [rsp + 0xb0]")
pin("S6 ... compares element with pivot", 0x00249D8F, "call r13")
pin("S6 ... stops advancing the left index on a non-negative result", 0x00249D94, "jns 0x249db5")
pin("S6 ... and keeps advancing while negative", 0x00249DB3, "js 0x249da0")
pin("S7 the sorted first record becomes the first child", 0x00247A58, "mov qword ptr [rdi + 0x18], rax")

# ============================================================ E: the two script adapters
DT = page("01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv")
check("E1 dispatch: 0x00EB eventplay -> 00354E80", re.search(r"^00EB\teventplay\t0\t00354E80\t", DT, re.M) is not None)
check("E2 dispatch: 0x00EC eventplay_ec -> 00354B20", re.search(r"^00EC\teventplay_ec\t1\t00354B20\t", DT, re.M) is not None)
check("E3 both handlers sit in .data slots and have no direct caller",
      len(T.qword_sites(0x00354E80)) >= 1 and len(T.qword_sites(0x00354B20)) >= 1 and callers(0x00354E80) == []
      and callers(0x00354B20) == [])

# ============================================================ R: board and register behind the pointers
for rid, w in (("L-12", "SUPERSEDED 2026-09-26"), ("L-13", "SUPERSEDED 2026-09-27")):
    check("R1 %s reads %s" % (rid, w), w in lead(rid))
B = json.load(open(os.path.join(DB, "_index", "_inbox", "TEAM.json"), encoding="utf-8"))
TK = {t["id"]: t for t in B["tasks"]}
rs = json.dumps(TK["FRONTIER-RT-RUNTIME-SURROGATE"])
check("R2 FRONTIER-RT-RUNTIME-SURROGATE does not carry L-13 (its seven rows are others)",
      "L-13" not in rs and "BG-6, BJ-1, BL-8, UC-2, UQ-332, GG-1, BQ-27" in rs)
l13 = TK["FABLE-REQ-ASTRA-L13-BANKS"]
check("R3 FABLE-REQ-ASTRA-L13-BANKS was DONE before the 2026-09-27 ruling", l13["status"] == "DONE" and
      l13["updated_at"][:10] < "2026-09-27", l13["updated_at"][:10])
naming = [t for t in B["tasks"] if "spawn-placement-and-retirement" in json.dumps(t)]
openn = sorted(t["id"] for t in naming if t["status"] != "DONE")
check("R4 no open board item names the spawn page except this batch's task", openn in ([], ["SWE2STRUCT-DD-B21-1001"]),
      "%d items name it; open: %s" % (len(naming), openn))
REVIEWS = ["ASTRA-CONTRA-FABLE-SPAWN-LIFECYCLE", "ASTRA-CONTRA-OPUS-SPAWN-LIFECYCLE", "ASTRA-CONTRA-FABLE-MANAGER-QUEUE",
           "ASTRA-CONTRA-OPUS-MANAGER-QUEUE", "ASTRA-REQ-FABLE-FIELD-PREP", "ASTRA-REQ-FABLE-RESTORE-REQUEST",
           "ASTRA-REQ-FABLE-WIDGET-TEARDOWN", "ASTRA-REQ-OPUS-WIDGET-TEARDOWN", "ASTRA-CONTRA-FABLE-WIDGET-ROOTS",
           "ASTRA-CONTRA-OPUS-WIDGET-ROOTS", "ASTRA-REQ-FABLE-WIDGET-RETENTION", "ASTRA-REQ-OPUS-WIDGET-RETENTION",
           "ASTRA-CONTRA-FABLE-WIDGET-GENERATION", "ASTRA-CONTRA-OPUS-WIDGET-GENERATION", "ASTRA-REQ-FABLE-LOAD-CLOSE",
           "ASTRA-REQ-OPUS-LOAD-CLOSE", "ASTRA-REQ-FABLE-LOAD-MATERIALIZATION", "ASTRA-REQ-OPUS-LOAD-MATERIALIZATION",
           "ASTRA-REQ-FABLE-LOAD-SUCCESS", "ASTRA-REQ-OPUS-LOAD-SUCCESS", "ASTRA-REQ-FABLE-STORAGE-COMPLETION",
           "ASTRA-REQ-OPUS-STORAGE-COMPLETION", "ASTRA-REQ-FABLE-SAVE-CONTAINER", "ASTRA-REQ-OPUS-SAVE-CONTAINER",
           "ASTRA-CONTRA-FABLE-OLD-SAVE-CONVERSION", "ASTRA-CONTRA-OPUS-OLD-SAVE-CONVERSION",
           "ASTRA-REQ-FABLE-GAMBIT-COMPATIBILITY-EXPORT", "ASTRA-REQ-OPUS-GAMBIT-COMPATIBILITY-EXPORT",
           "ASTRA-REQ-FABLE-OLD-SAVE-LIVE-REVIEW", "ASTRA-REQ-OPUS-OLD-SAVE-LIVE-REVIEW"]
notdone = [r for r in REVIEWS if TK.get(r, {}).get("status") != "DONE"]
check("R5 the %d review requests on sections 11-29 are DONE" % len(REVIEWS), notdone == [], str(notdone))

# ============================================================ C: the routed consumer
GP = page("09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md")
check("C1 the gambit page still says the restore helper copies both banks back",
      "`SpawnKeep_RestorePersistenceBank` copies them back." in GP)

# ============================================================ N: the notes are applied once, EOLs kept
TAG = "SWE2-STRUCT for OPUS, DD batch 21"
for rel, txt, n in ((SHOP, SH, 5), (SPAWN, SP, 8)):
    check("N1 %s carries %d batch-21 notes" % (rel.split("/")[-1], n), txt.count(TAG) == n, str(txt.count(TAG)))
    check("N1 %s stays pure CRLF" % rel.split("/")[-1], txt.count("\n") == txt.count("\r\n"))
    check("N1 %s has no open box" % rel.split("/")[-1], "- [ ]" not in txt and "- [~]" not in txt)

print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
