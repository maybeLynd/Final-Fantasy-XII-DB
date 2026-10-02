"""c0_receivers.py - what object is the `+0xC0` pointer in the twelve bodies of mempage-residue item 3? (FABLE, 2026-10-02)
Static, read-only. Shipping exe checked by ../mempage-residue-fable-1002/mp_lib.py (sha256 73461d08...21f8).

Question. Item 3's linear tracker followed any `mov reg, qword ptr [base + 0xc0]` and reported 17 wider stores in 12
bodies landing on SecondaryContext element `+0x10` offsets. The element byte `+0x10` is the source of the nibble that
002E28E0 / 002E3110 copy into CharacterRenderRecord `+0x0C1`. SecondaryContext is reached only as ActorStorageRecord
`+0xC0` (types.tsv: SecondaryContext allocation_site = INTERIOR ActorStorageRecord +0x350, planted by 00266AD0). So a
store can touch the nibble only if the loaded `+0xC0` belongs to an ActorStorageRecord. For each body: whose `+0xC0`
is it, and what does that slot hold?

Method.
  R1  the 17 stores are re-read from item 3's .out (B2 rows marked POSSIBLE, minus the setter 002EBC90 itself).
  R2  reaching definitions on each body's own CFG (direct branches, plus MSVC jump tables decoded from
      `lea rB,[rip->image base]` + `mov r32, dword [rB + rI*4 + T]`; any undecoded indirect jump is reported). From the
      store's base register, definitions are followed backward through field loads, reg copies, lea, induction
      (`add r, imm`), pool arithmetic (`imul`, `add r,[rip]`), call returns, global cells and stack arguments, to a root.
      A root with more than one reaching definition is printed AMBIGUOUS and counted as a failure.
  R3  each root is typed by facts re-checked against the bytes: raw E8/E9/jcc callers (mp_lib.raw_index), rip-lea /
      rip-mov references (byte scan of .text) for handler registrations, the allocator call and size that follow a
      registration, RTTI complete-object locators for vtables, the class's own writers of `+0xC0`, and the type store
      rows (types.tsv, fields.tsv, field-access-index.tsv) named by address.
  R4  an image-wide writer scan of the Manager0209AC60 members `+0x2E0` and `+0x300` (registers loaded from the
      pointer cell 0209AC30, plus direct rip operands at 0209AC60 + disp).
Controls.
  P1 (positive, CRR): R2 applied to the two known `+0x0C1` writers 002E29E9 and 002E33B3 must reach the pool cell
      022C6F28 with stride 0x740, which types.tsv gives as CharacterRenderRecord's instance; the same rule must fire on
      none of the 17 stores.
  P2 (positive, actor): R2 applied to the ActorStorageRecord census load 00225D86 (`mov rcx, [rbx + 0xc0]`) must root
      in the return of 00358940, which types.tsv names as the record lookup (block + 8 + i*8); no root of the 17 may be.
  N1 (negative): R2+R3 applied to 00406A60's `+0xC0` load 00406C45 must give the widget registered by 004051B0 (size
      0xF0, slot 02B62D88), matching the type store's WidgetSingleton02B62D88 row, and not ActorStorageRecord.
"""
import os, sys, struct, csv, re
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mempage-residue-fable-1002"))
from mp_lib import *
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))       # re-set: `from mp_lib import *` imports mp_lib's own HERE
TYPES = os.path.join(DBROOT, "FFXII TZA", "_types")
ITEM3_OUT = os.path.join(HERE, "..", "mempage-residue-fable-1002", "item3_c1_writers_and_domain.out")
OUT = []
FAILS = []


def p(s=""):
    print(s)
    OUT.append(s)


def need(cond, what):
    if not cond:
        FAILS.append(what)
        p("    FAIL: " + what)
    return cond


GPR = {}
for r in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp"):
    for v in ("r" + r, "e" + r, r):
        GPR[v] = "r" + r
for r8, r64 in (("al", "rax"), ("bl", "rbx"), ("cl", "rcx"), ("dl", "rdx"), ("sil", "rsi"), ("dil", "rdi"),
                ("bpl", "rbp"), ("spl", "rsp"), ("ah", "rax"), ("bh", "rbx"), ("ch", "rcx"), ("dh", "rdx")):
    GPR[r8] = r64
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        GPR["r%d%s" % (n, suf)] = "r%d" % n
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = {"rcx": 0, "rdx": 1, "r8": 2, "r9": 3}


def fam(r):
    return GPR.get(md.reg_name(r)) if r else None


def text(x):
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


ADDR = {}


def ins_at(a):
    if a not in ADDR:
        o = owner(a)
        if o is not None:
            for x in decode(o):
                ADDR[x.address] = x
    return ADDR.get(a)


def check_ins(a, expect):
    x = ins_at(a)
    got = text(x) if x else "<none>"
    return need(got == expect, "%08X expected `%s`, got `%s`" % (a, expect, got))


def rip_of(a):
    x = ins_at(a)
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return x.address + x.size + op.mem.disp
    return None


# ---------------------------------------------------------------- CFG and reaching definitions
_cfg = {}


def jump_table(ins, k, fn):
    """targets of an MSVC jump table feeding the indirect jmp at ins[k], or None."""
    end = fn + funcs[fn]
    for j in range(k - 1, max(-1, k - 9), -1):
        x = ins[j]
        if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM:
            m = x.operands[1].mem
            if m.scale == 4 and m.index != 0 and m.base not in (0, X86_REG_RIP):
                bfam = fam(m.base)
                for i in range(j - 1, max(-1, j - 12), -1):
                    y = ins[i]
                    if y.mnemonic == "lea" and fam(y.operands[0].reg) == bfam and y.operands[1].mem.base == X86_REG_RIP:
                        if y.address + y.size + y.operands[1].mem.disp == BASE:
                            tg = []
                            for e in range(512):
                                fo = off(BASE + m.disp + 4 * e)
                                if fo is None:
                                    break
                                t = BASE + struct.unpack_from("<I", d, fo)[0]
                                if not (fn <= t < end):
                                    break
                                tg.append(t)
                            return tg
                        break
    return None


