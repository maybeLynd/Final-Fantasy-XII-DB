"""uq354_untextured.py - UQ-354: does the dead nine-patch renderer's 8..47 size band correspond to an art asset's corner
dimensions? (FABLE, Claude Opus 5.5, 2026-09-26)

It cannot: the renderer draws no art. Its batch opener 002DD1E0, which 00392A10 calls on the nine-slice path, writes
the one PS2 GIF tag the batch carries. That tag declares an UNTEXTURED primitive.
  U1 002DD294 movabs rcx, 0x8026400000000001: PRE 1, PRIM 0x4C = triangle strip, gouraud (IIP 1), alpha blend (ABE 1),
     TME 0 (no texture).
  U2 002DD2B2 stores the REGS word 0x41414141: RGBAQ (1) and XYZF2 (4) only, with no ST (2) and no UV (3), so the
     vertices carry colour and position and no texture coordinate.
  U3 00392A10 calls 002DD1E0, and the cell drawer 002DC7F0 holds no GIF tag constant of its own, so every cell is drawn
     under the opener's primitive.
  U4 control (sensitivity): the same decoder over the neighbouring UI code finds textured tags, TME 1, at 002DB98F,
     002DB99B and 002A05C1. A texture flag is visible to it when present.
So the band gates the four-colour blend for small corner cells of an untextured gradient box. What made the designer
pick 8 and 47 is intent, not an asset property.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
def body(a): return list(cs.disasm(d[off(a):off(a) + F[a]], a))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def tags(a):   # GIF tag constants: movabs with PRE set, packed/reglist FLG, a small NLOOP and zero reserved bits
    out = []
    for x in body(a):
        if x.mnemonic == "movabs" and x.operands[1].type == X86_OP_IMM:
            t = x.operands[1].imm & 0xFFFFFFFFFFFFFFFF
            if (t >> 46) & 1 and ((t >> 58) & 3) in (0, 1) and (t & 0x7FFF) <= 64 and ((t >> 16) & 0x3FFFFFFF) == 0:
                out.append((x.address, t))
    return out
prim = lambda t: (t >> 47) & 0x7FF
X = {x.address: x for x in body(0x2DD1E0)}
op = tags(0x2DD1E0)
p = prim(op[0][1]) if op else 0
check("U1 the opener's tag: PRIM 0x4C, triangle strip, gouraud, alpha blend, TME 0",
      op == [(0x2DD294, 0x8026400000000001)] and p & 7 == 4 and (p >> 3) & 1 and (p >> 6) & 1 and not (p >> 4) & 1,
      "%s PRIM %03X" % ([("%08X" % a, hex(t)) for a, t in op], p))
r = X.get(0x2DD2B2)
regs = r.operands[1].imm if r is not None and len(r.operands) == 2 and r.operands[1].type == X86_OP_IMM else None
nib = {(regs >> (4 * k)) & 0xF for k in range(8)} if regs is not None else set()
check("U2 REGS 0x41414141: RGBAQ and XYZF2 only, no ST or UV", regs == 0x41414141 and nib == {1, 4})
calls = [x.address for x in body(0x392A10) if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x2DD1E0]
check("U3 00392A10 calls the opener, and the cell drawer has no tag of its own", calls != [] and tags(0x2DC7F0) == [],
      "calls at %s" % ["%08X" % c for c in calls])
tex = []
for a in F:
    if 0x2A0000 <= a < 0x2E0000 and off(a) is not None:
        tex += [(s, t) for s, t in tags(a) if (prim(t) >> 4) & 1]
check("U4 control: the decoder finds textured tags (TME 1) in the neighbouring UI code",
      {0x2DB98F, 0x2DB99B, 0x2A05C1} <= {s for s, _ in tex}, "%d textured tags" % len(tex))
print("FAILS", fails)
sys.exit(1 if fails else 0)
