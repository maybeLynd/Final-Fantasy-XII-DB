"""Reopened page 1 (SWE2-STRUCT for OPUS, 2026-10-01):
02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md

Run: python -B p1_vbf_st2e.py   (last line FAILS n; must be FAILS 0)
Inputs, read only: the shipped archive FFXII_TZA.vbf (through agent_flow/tools/vbfextract.py, the archive the page's
section 1 sizes); the certified image through retool.py (sha 73461d08...); callpairs_kind2_packed40.txt in this folder
(the output of ../bucket-members-0929/checks/callpairs.py over the 40 four-language slots, control 00268762).

  A0-A2  the archive and the st2e population: 31,196,932,183 bytes, SRYK, 89,414 entries; 407 st2e entries over
         73 names, all under test_battle/<lang>/binaryfile (the population AY-3 read)
  H1-H9  THE FALSIFICATION PASS - section 2's St2eHeader struct, field by field, over all 407 shipped files:
         +0x10 zero in all 407 (survives); +0x18 and +0x1C NOT zero in all 407 (the struct's comments are false:
         4 + 4, each the array end); headerSize 32 in 393, 0 in 14 (no record array); heapOffset equal to
         headerSize + count*recordSize in 255, 0x20 in the 2 mons_act.bin copies, 0 in 150; the heap's 'one'
         dword is 1 in all 257; the three length-arithmetic rows and the five string-table rows of section 2
  T1-T6  the reopening trigger (section 6's 40 -> 82): pool 01E4D830 NULL only at 40, 83, 84 in 0..84; the names
         section 11 places; the ch block 01E6BB40 has the same names and NULLs; 002DF9A0 forms pool leas at slots
         0, 84, 128, 450, 1640 only; section 8's '2, 8' row: in every arm slot 2 gets a battle-manifest block and
         slot 8 a block whose entries 0..82 hold no test_battle path (it is the event .ebp / .mot array)
  K1-K4  residue: battle_pack.bin's 3 'unknown' sections are entries 0 (WepJob {u16 1, u16 23}), 39 (shop table
         {tag 0x64, stride 8, count 57, data 0xC}) and 70 (licd 24 x 24); its 2 containers are entries 10 and 61
  Q1-Q6  residue: no request by constant for any of the 40 four-language standalone copies - the kind-2 loader
         00384420's three callers take 0x13, 0x47 + n and the 28-byte table 01E09F68, which holds exactly the
         localised slots; no direct call to a request API carries (2, k) for the 40 (callpairs output, control)
"""
import io, os, re, struct, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ROOT = os.path.dirname(DB)
sys.path.insert(0, os.path.join(ROOT, "agent_flow", "tools"))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import vbfextract as V  # noqa: E402
import retool as T  # noqa: E402
import capstone  # noqa: E402

R = T.R
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
FAILS = 0
N = 0


def check(cid, ok, text, detail=""):
    global FAILS, N
    N += 1
    if not ok:
        FAILS += 1
    print("%s %-4s %s%s" % ("PASS" if ok else "FAIL", cid, text, ("  -- " + detail) if detail else ""))


def q(a):
    return struct.unpack("<Q", R.at(a, 8))[0]


def cs(a):
    return (R.at(a, 200) or b"").split(b"\0")[0].decode("latin1")


def leaf(a):
    return cs(a).split("\\")[-1] if a else None


# ---------------------------------------------------------------- archive
f = io.open(VBF, "rb")
check("A0", os.path.getsize(VBF) == 31196932183, "archive is 31,196,932,183 bytes", str(os.path.getsize(VBF)))
magic = open(VBF, "rb").read(4)
names, blocks = V.load_index(f)
check("A1", magic == b"SRYK" and len(names) == 89414, "magic SRYK, 89,414 entries", "%r %d" % (magic, len(names)))
st = []
for n in sorted(names):
    if n.lower().endswith(".bin"):
        b = V.read_entry(f, names, blocks, n)
        if b[:4] == b"st2e":
            st.append((n, b))
leafs = collections.Counter(n.split("/")[-1] for n, _ in st)
check("A2", len(st) == 407 and len(leafs) == 73 and all("/test_battle/" in n and "/binaryfile/" in n for n, _ in st),
      "407 st2e entries, 73 names, all under test_battle/<lang>/binaryfile", "%d %d" % (len(st), len(leafs)))

