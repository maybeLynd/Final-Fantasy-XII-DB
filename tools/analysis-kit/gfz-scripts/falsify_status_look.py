"""Falsification pass 1 on how-a-status-shows-on-a-character (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  H0  section 7 and the notes: the 26 cited body sizes
  H1  section 3: 0046FFA0 (add) and 00470050 (remove) scan the mask's bits 0..13 upward (loop bound 0xE) and store the first set
      index in byte +5, or 0xFF when none is set - fourteen entries, lowest index wins
  H2  section 3: 02B59D70 has one writer image-wide (bounded and linear), 003E7CC0 (7 B); 002EA8E0 reads 0215FD44 and calls it
  H3  the SWE2-EC7-68 note: 0046FBB0 reads the dword count 01F20538 (= 60) and the table 01F20AA0
  H4  the SWE2-EC7-69 note: 003ABD00 indexes [02B3F528] + (ecx & 0xFF) * 0x70, compares the record's first dword with ecx, returns +0x20
  H5  the SWE2-EC7-70 note: 00428940 tail-jumps to 003E5D00 on r9d <= 1 and to 003E5D60 when rcx != 0
  H6  section 4a: the gather 003ABD50 copies record +0x5EC to 02B3F518 and caps the output at six lights
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None

SZ = {0x003E7650: 1566, 0x0046FD00: 615, 0x004703F0: 198, 0x004700E0: 332, 0x00470AA0: 208, 0x00470230: 448, 0x00470780: 798,
      0x00470EB0: 581, 0x00470590: 202, 0x00470B70: 827, 0x00470660: 280, 0x004704C0: 195, 0x003ABD50: 950, 0x0051DC90: 300,
      0x0051E0A0: 145, 0x0051E170: 549, 0x0051DE30: 621, 0x00428CD0: 269, 0x0051E3A0: 362, 0x0046FFA0: 85, 0x00470050: 97,
      0x003E7CC0: 7, 0x002EA8E0: 46, 0x0046FBB0: 60, 0x003ABD00: 26, 0x00428940: 20}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("H0", not bad, "mismatches %s" % bad if bad else "all twenty-six sizes as cited")
lb = {f: txt(f) for f in (0x0046FFA0, 0x00470050)}
check("H1", all(t.count("cmp eax, 0xe") == 2 and "add edx, edx" in t and "mov edx, 0xff" in t and "cmove ecx, edx" in t and "mov byte ptr [r9 + 5], cl" in t for t in lb.values()),
      "both workers scan bits 0..13 upward (bound 0xE) and store the first set index in +5, or 0xFF (cmove) when none is set")
text = next(x for x in SECS if x[0] == ".text")
W = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if 0x02B59D70 in rip(x) and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith(("mov", "and", "or", "set", "inc", "dec", "xor")) and not x.mnemonic.startswith(("movzx", "movsx")):
                W.append((x.address, fa))
    except ValueError:
        continue
raw = blob[text[3]:text[3] + text[4]]
want = {0x02B59D70 - t for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        if base + 4 * kk + d in want:
            cands.add(text[1] + s + 4 * kk)
lw = set()
for pos in cands:
    for L in range(11, 0, -1):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and 0x02B59D70 in rip(x):
            if x.operands[0].type == X86_OP_MEM and not x.mnemonic.startswith(("movzx", "movsx", "cmp", "test")):
                lw.add(x.address)
            break
R = body(0x002EA8E0)
check("H2", [f for _a, f in W] == [0x003E7CC0] and sorted(lw) == [a for a, _f in W] and 0x0215FD44 in rips(0x002EA8E0)
      and any(x.mnemonic in ("call", "jmp") and imm(x) == 0x003E7CC0 for x in R),
      "writers of 02B59D70 %s (linear %s); 002EA8E0 reads 0215FD44 and reaches 003E7CC0" % (["%08X in %08X" % w for w in W], sorted("%08X" % a for a in lw)))
cnt = struct.unpack("<I", blob[OFF(0x01F20538):OFF(0x01F20538) + 4])[0]
check("H3", rips(0x0046FBB0) == {0x01F20538, 0x01F20AA0} and cnt == 60 and txt(0x0046FBB0)[0].startswith("mov r8d, dword ptr"),
      "0046FBB0 reads %s; count %d" % (sorted("%08X" % r for r in rips(0x0046FBB0)), cnt))
H = txt(0x003ABD00)
check("H4", 0x02B3F528 in rips(0x003ABD00) and any("0x70" in s for s in H) and any(s.startswith("cmp dword ptr [rax], ecx") for s in H)
      and any("0x20" in s for s in H), "%s" % H)
F = txt(0x00428940)
check("H5", any(s == "jle 0x3e5d00" for s in F) and any(s == "jmp 0x3e5d60" or s == "jne 0x3e5d60" for s in F), "%s" % F)
G = txt(0x003ABD50)
check("H6", any("+ 0x5ec]" in s for s in G) and 0x02B3F518 in rips(0x003ABD50) and any(s.startswith("cmp") and s.endswith(", 6") for s in G),
      "+0x5EC and 02B3F518; the six-light compare")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
