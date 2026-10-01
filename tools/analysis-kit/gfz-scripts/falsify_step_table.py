"""Falsification pass 1 on CONTRACT-formula-step-table (OPUS, 2026-09-29), from the shipping image. Killers first.

  F0  ST-1: walking 01EFA5C0 until the first qword that is not a .text pointer stops at exactly 202, none null; slot 202 is
      3F80000000060303
  F1  ST-2 / ST-3: 152 distinct targets; 42 slots point at 0016D6A0; exactly seven targets carry more than one id, with the
      page's ids
  F2  ST-3: 0016D6A0 is `ret 0` (c2 00 00)
  F3  ST-4: the preparation band (ids 60..79) writes the scratch cells 02AEE054 / 58 / 5C, and the finalize 0038D280 reads them
  F4  ST-7: every step target whose name contains "Roll" calls a generator entry (00379CD0 gameplay MT, 00328370 shared LCG)
"""
import collections, io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
body = lambda fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) if fa in sizes else []
TB = 0x01EFA5C0

# F0
slots = []
while True:
    v = q(TB + 8 * len(slots))
    if not (text[1] <= v < text[1] + text[2]):
        break
    slots.append(v)
check("F0", len(slots) == 202 and 0 not in slots and q(TB + 8 * 202) == 0x3F80000000060303, "%d slots; slot 202 = %016X" % (len(slots), q(TB + 8 * 202)))
# F1
c = collections.Counter(slots)
multi = {"%08X" % t: [i for i, v in enumerate(slots) if v == t] for t, n in c.items() if n > 1 and t != 0x0016D6A0}
want = {"00389670": [40, 45, 46], "0038AA90": [61, 64, 75], "00388FE0": [23, 24], "00389F80": [60, 63], "0038AAF0": [65, 76],
        "0038D280": [113, 125], "0038F5A0": [115, 160]}
check("F1", len(c) == 152 and c[0x0016D6A0] == 42 and multi == want, "%d targets; %d no-ops; multi-id %s" % (len(c), c[0x0016D6A0], multi))
# F2
check("F2", blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3] == b"\xc2\x00\x00", "0016D6A0 bytes %s" % blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3].hex())
# F3
SCR = {0x02AEE054, 0x02AEE058, 0x02AEE05C}
def w(fa):
    return {t for x in body(fa) if x.operands and x.operands[0].type == X86_OP_MEM for t in rip(x) if t in SCR and x.mnemonic.startswith(("mov", "add", "sub", "imul", "or", "and"))}
band = sorted({slots[i] for i in range(60, 80)} - {0x0016D6A0})
writers = [("%08X" % f) for f in band if w(f)]
fin = {t for x in body(0x0038D280) for t in rip(x) if t in SCR}
check("F3", len(writers) >= 1 and fin == SCR, "band writers of the scratch: %d of %d distinct targets %s; the finalize reads %s"
      % (len(writers), len(band), writers[:6], sorted("%08X" % t for t in fin)))
# F4
rolls = sorted({t for t in c if "roll" in names.get(t, "").lower()})
def draws(fa, depth=2):
    seen, st = set(), [(fa, 0)]
    while st:
        f, d = st.pop()
        if f in seen or d > depth:
            continue
        seen.add(f)
        for x in body(f):
            t = T(x) if x.mnemonic in ("call", "jmp") else None
            if t in (0x00379CD0, 0x00328370, 0x00863BF0):
                return True
            if t is not None:
                st.append((t, d + 1))
    return False
nod = [names[r] for r in rolls if not draws(r)]
check("F4", rolls and not nod, "%d Roll* steps; without a generator call within two levels: %s" % (len(rolls), nod or "none"))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
