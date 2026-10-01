"""EH-4 correction: the LOD verbs write the secondary context's +0x13, not the actor storage record's (OPUS, 2026-09-27).
Static.

  L1 002EC680 (verbs 0160 setlod / 040F partysetlod) reloads rcx = [rcx + 0xC0] before its only store,
     mov byte [rcx + 0x13], dl: the byte written is +0x13 of the record's secondary context, not of the record
  L2 002EC6A0 (verb 042A puppetsetlod) has one caller, 0034BF79, which passes the return of 003EB720 - a puppet-table
     entry (qword table at 02B5EA20, index <= 0x1F) plus 0x10, the puppet's embedded context - not an actor record
  L3 both tail-jump to 002E8CE0, whose third caller Actor_RefreshPresentationVisibility passes rbx = [record + 0xC0]
     (loaded at 002E8FE6): the tail's receiver is the context on every route
  L4 the other thirteen verb-backed setters of the eighth pass's sweep (bluralpha 003DDE00, already refused on the page,
     excluded) store through their entry rcx with no reassignment before the store - the receiver error is confined to
     the two LOD setters
  L5 the type store already has it right: SecondaryContextElement +0x013 lodLevel names 002EC680 and 002EC6A0
  R1 REJECTS the fifth pass's '+0x13 IS THE LOD BYTE' of the actor storage record and its two consequences (the
     initialiser's &0x3C masks a LOD value; 0025E2AA's cmp byte [rdi+0x13], 0x80 tests a LOD top bit): no LOD verb
     writes the record's +0x13 (follows from L1-L3)
Not claimed: what the record's +0x13 bits 0 and 1 mean.
"""
import struct, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM, CS_OP_REG
from capstone.x86 import X86_REG_RCX, X86_REG_RIP

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}; names = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2]); names[int(c[0], 16)] = c[1]
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def body(f): return list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
def callers(t):
    out = []
    for ch, vs, va, rs, ro in SECS:
        if not ch & 0x20000000: continue
        for i in range(ro, ro + rs - 5):
            if d[i] in (0xE8, 0xE9) and BASE + va + (i - ro) + 5 + struct.unpack_from("<i", d, i + 1)[0] == t:
                out.append((BASE + va + (i - ro), d[i]))
    return out
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def txt(x): return "%s %s" % (x.mnemonic, x.op_str)

# L1
b = body(0x2EC680)
st = [i for i, x in enumerate(b) if txt(x) == "mov byte ptr [rcx + 0x13], dl"]
ld = [i for i, x in enumerate(b) if txt(x) == "mov rcx, qword ptr [rcx + 0xc0]"]
check("L1 setlod's setter writes [[rcx + 0xC0] + 0x13]", len(st) == 1 and len(ld) == 1 and ld[0] < st[0]
      and not any(x.mnemonic == "mov" and x.operands[0].type == CS_OP_REG and x.operands[0].reg == X86_REG_RCX for x in b[ld[0] + 1:st[0]]),
      "(load %X, store %X)" % (b[ld[0]].address, b[st[0]].address) if st and ld else "")

# L2
cl = callers(0x2EC6A0)
g = body(0x3EB720)
tbl = [x.address + x.size + x.operands[1].mem.disp for x in g if x.mnemonic == "lea" and x.operands[1].mem.base == X86_REG_RIP]
cb = [x for x in body(owner(0x34BF79)) if x.address < 0x34BF79][-4:]
check("L2 puppetsetlod's setter gets puppet-table entry + 0x10", [c for c, k in cl] == [0x34BF79]
      and tbl == [0x2B5EA20] and "cmp ecx, 0x1f" in [txt(x) for x in g] and "add rax, 0x10" in [txt(x) for x in g]
      and [txt(x) for x in cb][-3:] == ["je 0x34bf7e", "mov edx, edi", "mov rcx, rax"]
      and any(txt(x) == "call 0x3eb720" for x in body(owner(0x34BF79))),
      "(callers %s, table %s)" % ([hex(c) for c, k in cl], [hex(t) for t in tbl]))

# L3
t = sorted(c for c, k in callers(0x2E8CE0))
rv = body(0x2E8FD0)
pre = [txt(x) for x in rv if x.address < 0x2E90A4]
check("L3 the shared tail's receivers are the context", t == [0x2E90A4, 0x2EC694, 0x2EC6A8] and owner(0x2E90A4) == 0x2E8FD0
      and "mov rbx, qword ptr [rcx + 0xc0]" in pre and pre[-1] == "mov rcx, rbx"
      and not any(p.startswith("mov rbx,") or p.startswith("lea rbx,") for p in pre[pre.index("mov rbx, qword ptr [rcx + 0xc0]") + 1:]),
      "(callers %s)" % [hex(c) for c in t])

# L4
OTHER = [0x2659A0, 0x269FC0, 0x26A320, 0x26A3A0, 0x26A430, 0x26AD60, 0x26AF30, 0x26B480, 0x26B500, 0x26BA60, 0x26BED0,
         0x2EB030, 0x2EB330]
bad = []
for f in OTHER:
    xs = body(f); FL = {0x08, 0x09, 0x0C, 0x0D, 0x0E, 0x13, 0x14, 0x1C}
    first = next(i for i, x in enumerate(xs) if x.operands and x.operands[0].type == CS_OP_MEM
                 and x.operands[0].mem.base == X86_REG_RCX and x.operands[0].mem.disp in FL and x.mnemonic in ("and", "or", "mov"))
    if any(X86_REG_RCX in x.regs_access()[1] for x in xs[:first]): bad.append("%08X" % f)   # rcx written before the store
check("L4 the other thirteen store through their entry rcx", not bad, "(%s)" % (", ".join(bad) or "13 of 13"))

# L5
row = [l.split("\t") for l in open(ROOT / "Database/FFXII TZA/_types/fields.tsv", encoding="utf-8")
       if l.startswith("SecondaryContextElement\t0x013\t")]
check("L5 the type store names the same writers on the context", len(row) == 1 and row[0][3] == "lodLevel"
      and "002EC680" in row[0][5] and "002EC6A0" in row[0][5])
check("R1 no LOD verb writes the actor storage record's +0x13", fails == 0)
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
