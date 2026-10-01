"""Falsification pass 1 on how-close-a-unit-must-stand-to-act (OPUS, 2026-09-29), from the shipping image.
Each row checks what the bytes show against the page as corrected by this pass. The 543/557-row data census
(_experiments/evidence/action-range-bands) is carried, not re-run.

  B0  sizes 002FEB80 476, 00309300 169, 00320D70 146, 00338140 839, 00337A50 442. The one builder call 00304AB9 passes
      outs unit+0x6DC (reach, r9), +0x6D8 (middle), +0x6D4 (near): rsi = unit+0x6B0 (0030487F). The block the bands are
      copied to is unit+0x80 (003048EF), so its +0x120/+0x124/+0x128 are unit +0x1A0/+0x1A4/+0x1A8
  B1  section 1.1: the weapon word is stats(+0x698)+0x50; the builder's own bound is one-sided (id < count + 0x1000,
      jae to a null row); the empty sentinel 0xFFFF fails it
  B2  section 1.2: two radius-pair calls 00265090 (actor+0x10, target+0x10), maxss of each pair, the two maxima added
  B3  section 1.3/1.4: components 00320D70(actor, row, eqRow, 0) and (.., 1); reach 00309300(row, weapon word)
  B4  section 1.5 - CORRECTED (CON-187): the bands are authored only when BOTH components are non-zero. a == 0 jumps
      past b's test (002FECAA je 002FECB8) and b == 0 does too (002FECB1); ebx = 1 only at 002FECB3. Unordered (NaN)
      counts as non-zero (jp)
  B5  section 1.5/1.6: authored near a, middle a + b, reach a + b + R; else 0.6 R (008F3100) / 0.8 R (008F3108) / R;
      the radii sum is added to all three; each out pointer is null-tested before its store
  B6  section 2: 00309300 validates the id as class 6 (00322C50 with ecx 6); bit 26 of +0x0C picks byte +0x05 or the
      equipment row's +0x18, each / 10.0 (008F8180); no row -> 0; a null action row -> 0
  B7  section 3: bit 26 clear -> byte [row + component + 2] / 10.0; set -> kind byte +0x25; above 5 or 2 -> 0; a NULL
      equipment row is kind 0 (00320DAF xor eax), not "no pair"; the index is 01EED288[component + 2 kind]; a negative
      00320DC8 (003204E0) result -> 0
  B8  section 5: too far d > min(middle + 2.0 (01CEBC08), reach) -> +0x38 bit 1; too close near + 0.05 (008F30E8) > d
      and 003341A0 -> bit 2; each dropped against +0xD0; a failed 0033D660 forces bit 1; mutual rule reads the target
      unit's +0x1A4 / +0x1A0; two early exits (a slot-identity test at 0033818E and XZ < 0.1 (008C5F6C) at 003381AF)
      stop the step; with neither flag, 003343D0 (avoidance) is tried before the stand-and-face tail
  B9  section 6: gates +0x100 -> +0x3C bit 0x100, 002F8E70 == 1 for the unit and != 1 for the target's focus, speed
      +0xB0 non-zero; aim middle + 0.7 (008F3104) x (reach - middle); speed B +0xFC abandons (clears 0x100); the stand
      window is 30 x the global 01DFE0B4 (imul, not a literal 30); then speed A +0xF8
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]


def A(fa):
    return {x.address: (S(x), rip(x)) for x in body(fa)}


def eq(m, addr, text, target=None):
    got = m.get(addr)
    return got is not None and got[0] == text and (target is None or target in got[1])


SZ = {0x002FEB80: 476, 0x00309300: 169, 0x00320D70: 146, 0x00338140: 839, 0x00337A50: 442}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
C = A(0x00304850)
check("B0", not bad and eq(C, 0x0030487F, "lea rsi, [rcx + 0x6b0]") and eq(C, 0x003048EF, "lea rbx, [rdi + 0x80]")
      and eq(C, 0x00304A95, "lea r9, [rsi + 0x2c]") and eq(C, 0x00304A8A, "lea rcx, [rsi + 0x28]")
      and eq(C, 0x00304A7F, "lea rax, [rsi + 0x24]") and eq(C, 0x00304AA4, "mov qword ptr [rsp + 0x20], rcx")
      and eq(C, 0x00304A9F, "mov qword ptr [rsp + 0x28], rax") and eq(C, 0x00304AB9, "call 0x2feb80")
      and eq(C, 0x00304BF6, "mov dword ptr [rbx + 0x120], eax") and eq(C, 0x00304C0F, "mov dword ptr [rbx + 0x128], eax"),
      "sizes %s; outs reach +0x6DC / middle +0x6D8 / near +0x6D4; block at unit+0x80 (+0x120.. = unit +0x1A0..)"
      % (bad or "all five as cited"))
B = A(0x002FEB80)
check("B1", eq(B, 0x002FEBC3, "mov rax, qword ptr [rsi + 0x698]") and eq(B, 0x002FEBCA, "movzx edx, word ptr [rax + 0x50]")
      and eq(B, 0x002FEBCE, "lea eax, [r10 + 0x1000]") and eq(B, 0x002FEBD5, "cmp edx, eax") and eq(B, 0x002FEBD7, "jae 0x2fec1d")
      and eq(B, 0x002FEC1D, "mov rdi, rbx") and not any(t.startswith(("cmp edx, 0x1000", "cmp edi, 0x1000")) for t, _ in B.values())
      and 0xFFFF >= 0x1000 + 0xFFF,
      "weapon word stats +0x50; bound one-sided (id < count + 0x1000, else null row); 0xFFFF fails it for any table under 0xEFFF rows")
check("B2", eq(B, 0x002FEC34, "call 0x265090") and eq(B, 0x002FEC5C, "call 0x265090") and eq(B, 0x002FEC20, "mov rcx, qword ptr [rsi + 0x10]")
      and eq(B, 0x002FEC4A, "mov rcx, qword ptr [r15 + 0x10]") and eq(B, 0x002FEC53, "maxss xmm6, dword ptr [rsp + 0x98]")
      and eq(B, 0x002FEC6E, "maxss xmm8, dword ptr [rsp + 0x20]") and eq(B, 0x002FEC7E, "addss xmm8, xmm6"),
      "two radius pairs, max of each, summed")
check("B3", eq(B, 0x002FEC6B, "xor r9d, r9d") and eq(B, 0x002FEC83, "call 0x320d70") and eq(B, 0x002FEC88, "mov r9d, 1")
      and eq(B, 0x002FEC9A, "call 0x320d70") and eq(B, 0x002FECC2, "movzx edx, word ptr [rax + 0x50]") and eq(B, 0x002FECBF, "mov rcx, r14")
      and eq(B, 0x002FECC6, "call 0x309300"), "a = 00320D70(.., 0), b = (.., 1); R = 00309300(row, weapon word)")
check("B4", eq(B, 0x002FECA5, "ucomiss xmm7, xmm0") and eq(B, 0x002FECA8, "jp 0x2fecac") and eq(B, 0x002FECAA, "je 0x2fecb8")
      and eq(B, 0x002FECAC, "ucomiss xmm6, xmm0") and eq(B, 0x002FECAF, "jp 0x2fecb3") and eq(B, 0x002FECB1, "je 0x2fecb8")
      and eq(B, 0x002FECB3, "mov ebx, 1") and eq(B, 0x002FEB9F, "xor ebx, ebx")
      and [a for a, (t, _) in B.items() if t.startswith("mov ebx, ")] == [0x002FECB3],
      "CON-187: authored only when a != 0 AND b != 0 (a == 0 skips b's test); NaN counts as non-zero")
ok5 = (eq(B, 0x002FECD2, "addss xmm6, xmm7") and eq(B, 0x002FECD9, "addss xmm1, xmm2")
       and eq(B, 0x002FECDF, "mulss xmm0, dword ptr [rip + 0x5f4419]", 0x008F3100) and eq(B, 0x002FECEA, "mulss xmm1, dword ptr [rip + 0x5f4416]", 0x008F3108)
       and eq(B, 0x002FECFB, "addss xmm6, xmm8") and eq(B, 0x002FED00, "addss xmm7, xmm8") and eq(B, 0x002FED0A, "addss xmm1, xmm8")
       and eq(B, 0x002FED05, "test rbp, rbp") and eq(B, 0x002FED1C, "test rax, rax") and eq(B, 0x002FED2D, "test rax, rax")
       and abs(f32(0x008F3100) - 0.6) < 1e-6 and abs(f32(0x008F3108) - 0.8) < 1e-6)
check("B5", ok5, "authored a / a+b / a+b+R, else 0.6R / 0.8R / R; radii on all three; each out null-tested")
R = A(0x00309300)
check("B6", eq(R, 0x00309315, "lea ecx, [r8 + 6]") and eq(R, 0x00309319, "call 0x322c50") and eq(R, 0x00309377, "test dword ptr [rbx + 0xc], 0x4000000")
      and eq(R, 0x00309380, "movzx eax, byte ptr [rbx + 5]") and eq(R, 0x00309389, "je 0x309369") and eq(R, 0x0030938B, "movzx eax, byte ptr [rcx + 0x18]")
      and eq(R, 0x0030939B, "divss xmm0, dword ptr [rip + 0x5eeddd]", 0x008F8180) and f32(0x008F8180) == 10.0
      and eq(R, 0x00309364, "test rbx, rbx") and eq(R, 0x00309369, "xorps xmm0, xmm0"),
      "class-6 validity; bit 26 -> weapon +0x18 else action +0x05, / 10; no row -> 0; null action row -> 0")
K = A(0x00320D70)
check("B7", eq(K, 0x00320D74, "test dword ptr [rdx + 0xc], 0x4000000") and eq(K, 0x00320DE9, "movzx ecx, byte ptr [rax + rdx + 2]")
      and eq(K, 0x00320D93, "movzx eax, byte ptr [r8 + 0x25]") and eq(K, 0x00320D98, "cmp eax, 5") and eq(K, 0x00320D9D, "cmp eax, 2")
      and eq(K, 0x00320D91, "je 0x320daf") and eq(K, 0x00320DAF, "xor eax, eax") and eq(K, 0x00320DB1, "lea ecx, [r9 + rax*2]")
      and eq(K, 0x00320DB5, "lea rax, [rip + 0x1bcc4cc]", 0x01EED288) and eq(K, 0x00320DC8, "call 0x3204e0") and eq(K, 0x00320DCF, "js 0x320da2"),
      "bit 26 clear -> row +2+component / 10; set -> kind +0x25 (>5 or 2 -> 0); a NULL equipment row is kind 0; 01EED288[c + 2k]; failure -> 0")
L = A(0x00338140)
ok8 = (eq(L, 0x00338253, "addss xmm6, dword ptr [rip + 0x19b39ad]", 0x01CEBC08) and f32(0x01CEBC08) == 2.0
       and eq(L, 0x00338266, "minss xmm6, dword ptr [rax + 0x128]") and eq(L, 0x0033827D, "or dword ptr [rsi + 0x38], 2")
       and eq(L, 0x0033825B, "addss xmm7, dword ptr [rip + 0x5bae85]", 0x008F30E8) and abs(f32(0x008F30E8) - 0.05) < 1e-6
       and eq(L, 0x00338292, "call 0x3341a0") and eq(L, 0x0033829B, "or dword ptr [rsi + 0x38], 4")
       and eq(L, 0x003382AE, "movss xmm0, dword ptr [rax + 0xd0]") and eq(L, 0x003382D1, "comiss xmm8, dword ptr [rax + 0xd0]")
       and eq(L, 0x003382F2, "call 0x33d660") and eq(L, 0x00338301, "or dword ptr [rsi + 0x38], 2")
       and eq(L, 0x00338201, "call 0x31b7e0") and eq(L, 0x00338206, "cmp qword ptr [rdi + 0xf0], rax")
       and eq(L, 0x00338225, "comiss xmm1, dword ptr [rcx + 0x1a4]") and eq(L, 0x0033822E, "movss xmm7, dword ptr [rcx + 0x1a0]")
       and eq(L, 0x0033818E, "cmp dword ptr [rcx + 0x150], eax") and eq(L, 0x00338194, "je 0x338475")
       and eq(L, 0x003381A6, "movss xmm9, dword ptr [rip + 0x58ddbd]", 0x008C5F6C) and abs(f32(0x008C5F6C) - 0.1) < 1e-6
       and eq(L, 0x003381B3, "ja 0x338475") and eq(L, 0x003383C5, "call 0x3343d0") and eq(L, 0x0033843D, "call 0x33bc80"))
check("B8", ok8, "too far min(middle + 2, reach); too close near + 0.05 with 003341A0; +0xD0 drops; clearance forces approach; "
      "mutual rule on the target unit's +0x1A4 / +0x1A0 (its own copies); two early exits; avoidance tried before standing")
P = A(0x00337A50)
ok9 = (eq(P, 0x00337A74, "test dword ptr [rax + 0x3c], 0x100") and eq(P, 0x00337A88, "call 0x2f8e70") and eq(P, 0x00337AA3, "call 0x31b7e0")
       and eq(P, 0x00337AB3, "je 0x337bdf") and eq(P, 0x00337AB9, "movss xmm0, dword ptr [rbx + 0xb0]")
       and eq(P, 0x00337AF3, "mulss xmm6, dword ptr [rip + 0x5bb609]", 0x008F3104) and abs(f32(0x008F3104) - 0.7) < 1e-6
       and eq(P, 0x00337B32, "divss xmm6, dword ptr [rax + 0xfc]") and eq(P, 0x00337B50, "jbe 0x337bdf")
       and eq(P, 0x00337BE6, "and dword ptr [rax + 0x3c], 0xfffffeff")
       and eq(P, 0x00337B75, "imul ecx, dword ptr [rip + 0x1ac6538], 0x1e", 0x01DFE0B4)
       and eq(P, 0x00337B8A, "divss xmm7, dword ptr [rdx + 0xf8]") and eq(P, 0x00337BD7, "mov dword ptr [rbx + 0xb0], ecx"))
check("B9", ok9, "gates 0x100 / predicate / speed; aim middle + 0.7 (reach - middle); speed B abandons and clears 0x100; "
      "stand window 30 x [01DFE0B4]; then speed A")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
