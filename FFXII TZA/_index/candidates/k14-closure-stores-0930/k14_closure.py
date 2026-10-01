"""k14_closure.py - K-14's residue, static (OPUS, 2026-09-30): can a body reached from Movement_UpdateSteeringTowardTarget
002E45E0 store into byte +3 of any record?  The direct-call closure (rel32 E8 calls and E9 tail jumps inside each body's
functions.tsv extent, followed transitively, extents chained through .pdata fragments by functions.tsv as published) is
decoded, and every store whose destination is [reg + d] with a width covering offset 3 of that base (byte +3, word
+2..+3, dword +0..+3, qword +0..+3, xmm +0..+3, and rep stos/movs, and calls to memset/memcpy) is listed. Indirect calls
are listed separately - they are the closure's blind spot. Output k14_closure.tsv + summary."""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
TEXT = [s for s in SECS if s[0] == ".text"][0]


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("%08X" % va)


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
MEMFN = {0x00861EC0: "memset", 0x004746F0: "memcpy-adapter"}
ROOTFN = 0x002E45E0
seen, order, indirect, stores, unknown = set(), [], [], [], []
todo = [ROOTFN]
while todo:
    f = todo.pop()
    if f in seen:
        continue
    seen.add(f); order.append(f)
    if f not in sizes:
        unknown.append(f); continue
    lo, hi = f, f + sizes[f]
    for x in md.disasm(blob[OFF(lo):OFF(hi)], lo):
        if x.mnemonic in ("call", "jmp") and x.operands:
            op = x.operands[0]
            if op.type == X86_OP_IMM:
                t = op.imm
                if x.mnemonic == "jmp" and lo <= t < hi:
                    continue                                   # a jump inside the body
                if t in MEMFN:
                    stores.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str), MEMFN[t]))
                elif TEXT[1] <= t < TEXT[1] + TEXT[2]:
                    todo.append(t)
            elif x.mnemonic == "call" or op.type == X86_OP_MEM:
                indirect.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
            continue
        if x.mnemonic.startswith(("rep stos", "rep movs", "stos", "movs")) and not x.mnemonic.startswith(("movsx", "movss", "movsd", "movsb ")) :
            if x.mnemonic.startswith(("rep", "stos")) or x.mnemonic in ("movsb", "movsw", "movsd", "movsq"):
                stores.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str), "string op"))
            continue
        if len(x.operands) >= 1 and x.operands[0].type == X86_OP_MEM and x.mnemonic not in ("cmp", "test", "push", "prefetch", "prefetchw", "bt"):
            m = x.operands[0].mem
            if m.base in (0,) or x.reg_name(m.base) in ("rip", "rsp", "rbp") and x.reg_name(m.base) != "rbp":
                continue
            w = x.operands[0].size
            d = m.disp
            if m.index == 0 and d <= 3 < d + w:
                stores.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str), "width %d at +%d" % (w, d)))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k14_closure.tsv")
with io.open(out, "w", encoding="utf-8", newline="\n") as fo:
    fo.write("kind\tfunction\taddress\tinstruction\tnote\n")
    for f, a, t, n in stores:
        fo.write("store\t%08X\t%08X\t%s\t%s\n" % (f, a, t, n))
    for f, a, t in indirect:
        fo.write("indirect\t%08X\t%08X\t%s\t\n" % (f, a, t))
print("closure: %d bodies (%d without a functions.tsv extent)" % (len(order), len(unknown)))
print("stores that can cover +3: %d in %d bodies" % (len(stores), len({s[0] for s in stores})))
print("indirect calls/jumps: %d in %d bodies" % (len(indirect), len({s[0] for s in indirect})))
for s in stores[:40]:
    print("  %08X %08X %-48s %s" % s)
