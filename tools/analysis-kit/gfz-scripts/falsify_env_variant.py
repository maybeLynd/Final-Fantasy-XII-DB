"""Falsification pass 1 on CONTRACT-field-environment-variant (OPUS, 2026-09-29), from the shipping image. Killers first.

  V0  section 2 / EV-1: 0026D910 is 418 B and 111 instructions, ends `jmp 0x2e3d40` at 0026DAAD after zeroing rcx/rdx/r8/r9
  V1  EV-2: count - 1, negative -> 0, `cmovg` to 2
  V2  EV-3: the latch test at 0026D951 (+0x1061 == 0) guards the selector write at 0026D95E (+0x1060); 0026DA92 clears +0x1061
  V3  EV-5: `cmp ecx, 4 / setge al / inc eax` into 02099DAC, and 0 when 00377850 returns 0
  V4  EV-6: 02099DBC is written at 0026D946 before any lookup; the skip branches are 0026D9C6 and 0026D9D3
  V5  (resolves EV-6's open note) the body writes exactly six global cells: four rip-relative (02099DA8, 02099DAC, 02099DB0,
      02099DBC) and two through 002EF2B0, which returns the constant 02164280 + 0x200 - so +0x1060 is the selector byte 021654E0
      and +0x1061 the latch 021654E1. The page's five published globals are the four plus the selector
"""
import io, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
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


S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
dis = lambda fa, n: list(md.disasm(blob[OFF(fa):OFF(fa) + n], fa))
b = dis(0x0026D910, 418)
I = {x.address: x for x in b}
at = lambda va: S(I[va]) if va in I else "?"
run = lambda lo, hi: [S(I[a]) for a in sorted(I) if lo <= a <= hi]

check("V0", len(b) == 111 and b[-1].address == 0x0026DAAD and at(0x0026DAAD) == "jmp 0x2e3d40"
      and run(0x0026DA88, 0x0026DA90) == ["xor r9d, r9d", "xor r8d, r8d", "xor edx, edx", "xor ecx, ecx"], "%d instructions; tail jmp with (0, 0, 0, 0)" % len(b))
check("V1", run(0x0026D933, 0x0026D943) == ["sub edi, 1", "jns 0x26d93c", "mov edi, ebx", "jmp 0x26d946", "mov eax, 2", "cmp edi, eax", "cmovg edi, eax"], "clamp(count - 1, 0, 2)")
check("V2", run(0x0026D951, 0x0026D95E) == ["cmp byte ptr [rax + 0x1061], bl", "jne 0x26d965", "call 0x2ef2b0", "mov byte ptr [rax + 0x1060], dil"]
      and at(0x0026DA92) == "mov byte ptr [rax + 0x1061], 0", "first writer wins; released at 0026DA92")
check("V3", run(0x0026DA38, 0x0026DA4E)[-4:] == ["mov eax, ebx", "setge al", "inc eax", "mov dword ptr [rip + 0x1e2c358], eax"]
      and at(0x0026DA44) == "cmp ecx, 4" and rip(I[0x0026DA3C]) == [0x02099DAC], "0, or (result >= 4) + 1")
check("V4", rip(I[0x0026D946]) == [0x02099DBC] and at(0x0026D9C6) == "je 0x26da83" and at(0x0026D9D3) == "je 0x26da83", "pre-zero before the lookups")
wr = sorted({"%08X" % t for x in b if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov") for t in rip(x)})
g = dis(0x002EF2B0, 16)[:3]; h = dis(0x002EF640, 8)[:2]
ctx = rip(h[0])[0] + 0x200 if S(h[0]).startswith("lea rax") and S(g[2]) == "add rax, 0x200" and S(g[1]) == "call 0x2ef640" else None
reg = sorted({(x.operands[0].mem.disp) for x in b if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base not in (0, X86_REG_RIP)
              and x.reg_name(x.operands[0].mem.base) == "rax" and x.mnemonic == "mov"})
check("V5", wr == ["02099DA8", "02099DAC", "02099DB0", "02099DBC"] and ctx == 0x02164480 and reg == [0x1060, 0x1061],
      "rip writes %s; ctx = 002EF2B0() = %08X; register writes at +%s -> %s" % (wr, ctx or 0, [hex(r) for r in reg], ["%08X" % ((ctx or 0) + r) for r in reg]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
