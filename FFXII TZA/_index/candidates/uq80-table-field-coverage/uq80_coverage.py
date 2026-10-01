#!/usr/bin/env python3
"""uq80_coverage.py - UQ-80 coverage census of the authored battle_pack.bin tables behind the class slots.

Deterministic; stdlib + capstone only.  Inputs:
  * the shipping exe, its function list (graph) and the us battle_pack.bin (the three roots below);
  * uq80_manifest.tsv beside this script: one row per field / pad span per table, each marked
    page (meaning stated on a DB page), pass (meaning derived in the UQ-80 pass), pad (constant, no reader)
    or shape (no meaning) - see the manifest header;
  * the DB pages the manifest cites (existence checked; the registry and encoded-id pages parsed for shapes).

What it does:
  1. reads every table's st2e section out of battle_pack.bin itself (directory dword at +dir) and checks the header;
  2. checks every manifest row: offsets inside the record, no overlaps, pad spans constant over every shipped row,
     every cited reader instruction decodes to a memory operand of the stated displacement and width, every cited
     page exists;
  3. per table prints bytes mapped by pages, by this pass, as pads, and the residue; then one final
     "residue: N tables, M unmapped bytes, named: ..." line naming every unmapped (table, offset);
  4. runs the known-answer controls inline (C1-C10) and exits 1 if any control or manifest check FAILs.
Usage: python uq80_coverage.py [--write-coverage coverage.tsv]
"""
import os, re, sys, struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

# ---- the three roots (no scratch paths) ------------------------------------------------------------------------
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 5))
EXE = os.path.join(REPO, r"Database\Tools\work\exe\FFXII_TZA.exe")
FUNCS = os.path.join(REPO, r"Database\Tools\work\graph\functions.tsv")
PACK = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle\us\binaryfile\battle_pack.bin"
DB = os.path.join(REPO, r"Database\FFXII TZA")
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "uq80_manifest.tsv")
BASE = 0x120000

PAGES = {
    "EID": "00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md",
    "BAZ": "12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md",
    "GAMB": "09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md",
    "ACT": "07-Combat-Action/Action-Definition-Row/the-action-definition-row.md",
    "UDEF": "04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md",
    "EQC": "12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md",
    "AUTO": "08-Combat-Formula/the-auto-status-rebuild.md",
    "ASR": "10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md",
    "BSR": "08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md",
    "LCHK": "12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md",
    "LBV": "16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md",
    "TYPES": "_types/fields.tsv",
    "TEXT": "02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md",
    "ATK": "08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md",
    "MP": "10-Status-Periodic-Terminal/where-mp-comes-from.md",
    "IIE": "12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md",
    "REG": "02-Resource-And-Asset-Pipeline/authored-data-table-registry.md",
    "VBF": "02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md",
    "CLOSE": "07-Combat-Action/how-close-a-unit-must-stand-to-act.md",
}

# The 20 sections of the UQ-80 box (18 lines, the key-item line is three sections) plus the three class slots with their own binders. (name, slot, directory offset)
TABLES = [
    ("chr_data", 0x02EBF130, 0x44), ("dougu_data", 0x02EBF100, 0x4C), ("eventitem_data", 0x02EBF098, 0x84),
    ("maho_data", 0x02EBF0F0, 0x78), ("waza_data", 0x02EBF0E8, 0x7C), ("gambit_data", 0x02EBF0E0, 0x24),
    ("m_daiji", 0x02EBF090, 0x88), ("g_daiji", 0x02EBF088, 0x8C), ("q_daiji", 0x02EBF080, 0x90),
    ("eis_data", 0x02EBF070, 0x98), ("questreward_data", 0x02EBF068, 0x9C), ("price_data", 0x02EBF060, 0x74),
    ("menkyo_data", 0x02EBF0C8, 0x6C), ("horidashi", 0x02EBF058, 0xE8), ("comac_data", 0x02EBF128, 0x48),
    ("mgccategory_data", 0x02EBF110, 0x30), ("license_data", 0x02EBF038, 0x34), ("attribute_data", 0x02EBF050, 0xA8),
    ("sobicategory_data", 0x02EBF0B0, 0x18), ("ability_data", 0x02EBF040, 0xEC),
    ("eitm_data", 0x02EBF0F8, 0x38), ("status_data", 0x02EBF118, 0x40), ("action_data", 0x02EBF138, 0x3C),
]
# The other four class slots of the "26" are not battle_pack entries (registry box: .ard slots 0 and 2, the gambit
# target definitions, and 02EBF0D0); they cannot be measured from battle_pack.bin and are listed, not counted.
NON_PACK = [("02EBF150", "class 4, .ard slot 0"), ("02EBF120", "class 3, .ard slot 2"),
            ("02EBF0D8", "class 11, gambit target definitions"), ("02EBF0D0", "class 12")]

