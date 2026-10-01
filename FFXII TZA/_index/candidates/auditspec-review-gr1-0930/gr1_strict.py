"""gr1_strict.py - SWE2-AUDIT-SPEC strict re-check of GR-1's S4 pairing (2026-09-30).

Input: gr1_pairs.json (every access covering slot +0x27 that the package's structflow finds per handler, r8 = slot+0x18,
depth 2). The WRITE sites there are taken as the set of covering writes; everything else is this folder's img.py
(independent decode over .pdata extents; nothing from retool).

MUST-WRITE on the CFG instead of the package's rule ("any write in begin, or a write at a lower address in the same
handler's hit list"):
  W(f)      every path from f's entry to each exit (ret, tail jmp) passes a covering write in f, or a direct call / tail
            jmp to a g with W(g). Loops and joins by a forward AND dataflow; an indirect jmp or a jmp into another
            extent that is not a function start counts as NOT written (conservative).
  local(s)  at the read s, the same must-state in s's own function (a covering write, or a call to a W function,
            on every path from the function's entry to s).
Per command-read: covered if local(s), or - for a poll / result read - W(begin). A begin read that is not local is
listed for reading by hand (its covering write would have to be in the caller chain). Each credited write's
instruction is printed so a read-modify-write (or / and / add ...) credited as a write is visible.
"""
import os, sys, json, bisect, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img as I  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_REG  # noqa: E402

P = I.pdata()
PB = [b for b, e in P]
PE = dict(P)


def owner(a):
    k = bisect.bisect_right(PB, a) - 1
    return P[k][0] if k >= 0 and P[k][0] <= a < P[k][1] else None


_cfg = {}


def cfg(f):
    if f in _cfg:
        return _cfg[f]
    e = PE[f]
    ins = I.dis(f, e - f)
    idx = {x.address: k for k, x in enumerate(ins)}
    lead = {0}
    for k, x in enumerate(ins):
        if x.mnemonic.startswith("j") or x.mnemonic in ("ret", "int3"):
            if k + 1 < len(ins):
                lead.add(k + 1)
            if x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm in idx:
                lead.add(idx[x.operands[0].imm])
    _cfg[f] = (ins, idx, sorted(lead))
    return _cfg[f]


WSET = set()
_W = {}


def gen(x, depth):
    if x.address in WSET:
        return True
    if x.mnemonic == "call" and x.operands and x.operands[0].type == X86_OP_IMM:
        g = x.operands[0].imm
        return g in PE and W(g, depth + 1)
    return False


def must_states(f, depth):
    """per instruction index: must-written state BEFORE it; plus the exit verdict"""
    ins, idx, lead = cfg(f)
    if not ins:
        return {}, False
    blocks = {}
    for n, s in enumerate(lead):
        blocks[s] = list(range(s, (lead[n + 1] if n + 1 < len(lead) else len(ins))))
    succ = collections.defaultdict(list)
    exits = []   # (index, state-contribution kind)
    for s, ks in blocks.items():
        last = ins[ks[-1]]
        m = last.mnemonic
        nxt = ks[-1] + 1 if ks[-1] + 1 < len(ins) else None
        if m.startswith("j"):
            op = last.operands[0] if last.operands else None
            if op is not None and op.type == X86_OP_IMM and op.imm in idx:
                succ[s].append(idx[op.imm])
            elif m == "jmp" or op is not None:
                exits.append(ks[-1])
            if m != "jmp" and nxt is not None:
                succ[s].append(nxt)
        elif m == "ret":
            exits.append(ks[-1])
        elif m != "int3" and nxt is not None:
            succ[s].append(nxt)
    INs = {0: False}
    order = [0]
    changed = True
    state_before = {}
    it = 0
    while changed and it < 200:
        changed, it = False, it + 1
        for s in sorted(blocks):
            if s not in INs:
                continue
            st = INs[s]
            for k in blocks[s]:
                state_before[k] = st
                if gen(ins[k], depth):
                    st = True
            for t in succ[s]:
                new = st if t not in INs else (INs[t] and st)
                if t not in INs or new != INs[t]:
                    INs[t] = new
                    changed = True
    ok = True
    for k in exits:
        st = state_before.get(k)
        if st is None:
            continue       # unreachable
        x = ins[k]
        if st:
            continue
        if x.mnemonic == "jmp" and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm in PE:
            if W(x.operands[0].imm, depth + 1):
                continue
        if x.mnemonic.startswith("j") and x.mnemonic != "jmp" and x.operands[0].type == X86_OP_IMM \
                and x.operands[0].imm in PE and W(x.operands[0].imm, depth + 1):
            continue
        ok = False
    return state_before, ok


def W(f, depth=0):
    if f in _W:
        return _W[f]
    if depth > 5 or f not in PE:
        return False
    _W[f] = False          # recursion guard: a cycle does not prove a write
    _W[f] = must_states(f, depth)[1]
    return _W[f]


def local(s):
    f = owner(s)
    if f is None:
        return None
    st, _ = must_states(f, 0)
    ins, idx, _ = cfg(f)
    return st.get(idx.get(s))


def main():
    data = json.load(open(os.path.join(HERE, "gr1_pairs.json")))
    txt = {}
    for h, d in data.items():
        for fn, a, kind, form, off, w, t in d["hits"]:
            if kind == "w":
                WSET.add(int(a, 16))
            txt[int(a, 16)] = t
    print("covering writes credited: %d" % len(WSET))
    rmw = [("%08X" % a, txt[a]) for a in sorted(WSET) if txt[a].split()[0] not in ("mov", "movss", "movsd", "movq", "movd", "movups", "movaps")]
    print("   of which read-modify-write or other non-mov: %s" % (rmw or "none"))
    for a in sorted(WSET):
        f = owner(a)
        print("   %08X in %s: %s" % (a, ("%08X" % f) if f else "?", txt[a]))
    roles = collections.defaultdict(list)
    for h, d in data.items():
        for fam, N, role, b in d["roles"]:
            roles[(fam, N)].append((role, int(h, 16), int(b, 16) if b else None))
    print("== per command-read")
    tally = collections.Counter()
    for h, d in sorted(data.items()):
        reads = [x for x in d["hits"] if x[2] == "r"]
        if not reads:
            continue
        for fam, N, role, b in d["roles"]:
            b = int(b, 16) if b else None
            for fn, a, kind, form, off, w, t in reads:
                s = int(a, 16)
                lc = local(s)
                wb = W(b) if b else None
                if lc:
                    v = "COVERED-LOCAL"
                elif role != "begin" and wb:
                    v = "COVERED-BY-BEGIN (W(begin))"
                elif role == "begin":
                    v = "BEGIN-READ-NOT-LOCAL (hand check)"
                else:
                    v = "NOT-COVERED"
                tally[v] += 1
                print("   %s/%s %-6s handler %s read %s in %s %-40s | local %s | begin %s W=%s -> %s"
                      % (fam, N, role, h, a, fn, t, lc, ("%08X" % b) if b else "-", wb, v))
    print("tally: %s" % dict(tally))
    for b in sorted({r[2] for v in roles.values() for r in v if r[2]}):
        pass


if __name__ == "__main__":
    main()
