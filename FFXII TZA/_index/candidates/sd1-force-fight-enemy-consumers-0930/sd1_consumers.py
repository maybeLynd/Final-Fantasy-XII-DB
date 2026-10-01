"""sd1_consumers.py - SD-1: which of the force-fight flag's consumers can act on an enemy (spawned, kind-1) unit (OPUS,
2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.

The flag 01E0C2B8 has two consumer readers (UQ-152; its writer 00252C80 also reads the old value at 00252C94 -
SWE2-AUDIT-SPEC's sd1 review, comment narrowed 2026-10-01 by OPUS): 00253B90 (flag == 0, "force fight off", also through the jump thunk
0030C0D0) and 00253BA0. For every call site of the three, the containing function's block graph is built (linear sweep
of the body; jcc / jmp targets inside the body split blocks) and the site is classed by the unit-kind tests that gate
it. A kind test is a read of byte +5 of a stats record, the record loaded from a unit's +0x698 (kind 0 = party, kind 1 =
spawned; the-battle-unit-field-map.md +0x698). For each kind test, the site is checked for reachability from each of
the test's two successors without passing through the test again:
  KIND0-ONLY  a kind test lets only kind-0 units reach the site
  KIND1-ONLY  a kind test lets only kind-1 units reach the site
  ANY-KIND    no kind test on the paths to the site separates the kinds
  NO-UNIT     the function takes no unit (the flag gates a global quantity)
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
READERS = (0x00253B90, 0x0030C0D0, 0x00253BA0)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def graph(ins):
    lo, hi = ins[0].address, ins[-1].address + ins[-1].size
    leaders = {lo}
    for n, i in enumerate(ins):
        if i.mnemonic.startswith("j") or i.mnemonic == "ret":
            if n + 1 < len(ins):
                leaders.add(ins[n + 1].address)
            m = re.match(r"0x([0-9a-f]+)$", i.op_str)
            if m and lo <= int(m.group(1), 16) < hi:
                leaders.add(int(m.group(1), 16))
    blocks, cur = collections.OrderedDict(), None
    for i in ins:
        if i.address in leaders:
            cur = i.address
            blocks[cur] = []
        blocks[cur].append(i)
    succ = {}
    keys = list(blocks)
    for k, b in blocks.items():
        last, s = b[-1], []
        nxt = keys[keys.index(k) + 1] if keys.index(k) + 1 < len(keys) else None
        m = re.match(r"0x([0-9a-f]+)$", last.op_str)
        tgt = int(m.group(1), 16) if m and lo <= int(m.group(1), 16) < hi else None
        if last.mnemonic == "ret" or (last.mnemonic == "jmp" and tgt is None):
            s = []
        elif last.mnemonic == "jmp":
            s = [tgt]
        elif last.mnemonic.startswith("j"):
            s = [x for x in (nxt, tgt) if x is not None]
        else:
            s = [nxt] if nxt is not None else []
        succ[k] = s
    return blocks, succ


def block_of(blocks, a):
    return next(k for k, b in blocks.items() if any(i.address == a for i in b))


def reach(succ, start, goal, avoid):
    seen, st = set(), [start]
    while st:
        x = st.pop()
        if x == goal:
            return True
        if x in seen or x == avoid:
            continue
        seen.add(x)
        st.extend(succ.get(x, ()))
    return False


def kind_tests(blocks):
    """Blocks ending in a conditional branch on a +5 byte of a register last loaded from [.. + 0x698], with the
    comparison value; returns {block: (value, jcc, taken_target, fallthrough)}."""
    out, stats = {}, set()
    for k, b in blocks.items():
        cmpv = None
        for i in b:
            m = re.match(r"(\w+), qword ptr \[\w+ \+ 0x698\]$", i.op_str)
            if i.mnemonic == "mov" and m:
                stats.add(m.group(1))
            m = re.match(r"byte ptr \[(\w+) \+ 5\], (0x[0-9a-f]+|\d+)$", i.op_str)
            if i.mnemonic == "cmp" and m and m.group(1) in stats:
                cmpv = int(m.group(2), 0)
            m = re.match(r"(\w+), byte ptr \[(\w+) \+ 5\]$", i.op_str)
            if i.mnemonic == "movzx" and m and m.group(2) in stats:
                cmpv = ("reg", m.group(1))
            if i.mnemonic == "test" and isinstance(cmpv, tuple) and i.op_str == "%s, %s" % (cmpv[1], cmpv[1]):
                cmpv = 0
        last = b[-1]
        if isinstance(cmpv, int) and last.mnemonic in ("je", "jne"):
            out[k] = (cmpv, last.mnemonic, int(last.op_str, 16))
    return out


_G = {}


def classify(f, site):
    if f not in _G:
        blocks, succ = graph(body(f))
        _G[f] = (blocks, succ, kind_tests(blocks), {i.address: k for k, b in blocks.items() for i in b})
    blocks, succ, kt, where = _G[f]
    sb = where[site]
    keys = list(blocks)
    verdicts = []
    for k, (v, jcc, tgt) in kt.items():
        ft = keys[keys.index(k) + 1]
        eq, ne = (tgt, ft) if jcc == "je" else (ft, tgt)   # successor taken when kind == v / kind != v
        r_eq, r_ne = reach(succ, eq, sb, k), reach(succ, ne, sb, k)
        if r_eq and not r_ne:
            verdicts.append(("KIND%d-ONLY" % v if v in (0, 1) else "KIND==%d" % v, k))
        elif r_ne and not r_eq:
            verdicts.append(("KIND%d-ONLY" % (1 - v) if v in (0, 1) else "KIND!=%d" % v, k))
    return verdicts


sites = []
for e in READERS:
    for f, s in sorted(c["calls"].get(e, ())):
        sites.append((e, f, s))
rows = []
for e, f, s in sites:
    v = classify(f, s)
    rows.append((e, f, s, v))
    print("      %08X  %08X @ %08X  %s" % (e, f, s, ", ".join("%s (test block %08X)" % x for x in v) or "no separating kind test"))

by = {s: v for _, _, s, v in rows}
# K1 - census: 00253B90 7 direct sites + the thunk 0030C0D0 (a site itself) with 8 sites, 00253BA0 2 sites
n = collections.Counter(e for e, _, _ in sites)
check("K1", n[0x00253B90] == 8 and n[0x0030C0D0] == 8 and n[0x00253BA0] == 2,
      "sites: 00253B90 %d (incl. the thunk), 0030C0D0 %d, 00253BA0 %d" % (n[0x00253B90], n[0x0030C0D0], n[0x00253BA0]))
# K2 - control: the availability cascade's reason 0x24 is kind-0 only (cmp byte [rdi+5], 0 at 002FFDAE, rdi = [rdx+0x698])
check("K2", [x[0] for x in by[0x002FFDC9]] == ["KIND0-ONLY"] and dict(by[0x002FFDC9]) == {"KIND0-ONLY": 0x002FFDAE},
      "control: 002FFCF0's reason-0x24 gate is kind 0 only")
# Reachability from the per-unit frame. 00233F70 (BattleUnit_UpdateLifecycleAndCombatFrame) is the callback every bound
# battle unit runs, party and spawned alike (the-world-tick-and-the-field-frame.md 2.4: installed for every record with
# +0x14 >= 0x80 by 00265A20). A breadth-first walk of direct calls from it, up to DEPTH calls deep, skips every call
# site a kind test lets only kind-0 units reach; a consumer it reaches is one a spawned unit's own frame can run.
DEPTH = 9
fwd = collections.defaultdict(list)
for callee, xs in c["calls"].items():
    for f, s in xs:
        fwd[f].append((callee, s))
prev, level, frontier = {0x00233F70: None}, 0, [0x00233F70]
while frontier and level < DEPTH:
    level += 1
    nxt = []
    for f in frontier:
        if f not in SZ:
            continue
        for callee, s in fwd.get(f, ()):
            if callee in prev:
                continue
            if any(v == "KIND0-ONLY" for v, _ in classify(f, s)):
                continue
            prev[callee] = (f, s)
            nxt.append(callee)
    frontier = nxt
print("      functions a spawned unit's frame reaches within %d calls: %d" % (DEPTH, len(prev)))


def chain(f):
    out = []
    while prev.get(f):
        a, s = prev[f]
        out.append("%08X@%08X" % (a, s))
        f = a
    return " -> ".join(reversed(out))


enemy = {}
for e, f, s, v in rows:
    if f in READERS:
        continue
    site_k0 = any(x == "KIND0-ONLY" for x, _ in v)
    enemy[s] = (f in prev) and not site_k0
    print("      %08X @ %08X  %s" % (f, s, ("SPAWNED UNITS REACH IT via " + chain(f)) if enemy[s] else
          ("the site itself is kind-0 only" if site_k0 else "not reached from a unit frame")))
# P1 - reached from a spawned unit's frame with no kind-0-only hop, flag check without a kind test: the combo gate
#      (00308610), the combo continuation (0030C010), engagement (00307D10, through the status-change path 0030E360),
#      the AI distance threshold (00309A90, through AiOrder_CheckActionPreconditions 00301830) and five locomotion sites
check("P1", all(enemy.get(s) for s in (0x0030877D, 0x0030C02E, 0x00307D63, 0x00309A94, 0x003368FD, 0x00339D52,
                                       0x00339D7E, 0x0033B02D, 0x0033C3EA, 0x0033D1A1)),
      "combo gate, combo continuation, engagement, AI distance threshold and 6 locomotion sites run on spawned units")
# P3 - stance (00308130) is party only: each of its three callers tests the same unit's kind byte for 0 first
#      (00301A6E-00301A74, 00307E0A-00307E10, 0030BFED-0030BFF3)
check("P3", enemy.get(0x0030815A) is False and all(any(v == "KIND0-ONLY" for v, _ in classify(f, s))
      for f, s in c["calls"][0x00308130]) and len(c["calls"][0x00308130]) == 3,
      "stance 00308130: all 3 callers gate on kind 0")
# P4 - not on a unit's frame: the capability policy 00313A00, the field-frame orchestrator 00234590 and the command-menu
#      readers of 00253BA0 (00276650, 00276D30)
check("P4", all(enemy.get(s) is False for s in (0x00313A2C, 0x00234629, 0x0027668C, 0x00276FD3)),
      "capability policy, field-frame orchestrator and command menu are not reached from a unit frame")
# P2 - the kind-0 gates: the availability reason 0x24 (002FFDC9) and the locomotion site 00339C2C are party only
check("P2", enemy.get(0x002FFDC9) is False and enemy.get(0x00339C2C) is False,
      "reason 0x24 and locomotion site 00339C2C act on party units only")
print("FAILS %d" % fails)