FAILS = []
def check(label, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label, (" - " + detail) if detail else ""))
    if not ok: FAILS.append(label)
    return ok

# ---- exe: sections, functions, disassembly ---------------------------------------------------------------------
img = open(EXE, "rb").read()
_pe = struct.unpack_from("<I", img, 0x3C)[0]
_ns = struct.unpack_from("<H", img, _pe + 6)[0]; _opt = struct.unpack_from("<H", img, _pe + 20)[0]
SECS = []
for _i in range(_ns):
    _o = _pe + 24 + _opt + _i * 40
    SECS.append((img[_o:_o + 8].rstrip(b"\0").decode(), struct.unpack_from("<I", img, _o + 12)[0],
                 struct.unpack_from("<I", img, _o + 8)[0], struct.unpack_from("<I", img, _o + 20)[0],
                 struct.unpack_from("<I", img, _o + 16)[0]))
def off(va):
    """section-aware VA -> file offset; None for a virtual tail (reads as zero) or outside the image"""
    r = va - BASE
    for name, sva, vsz, raw, rawsz in SECS:
        if sva <= r < sva + max(vsz, rawsz):
            return raw + (r - sva) if (r - sva) < rawsz else None
    return None
FUNC = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: FUNC[int(p[0], 16)] = (p[1], int(p[2]))
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def dis1(va):
    o = off(va)
    if o is None: return None
    for x in md.disasm(img[o:o + 16], va, 1): return x
    return None
def disfunc(entry):
    name, size = FUNC[entry]
    o = off(entry)
    return list(md.disasm(img[o:o + size], entry))

# ---- pack --------------------------------------------------------------------------------------------------------
pk = open(PACK, "rb").read()
u32 = lambda o: struct.unpack_from("<I", pk, o)[0]
def section(doff):
    t = u32(doff)
    return dict(start=t, magic=pk[t:t + 4], count=u32(t + 4), size=u32(t + 8), hdr=u32(t + 0xC))
def records(doff):
    h = section(doff)
    b = h["start"] + h["hdr"]
    return [pk[b + i * h["size"]: b + (i + 1) * h["size"]] for i in range(h["count"])], h
REC = {}; HDR = {}
for name, slot, doff in TABLES:
    REC[name], HDR[name] = records(doff)

