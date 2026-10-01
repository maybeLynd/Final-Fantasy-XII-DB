"""S-33 / EXP-141 stub exposure, static half (OPUS, 2026-09-25, block 309).

For each of EXP-141's five scripted leaves (003FA160 op1, 003FAA10 op2, 003FA820 ops 3/4/5, 003FA900 op6, 00300B80 the
inventory grant) this asks, over the leaf's whole static closure (edges.tsv, direct edges):
  1. does any instruction reference the pool state - the nodes 02EC0FA0..02EC135F, head/tail 02EC1360/02EC1368, the
     presence table 022BE7F0 + i*0x20 (i < 10, 0x20 stride -> ..022BE92F), the collected counter 022C3174?
     (RIP-relative operands and absolute immediates; a register-relative write through a pointer the leaf was handed is
     answered by 2)
  2. does the closure call back into any pool function (00319600..00319D40, 002FB250/002FB2A0/002FB2D0), or into
     00319850 / 002FB150, the two readers that hand out node pointers?
  3. which leaf is handed a pool pointer at all? (the call-site argument registers, read from the pool bodies)
and, at every call site of 0028F000 / 00300B80 inside the pool bodies, whether the return value is read before being
overwritten (the only way a scripted return could reach pool state).
Evidence class: STATIC (capstone over the SHA-asserted image). Writes s33_leaf_reach.out.txt next to this file.
"""
import collections
import csv
import hashlib
import os
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
LEAVES = {0x3FA160: "op1", 0x3FAA10: "op2", 0x3FA820: "op3/4/5", 0x3FA900: "op6", 0x300B80: "grant"}
POOL_FNS = {0x319600, 0x3197B0, 0x319830, 0x319920, 0x319A00, 0x319A20, 0x319B10, 0x319CA0, 0x2FB250, 0x2FB2A0, 0x2FB2D0,
            0x319850, 0x2FB150}   # + the two readers that hand out node pointers (nearest selector, overlap test)
RANGES = [(0x2EC0FA0, 0x2EC1370, "pool nodes + head/tail"), (0x22BE7F0, 0x22BE930, "presence table"),
          (0x22C3174, 0x22C3178, "collected counter")]
POOL_BODIES = [0x319600, 0x319920, 0x3197B0, 0x319CA0]

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
n = struct.unpack_from("<H", raw, pe + 6)[0]
o = pe + 24 + struct.unpack_from("<H", raw, pe + 20)[0]
secs = []
for _ in range(n):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, o + 8)
    secs.append((va + 0x120000, rs, ra))
    o += 40


def off(v):
    for va, rs, ra in secs:
        if va <= v < va + rs:
            return ra + v - va


size = {}
for r in csv.DictReader(open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
    try:
        size[int(r["entry"], 16)] = int(r["body_bytes"])
    except (ValueError, KeyError):
        pass
g = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        g[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(g[x])
    return seen


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def refs(fn):
    hits = []
    k = off(fn)
    if k is None or fn not in size:
        return hits, False
    for ins in md.disasm(raw[k:k + size[fn]], fn):
        for op in ins.operands:
            t = None
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = ins.address + ins.size + op.mem.disp
            elif op.type == X86_OP_MEM and op.mem.base == 0 and op.mem.index == 0:
                t = op.mem.disp
            elif op.type == X86_OP_IMM:
                t = op.imm
            if t is not None:
                for lo, hi, nm in RANGES:
                    if lo <= t < hi:
                        hits.append("%08X %s %s -> %s %08X" % (ins.address, ins.mnemonic, ins.op_str, nm, t))
    return hits, True


out = []
for leaf, nm in LEAVES.items():
    c = closure(leaf)
    back = sorted("%08X" % x for x in c & POOL_FNS)
    allhits, unread = [], []
    for fn in sorted(c):
        h, ok = refs(fn)
        allhits += h
        if not ok:
            unread.append("%08X" % fn)
    out.append("LEAF %08X (%s): closure %d functions; pool-global references %d; calls back into the pool: %s; bodies without a size row: %s"
               % (leaf, nm, len(c), len(allhits), back or "none", unread or "none"))
    out += ["    " + h for h in allhits[:20]]

out.append("")
out.append("CALL SITES of 0028F000 / 00300B80 inside the pool bodies: the next instructions (is eax read before it is written?)")
for body in POOL_BODIES:
    k = off(body)
    ins = list(md.disasm(raw[k:k + size.get(body, 0x200)], body))
    for i, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str in ("0x28f000", "0x300b80"):
            nxt = ins[i + 1:i + 5]
            prev = ins[max(0, i - 4):i]
            out.append("  %08X  call %s   args: %s   | after: %s" % (
                x.address, x.op_str, "; ".join("%s %s" % (p.mnemonic, p.op_str) for p in prev),
                "; ".join("%08X %s %s" % (q.address, q.mnemonic, q.op_str) for q in nxt)))
text = "\n".join(out)
print(text)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "s33_leaf_reach.out.txt"), "w", encoding="utf-8").write(text + "\n")
