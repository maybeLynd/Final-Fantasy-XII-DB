"""Falsification pass 1 on the-bone-trails (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  B0  sizes: 0051C270 265, 0051CC30 385, 0051CC10 26, 0051BC10 93, 0051C3C0 2,128, 0051BC70 1,525, 00520160 23, 00425E70 202,
      003E6770 276, 00422170 121, 003711D0 232, 0046F460 75, 00202E10 115, 0042F250 70
  B1  section 3: 0051C270 allocates 0x3C00 bytes, stores the pool at 02CA8420 and zeroes 02CA8400 / 02CA8402 / 02CA8404 /
      02CA8408 / 02CA8410; it references the embedded image at 01F2A220
  B2  section 2: 00520160 stores command byte +2 into record +0x3D0 and ORs 0x1000000 (bit 24) into +0x294; 0051CC10 clears only the
      entry's byte +4; 003E6770 compares +0x438 with 0xFFFF and walks 0x50-byte descriptors capped at 4
  B3  section 4: 0051C3C0 ORs the entry's +5 with 02CA8402 and tests bit 0; reads the time base 01DFE0BC; 0046F460 indexes the
      table at 00D12590, whose first, middle and last floats are pi, pi/2 and 0
  B4  section 5 / 5a: 0051BC70 references the template 02CA8A90 and takes the address of 0053F490 once (at 0051C147); the phase-2
      pass jumps into it at 0041E4EF; 005409C0 writes VIF words with top bytes 0x03, 0x02, 0x01, 0x6C at 005409D6, 005409DF,
      005409E6, 005409ED and 0x10 at 00540B71
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
imms = lambda fa: {o.imm & 0xFFFFFFFF for x in body(fa) for o in x.operands if o.type == X86_OP_IMM}

SZ = {0x0051C270: 265, 0x0051CC30: 385, 0x0051CC10: 26, 0x0051BC10: 93, 0x0051C3C0: 2128, 0x0051BC70: 1525, 0x00520160: 23,
      0x00425E70: 202, 0x003E6770: 276, 0x00422170: 121, 0x003711D0: 232, 0x0046F460: 75, 0x00202E10: 115, 0x0042F250: 70}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("B0", not bad, "mismatches %s" % bad if bad else "all fourteen sizes as cited")
check("B1", 0x3C00 in imms(0x0051C270) and {0x02CA8420, 0x02CA8400, 0x02CA8402, 0x02CA8404, 0x02CA8408, 0x02CA8410, 0x01F2A220} <= rips(0x0051C270),
      "0x3C00 allocated; pool, header and image references present")
Cmd = txt(0x00520160); Off = txt(0x0051CC10); Bld = txt(0x003E6770)
check("B2", any("+ 0x3d0]" in s and s.startswith("mov byte") for s in Cmd) and any("+ 0x294]" in s and "0x1000000" in s for s in Cmd)
      and [s for s in Off if s.startswith("mov byte")] and all("+ 4]" in s for s in Off if s.startswith("mov byte"))
      and "lea rsi, [rbx + 0x438]" in Bld and "cmp dword ptr [rsi], 0xffff" in Bld and "lea rdi, [rdi + 0x50]" in Bld
      and "cmova eax, edi" in Bld and any(s == "mov edi, 4" for s in Bld),
      "command %s; switch-off %s; builder +0x438 / 0xFFFF / stride 0x50 / cap 4" % ([s for s in Cmd if "0x3d0" in s or "0x294" in s], [s for s in Off if s.startswith("mov byte")]))
tab = [struct.unpack("<f", blob[OFF(0x00D12590 + 4 * k):OFF(0x00D12590 + 4 * k) + 4])[0] for k in (0, 8192, 16383)]
check("B3", 0x02CA8402 in rips(0x0051C3C0) and 0x01DFE0BC in rips(0x0051C3C0) and 0x00D12590 in rips(0x0046F460)
      and abs(tab[0] - 3.14159) < 1e-3 and abs(tab[1] - 1.5708) < 1e-2 and abs(tab[2]) < 1e-3,
      "02CA8402 and 01DFE0BC read; arccos table first/middle/last %s" % [round(v, 4) for v in tab])
D = body(0x0051BC70)
mp = [x.address for x in D if 0x0053F490 in rip(x)]
into = [x.address for x in body(0x0041E4D0) if x.mnemonic in ("jmp", "call") and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x0051BC70] if 0x0041E4D0 in sizes else []
T = {x.address: x for x in body(0x005409C0)} if 0x005409C0 in sizes else {}
vif = {a: (T[a].operands[1].imm >> 24) & 0xFF for a in (0x005409D6, 0x005409DF, 0x005409E6, 0x005409ED, 0x00540B71) if a in T and len(T[a].operands) > 1 and T[a].operands[1].type == X86_OP_IMM}
check("B4", 0x02CA8A90 in rips(0x0051BC70) and mp == [0x0051C147] and into == [0x0041E4EF]
      and vif == {0x005409D6: 0x03, 0x005409DF: 0x02, 0x005409E6: 0x01, 0x005409ED: 0x6C, 0x00540B71: 0x10},
      "template 02CA8A90; microprogram address taken at %s; phase-2 edge %s; VIF top bytes %s" % (["%08X" % a for a in mp], ["%08X" % a for a in into], {("%08X" % a): hex(v) for a, v in vif.items()}))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
