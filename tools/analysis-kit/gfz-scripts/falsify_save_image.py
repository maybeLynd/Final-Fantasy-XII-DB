"""Falsification pass 1 on CONTRACT-save-image-pipeline (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  G0  section 2: 35 / 50 / 8 / 8 / 8 / 122 / 161 B
  G1  SV-1: the getters and copies address 02164280 / 021BA940 / 02211000 / 022676C0, three gaps of 0x566C0 against an image of 0x56690
  G2  SV-2: each copy loops 0xACD times over sixteen movups (eight loads, eight stores, 0x80 bytes) and then copies sixteen more
      (002EF5E3/002EF5E6, 002EF70C/002EF70F); 0xACD * 0x80 + 0x10 = 0x56690
  G3  SV-3: exactly six instructions load the immediate 0x56690: 002EF5FD, 002EF65D, 002EF718, 0057E42F, 00581117, 00581F2F
      (function-bounded), and the dword occurs exactly six times in .text (raw), so no unlisted site exists
  G4  SV-4: 022676C0 is referenced once image-wide (002EF570), and the others 4 / 2 / 3 times (both instruments)
  G5  SV-5: 002EF5F0 memsets and tail-jumps to 0016D6A0; 002EF650 memsets, calls 0016D6A0, 00253A80, 002EF2D0 and tail-jumps to
      00238A80; 002EF650's callers are 0022B6E0, 00280140, 00394130 and 002EF5F0's only caller is 003601D0
  G6  SV-6: 002EF690 calls 00236760 before the copy and tail-jumps to 0020E540 with ecx = that bit, rdx = 02211000, r8d = 0x56690;
      00236760 is five instructions returning bit 12 of dword [[02EBF190] + 4]
"""
import collections, io, os, struct
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
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
F = [0x002EF5F0, 0x002EF650, 0x002EF640, 0x002EF620, 0x002EF630, 0x002EF570, 0x002EF690]
check("G0", [sizes[f] for f in F] == [35, 50, 8, 8, 8, 122, 161], "%s" % [sizes[f] for f in F])
BUF = [0x02164280, 0x021BA940, 0x02211000, 0x022676C0]
gets = [rip(body(f)[f])[0] for f in (0x002EF640, 0x002EF620, 0x002EF630)]
check("G1", gets == BUF[:3] and rip(body(0x002EF570)[0x002EF570]) == [BUF[3]] and [BUF[k + 1] - BUF[k] for k in range(3)] == [0x566C0] * 3 and 0x566C0 - 0x56690 == 48,
      "buffers %s; gaps %s; padding 48" % (["%08X" % b_ for b_ in BUF], [hex(BUF[k + 1] - BUF[k]) for k in range(3)]))


def loop(fa, lo, hi, tail):
    I = body(fa)
    mv = [I[a] for a in sorted(I) if lo <= a <= hi and I[a].mnemonic == "movups"]
    ld = sum(1 for x in mv if x.operands[1].type == X86_OP_MEM); st = sum(1 for x in mv if x.operands[0].type == X86_OP_MEM)
    cnt = next(imm2 for x in I.values() for imm2 in [o.imm for o in x.operands if o.type == X86_OP_IMM] if imm2 == 0xACD)
    return ld, st, cnt, [S(I[a]) for a in tail]


b1 = loop(0x002EF570, 0x002EF590, 0x002EF5E1, (0x002EF5E3, 0x002EF5E6))
b2 = loop(0x002EF690, 0x002EF6B1, 0x002EF70A, (0x002EF70C, 0x002EF70F))
check("G2", b1[:3] == (8, 8, 0xACD) and b2[:3] == (8, 8, 0xACD) and b1[3][0].startswith("movups xmm0") and b1[3][1].startswith("movups xmmword ptr [rcx]")
      and b2[3][1].startswith("movups xmmword ptr [r8]") and 0xACD * 0x80 + 0x10 == 0x56690,
      "backup loop %s, submission loop %s; tails %s / %s" % (b1[:3], b2[:3], b1[3], b2[3]))
raw = blob[text[3]:text[3] + text[4]]
rawhits = raw.count(struct.pack("<I", 0x56690))
ld = set()
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if any(o.type == X86_OP_IMM and o.imm == 0x56690 for o in x.operands):
                ld.add((x.address, x.mnemonic))
    except ValueError:
        continue
loads = sorted(a for a, m in ld if m == "mov")
check("G3", loads == [0x002EF5FD, 0x002EF65D, 0x002EF718, 0x0057E42F, 0x00581117, 0x00581F2F] and rawhits == len(ld) == 6,
      "mov-immediate 0x56690 at %s; other uses %s; raw dword occurrences in .text %d" % (["%08X" % a for a in loads], sorted("%08X %s" % o for o in ld if o[1] != "mov"), rawhits))
refs = collections.defaultdict(set)
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            for t in rip(x):
                if t in BUF:
                    refs[t].add(x.address)
    except ValueError:
        continue
want = {b_ - t: b_ for b_ in BUF for t in (0, 1, 2, 4)}
lin = collections.defaultdict(set)
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        v = base + 4 * kk + d
        if v in want:
            lin[want[v]].add(text[1] + s + 4 * kk)
cnt = [len(refs[b_]) for b_ in BUF]
check("G4", cnt == [4, 2, 3, 1] and [len(lin[b_]) for b_ in BUF] == cnt and refs[BUF[3]] == {0x002EF570},
      "references active / staging / submission / backup: bounded %s, linear %s; the backup's one %s" % (cnt, [len(lin[b_]) for b_ in BUF], ["%08X" % a for a in refs[BUF[3]]]))
C1, C2 = body(0x002EF5F0), body(0x002EF650)
callers = collections.defaultdict(list)
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.mnemonic in ("call", "jmp") and imm(x) in (0x002EF5F0, 0x002EF650):
                callers[imm(x)].append(fa)
    except ValueError:
        continue
check("G5", at(C1, 0x002EF603) == "call 0x861ec0" and at(C1, 0x002EF60E) == "jmp 0x16d6a0" and at(C2, 0x002EF663) == "call 0x861ec0"
      and [at(C2, a) for a in (0x002EF66A, 0x002EF66F, 0x002EF674, 0x002EF67D)] == ["call 0x16d6a0", "call 0x253a80", "call 0x2ef2d0", "jmp 0x238a80"]
      and sorted(set(callers[0x002EF650])) == [0x0022B6E0, 0x00280140, 0x00394130] and callers[0x002EF5F0] == [0x003601D0],
      "compound callers %s (sites %d); bare-clear callers %s" % (["%08X" % f for f in sorted(set(callers[0x002EF650]))], len(callers[0x002EF650]), ["%08X" % f for f in callers[0x002EF5F0]]))
G = body(0x002EF690); Z = list(md.disasm(blob[OFF(0x00236760):OFF(0x00236760) + 17], 0x00236760))
check("G6", at(G, 0x002EF696) == "call 0x236760" and at(G, 0x002EF69B) == "mov ebx, eax" and at(G, 0x002EF718) == "mov r8d, 0x56690"
      and rip(G[0x002EF71E]) == [0x02211000] and at(G, 0x002EF725) == "mov ecx, ebx" and at(G, 0x002EF72C) == "jmp 0x20e540"
      and [S(x) for x in Z] == ["mov rax, qword ptr [rip + 0x2c88a29]", "mov eax, dword ptr [rax + 4]", "shr eax, 0xc", "and eax, 1", "ret"],
      "selector first, then the copy, then jmp 0020E540(bit, 02211000, 0x56690); 00236760 %s" % [S(x) for x in Z])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
