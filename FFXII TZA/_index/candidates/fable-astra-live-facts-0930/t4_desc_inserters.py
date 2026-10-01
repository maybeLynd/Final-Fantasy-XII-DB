"""T4 / BL-8: an inverted inserter census for PClassDescriptor's list heads +0x60 and +0xB0 (FABLE reader, 2026-09-29).
Run:  python t4_desc_inserters.py > t4_desc_inserters.out

Instead of looking for writes AT +0x60/+0xB0, this looks for the one thing every insertion into a circular
doubly-linked sentinel list must do: a store of the head's address INTO the node, paired with a store of the node's
address INTO the head (head.next = node or head.prev = node). Two insert directions, same two stores:
    [N + a] = H   and   [H + b] = N,   a, b in {0, 8},  N != H.
Symbols: each register write creates a new version (linear decode of every listed function, call clobbers
volatile registers). A value is a register version, or an absolute address when the register came from lea rip.
A rip-relative store targets an absolute address. The head H is then classified by how it was formed:
  lea r,[B + D]      -> inline insert into list offset D of object B
  abs X              -> inline insert into a static head X (checked against the 315 static descriptors + D)
  entry arg rcx/rdx/r8/r9 unmodified -> a HEAD-INSERT HELPER; its call sites are then resolved for the head argument.
Pairs whose H and N were both loaded from memory are unlinks or relinks and are counted, not classified.
Also: every stored qword (DIR64 reloc) equal to S + 0x60/0x68/0xB0/0xB8 for a static descriptor S (a statically
initialised node pointing at the head).
Positive controls: the inline +0x80 insert in 0062EFD0 (0062F051 / 0062F059); the rip-formed insert into PNamespace's
descriptor +0xA0 in 00635980 (006359FB / 00635A13, head 02CF8A20); the helper 006B67D0 (annotation add, head in rcx)
and its call sites resolving to +0x38 of data members."""
import json, os, bisect, collections
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
HERE = os.path.dirname(os.path.abspath(tk.__file__))
IDX = json.load(open(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "tools", "rawcalls.json")))
STAT = [int(x, 16) for x in open(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "_index", "candidates", "bl8-b0-nas-review-opus",
                                             "descriptor-statics.txt")).read().replace("\n", ",").split(",") if x.strip()]
