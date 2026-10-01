"""regval_audit2.py - SWE2-AUDIT-SPEC (2026-09-30): do regval's missed predecessors (regval_audit.out T3) touch any of the
135 push-site walks?  Imports regval read-only; wraps val() in memory to record the nodes each site's walk visits.

  J  decode the jump table behind each indirect jmp in a visited body (MSVC form: `cmp idx, N` / `ja` then a
     `[base + idx*4 + disp]` dword load, entries are RVAs); the case targets are predecessors regval does not see.
  S  validate each rel8 / rel32 outside-edge candidate by linear decode from the start of its .pdata range (a real
     instruction boundary there), and keep only the real ones.
  W  per push site: the set of (function, instruction) nodes its walk reached (memo cleared per site, so a cached
     sub-walk is re-walked and recorded).  Report every site whose walk reached a node that has a missed predecessor.
"""
import collections, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd164-167-0930"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import arena_ix as X  # noqa: E402
import regval as V  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_IMM

SITES = sorted(V.SC["calls"].get(0x0036C1D0, ()))
cur = None
reach = collections.defaultdict(set)
_val = V.val


def val(f, k, reg, depth, onpath):
    ins, idx, preds = V.body(f)
    reach[cur].add((f, ins[k].address))
    return _val(f, k, reg, depth, onpath)


V.val = val
for s in SITES:
    cur = s
    V._memo.clear()
    V.value_at(s[0], s[1], "rcx", 5)
visited = sorted(set(f for v in reach.values() for f, a in v))
print("W walks recorded: %d sites, %d bodies, %d nodes" % (len(reach), len(visited), len(set().union(*reach.values()))))

missed = collections.defaultdict(list)   # (f, addr) -> [why]

# J
for f in visited:
    ins, idx, preds = V.body(f)
    for k, i in enumerate(ins):
        if i.mnemonic != "jmp" or re.match(r"0x[0-9a-f]+$", i.op_str):
            continue
        n, disp = None, None
        for j in range(k - 1, max(-1, k - 14), -1):
            p = ins[j]
            for op in p.operands:
                if op.type == CS_OP_MEM and op.mem.scale == 4 and op.mem.disp > 0x1000 and disp is None and p.mnemonic == "mov":
                    disp = op.mem.disp
            if p.mnemonic == "ja" and j > 0 and ins[j - 1].mnemonic == "cmp" and ins[j - 1].operands[1].type == CS_OP_IMM and n is None:
                n = ins[j - 1].operands[1].imm + 1
        if n is None or disp is None:
            print("J %08X@%08X %s: table not decoded (n=%s disp=%s)" % (f, i.address, i.op_str, n, disp))
            for j in range(max(0, k - 10), k + 1):
                print("      %08X %s %s" % (ins[j].address, ins[j].mnemonic, ins[j].op_str))
            continue
        tg = [X.IB + struct.unpack("<I", X.rd(X.IB + disp + 4 * q, 4))[0] for q in range(n)]
        inb = [t for t in tg if t in idx]
        print("J %08X@%08X: %d cases from table %08X; %d targets in the decoded body; distinct %d" % (
            f, i.address, n, X.IB + disp, len(inb), len(set(tg))))
        for t in set(tg):
            missed[(f, t)].append("jump-table case of %08X" % i.address)

# S (rel32 from regval_audit T3b and rel8 candidates re-derived here)
allinsn = {}
for f in visited:
    ins, idx, preds = V.body(f)
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    for i in ins:
        allinsn[i.address] = (f, lo, hi)


def real(site):
    e = X.pentry(site)
    if e is None:
        return None
    for i in X.dis(X.IB + e[0], X.IB + e[1]):
        if i.address == site:
            return i
        if i.address > site:
            return False
    return False


rr = X.rel32(set(allinsn))
for t, sl in rr.items():
    f, lo, hi = allinsn[t]
    for s, kk in sl:
        if not (lo <= s < hi) and t != f:
            ok = real(s)
            print("S rel32 %s from %08X into %08X (body %08X): real instruction %s" % (kk, s, t, f, bool(ok) if ok is not None else "no .pdata"))
            if ok or ok is None:
                missed[(f, t)].append("rel32 %s from %08X" % (kk, s))
for f in visited:
    ins, idx, preds = V.body(f)
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    for a0, a1 in ((lo - 0x80, lo), (hi, hi + 0x80)):
        b = X.rd(a0, a1 - a0) or b""
        for q in range(len(b) - 1):
            op = b[q]
            if op == 0xEB or 0x70 <= op <= 0x7F:
                d = b[q + 1] - 256 if b[q + 1] > 127 else b[q + 1]
                t = a0 + q + 2 + d
                if t in idx and t != f:
                    ok = real(a0 + q)
                    if ok:
                        print("S rel8 %s at %08X into %08X (body %08X): real instruction" % (ok.mnemonic, a0 + q, t, f))
                        missed[(f, t)].append("rel8 %s from %08X" % (ok.mnemonic, a0 + q))
                    elif ok is None:
                        print("S rel8 at %08X into %08X (body %08X): no .pdata range - UNVERIFIED" % (a0 + q, t, f))
                        missed[(f, t)].append("rel8 unverified from %08X" % (a0 + q))

# W
hits = []
for s, nodes in reach.items():
    for n in nodes:
        if n in missed:
            hits.append((s, n, missed[n]))
print("W push-site walks that reached a node with a missed predecessor: %d" % len(set(h[0] for h in hits)))
for s, n, why in sorted(hits):
    print("   site %08X/%08X  node %08X:%08X  %s" % (s[0], s[1], n[0], n[1], "; ".join(why)))
