"""Catalogue tails (OPUS, 2026-09-29): code that .pdata chains to a catalogue function but lies past the catalogue's end.
Lists the tail ranges and re-runs today's function-bounded counts over them (direct call/jmp targets, rip references)."""
import collections, struct, sys, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"); FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True); b = open(EXE, "rb").read(); B = pe.OPTIONAL_HEADER.ImageBase
def off(va):
    for s in pe.sections:
        st = B + s.VirtualAddress
        if st <= va < st + s.SizeOfRawData: return s.PointerToRawData + va - st
pd = [s for s in pe.sections if s.Name.startswith(b".pdata")][0]; raw = b[pd.PointerToRawData:pd.PointerToRawData + pd.SizeOfRawData]
pent = {}
for j in range(0, len(raw) - 11, 12):
    x, y, u = struct.unpack_from("<III", raw, j)
    if x: pent[B + x] = (B + y, B + u)
def nxt(bg):
    u = pent[bg][1]; h = b[off(u):off(u) + 4]
    if not (h[0] >> 3) & 4: return None
    c = off(u) + 4 + 2 * ((h[2] + 1) & ~1); return B + struct.unpack_from("<I", b, c)[0]
root = {}
for bg in pent:
    r, seen = bg, set()
    while r in pent and r not in seen:
        seen.add(r); n = nxt(r)
        if n is None: break
        r = n
    root[bg] = r
frags = collections.defaultdict(list)
for bg, r in root.items(): frags[r].append((bg, pent[bg][0]))
sizes = {}
for i, l in enumerate(open(FUNCS, encoding="utf-8", errors="replace")):
    p = l.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try: sizes[int(p[0], 16)] = int(p[2])
        except ValueError: pass
tails = []
for r, fs in frags.items():
    if len(fs) < 2 or r not in sizes: continue
    end = max(e for _, e in fs)
    if r + sizes[r] < end: tails.append((r, r + sizes[r], end))
tails.sort()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
TARGETS = [int(a, 16) for a in sys.argv[1:]]
hits = collections.defaultdict(list); ntail = 0
for r, a, e in tails:
    # decode from the fragment boundary that contains a, so instruction boundaries are the unwind's own
    st = max(bg for bg, _ in frags[r] if bg <= a)
    for x in md.disasm(b[off(st):off(e)], st):
        if x.address < a: continue
        ntail += 1
        t = x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM and (x.mnemonic == "call" or x.mnemonic.startswith("j")) else None
        refs = [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
        for tg in TARGETS:
            if t == tg or tg in refs: hits[tg].append("%08X in %08X" % (x.address, r))
print("tails %d, bytes %d, instructions decoded %d" % (len(tails), sum(e - a for _, a, e in tails), ntail))
for tg in TARGETS: print("%08X: %s" % (tg, hits[tg] or "none in the tails"))
