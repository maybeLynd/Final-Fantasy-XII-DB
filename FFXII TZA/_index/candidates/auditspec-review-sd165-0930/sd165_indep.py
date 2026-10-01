"""sd165_indep.py - SWE2-AUDIT-SPEC (2026-09-30): independent re-derivation of SD-165's null-test census.
arena_ix only (raw E8/E9/jcc index + capstone regs_access); no retool, no package code.

Part 1 - the entry points and their real call sites:
  every raw rel32 site of 0036A100, 0036A190 (mov edx,1; jmp 0036A1A0), 0036A1A0, 0036A230 (xor edx,edx; jmp 0036A1A0),
  0036B160 and the realloc 0036CAD0 (null pointer -> 0036D050 -> 0036BFE0), with DIR64 / rva32 stored pointers;
  a site that is a thunk's own `jmp` into 0036A1A0 is not a caller.
Part 2 - my classifier, same 24-instruction linear window as the package, but:
  K  kill: any write (capstone regs_access, any alias width, memory source included) to a register holding the value
     removes it unless the instruction is a copy of the value (mov r64, live64);
  L  `lea r, [live + k]` is not a dereference; r becomes a DERIVED pointer (a later [r ..] is a dereference of the
     value + k, a later test of r is not a null test);
  J  an unconditional `jmp imm` inside the same function is followed (window continues at the target); only a jmp out
     of the function (or ret) with rax live is RETURNED;
  S  a store of the value to [rsp + k] is a SPILL, not STORED; a later reload `mov r, [rsp + k]` of that slot
     makes r live again. A store to any other memory operand is STORED, and a later load of the same operand text
     (base/index registers not rewritten in between) makes the destination live again;
  C  a copy is `mov r, live` at 64 or 32 bits (handles are dwords).
Part 3 - the package's own classify(), re-implemented verbatim from sd165_nulltests.py but reading bytes through
  arena_ix, instrumented to report which of the four suspected defects decided each site's class:
  dK  the deciding register had been overwritten (by K's rule) before the deciding instruction;
  dL  DEREF decided by a `lea`;
  dJ  RETURNED decided by a jmp whose target is inside the same function;
  dS  STORED decided by a store to [rsp + k] (and nothing else happened before the window ended);
  dN  DEREF decided by a multi-byte `nop` whose padding operand names the register.
"""
import collections, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd164-167-0930"))
import arena_ix as X  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG

ENTRIES = [0x0036A100, 0x0036A190, 0x0036A1A0, 0x0036A230, 0x0036B160, 0x0036CAD0]
THUNK_JMPS = {0x0036A195, 0x0036A232}
F64 = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for r in fam:
        F64[r] = fam[0]
for n in range(8, 16):
    for s in ("", "d", "w", "b"):
        F64["r%d%s" % (n, s)] = "r%d" % n
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def c64(r):
    return F64.get(r)


def rn(i, r):
    return c64(i.reg_name(r))


def writes(i):
    try:
        return {rn(i, r) for r in i.regs_access()[1]} - {None}
    except Exception:
        return set()


def memops(i):
    return [(k, op) for k, op in enumerate(i.operands) if op.type == CS_OP_MEM]


def same_fn(a, b):
    ra, rb = X.root(a), X.root(b)
    return ra is not None and ra == rb


def insns_from(a, n=0x200):
    return list(X.md.disasm(X.rd(a, n), a))


# ---------------- part 1
raw = X.rel32(ENTRIES)
sites = []
print("PART 1 raw call sites per entry (E8/E9/jcc), stored pointers:")
for e in ENTRIES:
    ss = sorted(raw[e])
    real = [(s, k) for s, k in ss if s not in THUNK_JMPS]
    print("   %08X raw %d (%s)  thunk jmps excluded %d  real %d  dir64 %s  rva32-non-pdata %s" % (
        e, len(ss), dict(collections.Counter(k for s, k in ss)), len(ss) - len(real), len(real),
        X.dir64([e])[e], [("%08X" % a, n) for a, n in X.rva32(e) if n != ".pdata"]))
    sites += [(e, s) for s, k in real]
print("   real allocation call sites: %d" % len(sites))


