"""Falsification pass 1 on fdm-and-for-entries (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The archive census
(members/for_fdm_entry_census.py, 1,066 files) and FABLE's composite-key control are carried, not re-run.

  M0  sizes and the evidence list's instruction count for 004201F0
  M1  the binder 00504F00: seven tags through 00409A30 into +0x208..+0x220, and 00504E70 binding @FRP / @FEF into +0x1F0 /
      +0x228; the unbind at 00504CBF passes '@FDM' to 00409CA0 behind test byte [obj + 8], 4
  M2  @FOR consumer 1, 004201F0: '@FOR' checked at 00420274; the stack vector {0, u16@3C x [008F30E4], u16@3E x [008F30E4],
      [00D10824]} with 0.01 and 1.0e8; +0xA0 used when byte +0xC0 bit 0; the window loop; the clamp by +0x3B; lodFrac to
      +0x2A4; word +0x90 to +0x64; the 0x2000 bit by +0x284 & 0x100; 00421280(object, 1)
  M3  @FOR consumer 2, 00504840: byte count +0x30, base u16 +0x38, stride 0xE0, key byte at +0, f32 +0x18, default
      [01CEBBA8] = 1.0; its one caller is 0042061B with byte +0x5C, stored to +0x26C
  M4  005048A0: +0x20C, u16 +0x32, {count, keys} linear search, -1; its one caller is 005210BB
  M5  00521050: w4 & 1 against +0x2F2; the composite key (w4 & 0xFFFC) << 14 | w2 on w4 & 2; else movsx w2; then 00373060
      (resolved, ordinal, w6), its one caller
  M6  00373060: bound by +0x38 at 003730BA; 0x7FFF stored bare, anything else stored with +0 |= 0x1000; 00372820 and
      00372510 store 0x7FFF and clear 0x1000; 00371330 is called only at 0053C36F / 0053C3AD
  M7  the 0053B2xx builder: table A / B / records resolved at 0053B33A..0053B35A; the @FTE (idx + 2) x 0x20 sum; list ->
      descriptor -> sub-record at 0053C305..0053C331; the 0x1000 gate at 0053C34C; slot ordinals >> 8 and >> 18 masked 0x3FF;
      the s8 +2 / +3 fallbacks; x 0x290 with 0x6C040000 at 0053CB58 / 0053CB71; | 0x30000000 at 0053CC18
  M8  0053D4B0's VIF row {desc +4 bit 0, A | B != 0, B, A} at 0053D52C..0053D577
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
at = lambda fa: {x.address: S(x) for x in body(fa)}
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x00504F00: 582, 0x004201F0: 648, 0x00504840: 93, 0x005048A0: 146, 0x00521050: 154, 0x00420480: 977, 0x00504E70: 134,
      0x00373060: 145, 0x00371330: 132, 0x0053D4B0: 705, 0x0053AB50: 9695}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
n_ins = len(body(0x004201F0))
check("M0", not bad and n_ins == 143,
      "sizes as measured %s; 004201F0 decodes to %d instructions in its 648 bytes (the evidence list says 144 - a count "
      "note, not a mechanism claim)" % ("(all eleven)" if not bad else bad, n_ins))

tag = lambda s: struct.unpack("<I", s.encode())[0]
B = at(0x00504F00)
want = [(0x00504F8C, "@FOR", 0x208), (0x00504FA2, "@FDM", 0x20C), (0x00504FB8, "@FTR", 0x210), (0x00504FCE, "@FEF", 0x214),
        (0x00504FE4, "@FTE", 0x218), (0x00504FFA, "@FCT", 0x21C), (0x00505010, "@FCP", 0x220)]
tags_ok = all(B.get(a) == "mov edx, 0x%x" % tag(t) for a, t, _o in want)
stores_ok = all(any(s == "mov dword ptr [rbx + 0x%x], eax" % o for s in B.values()) for _a, _t, o in want)
U = at(0x00504C40)
check("M1", tags_ok and stores_ok and B.get(0x00504F4C) == "lea rcx, [rbx + 0x1f0]" and B.get(0x00504F58) == "mov r9d, 0x%x" % tag("@FRP")
      and B.get(0x00504F6C) == "lea rcx, [rbx + 0x228]" and B.get(0x00504F78) == "mov r9d, 0x%x" % tag("@FEF")
      and U.get(0x00504CB1) == "test byte ptr [rsi + 8], 4" and U.get(0x00504CBF) == "mov edx, 0x%x" % tag("@FDM") and U.get(0x00504CC4) == "call 0x409ca0",
      "seven tags in order into +0x208..+0x220; @FRP -> +0x1F0, @FEF -> +0x228; the @FDM unbind behind bit 2 of byte +8")

L = at(0x004201F0)
check("M2", L.get(0x00420274) == "cmp dword ptr [rcx], 0x%x" % tag("@FOR") and abs(f32(0x008F30E4) - 0.01) < 1e-9 and f32(0x00D10824) == 1.0e8
      and L.get(0x004202AE) == "movzx eax, word ptr [rcx + 0x3c]" and L.get(0x004202CB) == "movzx eax, word ptr [rcx + 0x3e]"
      and L.get(0x004202C0) == "mov dword ptr [rsp + 0xb0], ebx" and L.get(0x00420303) == "movss dword ptr [rsp + 0xbc], xmm0"
      and L.get(0x00420397) == "test byte ptr [rsi + 0xc0], 1" and L.get(0x004203A8) == "lea rcx, [rsi + 0xa0]"
      and L.get(0x00420382) == "movss xmm1, dword ptr [rsi + 0x208]" and L.get(0x004203C0) == "comiss xmm1, dword ptr [rcx + rax*4]"
      and L.get(0x004203C6) == "movss xmm0, dword ptr [rcx + rax*4 + 4]" and L.get(0x004203DB) == "movzx eax, byte ptr [rbp + 0x3b]"
      and L.get(0x004203E1) == "cmovl ebx, eax" and L.get(0x004203FF) == "movss dword ptr [rdi + 0x2a4], xmm1"
      and L.get(0x0042040E) == "mov word ptr [rdi + 0x64], ax" and L.get(0x00420424) == "test dword ptr [rdi + 0x284], 0x100"
      and L.get(0x00420430) == "or dword ptr [rax], 0x2000" and L.get(0x0042043E) == "mov edx, 1" and L.get(0x00420446) == "call 0x421280",
      "magic, the {0, cm x 0.01, cm x 0.01, 1.0e8} vector, the +0xA0 alternative, the window loop, the +0x3B clamp and the four outputs")

K = at(0x00504840)
check("M3", K.get(0x00504840, "").endswith("[rip + 0x17e7360]") and f32(0x01CEBBA8) == 1.0 and K.get(0x00504850) == "movzx r11d, word ptr [rcx + 0x38]"
      and K.get(0x00504858) == "movzx r9d, byte ptr [rcx + 0x30]" and K.get(0x0050487E) == "add rcx, 0xe0" and K.get(0x00504870) == "movzx eax, byte ptr [rcx]"
      and K.get(0x00504895) == "movss xmm0, dword ptr [rcx + r11 + 0x18]" and callers(0x00504840) == [0x0042061B]
      and at(0x00420480).get(0x00420614) == "movzx edx, byte ptr [rsi + 0x5c]" and at(0x00420480).get(0x00420620) == "movss dword ptr [rsi + 0x26c], xmm0",
      "the 0xE0 walk, f32 +0x18, default 1.0; one caller 0042061B with byte +0x5C, result to +0x26C")
F = at(0x005048A0)
check("M4", F.get(0x005048E5) == "mov ecx, dword ptr [rax + 0x20c]" and F.get(0x005048EB) == "cmp ecx, -1" and F.get(0x005048FA) == "movzx eax, word ptr [rax + 0x32]"
      and F.get(0x0050490E) == "mov edx, dword ptr [rax]" and F.get(0x00504916) == "cmp dword ptr [rcx], ebx" and F.get(0x00504924) == "or eax, 0xffffffff"
      and callers(0x005048A0) == [0x005210BB],
      "+0x20C, u16 +0x32, the linear key search, -1; one caller 005210BB")
W = at(0x00521050)
check("M5", W.get(0x00521096) == "and ecx, 1" and W.get(0x00521099) == "cmp cx, word ptr [rdi + 0x2f2]" and W.get(0x005210A2) == "test al, 2"
      and W.get(0x005210B0) == "and edx, 0xfffc" and W.get(0x005210B6) == "shl edx, 0xe" and W.get(0x005210B9) == "or edx, eax"
      and W.get(0x005210C9) == "movsx edx, word ptr [rbx + 2]" and W.get(0x005210CD) == "movzx r8d, word ptr [rbx + 6]"
      and W.get(0x005210D5) == "call 0x373060" and callers(0x00373060) == [0x005210D5],
      "the +0x2F2 flag test, the composite key, the direct s16 ordinal, and the one call into 00373060")
T = at(0x00373060)
init = {fa: [S(x) for x in body(fa)] for fa in (0x00372820, 0x00372510)}
check("M6", T.get(0x003730BA) == "movzx ecx, word ptr [rax + 0x38]" and T.get(0x003730C0) == "jge 0x3730dc" and T.get(0x003730CC) == "mov word ptr [rdi + rsi*2], cx"
      and T.get(0x003730D2) == "mov word ptr [rdi + rsi*2], bp" and T.get(0x003730D6) == "or dword ptr [rbx], 0x1000"
      and all(any("0x7fff" in s for s in L2) and any(s.endswith("0xffffefff") for s in L2) for L2 in init.values())
      and callers(0x00371330) == [0x0053C36F, 0x0053C3AD],
      "the +0x38 bound, the bare 0x7FFF store, the flagged store; both initialisers store 0x7FFF and clear 0x1000; 00371330's two callers")
G = at(0x0053AB50)
check("M7", G.get(0x0053B33A) == "movzx eax, word ptr [rcx + 0x34]" and G.get(0x0053B347) == "movzx eax, word ptr [rcx + 0x36]" and G.get(0x0053B354) == "movzx ecx, word ptr [rbx + 0x38]"
      and G.get(0x0053B5B8) == "add rax, 2" and G.get(0x0053B5BC) == "shl rax, 5"
      and G.get(0x0053C308) == "mov ecx, dword ptr [r8 + r15*4 + 0x34]" and G.get(0x0053C320) == "add ecx, 0xc"
      and G.get(0x0053C34C) == "test dword ptr [rcx], 0x1000" and G.get(0x0053C352) == "je 0x53c3c2"
      and G.get(0x0053C366) == "shr edx, 8" and G.get(0x0053C3A4) == "shr edx, 0x12" and G.get(0x0053C369) == "and edx, 0x3ff"
      and G.get(0x0053C386) == "movsx ebx, byte ptr [r13 + 2]" and G.get(0x0053C3CA) == "movsx eax, byte ptr [r13 + 3]"
      and G.get(0x0053CB58) == "imul rcx, rax, 0x290" and G.get(0x0053CB71) == "or edx, 0x6c040000" and G.get(0x0053CC18) == "or rcx, 0x30000000",
      "the three u16 resolutions, the @FTE sum, list -> descriptor -> sub-record, the 0x1000 gate, the two slot ordinals and "
      "their s8 fallbacks, the 0x290 bone scale, the UNPACK tag, the | 0x30000000 row")
V = at(0x0053D4B0)
check("M8", V.get(0x0053D532) == "and edx, 1" and V.get(0x0053D539) == "mov dword ptr [rcx], edx" and V.get(0x0053D55D) == "mov dword ptr [rcx + 4], r8d"
      and V.get(0x0053D568) == "mov eax, dword ptr [rdx + 4]" and V.get(0x0053D56B) == "mov dword ptr [rcx + 8], eax"
      and V.get(0x0053D575) == "mov eax, dword ptr [rdx]" and V.get(0x0053D577) == "mov dword ptr [rcx + 0xc], eax",
      "row {bit 0, A | B != 0, B, A}")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
