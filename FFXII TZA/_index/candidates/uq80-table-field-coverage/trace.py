# trace.py - UQ-80 reader sweep (flow-aware "may" analysis).
# For each slot: every function that loads it rip-relative (from the y1p_all.txt instruction cache), then a
# worklist dataflow over each function's CFG (direct jumps + fallthrough; tags UNION at joins) with register tags:
#   T = table descriptor (value of qword [slot]); O = dword [T+0xC] (row-area offset); W = word [T+8] (stride);
#   R = rows base (0020E600(O), T+O, or T+0x20); P = W*idx; X = a record pointer (R+P, R+idx, lea over R/X).
# Every memory operand whose base or index may carry R or X is printed ("rec") with its access width, disp and text;
# operands based on T are printed as "hdr".
# Accessors (functions whose rax may be R/X at a ret) found in pass 1 seed rax=X at their call sites in pass 2,
# including callers that never load the slot. Stack spills ([rsp+N]) of tagged registers are tracked.
# Limits: indirect jumps (switch tables) are not followed; a record pointer passed in a register to a non-accessor
# callee is not followed into the callee (reported as "arg" lines so it can be read by hand).
import sys, struct, re, collections, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(HERE)
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0]))
def off(addr):
    r = addr - BASE
    for va, vs, ro in secs:
        if va <= r < va + vs: return ro + (r - va)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

FUNC_INS = collections.defaultdict(list)
SLOTREF = collections.defaultdict(set)
CALLS = collections.defaultdict(set)
for line in open(os.path.join(SCR, "y1p_all.txt"), encoding="utf-8", errors="replace"):
    p = line.split(" ", 3)
    if len(p) < 3: continue
    a = int(p[0], 16); f = int(p[1], 16)
    FUNC_INS[f].append(a)
    m = re.search(r"=>(02EBF[0-9A-F]{3})", line)
    if m: SLOTREF[m.group(1)].add(f)
    if p[2] == "call" and len(p) > 3:
        m = re.match(r"0x([0-9a-f]+)\s*$", p[3].strip())
        if m: CALLS[int(m.group(1), 16)].add(f)

_cache = {}
def dis1(a):
    if a in _cache: return _cache[a]
    o = off(a); r = None
    for x in md.disasm(d[o:o + 16], a, 1): r = x
    _cache[a] = r
    return r

FAM = {}
for fam in [("rax","eax","ax","al"),("rbx","ebx","bx","bl"),("rcx","ecx","cx","cl"),("rdx","edx","dx","dl"),
            ("rsi","esi","si","sil"),("rdi","edi","di","dil"),("rbp","ebp","bp","bpl"),("rsp","esp","sp","spl")] + \
           [tuple("r%d%s" % (i, s) for s in ("", "d", "w", "b")) for i in range(8, 16)]:
    for r in fam: FAM[r] = fam[0]
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
PTR = {"R", "X"}
def isptr(t): return t == "R" or t.startswith("X")
def anyptr(ts): return any(isptr(t) for t in ts)
def xoff(t):
    # "X+n" -> (n, False); "X*n" -> (n, True) (a strided walk starting at n); "R" -> (None, False)
    if t.startswith("X+"): return int(t[2:]), False
    if t.startswith("X*"): return int(t[2:]), True
    return None, False
def shift(ts, k):
    out = set()
    for t in ts:
        if t.startswith("X+"): out.add("X+%d" % (int(t[2:]) + k))
        elif t.startswith("X*"): out.add(t)
        elif t == "R": out.add("X+%d" % k)   # rows base + constant: row 0 / offset k, reported as such
        else: out.add(t)
    return out
def widen(ts):
    xs = sorted(xoff(t)[0] for t in ts if t.startswith("X"))
    if len(set(xs)) > 1 or (xs and any(t.startswith("X*") for t in ts)):
        ts = {t for t in ts if not t.startswith("X")} | {"X*%d" % min(xs)}
    return ts
ARGREGS = ("rcx", "rdx", "r8", "r9")

