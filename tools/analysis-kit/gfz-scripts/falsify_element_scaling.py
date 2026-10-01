"""Falsification pass 1 on CONTRACT-environmental-element-scaling (OPUS, 2026-09-29), from the shipping image. Killers first.

  X0  section 2: sizes 1,138 / 7 / 7 / 53
  X1  WE-3: 00263E10 reads 02099DA8 and 00263E20 reads 02099DAC, each then returns
  X2  WE-1: the element mask is read at 0038B295 from +0x13
  X3  WE-4: 0038B226 `test byte ptr [rdx + 0x6a], 1`, 0038B233 `test byte ptr [rdx + 0x7a], 1`, 0038B23D `test byte ptr [r8 + 0x1c], 1`
  X4  the rule table: the thunks 00321490 / 003214A0 are single jumps to the two class getters, and 003210E0 first loads the unit's
      +0x10 then jumps to 00263DD0; the stage loads [01CEBB70] = 0.5 and [008FCC90] = 1.2 into xmm6 and multiplies 02AEE054 by it, and stores to 02EBF188 at five sites
"""
import io, os, struct
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


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
dis = lambda fa, n=None: list(md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa))
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
ST = 0x0038B220
b = dis(ST)
at = lambda va: next((S(x) for x in b if x.address == va), "?")

check("X0", [sizes.get(f) for f in (ST, 0x00263E10, 0x00263E20, 0x00263DD0)] == [1138, 7, 7, 53], "%s" % [sizes.get(f) for f in (ST, 0x00263E10, 0x00263E20, 0x00263DD0)])
g1, g2 = dis(0x00263E10), dis(0x00263E20)
check("X1", rip(g1[0]) == [0x02099DA8] and S(g1[1]).startswith("ret") and rip(g2[0]) == [0x02099DAC] and S(g2[1]).startswith("ret"),
      "%s / %s" % ([S(x) for x in g1], [S(x) for x in g2]))
check("X2", "+ 0x13]" in at(0x0038B295), at(0x0038B295))
check("X3", at(0x0038B226) == "test byte ptr [rdx + 0x6a], 1" and at(0x0038B233) == "test byte ptr [rdx + 0x7a], 1" and at(0x0038B23D) == "test byte ptr [r8 + 0x1c], 1",
      "%s / %s / %s" % (at(0x0038B226), at(0x0038B233), at(0x0038B23D)))
th = {t: [S(x) for x in dis(t, 12)[:2]] for t in (0x00321490, 0x003214A0, 0x003210E0)}
loads = sorted({"%08X" % a for x in b if x.mnemonic == "movss" and x.op_str.startswith("xmm6,") for a in rip(x)})
scale = [x for x in b if 0x02AEE054 in rip(x)]
st188 = [x for x in b if x.operands and x.operands[0].type == X86_OP_MEM and 0x02EBF188 in rip(x)]
check("X4", th[0x00321490] == ["jmp 0x263e10"] + th[0x00321490][1:2] and th[0x003214A0][0] == "jmp 0x263e20"
      and th[0x003210E0] == ["mov rcx, qword ptr [rcx + 0x10]", "jmp 0x263dd0"]
      and loads == ["008FCC90", "01CEBB70"] and f32(0x01CEBB70) == 0.5 and abs(f32(0x008FCC90) - 1.2) < 1e-6
      and len(scale) % 2 == 0 and len(scale) >= 10 and len(st188) == 5,
      "thunks %s; xmm6 loads %s (0.5, 1.2); %d scale loads+stores of 02AEE054; 02EBF188 stores %d"
      % ({"%08X" % k: v for k, v in th.items()}, loads, len(scale), len(st188)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
