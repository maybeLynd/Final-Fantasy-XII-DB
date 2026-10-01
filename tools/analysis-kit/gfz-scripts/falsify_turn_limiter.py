"""Falsification pass 1 on CONTRACT-battle-locomotion-turn-limiter (OPUS, 2026-09-29), from the shipping image. Killers first.

  T0  section 2: 003364D0 is 564 B
  T1  BL-1: the three compared constants are 45 deg (00336519 -> 00915614), 120 deg (0033654E -> 00915FE0) and 20 deg
      (00336625 -> 00D10AD8); the flag raise is `or dword ptr [rdx + 0x38], 8`
  T2  BL-2: with bit 3 clear (`test r9b, 8` at 0033652A) the current heading is returned unchanged
  T3  BL-3 / BL-4: the latch needs `and ecx, 0x1c / cmp cl, 0x1c` (00336572); the release is `and dword ptr [rdx + 0x3c],
      0xfffffffe` (00336645); the middle band only tests the latch (0033662E)
  T4  BL-5: the direction pair is written clear-then-set (003366CD..003366DB); it is also READ above 120 deg (0033659D,
      `and cl, 6`), stepping +rate or -rate in the stored direction without the wrap - which the contract's later section
      states, and section 5's read list omits
  T5  BL-6: when the result equals desired (`ucomiss xmm4, xmm6`) bit 3 of +0x38 and bit 0 of +0x3C are cleared (003366E6..EE)
  T6  section 5: every memory write goes to the flag block (rdx = ctx + 0x100) - none to the motion state
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
F = 0x003364D0
b = list(md.disasm(blob[OFF(F):OFF(F) + sizes[F]], F))
at = lambda va: next(x for x in b if x.address == va)
run = lambda lo, hi: [S(x) for x in b if lo <= x.address <= hi]
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
deg = lambda va: round(f32(rip(at(va))[0]) * 180 / 3.14159265, 3)

# T0
check("T0", sizes[F] == 564, "003364D0 %d B" % sizes[F])
# T1
check("T1", deg(0x00336519) == 45.0 and deg(0x0033654E) == 120.0 and deg(0x00336625) == 20.0 and S(at(0x00336522)) == "or dword ptr [rdx + 0x38], 8",
      "raise %s deg, latch %s deg, release %s deg" % (deg(0x00336519), deg(0x0033654E), deg(0x00336625)))
# T2
check("T2", run(0x00336526, 0x00336537) == ["mov r9d, dword ptr [rdx + 0x38]", "test r9b, 8", "jne 0x33654e", "mov rax, qword ptr [rcx + 0x108]",
                                            "movss xmm0, dword ptr [rax + 0xe0]"], "bit 3 clear -> the current heading, unchanged")
# T3
check("T3", run(0x00336572, 0x0033657A) == ["and ecx, 0x1c", "cmp cl, 0x1c", "jne 0x33657e", "or dword ptr [rdx + 0x3c], 1"]
      and S(at(0x00336645)) == "and dword ptr [rdx + 0x3c], 0xfffffffe" and S(at(0x0033662E)) == "test byte ptr [rdx + 0x3c], 1",
      "latch needs 0x1C; release below 20 deg; middle band only reads the latch")
# T4
check("T4", run(0x003366CD, 0x003366DB) == ["and byte ptr [rdx + 0x21], 0xfb", "or byte ptr [rdx + 0x21], 2", "jmp 0x3366df",
                                            "and byte ptr [rdx + 0x21], 0xfd", "or byte ptr [rdx + 0x21], 4"]
      and run(0x0033659D, 0x003365A4) == ["movzx ecx, byte ptr [rdx + 0x21]", "and cl, 6", "jne 0x3365ff"]
      and run(0x003365FF, 0x00336620) == ["cmp cl, 2", "jne 0x336611", "addss xmm4, dword ptr [rax + 0xe0]", "jmp 0x3366aa",
                                          "movss xmm0, dword ptr [rax + 0xe0]", "subss xmm0, xmm4", "movaps xmm4, xmm0", "jmp 0x3366aa"],
      "written clear-then-set; read above 120 deg to step +rate / -rate in the stored direction with no wrap call")
# T5
check("T5", run(0x003366DF, 0x003366EE) == ["ucomiss xmm4, xmm6", "jp 0x3366f2", "jne 0x3366f2", "and r9d, 0xfffffff7", "and dword ptr [rdx + 0x3c], 0xfffffffe",
                                            "mov dword ptr [rdx + 0x38], r9d"], "arrival clears bit 3 of +0x38 and bit 0 of +0x3C")
# T6
w = sorted({S(x).split(",")[0] for x in b if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "or", "and", "movss", "movaps")
            and "rsp" not in S(x).split(",")[0]})
check("T6", all("[rdx +" in s for s in w) and run(0x003364DE, 0x003364DE) == ["mov rdx, qword ptr [rcx + 0x100]"],
      "writes %s - all through rdx = ctx + 0x100" % w)
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
