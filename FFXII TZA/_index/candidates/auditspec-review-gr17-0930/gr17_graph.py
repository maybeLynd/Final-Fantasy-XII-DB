"""gr17_graph.py - SWE2-AUDIT-SPEC (GR-17 review, 2026-09-30). Independent direct call graph, not retool.py's cache.

Edges: every E8/E9 rel32 site in rawcalls.json (FABLE's raw index) PLUS every 0F 8x jcc whose target lies in another
function (swept here from the image bytes). A site/target is mapped to its function by .pdata root (chained unwind
followed); a site without .pdata (a leaf) is mapped to the nearest preceding call/jmp target or .pdata start.

  R  the set of functions that can reach 00312280 (the reward computer) by direct edges; count vs the package's 383.
  W  the window bodies (S9): every call/jmp/jcc site in the listed address ranges, whether its target is in R, and
     every indirect call/jmp in those ranges.
  O  the timeline interpreter's opcode arms (package E6): for each arm start given on the command line, the direct
     closure from that address's straight-line code up to its next jmp back to the dispatcher is not computed here;
     instead the dispatcher's function-level edges into R are listed (every call site in 003B8670's body whose
     target is in R), so an arm the package missed shows up as an extra site.
"""
import os, sys, struct, json, bisect, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gr17_indep as G  # noqa: E402
T = G.T
from capstone import CS_OP_MEM, CS_OP_REG

RC = G.RC
starts = set(T.IB + b for b, e, u in G.PD)
for k in RC:
    starts.add(int(k, 16))
SS = sorted(starts)


def fn(va):
    r = G.root(va)
    if r:
        return r
    j = bisect.bisect_right(SS, va) - 1
    return SS[j] if j >= 0 else va


def tfn(t):
    r = G.root(t)
    return r if r else t


edges = {}
for k, sites in RC.items():
    t = int(k, 16)
    for s in sites:
        a = fn(int(s, 16))
        b = tfn(t)
        if a != b:
            edges.setdefault(a, set()).add(b)
# jcc sweep
njcc = 0
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
        k = m.start()
        if k + 6 > len(blob):
            continue
        d = struct.unpack_from("<i", blob, k + 2)[0]
        t = v + k + 6 + d
        if not (v <= t < v + len(blob)):
            continue
        a = fn(v + k)
        b = tfn(t)
        if a != b and G.root(t) == t:   # a jcc landing on a function start in another function
            edges.setdefault(a, set()).add(b)
            njcc += 1
rev = {}
for a, bs in edges.items():
    for b in bs:
        rev.setdefault(b, set()).add(a)

TARGET = 0x00312280
R = {TARGET}
st = [TARGET]
while st:
    x = st.pop()
    for y in rev.get(x, ()):
        if y not in R:
            R.add(y)
            st.append(y)

if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "RW"
    if "R" in part:
        print("== R. direct reach to 00312280 (E8/E9 from rawcalls.json + cross-function jcc to a function start: %d)" % njcc)
        print("  functions that reach: %d" % len(R))
        for f in (0x0030E360, 0x00300140, 0x0046EFD0, 0x003B8670, 0x002EB740, 0x00319F50, 0x003B1260, 0x0024FE70,
                  0x0024FE30, 0x00319420, 0x00310780, 0x003105D0, 0x00234200, 0x00319140, 0x002EB780, 0x002FD0C0,
                  0x003B3C00, 0x005372D0, 0x004FF2C0, 0x00333280, 0x003331A0, 0x003A74F0, 0x003337B0):
            print("    %08X reaches: %s" % (f, f in R))
    if "W" in part:
        print("== W. window bodies (package S9)")
        ranges = [(0x003EA888, None, "003EA820 after the first free"), (0x0032FC50, 0x0032FC9E, "0032FC30 after 003EA6E0"),
                  (0x0032FCA0, 0x0032FCFB, "0032FCA0 to 0032FCF6"), (0x002628B0, 0x00262D39, "002628B0 to 00262D34"),
                  (0x0025B070, 0x0025B249, "0025B070"), (0x00234200, 0x002342D3, "00234200 to 002342CE")]
        for lo, hi, nm in ranges:
            if hi is None:
                # to the end of 003EA820's pdata extent(s)
                hi = max(T.IB + e for b, e, u in G.PD if G.root(T.IB + b) == 0x003EA820)
            ins = T.dis(lo, hi)
            direct, reach, indirect = 0, [], []
            for i in ins:
                if i.mnemonic == "call" or i.mnemonic == "jmp" or (i.mnemonic.startswith("j") and i.mnemonic != "jmp"):
                    op = i.operands[0] if i.operands else None
                    if op is not None and op.type == 2:
                        t = op.imm
                        if i.mnemonic == "call" or not (lo - 0x2000 <= t < hi + 0x2000):
                            direct += 1
                            if tfn(t) in R:
                                reach.append("%08X->%08X" % (i.address, t))
                    elif op is not None:
                        indirect.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
            print("  %s [%08X,%08X): %d direct call/tail sites; reaching R: %s; indirect: %s" % (nm, lo, hi, direct, reach, indirect))
