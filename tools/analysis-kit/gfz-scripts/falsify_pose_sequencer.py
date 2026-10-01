"""Falsification pass 1 on the-pose-sequencer (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The 1,066-block section-7
census (_experiments/evidence/fcp-section7-pose-sequencer) is carried, not re-run.

  Q0  sizes (twenty-one bodies) and every caller set the page states (raw E8/E9 sweep)
  Q1  sections 1-2: the accessors pair +0x400's word +0x0E with the handle +0x450; the 32-entry, 0x40-stride table at 02CA6CA0;
      the handle serial << 8 | slot, serial never 0; the allocator stores n - 1 at +0xC and resets the eight slot arrays
  Q2  section 1: 00477610 indexes and compares with edx (n) - `movzx ecx, dl`, bytes 0F B6 CA - where its siblings use cl
  Q3  section 1 / 3: 004776D0's walk - record = event base + 6 x variant, T = record + 2 + rel + 0x10, sequence = T + off + 2c,
      value = byte [sequence + 5 + 4f], -1 when inactive
  Q4  section 3: 00477370's drop rules, the choiceCount at T - 2, and the random pick 003A6E60(pickParam) with the re-pick flag
  Q5  section 3: 00477480 runs only when 001EDE80 is non-zero and word +0 set, word +2 | [02CA6C98] zero; the end actions
      0 stop, 1 hold, 2 loop; 001EDE80 returns 1 outside half-rate mode
  Q6  section 4: the applier tests track kind 1, calls 004776D0 with the instance's +0x1E4 / +0x1E8, searches 0x28-stride
      groups for id +0x18
  Q7  section 4: 00477750 returns count << 7; 00477E90 resolves and tail-jumps 00504800, which returns width << 16 | height
      from the instance's +0x100 word table
  Q8  section 4b: command 0x1D's arms (0xFD bit 6 of +0x4B7; 0xFE 00428B30(index, 1); 0xFF byte +3 to +0xB8 then 00477610;
      else low nibble / byte +3 / the +0x413 + 1 filter); command 0x1E through 003E6A20
  Q9  section 4b: the activation raiser (event 2, random, only-if-changed, record [022C6F28] + word +0x364 x 0x740) and the
      status raiser (event 0, choice 0, only-if-changed, on +0x33 with a zero third argument); the set-up call with byte +0x5C
  Q10 the appended notes: 003E7450 as described; 00428B30 sets bit 3 on the record named by word +0 and on that record's +8
      child, then walks the child's +8 and +0xA words through 0042EF90 with 0042D810 (sharper than "the +0 / +8 / +0xA
      children take it"); 0040AA20 accumulates +0x24 x [01DFE0BC] (the note omits the time factor)
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


SZ = {0x003E6F50: 32, 0x003E7450: 88, 0x003E6A20: 62, 0x00477370: 265, 0x00477480: 347, 0x004776D0: 117, 0x00477670: 92,
      0x004772E0: 139, 0x00477610: 38, 0x00477750: 330, 0x00477B10: 889, 0x00477E90: 76, 0x00520D30: 190, 0x00520DF0: 50,
      0x00428B30: 265, 0x0040AA20: 138, 0x003714A0: 3387, 0x004775E0: 39, 0x00477640: 41, 0x004778A0: 46, 0x004778D0: 571}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
CALLERS = {0x003E7450: [0x0041DF95, 0x0051E494, 0x00520DDC], 0x004776D0: [0x00371F64], 0x00477610: [0x00520D85],
           0x00477B10: [0x0053C149], 0x003E6A20: [0x00520E16], 0x004772E0: [0x0041FEB3]}
cbad = {("%08X" % t): ["%08X" % c for c in callers(t)] for t, want in CALLERS.items() if callers(t) != want}
check("Q0", not bad and not cbad, "sizes %s; caller sets %s" % (bad or "all 21 as cited", cbad or "as stated (three raisers, one value caller, "
      "one setter caller, one patch-copy caller, one 0x1E door, one allocator call)"))

A = at(0x004772E0)
check("Q1", txt(0x003E6F50)[0] == "mov rdx, qword ptr [rcx + 0x400]" and "movzx eax, word ptr [rdx + 0xe]" in txt(0x003E6F50)
      and at(0x003E6A20).get(0x003E6A20) == "mov r9d, dword ptr [rcx + 0x450]" and A.get(0x00477302) == "cmp eax, 0x20" and A.get(0x004772FE) == "add r8, 0x40"
      and A.get(0x00477327) == "cmp ecx, 0xffffff" and A.get(0x0047732D) == "cmova ecx, r8d" and A.get(0x0047733E) == "shl ecx, 8"
      and A.get(0x00477343) == "lea eax, [r9 - 1]" and A.get(0x00477347) == "mov dword ptr [rdx + 0xc], eax"
      and A.get(0x00477357) == "mov qword ptr [rdx + 0x20], 0xffffffffffffffff" and 0x02CA6CA0 in rips(0x004772E0),
      "S = +0x400 + word +0x0E; handle +0x450; 32 x 0x40 entries at 02CA6CA0; serial << 8 | slot with the wrap to 1; n - 1 at +0xC")
st = blob[OFF(0x00477617):OFF(0x00477617) + 3]
sib = {("%08X" % fa): next(S(x) for x in body(fa) if S(x).startswith("movzx") and "0x" not in S(x)) for fa in (0x004776D0, 0x00477670, 0x00477370)}
check("Q2", st == b"\x0f\xb6\xca" and at(0x00477610).get(0x00477623) == "cmp dword ptr [rcx + 4], edx" and at(0x00477610).get(0x00477632) == "mov dword ptr [rcx + 0xc], eax"
      and all("cl" in s for s in sib.values()),
      "00477610: %s = movzx ecx, dl, compare with edx, store n - 1; siblings %s" % (st.hex(" ").upper(), sib))
V = at(0x004776D0)
check("Q3", V.get(0x00477712) == "lea rcx, [rax + rax*2]" and V.get(0x00477716) == "movzx eax, word ptr [rdx + rcx*2 + 2]" and V.get(0x0047771F) == "add eax, 2"
      and V.get(0x00477729) == "add rdx, 0x10" and V.get(0x00477733) == "lea ecx, [rax + rcx*2]" and V.get(0x0047773B) == "movzx eax, byte ptr [rcx + rax*4 + 5]"
      and V.get(0x00477741) == "or eax, 0xffffffff",
      "record = base + 6 x variant; T = record + 2 + rel + 0x10; sequence = T + off + 2c; value = byte [seq + 5 + 4f]; -1 inactive")
B = at(0x00477370)
check("Q4", B.get(0x004773BB) == "cmp ax, cx" and B.get(0x004773CD) == "cmp byte ptr [r9 + 4], 0" and B.get(0x004773F6) == "cmp byte ptr [r11 + r10 + 0x18], 0"
      and B.get(0x00477400) == "movzx eax, word ptr [rcx + 0xe]" and B.get(0x00477409) == "movzx eax, byte ptr [r11 + r10 + 0x28]"
      and B.get(0x0047744A) == "mov byte ptr [rbx + 0x18], 1" and B.get(0x00477453) == "call 0x3a6e60" and B.get(0x0047746A) == "mov byte ptr [rbx + 0x28], r8b",
      "rel 0xFFFF and enabled gates; the two only-if-changed drops; choiceCount at T - 2 (T - 0x10 + 0xE); the random pick with re-pick")
P = at(0x00477480)
G = txt(0x001EDE80)
check("Q5", P.get(0x0047748F) == "call 0x1ede80" and P.get(0x004774D3) == "movzx eax, word ptr [rdi + 2]" and 0x02CA6C98 in rips(0x00477480)
      and P.get(0x004774E3) == "cmp word ptr [rdi], bx" and P.get(0x00477542) == "cmp word ptr [r10 + 2], ax" and P.get(0x00477579) == "movzx eax, byte ptr [r10 + 4]"
      and P.get(0x004775A5) == "mov byte ptr [rdi + rbx + 0x10], 0" and P.get(0x00477598) == "dec dl" and P.get(0x0047758C) == "mov byte ptr [rdi + rbx + 0x30], 0"
      and at(0x001EDE80).get(0x001EDEB3) == "mov eax, 1" and at(0x001EDE80).get(0x001EDE8B) == "je 0x1edeb3" and at(0x001EDE80).get(0x001EDE94) == "jne 0x1edeb3"
      and {0x01F82E38, 0x01DFE0C0} <= rips(0x001EDE80),
      "the step-count gate, the freeze words, tick against duration, the three end actions; 001EDE80 is 1 outside half-rate")
W = at(0x003714A0)
check("Q6", W.get(0x00371F2E) == "cmp al, 1" and W.get(0x00371F57) == "mov rdx, qword ptr [rax + 0x1e8]" and W.get(0x00371F5E) == "mov ecx, dword ptr [rax + 0x1e4]"
      and W.get(0x00371F64) == "call 0x4776d0" and W.get(0x00371F82) == "add rdx, 0x18" and W.get(0x00371F8D) == "add rdx, 0x28" and W.get(0x00371F86) == "cmp dword ptr [rdx], eax",
      "kind 1; handle and S from +0x1E4 / +0x1E8; the id search over 0x28-stride groups")
check("Q7", at(0x00477750).get(0x0047788C) == "shl edi, 7" and txt(0x00477E90)[-1] == "jmp 0x504800"
      and at(0x00504800).get(0x00504807) == "movzx ecx, word ptr [rcx + rax*2 + 0x100]" and at(0x00504800).get(0x0050482A) == "shl eax, 0x10"
      and at(0x00477B10).get(0x00477CB9) == "movzx ecx, word ptr [r12 + rax*4 + 0xe]" and at(0x00477B10).get(0x00477CC2) == "movzx eax, word ptr [r12 + rax*4 + 0x10]",
      "count x 128; the size lookup returns width << 16 | height via +0x100; the value-indexed source x / y at R + 0x0E / + 0x10")
C = at(0x00520D30)
check("Q8", C.get(0x00520D48) == "or byte ptr [rcx + 0x4b7], 0x40" and C.get(0x00520DA3) == "call 0x428b30" and C.get(0x00520D9E) == "mov edx, 1"
      and C.get(0x00520D71) == "mov byte ptr [rcx + 0xb8], al" and C.get(0x00520D85) == "call 0x477610" and C.get(0x00520DBD) == "and edx, 0xf"
      and C.get(0x00520DC4) == "movsx eax, byte ptr [rbx + 0x413]" and C.get(0x00520DD6) == "xor r9d, r9d" and at(0x00520DF0).get(0x00520E16) == "call 0x3e6a20",
      "0xFD / 0xFE / 0xFF arms; the nibble event, byte +3 choice, the +0x413 + 1 filter, unconditional; 0x1E resets")
R1, R2, SU = at(0x0041DD40), at(0x0051E3A0), at(0x0041FCF0)
check("Q9", R1.get(0x0041DF83) == "mov edx, 2" and R1.get(0x0041DF88) == "mov r8d, 0xff" and R1.get(0x0041DF91) == "lea r9d, [rdx - 1]"
      and R1.get(0x0041DF56) == "movzx eax, word ptr [rbx + 0x364]" and R1.get(0x0041DF67) == "imul rdx, rax, 0x740"
      and R2.get(0x0051E480) == "test byte ptr [rbx + 0x33], al" and R2.get(0x0051E489) == "mov r9d, 1" and R2.get(0x0051E48F) == "xor r8d, r8d" and R2.get(0x0051E492) == "xor edx, edx"
      and SU.get(0x0041FEAC) == "movzx edx, byte ptr [rdi + 0x5c]" and SU.get(0x0041FEB8) == "mov dword ptr [rdi + 0x450], eax",
      "activation: event 2, random, only-if-changed, record by +0x364; status: event 0, choice 0, only-if-changed on +0x33; set-up with +0x5C")
N = at(0x00428B30)
X = at(0x0040AA20)
check("Q10", at(0x003E7450).get(0x003E747E) == "mov dword ptr [rsp + 0x20], r11d" and at(0x003E7450).get(0x003E7493) == "xor r9d, r9d"
      and N.get(0x00428B68) == "shr eax, 3" and N.get(0x00428B7F) == "movzx eax, word ptr [rcx]" and N.get(0x00428BA7) == "or byte ptr [rcx + 0x4b7], dl"
      and N.get(0x00428BAD) == "movzx eax, word ptr [rcx + 8]" and N.get(0x00428BE1) == "xor byte ptr [rbx + 0x4b7], al"
      and N.get(0x00428BDB) == "movzx ecx, word ptr [rbx + 8]" and N.get(0x00428BFE) == "movzx ecx, word ptr [rbx + 0xa]"
      and [a for a, s in N.items() if s == "call 0x42ef90"] == [0x00428BF9, 0x00428C1C] and N.get(0x00428BF2) == "lea rdx, [rip + 0x4c17]"
      and X.get(0x0040AA3A) == "mulss xmm0, dword ptr [rcx + 0x24]" and 0x01DFE0BC in rips(0x0040AA20) and X.get(0x0040AA56) == "or byte ptr [rcx + 0x3f], 1",
      "003E7450 as noted; 00428B30 writes bit 3 on [+0] and its [+8] child, then walks that child's +8 / +0xA via 0042EF90(0042D810); "
      "0040AA20 adds +0x24 x [01DFE0BC] (the note leaves out the time factor)")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
