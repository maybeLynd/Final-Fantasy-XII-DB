"""The eleven CharacterRenderRecord rows the 2026-09-22 pool-route census created are on OTHER objects (OPUS, 2026-09-27).

db2e18c60 ("BT-2's bytes were hiding behind a multiply") added rows reached "through the pool route" (idx * 0x740 +
[022C6F28]) and committed no receipt. b4b5f347b showed two of them, +0x14 / +0x16, were on other objects. This audits
the other eleven: +0xC..+0xF (four u8), +0x70 u8[16], +0x80 u8[10], +0x8A u16, +0x230 / +0x232 u16, +0x234 / +0x235 u8.

Method: a MAY reaching-definition pass (union at joins; copies followed through registers and rbp/rsp slots) over every
function that loads [022C6F28]. A value is tagged as a pool element when it is idx*0x740 plus the loaded pool base
(imul / add / lea, either order). Any other write, including a 32-bit one, which zero-extends, replaces the value.
  X  no memory access in the eleven spans has a pool-element receiver on ANY path, in any of the 372 functions
  A  the argument-rooted sites the census cited are on other objects too:
       00465CD0's receiver is its caller 00465690's r14 at all 8 calls - the pool element sits in rdx and is overwritten
       by `mov edx, eax` before each call (a 32-bit write the census did not treat as a kill);
       00524320's receiver keeps a POINTER at +0x20 (`mov rsi, [rcx + 0x20]`, then [rsi + 0x882]) where the record holds
       instanceKey char[32] (+0x1C..+0x3B), and the function forms its own pool element separately (r14, 005243A1);
       004256E0 is reached only through the thunks 00422400 / 00422410 (each referenced once, as a table qword), and
       it reads its receiver's +0x31C, the presentation entry's event word (BT-4), not a record field
  P  both flow receipts (flow-CharacterRenderRecord.tsv, crr-flow-accesses.tsv - pool formation among their seeds)
     have no access in the eleven spans
  N  negative control: the same pass finds pool-element receivers at +0x284, the record's slot-live word (hundreds of
     sites) - the tagging works
  S  REGRESSION: no non-DISCOVERED CharacterRenderRecord row starts inside the eleven spans (FAILS before the withdrawal)
Not claimed: that nothing touches these bytes. A pointer loaded from memory, a spill or a return value is not followed,
so the spans go back to DISCOVERED, not to 'unused'.
"""
import os, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
DB = HERE.parents[2]
os.chdir(DB.parent)
sys.path.insert(0, str(HERE.parent / "crr-flow-census"))
_a, sys.argv = sys.argv, sys.argv[:1]
import crr_flow_census as C
sys.argv = _a
import csv, struct
from capstone import CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP
args = sys.argv[1:]
FIELDS = Path(args[args.index("--fields") + 1]) if "--fields" in args else DB / "_types" / "fields.tsv"
POOL = 0x022C6F28
SPANS = [(0xC, 4), (0x70, 16), (0x80, 10), (0x8A, 2), (0x230, 6)]
def inspan(k, spans): return any(s <= k < s + w for s, w in spans)
def ripd(x, op): return x.address + x.size + op.mem.disp
funcs = [f for f in sorted(C.sizes) if any(any(op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP and ripd(x, op) == POOL
                                                for op in x.operands) for x in C.body(f))]
def slot(op):
    b = C.rn(op.mem.base) if op.mem.base else None
    return ("S", b, op.mem.disp) if b in ("rbp", "rsp") and not op.mem.index else None
def step(x, st):
    mn, ops = x.mnemonic, x.operands
    D = frozenset([("D", x.address)])
    if mn == "call":
        for r in C.VOL: st[r] = D
        return st
    dst = C.rn(ops[0].reg) if ops and ops[0].type == CS_OP_REG else None
    full = dst is not None and C.cs.reg_name(ops[0].reg) == dst
    g = lambda r: st.get(r, frozenset([("IN", r)]))
    if mn == "mov" and len(ops) == 2 and ops[0].type == CS_OP_MEM and ops[1].type == CS_OP_REG and ops[0].size == 8 and slot(ops[0]):
        st[slot(ops[0])] = g(C.rn(ops[1].reg)); return st
    if mn == "mov" and full and ops[1].type == CS_OP_REG: st[dst] = g(C.rn(ops[1].reg)); return st
    if mn == "mov" and full and ops[1].type == CS_OP_MEM and ops[1].mem.base == X86_REG_RIP:
        st[dst] = frozenset([("P",)]) if ripd(x, ops[1]) == POOL else D; return st
    if mn == "mov" and full and ops[1].type == CS_OP_MEM and slot(ops[1]):
        st[dst] = st.get(slot(ops[1]), D); return st
    if mn == "imul" and full and len(ops) == 3 and ops[2].type == CS_OP_IMM and ops[2].imm == 0x740:
        st[dst] = frozenset([("S",)]); return st
    if mn == "add" and full and ops[1].type == CS_OP_MEM and ops[1].mem.base == X86_REG_RIP and ripd(x, ops[1]) == POOL:
        st[dst] = frozenset([("E", 0)]) if ("S",) in g(dst) else D; return st
    if mn == "add" and full and ops[1].type == CS_OP_REG:
        a, b = g(dst), g(C.rn(ops[1].reg))
        st[dst] = frozenset([("E", 0)]) if (("P",) in a and ("S",) in b) or (("S",) in a and ("P",) in b) else D; return st
    if mn in ("add", "sub") and full and ops[1].type == CS_OP_IMM:
        d = ops[1].imm if mn == "add" else -ops[1].imm
        st[dst] = frozenset([("E", t[1] + d) if t[0] == "E" else ("D", x.address) for t in g(dst)]); return st
    if mn == "lea" and full:
        m = ops[1].mem; b = C.rn(m.base) if m.base else None; ix = C.rn(m.index) if m.index else None
        if b and not ix and m.base != X86_REG_RIP:
            st[dst] = frozenset([("E", t[1] + m.disp) if t[0] == "E" else ("D", x.address) for t in g(b)]); return st
        if b and ix and m.scale == 1 and m.disp == 0:
            a, c = g(b), g(ix)
            st[dst] = frozenset([("E", 0)]) if (("P",) in a and ("S",) in c) or (("S",) in a and ("P",) in c) else D; return st
        st[dst] = D; return st
    try: w = x.regs_access()[1]
    except Exception: w = [ops[0].reg] if dst else []
    for r in w:
        k = C.rn(r)
        if k and k != "rsp": st[k] = D
    return st
