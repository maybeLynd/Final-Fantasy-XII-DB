"""Falsification pass 1 on CONTRACT-music-control-file-and-bgm-stream (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  M0  section 2: 003EAB90 is 71 B; 0051EDB0 is 6 B, exactly `movsxd rax, ecx` / `jmp rax` (MC-4)
  M1  MC-1 as qualified: 02B5E0D0 has one store image-wide (003EAB78; bounded and linear agree); the binder 003EAB60 passes
      ecx = 9, edx = 0x20, r8 = 003EAB90 to 0051ED10 and stores rax without reading the old pointer
  M2  MC-2: 003EAB60 has no call site; its one inbound edge is the tail-jump at 00379D32
  M3  MC-5: 003EAB9A..003EABA7 is the biased signed divide by 128, 003EABAF `jle` skips when the count is 0, 003EABBA `test ecx, ecx`
      / `je` skips a zero word, and 003EABBE adds the table's low 32 bits (`add ecx, r9d`) before the store
  M4  MC-6: 003EB0D0 walks byte +0x31 at stride 0x38 with bound `cmp ecx, 1` (one iteration)
  M5  MC-7: 003EAE2E stores the file size at +0x24, 003EAE31 compares it with +0x10 and a conditional branch guards the store
      to +0x10 at 003EAE36; the cursor is `idiv dword ptr [rbx + 0x10]` (003EAFB1)
  M6  MC-8 and section 3: the reset 003EB050 stores requestId -1, word 0x4000 at +0x31 (so +0x32 = 0x40) and byte 0x7F at +0x33;
      the play setup 003EB100 stores kind 0x24 at +0x1C
"""
import io, os, struct
from array import array
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
body = lambda fa, n=None: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
TBL = 0x02B5E0D0

T = [S(x) for x in md.disasm(blob[OFF(0x0051EDB0):OFF(0x0051EDB0) + 6], 0x0051EDB0)]
check("M0", sizes[0x003EAB90] == 71 and sizes[0x0051EDB0] == 6 and T == ["movsxd rax, ecx", "jmp rax"], "71 B; trampoline %s" % T)
st, edges = [], []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if TBL in rip(x) and x.operands[0].type == X86_OP_MEM:
                st.append(x.address)
            if x.mnemonic in ("call", "jmp") and imm(x) == 0x003EAB60:
                edges.append((x.address, x.mnemonic))
    except ValueError:
        continue
raw = blob[text[3]:text[3] + text[4]]
want = {TBL - t for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        if base + 4 * kk + d in want:
            cands.add(text[1] + s + 4 * kk)
lin_st = []
for pos in cands:
    for L in range(11, 0, -1):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and TBL in rip(x):
            if x.operands[0].type == X86_OP_MEM:
                lin_st.append(x.address)
            break
Bd = body(0x003EAB60, 36)
check("M1", st == [0x003EAB78] and sorted(set(lin_st)) == [0x003EAB78] and at(Bd, 0x003EAB64) == "mov edx, 0x20" and at(Bd, 0x003EAB70) == "lea ecx, [rdx - 0x17]"
      and rip(Bd[0x003EAB69]) == [0x003EAB90] and at(Bd, 0x003EAB73) == "call 0x51ed10" and not any(TBL in rip(x) for a, x in Bd.items() if a != 0x003EAB78),
      "stores to 02B5E0D0: bounded %s, linear %s; binder (9, 0x20, 003EAB90) -> 0051ED10, no read of the old pointer"
      % (["%08X" % a for a in st], sorted({"%08X" % a for a in lin_st})))
check("M2", edges == [(0x00379D32, "jmp")], "edges into 003EAB60: %s" % ["%08X %s" % e for e in edges])
R = body(0x003EAB90)
check("M3", [at(R, a) for a in (0x003EAB9A, 0x003EAB9E, 0x003EABA1, 0x003EABA2, 0x003EABA5, 0x003EABA7)] ==
      ["mov eax, dword ptr [r8 + 4]", "add eax, 0x7f", "cdq", "and edx, 0x7f", "add eax, edx", "sar eax, 7"]
      and at(R, 0x003EABAF) == "jle 0x3eabd6" and at(R, 0x003EABBA) == "test ecx, ecx" and at(R, 0x003EABBC) == "je 0x3eabcc"
      and at(R, 0x003EABBE) == "add ecx, r9d" and at(R, 0x003EABC1) == "mov dword ptr [rax + r8], ecx", "biased divide, zero skip, 32-bit add in place")
C = body(0x003EB0D0)
check("M4", at(C, 0x003EB0E0) == "cmp byte ptr [rax], 0" and at(C, 0x003EB0E7) == "add rax, 0x38" and at(C, 0x003EB0EB) == "cmp ecx, 1"
      and rip(C[0x003EB0D2]) == [0x02B5E111], "stride 0x38, bound 1, starting at +0x31")
P = body(0x003EADE0)
br = [a for a in P if 0x003EAE31 < a < 0x003EAE36 and P[a].mnemonic.startswith("j")]
check("M5", at(P, 0x003EAE2E) == "mov dword ptr [rbx + 0x24], eax" and at(P, 0x003EAE31) == "cmp eax, dword ptr [rbx + 0x10]" and br
      and at(P, 0x003EAE36) == "mov dword ptr [rbx + 0x10], eax" and at(P, 0x003EAFB1) == "idiv dword ptr [rbx + 0x10]",
      "file size -> +0x24; %s guards the clamp store; cursor %s" % (at(P, br[0]) if br else "?", at(P, 0x003EAFB1)))
Z, Y = body(0x003EB050), body(0x003EB100)
check("M6", rip(Z[0x003EB060]) == [0x02B5E0E0] and at(Z, 0x003EB060).endswith("0xffffffff") and rip(Z[0x003EB06A]) == [0x02B5E111] and at(Z, 0x003EB06A).endswith("0x4000")
      and rip(Z[0x003EB073]) == [0x02B5E113] and at(Z, 0x003EB073).endswith("0x7f") and rip(Y[0x003EB10C]) == [0x02B5E0FC] and at(Y, 0x003EB10C).endswith("0x24"),
      "requestId -1; +0x31 word 0x4000 (+0x32 = 0x40); +0x33 = 0x7F; kind 0x24 at +0x1C")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
