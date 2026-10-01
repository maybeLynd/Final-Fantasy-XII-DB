"""tail_disp_hits.py - SWE2-AUDIT-SPEC: what field_disp_scan's linear decode (capstone md.disasm from the entry over
[entry, entry+size)) now emits inside the 254 extended tails. Counts decoded instructions that START at or past the
listed end and carry a non-rip memory operand with a displacement - the population field_disp_scan matches against
--disp. Split by tail kind (jump-table tail vs other) using the same leading-RVA rule as tail_kinds.py."""
import os, sys, struct, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
BASE = tk.BASE
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
txt = subprocess.run(["git", "-C", ROOT, "show", "d20226c17:Database/FFXII TZA/_index/FUNCTION-EXTENT-ERRATA.tsv"], capture_output=True).stdout.decode()
rows = []
for i, line in enumerate(txt.splitlines()):
    p = line.split("\t")
    if i and len(p) >= 15 and p[14].strip() == "pdata-chain":
        rows.append((int(p[0], 16), int(p[3], 16), int(p[12], 16)))
def is_jt(r, le, ce):
    a = le
    while a < ce and (a & 3): a += 1
    n, lead = (ce - a) // 4, 0
    while lead < n and r <= BASE + struct.unpack_from("<I", tk.d, tk.off(a) + 4 * lead)[0] < ce: lead += 1
    return lead >= 2
hits = collections.Counter(); rows_hit = collections.Counter(); disp_vals = collections.Counter(); ex = []
for r, le, ce in rows:
    kind = "jtable" if is_jt(r, le, ce) else "other"
    code = tk.d[tk.off(r):tk.off(r) + (ce - r)]
    n = 0
    for ins in md.disasm(code, r):
        if ins.address < le: continue
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base != X86_REG_RIP and op.mem.disp != 0:
                n += 1; disp_vals[op.mem.disp & 0xFFFFFFFF] += 1
                if kind == "jtable" and len(ex) < 6: ex.append("%08X %s %s" % (ins.address, ins.mnemonic, ins.op_str))
                break
    hits[kind] += n
    if n: rows_hit[kind] += 1
print("decoded tail instructions with a non-rip displacement memory operand: %s; rows with any: %s" % (dict(hits), dict(rows_hit)))
small = sum(c for v, c in disp_vals.items() if v < 0x2000)
print("distinct displacement values %d; hits with a field-sized displacement (< 0x2000): %d" % (len(disp_vals), small))
print("examples (jump-table bytes decoded as instructions):")
for e in ex: print("  " + e)