# ---- manifest ----------------------------------------------------------------------------------------------------
ROWS = collections.defaultdict(list)
for line in open(MANIFEST, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#") or line.startswith("table\t"): continue
    p = line.split("\t")
    if len(p) != 9:
        check("manifest row has 9 columns", False, line[:80]); continue
    t, o, w, st, nm, meaning, ev, readers, src = p
    ROWS[t].append(dict(off=int(o, 16), width=int(w), status=st, name=nm, meaning=meaning, evidence=ev,
                        readers=[r for r in readers.split(",") if r], source=src))

def parse_reader(tok, f):
    m = re.fullmatch(r"([0-9A-F]{8})(?:@(0x[0-9A-Fa-f]+|\d+))?(?::w(\d+))?", tok)
    if not m: return None
    va = int(m.group(1), 16)
    disp = int(m.group(2), 0) if m.group(2) else f["off"]
    size = int(m.group(3)) if m.group(3) else f["width"]
    return va, disp, size
def reader_ok(va, disp, size):
    x = dis1(va)
    if x is None: return False, "no decode"
    for o in x.operands:
        if o.type == X86_OP_MEM and o.mem.base != 0 and x.reg_name(o.mem.base) != "rip" and o.mem.disp == disp and o.size == size:
            return True, "%s %s" % (x.mnemonic, x.op_str)
    return False, "%s %s" % (x.mnemonic, x.op_str)

# ---- a compact copy of the reader-sweep dataflow (trace.py), for the instrument controls -----------------------
FAM = {}
for fam in [("rax","eax","ax","al"),("rbx","ebx","bx","bl"),("rcx","ecx","cx","cl"),("rdx","edx","dx","dl"),
            ("rsi","esi","si","sil"),("rdi","edi","di","dil"),("rbp","ebp","bp","bpl"),("rsp","esp","sp","spl")] + \
           [tuple("r%d%s" % (i, s) for s in ("", "d", "w", "b")) for i in range(8, 16)]:
    for r in fam: FAM[r] = fam[0]
def row_reads(entry, slot):
    """flow-aware (union at joins) pass over one function: T = [slot], O = [T+0xC], W = [T+8], R = 0020E600(O),
    P = W*idx, X = a row pointer.  Returns {(disp, size)} of memory reads based on X (or on R with an index).
    Direct jumps and fallthrough only; small, jump-table-free bodies (used for the instrument controls)."""
    ins = {x.address: x for x in disfunc(entry)}
    order = sorted(ins); nxt = dict(zip(order, order[1:]))
    rn = lambda x, r: FAM.get(x.reg_name(r), x.reg_name(r)) if r else None
    IN = {order[0]: {}}; work = [order[0]]; found = set()
    while work:
        a = work.pop(); st = {k: set(v) for k, v in IN[a].items()}; x = ins[a]; ops = x.operands; mn = x.mnemonic
        def tag(op):
            if op.type == X86_OP_REG: return set(st.get(rn(x, op.reg), ()))
            if op.type == X86_OP_MEM:
                b = rn(x, op.mem.base)
                if b == "rip": return {"T"} if x.address + x.size + op.mem.disp == slot and op.size == 8 else set()
                if "T" in st.get(b, ()): return {{0xC: "O", 8: "W"}[op.mem.disp]} if op.mem.disp in (0xC, 8) else set()
            return set()
        if mn != "lea" and not mn.startswith("nop"):
            for o in ops:
                if o.type != X86_OP_MEM: continue
                bt = st.get(rn(x, o.mem.base), set()); ix = rn(x, o.mem.index)
                if "X" in bt or ("R" in bt and ix): found.add((o.mem.disp, o.size))
        succ = []
        if mn.startswith("j") and ops and ops[0].type == X86_OP_IMM and ops[0].imm in ins: succ.append(ops[0].imm)
        if mn not in ("jmp", "ret", "int3") and a in nxt: succ.append(nxt[a])
        if mn == "call":
            rcx = st.get("rcx", set())
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"): st.pop(r, None)
            if ops and ops[0].type == X86_OP_IMM and ops[0].imm == 0x20E600 and "O" in rcx: st["rax"] = {"R"}
        elif ops and ops[0].type == X86_OP_REG and mn not in ("cmp", "test", "push") and not mn.startswith("j"):
            d = rn(x, ops[0].reg); sop = ops[1] if len(ops) > 1 else None; t = set()
            if mn in ("mov", "movzx", "movsxd"): t = tag(sop)
            elif mn == "imul": t = {"P"} if any("W" in tag(o) for o in ops) else set()
            elif mn == "add": t = {"X"} if (st.get(d, set()) | (tag(sop) if sop is not None else set())) & {"R", "X"} else set()
            elif mn == "lea": t = {"X"} if st.get(rn(x, sop.mem.base), set()) & {"R", "X"} else set()
            if t: st[d] = t
            else: st.pop(d, None)
        for s2 in succ:
            if s2 not in IN: IN[s2] = {k: set(v) for k, v in st.items()}; work.append(s2)
            else:
                ch = False
                for k, v in st.items():
                    if not v <= IN[s2].get(k, set()): IN[s2].setdefault(k, set()).update(v); ch = True
                if ch: work.append(s2)
    return found

# =================================================================================================================
print("UQ-80 coverage census - battle_pack.bin (us), %d tables" % len(TABLES))
print("controls:")

# C1 shapes: every section is st2e with a 0x20 header, fits before the next section, and reproduces the shapes the
#    registry box (20 sections) and the encoded-id page section 2.5 (the three class slots) state.
reg = open(os.path.join(DB, PAGES["REG"]), encoding="utf-8").read()
box = reg[re.search(r"- \[[ x]\] \*\*UQ-80\.\*\*", reg).start():]  # ticked or not: the box is read for its table, not its state (fixed 2026-09-27, FABLE, after 03c573fe6 ticked it)
box = box[:box.index("**Class slots with another loader.**")]
stated = {}
for line in box.splitlines():
    if not line.strip().startswith("| `02EBF"): continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    names = re.findall(r"`(\w+)`", c[3]); shape = c[4].split("(")[0]
    nums, size = shape.split("\u00d7")
    counts = [int(n) for n in re.findall(r"\d+", nums)]
    for n, k in zip(names, counts): stated[n] = (k, int(re.search(r"\d+", size).group()))
eid = open(os.path.join(DB, PAGES["EID"]), encoding="utf-8").read()
for m in re.finditer(r"\| \d+ \| `(02EBF[0-9A-F]{3})` \| `\+(0x[0-9A-F]+)` \| (\d+) \u00d7 (\d+) \|", eid):
    for name, slot, doff in TABLES:
        if slot == int(m.group(1), 16) and name not in stated: stated[name] = (int(m.group(3)), int(m.group(4)))
starts = sorted(set(u32(4 * k) for k in range(1, 0x48) if 0 < u32(4 * k) < len(pk)))
bad = []
for name, slot, doff in TABLES:
    h = HDR[name]; nxt = min([s for s in starts if s > h["start"]] + [len(pk)])
    if h["magic"] != b"st2e" or h["hdr"] != 0x20 or h["start"] + 0x20 + h["count"] * h["size"] > nxt: bad.append(name + " header")
    if stated.get(name) != (h["count"], h["size"]): bad.append("%s %s vs stated %s" % (name, (h["count"], h["size"]), stated.get(name)))
check("C1 shapes: %d sections read from the pack reproduce the registry/encoded-id stated count x size" % len(TABLES), not bad, "; ".join(bad))

# C2 names through a .data pointer table: manifest slot k = pack entry k (directory +4+4k), names at 01E4D830.
#    Tests the section-aware VA->offset (a .text-only offset corrupts this read) and the directory offsets.
o = off(0x01E4D830); bad = []
for name, slot, doff in TABLES:
    q = struct.unpack_from("<Q", img, o + 8 * ((doff - 4) // 4))[0]
    qo = off(q); s = img[qo:img.index(b"\0", qo)].decode(errors="replace") if qo else ""
    if name not in s.split("\\")[-1]: bad.append("%s -> %r" % (name, s))
check("C2 file names via 01E4D830 match all %d directory offsets" % len(TABLES), not bad, "; ".join(bad))

# C3 a count the pages state: price_data holds 1 on 45 rows (encoded-id page 2.8 / registry).
ones = sum(1 for r in REC["price_data"] if struct.unpack_from("<I", r, 0)[0] == 1)
check("C3 price_data rows equal to 1: 45 (stated)", ones == 45, "measured %d" % ones)
vals = sorted(struct.unpack_from("<I", r, 0)[0] for r in REC["price_data"] if struct.unpack_from("<I", r, 0)[0] != 1)
print("       note: the other %d rows run %d .. %d (the encoded-id page says 30 .. 11,160)" % (len(vals), vals[0], vals[-1]))

# C4 questreward: rows 128-172 carry a first id, every other row is 0xFFFF (encoded-id page 2.8).
rows = [i for i, r in enumerate(REC["questreward_data"]) if struct.unpack_from("<H", r, 0)[0] != 0xFFFF]
check("C4 questreward_data non-empty rows are exactly 128..172", rows == list(range(128, 173)), "measured %s..%s (%d)" % (rows[0], rows[-1], len(rows)))

# C5 action_data +0x15..+0x17 zero on all 543 rows, and +0x26 non-zero on 13 rows valued 27..39 (action page).
z = all(r[0x15:0x18] == b"\0\0\0" for r in REC["action_data"])
e = sorted(r[0x26] for r in REC["action_data"] if r[0x26])
check("C5 action_data +0x15..+0x17 zero on 543 and +0x26 = 27..39 on 13 rows", z and e == list(range(27, 40)), "zero=%s esper=%s" % (z, e))

# C6 reader instrument, known answers: the row reads of three published readers reproduce their pages' layouts.
got = row_reads(0x002FD530, 0x02EBF070)
check("C6a 002FD530 row reads = {u32 +0, u16 +4, +6, +8, +0xA} (encoded-id 2.8)", got == {(0, 4), (4, 2), (6, 2), (8, 2), (0xA, 2)}, str(sorted(got)))
got = row_reads(0x002FD780, 0x02EBF058)
check("C6b 002FD780 row reads = three (u16 item, u8 count) pairs from +4 (bazaar page 2.1)", got == {(4, 2), (6, 1), (8, 2), (0xA, 1), (0xC, 2), (0xE, 1)}, str(sorted(got)))
got = row_reads(0x002FD640, 0x02EBF068)
check("C6c 002FD640 row reads = six u16 ids +0..+0xA (encoded-id 2.8)", got == {(0, 2), (2, 2), (4, 2), (6, 2), (8, 2), (0xA, 2)}, str(sorted(got)))
got = row_reads(0x002FD530, 0x02EBF068)
check("C6d negative: 002FD530 has no row read for a slot it does not load (02EBF068)", got == set(), str(sorted(got)))

# C7 reader-check sensitivity: the decoder check accepts the published operand and rejects a wrong width / disp.
okc, _ = reader_ok(0x002FD5A9, 0, 4); w_bad, _ = reader_ok(0x002FD5A9, 0, 2); d_bad, _ = reader_ok(0x002FD5D8, 5, 2)
check("C7 reader check: 002FD5A9 = dword [row+0] accepted; wrong width and wrong disp rejected", okc and not w_bad and not d_bad)

# C8 pad-check sensitivity: a byte known to vary (dougu +0, the sort key) is not constant, a known pad (+1) is.
v0 = len(set(r[0] for r in REC["dougu_data"])); v1 = len(set(r[1] for r in REC["dougu_data"]))
check("C8 pad check: dougu +0 varies (%d values), dougu +1 constant" % v0, v0 > 1 and v1 == 1)

# C9 joins behind three pass meanings: the item / magick / technick row's action-row byte.
act = REC["action_data"]; H = lambda r, o: struct.unpack_from("<H", r, o)[0]
j1 = sum(1 for i, r in enumerate(REC["dougu_data"]) if H(act[r[7]], 0x22) == i and H(act[r[7]], 0x34) == H(r, 8))
j2 = sum(1 for i, r in enumerate(REC["maho_data"]) if H(act[r[2]], 0x22) == 0x3000 + i and H(act[r[2]], 0x34) == H(r, 4) and act[r[2]][0x1E] == 1)
j3 = sum(1 for i, r in enumerate(REC["waza_data"]) if H(act[r[2]], 0x22) == 0x4000 + i and H(act[r[2]], 0x34) == H(r, 4) and act[r[2]][0x1E] == 2)
check("C9 action-row joins: dougu +7 64/64, maho +2 81/81, waza +2 24/24", (j1, j2, j3) == (64, 81, 24), str((j1, j2, j3)))

# C10 a sort-key comparator really compares query +0x30 (the pass meaning of every sortKey row).
x1, x2 = dis1(0x002D01CE), dis1(0x002D01D8)
check("C10 002D01A0 compares query +0x30 of two ids (002D01CE, 002D01D8)",
      x1 is not None and x2 is not None and "+ 0x30]" in x1.op_str and x2.mnemonic == "sub" and "+ 0x30]" in x2.op_str)

# ---- manifest checks and the census -----------------------------------------------------------------------------
print("manifest checks:")
n_readers = 0; n_pages = set()
census = []; residue = []
for name, slot, doff in TABLES:
    size = HDR[name]["size"]; recs = REC[name]
    owner = [None] * size; bad = []
    for f in ROWS.get(name, []):
        if f["off"] + f["width"] > size: bad.append("%#x past the record" % f["off"]); continue
        for b in range(f["off"], f["off"] + f["width"]):
            if owner[b] is not None: bad.append("%#x overlaps" % b)
            owner[b] = f
        if f["status"] not in ("page", "pass", "pad", "shape"): bad.append("%#x status %s" % (f["off"], f["status"]))
        src = f["source"]
        if src != "PASS":
            if src not in PAGES or not os.path.exists(os.path.join(DB, PAGES[src])): bad.append("%#x page %s missing" % (f["off"], src))
            else: n_pages.add(src)
        if f["status"] == "pad":
            m = re.search(r"const=(0x[0-9A-Fa-f]+)", f["meaning"]); cv = int(m.group(1), 16) if m else 0
            for b in range(f["off"], f["off"] + f["width"]):
                vs = set(r[b] for r in recs)
                if vs != {cv}: bad.append("pad %#x not constant %#x: %s" % (b, cv, sorted(vs)[:4]))
        for tok in f["readers"]:
            pr = parse_reader(tok, f)
            if pr is None: bad.append("reader token %s" % tok); continue
            ok, txt = reader_ok(*pr); n_readers += 1
            if not ok: bad.append("reader %s (%s)" % (tok, txt))
    check("%-17s manifest rows consistent with the pack and the image" % name, not bad, "; ".join(bad[:6]))
    pg = sum(1 for b in range(size) if owner[b] and owner[b]["status"] == "page")
    ps = sum(1 for b in range(size) if owner[b] and owner[b]["status"] == "pass")
    pd = sum(1 for b in range(size) if owner[b] and owner[b]["status"] == "pad")
    pd_page = sum(1 for b in range(size) if owner[b] and owner[b]["status"] == "pad" and owner[b]["source"] != "PASS")
    res = [b for b in range(size) if owner[b] is None or owner[b]["status"] == "shape"]
    census.append((name, slot, doff, HDR[name]["count"], size, pg, ps, pd, pd_page, res))
    residue += [(name, b) for b in res]
print("  reader instructions decoded: %d; pages cited: %d" % (n_readers, len(n_pages)))

print("coverage (bytes of one record):")
print("  %-17s %-9s %-6s %-11s %5s %5s %5s %5s  %s" % ("table", "slot", "dir", "shape", "page", "pass", "pad", "resid", "residue offsets"))
for name, slot, doff, cnt, size, pg, ps, pd, pdp, res in census:
    print("  %-17s %08X +%#04x %4d x %-4d %5d %5d %5d %5d  %s" % (name, slot, doff, cnt, size, pg, ps, pd, len(res),
          ",".join("%#04x" % b for b in res) or "-"))
for s, why in NON_PACK:
    print("  %-17s %s  not a battle_pack entry (%s) - not measured here" % ("-", s, why))
full_page = [c[0] for c in census if c[5] + c[8] == c[4]]
tabs = sorted(set(t for t, b in residue), key=lambda t: [x[0] for x in TABLES].index(t))
print("tables fully mapped by existing pages (page + page-declared pads): %d: %s" % (len(full_page), ", ".join(full_page)))
print("tables fully mapped after this pass: %d of %d" % (sum(1 for c in census if not c[9]), len(census)))
print("residue: %d tables, %d unmapped bytes, named: %s" % (len(tabs), len(residue),
      "; ".join("%s %s" % (t, ",".join("%#04x" % b for tt, b in residue if tt == t)) for t in tabs)))

if "--write-coverage" in sys.argv:
    path = sys.argv[sys.argv.index("--write-coverage") + 1]
    with open(path, "w", encoding="utf-8", newline="\n") as w:
        w.write("table\tslot\tpack_dir\tshape\tcovering_pages\tbytes_mapped_by_pages\tbytes_mapped_after_pass\trecord_size\tresidue_bytes\tneeds_map\n")
        for name, slot, doff, cnt, size, pg, ps, pd, pdp, res in census:
            pages = sorted(set(PAGES[f["source"]] for f in ROWS[name] if f["source"] != "PASS" and f["status"] in ("page", "pad")))
            w.write("%s\t%08X\t+%#04x\t%d x %d\t%s\t%d\t%d\t%d\t%s\t%s\n" % (name, slot, doff, cnt, size, "; ".join(pages) or "-",
                    pg + pdp, size - len(res), size, ",".join("%#04x" % b for b in res) or "-", "no" if pg + pdp == size else "yes"))
    print("wrote", path)

print("FAILS: %d%s" % (len(FAILS), (" - " + "; ".join(FAILS)) if FAILS else ""))
sys.exit(1 if FAILS else 0)