def trace_func(f, slot_va, accessors, out):
    addrs = sorted(FUNC_INS.get(f, []))
    if not addrs: return False
    ins = {a: dis1(a) for a in addrs}
    ins = {a: x for a, x in ins.items() if x is not None}
    order = sorted(ins)
    nxt = {order[i]: order[i + 1] for i in range(len(order) - 1)}
    IN = {order[0]: ({}, {})}
    work = [order[0]]
    ret_ptr = False
    final = {}
    def rn(x, r): return FAM.get(x.reg_name(r), x.reg_name(r)) if r else None
    unvisited = list(order)
    while True:
        if not work:
            # seed instructions no direct edge reached (switch arms behind indirect jumps) with an empty state
            while unvisited and unvisited[-1] in IN: unvisited.pop()
            cand = [u for u in unvisited if u not in IN]
            if not cand: break
            u = cand[0]; IN[u] = ({}, {}); work.append(u)
            unvisited = cand
        a = work.pop()
        regs, stk = IN[a]
        regs = {k: set(v) for k, v in regs.items()}; stk = {k: set(v) for k, v in stk.items()}
        x = ins[a]; ops = x.operands; mn = x.mnemonic; text = "%s %s" % (mn, x.op_str)
        def tags(op):
            if op.type == X86_OP_REG: return set(regs.get(rn(x, op.reg), ()))
            if op.type == X86_OP_MEM:
                b = rn(x, op.mem.base)
                if b == "rip":
                    return {"T"} if (a + x.size + op.mem.disp == slot_va and op.size == 8) else set()
                if b == "rsp" and not op.mem.index: return set(stk.get(op.mem.disp, ()))
                bt = regs.get(b, set())
                s = set()
                if "T" in bt and op.mem.disp == 0xC: s.add("O")
                if "T" in bt and op.mem.disp == 8: s.add("W")
                return s
            return set()
        # report memory operands
        if mn != "lea" and not mn.startswith("nop"):
            for o in ops:
                if o.type != X86_OP_MEM: continue
                b = rn(x, o.mem.base); ix = rn(x, o.mem.index)
                bt = regs.get(b, set()) if b not in (None, "rip") else set()
                it = regs.get(ix, set()) if ix else set()
                kind = "rec" if (anyptr(bt) or anyptr(it)) else ("hdr" if "T" in bt else None)
                if kind:
                    key = (a, kind)
                    if True:
                        # row offset = pointer offset + disp, for each pointer tag the operand may carry
                        offs = []
                        for t in sorted(bt | it):
                            if not isptr(t): continue
                            n, walk = xoff(t)
                            if t == "R": offs.append("R%+d" % o.mem.disp)
                            elif walk: offs.append("walk>=%d" % (n + o.mem.disp))
                            else: offs.append("%d" % (n + o.mem.disp))
                        final[key] = (f, a, o.size, o.mem.disp, "".join(sorted(bt)) or "-", "".join(sorted(it)) or "-", o.mem.scale, text, kind, ",".join(offs))
        succ = []
        is_jmp = mn == "jmp"; is_j = mn.startswith("j")
        if is_j and ops and ops[0].type == X86_OP_IMM and ops[0].imm in ins: succ.append(ops[0].imm)
        if not is_jmp and mn not in ("ret", "int3", "ud2") and a in nxt: succ.append(nxt[a])
        # transfer
        if mn == "call":
            tgt = ops[0].imm if ops and ops[0].type == X86_OP_IMM else None
            rcx = regs.get("rcx", set())
            argtags = [(r, regs.get(r, set())) for r in ARGREGS if anyptr(regs.get(r, set()))]
            if argtags:
                key = (a, "arg")
                if True:
                    final[key] = ((f, a, 0, 0, ",".join(r + ":" + "".join(sorted(t)) for r, t in argtags), "-", 0, text, "arg", ""))
            for r in VOL: regs.pop(r, None)
            if tgt == 0x20E600 and "O" in rcx: regs["rax"] = {"R"}
            elif tgt in accessors: regs["rax"] = {"X+0"}
        elif mn == "ret":
            if anyptr(regs.get("rax", set())): ret_ptr = True
        elif is_j or mn in ("cmp", "test", "push", "nop", "int3"):
            pass
        elif ops and ops[0].type == X86_OP_MEM:
            dst = ops[0]
            if rn(x, dst.mem.base) == "rsp" and not dst.mem.index:
                if len(ops) > 1 and ops[1].type == X86_OP_REG and regs.get(rn(x, ops[1].reg)):
                    stk[dst.mem.disp] = set(regs[rn(x, ops[1].reg)])
                else: stk.pop(dst.mem.disp, None)
        elif ops and ops[0].type == X86_OP_REG:
            dr = rn(x, ops[0].reg); src = ops[1] if len(ops) > 1 else None
            if mn in ("mov", "movzx", "movsxd", "movsx"):
                t = tags(src)
                if t: regs[dr] = t
                else: regs.pop(dr, None)
            elif mn.startswith("cmov"):
                t = tags(src) | regs.get(dr, set())
                if t: regs[dr] = t
            elif mn == "lea":
                b = rn(x, src.mem.base); ix = rn(x, src.mem.index)
                bt = regs.get(b, set()); it = regs.get(ix, set()) if ix else set()
                t = set()
                if anyptr(bt) and not ix: t |= {x_ for x_ in shift({q for q in bt if isptr(q)}, src.mem.disp)}
                elif anyptr(bt) or anyptr(it):
                    # pointer plus an index register: the offset is only known when the other side is a stride product
                    other = it if anyptr(bt) else bt
                    ptrs = {q for q in (bt if anyptr(bt) else it) if isptr(q)}
                    if "P" in other or ptrs == {"R"}: t |= {"X+%d" % src.mem.disp}
                    else: t |= {"X*%d" % (min([xoff(q)[0] or 0 for q in ptrs]) + src.mem.disp)}
                if "T" in bt and src.mem.disp == 0x20 and not ix: t.add("R")
                if t: regs[dr] = t
                else: regs.pop(dr, None)
            elif mn == "imul":
                t = set()
                for o in ops: t |= tags(o)
                if "W" in t: regs[dr] = {"P"}
                else: regs.pop(dr, None)
            elif mn == "add":
                td = regs.get(dr, set()); ts = tags(src) if src is not None else set()
                t = set()
                if src is not None and src.type == X86_OP_IMM and anyptr(td):
                    t |= shift({q for q in td if isptr(q)}, src.imm)
                elif anyptr(td) or anyptr(ts):
                    ptrs = {q for q in (td | ts) if isptr(q)}
                    other = ts if anyptr(td) else td
                    if ptrs == {"R"} and ("P" in other or not other): t.add("X+0")
                    elif "P" in other: t |= shift(ptrs - {"R"}, 0) | ({"X+0"} if "R" in ptrs else set())
                    else: t |= {"X*%d" % min([xoff(q)[0] or 0 for q in ptrs])}
                if ("T" in td and "O" in ts) or ("O" in td and "T" in ts): t.add("R")
                if not t and ("P" in td or "P" in ts): t.add("P")
                if t: regs[dr] = t
                else: regs.pop(dr, None)
            elif mn == "sub" and src is not None and src.type == X86_OP_IMM and anyptr(regs.get(dr, set())):
                regs[dr] = shift({q for q in regs[dr] if isptr(q)}, -src.imm)
            elif mn == "inc" and anyptr(regs.get(dr, set())):
                regs[dr] = shift({q for q in regs[dr] if isptr(q)}, 1)
            elif mn == "xchg" and src is not None and src.type == X86_OP_REG:
                s = rn(x, src.reg); a1, b1 = regs.get(dr), regs.get(s)
                regs.pop(dr, None); regs.pop(s, None)
                if b1: regs[dr] = b1
                if a1: regs[s] = a1
            else:
                regs.pop(dr, None)
        # propagate (union)
        for s in succ:
            if s not in IN:
                IN[s] = ({k: set(v) for k, v in regs.items()}, {k: set(v) for k, v in stk.items()}); work.append(s)
            else:
                r0, s0 = IN[s]; changed = False
                for k, v in regs.items():
                    if not v <= r0.get(k, set()):
                        nv = widen(r0.get(k, set()) | v)
                        if nv != r0.get(k): r0[k] = nv; changed = True
                for k, v in stk.items():
                    if not v <= s0.get(k, set()):
                        nv = widen(s0.get(k, set()) | v)
                        if nv != s0.get(k): s0[k] = nv; changed = True
                if changed: work.append(s)
    for k in sorted(final): out.append(final[k])
    return ret_ptr