# ---------------------------------------------------------------- H: the falsification pass on section 2's struct
H = [(n, b, struct.unpack_from("<4s7I", b, 0)) for n, b in st]
nz10 = [n for n, b, h in H if h[4]]
check("H1", not nz10, "+0x10 (reservedA) is 0 in all 407 (section 2's comment survives)", str(nz10))
nz18 = [(n.split("/")[4], n.split("/")[-1], h[6], h[3] + h[1] * h[2]) for n, b, h in H if h[6]]
check("H2", len(nz18) == 4 and all(x[1] == "eitm_data.bin" and x[2] == 0x7144 == x[3] for x in nz18)
      and sorted(x[0] for x in nz18) == ["ch", "cn", "in", "kr"],
      "+0x18 is NOT 0 in all 407: 0x7144 in the 4 eitm_data.bin copies (ch cn in kr), = headerSize + count*recordSize "
      "(32 + 557*52); section 2's '0 in all 407 shipped files' for reservedB is false", str(nz18))
nz1c = [(n.split("/")[4], n.split("/")[-1], h[7], h[3] + h[1] * h[2]) for n, b, h in H if h[7]]
check("H3", len(nz1c) == 4 and all(x[1] == "tutorial_data.bin" and x[2] == 0x98 == x[3] for x in nz1c),
      "+0x1C is NOT 0 in all 407: 0x98 in the 4 tutorial_data.bin copies, = 32 + 6*20; section 2's comment for "
      "reservedC is false", str(nz1c))
h0 = [(n.split("/")[-1], h[1], h[2], len(b)) for n, b, h in H if h[3] != 32]
check("H4", len(h0) == 14 and all(x[1] * x[2] == 0 for x in h0)
      and all(h[3] in (0, 32) for n, b, h in H)
      and collections.Counter(x[0] for x in h0) == collections.Counter(
          {"jochumodel_data.bin": 4, "s_daiji_data.bin": 4, "actionchip_data.bin": 2, "bukitye_data.bin": 2,
           "mons_act.bin": 2}),
      "headerSize is 32 in 393 and 0 in 14 (jochumodel x4, s_daiji x4, actionchip x2, bukitye x2, mons_act x2), "
      "every 0 with count*recordSize == 0: no record array", str(collections.Counter(x[0] for x in h0)))
heap_end = [n for n, b, h in H if h[5] and h[5] == h[3] + h[1] * h[2]]
heap_20 = [n for n, b, h in H if h[5] and h[5] != h[3] + h[1] * h[2]]
heap_0 = [n for n, b, h in H if not h[5]]
check("H5", len(heap_end) == 255 and len(heap_0) == 150 and len(heap_20) == 2
      and all(n.endswith("/mons_act.bin") and h[5] == 0x20 and h[3] == 0 for n, b, h in H if n in heap_20),
      "heapOffset +0x14: = headerSize + count*recordSize in 255, 0 in 150, and 0x20 in the 2 mons_act.bin copies "
      "(headerSize 0, recordSize 0): the 'headerSize + count*recordSize, or 0' comment misses those 2",
      "%d %d %d" % (len(heap_end), len(heap_0), len(heap_20)))
ones = [struct.unpack_from("<I", b, h[5])[0] for n, b, h in H if h[5]]
check("H6", len(ones) == 257 and set(ones) == {1}, "the dword at every non-zero heapOffset is 1 (the heap's 'one'), 257 of 257",
      str(collections.Counter(ones)))
byname = collections.defaultdict(list)
for n, b, h in H:
    byname[n.split("/")[-1]].append((n.split("/")[4], b, h))
for cid, fn, size, cnt, rec in (("H7a", "action_data.bin", 32612, 543, 60), ("H7b", "ability_data.bin", 1056, 128, 8),
                                ("H7c", "attribute_data.bin", 48, 8, 2)):
    rows = byname[fn]
    ok = any(l == "in" for l, b, h in rows) and all(len(b) == size and h[1] == cnt and h[2] == rec and h[3] == 32 and 32 + cnt * rec == size
                      for l, b, h in rows if l == "in")
    check(cid, bool(ok), "%s (in): %d bytes = 32 + %d*%d, exact" % (fn, size, cnt, rec),
          str([(l, len(b), h[1], h[2]) for l, b, h in rows if l == "in"]))
