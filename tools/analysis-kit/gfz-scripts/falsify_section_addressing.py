"""Falsification pass 1 on CONTRACT-resource-section-addressing (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  X0  section 2: 101 / 89 / 41 / 86 B
  X1  RA-1: 00409C30 accepts tag 0 (00409C30/00409C32) and 0x4C4C4140 (00409C34/00409C3A) as wildcards and a NULL name (00409C40);
      the dword 0x4C4C4140 occurs as an instruction immediate once in .text (raw byte search, each hit decoded) - at 00409C34
  X2  RA-2: eight dword compares [rcx + 0x10 .. 0x2C] against [r8 + 0 .. 0x1C], 00409C48..00409C87
  X3  RA-3: 004096DF `add eax, ebx` / 004096E1 `cdqe`; 004096A4 `add eax, dword ptr [rsp + 0x40]` / 004096A8 `movsxd rbx, eax`
  X4  RA-4: 00409600 returns 0 for a mode other than 0 or 1 (0040961D/00409620 -> 0040960E), and neither resolver tests the base
      it gets back before adding the offset; the only explicit guards are the null entry and offset -1 (004096C8, 004096D5)
  X5  RA-5: mode 1 refreshes +0x38 through +0x30 only while byte 02B62E10 is non-zero (00409622), else returns +0x38; mode 0
      tail-jumps with rcx = entry + 0x10
  X6  RA-6: 004096D5 `cmp ebx, -1`; the pointer finder 00409660 reads the offset 00409780 writes and returns NULL (rbx = 0) when it
      is -1 (00409695/0040969A) - so -1 crosses as the offset output, and the pointer path turns it into NULL
"""
import io, os
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
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"

M, F, R, B = (body(a) for a in (0x00409C30, 0x00409660, 0x004096C0, 0x00409600))
check("X0", [sizes[a] for a in (0x00409C30, 0x00409660, 0x004096C0, 0x00409600)] == [101, 89, 41, 86], "%s" % [sizes[a] for a in (0x00409C30, 0x00409660, 0x004096C0, 0x00409600)])
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]
pat = (0x4C4C4140).to_bytes(4, "little")
sites = set()
k = raw.find(pat)
while k >= 0:
    pos = text[1] + k
    for L in range(1, 12):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and any(o.type == X86_OP_IMM and (o.imm & 0xFFFFFFFF) == 0x4C4C4140 for o in x.operands):
            sites.add(x.address); break
    k = raw.find(pat, k + 1)
check("X1", at(M, 0x00409C30) == "test edx, edx" and at(M, 0x00409C32) == "je 0x409c40" and at(M, 0x00409C34) == "cmp edx, 0x4c4c4140"
      and at(M, 0x00409C3A) == "je 0x409c40" and at(M, 0x00409C40) == "test r8, r8" and at(M, 0x00409C43) == "je 0x409c8f" and sorted(sites) == [0x00409C34],
      "tag 0 and '@ALL' skip the tag test, a NULL name returns 1; immediate 0x4C4C4140 sites in .text %s" % ["%08X" % s for s in sorted(sites)])
cmps = [S(M[a]) for a in sorted(M) if 0x00409C48 <= a <= 0x00409C87 and M[a].mnemonic == "cmp"]
loads = [S(M[a]) for a in sorted(M) if 0x00409C45 <= a <= 0x00409C83 and M[a].mnemonic == "mov"]
check("X2", cmps == ["cmp dword ptr [rcx + 0x%x], eax" % d for d in range(0x10, 0x30, 4)]
      and loads == ["mov eax, dword ptr [r8]"] + ["mov eax, dword ptr [r8 + %s]" % (d if d < 10 else hex(d)) for d in range(4, 0x20, 4)], "eight dword compares, +0x10..+0x2C against [r8+0..0x1C]")
check("X3", at(R, 0x004096DF) == "add eax, ebx" and at(R, 0x004096E1) == "cdqe" and at(F, 0x004096A4) == "add eax, dword ptr [rsp + 0x40]" and at(F, 0x004096A8) == "movsxd rbx, eax",
      "32-bit add then sign-extend in both")
check("X4", at(B, 0x0040961D) == "cmp ecx, 1" and at(B, 0x00409620) == "jne 0x40960e" and at(B, 0x0040960E) == "xor eax, eax"
      and at(R, 0x004096C8) == "test rcx, rcx" and at(R, 0x004096D5) == "cmp ebx, -1" and at(R, 0x004096DA) == "call 0x409600"
      and not any(R[a].mnemonic in ("test", "cmp") for a in R if 0x004096DA < a < 0x004096E3)
      and not any(F[a].mnemonic in ("test", "cmp") for a in F if 0x0040969F < a < 0x004096AB),
      "unsupported mode -> base 0; no test between the base and the add in either resolver")
check("X5", rip(B[0x00409622]) == [0x02B62E10] and at(B, 0x00409629) == "je 0x40963e" and at(B, 0x0040962B) == "mov rcx, qword ptr [rbx + 0x30]"
      and at(B, 0x00409634) == "mov qword ptr [rbx + 0x38], rax" and at(B, 0x0040963E) == "mov rax, qword ptr [rbx + 0x38]"
      and at(B, 0x00409648) == "lea rcx, [rbx + 0x10]" and at(B, 0x00409651).startswith("jmp "),
      "refresh via +0x30 into +0x38 only while 02B62E10 != 0; mode 0 -> %s" % at(B, 0x00409651))
check("X6", at(F, 0x00409690) == "call 0x409780" and at(F, 0x00409695) == "cmp dword ptr [rsp + 0x40], -1" and at(F, 0x0040969A) == "je 0x4096ab"
      and at(F, 0x0040966A) == "xor ebx, ebx" and at(F, 0x004096AB) == "mov rax, rbx",
      "the offset output is -1 on no match; the pointer finder returns NULL for it")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
