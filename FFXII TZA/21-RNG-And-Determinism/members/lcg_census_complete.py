"""lcg_census_complete.py - AD-2: is the shared gameplay LCG's consumer census complete? (FABLE, Claude Opus 5.5, 2026-09-26)

The page gives the consumers as two populations. The eight functions that write the recurrence (seven inliners plus the
generator 00328370), together with the reseed 00328D80, are the nine functions of shared-gameplay-lcg-state-accesses.tsv.
The fifteen functions that call the generator (23 sites, from the raw call index) are the other population. This
sweep covers what those two censuses could miss, over the WHOLE .text section, listed bodies or not.
  L1 every rip-relative operand whose target lies in the state dword 022C256C..022C256F, at any width and any mnemonic
     (lea included), is found by a raw disp32 sweep of .text. Each candidate is confirmed by decoding the containing
     listed body. The set is exactly the TSV's sites.
  L1b the base-plus-displacement blind spot is bounded. No data word points into the state's 0x100-byte neighbourhood,
     and the one lea to a base below it (0030D698, 0xAC below) belongs to a four-qword pointer array, read and sized.
  L2 every rel32 branch into the generator 00328370 - E8 call, E9 jmp, 0F 8x jcc - is found by a raw sweep and
     confirmed at an instruction boundary. They are 23 calls in 15 functions, with no jmp and no jcc.
  L3 nothing takes the generator's address. No rip-relative lea/mov forms 00328370, and no 8-byte absolute 0x00328370
     sits in .rdata or .data, so no indirect call can reach it.
  L4 control: the multiplier 0x41C64E6D sits at exactly 24 instruction sites in the eight writer functions, the page's
     published figure, reproduced by the same decoder.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = {struct.unpack_from("<8s", d, pe + 24 + optsz + i * 40)[0].rstrip(b"\0").decode():
        struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)}
def off(v):
    for vs, va, rs, ro in secs.values():
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
starts = sorted(F)
import bisect
def owner(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 and a < starts[i] + F[starts[i]] else None
def insn_at(a):
    f = owner(a)
    if f is None: return None, None
    for x in cs.disasm(d[off(f):off(f) + F[f]], f):
        if x.address == a: return f, x
        if x.address > a: break
    return f, None
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
vs, va, rs, ro = secs[".text"]; T0 = BASE + va; text = d[ro:ro + rs]
STATE, GEN = 0x022C256C, 0x00328370
# L1: raw disp32 sweep - an operand ending at i+4 may be followed by 0, 1, 2 or 4 immediate bytes
cand = set()
for i in range(0, len(text) - 4):
    disp = int.from_bytes(text[i:i + 4], "little", signed=True)
    for imm in (0, 1, 2, 4):
        t = T0 + i + 4 + imm + disp
        if STATE <= t < STATE + 4: cand.add(T0 + i)
sites = set()
for c in cand:
    for back in range(1, 12):   # the instruction starts a few bytes before its disp32
        f, x = insn_at(c - back)
        if x is not None and x.address + x.size > c and any(
                op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" and STATE <= x.address + x.size + op.mem.disp < STATE + 4
                for op in x.operands):
            sites.add((f, x.address, "%s %s" % (x.mnemonic, x.op_str))); break
tsv = [r for r in csv.DictReader(open(HERE.parent / "shared-gameplay-lcg-state-accesses.tsv", encoding="utf-8"), delimiter="\t")]
tsv_sites = {int(r["site"], 16) for r in tsv}
check("L1 every operand into 022C256C..F is a TSV site", {s[1] for s in sites} == tsv_sites,
      "%d found, %d in TSV; extra %s" % (len(sites), len(tsv_sites), sorted("%08X %s" % (s[1], s[2]) for s in sites if s[1] not in tsv_sites)))
# L1b: the base-plus-displacement blind spot - a pointer to the state held in data, or a lea to a base just below it
ptrs = []
for nm in (".rdata", ".data"):
    _, sva, srs, sro = secs[nm]
    blob = d[sro:sro + srs]
    for w, fmt in ((8, "<Q"), (4, "<I")):
        for k in range(0, len(blob) - w + 1, 4):
            v = struct.unpack_from(fmt, blob, k)[0]
            if STATE - 0x100 <= v < STATE + 4: ptrs.append("%s+%X=%X" % (nm, k, v))
leas = set()
for i in range(0, len(text) - 4):
    disp = int.from_bytes(text[i:i + 4], "little", signed=True)
    t = T0 + i + 4 + disp
    if STATE - 0x100 <= t < STATE:
        f, x = insn_at(T0 + i - 3)
        if x is not None and x.mnemonic == "lea" and x.address + x.size == T0 + i + 4: leas.add("%08X %s" % (x.address, x.op_str))
# The one lea found, 0030D698 lea rbp, [022C24C0], forms a base 0xAC below the state. It is read here instead of excused:
# FUN_0030D600 fills at most four qwords through it (the selection loop is bounded by cmp esi, 4 at 0030D690; the only
# store is 0030D6DD mov qword ptr [rdi], rcx with add rdi, 8) and publishes the base with that count, so the object is
# 0x20 bytes and ends 0x8C below the state.
Xd = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x30D600):off(0x30D600) + F[0x30D600]], 0x30D600)}
arr4 = (Xd.get(0x30D690) == "cmp esi, 4" and Xd.get(0x30D6DD) == "mov qword ptr [rdi], rcx" and Xd.get(0x30D6E0) == "add rdi, 8"
        and Xd.get(0x30D6A7) == "mov rdi, rbp" and sum(1 for v in Xd.values() if v.startswith("mov") and "[rdi" in v.split(",")[0]) == 1)
check("L1b no data pointer into the state's 0x100-byte neighbourhood; the one lea below it is a 4-qword array",
      ptrs == [] and leas == {"0030D698 rbp, [rip + 0x1fb4e21]"} and arr4, "ptrs %s leas %s array-of-4 %s" % (ptrs[:4], sorted(leas)[:4], arr4))
# L2: raw rel32 branches into the generator
br = collections.Counter(); fn = set(); bad = []
for i in range(0, len(text) - 6):
    b0 = text[i]
    for opl, kind in (((1, "call") if b0 == 0xE8 else (1, "jmp") if b0 == 0xE9 else (2, "jcc") if b0 == 0x0F and 0x80 <= text[i + 1] <= 0x8F else (0, None)),):
        if not kind: continue
        t = T0 + i + opl + 4 + int.from_bytes(text[i + opl:i + opl + 4], "little", signed=True)
        if t == GEN:
            f, x = insn_at(T0 + i)
            if x is None: bad.append("%08X" % (T0 + i)); continue
            br[kind] += 1; fn.add(f)
check("L2 rel32 branches into 00328370: 23 calls in 15 functions, no jmp, no jcc",
      dict(br) == {"call": 23} and len(fn) == 15, "%s in %d functions; non-boundary hits %s" % (dict(br), len(fn), bad[:5]))
# L3: address-taking
lea = []
for c in range(0, len(text) - 4):
    disp = int.from_bytes(text[c:c + 4], "little", signed=True)
    if T0 + c + 4 + disp == GEN:
        f, x = None, None
        for back in range(1, 8):
            f, x = insn_at(T0 + c - back)
            if x is not None and x.address + x.size == T0 + c + 4: break
            x = None
        if x is not None and x.mnemonic in ("lea", "mov"): lea.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
absq = []
for nm in (".rdata", ".data"):
    _, sva, srs, sro = secs[nm]
    blob = d[sro:sro + srs]; k = blob.find(struct.pack("<Q", GEN))
    while k != -1:
        absq.append("%s+%X" % (nm, k)); k = blob.find(struct.pack("<Q", GEN), k + 1)
check("L3 nothing takes 00328370's address (no rip lea/mov, no absolute qword)", lea == [] and absq == [], "%s %s" % (lea, absq))
# L4 control
mul = 0; mulf = set()
for f in {int(r["function"], 16) for r in tsv}:
    for x in cs.disasm(d[off(f):off(f) + F[f]], f):
        if any(op.type == X86_OP_IMM and (op.imm & 0xFFFFFFFF) == 0x41C64E6D for op in x.operands): mul += 1; mulf.add(f)
check("L4 control: 24 multiplier sites in the eight writer functions", mul == 24 and len(mulf) == 8, "%d sites in %d functions" % (mul, len(mulf)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
