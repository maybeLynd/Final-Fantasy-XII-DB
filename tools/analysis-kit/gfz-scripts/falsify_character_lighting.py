"""Falsification pass 1 on how-a-character-is-lit (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  G0  sizes: 003ACC10 2,342, 003ABD50 950, 003ACAA0 358, 003AB960 506, 003ABD00 26, 003ACA80 7, 003ACA90 9, 003AD540 745,
      003AE0E0 991, 003AC110 1,876
  G1  section 2 / 5a: 003AB960 walks the pool [02B3F528] in 0x70-byte steps bounded by 0x80, makes the handle [02B3F504] << 8 | index,
      copies five 16-byte blocks (0x50 bytes) to entry + 0x20, stores 1 / range^2 at entry + 0x50 (request + 0x30), and links the
      entry at the list whose head is 02B3F508 and tail 02B3F510
  G2  section 3: 003ACA80 is `or byte ptr [02B3F501], cl; ret` (7 B) and 003ACA90 `not cl; and byte ptr [02B3F501], cl; ret` (9 B);
      the selector reads both filter bytes 02B3F501 and 02B3F520
  G3  section 3: the selector reads the record's ambient mode +0x5E0, factor +0x5DC and colour +0x5D0, the scale gate 02B3F503 and
      scale 02B3F51C, and the camera position 02AEDF20
  G4  section 4: 003ACAA0 reads the enable byte 02B3F502 and the scale 02B3F518, and compares the light's +5 against 0x80
  G5  section 5b: 003AC110 stores 1.0 (0x3F800000) to 02B3F518 before its list walk; the only earlier call is the memset of its
      output block
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}

SZ = {0x003ACC10: 2342, 0x003ABD50: 950, 0x003ACAA0: 358, 0x003AB960: 506, 0x003ABD00: 26, 0x003ACA80: 7, 0x003ACA90: 9,
      0x003AD540: 745, 0x003AE0E0: 991, 0x003AC110: 1876}
check("G0", all(sizes.get(a) == n for a, n in SZ.items()), "%s" % {("%08X" % a): sizes.get(a) for a in SZ})
C = {x.address: S(x) for x in body(0x003AB960)}
copies = [C[a] for a in sorted(C) if C[a].startswith("movups xmmword ptr [rdx + 0x")]
check("G1", 0x02B3F528 in rips(0x003AB960) and C.get(0x003AB978) == "add rdx, 0x70" and C.get(0x003AB97C) == "cmp r8d, 0x80"
      and C.get(0x003AB9AB) == "shl eax, 8" and C.get(0x003AB9AE) == "or eax, r8d" and 0x02B3F504 in rips(0x003AB960)
      and copies == ["movups xmmword ptr [rdx + 0x%x], xmm%d" % (0x20 + 16 * k, k % 2) for k in range(5)]
      and C.get(0x003ABA1A) == "movss dword ptr [rdx + 0x50], xmm0" and {0x02B3F508, 0x02B3F510} <= rips(0x003AB960),
      "pool 0x70 x 0x80, handle << 8 | index, 0x50-byte copy to +0x20, 1/range^2 at +0x50, list 02B3F508 / 02B3F510")
check("G2", txt(0x003ACA80) == ["or byte ptr [rip + 0x2792a7b], cl", "ret"] and txt(0x003ACA90) == ["not cl", "and byte ptr [rip + 0x2792a69], cl", "ret"]
      and {0x02B3F501, 0x02B3F520} <= rips(0x003ACC10), "setter / clearer on 02B3F501; the selector reads 02B3F501 and 02B3F520")
T = txt(0x003ACC10)
check("G3", all(any("+ 0x%x]" % d in s for s in T) for d in (0x5E0, 0x5DC, 0x5D0)) and {0x02B3F503, 0x02B3F51C, 0x02AEDF20} <= rips(0x003ACC10),
      "ambient mode +0x5E0, +0x5DC, +0x5D0; 02B3F503 / 02B3F51C; camera 02AEDF20")
A = txt(0x003ACAA0)
check("G4", {0x02B3F502, 0x02B3F518} <= rips(0x003ACAA0) and any(s.startswith("cmp") and "0x80" in s for s in A),
      "enable 02B3F502, scale 02B3F518, the +5 < 0x80 test")
N = body(0x003AC110)
w18 = [(x.address, S(x)) for x in N if 0x02B3F518 in rip(x) and x.operands[0].type == X86_OP_MEM]
calls_before = [(x.address, S(x)) for x in N if x.mnemonic == "call" and x.address < (w18[0][0] if w18 else 0)]
walk = next(x.address for x in N if S(x) == "test r10, r10")
check("G5", w18 and w18[0][1].endswith("0x3f800000") and w18[0][0] < walk and calls_before == [(0x003AC190, "call 0x861ec0")],
      "1.0 stored to 02B3F518 at %08X, before the list walk at %08X; the only earlier call is the output memset %s" % (w18[0][0], walk, calls_before))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
