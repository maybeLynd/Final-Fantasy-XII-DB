"""SWE2-AUDIT-SEM: semantic review of FABLE's SD-125 / SD-128 answers (66f4ecd88), re-derived from the certified image.
Capstone and pefile read Tools/work/exe/FFXII_TZA.exe directly; the CFG (bounded jump tables) and the reaching-definition
walk below are this review's own code, not the producer's. A-checks = SD-125, B-checks = SD-128, F-checks = findings this
review adds (they PASS when the finding reproduces). Positive controls are marked CONTROL.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-sd125-128-0930/sd125_128_sem.py"
"""
import bisect, csv, os, struct, sys
import capstone, pefile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 5))  # repo root, not the cwd (OPUS-REQ-AUDITSEM-SEM-REGRESSIONS-UNRUNNABLE-1003, SWE2-AUDIT-SEM 2026-10-03)
DB = os.path.join(ROOT, "Database")
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DB, "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
X86 = capstone.x86
FAILS = []
FT = {int(r["entry"], 16): (int(r["body_bytes"] or 0), r["name"]) for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}
size = {k: v[0] for k, v in FT.items()}
starts = sorted(size)
TEXT = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"][0]
TVA = BASE + TEXT.VirtualAddress
TDATA = TEXT.get_data()


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def u32(va): return struct.unpack("<I", raw(va, 4))[0]
def f32(va): return struct.unpack("<f", raw(va, 4))[0]
def s(i): return f"{i.mnemonic} {i.op_str}"


def body(fn):
    n = size[fn]
    return [i for i in md.disasm(raw(fn, n + 16), fn) if i.address < fn + n]


def ripv(i):
    for op in i.operands:
        if op.type == X86.X86_OP_MEM and op.mem.base == X86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def tgt(i):
    if (i.mnemonic == "call" or i.mnemonic.startswith("j")) and i.operands and i.operands[0].type == X86.X86_OP_IMM:
        return i.operands[0].imm
    return None


def fn_of(a):
    k = bisect.bisect_right(starts, a) - 1
    if k < 0: return None
    f = starts[k]
    return f if a < f + max(size[f], 1) else None


_bnd = {}
def boundaries(f):
    if f not in _bnd:
        _bnd[f] = {i.address for i in body(f)}
    return _bnd[f]


def sweep_disp(disp):
    """every instruction whose (non-rip) memory displacement is disp, decoded back from each occurrence of the disp32
    bytes and kept only when it sits on its owner's instruction boundary (or outside every listed function)."""
    pat = struct.pack("<i", disp); out = {}; p = 0
    while True:
        k = TDATA.find(pat, p)
        if k < 0: break
        p = k + 1
        for back in range(1, 12):
            a = TVA + k - back
            ins = next(md.disasm(TDATA[k - back:k - back + 16], a), None)
            if ins is None or not (ins.address < TVA + k < ins.address + ins.size): continue
            if not any(o.type == X86.X86_OP_MEM and o.mem.disp == disp and o.mem.base != X86.X86_REG_RIP for o in ins.operands): continue
            f = fn_of(a)
            if f is None or a in boundaries(f):
                out[a] = (f, ins)
    return out


# ---- own CFG with bounded jump tables, and reaching definitions -------------------------------------------------------
def jtable(b, k):
    dt = bt = bound = None
    for j in range(k - 1, max(k - 12, -1), -1):
        y = b[j]
        mem = [o for o in y.operands if o.type == X86.X86_OP_MEM]
        if y.mnemonic == "mov" and mem and mem[0].size == 4 and mem[0].mem.scale == 4 and dt is None:
            dt = BASE + mem[0].mem.disp
        elif y.mnemonic == "movzx" and mem and mem[0].size == 1 and mem[0].mem.index != 0 and bt is None:
            bt = BASE + mem[0].mem.disp
        elif y.mnemonic == "cmp" and len(y.operands) == 2 and y.operands[1].type == X86.X86_OP_IMM:
            bound = y.operands[1].imm
            break
    if dt is None or bound is None: return None
    n = (max(raw(bt, bound + 1)) + 1) if bt is not None else bound + 1
    return [u32(dt + 4 * j) + BASE for j in range(n)]