def cfg(fn):
    if fn in _cfg:
        return _cfg[fn]
    ins = decode(fn)
    idx = {x.address: i for i, x in enumerate(ins)}
    preds = defaultdict(set)
    unresolved = []
    preds[0].add(-1)
    for i, x in enumerate(ins):
        m = x.mnemonic
        ft = not (m in ("ret", "jmp", "int3") or m.startswith("ud"))
        if ft and i + 1 < len(ins):
            preds[i + 1].add(i)
        if m.startswith("j") and x.operands and x.operands[0].type == X86_OP_IMM:
            t = x.operands[0].imm
            if t in idx:
                preds[idx[t]].add(i)
        elif m == "jmp" and x.operands and x.operands[0].type != X86_OP_IMM:
            tg = jump_table(ins, i, fn)
            if tg is None:
                unresolved.append(x.address)
            else:
                for t in tg:
                    if t in idx:
                        preds[idx[t]].add(i)
    _cfg[fn] = (ins, idx, preds, unresolved)
    return _cfg[fn]


def wfams(x):
    try:
        s = {GPR.get(md.reg_name(r)) for r in x.regs_access()[1]} - {None}
    except Exception:
        s = set()
    if x.mnemonic == "call":
        s |= VOL
    return s


WALK = {0x7B0311: "list walk: next node through +0x10"}   # read by hand, re-checked in R3 (B12)


def induction(x, f):
    o = x.operands
    if x.address in WALK:
        return True
    if x.mnemonic in ("add", "sub", "inc", "dec") and o and o[0].type == X86_OP_REG and fam(o[0].reg) == f:
        return len(o) == 1 or o[1].type == X86_OP_IMM
    if x.mnemonic == "lea" and fam(o[0].reg) == f and o[1].mem.index == 0 and fam(o[1].mem.base) == f:
        return True
    return False


def reaching(fn, j, f):
    ins, idx, preds, _u = cfg(fn)
    defs, seen, stack = set(), set(), [j]
    while stack:
        k = stack.pop()
        for q in preds[k]:
            if q == -1:
                defs.add("ENTRY")
                continue
            if q in seen:
                continue
            seen.add(q)
            if f in wfams(ins[q]):
                defs.add(q)
                if induction(ins[q], f):
                    stack.append(q)
            else:
                stack.append(q)
    return defs


def frame_at(fn, j):
    ins = decode(fn)
    fr = 0
    for x in ins[:j]:
        if x.mnemonic == "push":
            fr += 8
        elif x.mnemonic == "sub" and x.op_str.startswith("rsp, ") and x.operands[1].type == X86_OP_IMM:
            fr += x.operands[1].imm
    return fr


