"""action_row_reader_hops.py - UQ-106 / AY-2: readers of the action definition row (60-byte rows, registry slot 02EBF138) found by
following the row pointer THROUGH CALL ARGUMENTS, which the page's tracker does not do.

Hop 0 (the page's idiom, re-implemented): in every function that references 02EBF138, after `call 0020E600` the
result rax is the row-array base; the first instruction that adds a register to it (add / lea) yields the ROW
pointer. From there the tracker follows the row through register copies, stack-slot spills/reloads and
`lea r, [row + k]` (a derived pointer, offset k), killing a register when it is overwritten, and records every
memory read `[row + k + disp]` as a read of offset k + disp.
Hop 1: when a row value (offset k) sits in rcx/rdx/r8/r9 at a `call X`, X is analysed with that parameter register
bound to row+k (and followed the same way, one level deep, no further calls followed).

Controls: the page's own readers must reappear at hop 0 (+0x08 at 0038617E in BattleFormula_ResolveTargetResult,
+0x12 at 00389089). Output: per offset, the hop-0 and hop-1 reader sites; then the eighteen bytes the page lists
as unread."""
import struct, sys, collections, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000; SLOT = 0x2EBF138; RESOLVE = 0x20E600; ROWSZ = 0x3C
UNREAD = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x1C, 0x1D, 0x1F, 0x20, 0x21, 0x24, 0x2D, 0x30, 0x36, 0x38, 0x3A]
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((BASE + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs: return ro + (a - va)
sizes = {}; names = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
_cache = {}
def ins(f):
    if f not in _cache: _cache[f] = list(md.disasm(d[off(f):off(f) + sizes[f]], f))
    return _cache[f]
GPR64 = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15", "rsp"}
def full(r):
    """64-bit name of a register operand name"""
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp",
         "r8d": "r8", "r9d": "r9", "r10d": "r10", "r11d": "r11", "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15"}
    return m.get(r, r)
ARGREGS = ["rcx", "rdx", "r8", "r9"]

def track(f, start_i, vals, hop, out, hops):
    """vals: dict register/stackslot -> offset k meaning 'holds row + k'. Walk linearly from start_i; a jump
    backwards or forwards is not followed (linear, like the page's tracker); stop at ret. Records reads and hops."""
    xs = ins(f)
    dbg = os.environ.get("DEBUG_FN")
    index_of = {x.address: k for k, x in enumerate(xs)}
    pos = start_i
    while pos < len(xs):
        x = xs[pos]; pos += 1
        if x.mnemonic == "ret": break
        ops = x.operands
        # a FORWARD unconditional jmp inside the body is followed (it skips the other arm's join code, which a
        # linear walk would otherwise execute and let kill the binding); a backward one ends the walk
        if x.mnemonic == "jmp" and ops and ops[0].type == X86_OP_IMM:
            t = ops[0].imm
            if t in index_of and index_of[t] > pos - 1: pos = index_of[t]; continue
            break
        if dbg and f == int(dbg, 16) and 0x386150 <= x.address <= 0x386190:
            print("   TRACE %08X %-7s %-40s %s" % (x.address, x.mnemonic, x.op_str[:40], vals))
        # reads of [row + k + disp], and of [base + id*60 + disp] where the base register is bound to BASE
        for idx, op in enumerate(ops):
            if op.type == X86_OP_MEM and op.mem.base:
                b = md.reg_name(op.mem.base)
                if b in ("rsp", "rbp") or b not in vals: continue
                if vals[b] == "BASE":
                    if not op.mem.index or op.mem.scale != 1: continue
                    o = op.mem.disp
                elif not op.mem.index:
                    o = vals[b] + op.mem.disp
                else:
                    continue
                if True:
                    if 0 <= o < ROWSZ:
                        kind = "w" if (idx == 0 and x.mnemonic.startswith(("mov", "and", "or", "xor", "add", "sub", "inc", "dec")) and len(ops) > 1) else "r"
                        if idx == 0 and x.mnemonic in ("cmp", "test"): kind = "r"
                        out[o].append((hop, f, x.address, kind, op.size))
        # hop through a call
        if x.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM and hop == 0:
            t = ops[0].imm
            bound = {r: vals[r] for r in ARGREGS if r in vals and vals[r] != "BASE"}
            if bound and t in sizes and t != RESOLVE:
                hops.append((f, x.address, t, dict(bound)))
                track(t, 0, dict(bound), 1, out, hops)
            # volatile registers die
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                vals.pop(r, None)
            continue
        if x.mnemonic == "call":
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"): vals.pop(r, None)
            continue
        # propagation
        if x.mnemonic == "mov" and len(ops) == 2:
            dst, src = ops
            if dst.type == X86_OP_REG and src.type == X86_OP_REG:
                ds, ss = full(md.reg_name(dst.reg)), full(md.reg_name(src.reg))
                if ss in vals and dst.size == 8: vals[ds] = vals[ss]
                else: vals.pop(ds, None)
                continue
            if dst.type == X86_OP_MEM and src.type == X86_OP_REG and dst.mem.base and md.reg_name(dst.mem.base) in ("rsp", "rbp") and not dst.mem.index:
                key = "%s%+d" % (md.reg_name(dst.mem.base), dst.mem.disp); ss = full(md.reg_name(src.reg))
                if ss in vals and src.size == 8: vals[key] = vals[ss]
                else: vals.pop(key, None)
                continue
            if dst.type == X86_OP_REG and src.type == X86_OP_MEM and src.mem.base and md.reg_name(src.mem.base) in ("rsp", "rbp") and not src.mem.index:
                key = "%s%+d" % (md.reg_name(src.mem.base), src.mem.disp); ds = full(md.reg_name(dst.reg))
                if key in vals and dst.size == 8: vals[ds] = vals[key]
                else: vals.pop(ds, None)
                continue
        if x.mnemonic == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
            ds = full(md.reg_name(ops[0].reg)); m = ops[1].mem
            b = md.reg_name(m.base) if m.base else None
            ix = md.reg_name(m.index) if m.index else None
            if b in vals and vals[b] == "BASE" and ix and m.scale == 1: vals[ds] = m.disp          # row = base + id*60 (+disp)
            elif ix in vals and vals.get(ix) == "BASE" and m.scale == 1: vals[ds] = m.disp
            elif b in vals and vals[b] != "BASE" and not m.index: vals[ds] = vals[b] + m.disp
            else: vals.pop(ds, None)
            continue
        if x.mnemonic == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            a, b = full(md.reg_name(ops[0].reg)), full(md.reg_name(ops[1].reg))
            if vals.get(a) == "BASE" or vals.get(b) == "BASE": vals[a] = 0      # row = base + id*60
            else: vals.pop(a, None)
            continue
        # any other write to a register kills it (first operand written for most mnemonics)
        if ops and ops[0].type == X86_OP_REG and x.mnemonic not in ("cmp", "test", "push"):
            vals.pop(full(md.reg_name(ops[0].reg)), None)

def hop0_roots(f):
    """(index, binding) pairs: right after every call 0020E600 in a function that references the slot, rax is the
    row-array BASE. The tracker then derives the row (add / lea with an index) or reads through base+index itself."""
    xs = ins(f); roots = []
    for i, x in enumerate(xs):
        if x.mnemonic == "call" and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == RESOLVE:
            # PROVENANCE: the resolve's ecx must be [REG + 0xC] with REG loaded from [02EBF138]; a function that
            # resolves several registry slots must not have its other tables' rows attributed to the action row.
            slotreg = None; ok = False
            for j in range(i - 1, max(-1, i - 10), -1):
                y = xs[j]; o = y.operands
                if slotreg is None and y.mnemonic == "mov" and len(o) == 2 and o[0].type == X86_OP_REG and md.reg_name(o[0].reg) in ("ecx", "rcx") \
                        and o[1].type == X86_OP_MEM and o[1].mem.base and not o[1].mem.index and o[1].mem.disp == 0xC:
                    slotreg = md.reg_name(o[1].mem.base); continue
                if slotreg and y.mnemonic == "mov" and len(o) == 2 and o[0].type == X86_OP_REG and md.reg_name(o[0].reg) == slotreg \
                        and o[1].type == X86_OP_MEM and o[1].mem.base and md.reg_name(o[1].mem.base) == "rip":
                    ok = (y.address + y.size + o[1].mem.disp == SLOT); break
                if slotreg and o and o[0].type == X86_OP_REG and md.reg_name(o[0].reg) == slotreg and y.mnemonic not in ("cmp", "test"):
                    break
            if ok: roots.append((i + 1, "rax"))
    return roots

# functions referencing the slot
refs = []
for f in sorted(sizes):
    if f < 0x121000 or f >= 0x8C2000 or sizes[f] <= 0: continue
    body = d[off(f):off(f) + sizes[f]]
    if b"\x38\xf1\xeb\x02" not in body and b"\xeb\x02" not in body:
        pass
    for x in md.disasm(body, f):
        hit = False
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.base and md.reg_name(op.mem.base) == "rip" and x.address + x.size + op.mem.disp == SLOT:
                hit = True
        if hit: refs.append(f); break
print("functions referencing 02EBF138:", len(refs))
out = collections.defaultdict(list); hops = []; rooted = 0
for f in refs:
    rs = hop0_roots(f)
    if rs: rooted += 1
    for i, reg in rs:
        track(f, i, {reg: "BASE"}, 0, out, hops)
print("functions with a decoded row root:", rooted, " hops into callees:", len(hops), " distinct callees:", len({h[2] for h in hops}))
def fmt(sites):
    fs = collections.OrderedDict()
    for hop, f, a, k, w in sites: fs.setdefault((hop, f), []).append((a, k, w))
    return "; ".join("h%d %08X %s [%s]" % (hop, f, names.get(f, "?")[:28], ",".join("%08X%s%d" % (a, k, w) for a, k, w in v[:3]) + (" +%d" % (len(v) - 3) if len(v) > 3 else "")) for (hop, f), v in fs.items())
print("\nCONTROLS: +0x08 sites:", [("%08X" % a) for _, f, a, k, w in out[8] if f == 0x386000 or True][:6], "| +0x12:", [("%08X" % a) for _, f, a, k, w in out[0x12]][:6])
print("\nPER OFFSET (hop0 readers / hop1 readers):")
for o in range(ROWSZ):
    s = out.get(o, [])
    if not s: continue
    h0 = {f for h, f, a, k, w in s if h == 0}; h1 = {f for h, f, a, k, w in s if h == 1}
    print("  +0x%02X  hop0 %2d fn  hop1 %2d fn   %s" % (o, len(h0), len(h1), fmt(s)[:230]))
print("\nTHE EIGHTEEN UNREAD BYTES:")
for o in UNREAD:
    s = out.get(o, [])
    print("  +0x%02X: %s" % (o, fmt(s)[:400] if s else "NO READER FOUND (hop 0 or 1)"))
for a in sys.argv[1:]:
    if a.startswith("--tsv="):
        with open(a[6:], "w", encoding="utf-8", newline="\n") as fh:
            fh.write("offset\thop\tfunction\tname\tsite\taccess\twidth\n")
            for o in sorted(out):
                for hop, f, addr, k, w in sorted(set(out[o])):
                    fh.write("0x%02X\t%d\t%08X\t%s\t%08X\t%s\t%d\n" % (o, hop, f, names.get(f, "?"), addr, k, w))
        print("wrote", a[6:])
if "--hops" in sys.argv:
    print("\nHOPS:")
    for f, a, t, b in hops[:80]: print("  %08X @%08X -> %08X %-30s %s" % (f, a, t, names.get(t, "?")[:30], b))
