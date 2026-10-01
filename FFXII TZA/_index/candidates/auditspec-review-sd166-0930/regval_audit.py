"""regval_audit.py - SWE2-AUDIT-SPEC (2026-09-30): soundness tests of the kit's regval.py on SD-166's A3 query (the 135
push sites of 0036C1D0, rcx, depth 5). Imports regval read-only; instruments it only by wrapping functions in memory.

  T1 memo order-dependence: per-site value sets with the global memo (package order), with the memo cleared before
     every site, and in reverse order with a shared memo. Any difference = a cached result reused under a loop cut.
  T2 visited bodies: every function body regval decoded for the query, and every (function, register) it followed
     into callers.
  T3 missed predecessors in each visited body: (a) indirect jumps (`jmp reg` / `jmp [mem]`) in the body;
     (b) raw rel32 jmp/jcc/call from OUTSIDE the decoded body into an instruction inside it (arena_ix raw index,
     every executable section), (c) rel8 short jumps from the 0x80 bytes either side of the body into it.
  T4 missed callers of every followed function: raw E8/E9/0F8x rel32 sites vs regval's caller list (retool calls),
     DIR64 relocation slots and raw rva32 occurrences outside .pdata.
  C1 positive control: a push site with `mov ecx, K` right before the call must resolve to {K}.
  C2 unmodelled-writer control: the instruction right after real `inc ecx`, `pop rcx`, `sete cl`, `and ecx, imm`
     sites must give a U term (not a constant).
"""
import collections, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd164-167-0930"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import arena_ix as X  # noqa: E402
import regval as V  # noqa: E402

SITES = sorted(V.SC["calls"].get(0x0036C1D0, ()))
print("push sites (retool calls of 0036C1D0): %d" % len(SITES))
raw = X.rel32([0x0036C1D0])[0x0036C1D0]
print("raw rel32 sites of 0036C1D0: %d (%s); set-equal to retool's: %s" % (
    len(raw), dict(collections.Counter(k for s, k in raw)), sorted(s for s, k in raw) == sorted(s for f, s in SITES)))

visited, followed = set(), set()
_body, _entry = V.body, V.entry


def body(f):
    visited.add(f)
    return _body(f)


def entry(f, reg, depth):
    if reg in V.ARGS:
        followed.add((f, reg))
    return _entry(f, reg, depth)


V.body, V.entry = body, entry


def run(order, clear):
    V._memo.clear()
    out = {}
    for f, s in order:
        if clear:
            V._memo.clear()
        out[(f, s)] = frozenset(V.value_at(f, s, "rcx", 5))
    return out


A = run(SITES, False)
B = run(SITES, True)
C = run(list(reversed(SITES)), False)
agg = collections.Counter(x[1] for v in A.values() for x in v if x[0] == "C")
print("T1 package-order aggregate: %s" % dict(sorted(agg.items())))
dAB = [k for k in SITES if A[k] != B[k]]
dAC = [k for k in SITES if A[k] != C[k]]
print("T1 sites whose set differs, shared memo vs memo cleared per site: %d; vs reverse order: %d" % (len(dAB), len(dAC)))
for k in sorted(set(dAB) | set(dAC)):
    print("   %08X/%08X  pkg=%s  clear=%s  rev=%s" % (k[0], k[1], sorted(A[k], key=str), sorted(B[k], key=str), sorted(C[k], key=str)))
sevens = [k for k in SITES if ("C", 7) in (A[k] | B[k] | C[k])]
nonc = sorted(set(f for k in SITES for f in [k[0]] if any(x[0] != "C" for x in (A[k] | B[k] | C[k]))))
print("T1 sites with 7 in any run: %d; functions with a non-constant term in any run: %s" % (len(sevens), ["%08X" % f for f in nonc]))

print("T2 bodies decoded: %d; (function, argument) pairs followed into callers: %d" % (len(visited), len(followed)))
for f, r in sorted(followed):
    print("   followed %08X %s" % (f, r))

# T3
ind, into = [], []
allinsn = {}
for f in sorted(visited):
    ins, idx, preds = _body(f)
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    for i in ins:
        if i.mnemonic == "jmp" and not re.match(r"0x[0-9a-f]+$", i.op_str):
            ind.append((f, i.address, i.op_str))
        allinsn[i.address] = (f, lo, hi)
rr = X.rel32(set(allinsn))
for t, sl in rr.items():
    f, lo, hi = allinsn[t]
    for s, k in sl:
        if not (lo <= s < hi) and t != f:
            into.append((f, t, s, k))
