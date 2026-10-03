"""WT-4 exposure bound (SWE2-DATA, 2026-10-03): can EXP-191's intercepted callees 0017D280 / 0032FC30 reach a writer of
01EED060 / 01EED064? Writers = every instruction in the image whose memory operand is rip-relative to either cell and is a
store (capstone access flags). Reach = the E8/E9 call-graph closure in graph/edges.tsv (EH edges excluded), plus a raw
E8/E9 scan of each reached body (thunks and unlisted calls). Static; a reach census, not an execution."""
import collections, csv, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
CELLS = {0x01EED060, 0x01EED064}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0"), struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0],
                 struct.unpack_from("<I", d, o + 20)[0]))
def off(a):
    r = a - BASE
    for nm, va, vs, ro in secs:
        if va <= r < va + vs: return ro + (r - va)
funcs, tags = {}, {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: e = int(p[0], 16)
    except ValueError: continue
    funcs[e] = int(p[2]); tags[e] = "\t".join(p[3:])
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
entries = sorted(funcs)
import bisect
def owner(a):
    i = bisect.bisect_right(entries, a) - 1
    return entries[i] if i >= 0 and a < entries[i] + funcs[entries[i]] else None
def body(fn):
    o = off(fn)
    return list(md.disasm(d[o:o + funcs[fn]], fn)) if o is not None else []
# 1. writers of the cells, image-wide over .text
text = [s for s in secs if s[0] == b".text"][0]
writers = set()
for fn in entries:
    if "CompilerGeneratedEH" in tags.get(fn, ""): continue
    for x in body(fn):
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                tgt = x.address + x.size + op.mem.disp
                if tgt in CELLS and (op.access & CS_AC_WRITE):
                    writers.add((fn, x.address, "%s %s" % (x.mnemonic, x.op_str)))
print("writers of 01EED060/01EED064:")
for w in sorted(writers): print("   %08X in %08X  %s" % (w[1], w[0], w[2]))
wfn = {w[0] for w in writers}
# 2. call closure from each intercepted callee (direct E8/E9 to function entries)
def callees(fn):
    out = set()
    for x in body(fn):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            o = owner(t)
            if o is not None and o != fn and "CompilerGeneratedEH" not in tags.get(o, ""): out.add(o)
    return out
for root in (0x0017D280, 0x0032FC30):
    seen, work, parent = {root}, [root], {}
    while work:
        f = work.pop()
        for c in callees(f):
            if c not in seen:
                seen.add(c); parent[c] = f; work.append(c)
    hit = sorted(seen & wfn)
    print("closure of %08X: %d functions; writers reached: %s" % (root, len(seen), ["%08X" % h for h in hit]))
    for h in hit:
        path, x = [h], h
        while x in parent: x = parent[x]; path.append(x)
        print("   path: " + " <- ".join("%08X" % p for p in path))
    indirect = sum(1 for f in seen for x in body(f) if x.mnemonic == "call" and not x.op_str.startswith("0x"))
    print("   indirect calls inside the closure (not followed): %d" % indirect)
