"""SWE2-AUDIT-SEM: semantic review of FABLE's GR-19 answer, GR-11 narrowing and GR-12 narrowing (2c1666588), re-derived
from the certified image (capstone + pefile on Tools/work/exe/FFXII_TZA.exe). The CFG with bounded jump tables and the
reaching-definition walk are this review's own code. G19 = GR-19, G11 = GR-11, G12 = GR-12; F-checks are findings this
review adds (they PASS when the finding reproduces). Positive controls are marked CONTROL.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-gr19-gr11-0930/gr19_11_12_sem.py"
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


def bmap(fn): return {i.address: i for i in body(fn)}


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
    f = starts[k] if k >= 0 else None
    return f if f is not None and a < f + max(size[f], 1) else None


_b = {}
def boundaries(f):
    if f not in _b: _b[f] = {i.address for i in body(f)}
    return _b[f]


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
    return ["%08X %s" % (a, s(b[idx[a]])) for a in sorted(out)]
def reach(succ, start, stop=()):
    seen = set(); st = [start]
    while st:
        a = st.pop()
        if a in seen: continue
        seen.add(a)
        if a in stop and a != start: continue
        st.extend(succ[a])
    return seen


# =============================== GR-19 ================================================================================
g = bmap(0x00319490)
check("G19-1 00319490: focus 003590D0 -> 003588B0 -> 00263E30; passes the unit only when byte 02089340 bit 0x10 is set "
      "(003194AD) and unit byte 0 has bit 3 (003194CF), else null; w = 1.0 (01CEBBA8)",
      tgt(g[0x003194A8]) == 0x003590D0 and ripv(g[0x003194AD]) == 0x02089340 and s(g[0x003194AD]).endswith(", 0x10")
      and tgt(g[0x003194B8]) == 0x003588B0 and tgt(g[0x003194C5]) == 0x00263E30 and s(g[0x003194CF]) == "test byte ptr [rax], 8"
      and s(g[0x003194D4]) == "xor eax, eax" and ripv(g[0x003194F8]) == 0x01CEBBA8 and f32(0x01CEBBA8) == 1.0
      and tgt(g[0x0031950C]) == 0x003377C0)
G7 = cfg(0x003377C0); d7 = {x.address: x for x in G7[0]}
nan = [a for a, x in d7.items() if x.mnemonic == "ucomiss" and x.operands[0].reg == x.operands[1].reg]
check("F1 the gather switch tests all three coordinates for NaN, not only x: self-compares at 0033786A / 00337877 / "
      "00337884 on [r15], [r15+4], [r15+8], each jp/jne to 003378B9 (the 003920F0 gather)",
      nan == [0x0033786A, 0x00337877, 0x00337884] and s(d7[0x00337865]) == "movss xmm0, dword ptr [r15]"
      and s(d7[0x00337871]) == "movss xmm0, dword ptr [r15 + 4]" and s(d7[0x0033787E]) == "movss xmm0, dword ptr [r15 + 8]"
      and all(tgt(d7[a]) == 0x003378B9 for a in (0x0033786D, 0x0033786F, 0x0033787A, 0x0033787C, 0x00337887, 0x00337889))
      and tgt(d7[0x003378E6]) == 0x003920F0 and tgt(d7[0x003378B2]) == 0x00391D10)
rd = rdefs(G7, 0x00337956, "rdx")
check("G19-2 own reaching-definition walk: rdx at the pairing call 00337956 comes only from 0033790D (the gathered "
      "actor [rsp+rbx*8+0x80]); rcx = rbp (00337953)", rd == ["0033790D mov rdx, qword ptr [rsp + rbx*8 + 0x80]"]
      and s(d7[0x00337953]) == "mov rcx, rbp", str(rd))
rc = rdefs(G7, 0x0033796F, "rdx")
check("G19-2 CONTROL the same walk at the relation call 0033796F sees the reload 0033795F", rc == ["0033795F mov rdx, qword ptr [rsp + rbx*8 + 0x80]"], str(rc))
rb = rdefs(G7, 0x00337915, "rbp")
check("G19-2 the excluded / pairing actor rbp is 0031ABE0([00236820(byte [unit+0xEA9]) + 8]) (00337837-00337855) - the "
      "corridor family's GATE resolves its agent's actor through the same GTAB / MABE pair",
      rb == ["00337855 mov rbp, rax"] and s(d7[0x00337837]) == "movzx ecx, byte ptr [r14 + 0xea9]"
      and tgt(d7[0x00337845]) == 0x00236820 and tgt(d7[0x0033784D]) == 0x0031ABE0, str(rb))
tail = [s(d7[a]) for a in (0x0033798D, 0x0033798F, 0x00337991, 0x00337993, 0x00337995, 0x00337998, 0x0033799A, 0x0033799C)]
check("G19-3 any pairing actor refuses: esi != 0 -> 0033799A xor eax, eax; edi != 0 -> eax = 2, falls into the same xor; "
      "only esi = edi = 0 reaches 00337700 (0033799E)",
      tail == ["test esi, esi", "jne 0x33799a", "neg edi", "sbb eax, eax", "and eax, 2", "je 0x33799e", "xor eax, eax", "jmp 0x3379a9"]
      and tgt(d7[0x003379A4]) == 0x00337700)
p = body(0x00314EB0)
disps = sorted({o.mem.disp for x in p for o in x.operands if o.type == X86.X86_OP_MEM})
check("F2 00314EB0 reads only the two bodies' layer +6 and owner +0x119 (after [actor+0xC0]+0x138): it is the separation "
      "pass's pairing prerequisite, not its contact test - no radii (+0xF0 / +0xF4), activity, vertical extent or "
      "ellipse separation (00314F50's tests) is read", disps == [6, 0xC0, 0x119, 0x138] and size[0x00314EB0] < 0x80,
      "displacements %s" % [hex(x) for x in disps])
g7 = bmap(0x00337700)
check("G19-4 00337700: LQUERY 00391410(point, point, radius A) nonzero refuses (0033774C / 00337753); 00384130 = 0xFF "
      "refuses (0033776F-00337779); 00336390(point, max(A, B), byte [unit+0x1F4]) decides (00337784-00337792)",
      tgt(g7[0x0033774C]) == 0x00391410 and s(g7[0x00337753]) == "jne 0x337724" and tgt(g7[0x0033776F]) == 0x00384130
      and s(g7[0x00337774]) == "cmp eax, 0xff" and s(g7[0x00337784]) == "maxss xmm1, dword ptr [rsp + 0x24]"
      and s(g7[0x0033778A]) == "movzx r8d, byte ptr [rdi + 0x1f4]" and tgt(g7[0x00337792]) == 0x00336390)
q = body(0x00336390)
calls = [x.address for x in q if tgt(x) == 0x0032A6A0]
offs = [(s(x)) for x in q if x.mnemonic in ("addss", "subss") and x.operands[1].type == X86.X86_OP_REG]
check("G19-4 00336390: five calls of 0032A6A0 (centre, then x+r z+r, x+r z-r, x-r z+r, x-r z-r), each refusing on 0; "
      "the mode argument is the +0x1F4 byte, the third 0", len(calls) == 5
      and offs == ["addss xmm0, xmm6"] * 3 + ["subss xmm0, xmm6"] + ["subss xmm0, xmm6", "addss xmm0, xmm6"]
      + ["subss xmm0, xmm6"] * 2 and u32(0x0032A6A0) & 0xFF == 0xE9 and tgt(next(md.disasm(raw(0x0032A6A0, 8), 0x0032A6A0))) == 0x0026E100,
      "%d calls" % len(calls))
pv = {tgt(x) for x in body(0x00335B60) if x.mnemonic in ("call", "jmp")}
check("F3 the leader's forward-step clearance test PVAL 00335B60 calls the same two queries (LQUERY 00391410 and DE6A0 "
      "0032A6A0) - so 'could stand here' has the engine's own precedent, but neither query's world is named "
      "('static geometry' and 'walkable ground' are glosses)", {0x00391410, 0x0032A6A0} <= pv)

# =============================== GR-11 ================================================================================
c = bmap(0x0025A180)
pairs = [(x.operands[1].mem.disp, c[x.address + x.size].address) for x in c.values()
         if x.mnemonic == "movups" and x.operands[0].type == X86.X86_OP_REG and x.operands[1].type == X86.X86_OP_MEM
         and x.operands[1].mem.base == X86.X86_REG_RAX]
srcs = sorted(d for d, _ in pairs)
dsts = sorted(o.mem.disp for x in c.values() if x.mnemonic == "movups" and x.operands[0].type == X86.X86_OP_MEM
              and x.operands[0].mem.base == X86.X86_REG_R8 for o in [x.operands[0]])
check("G11-1 0025A180: ctx = 02097D20 + k*0x860 (0025A191 / 0025A198); body = [[actor+0xC0]+0x138]; eleven 16-byte "
      "copies +0x30..+0xDF -> ctx+0x7A0..+0x84F", ripv(c[0x0025A198]) == 0x02097D20 and s(c[0x0025A191]) == "imul rbx, rax, 0x860"
      and srcs == list(range(0x30, 0xE0, 0x10)) and dsts == list(range(0, 0xB0, 0x10))
      and s(c[0x0025A1C6]) == "lea r8, [rbx + 0x7a0]", "src %s" % [hex(x) for x in srcs])
i5 = body(0x00259510)
rdx_reads = sorted({o.mem.disp for x in i5 for o in x.operands if o.type == X86.X86_OP_MEM and o.mem.base in (X86.X86_REG_RDX, X86.X86_REG_RBX)})
r8_reads = sorted({o.mem.disp for x in i5 for o in x.operands if o.type == X86.X86_OP_MEM and o.mem.base in (X86.X86_REG_R8, X86.X86_REG_RDI)})
check("F4 the one function 0025A180 hands ctx+0x6F0 to (00259510, rdx = ctx+0x6F0 at 0025A1D5, called at 0025A25C) reads "
      "only +0x0..+0x18 of it (and of r8 = ctx+0x7A0): the interpolator; so this handed-pointer path does not read the "
      "0x90 bytes GR-11 still asks about", tgt(c[0x0025A25C]) == 0x00259510 and s(c[0x0025A1D5]) == "lea rdx, [rbx + 0x6f0]"
      and max(rdx_reads) <= 0x18 and max(r8_reads) <= 0x18 and size[0x00259510] < 0x120,
      "rdx/rbx disps %s, r8/rdi disps %s" % ([hex(x) for x in rdx_reads], [hex(x) for x in r8_reads]))

# =============================== GR-12 ================================================================================
GL = cfg(0x0027CE70); dl = {x.address: x for x in GL[0]}
check("G12-1 the list body 0027CE70: at 0027D131-0027D156 an entry whose id is 0x9C / 0x9D asks 00273270 (the stash) and "
      "branches on 0xFFFF (r14w = 0xFFFF from both reaching definitions)", s(dl[0x0027D131]) == "mov ecx, 0x9c" and s(dl[0x0027D145]) == "ja 0x27d184"
      and tgt(dl[0x0027D14D]) == 0x00273270 and s(dl[0x0027D152]) == "cmp ax, r14w" and s(dl[0x0027D156]) == "je 0x27d184"
      and rdefs(GL, 0x0027D152, "r14") == ["0027CF53 mov r14d, 0xffff", "0027D107 mov r14d, 0xffff"])
both = [0x0027D184 in reach(GL[2], t) for t in GL[2][0x0027D156]]
gated = [a for a in sorted(dl) if 0x0027D158 <= a < 0x0027D184]
gw = sorted({s(dl[a]) for a in gated if dl[a].operands and dl[a].operands[0].type == X86.X86_OP_MEM and dl[a].mnemonic not in ('test', 'cmp')})
check("F5 the stash gate does not drop the entry: both successors of 0027D156 reach 0027D184, which draws it "
      "(0027D193 call 002D8650, the same draw 0027CF18 uses); the gated block 0027D158-0027D17F writes only +0x15EF = 6 "
      "(flag bit 0 set) and the entry state word [rdi+0x5A] (0x40 when flag bit 0 is clear, else r15w = 0x80) - the "
      "inverse of the default set at 0027CF6C-0027CF7D (0x40 when bit 0 is set, else 0x80)",
      all(both) and len(both) == 2 and tgt(dl[0x0027D193]) == 0x002D8650 and tgt(dl[0x0027CF18]) == 0x002D8650
      and gw == ["mov byte ptr [rbx + 0x15ef], 6", "mov word ptr [rdi + 0x5a], r15w"]
      and s(dl[0x0027D175]) == "mov eax, 0x40" and s(dl[0x0027D17A]) == "cmovne r15w, ax"
      and rdefs(GL, 0x0027D17A, "r15") == ["0027CF5E mov r15d, 0x80"]
      and s(dl[0x0027CF74]) == "mov ecx, 0x40" and s(dl[0x0027CF79]) == "cmovne ax, cx" and s(dl[0x0027CF7D]) == "mov word ptr [rdx + 0x5a], ax"
      and s(dl[0x0027CE90]) == "mov rdi, rdx", "gated writes %s" % gw)
k = bmap(0x0027C3D0)
check("G12-2 kind 11 issues 0x9C / 0x9D at once: 00311CD0(unit, unit, id, 0) (0027C5F2-0027C5FE), answer 0x17; kind 24 "
      "issues 0x9D for an entry equal to the stash or 0xFFFF, else 0x9C (0027C619-0027C665); the kind-11 arm needs entry "
      "+0x54 bit 0 clear (0027C588), the kind-24 arm +0x52 bit 0 clear (0027C613)",
      s(k[0x0027C5F2]) == "mov ecx, dword ptr [rbx + 8]" and s(k[0x0027C5F8]) == "mov edx, ecx" and s(k[0x0027C5F5]) == "xor r9d, r9d"
      and tgt(k[0x0027C5FE]) == 0x00311CD0 and s(k[0x0027C608]) == "mov eax, 0x17" and s(k[0x0027C588]) == "test cl, 1"
      and s(k[0x0027C613]) == "test byte ptr [rdx + 0x52], 1" and tgt(k[0x0027C620]) == 0x00273270
      and s(k[0x0027C62A]) == "mov eax, 0xffff" and s(k[0x0027C637]) == "mov r8d, 0x9c" and s(k[0x0027C65A]) == "mov r8d, 0x9d")
# own census of compares of a +0x1E byte with 13, both idioms, with controls
direct, viaz = [], []
for kk in range(len(TDATA) - 4):
    b0, b1 = TDATA[kk], TDATA[kk + 1]
    if b0 == 0x80 and (b1 & 0xF8) == 0x78 and (b1 & 7) != 4 and TDATA[kk + 2] == 0x1E:
        for pre in (0, 1):
            a = TVA + kk - pre
            ins = next(md.disasm(TDATA[kk - pre:kk - pre + 16], a), None)
            if ins is None or ins.mnemonic != "cmp" or "+ 0x1e]" not in ins.op_str: continue
            f = fn_of(a)
            if f is None or a in boundaries(f): direct.append((a, ins.op_str)); break
    if b0 == 0x0F and b1 == 0xB6 and (TDATA[kk + 2] >> 6) == 1 and (TDATA[kk + 2] & 7) != 4 and TDATA[kk + 3] == 0x1E:
        for pre in (0, 1):
            a = TVA + kk - pre
            seq = list(md.disasm(TDATA[kk - pre:kk - pre + 48], a))[:5]
            if not seq or seq[0].mnemonic != "movzx" or "+ 0x1e]" not in seq[0].op_str: continue
            f = fn_of(a)
            if f is None or a in boundaries(f):
                viaz.append((a, [x.op_str for x in seq[1:] if x.mnemonic in ("cmp", "sub", "add")])); break
check("F6 CONTROL own +0x1E compare census (direct `cmp byte [reg+0x1e], imm` and movzx-then-cmp within four) finds the "
      "known category readers 00309425 (cmp 3), 0046A444 (cmp 2) and 004699F5 (movzx, cmp 2)",
      any(a == 0x00309425 for a, _ in direct) and any(a == 0x0046A444 for a, _ in direct) and any(a == 0x004699F5 for a, _ in viaz),
      "%d direct, %d movzx" % (len(direct), len(viaz)))
thirteen = [a for a, o in direct if o.endswith(", 0xd")] + [a for a, c in viaz if any(x.endswith(", 0xd") or x.endswith(", -0xd") for x in c)]
check("F6 neither idiom compares a +0x1E byte with 13 anywhere in .text (the producer's filter saw only the movzx form; "
      "a switch indexed by the byte is not covered by either)", thirteen == [], str(["%08X" % a for a in thirteen]))

print("FAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