def prov(fn, j, f, depth=0):
    """provenance of register family f just before ins[j] of fn: list of (kind, value, site) from the use back to the root."""
    ins, idx, preds, unresolved = cfg(fn)
    defs = reaching(fn, j, f)
    main = sorted([q for q in defs if q == "ENTRY" or not induction(ins[q], f)], key=str)
    ind = sorted(ins[q].address for q in defs if q != "ENTRY" and induction(ins[q], f))
    steps = []
    if ind:
        steps.append(("induction", ",".join("%08X" % a for a in ind), None))
    if len(main) != 1 or depth > 12:
        return steps + [("AMBIGUOUS", "%s <- %s" % (f, ["ENTRY" if q == "ENTRY" else "%08X" % ins[q].address for q in main]), None)]
    q = main[0]
    if q == "ENTRY":
        if f in ARGS:
            return steps + [("arg", ARGS[f], fn)]
        return steps + [("entry", f, fn)]
    x = ins[q]
    o = x.operands
    m = x.mnemonic
    a = x.address
    if m == "call":
        if f == "rax" and o[0].type == X86_OP_IMM:
            return steps + [("call", o[0].imm, a)]
        return steps + [("clobbered-by-call", text(x), a)]
    if m in ("mov", "movsxd", "movzx", "movsx") and len(o) == 2 and o[1].type == X86_OP_MEM:
        mm = o[1].mem
        if mm.base == X86_REG_RIP:
            return steps + [("cell", a + x.size + mm.disp, a)]
        if fam(mm.base) == "rsp":
            fr = frame_at(fn, q)
            if mm.disp >= fr + 8:
                return steps + [("stackarg", (mm.disp - fr - 8) // 8, a)]
            return steps + [("stack-local", mm.disp, a)]
        if mm.index:
            steps.append(("indexed", "+%#x + %s*%d" % (mm.disp, md.reg_name(mm.index), mm.scale), a))
        else:
            steps.append(("field", mm.disp, a))
        return steps + prov(fn, q, fam(mm.base), depth + 1)
    if m in ("mov", "movsx", "movzx", "movsxd") and len(o) == 2 and o[1].type == X86_OP_REG:
        steps.append(("copy", md.reg_name(o[1].reg), a))
        return steps + prov(fn, q, fam(o[1].reg), depth + 1)
    if m == "lea" and o[1].mem.index == 0:
        if o[1].mem.base == X86_REG_RIP:
            return steps + [("cell-address", a + x.size + o[1].mem.disp, a)]
        steps.append(("lea", o[1].mem.disp, a))
        return steps + prov(fn, q, fam(o[1].mem.base), depth + 1)
    if m == "add" and len(o) == 2 and o[1].type == X86_OP_MEM and o[1].mem.base == X86_REG_RIP:
        steps.append(("plus-cell", a + x.size + o[1].mem.disp, a))
        return steps + prov(fn, q, f, depth + 1)
    if m == "imul" and len(o) == 3 and o[2].type == X86_OP_IMM:
        steps.append(("stride", o[2].imm, a))
        return steps + prov(fn, q, fam(o[1].reg), depth + 1)
    if m == "xor" and len(o) == 2 and o[1].type == X86_OP_REG and fam(o[1].reg) == f:
        return steps + [("zero", 0, a)]
    return steps + [("other", text(x), a)]


def fmt(steps):
    out = []
    for k, v, a in steps:
        at = (" @%08X" % a) if isinstance(a, int) and k not in ("arg", "entry") else ""
        if k == "field":
            out.append("[+%#x]%s" % (v, at))
        elif k in ("cell", "plus-cell", "cell-address"):
            out.append("%s %08X%s" % (k, v, at))
        elif k == "call":
            out.append("ret of %08X%s" % (v, at))
        elif k == "arg":
            out.append("arg%d of %08X" % (v, a))
        elif k == "stackarg":
            out.append("stack argument %d (0-based, the %s)%s" % (v, ["first", "second", "third", "fourth", "fifth", "sixth"][v] if v < 6 else "later", at))
        elif k == "lea":
            out.append("lea %+#x%s" % (v, at))
        elif k == "stride":
            out.append("*%#x%s" % (v, at))
        else:
            out.append("%s %s%s" % (k, v, at))
    return " <- ".join(out)


def prov_at(site, reg):
    fn = owner(site)
    ins, idx, _p, _u = cfg(fn)
    return prov(fn, idx[site], GPR[reg])


def store_base(site):
    x = ins_at(site)
    for op, w in mem_writes(x):
        return md.reg_name(op.mem.base), op.mem.disp, w
    return None, None, None


# ---------------------------------------------------------------- reference scans
def rip_refs(targets):
    """{target: [instruction address]} for every `lea/mov r64, [rip + X]` in .text with X a target."""
    targets = set(targets)
    base = off(TEXT_VA)
    blob = d[base:base + TEXT_SZ]
    out = defaultdict(list)
    for i in range(len(blob) - 7):
        if blob[i] in (0x48, 0x4C) and blob[i + 1] in (0x8D, 0x8B) and (blob[i + 2] & 0xC7) == 0x05:
            t = TEXT_VA + i + 7 + struct.unpack_from("<i", blob, i + 3)[0]
            if t in targets:
                a = TEXT_VA + i
                x = ins_at(a)
                if x is not None and x.address == a:
                    out[t].append(a)
    return out


def abs_qwords(t):
    res = []
    pat = struct.pack("<Q", t)
    i = d.find(pat)
    while i != -1:
        for n, va, vs, ro, rs in SECS:
            if ro <= i < ro + rs:
                res.append(BASE + va + i - ro)
        i = d.find(pat, i + 1)
    return res


def rtti_name(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]
    o = off(col)
    sig, offs, cd, td, chd = struct.unpack_from("<IIIII", d, o)
    return d[off(BASE + td) + 16:].split(b"\0")[0].decode(errors="replace"), offs


def stores_disp(fn, disp, width=8):
    return [x for x in decode(fn) for op, w in mem_writes(x)
            if w == width and op.mem.disp == disp and op.mem.index == 0 and op.mem.base not in (0, X86_REG_RIP)
            and md.reg_name(op.mem.base) != "rsp"]


def follows(site, n, pred):
    """some instruction among the n after `site` in its body satisfies pred(text)."""
    fn = owner(site)
    ins = decode(fn)
    k = [i for i, x in enumerate(ins) if x.address == site][0]
    return [x for x in ins[k + 1:k + 1 + n] if pred(text(x))]


def tsv_rows(path):
    return list(csv.reader(open(path, encoding="utf-8", errors="replace"), delimiter="\t"))


# ================================================================ main
def main():
    p("# c0_receivers.py - the object behind the +0xC0 pointer in item 3's twelve bodies (FABLE). run at %s" % head_sha())
    p()
    types = {r[0]: r for r in tsv_rows(os.path.join(TYPES, "types.tsv")) if r}
    fields = tsv_rows(os.path.join(TYPES, "fields.tsv"))
    fai = tsv_rows(os.path.join(TYPES, "field-access-index.tsv"))

    # ---------------- R1: the 17 stores from item 3
    p("## R1 the stores item 3 left open (item3_c1_writers_and_domain.out, B2 rows marked POSSIBLE)")
    rows = []
    for line in open(ITEM3_OUT, encoding="utf-8"):
        mt = re.match(r"\s+([0-9A-F]{8}) in ([0-9A-F]{8}) .*?\(ctx-derived from ([0-9A-F]{8})\).*bits4-7 POSSIBLE", line)
        if mt:
            s, fn, ld = (int(g, 16) for g in mt.groups())
            if fn != 0x2EBC90:
                rows.append((s, fn, ld))
    bodies = sorted({r[1] for r in rows})
    p("  stores: %d in %d bodies: %s" % (len(rows), len(bodies), ", ".join("%08X" % b for b in bodies)))
    need(len(rows) == 17 and len(bodies) == 12, "item 3 lists 17 stores in 12 bodies")
    p()

    # ---------------- R2: provenance of each store's base
    p("## R2 reaching-definition chains, store base back to its root (own CFG; jump tables decoded)")
    p("  hand-read loop steps treated as induction: %s" % "; ".join("%08X %s" % kv for kv in WALK.items()))
    chains = {}
    for s, fn, ld in rows:
        reg, disp, w = store_base(s)
        ch = prov_at(s, reg)
        chains[s] = ch
        _i, _x, _p, unres = cfg(fn)
        p("  %08X in %08X  w%d [%s %+#x]  %s%s" % (s, fn, w, reg, disp, fmt(ch),
                                                  ("   (undecoded indirect jmp: %s)" % unres) if unres else ""))
        need(not any(k == "AMBIGUOUS" for k, v, a in ch), "%08X chain is unambiguous" % s)
        hit = [a for k, v, a in ch if k in ("field",) and v == 0xC0 and a == ld] or \
              [a for k, v, a in ch if k == "stackarg" and a == ld]
        need(bool(hit), "%08X chain passes item 3's cited +0xC0 site %08X" % (s, ld))
    p()

    # ---------------- reference scans used below
    handlers = [0x291D90, 0x299090, 0x29A0A0, 0x2CBF80, 0x2CABF0, 0x53E380, 0x558FB0, 0x561390, 0x560910,
                0x5636F0, 0x563930, 0x563B10, 0x563D20, 0x406A60, 0x406E80, 0x2EAD2D0]
    rr = rip_refs(handlers)
    callees = [0x2986E0, 0x53E640, 0x564E10, 0x564C80, 0x5651E0, 0x7DACF0, 0x7DACC0, 0x7E01F0, 0x297710,
               0x558F20, 0x561300, 0x7AF380, 0x7E0130, 0x29A0A0, 0x299090, 0x558FB0, 0x561390, 0x53E380, 0x292390]
    ri = raw_index(callees)

    def callers(t):
        return sorted((s, form, o) for s, form, o, al in ri[t] if al)

    def show_callers(t):
        cs = callers(t)
        p("    raw sites of %08X: %s; absolute qwords %d" % (t, ", ".join("%08X %s in %08X" % c for c in cs) or "none",
                                                          len(abs_qwords(t))))
        return cs

    def registration(h, size_site, size_ins, alloc_site, alloc_ins, ref_site):
        p("    handler %08X referenced by rip operands at: %s" % (h, ", ".join("%08X" % a for a in rr[h]) or "none"))
        need(ref_site in rr[h], "%08X registered at %08X" % (h, ref_site))
        check_ins(size_site, size_ins)
        check_ins(alloc_site, alloc_ins)

    def type_row(name, needles):
        r = types.get(name)
        ok = r is not None and all(n in "\t".join(r) for n in needles)
        need(ok, "types.tsv row %s contains %s" % (name, needles))
        return r

    def field_row(tname, offs):
        for r in fields:
            if len(r) > 3 and r[0] == tname and int(r[1], 16) == offs:
                return r
        need(False, "fields.tsv %s +%#x" % (tname, offs))
        return None

    # ---------------- R4: Manager0209AC60 +0x2E0 / +0x300 writers, image-wide
    p("## R4 writers of Manager0209AC60 +0x2E0 and +0x300 (registers loaded from cell 0209AC30, or rip operands)")
    CELL, STATIC = 0x209AC30, 0x209AC60
    w300, w2e0 = [], []
    for fn in all_functions():
        held = set()
        for x in decode(fn):
            for op, w in mem_writes(x):
                if op.mem.base == X86_REG_RIP:
                    t = x.address + x.size + op.mem.disp
                    if t in (STATIC + 0x300, STATIC + 0x2E0):
                        (w300 if t == STATIC + 0x300 else w2e0).append((x.address, fn, text(x)))
                elif fam(op.mem.base) in held and op.mem.index == 0 and op.mem.disp in (0x300, 0x2E0):
                    (w300 if op.mem.disp == 0x300 else w2e0).append((x.address, fn, text(x)))
            ws = wfams(x)
            if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM \
                    and x.operands[1].mem.base == X86_REG_RIP and x.address + x.size + x.operands[1].mem.disp == CELL:
                held -= ws
                held.add(fam(x.operands[0].reg))
            else:
                held -= ws
    for nm, lst in (("+0x300", w300), ("+0x2E0", w2e0)):
        p("  %s: %d writers: %s" % (nm, len(lst), "; ".join("%08X in %08X `%s`" % t for t in lst)))
    need([a for a, f, t in w300] == [0x291DD2, 0x291F96], "+0x300 writers are 00291DD2, 00291F96")
    need(sorted(a for a, f, t in w2e0) == [0x2CBE11, 0x2CBE96, 0x2CBF48, 0x2CBFBD], "+0x2E0 writers are the four")
    pub = {(r[4], r[5]) for r in fai[1:] if len(r) > 5 and r[0] == "Manager0209AC60" and r[3] == "w" and r[1] in ("0x300", "0x2E0")}
    need({(("%08X" % f), ("%08X" % a)) for a, f, t in w300 + w2e0} == pub,
         "the scan equals the type store's field-access-index write rows for those two members")
    p()

    # ---------------- R3: per body
    p("## R3 receiver typing, per body")
    verdict = {}

    # B1 00292390
    p("- 00292390 (store 00292793)")
    need(rip_of(0x2926B1) == CELL, "002926B1 reads cell 0209AC30")
    check_ins(0x2926BB, "mov rdx, qword ptr [rcx + 0x300]")
    registration(0x291D90, 0x2920DB, "mov ecx, 0x170", 0x2920E0, "jmp 0x244f50", 0x2920D4)
    check_ins(0x291DA4, "mov rdi, rcx")
    check_ins(0x291DAC, "je 0x291f8a")
    need(rip_of(0x291F8A) == CELL, "00291F8A reads cell 0209AC30")
    check_ins(0x291F96, "mov qword ptr [rax + 0x300], rdi")
    ws = stores_disp(0x291D90, 0xC0)
    p("    00291D90's own +0xC0 stores: %s" % ", ".join("%08X `%s` value: %s" % (x.address, text(x), fmt(prov_at(x.address, x.op_str.split(", ")[1]))) for x in ws))
    need([x.address for x in ws] == [0x291E71, 0x291F32], "00291D90 stores +0xC0 at 00291E71 and 00291F32 only")
    check_ins(0x24A456, "call 0x24a4e0")
    check_ins(0x24A461, "mov rbx, rax")
    check_ins(0x24A469, "mov rax, rbx")
    need(rip_of(0x24A4E3) == 0x208F580, "0024A4E0 scans the static table at 0208F580")
    check_ins(0x24A4F9, "add rax, 0x48")
    check_ins(0x24A51F, "cmp r8d, 0x40")
    verdict[0x292390] = ("Widget, 0x170 bytes, handler 00291D90 (Manager0209AC60 +0x300)",
                         "an entry of the 64-slot, 0x48-byte static table at 0208F580 from 0024A440 / 0024A4E0 (or null)",
                         "stores +0x10/+0x28/+0x38 into that 0x48-byte entry")

    # B2/B3 002986E0 / 00299090
    p("- 002986E0 (00298C4C, 00298C63, 00298DAC, 00298EFE) and 00299090 (002991AD, 0029926B, 00299305)")
    cs = show_callers(0x2986E0)
    need([c[0] for c in cs] == [0x299406], "002986E0's only raw site is 00299406")
    p("    rcx at 00299406: %s" % fmt(prov_at(0x299406, "rcx")))
    need(prov_at(0x299406, "rcx")[-1][:2] == ("arg", 0), "00299406 passes 00299090's own receiver")
    need(len(abs_qwords(0x2986E0)) == 0, "no pointer route to 002986E0")
    registration(0x299090, 0x29C359, "mov edx, 0xd8", 0x29C374, "call 0x245000", 0x29C34D)
    check_ins(0x29C36A, "lea rcx, [rbx + 0x7c0]")
    ws = stores_disp(0x299090, 0xC0)
    need([x.address for x in ws] == [0x2990FC], "00299090 stores +0xC0 at 002990FC only")
    p("    002990FC value: %s" % fmt(prov_at(0x2990FC, "rax")))
    need(rip_of(0x28F830) == 0x209BE80, "0028F830 reads the ManagerSingleton0209BE80 slot")
    check_ins(0x28F842, "shl rax, 5")
    check_ins(0x28F846, "add rax, rdx")
    type_row("ManagerSingleton0209BE80", ["0x10FD0", "0209BE80"])
    for b in (0x2986E0, 0x299090):
        verdict[b] = ("Widget, 0xD8 bytes, handler 00299090, built in place in PaneListWidget0B68 +0x7C0",
                      "a 32-byte slot at ManagerSingleton0209BE80 + index*0x20 (0028F830)",
                      "word/qword stores inside that 32-byte slot")

    # B4 0029A0A0
    p("- 0029A0A0 (0029A29C)")
    registration(0x29A0A0, 0x29BBCE, "mov edx, 0x160", 0x29BBDA, "call 0x245000", 0x29BBD3)
    type_row("PaneSlotWidget0160", ["0x160", "0029A0A0"])
    need(stores_disp(0x29A0A0, 0xC0) == [], "0029A0A0 itself stores no qword at +0xC0")
    cs = show_callers(0x297710)
    need([c[0] for c in cs] == [0x29A4EB], "00297710's only raw site is 0029A4EB")
    need(prov_at(0x29A4EB, "rcx")[-1][:2] == ("arg", 0), "0029A4EB passes 0029A0A0's receiver")
    ws = stores_disp(0x297710, 0xC0)
    need([x.address for x in ws] == [0x2977B9, 0x297810, 0x29786C], "00297710's three +0xC0 stores")
    for x in ws:
        p("    %08X `%s` value: %s" % (x.address, text(x), fmt(prov_at(x.address, x.op_str.split(", ")[1]))))
    check_ins(0x2977A1, "mov rcx, qword ptr [rcx + 0x18]")
    check_ins(0x2977A5, "call 0x247870")
    check_ins(0x247884, "mov ecx, dword ptr [rcx + 0x40]")
    check_ins(0x247887, "test cl, 0x20")
    fr = field_row("Widget", 0xA0)
    p("    Widget +0xA0 (types fields): %s - %s" % (fr[2] if fr else "?", (fr[5][:90] if fr else "?")))
    verdict[0x29A0A0] = ("PaneSlotWidget0160 (Widget, 0x160 bytes, handler 0029A0A0)",
                         "a child Widget from the element block (00297710: [[+0x60]+0xA0/0xA8/0xB0]+0x18)",
                         "byte +0xA0 = the child widget's own opacity byte")

    # B5 002CBA50
    p("- 002CBA50 (002CBBD3)")
    need(rip_of(0x2CBA56) == CELL, "002CBA56 reads cell 0209AC30")
    check_ins(0x2CBA5D, "mov r14, qword ptr [rax + 0x2e0]")
    for ref, sz, al in ((0x2CBDF1, 0x2CBDF8, 0x2CBE02), (0x2CBE80, 0x2CBE6D, 0x2CBE87), (0x2CBF25, 0x2CBF34, 0x2CBF39)):
        registration(0x2CBF80, sz, "mov ecx, 0x170", al, "call 0x244f50", ref)
    check_ins(0x2CBFBA, "xor r15d, r15d")
    check_ins(0x2CBF97, "mov rbx, rcx")
    ws = stores_disp(0x2CBF80, 0xC0)
    need([x.address for x in ws] == [0x2CC20E], "002CBF80 stores +0xC0 at 002CC20E only")
    p("    002CC20E value: %s" % fmt(prov_at(0x2CC20E, "rax")))
    registration(0x2CABF0, 0x2CC1E7, "mov ecx, 0xf8", 0x2CC206, "call 0x244f50", 0x2CC1D2)
    check_ins(0x2CC218, "call 0x244960")
    verdict[0x2CBA50] = ("Widget, 0x170 bytes, handler 002CBF80 (Manager0209AC60 +0x2E0)",
                         "its child Widget, 0xF8 bytes, handler 002CABF0 (002CC20E)",
                         "dword/word stores at +0xC0..+0xEC inside the 0xF8-byte child")

    # B6 00408780
    p("- 00408780 (004087C2)")
    need(rip_of(0x408780) == 0x2B62D80, "00408780 reads slot 02B62D80")
    type_row("WidgetSingleton02B62D80", ["0xE8", "00406E80"])
    need(any(r[0] == "WidgetSingleton02B62D80" and r[5] == "0040879A" for r in fai if len(r) > 5),
         "field-access-index already types 0040879A as WidgetSingleton02B62D80 +0xC0")
    ws = stores_disp(0x406E80, 0xC0)
    need([x.address for x in ws] == [0x406FB8, 0x407107], "00406E80 stores +0xC0 at 00406FB8 and 00407107")
    for x in ws:
        p("    %08X `%s` value: %s" % (x.address, text(x), fmt(prov_at(x.address, x.op_str.split(", ")[1]))))
    check_ins(0x408226, "call 0x245020")
    verdict[0x408780] = ("WidgetSingleton02B62D80 (Widget, 0xE8 bytes, handler 00406E80)",
                         "a child Widget built by 00244F50 at 00407102 (null before), released by 00245020 (00408226)",
                         "dword stores at +0xF8..+0x104 of that child")

    # B7 0053E640
    p("- 0053E640 (0053E814)")
    cs = show_callers(0x53E640)
    need([c[0] for c in cs] == [0x53E48F], "0053E640's only raw site is 0053E48F")
    need(prov_at(0x53E48F, "rcx")[-1][:2] == ("arg", 0), "0053E48F passes 0053E380's receiver")
    registration(0x53E380, 0x53ED46, "mov ecx, 0x1498", 0x53ED4F, "jmp 0x244f50", 0x53ED3F)
    need(rip_of(0x53E4B2) == 0x2CA8A80, "0053E380 publishes itself to 02CA8A80 (0053E4B2)")
    ws = stores_disp(0x53E380, 0xC0)
    need([x.address for x in ws] == [0x53E3DA, 0x53E50D], "0053E380 stores +0xC0 at 0053E3DA and 0053E50D")
    for x in ws:
        p("    %08X `%s` value: %s" % (x.address, text(x), fmt(prov_at(x.address, x.op_str.split(", ")[1]))))
    check_ins(0x53E4E9, "mov edx, 0x10000")
    check_ins(0x53E506, "call 0x249810")
    check_ins(0x53E514, "mov r8d, 0x10000")
    check_ins(0x53E51D, "call 0x861ec0")
    check_ins(0x53E3D5, "call 0x3697f0")
    verdict[0x53E640] = ("Widget, 0x1498 bytes, handler 0053E380 (slot 02CA8A80)",
                         "a 64 KiB zeroed buffer from 00249810 (0053E50D), freed by 003697F0",
                         "dword stores at +0x10 of 0x20-byte records in that buffer")

    # B8/B9 00558FB0 / 00561390 and their owner
    p("- 00558FB0 (00559306) and 00561390 (005616A8)")
    registration(0x558FB0, 0x558F69, "mov ecx, 0xe8", 0x558F85, "call 0x244f50", 0x558F72)
    registration(0x561390, 0x56134F, "mov ecx, 0x110", 0x561364, "call 0x244f50", 0x561358)
    type_row("WidgetSingleton02CA9670", ["0x110", "00561390"])
    for crt, a in ((0x558F20, (0x558F4B, 0x558F56, 0x558F79, 0x558F46)), (0x561300, (0x56132B, 0x561336, 0x56135F, 0x561326))):
        check_ins(a[0], "mov qword ptr [rsp + 0x20], rcx")
        check_ins(a[1], "lea rax, [rsp + 0x20]")
        check_ins(a[2], "mov qword ptr [rsp + 0x48], rax")
        check_ins(a[3], "lea r8, [rsp + 0x40]")
    ws1, ws2 = stores_disp(0x558FB0, 0xC0), stores_disp(0x561390, 0xC0)
    need([x.address for x in ws1] == [0x559107] and [x.address for x in ws2] == [0x561580],
         "each handler stores +0xC0 once (00559107, 00561580)")
    check_ins(0x5590EF, "mov rbx, qword ptr [rdx + 8]")
    check_ins(0x559102, "mov rax, qword ptr [rbx]")
    check_ins(0x56153C, "mov rbx, qword ptr [rdx + 8]")
    check_ins(0x56157B, "mov rcx, qword ptr [rbx]")
    check_ins(0x5613B1, "je 0x56153c")
    jt = jump_table(decode(0x558FB0), [i for i, x in enumerate(decode(0x558FB0)) if x.address == 0x558FEE][0], 0x558FB0)
    need(jt is not None and jt[0] == 0x5590EF and jt.count(0x5590EF) == 1,
         "00558FB0's jump table sends message 1 (entry 0), and only it, to 005590EF")
    for c in (0x558F20, 0x561300):
        cs = show_callers(c)
        for s, form, o in cs:
            p("      rcx at %08X: %s" % (s, fmt(prov_at(s, "rcx"))))
    need([c[0] for c in callers(0x558F20)] == [0x560C89, 0x5614A1], "00558F20's sites")
    need([c[0] for c in callers(0x561300)] == [0x5590E3, 0x560C98], "00561300's sites")
    registration(0x560910, 0x5601E7, "mov ecx, 0x190", 0x5601F8, "call 0x244f50", 0x5601EC)
    for b in (0x558FB0, 0x561390):
        verdict[b] = ("Widget, %s bytes, handler %08X" % ("0xE8" if b == 0x558FB0 else "0x110", b),
                      "the owning Widget, 0x190 bytes, handler 00560910 (creation parameter; the two creators pass "
                      "either 00560910's receiver or their own +0xC0)",
                      "qword store at +0x100 of the 0x190-byte owner")

    # B10 00564E10
    p("- 00564E10 (005650DD)")
    cs = show_callers(0x564E10)
    need([c[0] for c in cs] == [0x564CAC, 0x5651D7], "00564E10's sites are 00564CAC and 005651D7")
    p("      rcx at 00564CAC: %s" % fmt(prov_at(0x564CAC, "rcx")))
    p("      rcx at 005651D7: %s" % fmt(prov_at(0x5651D7, "rcx")))
    cs = show_callers(0x564C80)
    need([c[0] for c in cs] == [0x565218] and prov_at(0x565218, "rcx")[-1][:2] == ("arg", 0),
         "00564C80's only site 00565218 passes 005651E0's receiver")
    cs = show_callers(0x5651E0)
    need(sorted(c[2] for c in cs) == [0x5636F0, 0x563930, 0x563B10, 0x563D20], "005651E0 is the shared tail of four handlers")
    for s, form, o in cs:
        ch = prov_at(s, "rcx")
        p("      rcx at %08X (%s in %08X): %s" % (s, form, o, fmt(ch)))
        need(ch[-1][:3] == ("arg", 0, o), "%08X hands its own receiver to 005651E0" % o)
    for h, ref in ((0x5636F0, 0x564C0A), (0x563930, 0x564C13), (0x563B10, 0x564C1C), (0x563D20, 0x564C25)):
        need(ref in rr[h], "%08X registered at %08X" % (h, ref))
    check_ins(0x564C2F, "xor edx, edx")
    check_ins(0x564C34, "call 0x564ac0")
    check_ins(0x564BD1, "lea rbx, [rax*8 + 0x170]")
    need(rip_of(0x564C39) == CELL, "00564C39 reads cell 0209AC30")
    check_ins(0x564C40, "mov qword ptr [rbx + rcx], rax")
    check_ins(0x564B3F, "mov ecx, 0x188")
    check_ins(0x564B44, "mov rdx, r9")
    check_ins(0x564B47, "cmovg ecx, r10d")
    check_ins(0x564B4B, "call 0x244f50")
    need(rip_of(0x5651BE) == CELL, "005651BE reads cell 0209AC30")
    check_ins(0x5651C5, "mov rcx, qword ptr [rax + r9*8 + 0x170]")
    check_ins(0x5650E6, "mov rcx, qword ptr [rbx + 0xc0]")
    check_ins(0x5650ED, "call 0x247950")
    check_ins(0x24795C, "cmp qword ptr [rcx + 0x10], 0")
    check_ins(0x247963, "and dword ptr [rcx + 0x40], 0xfffffffd")
    check_ins(0x5650BC, "mov qword ptr [rbx + 0xd8], rcx")
    check_ins(0x5650F2, "mov rcx, qword ptr [rbx + 0xd8]")
    check_ins(0x5650FE, "call 0x2d45c0")
    check_ins(0x2D45FB, "mov edx, dword ptr [rbx + 0x40]")
    check_ins(0x2D460A, "mov eax, dword ptr [rbx + 0x7c]")
    check_ins(0x2D4622, "mov rbx, qword ptr [rbx + 0x10]")
    verdict[0x564E10] = ("a Widget held at +0xC0 of a 0x188-byte widget (handlers 005636F0 / 00563930 / 00563B10 / "
                         "00563D20 over 005651E0; Manager0209AC60 +0x170 + i*8)",
                         "a peer Widget: cross-linked through +0xD8 and walked by 002D45C0 as a widget (+0x10 parent, "
                         "+0x40 flags, +0x7C)",
                         "qword store at +0xD0 of the peer widget")

    # B11 007DACF0
    p("- 007DACF0 (007DAD95)")
    cs = show_callers(0x7DACF0)
    need([c[0] for c in cs] == [0x7DACDE], "007DACF0's only site is 007DACDE")
    check_ins(0x7DACC7, "lea rax, [rcx + 0x40]")
    check_ins(0x7DACD9, "mov qword ptr [rsp + 0x20], rax")
    q = abs_qwords(0x7DACC0)
    need(q == [0x1CB7988] and not callers(0x7DACC0), "007DACC0 is reached only through the vtable slot 01CB7988")
    nm, offs = rtti_name(0x1CB7970)
    p("    vtable 01CB7970 (slot 3 = 007DACC0): %s, COL offset %d" % (nm, offs))
    need(nm == "AVHilbertFilter@Driver@Sd@SQEX@@" or nm.endswith("HilbertFilter@Driver@Sd@SQEX@@"), "RTTI HilbertFilter")
    verdict[0x7DACF0] = ("no +0xC0 field load: `[rsp + 0xc0]` is the fifth (stack) argument",
                         "007DACC0's receiver + 0x40, a SQEX::Sd::Driver::HilbertFilter method (vtable slot)",
                         "float stores into the filter's own state")

    # B12 007E01F0
    p("- 007E01F0 (007E0504)")
    cs = show_callers(0x7E01F0)
    need([c[0] for c in cs] == [0x7B0306], "007E01F0's only site is 007B0306")
    p("      rcx at 007B0306: %s" % fmt(prov_at(0x7B0306, "rcx")))
    need(rip_of(0x7B02F1) == 0x2EAD2F0, "007B02F1 reads the list head 02EAD2F0")
    check_ins(0x7AF44C, "mov qword ptr [rcx + 0x20], r9")
    check_ins(0x7AF455, "mov qword ptr [r9 + 0x20], r8")
    need(rr[0x2EAD2D0] == [0x7AEC90, 0x7AF2F3], "the list object 02EAD2D0 is named by two rip operands, 007AEC90 and 007AF2F3")
    check_ins(0x7AF2FA, "call 0x7aee20")
    check_ins(0x7AEE5A, "xor ebp, ebp")
    check_ins(0x7AEEF1, "mov qword ptr [rax + 0x20], rbp")
    check_ins(0x7B0311, "mov rbx, qword ptr [rbx + 0x10]")
    check_ins(0x7AF440, "mov qword ptr [r9 + 0x10], rax")
    check_ins(0x7AEC99, "call 0x7af380")
    check_ins(0x7AEC8D, "mov r8, rbx")
    check_ins(0x7AEC57, "call 0x7dff20")
    check_ins(0x7AEC5C, "mov rbx, rax")
    need(rip_of(0x7DFF26) == 0x1CB82D0, "007DFF20 installs vtable 01CB82D0")
    nm, offs = rtti_name(0x1CB82D0)
    p("    vtable 01CB82D0: %s, COL offset %d" % (nm, offs))
    need("CoreSubmixVoice@Core@Driver@Sd@SQEX@@" in nm, "RTTI CoreSubmixVoice")
    check_ins(0x7DFF63, "mov qword ptr [rbx + 0xc0], rax")
    check_ins(0x7AEC80, "mov rcx, rbx")
    check_ins(0x7AEC88, "call 0x7e0130")
    check_ins(0x7E013F, "mov rbx, rcx")
    check_ins(0x7E01A4, "add rbx, 0xb8")
    check_ins(0x7E01AB, "mov edi, 2")
    check_ins(0x7E01C5, "call 0x7ad460")
    check_ins(0x7E01CA, "mov qword ptr [rbx], rax")
    check_ins(0x7E01CD, "lea rbx, [rbx + 8]")
    for s in (0x7B1763, 0x7B1982, 0x7B1CC6, 0x7B203F):
        check_ins(s, "xor r8d, r8d")
    verdict[0x7E01F0] = ("SQEX::Sd::Driver::Core::CoreSubmixVoice (RTTI), payload of the list 02EAD2D0",
                         "a per-channel buffer from 007AD460 (007E0130, second of two slots +0xB8/+0xC0)",
                         "xmm store at +0x10 of that buffer")
    p()

    # ---------------- controls
    p("## Controls")
    crr = types.get("CharacterRenderRecord")
    crr_inst = crr[3] if crr else ""
    need("022C6F28" in crr_inst and "0x740" in crr_inst, "types.tsv CharacterRenderRecord instance names 022C6F28 and 0x740")

    def is_crr(ch):
        return any(k == "plus-cell" and v == 0x22C6F28 for k, v, a in ch) and any(k == "stride" and v == 0x740 for k, v, a in ch)

    for s in (0x2E29E9, 0x2E33B3):
        ch = prov_at(s, store_base(s)[0])
        p("  P1 %08X: %s -> %s" % (s, fmt(ch), "CharacterRenderRecord" if is_crr(ch) else "not CRR"))
        need(is_crr(ch), "P1 %08X traced to the CRR pool" % s)
    fired = [s for s, ch in chains.items() if is_crr(ch)]
    p("  P1 rule on the 17 stores: fires on %d" % len(fired))
    need(not fired, "P1 rule fires on none of the 17")
    asr = types.get("ActorStorageRecord")
    need(asr is not None and "00358940" in "\t".join(asr), "types.tsv ActorStorageRecord names 00358940 as the record lookup")
    ch = prov_at(0x225D86, "rbx")
    p("  P2 00225D86 `%s`: rbx = %s" % (text(ins_at(0x225D86)), fmt(ch)))
    need(ch[-1][:2] == ("call", 0x358940), "P2 roots in the return of 00358940 (ActorStorageRecord)")
    p("      rcx at 00225D56: %s" % fmt(prov_at(0x225D56, "rcx")))
    check_ins(0x358955, "mov rax, qword ptr [r8 + rax*8 + 8]")
    need(rip_of(0x263FF3) == 0x2098E10, "00263FF0 returns the manager slot table 02098E10 + i*0x288")
    bad = [s for s, c in chains.items() if any(k == "call" and v == 0x358940 for k, v, a in c)
           or any(k in ("cell", "cell-address") and 0x2098E10 <= v < 0x2098E10 + 0x288 * 5 for k, v, a in c)]
    need(not bad, "no chain of the 17 reaches the actor record lookup or the manager slot table")
    ch = prov_at(0x406C45, "rbx")
    p("  N1 00406C45 `%s`: rbx = %s" % (text(ins_at(0x406C45)), fmt(ch)))
    need(ch[-1][:3] == ("arg", 0, 0x406A60), "N1 receiver is 00406A60's first argument")
    registration(0x406A60, 0x4051C4, "mov ecx, 0xf0", 0x4051C9, "jmp 0x244f50", 0x4051BD)
    need(rip_of(0x4051B0) == 0x2B62D88, "004051B0 guards on slot 02B62D88")
    type_row("WidgetSingleton02B62D88", ["0xF0", "00406A60"])
    fr = field_row("WidgetSingleton02B62D88", 0xC0)
    need(fr is not None and "00406C45" in fr[5], "fields.tsv WidgetSingleton02B62D88 +0xC0 cites 00406C45")
    p("  N1 -> Widget 0xF0, handler 00406A60, slot 02B62D88 = type store WidgetSingleton02B62D88 (not ActorStorageRecord)")
    p()

    # ---------------- table
    p("## Result table")
    p("| body | stores | receiver of the +0xC0 load | what +0xC0 holds (the stored-to object) | stores land in | verdict |")
    p("|---|---|---|---|---|---|")
    for b in bodies:
        ss = ", ".join("%08X" % s for s, fn, ld in rows if fn == b)
        r, h, l = verdict[b]
        p("| %08X | %s | %s | %s | %s | not an ActorStorageRecord: cannot reach CRR +0x0C1 |" % (b, ss, r, h, l))
    p()
    p("bodies decided: %d of %d; ActorStorageRecord receivers: 0" % (len(verdict), len(bodies)))
    need(sorted(verdict) == bodies, "every body has a verdict")
    p()
    p("FAILS %d %s" % (len(FAILS), FAILS))
    with open(os.path.join(HERE, "c0_receivers.out"), "w", encoding="utf-8") as f:
        f.write("\n".join(OUT) + "\n")


main()