def pool_hits(spans):
    hits = []
    for f in funcs:
        xs = C.body(f); bl, succ = C.blocks(xs)
        IN = {xs[0].address: {}}; work = [xs[0].address]; at = {}
        while work:
            a = work.pop(); st = dict(IN[a])
            for x in bl[a]: at[x.address] = dict(st); st = step(x, st)
            for s in succ[a]:
                if s not in IN: IN[s] = dict(st); work.append(s)
                else:
                    m = dict(IN[s]); ch = False
                    for k, v in st.items():
                        u = m.get(k, frozenset()) | v
                        if u != m.get(k): m[k] = u; ch = True
                    if ch: IN[s] = m; work.append(s)
        for x in xs:
            if x.address not in at: continue
            for op in x.operands:
                if op.type == CS_OP_MEM and op.mem.base and not op.mem.index and op.mem.base != X86_REG_RIP:
                    defs = at[x.address].get(C.rn(op.mem.base), ())
                    ks = {t[1] + op.mem.disp for t in defs if t[0] == "E"}
                    if any(inspan(k, spans) for k in ks): hits.append((f, x.address, sorted(ks)))
    return hits
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
hx = pool_hits(SPANS)
check("X no access in the eleven spans has a pool-element receiver on any path", len(funcs) > 300 and not hx,
      "(%d pool-loading functions; hits %s)" % (len(funcs), hx[:3]))
def calls_to(f, callee):
    xs = C.body(f); out = []
    for i, x in enumerate(xs):
        if x.mnemonic == "call" and x.op_str == hex(callee): out.append((x, xs[max(0, i - 6):i]))
    return out
c465 = calls_to(0x465690, 0x465CD0)
a1 = len(c465) == 8 and all(any(y.op_str == "rcx, r14" for y in pre) and any(y.op_str == "edx, eax" for y in pre) for x, pre in c465)
b524 = [x.op_str for x in C.body(0x524320)][:16]
a2 = "rsi, qword ptr [rcx + 0x20]" in b524 and "r13, [rcx + 0x230]" in b524 and "edx, word ptr [rsi + 0x882]" in b524      and "rbx, rcx" in b524 and any(x.op_str == "r14, [rdi + rax]" for x in C.body(0x524320))
d = open("Tools/work/exe/FFXII_TZA.exe", "rb").read()
refs = {t: d.count(struct.pack("<Q", t)) for t in (0x422400, 0x422410, 0x4256E0)}
thunks = [(x.mnemonic, x.op_str) for x in C.body(0x422400)] + [(x.mnemonic, x.op_str) for x in C.body(0x422410)]
a3 = refs[0x422400] == 1 and refs[0x422410] == 1 and ("jmp", "0x4256e0") in thunks and \
     any(x.op_str == "r13, rcx" for x in C.body(0x4256E0)) and any("[r13 + 0x31c]" in x.op_str for x in C.body(0x4256E0))
check("A the argument-rooted sites are on other objects (00465690 passes r14 after `mov edx, eax`; 00524320's receiver "
      "holds a pointer at +0x20; 004256E0 is reached through two table thunks and reads +0x31C)", a1 and a2 and a3,
      "(%d calls 00465690->00465CD0; thunk refs %s)" % (len(c465), refs))
cover = set()
for p in (DB / "_index/candidates/type-flow-census/flow-CharacterRenderRecord.tsv", DB / "_index/candidates/crr-flow-census/crr-flow-accesses.tsv"):
    for a in csv.DictReader(open(p, encoding="latin1"), delimiter="\t"):
        if a["field"].startswith("-"): continue
        o, w = int(a["field"], 16), int(a["width"])
        if any(o < s + sw and o + w > s for s, sw in SPANS): cover.add(a["site"])
check("P both flow receipts have no access in the eleven spans", not cover, str(sorted(cover)[:5]))
n284 = pool_hits([(0x284, 4)])
check("N the same pass finds pool-element receivers at +0x284", len(n284) > 100, "(%d sites)" % len(n284))
bad = []
for l in FIELDS.read_bytes().decode("utf-8").splitlines():
    c = l.split("\t")
    if len(c) > 8 and c[0] == "CharacterRenderRecord" and c[6] != "DISCOVERED" and inspan(int(c[1], 16), SPANS): bad.append(c[1] + " " + c[3])
check("S no non-DISCOVERED CharacterRenderRecord row starts inside the eleven spans", not bad, str(bad))
print("FAILS", fails)
sys.exit(1 if fails else 0)
