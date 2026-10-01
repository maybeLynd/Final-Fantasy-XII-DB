"""Falsification pass 1 on CONTRACT-equipment-compatibility (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  Q0  section 2 sizes: 212 / 493 / 70 / 172 / 435 B
  Q1  EQ-1: 002F7F70 `movzx ecx, byte ptr [rcx + 9]`, 002F7F76 `cmp byte ptr [rbx + 0x11], cl` with rbx = arg2 (edx) and rcx
      from arg1 (ecx); exactly 2 call sites image-wide, both in 002F9F20: 002FA013 (ecx = the slot-1 candidate bx, edx = out[0])
      and 002FA069 (ecx = out[1], edx = out[0]); the inlined copy 00317A7B/00317A7F takes +0x11 from the record resolved from
      word [r15] (the main hand) and +0x09 from the candidate
  Q2  EQ-2: 00317A2C `cmp byte ptr [rdi + 9], 0x12` / je past the partner test; both exempt an empty main hand (00317A32,
      002F7EEA); only the standalone returns 1 on a 0xFFFF candidate (002F7ED5); the slot-1 loop re-tests every candidate with
      002F7EC0 (002FA008..002FA01A); out[1] is copied from stats +0x52 (002F9F94..002F9F99)
  Q3  EQ-3: 00317A18..00317A21 `movzx eax, byte ptr [rdi + 7]; shr eax, 5; cmp eax, esi; jne`; 00323CDF `test byte ptr [rcx + 7],
      0x10` / jne to the return-1 exit
  Q4  EQ-4: 00D0F9C0 = {1000, 10C8, 10DC, 1118}, 00D0F9D0 = {10C8, 11A4, 1118, 1154}, loaded at 002F9F37 / 002F9F42 and indexed
      at 002F9FE0 / 002F9FE5
  Q5  EQ-5: 00317AD1 `mov eax, dword ptr [rbx]`, 00317AD3 `bt eax, ecx`, 00317AD6 `jb 0x317ae7`, and 00317AE7 is `xor eax, eax`
  Q6  EQ-6: 00317A89/00317A8F test stats +5 and jump to the eligible exit; 00323C8F/00323C93 and 00323C97 `cmp byte ptr [rbx + 4],
      6` / ja reach 00323CFC `mov eax, 1`
  Q7  EQ-7: class 6 at 0031799A (r8 zeroed at 0031798B) and class 1 at 00323C72 (r8 zeroed at 00323C6A), both calling 00322C50;
      the class-1 failure is the gate's only exit that returns the validator's 0, every other early exit reaches 00323CFC
  Q8  EQ-8: 002FA056 `test esi, esi` / jne; 002FA05F stores 0x1000 into out[0]; 002FA077 stores 0xFFFF into out[1]; five
      stats words +0x50..+0x58 copied at 002F9F8D..002F9FB4; the slot loop bound is `cmp esi, 4` (002FA08F)
  Q9  section 10: 0031794D `ja` on a slot above 4; 0031795A compares against the 00D107E8 table = {1000, FFFF x4}; 0031797E
      rejects 0xFFFF
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
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"

C, E, W, L, R = (body(a) for a in (0x002F7EC0, 0x00317930, 0x00317B20, 0x00323C60, 0x002F9F20))
check("Q0", [sizes[a] for a in (0x002F7EC0, 0x00317930, 0x00317B20, 0x00323C60, 0x002F9F20)] == [212, 493, 70, 172, 435],
      "%s" % [sizes[a] for a in (0x002F7EC0, 0x00317930, 0x00317B20, 0x00323C60, 0x002F9F20)])

sites = []
text = next(x for x in SECS if x[0] == ".text")
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x002F7EC0:
                sites.append((x.address, fa))
    except ValueError:
        continue
check("Q1", at(C, 0x002F7ECF) == "movzx ebx, dx" and at(C, 0x002F7ED2) == "movzx edi, cx" and at(C, 0x002F7F70) == "movzx ecx, byte ptr [rcx + 9]"
      and at(C, 0x002F7F76) == "cmp byte ptr [rbx + 0x11], cl"
      and sorted(sites) == [(0x002FA013, 0x002F9F20), (0x002FA069, 0x002F9F20)]
      and at(R, 0x002FA00D) == "movzx edx, word ptr [rdi]" and at(R, 0x002FA010) == "movzx ecx, bx"
      and at(R, 0x002FA062) == "movzx edx, word ptr [rdi]" and at(R, 0x002FA065) == "movzx ecx, word ptr [rdi + 2]"
      and at(E, 0x00317A61) == "movzx r8d, word ptr [r15]" and at(E, 0x00317A7B) == "movzx eax, byte ptr [rcx + 0x11]"
      and at(E, 0x00317A7F) == "cmp byte ptr [rdi + 9], al",
      "arg2 in rbx (%s), %s / %s; call sites %s; inline %s / %s from %s"
      % (at(C, 0x002F7ECF), at(C, 0x002F7F70), at(C, 0x002F7F76), ["%08X" % s for s, _ in sorted(sites)], at(E, 0x00317A7B), at(E, 0x00317A7F), at(E, 0x00317A61)))
check("Q2", at(E, 0x00317A2C) == "cmp byte ptr [rdi + 9], 0x12" and at(E, 0x00317A30) == "je 0x317a84" and at(E, 0x00317A32) == "cmp word ptr [r15], r12w"
      and at(E, 0x00317A36) == "je 0x317a84" and at(C, 0x002F7ED5) == "cmp cx, ax" and at(C, 0x002F7EDA) == "mov eax, 1"
      and at(C, 0x002F7EEA) == "cmp bx, ax" and at(C, 0x002F7EED) == "je 0x2f7eda" and at(R, 0x002FA008) == "cmp esi, 1"
      and at(R, 0x002FA013) == "call 0x2f7ec0" and at(R, 0x002FA01A) == "je 0x2fa041" and at(R, 0x002F9F94) == "movzx eax, word ptr [r13 + 0x52]"
      and at(R, 0x002F9F99) == "mov word ptr [rdi + 2], ax",
      "shield skip %s; empty main %s / %s; empty candidate %s; slot-1 re-test %s; out[1] %s" %
      (at(E, 0x00317A30), at(E, 0x00317A32), at(C, 0x002F7EEA), at(C, 0x002F7ED5), at(R, 0x002FA013), at(R, 0x002F9F94)))
check("Q3", [at(E, a) for a in (0x00317A18, 0x00317A1C, 0x00317A1F, 0x00317A21)] == ["movzx eax, byte ptr [rdi + 7]", "shr eax, 5", "cmp eax, esi", "jne 0x317ae7"]
      and at(L, 0x00323CDF) == "test byte ptr [rcx + 7], 0x10" and at(L, 0x00323CE3) == "jne 0x323cfc" and at(L, 0x00323CFC) == "mov eax, 1",
      "slot bits %s; exemption %s -> %s" % (at(E, 0x00317A1C), at(L, 0x00323CDF), at(L, 0x00323CFC)))
lo = list(struct.unpack("<4i", blob[OFF(0x00D0F9C0):OFF(0x00D0F9C0) + 16])); hi = list(struct.unpack("<4i", blob[OFF(0x00D0F9D0):OFF(0x00D0F9D0) + 16]))
check("Q4", lo == [0x1000, 0x10C8, 0x10DC, 0x1118] and hi == [0x10C8, 0x11A4, 0x1118, 0x1154] and rip(R[0x002F9F37]) == [0x00D0F9C0]
      and rip(R[0x002F9F42]) == [0x00D0F9D0] and at(R, 0x002F9FE0) == "mov ebx, dword ptr [rsp + r14 + 0x28]" and at(R, 0x002F9FE5) == "mov ebp, dword ptr [rsp + r14 + 0x38]"
      and lo[1] <= lo[2] and hi[3] <= hi[1],
      "lo %s hi %s; slot 1 contains slots 2 and 3" % ([hex(v) for v in lo], [hex(v) for v in hi]))
check("Q5", at(E, 0x00317AD1) == "mov eax, dword ptr [rbx]" and at(E, 0x00317AD3) == "bt eax, ecx" and at(E, 0x00317AD6) == "jb 0x317ae7" and at(E, 0x00317AE7) == "xor eax, eax",
      "%s / %s -> %s" % (at(E, 0x00317AD3), at(E, 0x00317AD6), at(E, 0x00317AE7)))
elig = next((a for a in sorted(E) if a >= 0x00317B06), None)
check("Q6", at(E, 0x00317A89) == "movzx eax, byte ptr [rbp + 5]" and at(E, 0x00317A8F) == "jne 0x317b06" and at(E, 0x00317B06) == "mov eax, 1"
      and at(L, 0x00323C8F) == "movzx eax, byte ptr [rbx + 5]" and at(L, 0x00323C95) == "jne 0x323cfc" and at(L, 0x00323C97) == "cmp byte ptr [rbx + 4], 6"
      and at(L, 0x00323C9B) == "ja 0x323cfc",
      "chain %s -> %s; gate %s / %s" % (at(E, 0x00317A8F), at(E, 0x00317B06), at(L, 0x00323C95), at(L, 0x00323C9B)))
early = sorted({x.operands[0].imm for a, x in L.items() if x.mnemonic.startswith("j") and x.mnemonic != "jmp" and x.operands[0].type == X86_OP_IMM}
               - {0x00323C8A, 0x00323CDD, 0x00323CDF})
check("Q7", at(E, 0x0031798B) == "xor r8d, r8d" and at(E, 0x0031799A) == "lea ecx, [r8 + 6]" and at(E, 0x0031799E) == "call 0x322c50"
      and at(L, 0x00323C6A) == "xor r8d, r8d" and at(L, 0x00323C72) == "lea ecx, [r8 + 1]" and at(L, 0x00323C76) == "call 0x322c50"
      and at(L, 0x00323C7D) == "jne 0x323c8a" and at(L, 0x00323C89) == "ret" and early == [0x00323CFC] and at(L, 0x00323CF7) == "jmp 0x323bb0",
      "classes 6 and 1 to 00322C50; failed class-1 test returns at 00323C89; every other early exit targets %s; the board lookup is the tail %s"
      % (["%08X" % e for e in early], at(L, 0x00323CF7)))
copies = [at(R, a) for a in (0x002F9F8D, 0x002F9F94, 0x002F9F9D, 0x002F9FA6, 0x002F9FAF)]
check("Q8", at(R, 0x002FA056) == "test esi, esi" and at(R, 0x002FA058) == "jne 0x2fa07b" and at(R, 0x002FA05F) == "mov word ptr [rdi], cx"
      and at(R, 0x002FA051) == "mov ecx, 0x1000" and at(R, 0x002FA077) == "mov word ptr [rdi + 2], ax" and at(R, 0x002FA070) == "mov eax, 0xffff"
      and copies == ["movzx eax, word ptr [rax + 0x50]"] + ["movzx eax, word ptr [r13 + 0x%x]" % o for o in (0x52, 0x54, 0x56, 0x58)]
      and at(R, 0x002FA08F) == "cmp esi, 4",
      "epilogue %s; forced %s; dropped %s; five copies; bound %s" % (at(R, 0x002FA056), at(R, 0x002FA05F), at(R, 0x002FA077), at(R, 0x002FA08F)))
tab = list(struct.unpack("<5H", blob[OFF(0x00D107E8):OFF(0x00D107E8) + 10]))
check("Q9", at(E, 0x0031794A) == "cmp esi, 4" and at(E, 0x0031794D) == "ja 0x317b0d" and rip(E[0x00317953]) == [0x00D107E8]
      and at(E, 0x0031795A) == "cmp bx, word ptr [rcx + rsi*2]" and tab == [0x1000, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF]
      and at(E, 0x0031797E) == "cmp bx, r12w" and at(E, 0x00317984) == "xor eax, eax",
      "slot bound %s; short-circuit table %s; 0xFFFF reject %s" % (at(E, 0x0031794D), [hex(v) for v in tab], at(E, 0x0031797E)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
