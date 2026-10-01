"""Flow-aware access census for one record type (OPUS, 2026-09-27), generalised from crr-flow-census/crr_flow_census.py.

Seeds are configured by environment:
  CELLS=ADDR[,ADDR]      a qword load of the cell gives the record base (+0)
  ENTRIES=FUNC:ARG[,..]  the argument register (0 = rcx .. 3 = r9) holds the base at that function's entry
  POOL=ADDR, TYPE_SIZE=N an index * N plus the pool base loaded from ADDR gives base + 0 (the CharacterRenderRecord form)
  STATIC=ADDR            an image static: rip-relative operands inside [ADDR, ADDR + TYPE_SIZE) are field accesses
  GETTERS=FUNC[,..]      a call to FUNC leaves base + 0 in rax (a singleton accessor)
Everything else is the CharacterRenderRecord census's method: a must-analysis per function over its control-flow graph
(plus, since 2026-09-27, argument seeds carried through TAIL CALLS - a jmp to another function's entry),
record + k tracked in registers, argument seeds propagated to a fixpoint, every [base + disp] (no index) recorded as field
k + disp with its width and read / write. Limits: memory-loaded pointers other than the configured cells, stack spills and
return values are not followed.
Usage: CELLS=.. ENTRIES=.. TYPE_SIZE=.. python type_flow_census.py [exe] [functions.tsv] [out.tsv]"""
import collections, struct, sys
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import reg_tracking as RT
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_RSP

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
OUT = sys.argv[3] if len(sys.argv) > 3 else None
import os as _os
BASE = 0x120000
POOL = int(_os.environ.get("POOL", "0"), 16)            # pool base cell for idx*SIZE formation (0 = none)
SIZE = int(_os.environ.get("TYPE_SIZE", "0x740"), 16)
CELLS = {int(c, 16) for c in _os.environ.get("CELLS", "").split(",") if c}           # qword cells holding base + 0
GETTERS = {int(g, 16) for g in _os.environ.get("GETTERS", "").split(",") if g}  # functions whose return value is base + 0
STATICS = sorted(int(a, 16) for a in open(_os.environ["STATICS_FILE"]).read().split(",") if a) if _os.environ.get("STATICS_FILE") else []
import bisect as _bis
def static_of(t):
    k = _bis.bisect_right(STATICS, t) - 1
    return STATICS[k] if k >= 0 and t < STATICS[k] + SIZE else None
STATIC = 1 if STATICS else 0   # an image static of TYPE_SIZE bytes: rip-relative operands inside it are fields, and lea gives base + k
ENTRIES = {(int(e.split(":")[0], 16), int(e.split(":")[1]), 0) for e in _os.environ.get("ENTRIES", "").split(",") if e}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
sizes = {}
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: f, s = int(c[0], 16), int(c[2])
    except (ValueError, IndexError): continue
    if 0x121000 <= f < 0x900000 and off(f) is not None and s > 0: sizes[f] = s