for cid, fn, cnt, rec, size in (("H8a", "listhelp_action.bin", 251, 4, 7556), ("H8b", "help_action.bin", 322, 4, 9848),
                                ("H8c", "questtitle.bin", 257, 4, 3032), ("H8d", "key_signal.bin", 69, 4, 824),
                                ("H8e", "battle_message.bin", 102, 8, 6668)):
    rows = [(l, b, h) for l, b, h in byname[fn] if l == "us"]
    ok = len(rows) == 1 and rows[0][2][1] == cnt and rows[0][2][2] == rec and len(rows[0][1]) == size \
        and len(rows[0][1]) != 32 + cnt * rec and rows[0][2][5] == 32 + cnt * rec
    check(cid, ok, "%s (us): %d x %d, %d bytes, the arithmetic does not close and +0x14 = 32 + count*rec" % (fn, cnt, rec, size),
          str([(l, len(b), h[1], h[2], h[5]) for l, b, h in rows]))
check("H9", sum(1 for n, b, h in H if h[3] == 32) == 393, "headerSize 32 count is 393 of 407 (the complement of H4)")

# ---------------------------------------------------------------- T: the reopening trigger (section 6, 40 -> 82)
POOL, CH = 0x01E4D830, 0x01E6BB40
nulls = [i for i in range(85) if q(POOL + 8 * i) == 0]
check("T1", nulls == [40, 83, 84], "pool 01E4D830 slots 0..84: NULL only at 40, 83 and 84 (82 entries + interior NULL)",
      str(nulls))
want = {0: "WepJob_Matrix.bin", 14: "action_data.bin", 19: "battle_pack.bin", 39: "shop_data.bin", 41: "attribute_data.bin",
        47: "listhelp_action.bin", 49: "listhelp_status.bin", 58: "ability_data.bin", 61: "word.bin", 82: "board_12.bin"}
got = {k: leaf(q(POOL + 8 * k)) for k in want}
check("T2", got == want and all("\\test_battle\\in\\" in cs(q(POOL + 8 * k)) for k in range(83) if k != 40),
      "section 11's slot names (0, 14, 19, 39, 41, 47, 49, 58, 61, 82), every entry an in test_battle path", str(got))
chn = [i for i in range(85) if q(CH + 8 * i) == 0]
same = all(leaf(q(POOL + 8 * k)) == leaf(q(CH + 8 * k)) for k in range(83) if k != 40)
check("T3", chn == [40, 83, 84] and same and "\\ch\\" in cs(q(CH)), "the ch block 01E6BB40: the same 82 names and NULLs",
      str(chn))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