def sweep(slot, extra_funcs=()):
    slot_va = int(slot, 16)
    funcs = sorted((SLOTREF.get(slot, set()) - {0x236C30}) | set(extra_funcs))
    accessors = set()
    for f in funcs:
        if trace_func(f, slot_va, set(), []): accessors.add(f)
    todo = set(funcs)
    for acc in accessors: todo |= CALLS.get(acc, set())
    out = []
    for f in sorted(todo): trace_func(f, slot_va, accessors, out)
    return funcs, accessors, todo, out

def fmt(r):
    f, a, sz, disp, bt, it, sc, text, kind, offs = r
    if kind == "arg": return "arg %08X %08X passes %s  %s" % (f, a, bt, text)
    return "%s %08X %08X w%d disp=%s rowoff=%s base=%s idx=%s*%d  %s" % (kind, f, a, sz, hex(disp), offs or "-", bt, it, sc, text)

if __name__ == "__main__":
    for slot in sys.argv[1:]:
        funcs, acc, todo, out = sweep(slot)
        print("== slot", slot, "loading funcs:", " ".join("%08X" % f for f in funcs))
        print("accessors:", " ".join("%08X" % f for f in sorted(acc)) or "-", "| traced funcs:", len(todo))
        for r in out: print(fmt(r))