STATSET = set(STAT)
FAM = {}
for r64, subs in {"rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh", "rsi": "esi si sil",
                  "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    FAM[r64] = r64
    for s in subs.split(): FAM[s] = r64
for n in range(8, 16):
    for suf in ("", "d", "w", "b"): FAM["r%d%s" % (n, suf)] = "r%d" % n
def fam(r): return FAM.get(r, r)
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ARGS = ("rcx", "rdx", "r8", "r9")
def ripT(x, op): return x.address + x.size + op.mem.disp
def desc_of(addr):
    """static descriptor S and offset if addr lies within S..S+0x100"""
    i = bisect.bisect_right(STAT, addr) - 1
    if i >= 0 and addr - STAT[i] < 0x100: return STAT[i], addr - STAT[i]
    return None
STAT.sort()
def analyze(fn, ins):
    ver = collections.Counter(); prov = {}
    cur = {}
    def newv(r, p):
        ver[r] += 1; v = (r, ver[r]); cur[r] = v; prov[v] = p; return v
    for r in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
        newv(r, ("arg", r) if r in ARGS else ("entry", r))
    def val(r):
        v = cur[fam(r)]; p = prov[v]
        return ("abs", p[1]) if p[0] == "rip" else ("v", v)
    stores = []
    for x in ins:
        mn = x.mnemonic; ops = x.operands
        if mn in ("call",):
            for r in VOL: newv(r, ("call", x.address))
            continue
        # stores of a register value to memory
        if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG and ops[0].size == 8:
            m = ops[0].mem
            if m.base and x.reg_name(m.base) == "rip":
                tgt = ("abs", ripT(x, ops[0]), 0)
            elif m.base and not m.index:
                b = x.reg_name(m.base)
                if fam(b) == "rsp": tgt = None
                else:
                    bv = val(b); tgt = (bv[0], bv[1], m.disp) if bv[0] == "v" else ("abs", bv[1] + m.disp, 0)
            else: tgt = None
            if tgt: stores.append((x.address, tgt, val(x.reg_name(ops[1].reg))))
        # register definitions
        if ops and ops[0].type == X86_OP_REG and mn not in ("cmp", "test", "push", "bt"):
            r = fam(x.reg_name(ops[0].reg))
            if mn == "lea" and ops[1].mem.base and x.reg_name(ops[1].mem.base) == "rip":
                newv(r, ("rip", ripT(x, ops[1])))
            elif mn == "lea" and ops[1].mem.base and not ops[1].mem.index:
                b = fam(x.reg_name(ops[1].mem.base)); newv(r, ("lea", cur[b], prov[cur[b]], ops[1].mem.disp))
            elif mn == "mov" and ops[1].type == X86_OP_REG and ops[0].size == 8:
                cur[r] = cur[fam(x.reg_name(ops[1].reg))]
            elif mn == "add" and ops[1].type == X86_OP_IMM and ops[0].size == 8:
                old = cur[r]; newv(r, ("lea", old, prov[old], ops[1].imm))
            elif mn == "mov" and ops[1].type == X86_OP_MEM:
                m = ops[1].mem
                newv(r, ("load", x.address, ripT(x, ops[1]) if m.base and x.reg_name(m.base) == "rip" else None))
            elif mn == "xchg":
                newv(r, ("other", x.address))
            else:
                newv(r, ("other", x.address))
    # pairs
    out = []
    for a1, t1, v1 in stores:          # [N + a] = H
        for a2, t2, v2 in stores:      # [H + b] = N
            if a1 == a2: continue
            if t1[0] == "v" and t1[2] in (0, 8): N = ("v", t1[1]); na = t1[2]
            elif t1[0] == "abs": N = None; na = None
            else: continue
            H = v1
            # target of store 2 must be H + b
            if H[0] == "v":
                if not (t2[0] == "v" and t2[1] == H[1] and t2[2] in (0, 8)): continue
            else:
                if not (t2[0] == "abs" and t2[1] - H[1] in (0, 8)): continue
            # value of store 2 must be N
            if t1[0] == "v":
                if v2 != N: continue
            else:
                if not (v2[0] == "abs" and t1[1] - v2[1] in (0, 8)): continue
            if H == v2: continue
            out.append((a1, a2, H, v2))
    return out, prov
def hclass(H, prov):
    if H[0] == "abs":
        dd = desc_of(H[1])
        return ("static-head", H[1], "static descriptor %08X +%#x" % dd if dd else "not a static descriptor")
    p = prov[H[1]]
    if p[0] == "lea":
        return ("lea", p[3], "base %s" % (p[2][0] + ("(" + str(p[2][1]) + ")" if len(p[2]) > 1 else "")))
    if p[0] == "arg": return ("helper", p[1], "")
    if p[0] == "load": return ("load", None, "loaded at %08X%s" % (p[1], " from %08X" % p[2] if p[2] else ""))
    return (p[0], None, "")
res = collections.defaultdict(list); helpers = {}
for e, sz in tk.flist:
    if sz <= 0 or not (0x121000 <= e < 0x8C2000): continue
    try: ins = tk.fdis(e)
    except Exception: continue
    pairs, prov = analyze(e, ins)
    seen = set()
    for a1, a2, H, N in pairs:
        c = hclass(H, prov)
        key = (a1, a2)
        if key in seen: continue
        seen.add(key)
        res[c[0]].append((e, a1, a2, c))
        if c[0] == "helper": helpers.setdefault(e, set()).add(c[1])
print("== pair counts by head class:", {k: len(v) for k, v in res.items()})
print("\n== inline register-formed heads (lea [B + D]) by D:")
byD = collections.defaultdict(list)
for e, a1, a2, c in res["lea"]: byD[c[1]].append((e, a1, a2, c[2]))
print("  ", sorted((("%#x" % k) if k >= 0 else str(k), len(v)) for k, v in byD.items() if 0 <= k <= 0x200)[:60])
for D in (0x60, 0x68, 0xB0, 0xB8):
    print("  D=%#x:" % D)
    for e, a1, a2, b in byD.get(D, []): print("     %s  stores %08X / %08X  %s" % (tk.fname(e), a1, a2, b))
ok80 = any(e == 0x0062EFD0 for e, a1, a2, b in byD.get(0x80, []))
print("CONTROL +0x80 inline insert 0062EFD0 found:", ok80, [("%08X" % a1, "%08X" % a2) for e, a1, a2, b in byD.get(0x80, []) if e == 0x0062EFD0])
print("   D=0x90 pairs: %d functions %d ; D=0xA0 pairs: %d functions %d" % (len(byD.get(0x90, [])), len(set(e for e, *_ in byD.get(0x90, []))),
      len(byD.get(0xA0, [])), len(set(e for e, *_ in byD.get(0xA0, [])))))
print("\n== static (rip-formed) heads:")
for e, a1, a2, c in res["static-head"]:
    print("   %s  stores %08X / %08X  head %08X  %s" % (tk.fname(e), a1, a2, c[1], c[2]))
okNS = any(e == 0x00635980 and c[1] == 0x02CF8A20 for e, a1, a2, c in res["static-head"])
print("CONTROL rip-formed insert into PNamespace descriptor +0xA0 (00635980, head 02CF8A20) found:", okNS)
# Descriptor typing for static heads without relying on the 315-list alone: an object O is descriptor-shaped if it is
# a listed static descriptor, or if some inline static insert uses O+0x80, O+0x90 or O+0xA0 as a head (the filled lists).
# abs-abs pairs are symmetric, so both orientations are already in res["static-head"].
all_abs = set(c[1] for e, a1, a2, c in res["static-head"])
shaped = set()
for X in all_abs:
    for D in (0x80, 0x90, 0xA0): shaped.add(X - D)
shaped_real = {O for O in shaped if sum((O + D) in all_abs for D in (0x80, 0x90, 0xA0)) >= 2}   # two filled lists on one object
print("objects with an inline static insert at +0x80/+0x90/+0xA0:", len(shaped_real), "; in the 315 static list:",
      len(shaped_real & STATSET), "; PNamespace 02CF8980 among them:", 0x02CF8980 in shaped_real)
hits_static = []
for X in sorted(all_abs):
    for D in (0x60, 0x68, 0xB0, 0xB8):
        O = X - D
        if O in STATSET or O in shaped_real:
            hits_static.append(("%08X" % X, "object %08X +%#x" % (O, D), [("%08X" % e, "%08X/%08X" % (a1, a2)) for e, a1, a2, c in res["static-head"] if c[1] == X]))
print("static-head inserts whose head is +0x60/+0x68/+0xB0/+0xB8 of a descriptor-typed object:", hits_static)
print("\n== head-insert helpers (head is an unmodified entry argument): %d" % len(helpers))
FWD = {}
def resolve_arg(site, reg):
    fn, _ = tk.owner(site)
    if fn is None or tk.fsize(fn) is None: return ("?", "unowned")
    ins = tk.fdis(fn); i = next((k for k, y in enumerate(ins) if y.address == site), None)
    if i is None: return ("?", "off-boundary")
    want = reg
    for j in range(i - 1, max(-1, i - 30), -1):
        y = ins[j]
        if y.mnemonic == "call": return ("?", "call before")
        if not y.operands or y.operands[0].type != X86_OP_REG or fam(y.reg_name(y.operands[0].reg)) != want: continue
        if y.mnemonic in ("cmp", "test"): continue
        if y.mnemonic == "lea" and y.operands[1].mem.base:
            b = y.reg_name(y.operands[1].mem.base)
            if b == "rip":
                t = ripT(y, y.operands[1]); dd = desc_of(t)
                return ("abs", t, ("static descriptor %08X +%#x" % dd) if dd else "")
            return ("lea", y.operands[1].mem.disp, "%08X %s %s" % (y.address, y.mnemonic, y.op_str))
        if y.mnemonic == "mov" and y.operands[1].type == X86_OP_REG:
            want = fam(y.reg_name(y.operands[1].reg)); continue
        if y.mnemonic == "add" and y.operands[1].type == X86_OP_IMM:
            return ("add", y.operands[1].imm, "%08X %s %s" % (y.address, y.mnemonic, y.op_str))
        return ("other", "%08X %s %s" % (y.address, y.mnemonic, y.op_str))
    return ("?", "window")
hcalls = {}
for h, regs in sorted(helpers.items()):
    sites = [int(s, 16) for s in IDX.get("%X" % h, [])]
    dist = collections.Counter(); hit = []
    for s in sites:
        for r in regs:
            v = resolve_arg(s, r)
            key = ("%s %#x" % (v[0], v[1])) if v[0] in ("lea", "add") else (("abs " + (v[2] or "%08X" % v[1])) if v[0] == "abs" else v[0])
            dist[key] += 1
            if (v[0] in ("lea", "add") and v[1] in (0x60, 0x68, 0xB0, 0xB8)) or (v[0] == "abs" and v[2] and int(v[2].split("+")[1], 16) in (0x60, 0x68, 0xB0, 0xB8)):
                hit.append(("%08X" % s, tk.fname(s), v))
    hcalls[h] = (sites, dist, hit)
    print("  helper %s head-arg %s, %d raw call sites; head forms: %s" % (tk.fname(h), sorted(regs), len(sites), dict(dist.most_common(8))))
    if h != 0x006B67D0:
        for s in sites:
            for r in regs: print("      site %08X in %s: %s" % (s, tk.fname(s), resolve_arg(s, r)))
    else:
        typed = [(s, resolve_arg(s, r)) for s in sites for r in regs]
        bad = [(("%08X" % s), v) for s, v in typed if v[0] == "abs" and any((v[1] - D) in (STATSET | shaped_real) for D in (0x60, 0x68, 0xB0, 0xB8))]
        print("      006B67D0 sites resolved to an absolute head: %d of %d; any at +0x60/+0x68/+0xB0/+0xB8 of a descriptor-typed object: %s"
              % (sum(1 for s, v in typed if v[0] == "abs"), len(typed), bad))
    for z in hit: print("      HEAD AT +0x60/+0x68/+0xB0/+0xB8: %s" % (z,))
ok_ann = 0x006B67D0 in helpers
d_ann = hcalls.get(0x006B67D0, ([], collections.Counter(), []))[1]
print("CONTROL helper 006B67D0 detected:", ok_ann, "; its head forms:", dict(d_ann))
print("\n== forward value census: every lea r,[B + D] whose register VALUE is stored to memory other than its own self-link,")
print("   or passed in an argument register to a direct call of a detected helper at that helper's head argument")
def forward(D):
    out = []
    for e, sz in tk.flist:
        if sz <= 0 or not (0x121000 <= e < 0x8C2000): continue
        ins = tk.fdis(e)
        for i, x in enumerate(ins):
            if x.mnemonic != "lea" or not x.operands[1].mem.base or x.operands[1].mem.index or x.operands[1].mem.disp != D: continue
            b = x.reg_name(x.operands[1].mem.base)
            if b in ("rip", "rsp", "rbp"): continue
            r = fam(x.reg_name(x.operands[0].reg)); live = {r}
            for y in ins[i + 1:i + 40]:
                ops = y.operands
                if y.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG and fam(y.reg_name(ops[1].reg)) in live:
                    m = ops[0].mem
                    selfl = m.base and fam(y.reg_name(m.base)) in live and m.disp in (0, 8)
                    if not selfl and not (m.base and y.reg_name(m.base) == "rsp"): out.append((e, x.address, y.address, "stored: %s %s" % (y.mnemonic, y.op_str)))
                if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"):
                    t = int(y.op_str, 16)
                    if t in helpers and live & helpers[t]: out.append((e, x.address, y.address, "passed to helper %08X" % t))
                    if y.mnemonic == "call": live -= set(VOL)
                if y.mnemonic == "ret": break
                if ops and ops[0].type == X86_OP_REG and y.mnemonic not in ("cmp", "test", "push"):
                    rr = fam(y.reg_name(ops[0].reg))
                    if y.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_REG and fam(y.reg_name(ops[1].reg)) in live: live.add(rr)
                    else: live.discard(rr)
                if not live: break
    return out
for D in (0x90, 0x60, 0xB0):
    f = forward(D)
    print("  D=%#x: %d sites in %d functions" % (D, len(f), len(set(z[0] for z in f))))
    if D != 0x90:
        for e, a, s, why in f: print("     %s  lea %08X -> %08X %s" % (tk.fname(e), a, s, why))

print("\n== stored qword pointers (DIR64 relocs) to S+0x60/0x68/0xB0/0xB8 of a static descriptor:")
want = set()
for S in STAT:
    for o in (0x60, 0x68, 0xB0, 0xB8): want.add(S + o)
rl = [(a, tk.u64(a)) for a in tk.relocs() if tk.u64(a) in want]
print("  ", [("%08X" % a, "%08X" % q) for a, q in rl])
ctl = [(a, tk.u64(a)) for a in tk.relocs() if tk.u64(a) in {S + 0xA0 for S in STAT} | {S + 0x90 for S in STAT} | {S + 0x80 for S in STAT}]
print("  control: the same reloc test at +0x80/+0x90/+0xA0: %d hits %s" % (len(ctl), [("%08X" % a, "%08X" % q) for a, q in ctl[:8]]))
print("\nstatic descriptors loaded:", len(STAT))
