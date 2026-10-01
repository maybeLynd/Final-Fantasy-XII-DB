"""Falsification pass 1 on CONTRACT-enmity (OPUS, 2026-09-29), from the shipping image. Killers first.

  Y0  section 2: sizes 141 / 381 / 296 / 551 / 142
  Y1  E-1: the decay reads byte [rdi] (0032158F); the write reads table[id + 1] (00321906)
  Y2  E-3: the generate gate reads caster stats byte +5 (0032170D); decay, propagate and write gate on a class byte at their sites
  Y3  E-4: 003216E0 calls 00321850, 003219D0 and 00321B00, and negates the third parameter
  Y4  E-6: 00321576 calls the engagement test; 0032159F `lea edx, [rsi - 0xa]`; 003215A5 calls the write-all 00321D30
  Y5  E-7: [01DFE0B8] x [008F8D80] where [008F8D80] = 30.0
  Y6  E-8: `0x80000003` at 003218AC, a call at 003218B3, and 00322C50 at 003218F9
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

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
E = [0x003216E0, 0x00321850, 0x003219D0, 0x00321B00, 0x00321530]
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in E}
allins = {x.address: x for b in B.values() for x in b}
at = lambda va: S(allins[va]) if va in allins else "?"

check("Y0", [sizes[f] for f in E] == [141, 381, 296, 551, 142], "%s" % [sizes[f] for f in E])
check("Y1", at(0x0032158F) == "movzx ecx, byte ptr [rdi]" and at(0x00321906) == "movzx esi, byte ptr [r14 + rbp + 1]", "%s / %s" % (at(0x0032158F), at(0x00321906)))
check("Y2", at(0x0032170D) == "movzx eax, byte ptr [r9 + 5]" and all(at(a) != "?" for a in (0x0032154D, 0x00321A33, 0x003218D0)),
      "generate %s; decay %s; propagate %s; write %s" % (at(0x0032170D), at(0x0032154D), at(0x00321A33), at(0x003218D0)))
g = [S(x) for x in B[0x003216E0]]
check("Y3", at(0x0032172E) == "call 0x321850" and at(0x0032173F) == "call 0x3219d0" and at(0x00321753) == "call 0x321b00"
      and any(s.startswith("neg") for s in g), "three calls; negation %s" % [s for s in g if s.startswith("neg")])
check("Y4", at(0x00321576).startswith("call") and at(0x0032159F) == "lea edx, [rsi - 0xa]" and at(0x003215A5) == "call 0x321d30",
      "%s; %s; %s" % (at(0x00321576), at(0x0032159F), at(0x003215A5)))
m1 = rip(allins[0x0032157F]); m2 = rip(allins[0x00321587])
f30 = struct.unpack("<f", blob[OFF(m2[0]):OFF(m2[0]) + 4])[0] if m2 else None
check("Y5", m1 == [0x01DFE0B8] and m2 == [0x008F8D80] and f30 == 30.0, "%s x %s = 30.0? %s" % (["%08X" % v for v in m1], ["%08X" % v for v in m2], f30))
check("Y6", "0x80000003" in at(0x003218AC) and at(0x003218B3).startswith("call") and at(0x003218F9) == "call 0x322c50",
      "%s; %s; %s" % (at(0x003218AC), at(0x003218B3), at(0x003218F9)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
