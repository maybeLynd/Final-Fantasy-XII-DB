"""Falsification pass 1 on CONTRACT-the-moment-an-action-is-committed (OPUS, 2026-09-29), from the shipping image.

  M1  CM-1: the target resolves through 0031B7E0 (0030F791) and a null result does not return
  M2  CM-2: `mov r13d, 0x21e` / `cmp di, r13w` / `ja`; above it `sub ax, cx` (0x4000) and `cmp ax, cx` (0x166) / `ja` refuse
  M3  CM-3 / CM-4: the low range resets +0x778 (00316CF0) and appends (00316CD0) with rdx = [r15 + 0x10] or the zeroed rsi; the
      high range jumps to the command block at 0030F7F2
  M4  CM-5 and section 3: `and dword ptr [rbx + 0x700], 0xfffffffc`, the three fields, +0x6B4 = 0, then +0x700..+0x70F movups to
      +0x718 and +0x710..+0x717 movsd to +0x728; the commit never reads +0x718..+0x72F back
  M5  CM-5 "the cancel is what consumes it": 003105D0 reads +0x718..+0x72F
  M6  CM-6: 003105D0 returns at once on a null unit or a null +0x698
"""
import io, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

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
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in (0x0030F760, 0x003105D0)}
run = lambda fa, lo, hi: [S(x) for x in B[fa] if lo <= x.address <= hi]
C = 0x0030F760

check("M1", run(C, 0x0030F791, 0x0030F79E) == ["call 0x31b7e0", "xor esi, esi", "mov r13d, 0x21e", "mov r15, rax"],
      "resolve at 0030F791; its result kept in r15, with no test that returns")
check("M2", run(C, 0x0030F7A1, 0x0030F7A5) == ["cmp di, r13w", "ja 0x30f7d9"]
      and run(C, 0x0030F7D9, 0x0030F7EC) == ["mov ecx, 0x4000", "movzx eax, di", "sub ax, cx", "mov ecx, 0x166", "cmp ax, cx", "ja 0x30f981"],
      "<= 0x21E, or id - 0x4000 <= 0x166 as 16-bit arithmetic")
check("M3", run(C, 0x0030F7A7, 0x0030F7D7) == ["lea rcx, [rbx + 0x778]", "mov qword ptr [rsp + 0x50], r14", "call 0x316cf0", "test r15, r15", "je 0x30f7c3",
                                                "mov rdx, qword ptr [r15 + 0x10]", "jmp 0x30f7c6", "mov rdx, rsi", "lea rcx, [rbx + 0x778]", "call 0x316cd0",
                                                "mov r14, qword ptr [rsp + 0x50]", "jmp 0x30f7f2"],
      "low range: reset +0x778, append [r15+0x10] or 0; both then reach 0030F7F2")
m4 = run(C, 0x0030F7F2, 0x0030F82A)
rd = [S(x) for x in B[C] if any(o.type == X86_OP_MEM and 0x718 <= o.mem.disp <= 0x72F for o in x.operands[1:])]
check("M4", m4 == ["and dword ptr [rbx + 0x700], 0xfffffffc", "mov qword ptr [rbx + 0x708], r12", "mov dword ptr [rbx + 0x710], ebp", "mov word ptr [rbx + 0x714], di",
                   "movups xmm0, xmmword ptr [rbx + 0x700]", "mov byte ptr [rbx + 0x6b4], sil", "movsd xmm1, qword ptr [rbx + 0x710]",
                   "movups xmmword ptr [rbx + 0x718], xmm0", "movsd qword ptr [rbx + 0x728], xmm1"] and not rd,
      "flags & ~3, three fields, phase 0, shadow copy; the commit reads the shadow: %s" % (rd or "never"))
cr = [S(x) for x in B[0x003105D0] if any(o.type == X86_OP_MEM and 0x718 <= o.mem.disp <= 0x72F for o in x.operands[1:])]
check("M5", bool(cr), "003105D0 reads the shadow: %s" % cr[:4])
check("M6", run(0x003105D0, 0x003105D0, 0x003105E9) == ["test rcx, rcx", "je 0x310771", "push rbx", "sub rsp, 0x20", "cmp qword ptr [rcx + 0x698], 0",
                                                         "mov rbx, rcx", "je 0x31076c"], "null unit and null +0x698 both exit before any write")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
