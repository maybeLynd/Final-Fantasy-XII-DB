"""Falsification pass 1 on CONTRACT-combo-continuation (OPUS, 2026-09-29), from the shipping image. Killers first.

  C0  section 2: sizes 602 / 146 / 418
  C1  CB-1, image-wide by access width: +0x6B7 has seven accesses, exactly one word-wide (003106EB); +0x6B8 has 64 accesses,
      four of them byte-wide
  C2  CB-2 / CB-6: 0030FA00 saves +0x6B7 / +0x6B8 (0030FA0F, 0030FA19), commits with fifth argument 1 (0030FA54), increments on
      success (0030FA6C `inc dil`) and writes back only on success (0030FA65, 0030FA79)
  C3  CB-3: 00388660 draws at two call sites (003886FD, 003887E3), the second inside an 11-iteration loop (`0xb`), and stores the
      count in the high nibble of record+0x12 (`and ..., 0xf` then `or ..., r14b`)
  C4  CB-4: the continue test reloads record+0x12, `shr eax, 4`, `cmp ebx, eax`, `jae`
  C5  CB-5: the party records at 0208D480 and the foe records at 0208DE80, both 0x40 apart
"""
import collections, io, os
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
text = next(x for x in SECS if x[0] == ".text")
acc = collections.defaultdict(list)       # displacement -> [(address, size)]
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    if fa in (0x00388660, 0x0030FA00, 0x003105D0):
        bodies[fa] = ins
    for x in ins:
        for o in x.operands:
            if o.type == X86_OP_MEM and o.mem.base not in (0, X86_REG_RIP) and o.mem.disp in (0x6B7, 0x6B8):
                acc[o.mem.disp].append((x.address, o.size))
at = lambda fa, va: next(S(x) for x in bodies[fa] if x.address == va)

# C0
check("C0", [sizes[f] for f in (0x00388660, 0x0030FA00, 0x003105D0)] == [602, 146, 418], "%s" % [sizes[f] for f in (0x00388660, 0x0030FA00, 0x003105D0)])
# C1
a7, a8 = acc[0x6B7], acc[0x6B8]
w7 = [("%08X" % a) for a, s in a7 if s == 2]
check("C1", len(a7) == 7 and w7 == ["003106EB"] and all(s == 1 for a, s in a7 if s != 2) and len(a8) == 64 and sum(1 for _a, s in a8 if s == 1) == 4,
      "+0x6B7: %d accesses, word-wide at %s; +0x6B8: %d accesses, %d byte-wide" % (len(a7), w7, len(a8), sum(1 for _a, s in a8 if s == 1)))
# C2
b = bodies[0x0030FA00]
check("C2", "0x6b7]" in at(0x0030FA00, 0x0030FA0F) and "0x6b8]" in at(0x0030FA00, 0x0030FA19) and at(0x0030FA00, 0x0030FA6C) == "inc dil"
      and "0x6b8]" in at(0x0030FA00, 0x0030FA65) and "0x6b7]" in at(0x0030FA00, 0x0030FA79) and "1" in at(0x0030FA00, 0x0030FA54),
      "save %s / %s; commit arg %s; inc; restore %s / %s" % (at(0x0030FA00, 0x0030FA0F), at(0x0030FA00, 0x0030FA19), at(0x0030FA00, 0x0030FA54),
                                                              at(0x0030FA00, 0x0030FA65), at(0x0030FA00, 0x0030FA79)))
# C3
r = bodies[0x00388660]
calls = [x.address for x in r if x.mnemonic == "call"]
rs = [S(x) for x in r]
check("C3", 0x003886FD in calls and 0x003887E3 in calls and at(0x00388660, 0x003886FD) == at(0x00388660, 0x003887E3)
      and any(s.endswith(", 0xb") for s in rs) and "and" in at(0x00388660, 0x0038885D) and at(0x00388660, 0x00388865).startswith("or"),
      "draw sites %s / %s; loop bound 0xB; nibble store %s / %s" % (at(0x00388660, 0x003886FD), at(0x00388660, 0x003887E3), at(0x00388660, 0x0038885D), at(0x00388660, 0x00388865)))
# C4
check("C4", at(0x00388660, 0x0038886F) == "shr eax, 4" and at(0x00388660, 0x00388872) == "cmp ebx, eax" and at(0x00388660, 0x00388874).startswith("jae")
      and "0x12]" in at(0x00388660, 0x0038886B), "%s / shr 4 / cmp / jae" % at(0x00388660, 0x0038886B))
# C5
tabs = sorted({t for x in r for t in rip(x)} & {0x0208D480, 0x0208DE80})
check("C5", tabs == [0x0208D480, 0x0208DE80], "record tables %s" % ["%08X" % t for t in tabs])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
