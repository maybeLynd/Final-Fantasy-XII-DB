"""EH-4 correction: the eight +0x1C request indices the seventeenth pass called engine-unwritten are preset by the
initialiser (OPUS, 2026-09-27). Static.

  C1 00266BD0 has exactly one direct caller, 002665B1, inside ActorStorage_InitializeRecord 00266530, and no conditional
     jump before it leaves the entry path (every jcc in [00266530, 002665B1) lands at or before 002665B1)
  C2 00266BD0 switches on byte[+0x03] & 0x1F through the eight-entry table at 00266C30 and stores one whole-word preset
     to dword [rcx + 0x1C] per row: 0 -> 0, 1-2 -> 0x38, 3-4 -> 0x40, 5-6 -> 0x30004, 7 -> 0x34C85 (decoded here)
  C3 every later access to dword [rbx + 0x1C] in the initialiser is an and / or with an immediate that touches only
     indices 2, 8, 10 and 13, so the presets of the other indices survive initialisation
  R1 REJECTS the seventeenth pass's "0, 4, 5, 6, 7, 14, 16, 17 are read by the engine and never written by it" and
     the census conclusion "bits 0 and 6 have zero producers, script or executable": each of the eight is set by at
     least one preset row (4, 5 by rows 1-2; 6 by rows 3-4; 16, 17 by rows 5-7; 0, 7, 14 by row 7)
  R2 REJECTS the sixteenth / seventeenth passes' "the engine protects two indices it never sets itself": rows 1-2
     preset indices 4 and 5 together
  N1 negative control: index 1 (read by nothing named, set by no literal) is in no preset, so the decoder does not
     return every bit
Not claimed: what any of the eight means, or how often a record is carved with rows 3, 4 or 7.
"""
import struct, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM
from capstone.x86 import X86_REG_RBX, X86_REG_RCX

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

PRESET, INIT, CALL, TABLE = 0x266BD0, 0x266530, 0x2665B1, 0x266C30

# C1 direct callers of the preset function, image-wide
callers = []
for ch, vs, va, rs, ro in SECS:
    if not ch & 0x20000000: continue
    for i in range(ro, ro + rs - 5):
        if d[i] in (0xE8, 0xE9) and BASE + va + (i - ro) + 5 + struct.unpack_from("<i", d, i + 1)[0] == PRESET:
            callers.append(BASE + va + (i - ro))
xs = list(cs.disasm(d[off(INIT):off(INIT) + sizes[INIT]], INIT))
jcc = [x for x in xs if x.address < CALL and x.mnemonic.startswith("j") and x.mnemonic != "jmp"]
check("C1 one caller, on the initialiser's entry path", callers == [CALL] and owner(CALL) == INIT
      and all(x.operands[0].type == CS_OP_IMM and x.operands[0].imm <= CALL for x in jcc),
      "(callers %s, owner %s, %d jcc before the call)" % ([hex(c) for c in callers], hex(owner(CALL) or 0), len(jcc)))

# C2 decode the table and the store each row reaches first
rows = {}
for r in range(8):
    t = BASE + struct.unpack_from("<I", d, off(TABLE) + 4 * r)[0]
    for x in cs.disasm(d[off(t):off(t) + 0x40], t):
        if x.mnemonic == "ret": break
        o = x.operands
        if x.mnemonic == "mov" and o[0].type == CS_OP_MEM and o[0].mem.base == X86_REG_RCX and o[0].mem.disp == 0x1C \
                and o[0].size == 4 and o[1].type == CS_OP_IMM:
            rows[r] = o[1].imm & 0xFFFFFFFF; break
head = [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(PRESET):off(PRESET) + 0x14], PRESET)]
EXPECT = {0: 0, 1: 0x38, 2: 0x38, 3: 0x40, 4: 0x40, 5: 0x30004, 6: 0x30004, 7: 0x34C85}
check("C2 eight rows, one whole-word preset each", rows == EXPECT and ("movzx", "r8d, byte ptr [rcx + 3]") in head
      and ("and", "eax, 0x1f") in head, "(%s)" % ", ".join("%d:%#x" % kv for kv in sorted(rows.items())))

# C3 the initialiser's other +0x1C accesses on the record register
touch = set(); other = []
for x in xs:
    for o in x.operands:
        if o.type == CS_OP_MEM and o.mem.base == X86_REG_RBX and not o.mem.index and 0x1C <= o.mem.disp < 0x20:
            ok = x.mnemonic in ("and", "or") and x.operands[1].type == CS_OP_IMM
            if ok:
                m = (x.operands[1].imm & 0xFFFFFFFF) << (8 * (o.mem.disp - 0x1C))
                touch |= {b for b in range(32) if ((~m if x.mnemonic == "and" else m) >> b) & 1}
            else:
                other.append("%X %s %s" % (x.address, x.mnemonic, x.op_str))
check("C3 later initialiser writes touch only 2, 8, 10, 13", not other and touch == {2, 8, 10, 13},
      "(touched %s%s)" % (sorted(touch), "; other " + "; ".join(other) if other else ""))

EIGHT = [0, 4, 5, 6, 7, 14, 16, 17]
by = {b: [r for r, v in sorted(rows.items()) if v >> b & 1] for b in range(32)}
check("R1 each of the eight is preset by some row", all(by[b] for b in EIGHT),
      "(%s)" % "; ".join("%d <- rows %s" % (b, ",".join(map(str, by[b]))) for b in EIGHT))
check("R2 rows 1-2 preset indices 4 and 5 together", by[4] == by[5] == [1, 2])
check("N1 index 1 is in no preset", by[1] == [])
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
