"""Falsification pass 1 on how-a-gamepad-becomes-a-controller-object (OPUS, 2026-09-29), from the shipping image.
Rows check the page as corrected by this pass (CON-188, CON-189).

  G0  sizes 00797910 147, 00796230 75, 00798A40 55, 00797690 638, 00792940 357, 00792AB0 181, 00792CB0 223, 00792B70 308
  G1  section 1: Steam interface -> 02EA9508 and its first method; DirectInput8Create(.., 0x800, .., 02EA5370); failure 9;
      EnumDevices(type 0, 00796230, 0, flags 1 = attached only); an EnumDevices failure also returns 9
  G2  section 2: the type byte +0x24; 0x12 mouse, 0x13 keyboard (start-up only); (t - 0x14) & 0xFA == 0 and t != 0x19
      admits 0x14/0x15/0x18
  G3  section 3.1: the XInput test 00797AD0 on the product GUID (+0x14), the sticky byte 02EA5379; the test runs again at
      007977B9 before the XInput build
  G4  section 3.2: the dedup walk over 01F401E8 compares the n-th kind-2 entry (n < 0x12) on +0x1D4/+0x1DC with the
      instance GUID (+4/+0xC); every controller class's kind method (vtable +8 of 01CB24C8/01CB2638/01CB2678/01CB26B8)
      is 00290180, "mov eax, 2; ret"; the Steam object's descriptor cell stays zeroed (no copy in 00792B70)
  G5  CON-188: the XInput build does not depend on the Steam step (bl is tested only at 00797826, after the XInput
      branch); Steam suppresses the DirectInput path only
  G6  CON-189: SetCooperativeLevel (vtable +0x68, flags 6) abandons only on E_NOTIMPL 0x80004001; any other result
      continues; Acquire (+0x38) is unchecked; no failure path releases the created device
  G7  section 4: base ctor - list link at +8 (tail insert via 01F401F0), device +0x28, 2 x 17 button bytes, four 0x48
      sub-objects via the vector iterator, memset 0x244 at +0x1D0
  G8  section 4 table: DI and XInput copy 0x244 bytes into +0x1D0; XInput stores the index at +0x458, zeroes +0x45C /
      +0x464 and calls 00862C70, which loads ".\\xinput1_3.dll" (LoadLibraryW) and resolves ordinal 100 into 02EBA3F0
  G9  section 5: the Steam ctor's handle 02EA95A0, "Global", 16 digital handles (02EA9510, names 01F40210) and 2 analog
      (02EA9590, names 01F40290) - image globals, rewritten by every Steam object
  G10 section 6: the window procedure sets 02EA5363 on 0x8000; 007999E0 clears it, re-enumerates with 00798A40, returns 9
      on failure (skipping the poll), then polls every registered device through vtable +0x28
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
body = lambda fa, n=None: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa)]
A = lambda fa, n=None: {x.address: (S(x), rip(x)) for x in body(fa, n)}
q64 = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]


def eq(m, a, text, target=None):
    g = m.get(a)
    return g is not None and g[0] == text and (target is None or target in g[1])


SZ = {0x00797910: 147, 0x00796230: 75, 0x00798A40: 55, 0x00797690: 638, 0x00792940: 357, 0x00792AB0: 181,
      0x00792CB0: 223, 0x00792B70: 308}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("G0", not bad, "sizes %s" % (bad or "all eight as cited"))
I = A(0x00797910)
check("G1", eq(I, 0x00797927, "mov qword ptr [rip + 0x2711bda], rcx", 0x02EA9508) and eq(I, 0x00797936, "call qword ptr [rax]")
      and eq(I, 0x00797958, "mov edx, 0x800") and eq(I, 0x00797942, "lea r9, [rip + 0x270da27]", 0x02EA5370)
      and eq(I, 0x00797966, "lea eax, [rbx + 9]") and eq(I, 0x00797976, "lea r8, [rip - 0x174d]", 0x00796230)
      and eq(I, 0x00797980, "mov dword ptr [rsp + 0x20], 1") and eq(I, 0x00797988, "xor edx, edx")
      and eq(I, 0x0079798D, "call qword ptr [r10 + 0x20]") and eq(I, 0x00797998, "cmovs ebx, ecx"),
      "Steam interface, DirectInput8Create 0x800 (fail 9), EnumDevices all/attached-only; its failure also 9")
C1, C2 = A(0x00796230), A(0x00798A40)
adm = [t for t in range(256) if ((t - 0x14) & 0xFF) & 0xFA == 0 and t != 0x19]
check("G2", eq(C1, 0x00796234, "movzx edx, byte ptr [rcx + 0x24]") and eq(C1, 0x00796238, "cmp dl, 0x12") and eq(C1, 0x0079623D, "cmp dl, 0x13")
      and eq(C1, 0x00796245, "test al, 0xfa") and eq(C1, 0x00796249, "cmp dl, 0x19") and eq(C1, 0x0079624E, "call 0x797690")
      and eq(C2, 0x00798A48, "cmp dl, 0x12") and not any("0x13" in t for t, _ in C2.values()) and eq(C2, 0x00798A59, "call 0x797690")
      and adm == [0x14, 0x15, 0x18],
      "device type +0x24; pads 0x14/0x15/0x18; the hot-plug callback ignores the keyboard")
P = A(0x00797690)
check("G3", eq(P, 0x007976C9, "add rcx, 0x14") and eq(P, 0x007976CD, "call 0x797ad0") and eq(P, 0x007976E3, "mov byte ptr [rip + 0x270dc90], cl", 0x02EA5379)
      and eq(P, 0x007977B5, "lea rcx, [rbp + 0x14]") and eq(P, 0x007977B9, "call 0x797ad0"),
      "XInput test on the product GUID, sticky byte; run again before the XInput build")
kinds = {vt: q64(vt + 8) for vt in (0x01CB24C8, 0x01CB2638, 0x01CB2678, 0x01CB26B8)}
k2 = body(0x00290180, 6)
ctor_s = A(0x00792B70)
check("G4", eq(P, 0x00797711, "call qword ptr [rax + 8]") and eq(P, 0x00797714, "cmp eax, 2") and eq(P, 0x00797719, "cmp edi, esi")
      and eq(P, 0x0079773A, "cmp rax, qword ptr [rbx + 0x1d4]") and eq(P, 0x00797747, "cmp rax, qword ptr [rbx + 0x1dc]")
      and eq(P, 0x00797756, "cmp esi, 0x12") and set(kinds.values()) == {0x00290180}
      and [S(x) for x in k2] == ["mov eax, 2", "ret"] and not any("+ 0x1d0" in t or "0x1d4" in t for t, _ in ctor_s.values()),
      "dedup on +0x1D4/+0x1DC over the first 18 kind-2 entries; all four classes answer 2 (00290180); Steam copies no descriptor")
check("G5", eq(P, 0x007977B3, "mov bl, 1") and eq(P, 0x007977BE, "test al, al") and eq(P, 0x007977C0, "je 0x797826")
      and eq(P, 0x00797821, "jmp 0x7978e1") and eq(P, 0x00797826, "test bl, bl") and eq(P, 0x00797828, "jne 0x7978e1")
      and [a for a, (t, _) in P.items() if t.startswith("test bl")] == [0x00797826],
      "CON-188: the XInput branch runs whatever Steam did; bl gates only the DirectInput path")
calls_rel = [a for a, (t, _) in P.items() if "+ 0x10]" in t and t.startswith("call qword ptr [rax") and a > 0x00797846]
check("G6", eq(P, 0x0079787E, "mov r8d, 6") and eq(P, 0x0079788B, "call qword ptr [rax + 0x68]") and eq(P, 0x0079788E, "cmp eax, 0x80004001")
      and eq(P, 0x00797893, "je 0x7978e1") and eq(P, 0x007978B9, "call qword ptr [rax + 0x38]") and eq(P, 0x007978BC, "mov ecx, 0x458")
      and eq(P, 0x0079785A, "js 0x7978e1") and eq(P, 0x00797874, "js 0x7978e1") and eq(P, 0x007978AF, "js 0x7978e1")
      and not calls_rel,
      "CON-189: only E_NOTIMPL from SetCooperativeLevel abandons; Acquire unchecked; no Release on any abandon path")
B0 = A(0x00792940)
check("G7", eq(B0, 0x00792956, "lea r8, [rcx + 8]") and eq(B0, 0x00792976, "mov qword ptr [rcx + 0x28], rdx")
      and eq(B0, 0x00792992, "mov qword ptr [rip + 0x17ad857], r8", 0x01F401F0) and eq(B0, 0x00792A2C, "mov ecx, 0x11")
      and eq(B0, 0x00792A31, "mov byte ptr [rax + 0x11], dl") and eq(B0, 0x007929C4, "mov edx, 0x48") and eq(B0, 0x007929C9, "lea r8d, [rdx - 0x44]")
      and eq(B0, 0x00792A89, "lea rcx, [rbx + 0x1d0]") and eq(B0, 0x00792A90, "mov r8d, 0x244") and eq(B0, 0x00792A96, "call 0x861ec0"),
      "list link at +8, device +0x28, 2 x 17 bytes, four 0x48 sub-objects, 0x244 zeroed at +0x1D0")
D, X, L = A(0x00792AB0), A(0x00792CB0), A(0x00862C70, 0x7F)
w = blob[OFF(0x01CCF9D8):OFF(0x01CCF9D8) + 64].decode("utf-16le", "replace").split("\x00")[0]
check("G8", eq(D, 0x00792ACF, "mov edx, 4") and eq(D, 0x00792B59, "mov dword ptr [rax + 0x40], ecx")
      and eq(X, 0x00792CD6, "mov dword ptr [rsi + 0x458], ebx") and eq(X, 0x00792CE6, "mov qword ptr [rsi + 0x45c], rax")
      and eq(X, 0x00792CED, "mov qword ptr [rsi + 0x464], rax") and eq(X, 0x00792D77, "call 0x862c70")
      and w == ".\\xinput1_3.dll" and eq(L, 0x00862CBB, "mov edx, 0x64") and eq(L, 0x00862CC6, "mov qword ptr [rip + 0x2657723], rax", 0x02EBA3F0),
      "4 x 0x80 + 0x44 = 0x244-byte copies; XInput index +0x458; the XInput ctor loads %r and resolves ordinal 100" % w)
check("G9", eq(ctor_s, 0x00792BDB, "mov qword ptr [rip + 0x27169be], rax", 0x02EA95A0) and eq(ctor_s, 0x00792BEC, "lea rdx, [rip + 0x1520d09]", 0x01CB38FC)
      and eq(ctor_s, 0x00792C41, "cmp rdi, 0x80") and eq(ctor_s, 0x00792C72, "cmp rbx, 0x10")
      and eq(ctor_s, 0x00792C2A, "mov rdx, qword ptr [rdi + rbp + 0x1e20210]") and eq(ctor_s, 0x00792C35, "mov qword ptr [rdi + rbp + 0x2d89510], rax")
      and eq(ctor_s, 0x00792C5A, "mov rdx, qword ptr [rbx + rbp + 0x1e20290]") and eq(ctor_s, 0x00792C66, "mov qword ptr [rbx + rbp + 0x2d89590], rax"),
      "handle 02EA95A0, 'Global', 16 digital + 2 analog handles into image globals")
U, W = A(0x007999E0), A(0x00798FF0)
check("G10", eq(W, 0x0079973E, "cmp rdi, 0x8000") and eq(W, 0x00799747, "mov byte ptr [rip + 0x270bc15], r13b", 0x02EA5363)
      and eq(U, 0x007999E4, "cmp byte ptr [rip + 0x270b978], 0", 0x02EA5363) and eq(U, 0x007999F4, "lea r8, [rip - 0xfbb]", 0x00798A40)
      and eq(U, 0x007999FB, "mov byte ptr [rip + 0x270b961], 0", 0x02EA5363) and eq(U, 0x00799A19, "mov eax, 9")
      and eq(U, 0x00799A56, "call qword ptr [rax + 0x28]"),
      "arrival byte on 0x8000; cleared, re-enumerated with 00798A40 (failure 9, no poll); every device polled")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
