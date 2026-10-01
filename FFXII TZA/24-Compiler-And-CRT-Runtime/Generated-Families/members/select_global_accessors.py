"""select_global_accessors.py [--write] - EC-7 selector for the trivial global
accessor family (SWE2-EC7, 2026-09-16; FABLE-REQ-SWE2-EC7-GLOBAL-ACCESSORS-B).

Independent re-derivation of FABLE's accessor-family/global_accessors.py: my
own candidate enumeration is every frontier census entry whose decoded body is
exactly two instructions - <one instruction with a single RIP-relative memory
operand>, then RET. The operand's section must be a data section (.data /
.rdata / .bss-side address inside .data's virtual range); a .text operand is a
code address, refused as not-a-global.

Member semantics, complete in the TSV (address, kind, width, global, section,
operand, mnemonic):
   read        mov/movzx/movsx/movsxd/movss/movsd/movaps/movups/movq/movd
               reg, [rip+global]
   addr        lea reg, [rip+global]
   write       mov*/[rip+global], reg
   write-const mov [rip+global], imm

Anything else - two memory accesses, a flag test, arithmetic, a call, an
extra instruction, a non-RIP operand - is refused. The member table carries
the ENTIRE behaviour of each member, which is the B bar: ignorance of a member
cannot prevent reproducing FFXII. The 454 globals' meanings are NOT
dispositioned by the row.

Controls printed: refusal census; distinct-global count; globals shared by
more than one member; the diff against FABLE's list (membership agreement is
reported, not assumed).

Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe,
graph/functions.tsv; needs capstone."""
import sys, os, struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "Trivial global accessors"
IMG = 0x120000

d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (IMG + va, vs, ro, rs)
def section_of(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + max(vs, rs):
            return next(k for k, v in secs.items() if v[0] == va)
def body(e):
    o = off(e); return d[o:o + sizes[e]] if o is not None else b""
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)

sizes = cd.load_functions()
# UC-1 SERIES BREAK (2026-09-28): the default census now also carries the UC-1 frontier bodies, which are
# frontier BY RULING - never A/B/C by default - and check_dispositions refuses any members file that names one.
# Leave them out of the population so a re-run reproduces the declared family: unpatched, this selector admitted
# 10 UC-1 bodies on 2026-09-29. The same patch select_ppfx.py / select_audio_libraries.py / select_libvpx.py
# received in 839236205. SWE2-EC7 2026-09-29 (FABLE family ruling R3).
import uc1_band
sizes = {k: v for k, v in sizes.items() if k not in uc1_band.frontier_starts()}
ents = sorted(sizes); eset = set(ents)
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
frontier = [e for e in ents if e not in a_set and e not in declared]

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
READ = {"mov", "movzx", "movsx", "movsxd", "movss", "movsd", "movaps", "movups", "movq", "movd"}

rows, refused = [], collections.Counter()
for e in frontier:
    if sizes[e] <= 0 or sizes[e] > 24:           # one instruction + ret cannot exceed this
        continue
    ins = list(md.disasm(body(e), e))
    if len(ins) != 2 or ins[1].mnemonic != "ret":
        if len(ins) <= 3: refused["not one instruction + ret"] += 1
        continue
    i = ins[0]; ops = i.operands
    mem = [op for op in ops if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and op.mem.index == 0]
    if len(ops) != 2 or len(mem) != 1:
        refused["no single rip operand"] += 1; continue
    g = i.address + i.size + mem[0].mem.disp
    if i.mnemonic == "lea" and ops[0].type == X86_OP_REG:
        kind, other = "addr", md.reg_name(ops[0].reg)
    elif ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM and i.mnemonic in READ:
        kind, other = "read", md.reg_name(ops[0].reg)
    elif ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG and i.mnemonic in READ:
        kind, other = "write", md.reg_name(ops[1].reg)
    elif ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_IMM and i.mnemonic == "mov":
        kind, other = "write-const", "%#x" % (ops[1].imm & 0xFFFFFFFFFFFFFFFF)
    else:
        refused["other instruction %s" % i.mnemonic] += 1; continue
    s = section_of(g)
    if s == ".text": refused["global in .text"] += 1; continue
    rows.append((e, kind, mem[0].size, g, s, other, i.mnemonic))

members = [r[0] for r in rows]
print("frontier tested %d -> %d members" % (len(frontier), len(rows)))
print("kinds", sorted(collections.Counter((r[1], r[2]) for r in rows).items()))
print("sections", collections.Counter(r[4] for r in rows))
print("refused", sorted(refused.items(), key=lambda kv: -kv[1])[:8])
per = collections.Counter(r[3] for r in rows)
dup = collections.Counter((r[1], r[2], r[3], r[5]) for r in rows)
print("distinct globals %d   shared-by->1-member %d   identical-body duplicates %d"
      % (len(per), sum(1 for c in per.values() if c > 1), sum(c - 1 for c in dup.values() if c > 1)))

# diff against FABLE's independently-derived list
fp = os.path.join(W, "FABLE", "accessor-family", "global_accessors.tsv")
if os.path.exists(fp):
    fable = set()
    for line in open(fp):
        p = line.split("\t")
        try: fable.add(int(p[0], 16))
        except (ValueError, IndexError): pass
    mine = set(members)
    print("FABLE list %d - mine %d - only-FABLE %d %s - only-mine %d %s"
          % (len(fable), len(mine), len(fable - mine), sorted("%08X" % x for x in fable - mine)[:8],
             len(mine - fable), sorted("%08X" % x for x in mine - fable)[:8]))

if "--write" in sys.argv:
    out = os.path.join(HERE, "trivial-global-accessors.tsv")
    with open(out, "w", newline="\n") as f:
        f.write("# trivial global accessors: body = one RIP-relative global access + ret - select_global_accessors.py\n")
        f.write("address\tkind\twidth\tglobal\tsection\toperand\tmnemonic\n")
        for e, k, w, g, s, o, m in rows:
            f.write("%08X\t%s\t%d\t%08X\t%s\t%s\t%s\n" % (e, k, w, g, s, o, m))
    print("wrote", len(rows))
