"""ee_member_calls.py - a SECOND instrument for UQ-38 (whole translated routine vs C routine with translated fragments),
using a different signal from FRONTIER's bank-access density: what ELSE the body does.

A routine translated whole from PS2 assembly keeps its registers in the bank, so it has (a) no calls except the
bank save/restore pair 0036D930 / 0036D8E0 and (b) almost no stack-slot traffic beyond the prologue. A C routine
with translated fragments has ordinary calls and ordinary [rsp+..]/[rbp+..] locals around the fragments.

Per member (all 267 of ee-register-census.tsv, cited or not): size, insns, bank ops, calls (other than the pair),
stack-slot operands, and a verdict:
   whole        no other calls, stack operands <= 5 % of insns
   mostly       no other calls, more stack traffic than that (translated body with spills through the frame)
   C+fragments  calls other functions
Compared against FRONTIER's `split` for the 188 rows that have one. Two controls named in the page: 004355D0 and
00437130 are C with fragments (section 5). Output TSV to the scratch dir."""
import os, re, struct, sys, csv, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
DBM = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\00-Engine-Core-Runtime\Shared-Transform-Workbench\members"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ee-member-calls.tsv")
BASE = 0x120000
BANK = [(0x022D8F10, 0x022D94A0), (0x01EF93F0, 0x01EF9400)]
PAIR = {0x36D930, 0x36D8E0}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((BASE + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs: return ro + (a - va)
sizes = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
members = [int(l.split("\t")[0], 16) for l in open(os.path.join(DBM, "ee-register-census.tsv"), encoding="utf-8") if not l.startswith(("function", "#"))]
MSET = set(members)
fr = {}
for r in csv.DictReader(open(os.path.join(DBM, "ee-register-members.tsv"), encoding="utf-8"), delimiter="\t"):
    fr[int(r["address"], 16)] = r["split"]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
rows = []
for f in members:
    ins = list(md.disasm(d[off(f):off(f) + sizes[f]], f))
    bank = calls = stack = 0; callees = set()
    for x in ins:
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == X86_OP_IMM:
            t = x.operands[0].imm
            if x.mnemonic == "call" or not (f <= t < f + sizes[f]):
                if t not in PAIR and t in sizes and t not in MSET:
                    calls += 1; callees.add(t)
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.base:
                b = x.reg_name(op.mem.base)
                if b == "rip":
                    t = x.address + x.size + op.mem.disp
                    if any(lo <= t < hi for lo, hi in BANK): bank += 1
                elif b in ("rsp", "rbp"):
                    stack += 1
    ni = max(len(ins), 1)
    if calls == 0:
        v = "whole" if stack / ni <= 0.05 else "mostly"
    else:
        v = "C+fragments"
    rows.append((f, sizes[f], len(ins), bank, calls, stack, v, fr.get(f, "-")))
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("function\tsize\tinsns\tbank_ops\tother_calls\tstack_ops\tverdict\tfrontier_split\n")
    for r in rows: fh.write("%08X\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n" % r)
print("members:", len(rows))
print("verdict:", collections.Counter(r[6] for r in rows))
print("verdict x frontier split (188 with one):")
ct = collections.Counter((r[6], r[7]) for r in rows if r[7] != "-")
for k, v in sorted(ct.items()): print("   %-12s %-12s %d" % (k[0], k[1], v))
print("controls: 004355D0 ->", [r[6] for r in rows if r[0] == 0x4355D0], " 00437130 ->", [r[6] for r in rows if r[0] == 0x437130])
print("largest 'whole':", sorted([(r[1], "%08X" % r[0]) for r in rows if r[6] == "whole"], reverse=True)[:6])
print("cited (no frontier split) verdicts:", collections.Counter(r[6] for r in rows if r[7] == "-"))