FAM = {}
for r64, subs in {"rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh",
                  "rsi": "esi si sil", "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    FAM[r64] = r64
    for s in subs.split(): FAM[s] = r64
for i in range(8, 16):
    for s in ("", "d", "w", "b"): FAM["r%d%s" % (i, s)] = "r%d" % i
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ARGS = ("rcx", "rdx", "r8", "r9")
POOLTOK, SCALTOK = "POOL", "SCALED"

_cache = {}


def body(f):
    if f not in _cache:
        o = off(f); _cache[f] = list(cs.disasm(d[o:o + sizes[f]], f))
    return _cache[f]


def blocks(xs):
    lo, hi = xs[0].address, xs[-1].address + xs[-1].size
    idx = {x.address: i for i, x in enumerate(xs)}
    leaders = {lo}; succ = {}
    for i, x in enumerate(xs):
        g = x.group
        if x.mnemonic.startswith("j") or x.mnemonic == "ret":
            if i + 1 < len(xs): leaders.add(xs[i + 1].address)
            op = x.operands[0] if x.operands else None
            if op is not None and op.type == CS_OP_IMM and lo <= op.imm < hi and op.imm in idx: leaders.add(op.imm)
    order = sorted(leaders); bl = {}
    for j, a in enumerate(order):
        i0 = idx[a]; i1 = idx[order[j + 1]] if j + 1 < len(order) else len(xs)
        bl[a] = xs[i0:i1]
    for a, ins in bl.items():
        last = ins[-1]; s = []
        nxt = last.address + last.size
        if last.mnemonic == "ret" or last.mnemonic == "int3": pass
        elif last.mnemonic == "jmp":
            op = last.operands[0]
            if op.type == CS_OP_IMM and op.imm in bl: s.append(op.imm)
        elif last.mnemonic.startswith("j"):
            op = last.operands[0]
            if op.type == CS_OP_IMM and op.imm in bl: s.append(op.imm)
            if nxt in bl: s.append(nxt)
        elif nxt in bl: s.append(nxt)
        succ[a] = s
    return bl, succ


def rn(r):
    return FAM.get(cs.reg_name(r), None) if r else None


def analyse(f, entry, sink, calls):
    xs = body(f)
    if not xs: return
    bl, succ = blocks(xs)
    IN = {xs[0].address: dict(entry)}; work = [xs[0].address]; seen_out = {}
    while work:
        a = work.pop(); st = dict(IN[a])
        for x in bl[a]:
            st = step(f, x, st, sink, calls)
        for s in succ[a]:
            if s not in IN: IN[s] = dict(st); work.append(s)
            else:
                m = {r: v for r, v in IN[s].items() if st.get(r) == v}
                if m != IN[s]: IN[s] = m; work.append(s)


def _acc(x, op, oi):
    """'r' / 'w' / 'wr' / '?' for a memory operand, from reg_tracking.op_kind (lea is labelled by the caller)."""
    return {"r": "r", "w": "w", "rw": "wr", "addr": "", "?": "?"}[RT.op_kind(x, op, oi)]


def step(f, x, st, sink, calls):
    mn = x.mnemonic; ops = x.operands
    # record memory operands on tracked bases (labels from the shared policy, reg_tracking.op_kind:
    # capstone's raw flags call movups stores reads and nop / prefetch reads - OPUS 2026-09-28)
    if mn == "nop" or mn.startswith("prefetch"):
        ops = ()
    for oi, op in enumerate(ops):
        if STATIC and op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP:
            t = x.address + x.size + op.mem.disp
            sb = static_of(t)
            if sb is not None:
                acc = _acc(x, op, oi)
                if mn == "lea":
                    acc = "addr"
                    if ops[0].type == CS_OP_REG: st[rn(ops[0].reg)] = t - sb
                sink.append((f, x.address, t - sb, op.size, acc or "r", mn + " " + x.op_str))
                if mn == "lea": return st
            continue
        if op.type == CS_OP_MEM and op.mem.base and not op.mem.index:
            b = rn(op.mem.base)
            if b in st and isinstance(st[b], int):
                acc = _acc(x, op, oi)
                if mn == "lea": acc = "addr"
                sink.append((f, x.address, st[b] + op.mem.disp, op.size, acc or "r", mn + " " + x.op_str))
    if mn == "call":
        op = ops[0] if ops else None
        if op is not None and op.type == CS_OP_IMM and op.imm in sizes:
            for i, r in enumerate(ARGS):
                if isinstance(st.get(r), int): calls.add((op.imm, i, st[r]))
        for r in VOL: st.pop(r, None)
        if op is not None and op.type == CS_OP_IMM and op.imm in GETTERS: st["rax"] = 0
        return st
    if mn == "jmp" and ops and ops[0].type == CS_OP_IMM and ops[0].imm in sizes and not (f <= ops[0].imm < f + sizes[f]):
        # a tail call (2026-09-27): the callee receives this function's argument registers, as a call would pass them
        for i, r in enumerate(ARGS):
            if isinstance(st.get(r), int): calls.add((ops[0].imm, i, st[r]))
        return st
    dst = rn(ops[0].reg) if ops and ops[0].type == CS_OP_REG else None
    full = dst is not None and cs.reg_name(ops[0].reg) == dst
    if mn == "mov" and full and ops[1].type == CS_OP_REG:
        s = rn(ops[1].reg)
        if s in st and cs.reg_name(ops[1].reg) == s: st[dst] = st[s]
        else: st.pop(dst, None)
        return st
    if mn == "mov" and full and ops[1].type == CS_OP_MEM and ops[1].mem.base == X86_REG_RIP:
        t = x.address + x.size + ops[1].mem.disp
        if t == POOL: st[dst] = POOLTOK
        elif t in CELLS and ops[1].size == 8: st[dst] = 0
        else: st.pop(dst, None)
        return st
    if mn == "imul" and full and len(ops) == 3 and ops[2].type == CS_OP_IMM and ops[2].imm == SIZE:
        st[dst] = SCALTOK; return st
    if mn == "add" and full and ops[1].type == CS_OP_MEM and ops[1].mem.base == X86_REG_RIP:
        if x.address + x.size + ops[1].mem.disp == POOL and st.get(dst) == SCALTOK: st[dst] = 0
        else: st.pop(dst, None)
        return st
    if mn == "add" and full and ops[1].type == CS_OP_REG:
        s = rn(ops[1].reg)
        if {st.get(dst), st.get(s)} == {POOLTOK, SCALTOK}: st[dst] = 0
        else: st.pop(dst, None)
        return st
    if mn in ("add", "sub") and full and ops[1].type == CS_OP_IMM and isinstance(st.get(dst), int):
        st[dst] += ops[1].imm if mn == "add" else -ops[1].imm; return st
    if mn == "lea" and full:
        m = ops[1].mem; b = rn(m.base) if m.base else None; ix = rn(m.index) if m.index else None
        if b and not ix and isinstance(st.get(b), int) and m.base != X86_REG_RIP: st[dst] = st[b] + m.disp
        elif b and ix and m.scale == 1 and {st.get(b), st.get(ix)} == {POOLTOK, SCALTOK} and m.disp == 0: st[dst] = 0
        else: st.pop(dst, None)
        return st
    if mn.startswith("cmov") and full and dst in st:
        return st
    # generic kill of every written register
    try:
        # kills from the shared policy (reg_tracking.written: sub-registers folded, capstone's implicit-write
        # defects for cmpxchg / cdq / test corrected) - OPUS 2026-09-28
        for k in RT.written(x):
            if k and k != "rsp": st.pop(k, None)
    except Exception:
        if dst: st.pop(dst, None)
    return st


def main():
    sink = []; calls = set(); done = set()
    # pass 1: every function with an empty entry state (intra-function pool seeds)
    for f in sorted(sizes):
        analyse(f, {}, sink, calls)
    # pass 2..: argument seeds to a fixpoint (plus configured entry seeds)
    pending = set(calls) | set(ENTRIES)
    while pending:
        f, i, k = pending.pop()
        if (f, i, k) in done: continue
        done.add((f, i, k)); new = set()
        analyse(f, {ARGS[i]: k}, sink, new)
        pending |= (new - done)
    rows = sorted(set(sink))
    print("accesses", len(rows), "functions", len({r[0] for r in rows}), "argument seeds", len(done))
    if OUT:
        with open(OUT, "w", newline="") as w:
            w.write("function\tsite\tfield\twidth\tkind\tinstruction\n")
            for f, a, fld, wd, k, ins in rows:
                w.write("%08X\t%08X\t0x%X\t%d\t%s\t%s\n" % (f, a, fld, wd, k, ins))
    return rows


if __name__ == "__main__":
    main()