SZ = T.sizes()
code = R.at(0x002DF9A0, SZ[0x002DF9A0])
leas, stores, last = [], [], {}
for i in md.disasm(code, 0x002DF9A0):
    for op in i.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
            g = i.address + i.size + op.mem.disp
            if i.mnemonic == "lea":
                leas.append(g)
                last[i.operands[0].reg] = g
            elif i.mnemonic == "mov" and i.operands[0].type == capstone.x86.X86_OP_MEM and 0x0215F000 <= g < 0x0215F148:
                src = i.operands[1].reg if i.operands[1].type == capstone.x86.X86_OP_REG else None
                stores.append(((g - 0x0215F000) // 8, last.get(src)))
slots = sorted(set((g - POOL) // 8 for g in leas if POOL <= g < POOL + 8 * 2000 and (g - POOL) % 8 == 0))
check("T4", slots == [0, 84, 128, 450, 1640], "002DF9A0's leas into the pool: slots 0, 84, 128, 450, 1640 only", str(slots))
s2 = [v for k, v in stores if k == 2]
s8 = [v for k, v in stores if k == 8]
ok2 = len(s2) == 10 and all(v and "\\test_battle\\" in cs(q(v)) and leaf(q(v)) == "WepJob_Matrix.bin" for v in s2)
check("T5", ok2, "directory slot 2 receives a battle-manifest block (entry 0 WepJob_Matrix.bin) in all 10 arms",
      str([hex(v) for v in s2]))
ok8 = len(s8) == 10 and all(v and not any(q(v + 8 * k) and "\\test_battle\\" in cs(q(v + 8 * k)) for k in range(83)) for v in s8)
first8 = []
for v in s8:
    k = next((k for k in range(400) if q(v + 8 * k)), None)
    first8.append(cs(q(v + 8 * k)) if k is not None else None)
ok8b = all(p and "\\event\\" in p and p.endswith(".ebp") for p in first8)
check("T6", ok8 and ok8b, "directory slot 8 is NOT the battle manifest: in all 10 arms its entries 0..82 hold no test_battle "
      "path, and its first entry is an event .ebp path (section 8's '2, 8' row is wrong on slot 8)", first8[-1] or "")

# ---------------------------------------------------------------- K: battle_pack's 'unknown' sections
pk = V.read_entry(f, names, blocks, "ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin")
cnt = struct.unpack_from("<I", pk, 0)[0]
offs = struct.unpack_from("<%dI" % (cnt + 1), pk, 4)
kinds = {}
for i in range(cnt):
    s = pk[offs[i]:offs[i + 1]]
    if not s:
        k = "empty"
    elif s[:4] == b"st2e":
        k = "st2e"
    else:
        c = struct.unpack_from("<I", s, 0)[0]
        k = "other"
        if 4 + 4 * (c + 1) <= len(s):
            o = struct.unpack_from("<%dI" % (c + 1), s, 4)
            if o[0] == 4 + 4 * (c + 1) and all(o[j] <= o[j + 1] for j in range(c)) and o[c] <= len(s):
                k = "container"
    kinds.setdefault(k, []).append(i)
tally = {k: len(v) for k, v in kinds.items()}
check("K1", cnt == 71 and tally == {"st2e": 37, "container": 2, "other": 3, "empty": 29},
      "battle_pack.bin (us): 71 entries = 37 st2e + 2 containers + 3 other + 29 empty (section 9's census)", str(tally))
check("K2", kinds.get("container") == [10, 61] and kinds.get("other") == [0, 39, 70],
      "the 2 containers are entries 10 (commandpack, AY-4) and 61 (word.bin); the 3 'unknown' are entries 0, 39, 70",
      "%s %s" % (kinds.get("container"), kinds.get("other")))
e0 = pk[offs[0]:offs[1]]
e39 = pk[offs[39]:offs[40]]
e70 = pk[offs[70]:offs[71]]
st0, c0 = struct.unpack_from("<HH", e0, 0)
tag, s39, c39, d39 = struct.unpack_from("<IHHI", e39, 0)
w, hh = struct.unpack_from("<HH", e70, 4)
check("K3", (st0, c0) == (1, 23) and 4 + st0 * c0 <= len(e0) and (tag, s39, c39, d39) == (0x64, 8, 57, 0xC),
      "entry 0 is the WepJob matrix {u16 stride 1, u16 count 23, u8 row[23]}; entry 39 the shop table "
      "{tag 0x64, stride 8, count 57, data 0xC} (the 2026-09-29 SWE2-DATA paragraph)", "%d %d" % (st0, c0))
check("K4", e70[:4] == b"licd" and (w, hh) == (24, 24) and 8 + 2 * w * hh <= len(e70),
      "entry 70 is a licd grid {licd, u16 24, u16 24, u16 cell[576]} (license-board-grid-format.md)", "%r %d %d" % (e70[:4], w, hh))

# ---------------------------------------------------------------- Q: are the 40 four-language standalone copies requested?
LANGS = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]
low = {n.lower() for n in names}
four, local = [], []
for k in range(83):
    p = q(POOL + 8 * k)
    fn = leaf(p).lower() if p else None
    langs = [l for l in LANGS if fn and ("ps2data/image/ff12/test_battle/%s/binaryfile/%s" % (l, fn)) in low]
    ne = k < cnt and offs[k + 1] > offs[k]
    if ne and len(langs) == 4:
        four.append(k)
    if not ne and len(langs) == 9 and k != 19:
        local.append(k)
check("Q1", len(four) == 40 and 14 in four and 10 in four,
      "40 slots are packed (non-empty pack entry) and ship standalone in exactly 4 languages; action_data (14) and "
      "commandpack (10) among them", str(four))
callers = T.scan()["calls"]
c420 = sorted(set(fn for fn, site in callers.get(0x00384420, ())))
c3f0 = sorted(set(site for fn, site in callers.get(0x003843F0, ())))
check("Q2", c420 == [0x00238260, 0x002385D0, 0x003843F0] and c3f0 == [0x002369CE, 0x00236C6B],
      "the kind-2 loader 00384420 has three callers (00238260, 002385D0, 003843F0); 003843F0 is called at 002369CE "
      "and 00236C6B", str([hex(x) for x in c420 + c3f0]))


def ins(a):
    i = next(md.disasm(R.at(a, 16), a))
    return "%s %s" % (i.mnemonic, i.op_str)


check("Q3", ins(0x002369C2) == "mov ecx, 0x13" and ins(0x00236C5B) == "mov ecx, 0x13" and ins(0x0023836A) == "add ecx, 0x47",
      "the id at 003843F0's two calls is 0x13 (battle_pack.bin, slot 19); the board caller adds 0x47 (slots 71..82)",
      "%s / %s / %s" % (ins(0x002369C2), ins(0x00236C5B), ins(0x0023836A)))
tab = list(R.at(0x01E09F68, 0x1C))
check("Q4", ins(0x002385E1).startswith("lea rcx") and ins(0x002385D9) == "cmp ecx, 0x1b"
      and sorted(x for x in tab if x < 0x80) == sorted(local + [67]) and not set(tab) & set(four),
      "002385D0 indexes the 28-byte table 01E09F68 (cmp ecx, 0x1b); its 27 ids are the 26 localised slots plus 67 "
      "(menu05.bin, which ships nowhere), and none of the 40", str(tab))
cp = open(os.path.join(HERE, "callpairs_kind2_packed40.txt"), encoding="utf-8").read().splitlines()
hdr = cp[0]
wanted = set(int(x, 16) for x in re.findall(r"\('0x2', '(0x[0-9a-f]+)'\)", hdr))
API = {0x32E400, 0x32E620, 0x3843F0, 0x384420, 0x24AB90, 0x249210, 0x2493D0, 0x249350, 0x249180}
allhits = [l.split("\t") for l in cp[1:] if l and not l.startswith(("CONTROL", "FAILS"))]
hits = [h for h in allhits if len(h) > 3 and "=0x2," in h[2]]
ctl = [h for h in allhits if len(h) > 3 and h[0] == "00268762" and "=0x9, next=0x4" in h[2] and h[3] == "call 0x32e400"]
tg = [int(h[3].split("0x")[1], 16) for h in hits if len(h) > 3 and re.match(r"call 0x[0-9a-f]+$", h[3])]
reg = [h for h in hits if len(h) > 3 and re.match(r"call r[a-z0-9]+$", h[3])]
check("Q5", wanted == set(four) and ctl and "CONTROL 00268762: PASS" in cp and cp[-1] == "FAILS 0" and not set(tg) & API,
      "callpairs over all 122,250 call sites: no direct call to a request API carries (2, k) for any of the 40 "
      "(control 00268762, MapRef (9, 4), reported)", "%d sites, %d direct targets" % (len(hits), len(set(tg))))
regsites = sorted(set(h[1].split()[0] for h in reg))
code313 = R.at(0x00313A00, SZ[0x00313A00])
lt = set()
for i in md.disasm(code313, 0x00313A00):
    if i.mnemonic == "lea" and i.operands[1].type == capstone.x86.X86_OP_MEM and i.operands[1].mem.base == capstone.x86.X86_REG_RIP:
        lt.add(i.address + i.size + i.operands[1].mem.disp)
check("Q6", regsites == ["00313A00", "003F8B40", "00808D78"] and {0x002E1CA0, 0x002E1C20} <= lt and not lt & API
      and ins(0x003F8B60) == "mov rax, qword ptr [rbx + 0x38]",
      "the register calls are 00313A00 (targets 002E1CA0 / 002E1C20, not request APIs), 003F8B40 (an object's own "
      "+0x38 callback) and 00808D78 (the CRT TLS callback walk)", str(regsites))
print("CHECKS %d" % N)
print("FAILS %d" % FAILS)
