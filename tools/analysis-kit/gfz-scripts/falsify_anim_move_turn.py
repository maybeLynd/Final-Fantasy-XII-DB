"""Falsification pass 1 on how-an-animation-moves-and-turns-a-character-toward-its-target (OPUS, 2026-09-29), from the
shipping image. Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The staged
profile census is carried, not re-run.

  A0  sizes: 00520C10 61, 003E6340 657, 003AED70 371, 003AEF90 655, 003AF220 136, 003E6EF0 84, 0041F2F0 65; the caller chain
      00520C10 -> 003E6340 -> 003AED70 and 003E6EF0 -> 003AF220 -> 003AEF90
  A1  section 1: the handler needs a motion section (+0x370) and passes word +2; the builder asks 0041F2F0(record, ..) for a
      zeroed 64-byte view, compares x / z with +0x140 / +0x148, turns through 00424370 from +0x180, tests +0x2AF == 3, and
      queues on +0x550 (003E6589)
  A2  section 2: 003AF2B0 allocates 0x3000 = 128 x 0x60 at [02B3F530] once and clears 02B3F538 / 02B3F53C / 02B3F540; the take
      copies 0x20 bytes to +0x20, stores the heading signs +-1.0 at +8 / +0xC, sets bytes +1 and +2, and starts +4 at -1
  A3  section 3: the @FRM window keeps body = entry + 0x30 at +0x378 and the table = body + dword [body + 8] (entry + 0x38)
  A4  section 4: the consumer's frame counter +4 against duration x [01DFE0B4] (unlink past it), the move window against
      moveFrames x the same word, the curve indexed by counter / word; mode 0x16 from list +0x10, dropped with none
  A5  section 4: 003AF220 clamps the summed move to min(maxStep, |move|) along its own direction
  A6  section 2 (REFUTES "003AED70 refuses while either switch is up or the list is disabled"): the take tests one global
      switch, 02B3F53C, with the list's +0x28 (non-zero refuses) and +0 (zero refuses); the other switch, 02B3F540, is
      tested by the consumer 003AEF90 (003AEFA5), so with it up requests still queue but nothing advances or frees
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
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x00520C10: 61, 0x003E6340: 657, 0x003AED70: 371, 0x003AEF90: 655, 0x003AF220: 136, 0x003E6EF0: 84, 0x0041F2F0: 65}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("A0", not bad and callers(0x003E6340) == [0x00520C3B] and 0x003E6589 in callers(0x003AED70) and callers(0x003AEF90) == [0x003AF239]
      and callers(0x003AF220) == [0x003E6F2A],
      "sizes %s; the chain command -> builder -> take, door -> clamp -> consumer" % (bad or "all seven as cited"))
H, B = at(0x00520C10), at(0x003E6340)
V = txt(0x0041F2F0)
check("A1", H.get(0x00520C2A) == "cmp qword ptr [rax + 0x370], 0" and H.get(0x00520C34) == "movzx edx, word ptr [rdi + 2]"
      and B.get(0x003E6390) == "call 0x41f2f0" and sum(1 for s in V[:10] if s.startswith("mov qword ptr [r8")) == 8
      and B.get(0x003E639A) == "movss xmm6, dword ptr [rbx + 0x140]" and B.get(0x003E63AE) == "movss xmm0, dword ptr [rbx + 0x148]"
      and B.get(0x003E63BB) == "je 0x3e65a8" and B.get(0x003E6406) == "call 0x424370" and B.get(0x003E63E8) == "lea rcx, [rbx + 0x180]"
      and B.get(0x003E64FD) == "cmp byte ptr [rbx + 0x2af], 3" and B.get(0x003E6554) == "lea rcx, [rbx + 0x550]" and B.get(0x003E6589) == "call 0x3aed70",
      "motion-section gate and word +2; the zeroed 64-byte view; the x / z sameness exit; +0x180 turn; +0x2AF; queued on +0x550")
P, T = at(0x003AF2B0), at(0x003AED70)
check("A2", P.get(0x003AF2CA) == "mov ecx, 0x3000" and P.get(0x003AF2E7) == "mov ecx, 0x80" and P.get(0x003AF2F3) == "lea rax, [rax + 0x60]"
      and {0x02B3F530, 0x02B3F538, 0x02B3F53C, 0x02B3F540} <= rips(0x003AF2B0)
      and T.get(0x003AEDBF) == "movups xmmword ptr [rcx + 0x20], xmm0" and T.get(0x003AEDDC) == "movups xmmword ptr [rcx + 0x30], xmm1"
      and T.get(0x003AEDD7) == "mov word ptr [rcx], 0x101" and T.get(0x003AEDE3) == "mov byte ptr [rcx + 2], r10b"
      and T.get(0x003AEDEA) == "mov dword ptr [rcx + 4], 0xffffffff" and T.get(0x003AEDFC) == "mov dword ptr [rcx + 8], 0x3f800000"
      and T.get(0x003AEE20) == "mov dword ptr [rcx + 0xc], 0xbf800000",
      "128 x 0x60 once; serial and two switches cleared; the request copy, the sign pair, bytes +1 / +2, counter from -1")
W = {x.address: S(x) for x in md.disasm(blob[OFF(0x0041D318):OFF(0x0041D318) + 0x56], 0x0041D318)}
check("A3", W.get(0x0041D34F) == "mov edx, 0x4d524640" and W.get(0x0041D35C) == "add eax, 0x30" and W.get(0x0041D35F) == "mov dword ptr [rsi + 0x378], eax"
      and W.get(0x0041D365) == "mov ecx, dword ptr [rbx + 0x38]" and W.get(0x0041D36C) == "add eax, ecx",
      "'@FRM'; body = entry + 0x30; table = body + dword [entry + 0x38] = body + dword [body + 8]")
C = at(0x003AEF90)
check("A4", C.get(0x003AF054) == "inc dword ptr [rbx + 4]" and C.get(0x003AF064) == "imul eax, dword ptr [r8]" and C.get(0x003AF06F) == "cmp r10d, eax"
      and C.get(0x003AF07C) == "mov byte ptr [rbx], 0" and C.get(0x003AF08A) == "movzx ecx, word ptr [r8 + 4]" and C.get(0x003AF08F) == "imul ecx, r9d"
      and C.get(0x003AF0A3) == "div r9d" and C.get(0x003AF0A6) == "movzx eax, word ptr [rsi + rax*2]" and 0x01DFE0B4 in rips(0x003AEF90)
      and C.get(0x003AEFF8) == "cmp ax, 0x16" and C.get(0x003AEFFE) == "mov r8, qword ptr [rdi + 0x10]" and C.get(0x003AF00F) == "mov byte ptr [rbx], r8b",
      "counter vs duration x [01DFE0B4] with unlink; move window vs moveFrames x the word; curve by counter / word; mode 0x16 from +0x10")
L = at(0x003AF220)
check("A5", L.get(0x003AF271) == "call 0x861f14" and L.get(0x003AF27F) == "call 0x380800" and L.get(0x003AF287) == "minss xmm7, xmm6" and L.get(0x003AF297) == "mulps xmm1, xmm0",
      "|move| (sqrt), the direction normalised, scaled by min(maxStep, |move|)")
check("A6", T.get(0x003AED70) == "mov eax, dword ptr [rcx + 0x28]" and T.get(0x003AED76) == "or eax, dword ptr [rip + 0x27907c0]" and T.get(0x003AED81) == "cmp dword ptr [rcx], eax"
      and 0x02B3F53C in rips(0x003AED70) and 0x02B3F540 not in rips(0x003AED70)
      and C.get(0x003AEFA5) == "cmp dword ptr [rip + 0x2790595], eax" and 0x02B3F540 in rips(0x003AEF90) and C.get(0x003AEFC2) == "jne 0x3af20f",
      "(REFUTES 'either switch') the take tests 02B3F53C and the list's +0x28 / +0; 02B3F540 gates the consumer instead")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
