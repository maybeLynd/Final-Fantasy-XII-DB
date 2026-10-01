"""gr17_graph2.py - boundary-checked direct call graph (reviewer instrument, GR-17 review 2026-09-30).

rawcalls.json is a RAW byte index: it holds E8/E9 bytes inside other instructions (e.g. 00224E85 'call 00294472', a
target in the middle of 00293FE0's code). Here an edge is kept only if (1) the site is an instruction boundary of a
linear decode of its .pdata chunk (or, for a leaf without .pdata, of the decode from the nearest preceding call target),
and (2) the target is a .pdata chunk start or lies outside every .pdata range (a leaf). Cross-function jcc (0F 8x) edges
are added under the same two tests. Then: the reach set to 00312280, the window-callee probes, and a path per probe.
"""
import sys, os, struct, re, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr17_graph as GG
import gr17_path2 as P
G = GG.G; T = GG.T

BOUND = set()
for b, e, u in G.PD:
    for i in T.dis(T.IB + b, T.IB + e):
        BOUND.add(i.address)
PDS = [T.IB + b for b, e, u in G.PD]
PDE = {T.IB + b: T.IB + e for b, e, u in G.PD}


def in_pdata(va):
    j = bisect.bisect_right(PDS, va) - 1
    return j >= 0 and PDS[j] <= va < PDE[PDS[j]]


leaf_cache = {}


def on_boundary(s):
    if in_pdata(s):
        return s in BOUND
    st = GG.fn(s)
    if st not in leaf_cache:
        leaf_cache[st] = set(i.address for i in T.dis(st, st + 0x400))
    return s in leaf_cache[st]


def ok_target(t):
    return (G.root(t) is not None and t in PDE) or not in_pdata(t)


def build(jcc):
    ed = {}
    drop = 0
    for k, sites in GG.RC.items():
        t = int(k, 16)
        if not ok_target(t):
            drop += len(sites)
            continue
        for s in sites:
            s = int(s, 16)
            if not on_boundary(s):
                drop += 1
                continue
            a = GG.fn(s); b = GG.tfn(t)
            if a != b:
                ed.setdefault(a, {}).setdefault(b, s)
    nj = 0
    if jcc:
        for n, v, vs, p, rs in T.TEXT:
            blob = T.raw[p:p + min(vs, rs)]
            for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
                k = m.start()
                if k + 6 > len(blob):
                    continue
                d = struct.unpack_from("<i", blob, k + 2)[0]
                t = v + k + 6 + d
                a = GG.fn(v + k)
                if not (T.IB < t < T.IB + 0x3000000) or not ok_target(t) or GG.tfn(t) == a:
                    continue
                if G.root(t) != t and in_pdata(t):
                    continue
                if not on_boundary(v + k):
                    continue
                # a jcc to a leaf start must land on a known call target or .pdata start
                if not in_pdata(t) and ("%X" % t) not in GG.RC:
                    continue
                ed.setdefault(a, {}).setdefault(GG.tfn(t), v + k)
                nj += 1
    return ed, drop, nj


if __name__ == "__main__":
    probes = [0x0024CFF0, 0x002693D0, 0x002E3AF0, 0x00319140, 0x002EB780, 0x003603F0, 0x0032E620, 0x0036DE70,
              0x003DEE10, 0x003EB010, 0x0024E910, 0x003319D0, 0x00300140, 0x0046EFD0, 0x003B8670, 0x00319F50]
    for jcc in (False, True):
        ed, drop, nj = build(jcc)
        R = P.reach(ed)
        print("boundary-checked, jcc=%s: dropped %d raw sites; %d jcc edges; %d functions reach 00312280" % (jcc, drop, nj, len(R)))
        print("   probes: %s" % " ".join("%08X=%s" % (p, p in R) for p in probes))
        for src in probes:
            if src in R and src not in (0x00300140, 0x0046EFD0, 0x003B8670, 0x00319F50):
                p = P.path(ed, src)
                print("   path %08X: %s" % (src, " | ".join("%08X@%08X" % (b, s) for a, s, b in p)))
    # window sites against the boundary-checked graph with jcc
    ed, drop, nj = build(True)
    R = P.reach(ed)
    print("== window (package S9) against the boundary-checked graph with jcc")
    ranges = [(0x003EA888, 0x003EA9FC, "003EA820 after the first free"), (0x0032FC50, 0x0032FC9E, "0032FC30 after 003EA6E0"),
              (0x0032FCA0, 0x0032FCFB, "0032FCA0 to 0032FCF6"), (0x002628B0, 0x00262D39, "002628B0 to 00262D34"),
              (0x0025B070, 0x0025B249, "0025B070"), (0x00234200, 0x002342D3, "00234200 to 002342CE")]
    tot = 0
    for lo, hi, nm in ranges:
        ins = T.dis(lo, hi)
        direct, reach_, indirect = 0, [], []
        for i in ins:
            if i.mnemonic in ("call", "jmp") or (i.mnemonic.startswith("j") and i.operands):
                op = i.operands[0]
                if op.type == 2:
                    t = op.imm
                    if i.mnemonic == "call" or not (lo <= t < hi):
                        direct += 1
                        if GG.tfn(t) in R:
                            reach_.append("%08X->%08X" % (i.address, t))
                elif i.mnemonic in ("call", "jmp"):
                    indirect.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
        tot += direct
        print("  %s: %d direct call/tail sites; reaching: %s; indirect: %s" % (nm, direct, reach_, indirect))
    print("  total direct call/tail sites %d" % tot)
