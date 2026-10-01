"""FE-4: the routes the BattleStatsRecord field scan did not follow, run; the surviving gap bytes classified (OPUS, 2026-09-27).

The bytes left unaccounted: +0x22..+0x23, +0x4F, +0x5C..+0x63 (with the stale +0x05C row struck, R6), +0xBB, +0x1C6..+0x1C7. Each route is followed linearly with
register copies; each carries a positive control (a known field it must reach) so silence is not a blind engine.
  R1 THE ACCESSOR: all call sites of BattleStats_GetByBattleSlotIndex 00320A40, rax followed, callees 2 deep
  R2 THE INLINE ARRAY FORM *(02EBF190) + 8 + k*0x1C8: every imul-by-0x1C8 in the functions that load the pool (46 / 54)
  R3 THE STORED POINTER: every image-wide qword load at +0x698 (the battle unit's stats pointer; over-inclusive)
  R4 LAYOUT: +0x22..+0x23 sit between a u8 (+0x20) and an int32 (+0x24), +0x4F between a u8 (+0x4E) and a u16 array
     (+0x50), +0xBB is GambitConfig's tail (its u8 filledCount +0x32 = record +0xBA, type size 0x34, then the u32 array
     at +0xBC), +0x1C6..+0x1C7 between the last u8 (+0x1C5) and the 0x1C8 end - all four are what natural alignment
     inserts; +0x5C..+0x63 - 8 bytes after the u16 at +0x5A, before the u32 at +0x64, +0x5C already 4-aligned - is not
  R5 REGRESSION (rejects the store's 'tailSentinelWord u16 at +0x1C3, no runtime reader'): +0x1C3 and +0x1C4 are
     separate bytes with runtime byte writers (00323772, 00323722) and +0x1C5 has three (00323729, 00323779, 00324341);
     only the initialiser's 0xFFFF word store (0023ACD5) covers +0x1C3..+0x1C4 at once. The store rows must be u8.
  R6 REGRESSION (rejects the store's stats field 'slotCounter5C' at +0x05C): its three accesses address the RESULT record
     at +0x5C + 4i (FE-3; FABLE's FE-4 record routes the store row here)
Not claimed: dynamic reach (a linear static follow); what +0x5C..+0x63 was for.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_REG, CS_OP_MEM, CS_OP_IMM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
_c = {}
def D(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + sizes.get(f, 0x200)], f))
    return _c[f]
M = {"eax": "rax", "ax": "rax", "al": "rax", "ebx": "rbx", "bx": "rbx", "bl": "rbx", "ecx": "rcx", "cx": "rcx", "cl": "rcx",
     "edx": "rdx", "dx": "rdx", "dl": "rdx", "esi": "rsi", "si": "rsi", "sil": "rsi", "edi": "rdi", "di": "rdi", "dil": "rdi",
     "ebp": "rbp", "bp": "rbp", "bpl": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
GAPS = {0x22, 0x23, 0x4F, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63, 0xBB, 0x1C6, 0x1C7}
KNOWN = {0x24, 0x48, 0x1C2}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

def follow(body, i0, regs, depth, sink, seen, n_ins=60, bias=0):
    regs = set(regs)
    for y in body[i0:i0 + n_ins]:
        for op in y.operands:
            if op.type == CS_OP_MEM and op.mem.base and y.mnemonic != "lea" and fam(y.reg_name(op.mem.base)) in regs and op.mem.index == 0:
                sink.append((op.mem.disp - bias, max(op.size, 1), y.address))
        if y.mnemonic == "call":
            if depth and y.operands and y.operands[0].type == CS_OP_IMM:
                t = y.operands[0].imm; carried = tuple(r for r in ("rcx", "rdx", "r8", "r9") if r in regs)
                if carried and t in sizes and (t, carried) not in seen:
                    seen.add((t, carried)); follow(D(t), 0, carried, depth - 1, sink, seen)
            regs -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
        elif y.mnemonic in ("mov", "lea") and len(y.operands) == 2 and y.operands[0].type == CS_OP_REG and y.operands[1].type == CS_OP_REG:
            s, t = fam(y.reg_name(y.operands[1].reg)), fam(y.reg_name(y.operands[0].reg))
            if s in regs: regs.add(t)
            else: regs.discard(t)
        elif y.operands and y.operands[0].type == CS_OP_REG and y.mnemonic not in ("cmp", "test", "push"):
            regs.discard(fam(y.reg_name(y.operands[0].reg)))
        if not regs or y.mnemonic == "ret": break
def touched(sink, keyset): return sorted({k for disp, w, a in sink for k in range(disp, disp + w) if k in keyset})
def exec_scan(pred):
    for ch, vs, va, rs, ro in SECS:
        if ch & 0x20000000:
            for p in range(ro, ro + rs - 5):
                r = pred(BASE + va + p - ro, p)
                if r: yield r
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None

# R1
sink = []; seen = set(); sites = 0
for v in exec_scan(lambda v, p: v if d[p] == 0xE8 and v + 5 + struct.unpack_from("<i", d, p + 1)[0] == 0x320A40 else None):
    f = owner(v)
    if f is None: continue
    b = D(f); i = next((k for k, x in enumerate(b) if x.address == v), None)
    if i is not None: sites += 1; follow(b, i + 1, {"rax"}, 2, sink, seen)
check("R1 the accessor route (%d call sites) reaches known fields and no gap byte" % sites,
      sites >= 20 and touched(sink, KNOWN) and not touched(sink, GAPS), "known %s gaps %s" % (touched(sink, KNOWN), touched(sink, GAPS)))

# R2
POOL = 0x2EBF190
pf = {owner(v) for v in exec_scan(lambda v, p: v if v + 4 + struct.unpack_from("<i", d, p)[0] == POOL else None)} - {None}
sink2 = []; forms = 0; ffs = set(); seen2 = set()
for f in pf:
    b = D(f)
    for i, x in enumerate(b):
        if x.mnemonic == "imul" and x.op_str.endswith(", 0x1c8"):
            forms += 1; ffs.add(f); regs = {fam(x.op_str.split(",")[0])}
            # does this form add the +8 itself (lea r, [pool + 8] / add r, 8 around the imul)? then displacements are
            # record offsets as written; only a form without it can carry the +8 inside the displacement
            win = b[max(0, i - 6):i + 6]
            biases = (0,) if any(re.search(r"\+ 8\]$", z.op_str) and z.mnemonic == "lea" or (z.mnemonic == "add" and z.op_str.endswith(", 8")) for z in win) else (0, 8)
            for y in b[i + 1:i + 40]:
                if y.mnemonic == "add" and len(y.operands) == 2 and y.operands[0].type == CS_OP_REG and y.operands[1].type == CS_OP_REG \
                   and (fam(y.reg_name(y.operands[1].reg)) in regs or fam(y.reg_name(y.operands[0].reg)) in regs):
                    # the add that completes pool + 8 + k*0x1C8: follow the finished record pointer, callees 2 deep
                    dst = fam(y.reg_name(y.operands[0].reg)); regs.add(dst)
                    follow(b, b.index(y) + 1, {dst}, 2, sink2, seen2)
                for op in y.operands:
                    if op.type == CS_OP_MEM and y.mnemonic != "lea":
                        bs = fam(y.reg_name(op.mem.base)) if op.mem.base else None
                        ix = fam(y.reg_name(op.mem.index)) if op.mem.index else None
                        if (bs in regs or ix in regs) and bs != "rip":
                            for bias in biases:     # the +8 inside the displacement only when the form did not add it
                                sink2.append((op.mem.disp - bias, max(op.size, 1), y.address))
                if y.mnemonic in ("call", "ret"): break
# +0xBB is CARRIED, not accessed, by exactly one site: 00327BE0 copies a whole GambitConfig out of the record - movups
# from +0x88 / +0x98 / +0xA8 and a dword from +0xB8 (00327C22): 3 x 16 + 4 = 0x34 bytes, the type's size with its tail.
cp = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x327BE0)}
whole_copy = (cp.get(0x327BFF) == "movups xmm0, xmmword ptr [r8 + 0x88]" and cp.get(0x327C0A) == "movups xmm1, xmmword ptr [r8 + 0x98]"
              and cp.get(0x327C16) == "movups xmm0, xmmword ptr [r8 + 0xa8]" and cp.get(0x327C22) == "mov eax, dword ptr [r8 + 0xb8]")
gap2 = sorted({k for disp, w, a in sink2 for k in range(disp, disp + w) if k in GAPS and not (a == 0x327C22 and k == 0xBB)})
check("R2 the inline array form (%d functions, %d forms) reaches known fields and no gap byte (+0xBB only inside the"
      " whole-GambitConfig copy 00327BE0)" % (len(ffs), forms),
      len(ffs) >= 40 and touched(sink2, KNOWN) and not gap2 and whole_copy, "known %s gaps %s" % (touched(sink2, KNOWN), gap2))

# R3
sink3 = []; loads = 0
for f, sz in sizes.items():
    o = off(f)
    if o is None or sz <= 0 or sz > 40000 or b"\x98\x06\x00\x00" not in d[o:o + sz]: continue
    b = D(f)
    for i, x in enumerate(b):
        if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[0].type == CS_OP_REG and x.operands[1].type == CS_OP_MEM \
           and x.operands[1].mem.disp == 0x698 and x.operands[1].size == 8:
            loads += 1; follow(b, i + 1, {fam(x.reg_name(x.operands[0].reg))}, 0, sink3, set())
check("R3 the stored-pointer route (%d qword loads at +0x698) reaches known fields and no gap byte" % loads,
      loads >= 500 and touched(sink3, KNOWN) and not touched(sink3, GAPS), "known %s gaps %s" % (touched(sink3, KNOWN), touched(sink3, GAPS)))

rows = {}; gc = {}
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "BattleStatsRecord":
        rows[int(c[1], 16)] = c
    if c[0] == "GambitConfig":
        gc[int(c[1], 16)] = c
def w(o): return int(rows[o][2]) if o in rows else None
check("R4 layout: four gaps are what alignment inserts; +0x5C..+0x63 (8 B after the u16 at +0x5A, before the u32 at +0x64) is not",
      w(0x20) == 1 and rows[0x24][4] == "int32" and w(0x4E) == 1 and rows[0x50][4].startswith("uint16")
      and w(0x5A) == 2 and w(0x5C) == 8 and rows[0x5C][6] == "DISCOVERED" and w(0x64) == 4 and 0x5C % 4 == 0
      and w(0x1C5) == 1 and 0x1C8 % 4 == 0
      and gc[0x32][3] == "filledCount" and int(gc[0x32][2]) == 1 and int(gc[0x33][2]) == 1 and 0x88 + 0x32 == 0xBA
      and rows[0xBC][4].startswith("uint32"))

def ins_at(a):
    f = owner(a); x = next((x for x in D(f) if x.address == a), None) if f else None
    return "%s %s" % (x.mnemonic, x.op_str) if x else ""
check("R5 REGRESSION: +0x1C3 / +0x1C4 / +0x1C5 are byte fields with runtime writers; the store rows are u8",
      ins_at(0x323772).startswith("mov byte ptr") and "+ 0x1c3]" in ins_at(0x323772)
      and ins_at(0x323722).startswith("mov byte ptr") and "+ 0x1c4]" in ins_at(0x323722)
      and all("+ 0x1c5]" in ins_at(a) and "byte ptr" in ins_at(a) for a in (0x323729, 0x323779, 0x324341))
      and ins_at(0x23ACD5).startswith("mov word ptr") and "+ 0x1c3]" in ins_at(0x23ACD5)
      and all(o in rows and rows[o][2] == "1" and rows[o][4] in ("uint8", "u8") for o in (0x1C3, 0x1C4, 0x1C5)),
      str({o: (rows[o][2], rows[o][4]) if o in rows else None for o in (0x1C3, 0x1C4, 0x1C5)}))
B = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x386C70)}
check("R6 REGRESSION (rejects the store's 'slotCounter5C' stats field): 00386E43 / 00386E56 / 00386EEC are [r14 + r12 - 0x60]"
      " with r14 = stats + 0xBC + 4i and r12 = result - stats, i.e. result + 0x5C + 4i; the store declares no stats field there",
      all(B.get(a, "").endswith("ptr [r14 + r12 - 0x60], eax") or B.get(a, "") == "cmp dword ptr [r14 + r12 - 0x60], 1" for a in (0x386E43, 0x386E56, 0x386EEC))
      and B.get(0x386C90) == "lea r14, [rcx + 0xbc]" and B.get(0x386CA6) == "mov rsi, rcx" and B.get(0x386CBE) == "mov r12, rdx"
      and B.get(0x386CC6) == "sub r12, rsi" and rows.get(0x5C, [None] * 7)[3] != "slotCounter5C")
print("FAILS", fails)
sys.exit(1 if fails else 0)