def cfg(fn):
    b = body(fn); idx = {x.address: i for i, x in enumerate(b)}; succ = {}
    for i, x in enumerate(b):
        nx = b[i + 1].address if i + 1 < len(b) else None; m = x.mnemonic; t = []
        if m in ("ret", "int3"): pass
        elif m == "jmp":
            if x.operands[0].type == X86.X86_OP_IMM:
                if x.operands[0].imm in idx: t.append(x.operands[0].imm)
            else:
                tb = jtable(b, i)
                if tb: t.extend(a for a in tb if a in idx)
        elif m.startswith("j"):
            if x.operands[0].type == X86.X86_OP_IMM and x.operands[0].imm in idx: t.append(x.operands[0].imm)
            if nx: t.append(nx)
        elif nx: t.append(nx)
        succ[x.address] = t
    pred = {a: [] for a in succ}
    for a, ts in succ.items():
        for q in ts: pred[q].append(a)
    return b, idx, succ, pred


FAM = {}
for a4 in [("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
           ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl")]:
    FAM[a4[0]] = set(a4)
for n in range(8, 16): FAM["r%d" % n] = {"r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n}
SAVED = {"rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"}


def fam(r):
    for k, v in FAM.items():
        if r in v: return k
    return r


def writes(x, reg):
    m = x.mnemonic
    if m == "call": return reg not in SAVED
    if m.startswith("j") or m in ("cmp", "test", "bt", "push", "ret", "nop", "ucomiss", "comiss"): return False
    if m == "xchg": return any(o.type == X86.X86_OP_REG and fam(x.reg_name(o.reg)) == reg for o in x.operands)
    if not x.operands or x.operands[0].type != X86.X86_OP_REG: return m == "cdqe" and reg == "rax"
    return fam(x.reg_name(x.operands[0].reg)) == reg


def rdefs(G, site, reg):
    b, idx, succ, pred = G
    out = set(); seen = set(); st = list(pred[site])
    while st:
        a = st.pop()
        if a in seen: continue
        seen.add(a)
        if writes(b[idx[a]], reg): out.add(a); continue
        st.extend(pred[a])
    return [s(b[idx[a]]) for a in sorted(out)], sorted(out)


def reach(succ, start, stop=()):
    seen = set(); st = [start]
    while st:
        a = st.pop()
        if a in seen: continue
        seen.add(a)
        if a in stop and a != start: continue
        st.extend(succ[a])
    return seen


# =============================== SD-125 ===============================================================================
GD = cfg(0x002778C0)            # the battle command dispatcher
GM = cfg(0x00276D30)            # the menu widget
GC = cfg(0x00279E20)            # the controller
dD = {x.address: x for x in GD[0]}; dM = {x.address: x for x in GM[0]}; dC = {x.address: x for x in GC[0]}

# A1: the whole census of +0x2FF0 and what every writer can do to bit 0x4000
sites = sweep_disp(0x2FF0)
check("A1 CONTROL the +0x2FF0 sweep finds the producer's setter 002795B5, its clear 002795C2 and the reader 00276FD8",
      all(a in sites for a in (0x002795B5, 0x002795C2, 0x00276FD8)), "%d sites" % len(sites))
check("A1 every +0x2FF0 site lies in the menu family: 00276D30, 002778C0, 00279E20, 0027B430, 0027D330",
      {f for f, _ in sites.values()} == {0x00276D30, 0x002778C0, 0x00279E20, 0x0027B430, 0x0027D330})
WR = ("mov", "or", "and", "xor", "btr", "bts", "btc", "add", "sub")
writers = {a: ins for a, (f, ins) in sites.items()
           if ins.mnemonic in WR and ins.operands[0].type == X86.X86_OP_MEM}
imm_effect = {}
reg_writers = {}
for a, ins in writers.items():
    o1 = ins.operands[1]
    if o1.type == X86.X86_OP_IMM:
        v = o1.imm & 0xFFFFFFFF
        touches = bool(v & 0x4000) if ins.mnemonic in ("or", "xor") else bool((~v) & 0x4000) if ins.mnemonic == "and" else True
        imm_effect[a] = touches
    else:
        reg_writers[a] = ins
check("A1 immediate writers: only 002795B5 (or 0x4000) and 002795C2 (and 0xFFFFBFFF) can change bit 14",
      sorted(a for a, t in imm_effect.items() if t) == [0x002795B5, 0x002795C2],
      "%d immediate writers" % len(imm_effect))
# every register-sourced writer, resolved by reaching definitions in its own function (own CFG)
EXPECT = {   # site: (graph, reg, expected defining instruction texts, why bit 14 is untouched)
    0x00277B0B: (GD, "rcx", ["mov ecx, 0x200"], "or 0x200"),
    0x00277C8A: (GD, "rbx", ["mov ebx, 0x800"], "or 0x800"),
    0x00278797: (GD, "r12", ["mov r12d, 0x200"], "or 0x200"),
    0x0027884D: (GD, "rdi", ["mov edi, 0x200", "mov edi, 0x200"], "or 0x200"),
    0x00278DBB: (GD, "r12", ["mov r12d, 0x200"], "or 0x200"),
    0x00277A9B: (GD, "rdx", ["btr edx, 0x10"], "read of +0x2FF0 (00277A64) with bit 16 cleared"),
    0x00276F3B: (GM, "rax", ["btr eax, 9"], "read of +0x2FF0 (00276F27) with bit 9 cleared"),
    0x0027781E: (GM, "rax", ["and eax, 0x40000"], "xor-merge masked to bit 18"),
    0x0027A458: (GC, "rcx", ["and ecx, 0x40000"], "xor-merge masked to bit 18"),
    0x0027A503: (GC, "rcx", ["xor ecx, dword ptr [rdi + 0x2ff0]"], "merge masked to bit 17 (0027A4F7 and ecx, 0x20000)"),
    0x0027A523: (GC, "rcx", ["btr ecx, 0xb"], "the 0027A503 value with bit 11 cleared"),
    0x0027A53D: (GC, "rax", ["xor eax, ecx"], "merge masked to bit 11 (0027A536 and eax, 0x800)"),
    0x0027A55C: (GC, "rax", ["or eax, r12d"], "read of +0x2FF0 (0027A54D) or r12d, r12d = 0x2000 (0027A2FB)"),
    0x0027A487: (GC, None, None, "byte store: bits 0-7 only"),
}
bad = []
for a, ins in sorted(reg_writers.items()):
    if a not in EXPECT:
        bad.append("%08X unclassified %s" % (a, s(ins))); continue
    G, reg, exp, why = EXPECT[a]
    if reg is None:
        if not (ins.operands[0].size == 1): bad.append("%08X not a byte store" % a)
        continue
    got, _ = rdefs(G, a, reg)
    if got != exp: bad.append("%08X %s defs %s != %s" % (a, reg, got, exp))
check("A1 every register-sourced +0x2FF0 writer resolves (own reaching-definition walk) to a value that leaves bit 14 alone",
      not bad and len(reg_writers) == len(EXPECT), "; ".join(bad) if bad else "%d register writers classified" % len(reg_writers))
d55, _ = rdefs(GC, 0x0027A559, "r12")
check("A1 0027A55C's or-operand r12d reaches only from 0027A2FB mov r12d, 0x2000", d55 == ["mov r12d, 0x2000"], str(d55))
# no wider store from a neighbouring displacement covers byte +0x2FF1 (where bit 14 lives)
cover = []
for disp in [d for d in range(0x2FE2, 0x2FF2) if d != 0x2FF0]:
    for a, (f, ins) in sweep_disp(disp).items():
        mem = [o for o in ins.operands if o.type == X86.X86_OP_MEM]
        if mem and mem[0].mem.disp == disp and disp + mem[0].size > 0x2FF1 and ins.operands[0].type == X86.X86_OP_MEM:
            cover.append("%08X %s" % (a, s(ins)))
check("A1 no store at a displacement 0x2FE2..0x2FF1 other than +0x2FF0 itself reaches byte +0x2FF1 (where bit 14 lives)", not cover, "; ".join(cover))

b45 = {x.address: x for x in body(0x00245000)}; b46 = {x.address: x for x in body(0x002465F0)}
check("F3 the bit starts clear: the controller builds the 0x3010-byte menu (0027A428 mov edx, 0x3010, handler 00276D30 at "
      "0027A402) through 00245000 -> 002465F0, which memsets the whole object first (00246612 movsxd r8, edx / 00246618 "
      "xor edx, edx / 00246626 call 00861EC0 memset)",
      s(dC[0x0027A428]) == "mov edx, 0x3010" and ripv(dC[0x0027A402]) == 0x00276D30 and tgt(dC[0x0027A42D]) == 0x00245000
      and tgt(b45[0x00245011]) == 0x002465F0 and s(b46[0x00246612]) == "movsxd r8, edx" and s(b46[0x00246618]) == "xor edx, edx"
      and tgt(b46[0x00246626]) == 0x00861EC0 and FT[0x00861EC0][1] == "memset")

# A2: the kind word and the bit are written together
d_writes = [a for a, x in dD.items() if x.operands and x.operands[0].type == X86.X86_OP_MEM and x.operands[0].mem.disp == 0xD8
            and x.mnemonic in ("mov", "add", "sub", "inc", "dec", "and", "or", "xor")]
check("A2 inside the dispatcher the window-kind word +0xD8 has one writer, 002791AC (the message-31 arm)",
      d_writes == [0x002791AC], str(["%08X" % a for a in d_writes]))
r = reach(GD[2], 0x002791AC, stop={0x002795AE})
rets = [a for a, x in dD.items() if x.mnemonic == "ret"]
check("A2 every path from the kind store 002791AC to the dispatcher's ret passes the bit test 002795AE (so after each "
      "message 31 the bit equals 'k == 1')", 0x002795AE in reach(GD[2], 0x002791AC) and not any(a in r for a in rets),
      "rets %s" % ["%08X" % a for a in rets])
dd, _ = rdefs(GD, 0x002795AE, "rdi")
check("A2 CONTROL own reaching-definition walk agrees with the producer's P3: rdi at 002795AE is only 002791A7 mov edi, 1",
      dd == ["mov edi, 1"], str(dd))
check("A2 the test and both outcomes: 002795AE cmp qword [r12+8], rdi ; 002795B5 or 0x4000 ; 002795C2 and 0xFFFFBFFF",
      s(dD[0x002795AE]) == "cmp qword ptr [r12 + 8], rdi" and s(dD[0x002795B5]) == "or dword ptr [r15 + 0x2ff0], 0x4000"
      and s(dD[0x002795C2]) == "and dword ptr [r15 + 0x2ff0], 0xffffbfff")
# r15 = the menu widget: 00276D30's create arm builds the dispatcher at +0x220 with itself as the parameter
check("A2 the bit lives on the menu widget: the menu's create arm builds handler 002778C0 (00276DD3) at rdi+0x220 with "
      "+8 = its own pointer (00276DBD movsxd rax, edi); the dispatcher's id-1 arm stores +8 at +0xD0 (00277931) and "
      "002778EF loads r15 = [rcx+0xd0]",
      ripv(dM[0x00276DD3]) == 0x002778C0 and s(dM[0x00276DBD]) == "movsxd rax, edi" and s(dM[0x00276DC0]) == "lea rcx, [rdi + 0x220]"
      and s(dD[0x00277931]) == "mov qword ptr [rsi + 0xd0], rax" and s(dD[0x002778EF]) == "mov r15, qword ptr [rcx + 0xd0]")

# A3: the reader and the fleeing close
check("A3 00276FA0: 001EDEC0([rdi+0xB4]) == 0 leaves the arm before the test (00276FAD je 00277060), and bit 8 of "
      "+0x2FF0 skips the close block (00276FBB bt ecx, 8 / 00276FBF jb 00277067)",
      tgt(dM[0x00276FA6]) == 0x001EDEC0 and s(dM[0x00276FAD]) == "je 0x277060" and s(dM[0x00276FBB]) == "bt ecx, 8"
      and s(dM[0x00276FBF]) == "jb 0x277067")
check("A3 r14d = 00253BA0() (00276FD3 / 00276FE2), forced to 1 by bit 0x4000 (00276FD8 test, 00276FF2 cmovne r14d, r15d "
      "with r15d = 1 at 00276FEC)",
      tgt(dM[0x00276FD3]) == 0x00253BA0 and s(dM[0x00276FE2]) == "mov r14d, eax" and s(dM[0x00276FEC]) == "mov r15d, 1"
      and s(dM[0x00276FF2]) == "cmovne r14d, r15d")
check("A3 r14d == 0 closes unconditionally (00277034 je 0027704E -> or 0x200, 0027705B call 00244F00); r14d != 0 closes "
      "only when (bit 17 clear and edx) or r15d (00277036-0027704C)",
      s(dM[0x00277034]) == "je 0x27704e" and s(dM[0x0027704E]) == "or dword ptr [rdi + 0x2ff0], 0x200"
      and tgt(dM[0x0027705B]) == 0x00244F00 and s(dM[0x0027703E]) == "bt ecx, 0x11" and s(dM[0x00277042]) == "cmovae eax, edx"
      and s(dM[0x0027704C]) == "je 0x277067")
bb = body(0x00253BA0); b3 = body(0x003BA2E0)
check("A3 00253BA0 (27 B) = 003BA2E0() ? dword[01E0C2B8] : 0; 003BA2E0 reads bytes 02B4053C / 02B4053D (the force-fight "
      "page: both set at boot, the only clearing verb unused) - so effective 0 means the flag 01E0C2B8 is 0 (FLEEING)",
      size[0x00253BA0] == 27 and any(tgt(x) == 0x003BA2E0 for x in bb) and any(ripv(x) == 0x01E0C2B8 for x in bb)
      and {ripv(x) for x in b3 if ripv(x)} >= {0x02B4053C, 0x02B4053D})
g1 = body(0x001EDEC0)
check("F1 the 001EDEC0 gate the register paragraph leaves out: answers 1 unless dword 01F82E38 is set and 01DFE0C0 is "
      "clear, then (~arg) & 1 (arg = menu +0xB4)",
      [ripv(x) for x in g1 if ripv(x)] == [0x01F82E38, 0x01DFE0C0] and any(s(x) == "not ecx" for x in g1))

# A4: senders - an independent immediate census of `mov dword [mem], 0x1f`
pat = struct.pack("<I", 0x1F); hits = set(); p = 0
while True:
    k = TDATA.find(pat, p)
    if k < 0: break
    p = k + 1
    for back in range(2, 12):
        a = TVA + k - back
        ins = next(md.disasm(TDATA[k - back:k - back + 16], a), None)
        if ins is None or ins.address + ins.size != TVA + k + 4: continue
        if ins.mnemonic == "mov" and ins.operands[0].type == X86.X86_OP_MEM and ins.operands[0].size == 4 \
                and ins.operands[1].type == X86.X86_OP_IMM and ins.operands[1].imm == 0x1F:
            f = fn_of(a)
            if f is None or a in boundaries(f):
                hits.add(a)
want = {0x00277C9B, 0x00278030, 0x00278212, 0x00278882, 0x00278F80, 0x0027A5D3, 0x002BB7C4, 0x002BBA0B, 0x003CA245,
        0x00551E32, 0x00551F3D, 0x005541CD, 0x00832417}
check("A4 own census of `mov dword [mem], 0x1f` on instruction boundaries = the producer's 13 builds exactly",
      hits == want, "extra %s missing %s" % (sorted("%08X" % a for a in hits - want), sorted("%08X" % a for a in want - hits)))
check("A4 the two foreign {31, 1} builds load the payload qword 1 from 00915BB0 (002BB7C4 / 002BBA0B in 002BAF80)",
      struct.unpack("<QQ", raw(0x00915BB0, 16)) == (1, 0) and fn_of(0x002BB7C4) == 0x002BAF80 and fn_of(0x002BBA0B) == 0x002BAF80)
check("A4 kind 1 -> list code 6: 0027E050's table 0027E384 entry 0 (kind - 1 = 0) is 0027E098, whose case stores 6 at "
      "+0x4C0 (0027E0A6)", u32(0x0027E384) + BASE == 0x0027E098
      and s(next(md.disasm(raw(0x0027E0A6, 16), 0x0027E0A6))) == "mov dword ptr [rcx + 0x4c0], 6")

# =============================== SD-128 ===============================================================================
bx = body(0x002C7660); dX = {x.address: x for x in bx}
check("B1 002C7660 is 1,190 B with one ret (002C7B05) and no indirect jmp",
      size[0x002C7660] == 1190 and [x.address for x in bx if x.mnemonic == "ret"] == [0x002C7B05]
      and not any(x.mnemonic == "jmp" and x.operands[0].type != X86.X86_OP_IMM for x in bx))
# callers: own raw rel32 sweep for E8/E9 to 002C7660 and 002C62B0
def rel_callers(t):
    out = []
    for op in (b"\xe8", b"\xe9"):
        p = 0
        while True:
            k = TDATA.find(op, p)
            if k < 0: break
            p = k + 1
            if k + 5 <= len(TDATA) and TVA + k + 5 + struct.unpack("<i", TDATA[k + 1:k + 5])[0] == t:
                f = fn_of(TVA + k)
                if f is None or (TVA + k) in boundaries(f): out.append(TVA + k)
    return sorted(out)
c1 = rel_callers(0x002C7660); c2 = rel_callers(0x002C62B0)
check("B2 CONTROL own rel32 sweep finds 0028EDAD -> 002C62B0", c2 == [0x0028EDAD], str(["%08X" % a for a in c2]))
check("B2 002C7660 has one direct caller, 002C632F in 002C62B0", c1 == [0x002C632F], str(["%08X" % a for a in c1]))
b62 = {x.address: x for x in body(0x002C62B0)}
check("B2 002C62B0 walks the list at [hud+0x1D70] with next = [node+0x18] around the call",
      s(b62[0x002C62F1]) == "mov rbx, qword ptr [rsi + 0x1d70]" and tgt(b62[0x002C632F]) == 0x002C7660
      and s(b62[0x002C6334]) == "mov rbx, qword ptr [rbx + 0x18]" and s(b62[0x002C633B]) == "jne 0x2c6310")
# the distance scale
check("B3 the label scale constants: R/3 (008F311C = 3.0), floor 0.8 (008F3108), span 0.2 (00916F24), 1.0 (01CEBBA8); "
      "R = hud+0x1D7C (002C79BA); stored to slot +0x1834 (002C7A14)",
      ripv(dX[0x002C79C9]) == 0x008F311C and f32(0x008F311C) == 3.0 and ripv(dX[0x002C79E4]) == 0x008F3108
      and abs(f32(0x008F3108) - 0.8) < 1e-6 and ripv(dX[0x002C79F6]) == 0x00916F24 and abs(f32(0x00916F24) - 0.2) < 1e-6
      and ripv(dX[0x002C7A08]) == 0x01CEBBA8 and f32(0x01CEBBA8) == 1.0
      and s(dX[0x002C79BA]) == "movss xmm2, dword ptr [r14 + 0x1d7c]" and "0x1834]" in s(dX[0x002C7A14]))
# the label is the unit's display name (the record calls it the name label without citing the text writer)
b8a = {x.address: x for x in body(0x002C8A60)}; b8b = {x.address: x for x in body(0x002C8BC0)}
bcd = {x.address: x for x in body(0x00272CE0)}
check("F2 the slot text the label measures (+0x130 of the 0x1C0 record, = hud+0x1930 for slot 0) is written by 002C8BC0 "
      "(002C8BDF lea rbx, [rcx+0x130]) through 00272CE0(buf, node+0x10); 002C8BC0's one caller is the slot claim 002C8A60, "
      "which keys the slot by the node handle (002C8B96 mov [rbx+0x1b0], eax)",
      s(b8b[0x002C8BDF]) == "lea rbx, [rcx + 0x130]" and tgt(b8b[0x002C8C02]) == 0x00272CE0 and tgt(b8b[0x002C8CB5]) == 0x00272CE0
      and s(b8b[0x002C8BF0]) == "mov edx, dword ptr [rdx + 0x10]" and rel_callers(0x002C8BC0) == [0x002C8B8E]
      and s(b8a[0x002C8B96]) == "mov dword ptr [rbx + 0x1b0], eax")
check("F2 00272CE0 resolves the handle (003588B0) and copies 00263990(unit) = Actor_GetDisplayName (+0xF8 literal or the "
      "+0x102 name id), plus a formatted suffix from 00263A10 - so 'name label' holds; with node+0x17 & 0x30 == 0x30 the "
      "name is prefixed by text id 0x46D8 (002C8BF3-002C8C0C)",
      tgt(bcd[0x00272CFE]) == 0x003588B0 and tgt(bcd[0x00272D1A]) == 0x00263990 and tgt(bcd[0x00272D2E]) == 0x00263A10
      and FT[0x00263990][1] in ("Actor_GetDisplayName", "FUN_00263990")
      and s(b8b[0x002C8BF3]) == "and al, 0x30" and s(b8b[0x002C8C07]) == "mov ecx, 0x46d8" and tgt(b8b[0x002C8C0C]) == 0x002F9860)
callees = {tgt(x) for x in bx if x.mnemonic == "call"}
check("B4 002C7660 calls none of 00329220 / 0031FE70 / 00320040 / 0031FEC0 / 0031FF70 and makes no indirect call",
      not callees & {0x00329220, 0x0031FE70, 0x00320040, 0x0031FEC0, 0x0031FF70}
      and not any(x.mnemonic == "call" and x.operands[0].type != X86.X86_OP_IMM for x in bx))

print("FAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
