"""Falsification pass 1 on the-handbooks-monster-viewer (OPUS, 2026-09-29), from the shipping image. Every row survives;
the additions are stated in the pass section.

  M0  sizes 001846F0 75, 001846B0 57, 001EB7B0 79, 001EB9C0 114, 001EB940 66, 002EF050 165, 00477F20 261, 004781A0 59,
      004781E0 138, 002EE9C0 343
  M1  section 1: open saves the cubemap intensity 02CB8138 into 01F7F53C and zeroes it; close restores it; both also call
      0018CCF0 (0 on open, 1 on close)
  M2  section 1: 001EB7B0 stores the index at +0x11C and closes an open slot (+0x118 = 0, 002EEB20, +0x130 / +0x120 = -1);
      001EB9C0 requests only when the model id differs from +0x120, with mode 1, weapon ids +0x124, count +0x12C and two
      more words +0x138 / +0x13C; +0x118 = 1 is set only on that path (a missing entry, -1, equals the closed +0x120)
  M3  the loader's only caller: one E8 edge into 002EE9C0 (001EBA05) and no data reference, so mode 0 is never requested
  M4  section 3: the loader stores +0x6E0 = 1 at three sites (body and both attachments)
  M5  section 3: 002EF050 walks the ten slots at 01EEBAB0; +0x6E0 == 0 advances +0x124 by 0215FD40 and wraps at 2 pi;
      0215FD40 has two rip-relative readers (002EEED0, 002EF050) and no rip-relative writer, in uninitialised data
  M6  section 4: 00477F20's mode 0 list via 004781E0 (sorted ascending by +4, after equals, head +0x60, next +2), +0xB2
      from +0x66, frame mode 00229EA0 = byte 02064AD3; mode 3 draws +0x6E0 == 1, else +0x6E0 == 0 (002EF010 reads it,
      -1 -> 0); the owner record (+0x40 index) is dereferenced with no null guard
  M7  section 4: 004781A0 queues key +4 >> 4 with the draw callback 0016D6A0, the folded empty function
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


def raw_backed(va):
    return any(start <= va < start + rawsz for _n, start, size, raw, rawsz in SECS)


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
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]


def eq(m, a, text, target=None):
    g = m.get(a)
    return g is not None and g[0] == text and (target is None or target in g[1])


SZ = {0x001846F0: 75, 0x001846B0: 57, 0x001EB7B0: 79, 0x001EB9C0: 114, 0x001EB940: 66, 0x002EF050: 165, 0x00477F20: 261,
      0x004781A0: 59, 0x004781E0: 138, 0x002EE9C0: 343}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("M0", not bad, "sizes %s" % (bad or "all ten as cited"))
O, C = A(0x001846F0), A(0x001846B0)
check("M1", eq(O, 0x001846FD, "movss xmm0, dword ptr [rip + 0x2b33a33]", 0x02CB8138) and eq(O, 0x00184708, "movss dword ptr [rip + 0x1dfae2c], xmm0", 0x01F7F53C)
      and eq(O, 0x00184710, "movss dword ptr [rip + 0x2b33a20], xmm1", 0x02CB8138) and eq(O, 0x00184720, "xor edx, edx") and eq(O, 0x00184722, "call 0x18ccf0")
      and eq(O, 0x00184736, "jmp 0x1eb7b0") and eq(C, 0x001846C6, "movss xmm0, dword ptr [rip + 0x1dfae6e]", 0x01F7F53C)
      and eq(C, 0x001846CE, "movss dword ptr [rip + 0x2b33a62], xmm0", 0x02CB8138) and eq(C, 0x001846DE, "mov dl, 1") and eq(C, 0x001846E4, "jmp 0x18ccf0"),
      "cubemap intensity saved/zeroed/restored; 0018CCF0 with 0 on open and 1 on close")
V, R = A(0x001EB7B0), A(0x001EB9C0)
check("M2", eq(V, 0x001EB7B9, "mov dword ptr [rcx + 0x11c], edx") and eq(V, 0x001EB7CA, "mov byte ptr [rbx + 0x118], 0") and eq(V, 0x001EB7D1, "call 0x2eeb20")
      and eq(R, 0x001EB9CD, "call 0x1c6320") and eq(R, 0x001EB9D4, "cmp eax, dword ptr [rbx + 0x120]") and eq(R, 0x001EB9DA, "je 0x1eba27")
      and eq(R, 0x001EBA00, "mov edx, 1") and eq(R, 0x001EB9E2, "lea r9, [rbx + 0x124]") and eq(R, 0x001EB9E9, "mov r8d, dword ptr [rbx + 0x12c]")
      and eq(R, 0x001EB9F6, "mov edx, dword ptr [rbx + 0x138]") and eq(R, 0x001EB9DC, "mov edx, dword ptr [rbx + 0x13c]")
      and eq(R, 0x001EBA0A, "mov dword ptr [rbx + 0x130], eax") and eq(R, 0x001EBA20, "mov byte ptr [rbx + 0x118], 1"),
      "index +0x11C, close-then-open; request only on a new model id (mode 1, +0x124 / +0x12C / +0x138 / +0x13C); +0x118 set only then")
text = next(x for x in SECS if x[0] == ".text")
traw = blob[text[3]:text[3] + text[4]]
e8 = [text[1] + k for k in range(len(traw) - 5) if traw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", traw, k + 1)[0] == 0x002EE9C0]
refs = {0x002EE9C0: [], 0x0215FD40: []}
for fa, sz in sizes.items():
    if sz <= 0 or sz > 30000 or not (text[1] <= fa < text[1] + text[4]):
        continue
    for x in md.disasm(blob[OFF(fa):OFF(fa) + sz], fa):
        for t in rip(x):
            if t in refs:
                refs[t].append((fa, x.address, S(x)))
absq = blob.find(struct.pack("<Q", 0x002EE9C0))
check("M3", e8 == [0x001EBA05] and not refs[0x002EE9C0] and absq < 0, "one call edge 001EBA05 (edx 1), no data reference: mode 0 never requested")
L = body(0x002EE430)
sites = [x.address for x in L if S(x) == "mov dword ptr [rax + 0x6e0], 1"]
check("M4", sites == [0x002EE5E6, 0x002EE71A, 0x002EE831], "+0x6E0 = 1 at %s" % ",".join("%08X" % a for a in sites))
T = A(0x002EF050)
w = [r for r in refs[0x0215FD40] if not r[2].startswith("movss xmm")]
check("M5", eq(T, 0x002EF05F, "lea rbx, [rip + 0x1bfca4a]", 0x01EEBAB0) and eq(T, 0x002EF06E, "mov edi, 0xa")
      and eq(T, 0x002EF08C, "cmp dword ptr [rax + 0x6e0], 0") and eq(T, 0x002EF095, "movss xmm2, dword ptr [rip + 0x1e70ca3]", 0x0215FD40)
      and abs(f32(0x01CEBC78) - 6.2831855) < 1e-5 and sorted(r[0] for r in refs[0x0215FD40]) == [0x002EEED0, 0x002EF050]
      and not w and not raw_backed(0x0215FD40),
      "ten slots, +0x6E0 == 0 turntable, 2 pi wrap; step 0215FD40: readers 002EEED0/002EF050 only, uninitialised data")
N, K, Q = A(0x00477F20), A(0x004781E0), A(0x00229EA0 if 0x00229EA0 in sizes else 0x00229EA0)
check("M6", eq(Q, 0x00229EA0, "movsx eax, byte ptr [rip + 0x1e3ac2c]", 0x02064AD3) and eq(N, 0x00477F43, "movsx ecx, byte ptr [rsi + 0x62]")
      and eq(N, 0x00477F6E, "lea rdx, [rip + 0x26b]", 0x004781E0) and eq(N, 0x00477FB5, "mov byte ptr [rax + 0xb2], cl")
      and eq(N, 0x00477FD5, "cmp eax, 3") and eq(N, 0x00477FE5, "cmp eax, 1") and eq(N, 0x00477FFF, "test eax, eax")
      and eq(N, 0x00477FC0, "xor edi, edi") and eq(N, 0x00477FDA, "mov ecx, dword ptr [rdi + 0xa8]")
      and eq(K, 0x00478220, "cmp dword ptr [rdi + 4], ecx") and eq(K, 0x00478223, "jl 0x478232") and eq(K, 0x0047823A, "mov word ptr [rbp + 0x60], ax"),
      "sorted ascending after equals; mode 3 draws +0x6E0 == 1, else == 0; the owner-less entry (edi 0) is dereferenced at +0xA8")
M = A(0x004781A0)
check("M7", eq(M, 0x004781C3, "sar eax, 4") and eq(M, 0x004781C6, "lea rcx, [rip - 0x30ab2d]", 0x0016D6A0) and eq(M, 0x004781D1, "call 0x3a2c80"),
      "mode-1 queue: key +4 >> 4, draw callback 0016D6A0 (the folded empty function)")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
