"""ag2_slot_identity.py - AG-2: an identity for every one of the registry's 64 slots (FABLE, Claude Opus 5.5, 2026-09-26).

The 2026-09-22 band-shape ruling left AG-2 with a stated next step: "name the battle_pack.bin directory fields in offset
order". The two halves of that join were already published and had not been put together:
  - the STATIC binder 00236C30 pairs each directory field with a slot (the row-lookup contract's section 7a);
  - UQ-73 (2026-09-15): battle_pack.bin opens {u32 count = 71; u32 offset[71]} and manifest slot k is pack entry k, at
    directory +4 + 4k. The manifest is the image's own path array at 01E4D830.
This script decodes the binder from the image, joins field -> k -> manifest file, and adds the page's already-read
identities for the 22 slots no directory field reaches, so each of the 64 grid positions gets exactly one row.
  C1 the binder yields 42 (field, slot) pairs with distinct fields and slots, by four routes: the registrar
     (003845F0 / 003846F0, lea + movsxd), bespoke binders called with the field in ecx, and two direct stores.
  C2 control: the registrar pairs reproduce the contract's section 7a (35 rows) exactly.
  C3 every bespoke binder's own body takes the slot this script assigns it (lea or store into the band).
  C4 every field lands inside the pack's 71-entry directory, in all nine language packs of the extract.
  C5 semantic controls, eleven names the database gave these slots from their CONSUMERS, not from this join:
     0x180 weapon-class map = WepJob_Matrix; 0x130 party definition = chr_data; 0x138 action definitions = action_data;
     0x118 status definitions = status_data; 0x0F8 equipment = eitm_data; 0x158 shop table = shop_data;
     0x0D8 gambit target definitions = targetchip_data; 0x200 = license_board (UQ-73's +0x11C); 0x0B8 MP gain by HP
     damage = damagemp_data; 0x0C0 loot = drop; 0x170 text banks = word.bin.
  C6 the five area slots are the ones BattleData_SetAreaArdSectionCategory (0023A160) addresses, and the twelve
     board-request words are the rep-stosq run from 02EBF1A0 with ecx = 12 (002369E5).
  C7 coverage: 42 + 5 + 12 + 5 others = 64 rows, one per grid position 02EBF008 .. 02EBF200, none twice.
Also: the page's section 2 note (2026-09-22) cites 00236C74 as the store to 02EBF008 from +4. The bytes store to
02EBF180; 02EBF008 is bound from +0x118 at 00237010 (checked below as C8, because the page must be corrected).
Writes ag2-slot-identity.tsv beside itself. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
def body(a): return list(cs.disasm(d[off(a):off(a) + F[a]], a))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
LO, HI = 0x02EBF008, 0x02EBF200
def rip(x, op): return x.address + x.size + op.mem.disp
def band_targets(x):
    return [rip(x, op) for op in x.operands if op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" and LO <= rip(x, op) <= HI]
REG = {0x3845F0, 0x3846F0}
# ---- C1: decode the binder
L = body(0x236C30)
pairs = {}      # slot -> (field, route, site)
lea = fld = None
for i, x in enumerate(L):
    ops = x.operands
    if x.mnemonic == "lea" and band_targets(x): lea = band_targets(x)[0]
    if x.mnemonic in ("movsxd", "mov") and len(ops) == 2 and ops[1].type == X86_OP_MEM and cs.reg_name(ops[1].mem.base) != "rip":
        fld = ops[1].mem.disp
    if x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and band_targets(x):
        pairs[band_targets(x)[0]] = (fld, "direct store", x.address)
    if x.mnemonic == "call" and ops[0].type == X86_OP_IMM:
        t = ops[0].imm
        if t in REG: pairs[lea] = (fld, "registrar %08X" % t, x.address); lea = None
        elif t in F and L[i - 1].mnemonic == "mov" and cs.reg_name(L[i - 1].operands[0].reg) == "ecx":
            pairs[("binder", t)] = (L[i - 1].operands[1].mem.disp, "binder %08X" % t, x.address)
# resolve each bespoke binder to the band slot its own body addresses (C3)
bespoke = {}
for key in [k for k in pairs if isinstance(k, tuple)]:
    t = key[1]; ts = sorted({a for x in body(t) for a in band_targets(x)})
    bespoke[t] = ts
    fld, route, site = pairs.pop(key)
    if len(ts) == 1: pairs[ts[0]] = (fld, route, site)
fields = [v[0] for v in pairs.values()]
check("C1 42 (field, slot) pairs, distinct fields and slots", len(pairs) == 42 and len(set(fields)) == 42,
      "%d pairs, %d distinct fields" % (len(pairs), len(set(fields))))
# ---- C2: the contract's section 7a
SEC7A = {0xC: 0x2EBF018, 0x10: 0x2EBF0B8, 0x14: 0x2EBF0A8, 0x18: 0x2EBF0B0, 0x1C: 0x2EBF0C0, 0x24: 0x2EBF0E0, 0x28: 0x2EBF108,
         0x2C: 0x2EBF160, 0x30: 0x2EBF110, 0x34: 0x2EBF038, 0x44: 0x2EBF130, 0x48: 0x2EBF128, 0x4C: 0x2EBF100, 0x6C: 0x2EBF0C8,
         0x70: 0x2EBF020, 0x74: 0x2EBF060, 0x78: 0x2EBF0F0, 0x7C: 0x2EBF0E8, 0x80: 0x2EBF0A0, 0x84: 0x2EBF098, 0x88: 0x2EBF090,
         0x8C: 0x2EBF088, 0x90: 0x2EBF080, 0x94: 0x2EBF078, 0x98: 0x2EBF070, 0x9C: 0x2EBF068, 0xA8: 0x2EBF050, 0xAC: 0x2EBF048,
         0xE8: 0x2EBF058, 0xEC: 0x2EBF040, 0xF4: 0x2EBF030, 0xF0: 0x2EBF028, 0xF8: 0x2EBF170, 0x114: 0x2EBF010, 0x118: 0x2EBF008}
reg = {v[0]: s for s, v in pairs.items() if v[1].startswith("registrar")}
check("C2 control: the registrar pairs are the contract's section 7a, row for row", reg == SEC7A, "%d rows" % len(reg))
check("C3 each bespoke binder addresses exactly one band slot", all(len(v) == 1 for v in bespoke.values()),
      "; ".join("%08X->%s" % (t, ",".join("%08X" % a for a in v)) for t, v in sorted(bespoke.items())))
# ---- C4: manifest names and the pack directory
def manifest(k):
    p = struct.unpack_from("<Q", d, off(0x01E4D830 + 8 * k))[0]
    return d[off(p):off(p) + 200].split(b"\0")[0].decode().rsplit("\\", 1)[-1] if p else None
EX = Path("D:/FFXII_TZA_extract")
packs = sorted(EX.rglob("battle_pack.bin")) if EX.exists() else []
dirs = []
for p in packs:
    b = p.read_bytes(); c = struct.unpack_from("<I", b, 0)[0]
    dirs.append((p, c, struct.unpack_from("<%dI" % c, b, 4), len(b)))
ks = {s: (v[0] - 4) // 4 for s, v in pairs.items()}
check("C4 every field is a directory entry (+4 + 4k, k < 71) in all nine packs",
      len(dirs) >= 9 and all(c == 71 for _, c, _, _ in dirs) and all((v[0] - 4) % 4 == 0 and 0 <= ks[s] < 71 for s, v in pairs.items()),
      "%d packs" % len(dirs))
def length(k, o, size):   # an entry's length is the distance to the next entry's offset (UQ-73), or to the file end
    nxt = [x for x in o[k + 1:] if x > o[k]]
    return (nxt[0] - o[k]) if nxt else size - o[k]
check("C4b every one of the 42 entries is non-empty in all nine packs",
      all(length(ks[s], o, z) > 0 for s in pairs for _, _, o, z in dirs))
# ---- C5: semantic controls from consumer-side names
CTRL = {0x2EBF180: "WepJob_Matrix.bin", 0x2EBF130: "chr_data.bin", 0x2EBF138: "action_data.bin", 0x2EBF118: "status_data.bin",
        0x2EBF0F8: "eitm_data.bin", 0x2EBF158: "shop_data.bin", 0x2EBF0D8: "targetchip_data.bin", 0x2EBF200: "license_board.bin",
        # three more from the page's 2026-09-07 named-reader census: MP gain by HP damage, the loot table, the text banks
        0x2EBF0B8: "damagemp_data.bin", 0x2EBF0C0: "drop.bin", 0x2EBF170: "word.bin"}
got = {s: manifest(ks[s]) for s in CTRL if s in ks}
check("C5 eleven consumer-side names agree with the join", got == CTRL,
      str({"%08X" % s: v for s, v in got.items() if CTRL.get(s) != v}))
# ---- C6: the area slots and the board words
ard = sorted({a for x in body(0x23A160) for a in band_targets(x)})
# decoded from BattleStorage_InitializeWorkArrays' own entry, so the window is on instruction boundaries
W = [x for x in body(0x2368D0) if 0x2369E5 <= x.address <= 0x236A01]
stos = [x.address for x in W if x.mnemonic.startswith("rep stos")]
lea1a0 = W[0].mnemonic == "lea" and band_targets(W[0]) == [0x2EBF1A0] and W[0].op_str.startswith("rdi")
ecx12 = any(x.mnemonic == "mov" and x.op_str == "ecx, 0xc" for x in W)
check("C6 area slots from 0023A160, and the 12-word board run zeroed at 002369E5",
      ard == [0x2EBF120, 0x2EBF140, 0x2EBF148, 0x2EBF150, 0x2EBF168] and bool(stos) and lea1a0 and ecx12,
      "ard %s stos %s" % (["%08X" % a for a in ard], ["%08X" % a for a in stos]))
# ---- the 22 slots no directory field reaches: identities already read on the registry page
OTHER = {
 0x2EBF150: ("area .ard section, category 0", "BattleData_SetAreaArdSectionCategory", "stats-side; rebound on every area change, null when the area ships no .ard (AG-11)"),
 0x2EBF168: ("area .ard section, category 1", "BattleData_SetAreaArdSectionCategory", "the gambit order-set section; the one category bound through 003846F0"),
 0x2EBF120: ("area .ard section, category 2", "BattleData_SetAreaArdSectionCategory", "stats-side; as category 0"),
 0x2EBF148: ("area .ard section, category 3", "BattleData_SetAreaArdSectionCategory", "stats-side; as category 0"),
 0x2EBF140: ("area .ard section, category 4", "BattleData_SetAreaArdSectionCategory", "stats-side; as category 0"),
 0x2EBF178: ("runtime-published buffer pointer", "main-loop builder (tail read)", "not a table; the 301-entry blob; its reader is FZ-8"),
 0x2EBF188: ("write-only state sink", "93 stores in 40 functions", "nothing loads it (upper-sixteen table)"),
 0x2EBF190: ("BattleSystemState pointer", "runtime", "the 0x7410-byte block; runtime stats, not an authored table (section 8b, corrected 2026-09-13)"),
 0x2EBF198: ("unnamed initialised element", "none", "reached only as index -1 of the board array (AG-4)"),
 0x2EBF0D0: ("encoded-id class 12 descriptor, never installed", "none", "no lea and no store in the image; class 12 is permanently empty (band ruling item 7)"),
}
for k in range(12):
    OTHER[0x2EBF1A0 + 8 * k] = ("board_%d.bin request slot" % (k + 1), "setter %08X" % (0x238390 + 0x30 * k),
                                "loader id 0x%X; at most six resident (tail read, M-7); whether it holds the completion word or a grid "
                                "pointer is the upper-sixteen section's recorded tension" % (0x47 + k))
rows = []
for s in range(LO, HI + 1, 8):
    if s in pairs:
        fld, route, site = pairs[s]; k = ks[s]
        lens = sorted({length(k, o, z) for _, _, o, z in dirs})
        rows.append(["%08X" % s, (s - LO) // 8, "battle_pack directory +0x%X" % fld, route, "%08X" % site, k, manifest(k),
                     "entry empty in some pack" if min(lens) <= 0 else "non-empty in all nine packs", ""])
    elif s in OTHER:
        kind, who, note = OTHER[s]
        rows.append(["%08X" % s, (s - LO) // 8, kind, who, "", "", "", "", note])
covered = [r[0] for r in rows]
check("C7 coverage: one row per grid position, 64 rows, none twice",
      len(rows) == 64 and len(set(covered)) == 64 and len(set(pairs) & set(OTHER)) == 0,
      "%d rows (%d directory, %d other)" % (len(rows), len(pairs), len(OTHER)))
# ---- C8: the section-2 citation the page must correct
X = {x.address: x for x in L}
check("C8 00236C74 stores directory +4 to 02EBF180, and 02EBF008 is bound from +0x118 at 00237010",
      band_targets(X[0x236C74]) == [0x2EBF180] and X[0x236C70].op_str == "rax, dword ptr [rcx + 4]"
      and band_targets(X[0x237010]) == [0x2EBF008] and X[0x237017].op_str == "rdx, dword ptr [rax + 0x118]")
with open(HERE / "ag2-slot-identity.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("slot\tindex\tbinding\troute\tsite\tpack_entry\tmanifest_file\tpack_entry_state\tnote\n")
    for r in rows: f.write("\t".join(str(c) for c in r) + "\n")
empty = [r for r in rows if r[7].startswith("entry empty")]
print("directory-bound slots whose pack entry is empty in every pack:", [(r[0], r[6]) for r in empty])
print("FAILS", fails)
sys.exit(1 if fails else 0)
