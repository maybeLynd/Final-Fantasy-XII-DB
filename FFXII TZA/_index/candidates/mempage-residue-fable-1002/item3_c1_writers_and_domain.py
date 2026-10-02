"""item3_c1_writers_and_domain.py - CharacterRenderRecord +0x0C1: (a) every writer, (b) the domain of the nibble it
carries (FABLE, 2026-10-02). Static, read-only.

Question (memory page, "The closure qualified"): OPUS showed 002E28E0 and 002E3110 store a source byte's upper
nibble at +0x0C1 (002E29E9, 002E33B3). Open: (a) other writers, including wider stores and other base registers;
(b) can the source byte's bits 5..7 be set (an accounting index of 2 or more)?

(a) Method
  A1  image-wide width-aware store sweep: every instruction in every listed body that WRITES memory (capstone
      access flags) through a base register other than rsp/rip, with displacement d and operand width w such that
      d <= 0xC1 < d + w. Widths: byte d=0xC1; word d=0xC0; dword d=0xBE..0xC1; qword d=0xBA..0xC1; xmm d=0xB2..0xC1;
      ymm d=0xA2..0xC1. A displacement sweep returns every type in the image, so each hit is then tested for being a
      CharacterRenderRecord store: its body appears in the published CRR receiver census
      (17-Presentation-Rendering/Character-Render-Records/character-render-record-accesses.tsv, cell + ctor seeds,
      CFG fixpoint), or the body indexes the 0x740-stride pool (imul by 0x740, or the pool cell 022C6F28).
  A2  bulk writers in those CRR bodies: rep stos / rep movs, and calls to the memset / memcpy import thunks
      (resolved through the import directory) - a zeroing or copying writer covers +0x0C1 without naming it.
  Controls: K1 both known byte stores (002E29E9, 002E33B3) are found and tagged CRR; K2 sensitivity to width: the
  same coverage test asked for byte 0xBF must find ResetDefaults' dword store at +0xBC (0041F80A); K3 the bulk scan
  must find ResetDefaults' 0x740 memset (0041F754).

(b) Method
  B1  the source byte is byte +0x10 of a SecondaryContext element (actor +0xC0 points at the context; six 0x30-byte
      elements). The only instruction that ORs a value into its upper nibble found by B2 is 002EBC90 (`shl r8b, 4` /
      `or byte ptr [rcx + 0x10], r8b`). Census of its raw call sites (E8/E9/jcc) and pointer routes; the r8 value
      each site passes (last writer of r8 in the block).
  B2  every store whose byte range covers an element's byte +0x10, found three ways and unioned:
        - a linear (no-CFG) register tracker in every body that loads a qword at +0xC0, or calls a small getter that
          returns one (002E97B0 and its kind): a register holding that
          pointer plus a constant (mov / lea / add imm) is followed to each store; the +0xC0 load site is printed;
        - the published SecondaryContext context and element censuses (their write sites are receiver-proven);
        - the actor storage record census, for stores reaching the inline context (record +0x350) through the
          record itself (record +0x340..+0x47F).
      Each store is classified: AND (clears only), immediate (its byte at the element offset), a byte register (a
      backward bit-mask evaluation of the register's writers in the block: and/or/shl/add-self/set*), or WIDE/OTHER.
  B3  002E3110's own read: the `and byte ptr [rbx + 0x10], 0xf` at 002E3315 lies on every path to the read at
      002E3367; the calls in between (00269D60, 002E8FD0, 0042FB80) are checked through their transitive callee
      closure (edges.tsv plus raw E8/E9 of each body) for 002EBC90 and for the B2 setters.
  Control K4: B1 must find 0026DF40's six calls (the published "six-clear pass", five calls and one tail jump).
"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp_lib import *
from capstone.x86 import X86_REG_R8, X86_REG_R8D, X86_REG_R8W, X86_REG_R8B

CRR_TSV = os.path.join(DBROOT, "FFXII TZA", "17-Presentation-Rendering", "Character-Render-Records", "character-render-record-accesses.tsv")
SCX_TSV = os.path.join(DBROOT, "FFXII TZA", "04-Actor-Entity", "Actor-Contexts", "secondary-context-element-accesses.tsv")
SCX_ALL = os.path.join(DBROOT, "FFXII TZA", "04-Actor-Entity", "Actor-Contexts", "secondary-context-accesses.tsv")
SETTER = 0x2EBC90
GETTERS = set()
# hand readings, each re-checked against the bytes: site -> (reason, [(address, exact instruction)])
MANUAL = {
    0x25E37E: ("sil is 0 or 1 here: ebp is zeroed at entry and set to 1 only after esi is computed; every path to "
               "0025E373 passes `mov esi, ebp` at 0025E255 (the region 0025E256..0025E373 has no entry from outside, and "
               "the body's backward jumps all lie before it), and the only later write is `and esi, 1`; so `shl al, 2` "
               "gives bit 2 only",
               [(0x25DF1F, "xor ebp, ebp"), (0x25E255, "mov esi, ebp"), (0x25E363, "mov esi, eax"), (0x25E367, "and esi, 1"),
                (0x25E36E, "mov ebp, 1"), (0x25E377, "movzx eax, sil"), (0x25E37B, "shl al, 2")]),
    0x3B7833: ("r12 is 1: it is set once, before the loop head 003B77A7, from r15 = 0 (r15 is the loop counter, "
               "incremented at 003B7845 only after); r12's only other write is the epilogue pop 003B786E; so "
               "`and bl, r12b` / `add bl, bl` gives bit 1 only",
               [(0x3B77A0, "xor r15d, r15d"), (0x3B77A3, "lea r12d, [r15 + 1]"), (0x3B7845, "inc r15d"),
                (0x3B786E, "pop r12"), (0x3B782E, "and bl, r12b"), (0x3B7831, "add bl, bl")]),
}
R8 = {X86_REG_R8, X86_REG_R8D, X86_REG_R8W, X86_REG_R8B}
fails = []


def covering_stores(target, fns):
    hits = []
    for fn in fns:
        for x in decode(fn):
            for op in x.operands:
                if op.type != X86_OP_MEM or not (op.access & CS_AC_WRITE):
                    continue
                if op.mem.base in (0, X86_REG_RIP) or reg_name(op.mem.base) == "rsp":
                    continue
                dsp, w = op.mem.disp, op.size
                if dsp <= target < dsp + w:
                    hits.append((x.address, fn, w, x.mnemonic, x.op_str))
    return hits


def crr_bodies():
    s, sites = set(), set()
    for row in csv.DictReader(open(CRR_TSV, encoding="utf-8"), delimiter="\t"):
        try:
            s.add(int(row["function"], 16)); sites.add(int(row["site"], 16))
        except (KeyError, ValueError):
            pass
    return s, sites


def pool_indexer(fn):
    for x in decode(fn):
        if x.mnemonic == "imul" and x.op_str.endswith("0x740"):
            return True
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == 0x22C6F28:
                return True
    return False


def last_r8(ins, k):
    for j in range(k - 1, -1, -1):
        y = ins[j]
        if y.mnemonic in ("call", "ret") or y.mnemonic.startswith("j"):
            return None
        try:
            w = set(y.regs_access()[1])
        except Exception:
            w = set()
        if w & R8:
            return y
    return None


def main():
    out = []
    p = out.append
    p("# item 3 - CharacterRenderRecord +0x0C1 writers and the nibble domain (static). run: item3_c1_writers_and_domain.py at %s" % head_sha())
    allf = all_functions()
    crr, crr_sites = crr_bodies()
    p("\n## (a) A1 width-aware store sweep for byte 0xC1, %d listed bodies; CRR receiver census bodies: %d" % (len(allf), len(crr)))
    hits = covering_stores(0xC1, allf)
    p("  stores covering 0xC1 (any type): %d in %d bodies; by width: %s" % (len(hits), len({h[1] for h in hits}),
      ", ".join("w%d=%d" % (w, sum(1 for h in hits if h[2] == w)) for w in sorted({h[2] for h in hits}))))
    crr_hits = []
    for h in hits:
        why = ("census SITE (receiver-proven CRR)" if h[0] in crr_sites else "census body, site not attributed to CRR") if h[1] in crr             else ("0x740 pool-indexer body" if pool_indexer(h[1]) else "")
        if why:
            crr_hits.append(h + (why,))
    p("  of those, in a CRR body (census or 0x740 pool indexer): %d" % len(crr_hits))
    for a, fn, w, m, s, why in crr_hits:
        p("    %08X in %08X %-44s w%d %s %s   [%s]" % (a, fn, names.get(fn, "")[:44], w, m, s, why))
    found = {h[0] for h in crr_hits}
    p("  receiver-proven CRR stores covering 0xC1: %d" % sum(1 for h in crr_hits if h[5].startswith("census SITE")))
    if not {0x2E29E9, 0x2E33B3} <= {h[0] for h in crr_hits if h[5].startswith("census SITE")}:
        fails.append("K1 known writers not found/tagged")
    k2 = covering_stores(0xBF, [0x41F730])
    p("  K2 width sensitivity: stores covering byte 0xBF in ResetDefaults 0041F730: %s" % ["%08X w%d %s %s" % (a, w, m, s) for a, fn, w, m, s in k2])
    if not any(a == 0x41F80A and w == 4 for a, fn, w, m, s in k2):
        fails.append("K2")
    # A2 bulk
    p("\n## (a) A2 bulk writers in CRR bodies (rep stos/movs; calls to the memset / memcpy import thunks)")
    memfns = {}
    for a, n in import_thunks({"memset", "memcpy", "memmove"}).items():
        if a in funcs or owner(a) is None or funcs.get(owner(a), 99) <= 8:
            memfns[a] = n
    p("  import thunks: %s" % ", ".join("%08X %s" % (a, n) for a, n in sorted(memfns.items())))
    bulk = []
    for fn in sorted(crr):
        if fn not in funcs:
            continue
        ins = decode(fn)
        for k, x in enumerate(ins):
            if x.mnemonic.startswith("rep") and ("stos" in x.mnemonic or "movs" in x.mnemonic):
                bulk.append((x.address, fn, x.mnemonic + " " + x.op_str, ""))
            if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and int(x.op_str, 16) in memfns:
                r8 = last_r8(ins, k)
                bulk.append((x.address, fn, x.mnemonic + " " + x.op_str, "r8<- %s %s" % (r8.mnemonic, r8.op_str) if r8 else "r8 not set in block"))
    for a, fn, s, r in bulk:
        p("  %08X in %08X %-40s %s  %s" % (a, fn, names.get(fn, "")[:40], s, r))
    if not any(a == 0x41F754 for a, *_ in bulk):
        fails.append("K3 ResetDefaults memset not seen")
    # (b) B1
    p("\n## (b) B1 the nibble setter 002EBC90 and the r8 value at each site")
    p("  body tail: " + " | ".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in decode(SETTER)[-5:]))
    r = raw_index([SETTER])[SETTER]
    vals = []
    for site, form, o, al in sorted(r):
        if not al:
            continue
        ins = decode(o)
        k = [i for i, x in enumerate(ins) if x.address == site][0]
        y = last_r8(ins, k)
        v = None
        if y is not None:
            ops = y.op_str.replace(" ", "")
            if y.mnemonic == "xor" and ops in ("r8d,r8d", "r8,r8"):
                v = 0
            elif y.mnemonic == "mov" and ops.startswith(("r8d,0x", "r8,0x")) or (y.mnemonic == "mov" and ops.split(",")[1].isdigit()):
                v = int(ops.split(",")[1], 0)
            elif y.mnemonic == "lea" and ops.startswith("r8d,[rdx"):
                # lea r8d, [rdx +/- n] with edx a constant set just before
                for j in range(k - 1, -1, -1):
                    z = ins[j]; zo = z.op_str.replace(" ", "")
                    if zo.startswith("edx,") and z.mnemonic in ("mov", "xor"):
                        base = 0 if z.mnemonic == "xor" else int(zo.split(",")[1], 0)
                        inner = ops[len("r8d,[rdx"):-1]
                        v = base + int(inner.replace("+", ""), 0) if inner else base
                        break
            elif y.mnemonic == "lea" and ops.startswith("r8d,[r8"):
                v = "lea-on-r8"
            elif y.mnemonic == "mov" and ops in ("r8d,edi", "r8d,edx"):
                # trace the source register once
                src = ops.split(",")[1]
                for j in range(k - 1, -1, -1):
                    z = ins[j]; zo = z.op_str.replace(" ", "")
                    if zo.startswith(src + ",") and z.mnemonic == "mov":
                        v = int(zo.split(",")[1], 0) if zo.split(",")[1].startswith("0x") or zo.split(",")[1].isdigit() else zo
                        break
        if v == "lea-on-r8":
            # lea r8d, [r8 + n] after xor r8d, r8d
            v = None
            for j in range(k - 1, -1, -1):
                z = ins[j]; zo = z.op_str.replace(" ", "")
                if z.mnemonic == "xor" and zo == "r8d,r8d":
                    v = int(y.op_str.replace(" ", "").split("+")[1].rstrip("]"), 0); break
        vals.append(v)
        p("  %-5s %08X in %08X %-34s r8 <- %s => nibble %s" % (form, site, o, names.get(o, "")[:34],
          "%08X %s %s" % (y.address, y.mnemonic, y.op_str) if y is not None else "not set in block", v))
    p("  sites: %d; nibble values: %s" % (len(vals), sorted({str(v) for v in vals})))
    if sum(1 for s, f, o, al in r if al and o == 0x26DF40) != 6:
        fails.append("K4 0026DF40 six sites")
    q = re.findall(re.escape(struct.pack("<Q", SETTER)), d); rv = re.findall(re.escape(struct.pack("<I", SETTER - BASE)), d)
    ripn = sum(1 for fn in allf for x in decode(fn) for op in x.operands
               if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == SETTER)
    p("  pointer routes to 002EBC90: absolute qwords %d, RVA dwords %d, rip operands %d" % (len(q), len(rv), ripn))
    # B2
    p("\n## (b) B2 stores to an element's byte +0x10 (element k at context + 0x30k) that could set bits 4..7")
    eld = {0x10 + 0x30 * k for k in range(6)}
    GPR = {}
    for full, al in (("rax", ("eax", "ax", "al", "ah")), ("rbx", ("ebx", "bx", "bl", "bh")), ("rcx", ("ecx", "cx", "cl", "ch")),
                     ("rdx", ("edx", "dx", "dl", "dh")), ("rsi", ("esi", "si", "sil")), ("rdi", ("edi", "di", "dil")),
                     ("rbp", ("ebp", "bp", "bpl"))):
        GPR[full] = full
        for a in al:
            GPR[a] = full
    for n in range(8, 16):
        for suf in ("", "d", "w", "b"):
            GPR["r%d%s" % (n, suf)] = "r%d" % n
    VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}

    def wfam(x):
        try:
            return {GPR.get(md.reg_name(r)) for r in x.regs_access()[1]} - {None}
        except Exception:
            return set()

    def ctx_stores(fn):
        """linear dataflow: registers holding (context pointer + c); returns stores whose c + disp covers an element +0x10."""
        tr, res, src = {}, [], {}
        for x in decode(fn):
            ops = x.op_str.replace(" ", "")
            for op in x.operands:
                if op.type == X86_OP_MEM and (op.access & CS_AC_WRITE) and op.mem.index == 0:
                    b = GPR.get(reg_name(op.mem.base))
                    if b in tr:
                        lo = tr[b] + op.mem.disp
                        hitb = [e for e in eld if lo <= e < lo + op.size]
                        if hitb:
                            res.append((x, op, hitb[0] - lo, src.get(b)))
            dst = GPR.get(ops.split(",")[0]) if "," in ops else None
            new = None
            if x.mnemonic == "mov" and dst and x.operands[1].type == X86_OP_MEM and x.operands[1].mem.disp == 0xC0 and x.operands[1].size == 8 \
                    and x.operands[1].mem.index == 0 and x.operands[1].mem.base != X86_REG_RIP:
                new = 0
            elif x.mnemonic == "lea" and dst and x.operands[1].mem.index == 0 and GPR.get(reg_name(x.operands[1].mem.base)) in tr:
                new = tr[GPR.get(reg_name(x.operands[1].mem.base))] + x.operands[1].mem.disp
            elif x.mnemonic == "mov" and dst and x.operands[1].type == X86_OP_REG and GPR.get(md.reg_name(x.operands[1].reg)) in tr \
                    and x.operands[0].size == 8:
                new = tr[GPR.get(md.reg_name(x.operands[1].reg))]
            elif x.mnemonic == "add" and dst in tr and x.operands[1].type == X86_OP_IMM:
                new = tr[dst] + x.operands[1].imm
            for f in wfam(x):
                tr.pop(f, None)
            if x.mnemonic == "call":
                for f in VOL:
                    tr.pop(f, None)
                if x.op_str.startswith("0x") and int(x.op_str, 16) in GETTERS:
                    tr["rax"] = 0; src["rax"] = x.address     # the getter returns the context pointer
            if new is not None and dst:
                tr[dst] = new
                if new == 0 and x.mnemonic == "mov":
                    src[dst] = x.address
                elif x.mnemonic in ("lea", "mov", "add"):
                    o1 = x.operands[1]
                    sreg = GPR.get(reg_name(o1.mem.base)) if o1.type == X86_OP_MEM else (GPR.get(md.reg_name(o1.reg)) if o1.type == X86_OP_REG else dst)
                    src[dst] = src.get(sreg, src.get(dst))
        return res

    def const_of(fn, reg):
        """a register's value when every write to it in the body is the same constant form."""
        vals = set()
        for x in decode(fn):
            if reg in wfam(x) and x.mnemonic != "pop":      # an epilogue restore is not a value the body computes
                ops = x.op_str.replace(" ", "")
                if x.mnemonic == "xor" and len(set(ops.split(","))) == 1:
                    vals.add(0)
                elif x.mnemonic == "mov" and x.operands[1].type == X86_OP_IMM:
                    vals.add(x.operands[1].imm)
                elif x.mnemonic == "lea" and x.operands[1].mem.index == 0:
                    b = GPR.get(reg_name(x.operands[1].mem.base))
                    bv = const_of(fn, b) if b and b != reg else None
                    vals.add(None if bv is None else bv + x.operands[1].mem.disp)
                else:
                    vals.add(None)
        return vals.pop() if len(vals) == 1 else None

    def src_mask(fn, ins, k, reg):
        """possible-bits mask of an 8-bit source register at ins[k], from its writers in the same block."""
        fam = GPR.get(reg)
        chain = []
        for j in range(k - 1, -1, -1):
            y = ins[j]
            if y.mnemonic in ("call", "ret") or y.mnemonic.startswith("j"):
                break
            if fam in wfam(y):
                chain.append(y)
                yo = y.op_str.replace(" ", "")
                if y.mnemonic in ("and", "or", "shl", "add", "shr") and yo.split(",")[0] in GPR and GPR[yo.split(",")[0]] == fam:
                    continue        # a transform: keep walking to its definer
                break
        if not chain:
            return 0xFF, "argument/unknown"
        mask = 0xFF
        steps = []
        for y in reversed(chain):
            yo = y.op_str.replace(" ", "")
            src = yo.split(",", 1)[1] if "," in yo else ""
            if y.mnemonic == "xor" and len(set(yo.split(","))) == 1:
                mask = 0
            elif y.mnemonic in ("mov", "movzx") and y.operands[1].type == X86_OP_IMM:
                mask = y.operands[1].imm & 0xFF
            elif y.mnemonic.startswith("set"):
                mask = 1
            elif y.mnemonic == "and" and y.operands[1].type == X86_OP_IMM:
                mask &= y.operands[1].imm & 0xFF
            elif y.mnemonic == "and" and y.operands[1].type == X86_OP_REG:
                c = const_of(fn, GPR.get(md.reg_name(y.operands[1].reg)))
                if c is not None:
                    mask &= c & 0xFF
            elif y.mnemonic == "or" and y.operands[1].type == X86_OP_IMM:
                mask |= y.operands[1].imm & 0xFF
            elif y.mnemonic == "shl" and y.operands[1].type == X86_OP_IMM:
                mask = (mask << y.operands[1].imm) & 0xFF
            elif y.mnemonic == "add" and len(set(yo.split(","))) == 1:
                mask = (mask << 1) & 0xFF
            else:
                mask = 0xFF
            steps.append("%s %s" % (y.mnemonic, y.op_str))
        return mask, " ; ".join(steps)

    loaders = [fn for fn in allf if any(x.mnemonic == "mov" and x.op_str.endswith("+ 0xc0]") and x.op_str.startswith("r")
                                        and "qword ptr [" in x.op_str for x in decode(fn))]
    # small getters whose only memory read is `mov rax, qword ptr [rcx + 0xc0]` (e.g. 002E97B0): their callers
    # receive the context pointer in rax, which a loader-only scan would not see
    for fn in loaders:
        if funcs[fn] <= 0x20:
            ins = decode(fn)
            reads = [x for x in ins if any(op.type == X86_OP_MEM and (op.access & CS_AC_READ) for op in x.operands)]
            if len(reads) == 1 and reads[0].op_str == "rax, qword ptr [rcx + 0xc0]" and not any(
                    x.mnemonic == "call" for x in ins):
                GETTERS.add(fn)
    gcallers = set()
    for t, lst in raw_index(GETTERS).items():
        for site, form, o, al in lst:
            if al and form == "call":
                gcallers.add(o)
    p("  context getters (body <= 32 bytes, sole read `mov rax, qword ptr [rcx + 0xc0]`): %s; bodies calling them: %d"
      % (", ".join("%08X" % g for g in sorted(GETTERS)), len(gcallers)))
    if 0x2E97B0 not in GETTERS:
        fails.append("getter 002E97B0 not recognised")
    loaders = sorted(set(loaders) | gcallers)
    rows = []
    for fn in loaders:
        for x, op, sh, ld in ctx_stores(fn):
            rows.append((x, fn, op, sh, "ctx-derived from %s" % ("%08X" % ld if ld else "?")))
    # union with the published censuses (their sites are receiver-proven)
    pub = []
    for path, rel in ((SCX_TSV, "element"), (SCX_ALL, "context")):
        for row in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
            if "w" not in row.get("kind", ""):
                continue
            try:
                site, fn = int(row["site"], 16), int(row["function"], 16)
            except (KeyError, ValueError):
                continue
            pub.append((site, fn, rel))
    have = {r[0].address for r in rows}
    added = 0
    for site, fn, rel in pub:
        if site in have or fn not in funcs:
            continue
        for x in decode(fn):
            if x.address != site:
                continue
            for op in x.operands:
                if op.type == X86_OP_MEM and (op.access & CS_AC_WRITE):
                    targets = eld if rel == "element" else eld
                    hitb = [e for e in targets if op.mem.disp <= e < op.mem.disp + op.size] if rel == "context" else \
                           ([0x10] if op.mem.disp <= 0x10 < op.mem.disp + op.size else [])
                    if hitb:
                        rows.append((x, fn, op, hitb[0] - op.mem.disp, "census-" + rel)); have.add(site); added += 1
    p("  bodies loading a qword at +0xC0: %d; ctx-derived element-byte stores: %d; added from the published context /"
      " element censuses: %d" % (len(loaders), len(rows) - added, added))
    verdicts = {}
    for x, fn, op, sh, how in sorted(rows, key=lambda r: r[0].address):
        m = x.mnemonic
        imm = [o.imm for o in x.operands if o.type == X86_OP_IMM]
        if m in ("and", "btr"):
            v, mask = "AND (clears only)", 0
        elif imm and m in ("or", "mov", "xor", "add", "bts"):
            mask = (imm[0] >> (8 * sh)) & 0xFF
            v = "IMM byte %#x" % mask
        elif m in ("inc", "dec", "sub", "add", "neg", "not"):
            v, mask = "ARITH", 0xFF
        else:
            srcs = [o for o in x.operands if o.type == X86_OP_REG]
            ins = decode(fn)
            k = [i for i, y in enumerate(ins) if y.address == x.address][0]
            if srcs and op.size == 1:
                mask, how2 = src_mask(fn, ins, k, md.reg_name(srcs[0].reg))
                v = "REG %s mask %#x [%s]" % (md.reg_name(srcs[0].reg), mask, how2)
            else:
                v, mask = "WIDE/OTHER", 0xFF
        hi = "bits4-7 %s" % ("POSSIBLE" if mask & 0xF0 else "clear")
        if x.address in MANUAL:
            why, cites = MANUAL[x.address]
            ok = all(any(y.address == a and ("%s %s" % (y.mnemonic, y.op_str)) == t for y in decode(fn)) for a, t in cites)
            if not ok:
                fails.append("manual cite %08X" % x.address)
            mask = 0 if ok else mask
            hi = "bits4-7 %s" % ("POSSIBLE" if mask & 0xF0 else "clear")
            v += " | READ BY HAND (%d cited instructions %s): %s" % (len(cites), "verified" if ok else "MISMATCH", why)
        verdicts[hi] = verdicts.get(hi, 0) + 1
        p("  %08X in %08X %-38s w%d %s %s  (%s)  %s -> %s" % (x.address, fn, names.get(fn, "")[:38], op.size, m, x.op_str, how, v, hi))
    p("  verdicts: %s" % verdicts)
    ASR = os.path.join(DBROOT, "FFXII TZA", "04-Actor-Entity", "Actor-Storage-Record", "actor-storage-record-accesses.tsv")
    n_all = n_ctx = 0
    for row in csv.DictReader(open(ASR, encoding="utf-8"), delimiter="	"):
        try:
            dd = int(row["disp"], 16)
        except (KeyError, ValueError):
            continue
        n_all += 1
        if 0x340 <= dd < 0x480:
            n_ctx += 1
    p("  actor storage record census: %d rows, %d at record +0x340..+0x47F (the inline context reached through the record)" % (n_all, n_ctx))
    setters = {fn for x, fn, op, sh, how in rows if True}
    # B3
    p("\n## (b) B3 002E3110: clear dominates the read; closure of the calls in between")
    for x in decode(0x2E3110):
        if 0x2E32DE <= x.address <= 0x2E33B3:
            p("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    edges = {}
    for line in open(EDGES, encoding="utf-8"):
        a = line.split("\t")
        try:
            edges.setdefault(int(a[0], 16), set()).add(int(a[1], 16))
        except ValueError:
            pass
    def callees(fn):
        s = set(edges.get(fn, ()))
        if fn in funcs:
            for x in decode(fn):
                if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                    t = int(x.op_str, 16)
                    if not (fn <= t < fn + funcs[fn]):
                        s.add(t)
        return s
    clos, todo = set(), [0x269D60, 0x2E8FD0, 0x42FB80]
    while todo:
        f = todo.pop()
        if f in clos:
            continue
        clos.add(f)
        todo.extend(callees(f) - clos)
    p("  closure of {00269D60, 002E8FD0, 0042FB80}: %d bodies; contains 002EBC90: %s; contains a B2 store body: %s" % (
        len(clos), SETTER in clos, sorted("%08X" % f for f in clos & setters) or "none"))
    p("\nFAILS %d %s" % (len(fails), fails))
    open(os.path.join(HERE, "item3_c1_writers_and_domain.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


import re
main()