# ---------------- part 2
def mine(site):
    live, derived, spill = {"rax"}, set(), set()
    slots = {}             # non-stack memory operand text the value was stored to -> its base/index registers
    first = None
    ins = insns_from(site + 5)
    k, n = 0, 0
    while n < 24 and k < len(ins):
        i = ins[k]
        n += 1
        mn, op = i.mnemonic, i.op_str
        # dereference through the value or a derived pointer (not lea)
        if mn != "lea" and mn != "nop":
            for j, m in memops(i):
                b = rn(i, m.mem.base) if m.mem.base else None
                x = rn(i, m.mem.index) if m.mem.index else None
                if b in live or x in live:
                    return "DEREF"
                if b in derived or x in derived:
                    return "DEREF"
        if mn in ("test", "cmp", "or") and len(i.operands) == 2 and i.operands[0].type == CS_OP_REG:
            r0 = rn(i, i.operands[0].reg)
            o1 = i.operands[1]
            if r0 in live and ((o1.type == CS_OP_REG and rn(i, o1.reg) == r0) or (mn == "cmp" and o1.type == 2 and o1.imm == 0)):
                return "TESTED"
        w = writes(i)
        if mn == "mov" and len(i.operands) == 2 and i.operands[0].type == CS_OP_REG and i.operands[1].type == CS_OP_REG \
                and rn(i, i.operands[1].reg) in live and i.operands[0].size in (4, 8):
            live.add(rn(i, i.operands[0].reg))
            k += 1
            continue
        if mn == "mov" and len(i.operands) == 2 and i.operands[0].type == CS_OP_REG and i.operands[1].type == CS_OP_MEM \
                and op.split(", ", 1)[1] in slots and i.operands[0].size in (4, 8):
            live.add(rn(i, i.operands[0].reg))
            k += 1
            continue
        if mn == "lea" and i.operands[0].type == CS_OP_REG:
            m = i.operands[1].mem
            b = rn(i, m.base) if m.base else None
            d = rn(i, i.operands[0].reg)
            if b in live or b in derived:
                live.discard(d)
                derived.add(d)
                k += 1
                continue
        if mn == "mov" and len(i.operands) == 2 and i.operands[0].type == CS_OP_MEM and i.operands[1].type == CS_OP_REG \
                and rn(i, i.operands[1].reg) in live:
            m = i.operands[0].mem
            if rn(i, m.base) == "rsp":
                spill.add(m.disp)
            else:
                first = first or "STORED"
                slots[op.split(", ", 1)[0]] = {rn(i, m.base), rn(i, m.index) if m.index else None} - {None}
            k += 1
            continue
        if mn == "mov" and len(i.operands) == 2 and i.operands[0].type == CS_OP_REG and i.operands[1].type == CS_OP_MEM \
                and rn(i, i.operands[1].mem.base) == "rsp" and i.operands[1].mem.disp in spill and i.operands[0].size in (4, 8):
            live.add(rn(i, i.operands[0].reg))
            k += 1
            continue
        if mn == "call":
            if live & {"rcx", "rdx", "r8", "r9"}:
                first = first or "PASSED"
            live -= VOL
            derived -= VOL
            if not live and not derived and not spill and not slots:
                break
            k += 1
            continue
        if mn == "ret":
            if "rax" in live:
                first = first or "RETURNED"
            break
        if mn == "jmp":
            if i.operands[0].type == 2:
                t = i.operands[0].imm
                if same_fn(t, i.address):
                    ins = insns_from(t)
                    k = 0
                    continue
                if "rax" in live:
                    first = first or "RETURNED"
            break
        if mn == "int3":
            break
        for t in [t for t, rr in slots.items() if rr & w]:
            del slots[t]
        killed = w & (live | derived)
        live -= killed
        derived -= killed
        if not live and not derived and not spill and not slots:
            break
        k += 1
    return first or "UNCLEAR"


# ---------------- part 3 (the package's classify, verbatim logic, instrumented)
REG64 = {"rax": ("rax", "eax"), "rbx": ("rbx", "ebx"), "rcx": ("rcx", "ecx"), "rdx": ("rdx", "edx"), "rsi": ("rsi", "esi"),
         "rdi": ("rdi", "edi"), "rbp": ("rbp", "ebp"), "r8": ("r8", "r8d"), "r9": ("r9", "r9d"), "r10": ("r10", "r10d"),
         "r11": ("r11", "r11d"), "r12": ("r12", "r12d"), "r13": ("r13", "r13d"), "r14": ("r14", "r14d"), "r15": ("r15", "r15d")}


