"""rc8_flow.py - RC-8 (ORACLE, 2026-09-30).  Where can the shadow object's pointer go, and does any code holding it write
its +0x13C cascade count?

The object: 0xB08 bytes, allocated and constructed (001EF2D0) only by the four get-or-create functions 001F0810,
001F0850, 001F1590, 001F1600, which publish it in the global 01F82EA8 (the only rip references to that cell are in
those four).  This script runs a forward pointer-flow (taint) analysis seeded at every place the pointer appears:
  - every load of 01F82EA8 (mov reg, [rip -> 01F82EA8]);
  - the return value (rax) at every call or tail jump to one of the four creators;
  - the constructor 001EF2D0 entered with rcx = the object (positive control: must report its store 001EF389).
Per function, a may-analysis over the basic-block graph (union at joins) tracks which registers and which [rsp+d]
stack slots hold "object + offset" (offset sets, 'var' when an index register is added).  At every instruction:
  - a memory access through a tainted base is recorded with its object offset (offset + disp) and width;
    a WRITE whose byte range covers +0x13C..+0x13F is reported as a count write;
  - a store of a tainted register to memory whose base is not rsp (and not the object itself) is an ESCAPE;
  - a call/tail jump with tainted rcx/rdx/r8/r9 is followed into the callee with that entry state (memoised); a tainted
    outgoing stack argument ([rsp+0x20..]) before a call, or tainted argument registers at an indirect call, is an
    ESCAPE for manual reading;
  - after a call, the volatile registers are cleared, except rax when the callee's own analysis returns the pointer.
Output rc8_flow.tsv (every function reached, how, the object offsets it touches, count writes, escapes) and a summary.
Blind spots, stated: a pointer that leaves through an ESCAPE is not followed further (each escape is listed for manual
reading); flags-only and SIMD register copies of the pointer are not tracked (movq xmm, reg is listed as an escape)."""
import collections, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP, X86_REG_RSP

HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = {0x01F82EA8}
CREATORS = {0x001F0810, 0x001F0850, 0x001F1590, 0x001F1600}
CTOR = 0x001EF2D0
ARGS = ("rcx", "rdx", "r8", "r9")
VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
R64 = {}
for full, subs in {"rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh",
                   "rsi": "esi si sil", "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    R64[full] = full
    for s in subs.split():
        R64[s] = full
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        R64["r%d%s" % (n, suf)] = "r%d" % n


def norm(x, r):
    return R64.get(x.reg_name(r))


BODY = {}


def body(root):
    if root not in BODY:
        ins = img.fn_ins(root) if img.fragments(root) else []
        if not ins:                                   # leaf without .pdata: decode to the first ret/jmp
            ins = []
            va = root
            for _ in range(400):
                x = img.dis(va, 16)
                if not x:
                    break
                x = x[0]; ins.append(x); va = x.address + x.size
                if x.mnemonic in ("ret", "jmp", "int3"):
                    break
        BODY[root] = ins
    return BODY[root]


def resolve(t):
    """follow a 5-byte jmp thunk chain to its target."""
    for _ in range(4):
        x = img.dis(t, 16)
        if x and x[0].mnemonic == "jmp" and x[0].operands[0].type == X86_OP_IMM and x[0].size == 5:
            t = x[0].operands[0].imm
        else:
            break
    return t


REPORT = collections.OrderedDict()   # root -> dict
MEMO = {}
QUEUE = []


def add(lst, item):
    if item not in lst:
        lst.append(item)


def rep(root):
    return REPORT.setdefault(root, {"how": set(), "offs": collections.Counter(), "count_writes": [], "escapes": [],
                                    "callees": set(), "returns_ptr": False})


def analyse(root, entry, how):
    key = (root, frozenset((k, frozenset(v)) for k, v in entry.items()))
    rep(root)["how"].add(how)
    if key in MEMO:
        return MEMO[key]
    MEMO[key] = False
    ins = body(root)
    if not ins:
        return False
    idx = {x.address: i for i, x in enumerate(ins)}
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    succ = collections.defaultdict(list)
    leaders = {ins[0].address}
    for i, x in enumerate(ins):
        m = x.mnemonic
        nxt = ins[i + 1].address if i + 1 < len(ins) else None
        if m.startswith("j"):
            if x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm in idx:
                succ[x.address].append(x.operands[0].imm); leaders.add(x.operands[0].imm)
            if m != "jmp" and nxt:
                succ[x.address].append(nxt)
            if nxt:
                leaders.add(nxt)
        elif m in ("ret", "int3"):
            if nxt:
                leaders.add(nxt)
        elif nxt:
            succ[x.address].append(nxt)
    state_in = {ins[0].address: {k: set(v) for k, v in entry.items()}}
    work = [ins[0].address]
    returns = False
    seen_iter = 0
    while work and seen_iter < 20000:
        seen_iter += 1
        a = work.pop()
        st = {k: set(v) for k, v in state_in[a].items()}
        i = idx[a]
        while True:
            x = ins[i]
            returns |= step(root, x, st)
            outs = succ.get(x.address, [])
            if x.mnemonic in ("ret",):
                break
            if len(outs) == 1 and outs[0] == (ins[i + 1].address if i + 1 < len(ins) else None) and outs[0] not in leaders:
                i += 1
                continue
            for o in outs:
                old = state_in.get(o)
                if old is None:
                    state_in[o] = {k: set(v) for k, v in st.items()}; work.append(o)
                else:
                    ch = False
                    for k, v in st.items():
                        if not v <= old.get(k, set()):
                            cur = old.setdefault(k, set()); cur.update(v); ch = True
                            if len(cur) > 4:              # widening: a loop-carried pointer becomes (var, lowest offset)
                                low = min(vlo(z) for z in cur)
                                cur.clear(); cur.add(("var", low))
                    if ch:
                        work.append(o)
            break
    MEMO[key] = returns
    rep(root)["returns_ptr"] |= returns
    return returns


import pefile as _pefile
_pe = _pefile.PE(img.EXE)
IAT = {}
for _d in _pe.DIRECTORY_ENTRY_IMPORT:
    for _i in _d.imports:
        IAT[_i.address] = "%s!%s" % (_d.dll.decode(), _i.name.decode() if _i.name else _i.ordinal)
IMPORTS = set()


def import_name(t):
    """name of the import when t is a `jmp qword ptr [rip -> IAT]` thunk, else None."""
    x = img.dis(t, 16)
    if x and x[0].mnemonic == "jmp" and img.ripmem(x[0]) in IAT:
        return IAT[img.ripmem(x[0])]
    return None


def isvar(o):
    return isinstance(o, tuple)


def vlo(o):
    return o[1] if isinstance(o, tuple) else o


FRAMEBP = {}


def framebp(root):
    if root not in FRAMEBP:
        pro = body(root)[:16]
        rax_is_rsp = bool(pro) and pro[0].mnemonic == "mov" and pro[0].op_str == "rax, rsp"
        FRAMEBP[root] = any((x.mnemonic == "lea" and (x.op_str.startswith("rbp, [rsp") or (rax_is_rsp and x.op_str.startswith("rbp, [rax"))))
                            or (x.mnemonic == "mov" and x.op_str == "rbp, rsp") for x in pro)
    return FRAMEBP[root]


CUR = [None]


def memloc(x, o):
    m = o.mem
    if m.base == X86_REG_RSP and m.index == 0:
        return ("stk", m.disp)
    if m.index == 0 and x.reg_name(m.base) == "rbp" and CUR[0] is not None and framebp(CUR[0]):
        return ("bp", m.disp)
    return None


def step(root, x, st):
    """transfer function; returns True if this is a ret with rax tainted."""
    R = rep(root)
    CUR[0] = root
    m = x.mnemonic
    ops = x.operands
    try:
        _r0, w0 = x.regs_access()
    except Exception:
        w0 = []
    keep = norm(x, ops[0].reg) if (m == "add" and ops and ops[0].type == X86_OP_REG) else None
    for r0 in w0:
        n0 = R64.get(x.reg_name(r0))
        if n0 and n0 != keep:
            LB.pop(n0, None)
    if m == "ret":
        return bool(st.get("rax"))
    # memory accesses through a tainted base
    for k, o in enumerate(ops):
        if o.type == X86_OP_MEM and o.mem.base not in (0, X86_REG_RIP, X86_REG_RSP) and memloc(x, o) is None:
            b = norm(x, o.mem.base)
            if st.get(b):
                write = (k == 0 and len(ops) > 1 and m != "lea" and not m.startswith(("cmp", "test", "bt", "ucomis", "comis"))) \
                    or (len(ops) == 1 and m in ("inc", "dec", "not", "neg"))
                for off in st[b]:
                    if isvar(off) or o.mem.index:
                        lo_ = vlo(off) + o.mem.disp
                        if m != "lea":
                            R["offs"]["var>=%X" % lo_] += 1
                        if write and lo_ <= 0x13C + 3:
                            add(R["count_writes"], ("%08X" % x.address, "%s %s" % (m, x.op_str), "indexed, object offset >= %X" % lo_))
                        continue
                    if m == "lea":
                        continue
                    lo_ = off + o.mem.disp; w = o.size or 1
                    R["offs"][lo_] += 1
                    if write and lo_ <= 0x13C < lo_ + w:
                        add(R["count_writes"], ("%08X" % x.address, "%s %s" % (m, x.op_str), "object+%X" % lo_))
    # calls and tail jumps
    if m == "call" or (m == "jmp" and ops and ops[0].type == X86_OP_IMM and not (body(root) and
                                                                                 body(root)[0].address <= ops[0].imm <= body(root)[-1].address)):
        tainted = {a: st[a] for a in ARGS if st.get(a)}
        stk = {k: v for k, v in st.items() if isinstance(k, tuple) and k[0] == "stk" and k[1] >= 0x20 and v}
        if ops and ops[0].type == X86_OP_IMM:
            t = resolve(ops[0].imm)
            rv = False
            if t in CREATORS:
                rv = True
            imp = import_name(t)
            if tainted and imp:
                IMPORTS.add(("%08X" % x.address, imp, ",".join(sorted(tainted))))
            elif tainted:
                R["callees"].add(t)
                rv |= analyse(t, tainted, "arg from %08X" % x.address)
            if stk and m == "call":
                add(R["escapes"], ("%08X" % x.address, "stack argument slot(s) %s to %08X offsets %s" % (sorted(k[1] for k in stk), t, sorted(str(v) for vv in stk.values() for v in vv))))
        else:
            rv = False
            if tainted or stk:
                add(R["escapes"], ("%08X" % x.address, "indirect %s %s with tainted %s offsets %s" % (m, x.op_str, sorted(tainted) + sorted(str(k) for k in stk), sorted(str(v) for vv in list(tainted.values()) + list(stk.values()) for v in vv))))
        for v in VOLATILE:
            st.pop(v, None)
            LB.pop(v, None)
        if rv:
            st["rax"] = {0}
        return False
    # register/stack transfer
    if m in ("mov", "movsxd") and len(ops) == 2:
        d, s = ops
        if d.type == X86_OP_REG and s.type == X86_OP_REG:
            dr, sr = norm(x, d.reg), norm(x, s.reg)
            if x.reg_name(d.reg) == dr and st.get(sr):
                st[dr] = set(st[sr]); return False
            st.pop(dr, None); return False
        if d.type == X86_OP_REG and s.type == X86_OP_MEM:
            dr = norm(x, d.reg)
            loc = memloc(x, s)
            if s.mem.base == X86_REG_RIP and x.address + x.size + s.mem.disp in CELLS:
                st[dr] = {0}; R["how"].add("loads %08X at %08X" % (x.address + x.size + s.mem.disp, x.address)); return False
            if loc and st.get(loc) and x.reg_name(d.reg) == dr:
                st[dr] = set(st[loc]); return False
            st.pop(dr, None); return False
        if d.type == X86_OP_MEM and s.type == X86_OP_REG:
            sr = norm(x, s.reg)
            loc = memloc(x, d)
            if loc:
                if st.get(sr) and x.reg_name(s.reg) == sr:
                    st[loc] = set(st[sr])
                else:
                    st.pop(loc, None)
                return False
            if st.get(sr) and x.reg_name(s.reg) == sr:
                tgt = x.address + x.size + d.mem.disp if d.mem.base == X86_REG_RIP else None
                if tgt is not None and st[sr] == {0}:
                    NEWCELLS.add(tgt)
                if tgt not in CELLS:
                    add(R["escapes"], ("%08X" % x.address, "store of the pointer (offsets %s): %s %s" % (sorted(str(v) for v in st[sr]), m, x.op_str)))
            return False
    if m == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG:
        dr = norm(x, ops[0].reg); s = ops[1]
        b = norm(x, s.mem.base) if s.mem.base not in (0, X86_REG_RIP) else None
        if b and st.get(b):
            st[dr] = {(vlo(o) + s.mem.disp if False else (("var", vlo(o) + s.mem.disp) if (s.mem.index or isvar(o)) else o + s.mem.disp)) for o in st[b]}
            return False
        if s.mem.index and st.get(norm(x, s.mem.index)):
            st[dr] = {("var", vlo(o)) for o in st[norm(x, s.mem.index)]}; return False
        st.pop(dr, None); return False
    if m in ("add", "sub") and len(ops) == 2 and ops[0].type == X86_OP_REG and x.reg_name(ops[0].reg) == norm(x, ops[0].reg):
        dr = norm(x, ops[0].reg)
        if st.get(dr):
            if ops[1].type == X86_OP_IMM:
                sgn = 1 if m == "add" else -1
                st[dr] = {(("var", vlo(o) + sgn * ops[1].imm) if isvar(o) else o + sgn * ops[1].imm) for o in st[dr]}
            else:
                st[dr] = {("var", vlo(o)) for o in st[dr]}
            return False
        if m == "add" and ops[1].type == X86_OP_REG and st.get(norm(x, ops[1].reg)):
            lb = LB.get(dr, 0)                         # the untainted addend's lower bound (see LB below)
            st[dr] = {("var", vlo(o) + lb) for o in st[norm(x, ops[1].reg)]}; LB.pop(dr, None); return False
        if m == "add" and ops[1].type == X86_OP_IMM and dr in LB:
            LB[dr] += ops[1].imm; return False
    if m in ("movq", "movd") and len(ops) == 2 and ops[1].type == X86_OP_REG and st.get(norm(x, ops[1].reg) or ""):
        add(R["escapes"], ("%08X" % x.address, "copied to a vector register: %s %s" % (m, x.op_str)))
    if m in ("push",) and ops and ops[0].type == X86_OP_REG and st.get(norm(x, ops[0].reg)):
        pass                                           # prologue saves of callee-saved registers
    if m == "xchg":
        add(R["escapes"], ("%08X" % x.address, "xchg (not modelled): %s" % x.op_str))
    # anything else that writes a register kills it
    try:
        _r, w = x.regs_access()
    except Exception:
        w = []
    for r in w:
        n = R64.get(x.reg_name(r))
        if n and n != "rsp":
            st.pop(n, None)
            LB.pop(n, None)
    # lower bound of an untainted index product: imul/shl by a positive constant is taken as >= 0 (ASSUMPTION: array
    # indices are non-negative); consumed by the add rule above within the same straight-line run
    if m == "imul" and len(ops) == 3 and ops[0].type == X86_OP_REG and ops[2].type == X86_OP_IMM and ops[2].imm > 0:
        LB[norm(x, ops[0].reg)] = 0
    if m == "shl" and ops and ops[0].type == X86_OP_REG and len(ops) == 2 and ops[1].type == X86_OP_IMM:
        LB[norm(x, ops[0].reg)] = 0
    return False


LB = {}


FAILS = []
# seeds
seed_fns = set()
for b, e, _u in img.PDATA:
    pass
import memsweep
recs = memsweep.load()
NEWCELLS = set()
rounds = 0
while True:
    rounds += 1
    loaders = sorted({r[1] for r in recs if r[10] in CELLS})
    for f in loaders:
        analyse(f, {}, "seed: references a cell holding the pointer")
    for c in sorted(CREATORS):
        for a, k in img.calls_to(c):
            analyse(img.owner(a) or a, {}, "seed: calls creator %08X at %08X" % (c, a))
    # functions that return the pointer without being handed it are getters: their callers are seeded like creators
    getters = {r for r, R in REPORT.items() if R["returns_ptr"] and r != CTOR
               and any(h.startswith(("seed", "loads")) for h in R["how"])} - CREATORS
    if (NEWCELLS <= CELLS and not getters) or rounds > 8:
        break
    CELLS |= NEWCELLS
    CREATORS |= getters
    REPORT.clear(); MEMO.clear()
print("cells holding the pointer:", ", ".join("%08X" % c for c in sorted(CELLS)), "| rounds", rounds)
print("creators and getters returning the pointer:", ", ".join("%08X" % c for c in sorted(CREATORS)))
callers = []
for c in sorted(CREATORS):
    for a, k in img.calls_to(c):
        o = img.owner(a) or a
        callers.append((a, o))
        analyse(o, {}, "seed: calls creator %08X at %08X" % (c, a))
analyse(CTOR, {"rcx": {0}}, "seed: constructor this")
if not REPORT.get(0x001EF6D0, {}).get("offs", {}).get(0x13C):
    FAILS.append("control: the cascade loop 001EF6D0 must be reached and read object+0x13C (001F04DF)")
if not any(w[0] == "001EF389" for w in rep(CTOR)["count_writes"]):
    FAILS.append("control: constructor store 001EF389 not reported")

with io.open(os.path.join(HERE, "rc8_flow.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("function\thow_reached\tobject_offsets_touched\tcount_writes\tescapes\tcallees_given_pointer\treturns_pointer\n")
    for root, R in REPORT.items():
        offs = ",".join(("%X" % o if isinstance(o, int) else o) for o in sorted(R["offs"], key=lambda z: (isinstance(z, str), z if isinstance(z, int) else 0, str(z))))
        f.write("%08X\t%s\t%s\t%s\t%s\t%s\t%s\n" % (root, "; ".join(sorted(R["how"]))[:400], offs[:600],
                                                     "; ".join("%s %s (%s)" % w for w in R["count_writes"]),
                                                     "; ".join("%s %s" % e for e in R["escapes"]),
                                                     ",".join("%08X" % c for c in sorted(R["callees"])), R["returns_ptr"]))
print("functions reached", len(REPORT), "| seeds: loaders", len(loaders), "creator call sites", len(callers))
cw = [(r, w) for r, R in REPORT.items() for w in R["count_writes"]]
print("count writes (+0x13C covered by a write through the pointer):")
for r, w in cw:
    print("  %08X %s" % (r, w))
print("escapes (grouped by site; lowest object offset the escaping value can carry):")
import re as _re
grp = collections.OrderedDict()
for r, R in REPORT.items():
    for a, e in R["escapes"]:
        nums = [int(z) for z in _re.findall(r"(?<![0-9A-Fa-fx])(\d+)(?=\)|')", e.split("offsets")[-1])] if "offsets" in e else []
        kind = e.split(" offsets")[0].split(" (offsets")[0]
        g = grp.setdefault((r, a, kind), set()); g.update(nums)
ESC = []
for (r, a, kind), nums in grp.items():
    lo = min(nums) if nums else None
    verdict = "cannot reach +0x13C (lowest offset >= 0x140)" if lo is not None and lo >= 0x140 else "READ MANUALLY"
    ESC.append((r, a, kind, lo, verdict))
    print("  %08X %s %-70s lowest=%s  %s" % (r, a, kind[:70], ("%X" % lo) if lo is not None else "?", verdict))
with io.open(os.path.join(HERE, "rc8_escapes.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("function\tsite\tescape\tlowest_object_offset\tverdict\n")
    for r, a, kind, lo, v in ESC:
        f.write("%08X\t%s\t%s\t%s\t%s\n" % (r, a, kind, ("%X" % lo) if lo is not None else "", v))
print("import calls made while a pointer register was live (the import is given no pointer by type):", sorted(IMPORTS))
print("FAILS", len(FAILS), FAILS)
