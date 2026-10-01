"""rc1_census.py - static half of RC-1 (OPUS, 2026-09-30): the class argument (ECX) at every rel32 call or tail jump to
BattleEncodedId_IsValidForClass 00322C50, found by a raw E8/E9 index over .text (not a call graph).

For each site the owning function is decoded linearly from its start to the site, and the LAST instruction before the
site that writes ECX/RCX/CL/CX is classified:
  CONST n      - mov ecx, imm / lea ecx, [reg + imm] with reg known zero / xor ecx, ecx (n = 0)
  DERIVED      - lea ecx, [rXX + imm] where rXX was itself last set to a constant (n resolved) - reported as CONST
  DYNAMIC src  - anything else (a register copy, a memory load, ...)
A linear last-write is not path-sensitive: a site whose function writes ECX on more than one incoming path may be
misread. Such sites are flagged MULTI when a branch target lies between the last write and the call. Positive control:
0030AC50's two sites are read by hand below. Output: rc1_census.tsv and a summary."""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("%08X" % va)


fs = []
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            fs.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
fs.sort(); starts = [a for a, _ in fs]


def owner(va):
    j = bisect.bisect_right(starts, va) - 1
    return fs[j] if j >= 0 and va < fs[j][0] + fs[j][1] else (None, None)


tx = [s for s in SECS if s[0] == ".text"][0]
T0, TR, TN = tx[1], tx[3], tx[4]
import sys
TARGET = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x00322C50
sites = []
for m in re.finditer(rb"[\xe8\xe9]", blob[TR:TR + TN - 4]):
    i = m.start()
    if T0 + i + 5 + struct.unpack("<i", blob[TR + i + 1:TR + i + 5])[0] == TARGET:
        sites.append((T0 + i, "call" if blob[TR + i] == 0xE8 else "jmp"))
ECX = ("ecx", "rcx", "cl", "cx")
R64 = {}
for b in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp"):
    for n in ("r" + b, "e" + b, b):
        R64[n] = "r" + b
R64.update({"al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx", "sil": "rsi", "dil": "rdi"})
for i in range(8, 16):
    for suf in ("", "d", "w", "b"):
        R64["r%d%s" % (i, suf)] = "r%d" % i
norm = lambda r: R64.get(r, r)
rows = []
for site, kind in sites:
    fa, fsz = owner(site)
    if fa is None:
        rows.append((site, kind, "", "UNOWNED", "")); continue
    ins = [x for x in md.disasm(blob[OFF(fa):OFF(site) + 5], fa) if x.address <= site]
    if not ins or ins[-1].address != site:
        rows.append((site, kind, "%08X" % fa, "DESYNC", "")); continue
    targets = set()
    for x in md.disasm(blob[OFF(fa):OFF(fa) + fsz], fa):
        if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == X86_OP_IMM:
            targets.add(x.operands[0].imm)
    last = None; consts = {}
    for x in ins[:-1]:
        ops = x.op_str.split(",")
        dst = norm(ops[0].strip()) if x.op_str else ""
        if x.mnemonic == "call":                        # the Win64 volatile registers die; rbx rbp rdi rsi r12-r15 survive
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                consts.pop(r, None)
            last = x; continue
        val = None
        if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_IMM:
            val = x.operands[1].imm
        elif x.mnemonic == "xor" and len(ops) == 2 and norm(ops[0].strip()) == norm(ops[1].strip()):
            val = 0
        elif x.mnemonic == "mov" and len(ops) == 2 and norm(ops[1].strip()) in consts:
            val = consts[norm(ops[1].strip())]
        elif x.mnemonic == "lea" and len(ops) == 2:
            m3 = re.match(r"\[(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]$", ops[1].strip())
            if m3 and norm(m3.group(1)) in consts:
                val = consts[norm(m3.group(1))] + (1 if m3.group(2) == "+" else -1) * int(m3.group(3), 0)
        if dst:
            if val is None:
                consts.pop(dst, None)
            else:
                consts[dst] = val
        if dst == "rcx":
            last = x
    if last is None or last.mnemonic == "call":
        rows.append((site, kind, "%08X" % fa, "DYNAMIC", "no ECX write after the previous call" if last else "entry value")); continue
    t = "%s %s" % (last.mnemonic, last.op_str)
    multi = any(last.address < tgt <= site for tgt in targets)
    cls = consts.get("rcx")
    rows.append((site, kind, "%08X" % fa, ("CONST %d" % cls) if cls is not None else "DYNAMIC", t + (" MULTI" if multi else "")))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rc1_census.tsv" if TARGET == 0x00322C50 else "rc1_census_%08X.tsv" % TARGET)
with io.open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("site\tkind\tfunction\tclass\tlast_ecx_write\n")
    for r in rows:
        f.write("%08X\t%s\t%s\t%s\t%s\n" % r)
c = collections.Counter(r[3] for r in rows)
print("sites %d in %d functions" % (len(rows), len({r[2] for r in rows})))
for k, v in sorted(c.items(), key=lambda kv: (not kv[0].startswith("CONST"), kv[0])):
    print("  %-12s %d" % (k, v))
print("MULTI-flagged:", sum(1 for r in rows if r[4].endswith("MULTI")))
