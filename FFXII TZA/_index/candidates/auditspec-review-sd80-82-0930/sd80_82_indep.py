"""sd80_82_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-80 / SD-82 (2026-09-30). Read-only.
Does not use retool or the rc22-34 `pe` module.

Part 1 (SD-80 S1/S3/S6): re-compare the identity pairs with an own normaliser (tk.fdis; rip displacements masked,
local branch targets as offsets, outside call/jmp targets listed).

Part 2 (SD-82): a rotation matcher that is NOT a store-order signature. It looks for the core data flow of a rotation
about x with child offset c and opposite child c2, register names tracked:
    y = [x + c]          (load)
    t = [y + c2]         (load, within 12 instructions)
    [x + c] = t          (store, within 12 instructions)
    [y + c2] = x         (store, within 40 instructions of the first load)
EASTL layout (children +0 / +8): c = 0 is the left rotation (right child at +0), c = 8 the right rotation.
MSVC layout (children +0 / +0x10) is run as a second family so the matcher's sensitivity is shown on known bodies.
Body list: every functions.tsv entry plus every .pdata range whose start is not a listed entry (covers unlisted code).
"""
import sys, re, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

def norm(f):
    sz = tk.fsize(f); out, tg = [], []
    for x in tk.fdis(f):
        op = x.op_str
        if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and op.startswith("0x"):
            t = int(op, 16)
            if 0 <= t - f < sz: op = "L+%x" % (t - f)
            else: tg.append(t); op = "T"
        out.append(x.mnemonic + " " + re.sub(r"\[rip \+ 0x[0-9a-f]+\]", "[RIP]", op))
    return out, tg

print("Part 1: identity pairs (own normaliser)")
PAIRS = [(0x714B60, 0x714BE0), (0x714B60, 0x714C60), (0x714B60, 0x79B0D0), (0x79B930, 0x714CE0), (0x79B930, 0x715110),
         (0x79B930, 0x7151F0), (0x79B930, 0x71F4B0), (0x714980, 0x799B80), (0x799BD0, 0x71F240)]
for a, b in PAIRS:
    na, ta = norm(a); nb, tb = norm(b)
    print("  %08X vs %08X: %d/%d insns, identical=%s, targets of %08X: %s" % (
        a, b, len(na), len(nb), na == nb, b, " ".join("%08X" % t for t in tb)))
import difflib
for a, b in ((0x714980, 0x71F1E0), (0x79BA10, 0x71F590)):
    na, _ = norm(a); nb, tb = norm(b)
    na = [re.sub(r"L\+[0-9a-f]+", "L", v) for v in na]; nb = [re.sub(r"L\+[0-9a-f]+", "L", v) for v in nb]  # label-free
    ops = [o for o in difflib.SequenceMatcher(a=na, b=nb, autojunk=False).get_opcodes() if o[0] != "equal"]
    print("  %08X -> %08X diff ops: %s; inserted: %s" % (a, b, [(o[0], o[2] - o[1], o[4] - o[3]) for o in ops],
          [nb[o[3]:o[4]] for o in ops if o[0] == "insert"]))

print("Part 2: data-flow rotation matcher")
md = Cs(CS_ARCH_X86, CS_MODE_64)
LOAD = re.compile(r"^(\w+), qword ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\]$")
STORE = re.compile(r"^qword ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\], (\w+)$")
def disp(s): return int(s, 0) if s else 0  # capstone prints small displacements in decimal

bodies = {e: e + sz for e, sz in tk.flist}
listed = len(bodies)
for b, e in tk.pdata:
    if b not in bodies: bodies[b] = e
print("  bodies: %d listed + %d .pdata-only = %d" % (listed, len(bodies) - listed, len(bodies)))

def st(op):
    g = STORE.match(op)
    return (g.group(1), disp(g.group(2)), g.group(3)) if g else None

FAM = {"EASTL": (0, 8), "MSVC": (0, 0x10)}
def scan(insns, c, c2):
    n = 0
    L = len(insns)
    for i in range(L):
        m, op = insns[i]
        if m != "mov": continue
        g = LOAD.match(op)
        if not g or g.group(2) in ("rip", "rsp", "rbp") or disp(g.group(3)) != c: continue
        y, x = g.group(1), g.group(2)
        if y == x: continue
        for j in range(i + 1, min(L, i + 13)):
            m2, op2 = insns[j]
            g2 = LOAD.match(op2) if m2 == "mov" else None
            if g2 and g2.group(2) == y and disp(g2.group(3)) == c2:
                t = g2.group(1)
                ok3 = any(insns[k][0] == "mov" and STORE.match(insns[k][1]) and st(insns[k][1]) == (x, c, t) for k in range(j + 1, min(L, j + 13)))
                ok4 = any(insns[k][0] == "mov" and STORE.match(insns[k][1]) and st(insns[k][1]) == (y, c2, x) for k in range(j + 1, min(L, i + 41)))
                if ok3 and ok4:
                    n += 1
                break
    return n

hits = collections.defaultdict(dict)
for b in sorted(bodies):
    o = tk.off(b)
    if o is None: continue
    ins = [(x.mnemonic, x.op_str) for x in md.disasm(tk.d[o:o + (bodies[b] - b)], b)]
    for fam, (p, q) in FAM.items():
        a1, a2 = scan(ins, p, q), scan(ins, q, p)
        if a1 or a2: hits[fam][b] = (a1, a2)
for fam in FAM:
    print("  %s layout (children %s): %d bodies" % (fam, FAM[fam], len(hits[fam])))
    for b, (a1, a2) in sorted(hits[fam].items()):
        isnil = any("+ 0x19], 0" in x.op_str for x in tk.dis(b, bodies[b]))
        print("     %08X size %6d  c=first %d  c=second %d  both=%s  isnil19=%s  %s" % (
            b, bodies[b] - b, a1, a2, bool(a1 and a2), isnil, "listed" if tk.fsize(b) else "pdata-only"))