short = []
for f in sorted(visited):
    ins, idx, preds = _body(f)
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    for a0, a1 in ((lo - 0x80, lo), (hi, hi + 0x80)):
        b = X.rd(a0, a1 - a0) or b""
        for q in range(len(b) - 1):
            op = b[q]
            if op == 0xEB or 0x70 <= op <= 0x7F:
                d = b[q + 1] - 256 if b[q + 1] > 127 else b[q + 1]
                t = a0 + q + 2 + d
                if t in idx and t != f:
                    i = next(X.md.disasm(b[q:q + 2], a0 + q, 1), None)
                    if i and i.size == 2:
                        short.append((f, t, a0 + q, i.mnemonic))
print("T3a indirect jmp in visited bodies: %d %s" % (len(ind), ["%08X@%08X %s" % x for x in ind]))
print("T3b rel32 edges from outside a visited body into its interior (not its entry): %d" % len(into))
for f, t, s, k in sorted(into):
    print("   body %08X  target %08X  from %08X %s (root %08X)" % (f, t, s, k, X.root(s) or 0))
print("T3c rel8 candidates from the 0x80 bytes around a body into it: %d (byte-pattern candidates, may be data)" % len(short))
for f, t, s, m in sorted(short):
    print("   body %08X  target %08X  from %08X %s" % (f, t, s, m))

# T4
fs = sorted(set(f for f, r in followed))
rawc = X.rel32(fs)
d64 = X.dir64(fs)
print("T4 callers of followed functions: retool vs raw rel32 (E8/E9/jcc), dir64, rva32 outside .pdata")
bad = 0
for f in fs:
    rv = sorted(s for cf, s in V.SC["calls"].get(f, ()))
    rw = sorted(s for s, k in rawc[f])
    jcc = [s for s, k in rawc[f] if k == "jcc"]
    r32 = [(a, n) for a, n in X.rva32(f) if n != ".pdata"]
    r32 = [(a, n) for a, n in r32 if not (n == ".rdata" and tuple(__import__("struct").unpack("<III", X.rd(a, 12))) in set(map(tuple, X.PD)))]
    flag = rv != rw or d64[f] or r32
    bad += bool(flag)
    print("   %08X retool %d raw %d (jcc %d) extra-raw %s missing-raw %s dir64 %s rva32 %s%s" % (
        f, len(rv), len(rw), len(jcc), ["%08X" % s for s in sorted(set(rw) - set(rv))], ["%08X" % s for s in sorted(set(rv) - set(rw))],
        ["%08X" % s for s in d64[f]], ["%08X %s" % x for x in r32], "   <-- CHECK" if flag else ""))
print("T4 followed functions with a caller regval did not walk or a stored pointer: %d of %d" % (bad, len(fs)))

# C1
c1 = [(f, s) for f, s in SITES if any(i.address + i.size == s and re.match(r"mov ecx, (0x[0-9a-f]+|\d+)$", "%s %s" % (i.mnemonic, i.op_str))
                                      for i in X.dis(s - 5, s))]
okc1 = all(V.value_at(f, s, "rcx", 5) == {("C", int(X.txt(s - 5).split(", ")[1], 0))} for f, s in c1)
print("C1 push sites with `mov ecx, K` immediately before the call: %d; all resolve to {K}: %s" % (len(c1), okc1))

# C2
pats = {"inc ecx": None, "pop rcx": None, "sete cl": None, "and ecx, 0x": None, "movzx ecx, cl": None}  # movzx ecx, cl: modelled as a copy - a truncation probe, not a U case
for f in sorted(V.SZ)[:40000]:
    if all(pats.values()):
        break
    ins, idx, preds = _body(f)
    for k, i in enumerate(ins[:-1]):
        t = "%s %s" % (i.mnemonic, i.op_str)
        for p in pats:
            if pats[p] is None and t.startswith(p) and ins[k + 1].mnemonic not in ("jmp", "ret", "int3"):
                pats[p] = (f, ins[k + 1].address, t)
for p, v in pats.items():
    if v:
        got = V.value_at(v[0], v[1], "rcx", 1)
        print("C2 %-14s at %08X (after `%s`): %s -> %s" % (p, v[1], v[2], sorted(got, key=str),
                                                          "U as required" if got and all(x[0] == "U" for x in got) else "NOT U"))
    else:
        print("C2 %-14s: no instance found" % p)
