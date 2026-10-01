"""Falsification pass 1 on fte-fct-texture-colour-tables (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The archive census and
FABLE's uq218-cm-entry-residues controls are carried, not re-run.

  X0  sizes of the bodies the page reads
  X1  @FCT consumer 00504D30: +0x21C / -1; idx < dword [entry + 0x0C], idx < 0x10, sub < 0x10; u16 [entry + idx x 16 + 0x32]
      >> 2 into 003CCB60, stored at +0x140 + idx x 4, retained by 003CD7C0(id, 1); the (idx << 4 | sub) byte into the 20-slot
      map +0x180; 003CCC20's handle at +0x194 + slot x 4
  X2  page selection: 005044D0 = entry + payloadOff (+0x3C) + s8 [+0xBA] x clutBytes; 00504D20 is `mov byte [rcx + 0xBA], dl;
      ret`, with three call sites - 00428D3C and 00428D82 (both inside 00428CD0) and 0042E520
  X3  the builder 0053AB50 is called twice from 0053D780; the frame offsets +0x83B0 / +0x8430 / +0x8530 occur in no other body
  X4  the key selection: s8 [r14 + 0xB8] against byte [rec + 0] over the source's 0xE0 records (0053B3EE..0053B40B);
      00504F00 writes +0xB8
  X5  tables A / B (REFUTES "table B ... indexed by (tableA byte + byte[FOR+0x32]·count)"): table A is read at 3 x selector +
      part; its byte plus byte [source @FOR + 0x32] x s8 [target + 0xB9] indexes table B's pairs (0053B4B6..0053B4EC) - the
      multiplier is the target record's +0xB9 byte (loaded at 0053AB9F), not a count
  X6  +0xB9 is the binder's second selector: its argument, kept when 0 <= v < byte [@FOR + 0x33], else 0 (005050CF..00505116)
  X7  the @FTE seed list byte [+0x30] / bytes [+0x31..] into +0x83B0, the pair halves de-duplicated into +0x83B0 / +0x83D0;
      the record reader ((idx + 2) << 5) + FTE; the PSM or-ed in before the << 0x14 at 0053BFD7
  X8  the 256-slot cache (0x100 bounds in 00521290 / 005210F0); the teardown walks +0x140 (16) and +0x100 (0x20) through
      003CD590 / 003CD5D0 / 00521250
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
at = lambda fa: {x.address: S(x) for x in body(fa)}
txt = lambda fa: [S(x) for x in body(fa)]
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x00504D30: 310, 0x005044D0: 65, 0x00504D20: 7, 0x0053AB50: 9695, 0x00504C40: 214, 0x00521290: 70, 0x005210F0: 250,
      0x00537AA0: 69, 0x00504F00: 582}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("X0", not bad, "mismatches %s" % bad if bad else "all nine sizes as measured")

C = at(0x00504D30)
check("X1", C.get(0x00504D4B) == "mov ecx, dword ptr [rcx + 0x21c]" and C.get(0x00504D6A) == "cmp dword ptr [rax + 0xc], ebx" and C.get(0x00504D73) == "cmp ebx, 0x10"
      and C.get(0x00504D7C) == "cmp r8d, 0x10" and C.get(0x00504DA7) == "movzx r8d, word ptr [rcx + rax*8 + 0x32]" and C.get(0x00504DAF) == "shr r8d, 2"
      and C.get(0x00504DB3) == "call 0x3ccb60" and C.get(0x00504DBD) == "mov dword ptr [rsi + 0x140], eax" and C.get(0x00504DC5) == "call 0x3cd7c0"
      and C.get(0x00504DF1) == "shl bl, 4" and C.get(0x00504E0D) == "cmp rax, 0x14" and C.get(0x00504E3C) == "call 0x3ccc20"
      and C.get(0x00504E41) == "mov dword ptr [rbp + rbx*4 + 0x194], eax" and C.get(0x00504E48) == "mov byte ptr [rbx + rbp + 0x180], dil",
      "the bounds, the colour count into 003CCB60, +0x140 slots, the 20-slot (idx << 4 | sub) map at +0x180, +0x194 handles")
P = at(0x005044D0)
cs = callers(0x00504D20)
check("X2", P.get(0x005044F8) == "movzx edx, word ptr [rax + rcx*8 + 0x32]" and P.get(0x005044FD) == "movsx eax, byte ptr [r8 + 0xba]"
      and P.get(0x00504505) == "imul eax, edx" and P.get(0x00504508) == "add eax, dword ptr [r9 + rcx*8 + 0x3c]"
      and txt(0x00504D20) == ["mov byte ptr [rcx + 0xba], dl", "ret"] and cs == [0x00428D3C, 0x00428D82, 0x0042E520],
      "page = entry + payloadOff + s8 [+0xBA] x clutBytes; the setter's call sites %s - three, two of them in 00428CD0 (the page "
      "counts 00428D3C and then 00428CD0 twice)" % ["%08X" % c for c in cs])
fb = {}
for fa in sorted(sizes):
    if fa == 0x0053AB50 or not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if any(("+ 0x%x]" % d) in x.op_str for d in (0x83B0, 0x8430, 0x8530)):
                fb.setdefault(fa, []).append(S(x))
    except ValueError:
        continue
check("X3", callers(0x0053AB50) == [0x0053DA5B, 0x0053DA94] and not fb,
      "two calls from 0053D780; frame offsets +0x83B0 / +0x8430 / +0x8530 elsewhere: %s" % ({("%08X" % k): v[:1] for k, v in fb.items()} or "none"))
B = at(0x0053AB50)
F = at(0x00504F00)
check("X4", B.get(0x0053B3EE) == "movsx r8d, byte ptr [r14 + 0xb8]" and B.get(0x0053B3F6) == "movzx eax, byte ptr [rbx]" and B.get(0x0053B3FE) == "add rbx, 0xe0"
      and F.get(0x00505044) == "mov byte ptr [rbx + 0xb8], r9b",
      "the 0xE0 record whose byte +0 equals s8 [r14 + 0xB8]; 00504F00 stores +0xB8")
check("X5", B.get(0x0053AB9F) == "movsx eax, byte ptr [rdx + 0xb9]" and B.get(0x0053ABBD) == "mov dword ptr [rbp + 8], eax" and B.get(0x0053ABC0) == "mov r13, rdx"
      and B.get(0x0053B2AD) == "mov r10d, dword ptr [r13 + 0x208]" and B.get(0x0053B4A0) == "mov rax, qword ptr [rbp + 0x98]"
      and B.get(0x0053B4B6) == "movzx r15d, byte ptr [rax + 0x32]" and B.get(0x0053B4BB) == "imul r15d, dword ptr [rbp + 8]"
      and B.get(0x0053B4C9) == "lea rax, [rcx*2]" and B.get(0x0053B4D4) == "add rcx, rax" and B.get(0x0053B4DE) == "movzx eax, byte ptr [rcx + rax]"
      and B.get(0x0053B4E2) == "add eax, r15d" and B.get(0x0053B4E7) == "movzx r10d, byte ptr [rsi + rax*2]" and B.get(0x0053B4EC) == "movzx r11d, byte ptr [rsi + rax*2 + 1]",
      "(REFUTES '·count') pair = B[ A[3 x sel + part] + byte [source @FOR + 0x32] x s8 [target + 0xB9] ]; the multiplier is the "
      "target's +0xB9 byte, loaded at 0053AB9F")
check("X6", F.get(0x005050CF) == "mov byte ptr [rbx + 0xb9], 0xff" and F.get(0x005050DB) == "movzx eax, byte ptr [rdx + 0x33]"
      and F.get(0x005050E8) == "jle 0x5050f6" and F.get(0x005050EC) == "js 0x5050f6" and F.get(0x005050EE) == "mov byte ptr [rbx + 0xb9], cl"
      and F.get(0x0050510B) == "cmove eax, r10d" and F.get(0x00505116) == "mov byte ptr [rbx + 0xb9], al",
      "+0xB9 = the binder's argument when 0 <= v < byte [@FOR + 0x33], else 0")
check("X7", B.get(0x0053B45A) == "movzx r8d, byte ptr [r12 + 0x30]" and B.get(0x0053B470) == "movzx eax, byte ptr [rdx + r12 + 0x31]"
      and B.get(0x0053B480) == "mov byte ptr [rbp + rcx + 0x83b0], al" and B.get(0x0053B508) == "cmp r10d, eax"
      and B.get(0x0053B523) == "mov byte ptr [rbp + rax + 0x83b0], r10b" and B.get(0x0053B563) == "mov byte ptr [rbp + rax + 0x83d0], r11b"
      and B.get(0x0053B5B8) == "add rax, 2" and B.get(0x0053B5BC) == "shl rax, 5" and B.get(0x0053BFD7) == "or r9, r8" and B.get(0x0053BFDA) == "shl r9, 0x14",
      "the seed list, the two de-duplicated pair lists, the (idx + 2) << 5 record reader, the PSM before << 0x14")
T = at(0x00504C40)
check("X8", any("0x100" in s and s.startswith("cmp") for s in txt(0x00521290)) and any("0x100" in s and s.startswith("cmp") for s in txt(0x005210F0))
      and T.get(0x00504C57) == "lea rdi, [rcx + 0x140]" and T.get(0x00504C67) == "cmp ebx, 0x10" and T.get(0x00504CC9) == "lea rbx, [rsi + 0x100]"
      and T.get(0x00504CD0) == "mov edi, 0x20" and {0x003CD590, 0x003CD5D0, 0x00521250} <= {x.operands[0].imm for x in body(0x00504C40) if x.mnemonic == "call"},
      "the 256-slot bound in both cache bodies; the +0x140 x 16 and +0x100 x 0x20 teardown walks")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
