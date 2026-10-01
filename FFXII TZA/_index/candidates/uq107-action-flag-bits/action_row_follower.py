"""action_row_follower.py - the GA-1 row follower (ga1-status-open-bytes/ga1_row_follower.py) pointed at the action table, registry slot 02EBF138.
Its seed list is every function that references the slot by rip (129, derived from the image when run).
Original docstring follows.


Tags:  H  = table header pointer (qword load of [02EBF118], or [slot] via a register holding the slot address)
       HC = the dword [H+0xC] (records offset / encoded pointer)
       S  = stride (word [H+8]) and products of it
       R(k) = pointer to a status row + k (k = byte offset inside the row; row index unknown)
       FP(o) = pointer into the current stack frame, entry-relative offset o
Gen:   R(0) = ImageAddress_ResolveRuntimePointer(HC) (0020E600) ; add/lea combining S with anything -> R(0)
Prop:  reg copies, stack spills/reloads (frame-normalised), push/pop, lea/add/sub with immediates, cmov,
       callees receiving tagged args in rcx/rdx/r8/r9 or outgoing stack slots (followed, memoised),
       callees returning R in rax (summaries; their callers image-wide are analysed too).
Report: every memory operand whose base or index carries R(k) -> row offset k+disp, access width;
        H-based operands; stores of R/H to non-stack memory (escapes); calls receiving R.
Usage: python ga1_taint.py [extra function entries...]"""
import struct, sys, re, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM
from pathlib import Path as _P
W = str(_P(__file__).resolve().parents[5] / "Database/Tools/work")
d = open(W + "/exe/FFXII_TZA.exe", "rb").read()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
names = {}; sizes = {}
for line in open(W + "/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: names[int(p[0], 16)] = p[1]; sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
FUNCS = set(names)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
SLOT = 0x02EBF138
RESOLVE = 0x20E600
TEXT_LO, TEXT_HI = 0x121000, 0x121000 + 0x7A0635 + 0x2000  # rough; .text is sec 0/1
IC = {}
def insn(a):
    if a not in IC:
        o = off(a)
        if o is None: IC[a] = None
        else:
            g = next(cs.disasm(d[o:o + 16], a), None); IC[a] = g
    return IC[a]
R64 = {}
for r in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp"):
    for v in ("r" + r, "e" + r, r): R64[v] = "r" + r
for r in ("al", "bl", "cl", "dl"): R64[r] = "r" + r[0] + "x"
for r in ("sil", "dil", "bpl", "spl"): R64[r] = "r" + r[:2]
for i in range(8, 16):
    for s in ("", "d", "w", "b"): R64["r%d%s" % (i, s)] = "r%d" % i
def c64(name): return R64.get(name, name)
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ARGS = ("rcx", "rdx", "r8", "r9")

# ---------- CFG ----------
def jt_targets(blk, prev=()):
    """blk = list of insns ending in jmp reg; decode an image-base-relative jump table (prev = earlier insns)."""
    tbl = None; cnt = None; btbl = None; bcnt = None
    for y in list(reversed(blk[:-1])) + list(reversed(list(prev)))[:12]:
        for o in y.operands:
            if o.type == X86_OP_MEM and o.mem.index != 0:
                if o.mem.scale == 4 and o.mem.disp > 0x1000 and tbl is None: tbl = BASE + o.mem.disp
                elif o.mem.scale == 1 and o.size == 1 and o.mem.disp > 0x1000 and btbl is None: btbl = BASE + o.mem.disp
        if y.mnemonic == "cmp" and len(y.operands) == 2 and y.operands[1].type == X86_OP_IMM and cnt is None:
            cnt = y.operands[1].imm + 1
    if tbl is None or cnt is None or cnt > 4096: return []
    if btbl is not None:
        o = off(btbl)
        if o is None: return []
        cnt = max(d[o:o + cnt]) + 1
    o = off(tbl)
    if o is None: return []
    out = []
    for i in range(cnt):
        t = BASE + struct.unpack_from("<I", d, o + 4 * i)[0]
        if TEXT_LO <= t < TEXT_HI: out.append(t)
    return out


_LINES = None
def _all_lines():
    """every listed function's instructions as 'ADDR FUNC mnemonic operands ; =>RIPTARGET' lines, built once from the image"""
    global _LINES
    if _LINES is None:
        _LINES = []
        _cs = Cs(CS_ARCH_X86, CS_MODE_64)
        for _f in sorted(sizes):
            if not (0x121000 <= _f < 0x8C0000) or sizes[_f] <= 0: continue
            _o = off(_f)
            if _o is None: continue
            for _x in _cs.disasm(d[_o:_o + sizes[_f]], _f):
                _m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", _x.op_str)
                _t = ""
                if _m:
                    _t = " ; =>%08X" % (_x.address + _x.size + (int(_m.group(2), 16) if _m.group(1) == "+" else -int(_m.group(2), 16)))
                _LINES.append("%08X %08X %s %s%s" % (_x.address, _f, _x.mnemonic, _x.op_str, _t))
    return _LINES
CFGC = {}
ROOTS = collections.defaultdict(set)
for _line in _all_lines():
    if "=>02EBF138" in _line:
        _p = _line.split(); ROOTS[int(_p[1], 16)].add(int(_p[0], 16))
def cfg(entry):
    """blocks: start -> (insn list, successors). Direct jmp to another known function entry = tail call."""
    if entry in CFGC: return CFGC[entry]
    starts = {entry}; work = [entry]; seen = set(); edges = {}
    blocks = {}
    # first pass: discover leaders
    todo = [entry] + list(ROOTS.get(entry, ())); visited = set()
    leaders = {entry} | set(ROOTS.get(entry, ()))
    while todo:
        a = todo.pop()
        if a in visited: continue
        visited.add(a)
        while True:
            x = insn(a)
            if x is None: break
            m = x.mnemonic
            if m == "ret" or m == "int3" or m == "ud2": break
            if m == "jmp":
                o = x.operands[0]
                if o.type == X86_OP_IMM:
                    t = o.imm
                    if t in FUNCS and t != entry: break  # tail call
                    leaders.add(t); todo.append(t); break
                # indirect
                break
            if m.startswith("j") or m.startswith("loop"):
                o = x.operands[0]
                if o.type == X86_OP_IMM:
                    leaders.add(o.imm); todo.append(o.imm)
                leaders.add(x.address + x.size); todo.append(x.address + x.size); break
            a = x.address + x.size
            if a in leaders: todo.append(a); break
    # jump tables need block contents: iterate until stable
    changed = True
    while changed:
        changed = False
        blocks = {}
        for L in sorted(leaders):
            a = L; lst = []
            while True:
                x = insn(a)
                if x is None: break
                lst.append(x); a = x.address + x.size
                m = x.mnemonic
                if m in ("ret", "int3", "ud2") or m == "jmp" or m.startswith("j") or m.startswith("loop") or a in leaders: break
            succ = []
            if lst:
                x = lst[-1]; m = x.mnemonic
                if m in ("ret", "int3", "ud2"): pass
                elif m == "jmp":
                    o = x.operands[0]
                    if o.type == X86_OP_IMM:
                        if not (o.imm in FUNCS and o.imm != entry): succ.append(o.imm)
                    elif o.type == X86_OP_REG:
                        prev = [y for L2 in sorted(blocks) if L2 < L for y in blocks[L2][0]][-12:]
                        for t in jt_targets(lst, prev):
                            succ.append(t)
                            if t not in leaders: leaders.add(t); changed = True
                elif m.startswith("j") or m.startswith("loop"):
                    o = x.operands[0]
                    if o.type == X86_OP_IMM: succ.append(o.imm)
                    succ.append(a)
                else: succ.append(a)
            blocks[L] = (lst, succ)
        # newly added leaders may need discovery of their own successors
        if changed:
            todo = [l for l in leaders if l not in visited]
            while todo:
                a = todo.pop()
                if a in visited: continue
                visited.add(a)
                while True:
                    x = insn(a)
                    if x is None: break
                    m = x.mnemonic
                    if m in ("ret", "int3", "ud2"): break
                    if m == "jmp":
                        o = x.operands[0]
                        if o.type == X86_OP_IMM and not (o.imm in FUNCS and o.imm != entry):
                            leaders.add(o.imm); todo.append(o.imm)
                        break
                    if m.startswith("j") or m.startswith("loop"):
                        o = x.operands[0]
                        if o.type == X86_OP_IMM: leaders.add(o.imm); todo.append(o.imm)
                        leaders.add(x.address + x.size); todo.append(x.address + x.size); break
                    a = x.address + x.size
                    if a in leaders: todo.append(a); break
    CFGC[entry] = blocks
    return blocks

# ---------- taint ----------
ACCESS = collections.OrderedDict()   # (addr) -> record
ESCAPE = {}; CALLR = {}; HACC = {}
RET_SUMMARY = {}                      # func -> set of R tags returned in rax (from empty entry state)
ANALYSED = {}
FOLLOW_DEPTH = 7

def regname(r): return c64(cs.reg_name(r)) if r else None

def memloc(o, st):
    """stack slot key for a memory operand, or None."""
    b = regname(o.mem.base)
    if o.mem.index: return None
    if b == "rsp": return ("stk", o.mem.disp - st["_d"])
    if b:
        for t in st.get(b, ()):
            if t[0] == "FP": return ("stk", t[1] + o.mem.disp)
    return None

def tags_of(st, r): return st.get(r, frozenset())

def analyse(func, init, depth, why):
    key = (func, frozenset((k, frozenset(v) if isinstance(v, (set, frozenset)) else v) for k, v in init.items()))
    if key in ANALYSED: return ANALYSED[key]
    ANALYSED[key] = frozenset()   # recursion guard
    blocks = cfg(func)
    if func not in blocks: return frozenset()
    IN = {func: dict(init)}
    IN[func].setdefault("_d", 0)
    work = [func]; rets = set(); iters = 0
    pending_roots = [r for r in ROOTS.get(func, ()) if r in blocks]
    while work or pending_roots:
        iters += 1
        if iters > 40000: break
        if not work:
            r = pending_roots.pop(0)
            if r in IN: continue
            IN[r] = {"_d": 0}; work.append(r)
        b = work.pop(0)
        st = {k: (set(v) if k != "_d" else v) for k, v in IN[b].items()}
        lst, succ = blocks[b]
        for x in lst:
            step(func, x, st, depth, why, rets)
        for s in succ:
            if s not in blocks: continue
            old = IN.get(s)
            if old is None:
                IN[s] = {k: (set(v) if k != "_d" else v) for k, v in st.items()}; work.append(s); continue
            ch = False
            for k, v in st.items():
                if k == "_d":
                    continue
                if not v <= old.get(k, set()):
                    old.setdefault(k, set()).update(v); ch = True
            if ch and s not in work: work.append(s)
    res = frozenset(rets)
    ANALYSED[key] = res
    return res

def rec_access(func, x, o, t, why, note=""):
    k = t[1]
    ro = None if k is None else k + o.mem.disp
    ACCESS.setdefault((x.address, ro), dict(func=func, addr=x.address, text="%s %s" % (x.mnemonic, x.op_str),
                      off=ro, width=o.size, index=bool(o.mem.index), why=why, note=note))

def step(func, x, st, depth, why, rets):
    m = x.mnemonic; ops = x.operands
    # 1) record accesses through tagged bases
    for o in ops:
        if o.type != X86_OP_MEM: continue
        b = regname(o.mem.base); ix = regname(o.mem.index)
        for r, role in ((b, "base"), (ix, "index")):
            if not r or r == "rip": continue
            for t in tags_of(st, r):
                if t[0] == "R": rec_access(func, x, o, t, why, role if role == "index" else "")
                elif t[0] == "H":
                    HACC.setdefault(x.address, (func, "%s %s" % (m, x.op_str), o.mem.disp, o.size))
    # rsp bookkeeping
    if m == "push":
        st["_d"] += 8
        o = ops[0]
        if o.type == X86_OP_REG: st[("stk", -st["_d"])] = set(tags_of(st, regname(o.reg)))
        return
    if m == "pop":
        o = ops[0]; v = st.pop(("stk", -st["_d"]), set())
        st["_d"] -= 8
        if o.type == X86_OP_REG: st[regname(o.reg)] = set(v)
        return
    if m in ("sub", "add") and ops and ops[0].type == X86_OP_REG and regname(ops[0].reg) == "rsp" and ops[1].type == X86_OP_IMM:
        st["_d"] += ops[1].imm if m == "sub" else -ops[1].imm; return
    if m == "call":
        o = ops[0]
        tgt = o.imm if o.type == X86_OP_IMM else None
        argst = {r: tags_of(st, r) for r in ARGS}
        ret = set()
        if tgt == RESOLVE:
            if any(t[0] == "HC" for t in argst["rcx"]): ret.add(("R", 0))
        elif tgt is not None and tgt in FUNCS:
            init = {}
            for r in ARGS:
                v = {t for t in argst[r] if t[0] in ("R", "H", "S", "HC")}
                if v: init[r] = v
            # outgoing stack args: caller [rsp+0x20+8k] -> callee entry-relative +0x28+8k (after return address)
            for k2, v in list(st.items()):
                if isinstance(k2, tuple) and k2[0] == "stk":
                    rel = k2[1] + st["_d"]           # rsp-relative in caller
                    if 0x20 <= rel < 0x80:
                        vv = {t for t in v if t[0] in ("R", "H")}
                        if vv: init[("stk", rel + 8)] = vv
            if any(t[0] == "R" for v in init.values() for t in v):
                CALLR.setdefault((x.address, tgt), (func, sorted({str(r) for r, v in init.items() if any(t[0] == "R" for t in v)})))
            if init and depth > 0:
                ret |= analyse(tgt, init, depth - 1, why + ">%08X" % tgt)
            if tgt in RET_SUMMARY: ret |= RET_SUMMARY[tgt]
        for r in VOL: st.pop(r, None)
        if ret: st["rax"] = set(ret)
        return
    if m == "ret":
        rets.update(t for t in tags_of(st, "rax") if t[0] == "R"); return
    if m == "jmp" and ops[0].type == X86_OP_IMM and ops[0].imm in FUNCS and ops[0].imm != func:
        # tail call: treat as call + ret
        tgt = ops[0].imm
        init = {}
        for r in ARGS:
            v = {t for t in tags_of(st, r) if t[0] in ("R", "H", "S", "HC")}
            if v: init[r] = v
        ret = set()
        if init and depth > 0: ret |= analyse(tgt, init, depth - 1, why + ">%08X" % tgt)
        if any(t[0] == "R" for v in init.values() for t in v):
            CALLR.setdefault((x.address, tgt), (func, sorted({str(r) for r, v in init.items() if any(t[0] == "R" for t in v)})))
        if tgt in RET_SUMMARY: ret |= RET_SUMMARY[tgt]
        rets.update(t for t in ret if t[0] == "R"); return
    if not ops: return
    dst = ops[0]
    def src_tags(o):
        if o.type == X86_OP_REG: return set(tags_of(st, regname(o.reg)))
        if o.type == X86_OP_MEM:
            b = regname(o.mem.base)
            if b == "rip":
                if x.address + x.size + o.mem.disp == SLOT and o.size == 8: return {("H", 0)}
                return set()
            loc = memloc(o, st)
            if loc is not None: return set(st.get(loc, ()))
            out = set()
            for t in tags_of(st, b):
                if t[0] == "H" and o.mem.disp == 8 and o.size == 2: out.add(("S", 0))
                if t[0] == "H" and o.mem.disp == 0xC and o.size == 4: out.add(("HC", 0))
                if t[0] == "SLOTP" and o.mem.disp == 0 and o.size == 8: out.add(("H", 0))
            return out
        return set()
    def setdst(v):
        if dst.type == X86_OP_REG:
            r = regname(dst.reg)
            if v: st[r] = set(v)
            else: st.pop(r, None)
        elif dst.type == X86_OP_MEM:
            loc = memloc(dst, st)
            if loc is not None:
                if v and dst.size >= 4: st[loc] = set(v)
                else: st.pop(loc, None)
            elif v and any(t[0] in ("R", "H") for t in v):
                ESCAPE.setdefault(x.address, (func, "%s %s" % (m, x.op_str), sorted(map(str, v)), why))
    if m in ("mov", "movsxd", "movzx", "movsx", "movq", "movabs"):
        v = src_tags(ops[1])
        if m in ("movzx", "movsx") and ops[1].size < 2: v = set()
        if m in ("movzx",) and ops[1].size == 2: v = {t for t in v if t[0] == "S"}
        setdst(v); return
    if m.startswith("cmov"):
        v = src_tags(ops[1])
        if dst.type == X86_OP_REG:
            r = regname(dst.reg); st[r] = set(tags_of(st, r)) | v
            if not st[r]: st.pop(r)
        return
    if m == "lea":
        o = ops[1]; b = regname(o.mem.base); ix = regname(o.mem.index)
        if b == "rip":
            t = x.address + x.size + o.mem.disp
            setdst({("SLOTP", 0)} if t == SLOT else set()); return
        if b == "rsp" and not ix: setdst({("FP", o.mem.disp - st["_d"])}); return
        out = set()
        bt = tags_of(st, b) if b else set(); it = tags_of(st, ix) if ix else set()
        for t in bt:
            if t[0] == "R": out.add(("R", None if t[1] is None else t[1] + o.mem.disp))
            if t[0] == "FP" and not ix: out.add(("FP", t[1] + o.mem.disp))
        if o.mem.scale == 1:
            for t in it:
                if t[0] == "R": out.add(("R", None if t[1] is None else t[1] + o.mem.disp))
        if any(t[0] == "S" for t in bt | it) and ix: out.add(("R", o.mem.disp))
        setdst(out); return
    if m in ("add", "sub"):
        if dst.type == X86_OP_REG:
            r = regname(dst.reg); cur = set(tags_of(st, r)); s = ops[1]
            out = set()
            if s.type == X86_OP_IMM:
                imm = s.imm if m == "add" else -s.imm
                for t in cur:
                    if t[0] == "R": out.add(("R", None if t[1] is None else t[1] + imm))
                    elif t[0] == "FP": out.add(("FP", t[1] + imm))
                    elif t[0] == "S": out.add(t)
            else:
                sv = src_tags(s)
                if m == "add":
                    for t in cur | sv:
                        if t[0] == "R": out.add(t)
                    if any(t[0] == "S" for t in cur | sv): out.add(("R", 0))
                else:
                    for t in cur:
                        if t[0] == "R": out.add(t)
            setdst(out); return
        return  # memory destination: value arithmetic
    if m == "imul":
        v = set()
        for o in ops:
            v |= {t for t in src_tags(o) if t[0] == "S"} if o.type != X86_OP_IMM else set()
        setdst(v); return
    if m in ("shl", "sal") and dst.type == X86_OP_REG:
        setdst({t for t in tags_of(st, regname(dst.reg)) if t[0] == "S"}); return
    if m == "xchg" and all(o.type == X86_OP_REG for o in ops):
        a, b2 = regname(ops[0].reg), regname(ops[1].reg)
        va, vb = st.get(a), st.get(b2)
        st.pop(a, None); st.pop(b2, None)
        if vb: st[a] = vb
        if va: st[b2] = va
        return
    # generic: kill written registers
    try:
        _, wr = x.regs_access()
        for r in wr:
            n = regname(r)
            if n and n != "rsp" and n in st: st.pop(n)
    except Exception:
        if dst.type == X86_OP_REG: st.pop(regname(dst.reg), None)

SRC18 = sorted({int(_l.split()[1], 16) for _l in _all_lines() if '=>02EBF138' in _l})

def callers_of(t):
    pat = re.compile(r" (?:call|jmp) 0x%x\b" % t)
    out = set()
    for line in _all_lines():
        if pat.search(line):
            p = line.split(); out.add(int(p[1], 16))
    return out

if __name__ == "__main__":
    extra = [int(a, 16) for a in sys.argv[1:]]
    todo = list(SRC18) + extra
    done = set(); rounds = 0
    while todo and rounds < 6:
        rounds += 1
        new_accessors = []
        for f in todo:
            if f in done: continue
            done.add(f)
            r = analyse(f, {}, FOLLOW_DEPTH, "%08X" % f)
            if r:
                if RET_SUMMARY.get(f) != r:
                    RET_SUMMARY[f] = set(RET_SUMMARY.get(f, set())) | set(r); new_accessors.append(f)
        # functions returning R from a tagged-argument analysis also count as accessors
        for (fn, _k), r in list(ANALYSED.items()):
            pass
        todo = []
        for a in new_accessors:
            cl = callers_of(a)
            print("accessor %08X returns %s; callers %d" % (a, sorted(map(str, RET_SUMMARY[a])), len(cl)))
            for c in cl:
                if c in done: done.discard(c)
                todo.append(c)
        if todo:
            ANALYSED.clear()
    print("functions analysed from entry:", len(done))
    # also: analyses with tagged args that returned R -> 'passthrough' accessors
    pt = sorted({k[0] for k, v in ANALYSED.items() if v and k[1]})
    print("pass-through (returns R when given R/H):", " ".join("%08X" % a for a in pt))
    print("\n== row accesses (offset, width) ==")
    for (a, ro), r in sorted(ACCESS.items(), key=lambda kv: (kv[1]["off"] if kv[1]["off"] is not None else 999, kv[0][0])):
        print("%s w%d %08X in %08X %-40s %s %s" % ("off?" if ro is None else "+0x%02X" % ro, r["width"], a, r["func"],
              r["text"], r["note"], r["why"]))
    print("\n== H-based operands ==")
    for a, v in sorted(HACC.items()): print("%08X in %08X %s disp=0x%x w%d" % (a, v[0], v[1], v[2], v[3]))
    print("\n== calls receiving R ==")
    for (a, t), v in sorted(CALLR.items()): print("%08X in %08X -> %08X %s args %s" % (a, v[0], t, names.get(t, ""), v[1]))
    print("\n== escapes (R/H stored to non-stack memory) ==")
    for a, v in sorted(ESCAPE.items()): print("%08X in %08X %s tags %s via %s" % (a, v[0], v[1], v[2], v[3]))