def pkg(site):
    live, first, why = {"rax"}, None, set()
    stale = set()          # registers the package still thinks live although K's rule killed them
    full = {REG64[r][1]: r for r in REG64}
    firstwhy = None
    for n, i in enumerate(X.md.disasm(X.rd(site, 0x100), site)):
        if n == 0:
            continue
        if n > 24:
            break
        op, mn = i.op_str, i.mnemonic
        regs = list(live)
        alias = regs + [REG64[r][1] for r in regs if r in REG64]
        hit = [r for r in regs if re.search(r"\[%s(\]| )" % r, op)]
        if hit:
            if mn == "lea":
                why.add("dL")
            if mn.startswith("nop"):
                why.add("dN")
            if any(r in stale for r in hit):
                why.add("dK")
            return "DEREF", why
        tm = [r for r in alias if mn in ("test", "cmp", "or") and re.match(r"%s, (%s|0)$" % (r, r), op)]
        if tm:
            if any((full.get(r, r)) in stale for r in tm):
                why.add("dK")
            return "TESTED", why
        m = re.match(r"(\w+), (\w+)$", op)
        # K bookkeeping: would a correct kill set have dropped a live register here?
        w = writes(i)
        is_copy = mn == "mov" and m and (m.group(2) in live or (m.group(2) in full and full[m.group(2)] in live))
        if not is_copy and mn not in ("call",):
            for r in list(live):
                if r in w and not (m and m.group(1) == r and mn not in ("test", "cmp")) and mn not in ("test", "cmp"):
                    stale.add(r)
        if mn == "mov" and m and m.group(2) in full and full[m.group(2)] in live and m.group(1) in full:
            live.add(full[m.group(1)])
            continue
        if mn == "mov" and m and m.group(2) in live:
            live.add(m.group(1))
            continue
        if mn == "mov" and re.match(r"\w+ ptr \[", op) and op.split(", ")[-1] in alias:
            if first is None:
                first = "STORED"
                firstwhy = "dS" if re.match(r"\w+ ptr \[rsp", op) else None
                if any(full.get(op.split(", ")[-1], op.split(", ")[-1]) in stale for _ in [0]):
                    firstwhy = (firstwhy or "") + "dK"
            continue
        if mn == "call":
            if live & {"rcx", "rdx", "r8", "r9"}:
                if first is None:
                    first = "PASSED"
                    firstwhy = "dK" if (live & {"rcx", "rdx", "r8", "r9"}) <= stale else None
            live -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
            if not live:
                break
            continue
        if mn == "ret" or (mn == "jmp" and op.startswith("0x")):
            if "rax" in live:
                if first is None:
                    first = "RETURNED"
                    firstwhy = "dJ" if (mn == "jmp" and same_fn(int(op, 16), i.address)) else None
                    if "rax" in stale:
                        firstwhy = (firstwhy or "") + "dK"
            break
        if mn == "jmp":
            break
        if m and m.group(1) in live and mn not in ("test", "cmp"):
            live.discard(m.group(1))
            stale.discard(m.group(1))
            if not live:
                break
    if firstwhy:
        for t in ("dS", "dK", "dJ"):
            if t in firstwhy:
                why.add(t)
    return first or "UNCLEAR", why


# the package's TSV
tsv = os.path.join(HERE, "..", "sd165-alloc-null-tests-0930", "sd165-sites.tsv")
P = {}
for l in open(tsv, encoding="utf-8").read().splitlines()[1:]:
    e, f, s, k = l.split("\t")
    P[int(s, 16)] = (e, k)
print("PART 1b package TSV rows %d; rows that are thunk jmps, not callers: %s; real sites missing from the TSV: %d" % (
    len(P), ["%08X" % s for s in sorted(P) if s in THUNK_JMPS], sum(1 for e, s in sites if s not in P)))
miss = collections.Counter("%08X" % e for e, s in sites if s not in P)
print("   missing by entry: %s" % dict(miss))

print("PART 3 package classify re-implemented: agrees with the TSV on every TSV row: %s" % all(
    pkg(s)[0] == P[s][1] for s in P))
dfx = collections.Counter()
dsites = collections.defaultdict(list)
for s in sorted(P):
    k, why = pkg(s)
    for w in why:
        dfx[w] += 1
        dsites[w].append((s, k))
print("PART 3 sites whose package class was decided by a suspected defect: %s" % dict(sorted(dfx.items())))
for w in sorted(dsites):
    print("   %s: %s" % (w, " ".join("%08X:%s" % x for x in dsites[w])))

M = {s: mine(s) for e, s in sites}
agg = collections.defaultdict(collections.Counter)
for e, s in sites:
    agg["%08X" % e][M[s]] += 1
tot = collections.Counter()
for v in agg.values():
    tot.update(v)
print("PART 2 my classes over all %d real sites: %s" % (len(sites), dict(sorted(tot.items()))))
for e in sorted(agg):
    print("   %s %s" % (e, dict(sorted(agg[e].items()))))
common = [s for e, s in sites if s in P]
tr = collections.Counter((P[s][1], M[s]) for s in common)
print("PART 2 on the %d sites common to both: package -> mine transitions (changed only):" % len(common))
for (a, b), n in sorted(tr.items()):
    if a != b:
        print("   %-9s -> %-9s %d" % (a, b, n))
print("   unchanged: %d" % sum(n for (a, b), n in tr.items() if a == b))
print("PART 2 changed sites:")
for s in common:
    if P[s][1] != M[s]:
        print("   %08X %s -> %s  (package defects: %s)" % (s, P[s][1], M[s], ",".join(sorted(pkg(s)[1])) or "-"))
ctot = collections.Counter(M[s] for s in common)
print("PART 2 my classes on the common sites: %s" % dict(sorted(ctot.items())))
new = collections.Counter(M[s] for e, s in sites if s not in P)
print("PART 2 my classes on the sites the package missed: %s" % dict(sorted(new.items())))
print("controls: 002E678F -> %s (package TESTED); 0024A2B9 -> %s (package DEREF)" % (M.get(0x002E678F), M.get(0x0024A2B9)))
with open(os.path.join(HERE, "sd165_indep-sites.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("entry\troot\tsite\tpackage\tmine\tpackage_defects\n")
    for e, s in sites:
        fo.write("%08X\t%08X\t%08X\t%s\t%s\t%s\n" % (e, X.root(s) or 0, s, P.get(s, ("", "-"))[1], M[s],
                                                     ",".join(sorted(pkg(s)[1])) if s in P else ""))
