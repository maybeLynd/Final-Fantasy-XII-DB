"""sd165_nulltests_v2.py - SD-165 repaired after SWE2-AUDIT-SPEC's REJECT (auditspec-review-sd165-0930, e1a2c0f05).
OPUS, 2026-10-01. Static, the certified image, via retool.py. Writes sd165-sites-v2.tsv beside itself.

ENTRY LIST (the review's item 1). Every raw call site of the five ways game code reaches the retry allocator 0036BFE0:
the raw-block wrappers 0036A100, 0036A190 (mov edx,1; jmp 0036A1A0) and 0036A230 (xor edx,edx; jmp 0036A1A0), the
handle path 0036B160, and the realloc 0036CAD0 (-> 0036D050, which reaches 0036BFE0 for a null pointer). 0036A1A0 is the
body the two thunks share; its two "sites" are the thunks' jmps (0036A195, 0036A232), not callers, so it is no entry.

CLASSIFIER (the review's item 2). The returned value is followed from the instruction after the call for up to 24
instructions, in its register and its copies:
  - a register is killed by ANY write to it, whatever the alias width (al/ax/eax/rax) and whatever the source
    (memory load, arithmetic, xor, set, pop, cmov) - except a copy from a live register (64- or 32-bit), which joins it;
  - `lea dst, [live + ...]` is a derived pointer: it is not a dereference, and dst joins the live set;
  - `nop` (any width, including `nop dword ptr [rax]`) is padding and ignored;
  - an unconditional `jmp` whose target lies inside the caller's own body is followed (once per target);
  - a store of the value to `[rsp + k]` is a spill, not STORED: the slot stays live and a reload from it joins the set;
  - a store to any other memory operand is STORED, and a reload from the same operand text joins the live set (so a
    store-and-reload that is then dereferenced is DEREF).
The site is classed by what comes first, as before: TESTED (test/cmp of the value with itself or 0), DEREF (a memory
operand based on or indexed by the value, other than lea/nop), else what it did first with no test or dereference in the
window: PASSED (a call or tail jump with the value in rcx/rdx/r8/r9), STORED (written to non-stack memory), RETURNED
(ret, or a tail jump out of the body, with the value in rax), UNCLEAR (lost).

CONTROLS (one per defect the review names, so a regression fails), checked against the review's hand reads:
  dK 0025623B  a load into the value's register kills it (the later [rax+0x1c] is a different slot): not DEREF
  dL 005033B1  `lea ecx, [rax+rax*8]` on a different value is not a dereference: not DEREF
  dJ 003EA03C  `jmp 0x3ea048` inside the body reaches `test rax, rax`: TESTED
  dS 00259E27  `mov [rsp+0x38], ebx` is a spill; the struct is then passed: PASSED, not STORED
  dN 002562FE  `nop dword ptr [rax]` is not the dereference (the true class is DEREF for another reason)
  C1 002E678F TESTED and 0024A2B9 DEREF (the package's original controls); 0043F58E TESTED (a 0036A230 site).
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
ENTRIES = {0x0036A100: "0036A100", 0x0036A190: "0036A190", 0x0036A230: "0036A230", 0x0036B160: "0036B160 (handle)",
           0x0036CAD0: "0036CAD0 (realloc)"}
FAM = {}
for b, names in {"rax": "rax eax ax al ah", "rbx": "rbx ebx bx bl bh", "rcx": "rcx ecx cx cl ch", "rdx": "rdx edx dx dl dh",
                 "rsi": "rsi esi si sil", "rdi": "rdi edi di dil", "rbp": "rbp ebp bp bpl", "rsp": "rsp esp sp spl"}.items():
    for n in names.split():
        FAM[n] = b
for k in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (k, suf)] = "r%d" % k
ARGS = {"rcx", "rdx", "r8", "r9"}
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
NOWRITE = {"test", "cmp", "push", "call", "ret", "nop", "bt", "ucomiss", "comiss", "ucomisd", "comisd"}
REG = re.compile(r"\b(" + "|".join(sorted(FAM, key=len, reverse=True)) + r")\b")


def mem_regs(op):
    return {FAM[r] for part in re.findall(r"\[([^\]]*)\]", op) for r in REG.findall(part)}


def classify(site, lo, hi):
    live, slots, first, seen = {"rax"}, set(), None, set()
    stored = set()
    pc, n = site, 0
    insns = list(R.md.disasm(R.at(pc, 0x80), pc))
    k = 1                                   # skip the call itself
    while n < 24:
        if k >= len(insns):
            insns = list(R.md.disasm(R.at(pc, 0x80), pc)); k = 0
            if not insns:
                break
        i = insns[k]; k += 1; n += 1; pc = i.address + i.size
        mn, op = i.mnemonic, i.op_str
        if mn.startswith("nop"):
            continue
        ops = [o.strip() for o in op.split(",")] if op else []
        dst = ops[0] if ops else ""
        dreg = FAM.get(dst)
        src_regs = {FAM[r] for r in REG.findall(", ".join(ops[1:]))} if len(ops) > 1 else set()
        # spill reload: mov reg, [rsp + k] from a live slot
        m_rl = re.match(r"\w+ ptr \[rsp(?: \+ (0x[0-9a-f]+|\d+))?\]$", ops[1]) if len(ops) > 1 else None
        if mn == "lea":
            if mem_regs(op) & live:
                if dreg:
                    live.add(dreg)
            elif dreg:
                live.discard(dreg)
            continue
        if mn in ("test", "cmp", "or") and len(ops) == 2 and FAM.get(ops[0]) in live and (
                FAM.get(ops[1]) == FAM.get(ops[0]) or ops[1] in ("0", "0x0")):
            return "TESTED"
        mr = mem_regs(op)
        if mr & (live - {"rsp"}):
            return "DEREF"
        if mn == "call":
            if live & ARGS:
                first = first or "PASSED"
            live -= VOLATILE
            if not live and not slots and not stored:
                break
            continue
        if mn == "ret":
            if "rax" in live:
                first = first or "RETURNED"
            break
        if mn == "jmp":
            if re.fullmatch(r"0x[0-9a-f]+", op):
                t = int(op, 16)
                if lo <= t < hi and t not in seen:
                    seen.add(t); pc = t; insns = list(R.md.disasm(R.at(pc, 0x80), pc)); k = 0
                    continue
                if live & ARGS:
                    first = first or "PASSED"
                elif "rax" in live:
                    first = first or "RETURNED"
            break
        if mn.startswith("mov") and "ptr [" in dst and len(ops) == 2 and FAM.get(ops[1]) in live:
            m_sp = re.match(r"\w+ ptr \[rsp(?: \+ (0x[0-9a-f]+|\d+))?\]$", dst)
            if m_sp:
                slots.add(int(m_sp.group(1) or "0", 0))
            else:
                first = first or "STORED"
                stored.add(dst.split("ptr ", 1)[-1])
            continue
        if dreg and mn not in NOWRITE:
            if mn in ("mov", "movsxd") and len(ops) == 2 and FAM.get(ops[1]) in live and ops[1] not in ("al", "ah", "ax"):
                live.add(dreg); continue
            if mn == "mov" and m_rl and int(m_rl.group(1) or "0", 0) in slots:
                live.add(dreg); continue
            if mn == "mov" and len(ops) == 2 and "ptr [" in ops[1] and ops[1].split("ptr ", 1)[-1] in stored:
                live.add(dreg); continue
            if mn == "xchg" and len(ops) == 2:
                a, b = FAM.get(ops[0]), FAM.get(ops[1])
                if a in live or b in live:
                    live.add(a); live.add(b)
                continue
            live.discard(dreg)
            if not live and not slots and not stored:
                break
    return first or "UNCLEAR"


rows, tally = [], collections.defaultdict(collections.Counter)
for e, name in ENTRIES.items():
    for f, s in sorted(c["calls"].get(e, ())):
        if f in (0x0036A190, 0x0036A230):           # the two thunks' jmps are not callers
            continue
        lo, hi = f, f + SZ.get(f, 0x10000)
        cls = classify(s, lo, hi)
        tally[name][cls] += 1
        rows.append((name, f, s, cls))
with open(os.path.join(HERE, "sd165-sites-v2.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("entry\tcaller\tsite\tfirst_use\n")
    for r in rows:
        fo.write("%s\t%08X\t%08X\t%s\n" % r)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


for name in ENTRIES.values():
    print("      %-20s %3d %s" % (name, sum(tally[name].values()), dict(sorted(tally[name].items()))))
total = collections.Counter()
for t in tally.values():
    total.update(t)
print("      all sites %d: %s" % (sum(total.values()), dict(sorted(total.items()))))
by = {s: k for _, f, s, k in rows}
cnt = {n: sum(tally[n].values()) for n in ENTRIES.values()}
check("E1", [cnt[n] for n in ENTRIES.values()] == [110, 81, 47, 13, 2] and len(rows) == 253,
      "entry sites 110 / 81 / 47 / 13 / 2 = 253 (the review's census): %s" % [cnt[n] for n in ENTRIES.values()])
check("C1", by.get(0x002E678F) == "TESTED" and by.get(0x0024A2B9) == "DEREF" and by.get(0x0043F58E) == "TESTED",
      "002E678F TESTED, 0024A2B9 DEREF, 0043F58E TESTED: %s %s %s" % (by.get(0x002E678F), by.get(0x0024A2B9), by.get(0x0043F58E)))
check("dK", by.get(0x0025623B) not in ("DEREF", None), "0025623B is not DEREF: %s" % by.get(0x0025623B))
check("dL", by.get(0x005033B1) not in ("DEREF", None), "005033B1 is not DEREF: %s" % by.get(0x005033B1))
check("dJ", by.get(0x003EA03C) == "TESTED", "003EA03C TESTED through its in-body jmp: %s" % by.get(0x003EA03C))
check("dS", by.get(0x00259E27) == "PASSED", "00259E27 PASSED (spill, then the struct is passed): %s" % by.get(0x00259E27))
check("dN", by.get(0x002562FE) == "DEREF", "002562FE DEREF (not through the nop): %s" % by.get(0x002562FE))
# comparison with the reviewer's independent classes (not a gate: a different implementation)
ref = {}
rp = os.path.join(HERE, "..", "auditspec-review-sd165-0930", "sd165_indep-sites.tsv")
for l in open(rp, encoding="utf-8").read().splitlines()[1:]:
    p = l.split("\t")
    if len(p) >= 5:
        ref[int(p[2], 16)] = p[4]
same = sum(1 for s, k in by.items() if ref.get(s) == k)
diff = sorted((s, k, ref.get(s)) for s, k in by.items() if ref.get(s) != k)
print("      agreement with the reviewer's classifier: %d of %d sites; differing: %s" % (
    same, len(by), "; ".join("%08X mine %s / review %s" % d for d in diff[:20])))
print("FAILS %d" % fails)
