"""Falsification pass 1 on ftr-node-table (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The 1,066-file archive
census (members/ftr_entry_census.py) and FABLE's parent-tree controls are carried, not re-run.

  N0  sizes of the bodies the page reads whole
  N1  section 2: the sizer 003712E0 computes align16((count * 0x149 + u16 [entry + 0x38]) * 2) and adds its fifth argument
  N2  section 2: the binder writes u16 count to +0x88, entry +0x30 to +0x8A, coreBytes to +0x90, -1 then the matched index
      of the 0x30-stride name table [02AD9E30] to +0xB0; the FCP tail copy calls 00861EBA with core + coreBytes
  N3  section 2 table (REFUTES "+0x80 arena handle of the entry (0020E620 of the 00409A30 lookup)", "+0x84 resolved pointer",
      "+0x94 tail pointer"): 0020E620 subtracts the arena base [01F83530]; the 00409A30 lookup is stored at +0x1C; +0x80 is
      0020E620 of the binder's fifth argument (the caller's core block), +0x84 is 0020E620 of 003AB7F0's live resolution,
      +0x94 is 0020E620 of core + coreBytes - three dword arena offsets, no pointer
  N4  section 1 flag table: bit 30 skips a u16; 0x200100 gates the rich arm, else 0046D110; bits 23-25 -> +0x30 / +0x34 /
      +0x38; bits 26-28 -> the vec3 into 0046D560; 004094D0's bit 21 fans 16 u16s
  N5  section 1 flag table, an omission: in the rich arm bits 31 and 22 each skip one more u16 (0040936A-00409375,
      0040937D-00409385), and 004094D0 skips bit 31's u16 too (004094F5-004094FB)
  N6  section 1: 00373DC0 builds identities at +0x1F0 / +0x230 and clears +0x270..+0x27C
  N7  section 1 correction box: the parent (bits 12-23, all-ones = root) to record +0x270, first-child +0x274, next-sibling
      +0x272, a root joining record 0's sibling chain (00372B15..00372B99)
  N8  section 3 (REFUTES "when dword[entry + 4] != 2 the binder runs a second loop"): kind 0 goes to 00372CBE (the 0x4C
      loop); any other non-2 kind goes to 00372E84, which builds no records and only fills the 0x7FFF override slots
  N9  section 2: 003E1C50 indexes [022C6F28] by +0x68 / +0x6C x 0x740 gated on +0x284, rebases +0x70 / +0x74 / +0x78 through
      0020E600 / 0020E620, and calls 0040EEA0, 00415A80 and 00421D20
  N10 section 1 correction box (REFUTES "71 functions stride 0x290 - imul290.txt"): 55 listed bodies multiply by 0x290; the
      16 more in imul290.txt carry 0x290 as a stack frame, a size or an offset, not a stride
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
IMUL290 = os.path.join(ROOT, "FFXII TZA", "_index", "candidates", "uq218-cm-entry-residues", "imul290.txt")
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
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None

SZ = {0x003712E0: 69, 0x00372820: 1844, 0x00409300: 451, 0x004094D0: 200, 0x003713C0: 215, 0x00373DC0: 221, 0x004095A0: 8,
      0x003E1C50: 2992, 0x0020E600: 10, 0x0020E620: 9}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("N0", not bad, "mismatches %s" % bad if bad else "all ten sizes as measured")

Z = at(0x003712E0)
check("N1", Z.get(0x003712FE) == "imul ecx, dword ptr [rax + 0xc], 0x149" and Z.get(0x00371305) == "movzx eax, word ptr [rax + 0x38]"
      and Z.get(0x0037130B) == "lea eax, [rcx*2 + 0xf]" and Z.get(0x00371318) == "and eax, 0xfffffff0" and Z.get(0x0037131B) == "add eax, dword ptr [rsp + 0x50]",
      "align16((count x 0x149 + u16 +0x38) x 2) + the fifth argument")

B = at(0x00372820)
check("N2", B.get(0x0037295B) == "mov word ptr [rsi + 0x88], cx" and B.get(0x00372957) == "movzx ecx, word ptr [rbp + 0xc]"
      and B.get(0x003729FD) == "movzx ecx, word ptr [r15 + 0x30]" and B.get(0x00372A02) == "mov word ptr [rsi + 0x8a], cx"
      and B.get(0x00372969) == "mov dword ptr [rsi + 0x90], ebx" and B.get(0x003728A8) == "mov dword ptr [rsi + 0xb0], r13d"
      and B.get(0x003728F7) == "mov dword ptr [rsi + 0xb0], r9d" and 0x02AD9E30 in rips(0x00372820) and B.get(0x003728CA) == "shl r8, 4"
      and B.get(0x003729BD) == "call 0x861eba" and B.get(0x00372991) == "add eax, dword ptr [rsi + 0x90]",
      "+0x88 count, +0x8A entry +0x30, +0x90 coreBytes, +0xB0 name index (stride 3 << 4 = 0x30), the tail copy at core + coreBytes")

H = [S(x) for x in body(0x0020E620)]
check("N3", H[0] == "sub ecx, dword ptr [rip + 0x1d74f0a]" and rips(0x0020E620) == {0x01F83530} and rips(0x0020E600) == {0x01F83530}
      and B.get(0x0037287A) == "call 0x409a30" and B.get(0x00372881) == "mov dword ptr [rsi + 0x1c], eax"
      and B.get(0x00372935) == "mov rcx, qword ptr [rsp + 0x70]" and B.get(0x00372944) == "call 0x20e620" and B.get(0x00372951) == "mov dword ptr [rsi + 0x80], eax"
      and B.get(0x00372977) == "call 0x3ab7f0" and B.get(0x0037297F) == "call 0x20e620" and B.get(0x00372986) == "mov dword ptr [rsi + 0x84], eax"
      and B.get(0x0037299A) == "call 0x20e620" and B.get(0x003729A9) == "mov dword ptr [rsi + 0x94], eax",
      "(REFUTES) the 00409A30 lookup goes to +0x1C; +0x80 / +0x84 / +0x94 are dword arena offsets (x - [01F83530]) of the "
      "caller's core block, its live resolution and core + coreBytes")

C = at(0x00409300)
D = at(0x004094D0)
check("N4", C.get(0x0040934E) == "bt edx, 0x1e" and C.get(0x00409358) == "and eax, 0x200100" and C.get(0x00409428) == "call 0x46d110"
      and [C.get(a) for a in (0x00409392, 0x004093A9, 0x004093C0)] == ["test dword ptr [rbx + 4], 0x800000", "test dword ptr [rbx + 4], 0x1000000", "test dword ptr [rbx + 4], 0x2000000"]
      and [C.get(a) for a in (0x004093A6, 0x004093BD, 0x004093D4)] == ["mov dword ptr [rdi + 0x30], ecx", "mov dword ptr [rdi + 0x34], ecx", "mov dword ptr [rdi + 0x38], ecx"]
      and [C.get(a) for a in (0x004093E3, 0x004093F6, 0x00409409)] == ["bt ecx, 0x1a", "bt ecx, 0x1b", "bt ecx, 0x1c"] and C.get(0x0040941B) == "call 0x46d560"
      and D.get(0x004094FF) == "bt edx, 0x15" and D.get(0x00409589) == "cmp rdx, 0x26" and D.get(0x00409509) == "mov edx, 6",
      "bit 30 skip, the 0x200100 gate, bits 23-25 -> +0x30/+0x34/+0x38, bits 26-28 -> 0046D560, bit 21's 16-index fan")
check("N5", C.get(0x00409368) == "test edx, edx" and C.get(0x00409375) == "cmovns rax, rcx" and C.get(0x00409379) == "add rax, 0x20"
      and C.get(0x0040937D) == "bt edx, 0x16" and C.get(0x00409385) == "cmovae rdx, rax" and D.get(0x004094F5) == "test edx, edx" and D.get(0x004094FB) == "cmovns r10, rcx",
      "(OMISSION) bit 31 (sign test) and bit 22 each skip one u16 in the rich arm, after bit 21's 16 (add 0x20); 004094D0 skips bit 31's")
I = at(0x00373DC0)
check("N6", I.get(0x00373DC9) == "add rcx, 0x1f0" and I.get(0x00373DD5) == "lea rcx, [rbx + 0x230]"
      and all(any(s.startswith("mov %s ptr [rbx + 0x%x]" % (w, o)) for s in I.values()) for w, o in (("word", 0x270), ("word", 0x272), ("word", 0x274), ("word", 0x276), ("dword", 0x278), ("word", 0x27C))),
      "identities at +0x1F0 / +0x230; +0x270..+0x27C cleared")
check("N7", B.get(0x00372B1A) == "and eax, 0xfff000" and B.get(0x00372B26) == "or ecx, 0xffffffff" and B.get(0x00372B34) == "mov word ptr [rbx + 0xb8], cx"
      and B.get(0x00372B45) == "movzx eax, word ptr [rbp + 0x272]" and B.get(0x00372B67) == "movzx eax, word ptr [rcx + rbp + 0x274]"
      and B.get(0x00372B99) == "mov word ptr [rcx + rbp + 0x272], di" and B.get(0x00372C9D) == "add rbx, 0x290",
      "parent to +0xB8 of rbx (= record +0x270), first-child +0x274, next-sibling +0x272, roots on record 0's chain")
check("N8", B.get(0x003729DD) == "mov eax, dword ptr [rax + 4]" and B.get(0x003729EE) == "je 0x372cbe" and B.get(0x003729F7) == "jne 0x372e84"
      and B.get(0x00372CC4) == "lea rdi, [r15 + 0x30]" and B.get(0x00372DB6) == "add rdi, 0x4c"
      and B.get(0x00372EA8) == "jne 0x372ee7" and B.get(0x00372F2D) == "mov edx, 0x7fff" and B.get(0x00372F45) == "and dword ptr [rsi], 0xffffefff",
      "(REFUTES '!= 2 -> second loop') kind 0 -> 00372CBE (0x4C stride from +0x30); other non-2 kinds -> 00372E84, no records, "
      "only the 0x7FFF slot fill and the 0x1000 clear")
E = at(0x003E1C50)
callees = {imm(x) for x in body(0x003E1C50) if x.mnemonic in ("call", "jmp") and imm(x)}
check("N9", E.get(0x003E1C7A) == "movzx eax, word ptr [rdi + 0x68]" and E.get(0x003E1C8C) == "imul rcx, rax, 0x740" and E.get(0x003E1CD9) == "movzx eax, word ptr [rdi + 0x6c]"
      and 0x022C6F28 in rips(0x003E1C50) and E.get(0x003E1C9A) == "cmp dword ptr [rcx + 0x284], ebx"
      and E.get(0x003E1CAB) == "mov dword ptr [rdi + 0x70], eax" and E.get(0x003E1CC3) == "mov dword ptr [rdi + 0x78], eax" and E.get(0x003E1D0C) == "mov dword ptr [rdi + 0x74], eax"
      and {0x0040EEA0, 0x00415A80, 0x00421D20, 0x0020E600, 0x0020E620} <= callees,
      "the 0x740 index on [022C6F28] gated +0x284; +0x70 / +0x74 / +0x78 rebased; the three helpers called")

theirs = {int(l.split()[1], 16) for l in io.open(IMUL290, encoding="utf-8") if l.strip()}
text = next(x for x in SECS if x[0] == ".text")
mine, other = set(), {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        ins = list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
    except ValueError:
        continue
    if any(x.mnemonic == "imul" and x.op_str.endswith(", 0x290") for x in ins):
        mine.add(fa)
    elif fa in theirs:
        other[fa] = [S(x) for x in ins if "0x290" in x.op_str][:1]
frames = [fa for fa, s in other.items() if s and s[0].startswith(("sub rsp", "add rsp"))]
check("N10", len(theirs) == 71 and len(mine) == 55 and mine <= theirs and len(theirs - mine) == 16 and len(frames) >= 1,
      "(REFUTES '71 functions stride 0x290') %d listed bodies multiply by 0x290, all inside imul290.txt's %d; the other %d use "
      "0x290 otherwise (%d as a stack frame), e.g. %s" % (len(mine), len(theirs), len(theirs - mine), len(frames),
                                                           ["%08X %s" % (a, other[a][0]) for a in sorted(other)[:3] if other[a]]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
