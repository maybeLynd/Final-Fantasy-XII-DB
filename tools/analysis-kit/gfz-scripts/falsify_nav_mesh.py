"""Falsification pass 1 on how-a-unit-finds-its-way-across-the-navigation-mesh (OPUS, 2026-09-29), from the shipping image.
The 461-file dataset census and EXP-131's executions are carried, not re-run.

  N0  sizes 00383850 368, 0026E300 73, 003792E0 245, 003278D0 84, 0026E880 53, 0026E850 40, 003839F0 34, 003839C0 33,
      00383670 204
  N1  section 5: adjacency[from x regionCount + to] of 0 costs 0x7FFFFFFF; the class-mask test is bit moverClass of portal
      +6; byte +4 = 0xFF skips the gate query; the gated answer 0 falls back to the mask, 1 opens, anything else closes
  N2  section 5: 0026E300 - class table 00915760 = {23, 25, 26, 27, -1, 24}; a negative bit answers -1; the override pair at
      0209A3E0 + 8 x mapId: [+0] present bits, [+4] closed bits -> 0 / 1 / 2
  N3  section 5: cost = trunc(100.0 (008F3134) x d), plus the goal leg (hypot) only when to == goalRegion; d alone goes back
  N4  section 7: 003792E0's two ten-entry tables send kinds 0, 1, 2, 3, 7, 9 to bits 23, 25, 26, 27, 24, 12 and kinds 4, 5,
      6, 8 to the bare return; on >= 0 sets through 0026E880 with bit value (on == 0), on < 0 removes through 0026E850;
      both setters tail-jump to 003278D0
  N5  section 7: 003278D0 walks every battle-unit slot with byte +0 bit 4 and calls 003839C0 and 003839F0 on unit + 0x200
  N6  section 3: 003839F0 fills 128 bytes of 0xFF from +0x10; 003839C0 fills two words of 0xFFFF from +0x0C
  N7  sections 4 and 8: the search returns -2 / -3 after each lookup, bounds the region count at 0x80, starts distances at
      0x7FFFFFFF, returns -1 on failure; the follow step advances next[] while 00383A30 answers 1, re-aims with 00383C90,
      stores the region at [path] and copies the mover's own y
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
A = lambda fa: {x.address: (S(x), rip(x)) for x in body(fa)}
u32 = lambda va: struct.unpack("<I", blob[OFF(va):OFF(va) + 4])[0]


def eq(m, a, text, target=None):
    g = m.get(a)
    return g is not None and g[0] == text and (target is None or target in g[1])


SZ = {0x00383850: 368, 0x0026E300: 73, 0x003792E0: 245, 0x003278D0: 84, 0x0026E880: 53, 0x0026E850: 40, 0x003839F0: 34,
      0x003839C0: 33, 0x00383670: 204}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("N0", not bad, "sizes %s" % (bad or "all nine as cited"))
C = A(0x00383850)
check("N1", eq(C, 0x00383883, "movzx r10d, word ptr [r11 + 0xa]") and eq(C, 0x00383888, "imul r10d, ebx") and eq(C, 0x0038389A, "mov eax, 0x7fffffff")
      and eq(C, 0x003838C1, "shl r8d, cl") and eq(C, 0x003838C4, "test byte ptr [rax + rdi*8 + 6], r8b")
      and eq(C, 0x003838CC, "cmp byte ptr [rax + rdi*8 + 4], 0xff") and eq(C, 0x003838D8, "call 0x32a780")
      and eq(C, 0x003838DF, "je 0x3838f0") and eq(C, 0x003838E4, "je 0x3838f4") and eq(C, 0x003838E6, "mov eax, 0x7fffffff"),
      "adjacency 0 closed; class-mask bit; 0xFF ungated; gate 0 -> mask, 1 -> open, else closed")
G = A(0x0026E300)
tbl = struct.unpack("<6i", blob[OFF(0x00915760):OFF(0x00915760) + 24])
check("N2", tbl == (23, 25, 26, 27, -1, 24) and eq(G, 0x0026E317, "js 0x26e345") and eq(G, 0x0026E31C, "lea r8, [rdx + 0x1f7a3e0]")
      and eq(G, 0x0026E330, "test dword ptr [r8], edx") and eq(G, 0x0026E335, "test dword ptr [r8 + 4], edx")
      and eq(G, 0x0026E33E, "cmovne eax, ecx") and eq(G, 0x0026E345, "or eax, 0xffffffff"),
      "class table %s; override present/closed words at 0209A3E0 + 8 mapId" % (tbl,))
check("N3", struct.unpack("<f", blob[OFF(0x008F3134):OFF(0x008F3134) + 4])[0] == 100.0 and eq(C, 0x00383971, "movss dword ptr [rax], xmm6")
      and eq(C, 0x00383975, "cmp ebp, r15d") and eq(C, 0x00383997, "addss xmm6, xmm0")
      and eq(C, 0x0038399B, "mulss xmm6, dword ptr [rip + 0x56f791]", 0x008F3134) and eq(C, 0x003839A3, "cvttss2si eax, xmm6"),
      "cost trunc(100 x (d + goal leg on the last hop)); d stored before the goal leg")
V = A(0x003792E0)
t_set = [0x00120000 + u32(0x003793D8 + 4 * i) for i in range(10)]
t_del = [0x00120000 + u32(0x00379400 + 4 * i) for i in range(10)]
bit_set = {0x0037930D: 23, 0x0037931C: 24, 0x0037932B: 25, 0x0037933A: 26, 0x00379349: 27, 0x00379358: 12, 0x003793D4: None}
bit_del = {0x00379380: 23, 0x0037938E: 24, 0x0037939C: 25, 0x003793AA: 26, 0x003793B8: 27, 0x003793C6: 12, 0x003793D4: None}
want = [23, 25, 26, 27, None, None, None, 24, None, 12]
ok_bits = [bit_set.get(a, "?") for a in t_set] == want and [bit_del.get(a, "?") for a in t_del] == want
ok_lea = all(eq(V, a + 6, "lea r8d, [r9 + 0x%x]" % (b - 1)) for a, b in bit_set.items() if b)
S1, S2 = A(0x0026E880), A(0x0026E850)
check("N4", ok_bits and ok_lea and eq(V, 0x003792ED, "sete dl") and eq(V, 0x003792E6, "js 0x379367")
      and eq(S1, 0x0026E8B0, "jmp 0x3278d0") and eq(S2, 0x0026E873, "jmp 0x3278d0")
      and eq(S1, 0x0026E883, "lea rcx, [rip + 0x1e2bb56]", 0x0209A3E0) and eq(S2, 0x0026E870, "and dword ptr [r9], eax"),
      "kinds 0,1,2,3,7,9 -> bits 23,25,26,27,24,12; 4,5,6,8 bare; set (on == 0 closes) or remove; both end in 003278D0")
W = A(0x003278D0)
check("N5", eq(W, 0x003278F2, "test byte ptr [rax], 0x10") and eq(W, 0x003278F7, "lea rdi, [rax + 0x200]")
      and eq(W, 0x00327901, "call 0x3839c0") and eq(W, 0x00327909, "call 0x3839f0"),
      "every live unit's path record (unit + 0x200) loses its no-route memory and next[] chain")
R1, R2 = A(0x003839F0), A(0x003839C0)
check("N6", eq(R1, 0x003839F2, "lea rax, [rcx + 0x10]") and eq(R1, 0x00383A02, "mov byte ptr [rax], 0xff") and eq(R1, 0x00383A09, "cmp edx, 0x80")
      and eq(R2, 0x003839C2, "lea rax, [rcx + 0xc]") and eq(R2, 0x003839D2, "mov word ptr [rax], 0xffff") and eq(R2, 0x003839DB, "cmp edx, 2"),
      "next[128] = 0xFF from +0x10; two no-route words = 0xFFFF from +0x0C")
Q, F = A(0x00382FF0), A(0x00383670)
check("N7", eq(Q, 0x00383051, "mov eax, 0xfffffffe") and eq(Q, 0x00383077, "mov eax, 0xfffffffd") and eq(Q, 0x00383149, "cmp eax, 0x80")
      and eq(Q, 0x003831C6, "mov r14d, 0x7fffffff") and eq(Q, 0x003835E1, "or eax, 0xffffffff")
      and eq(F, 0x003836B8, "call 0x383a30") and eq(F, 0x003836D8, "je 0x3836c2") and eq(F, 0x003836ED, "call 0x383c90")
      and eq(F, 0x00383700, "mov dword ptr [rdi], esi") and eq(F, 0x0038371D, "mov ecx, dword ptr [r14 + 4]"),
      "-2 / -3 / 0x80 bound / 0x7FFFFFFF / -1; follow advances while inside, re-aims, stores the region, keeps the mover's y")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
