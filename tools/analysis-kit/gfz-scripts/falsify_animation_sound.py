"""Falsification pass 1 on how-an-animation-makes-a-sound (OPUS, 2026-09-29), from the shipping image. Rows check the page as
corrected by this pass (CON-190). The authored-command census is carried, not re-run.

  S0  sizes 00520C50 43, 00520D00 37, 0046C250 1090, 0046C6E0 438, 0046CC70 1069, 0046CBA0 8, 003A6E60 345
  S1  section 1: command 0x05 passes word +2 as (>> 12, & 0xFFF) to 0046CBA0, which zeroes r9d (volume 0) and jumps to
      0046CC70; command 0x29 passes mode 0, type 1 and the signed word +2; the emitter is record +0x5F0
  S2  CON-190: every draw in the picker is 003A6E60, and 003A6E60 advances the PRESENTATION bit-feedback state 01EF93E8
      (gated by 022D9138), not a gameplay generator
  S3  section 2's table: the 12 arms (00120000 + dword[0046C694 + 4 (type - 1)]) - type 1 group 1 variant 0; 3 -> 0x0A;
      8/9/10 -> 0x15/0x17/0x19; 11/12 -> 0x0E/0x0F (group 0); 6 draws 2 and adds 8; 7 counts down byte +4, reloads with a
      draw of 9 plus 3, then draws 4 (0 = silence) and adds 0x0A; 4 and 5 are silent when 003326C0 finds nothing
  S4  section 3: the twelve-entry point table (0046C898): 1 and 8 -> 0x101; 2 and 3 -> the 0x200 attachment; 4-7 -> 0x0C;
      9-12 -> 0x100; the radius is FCP property 0x9001D1E times 0.5 (01CEBB70)
  S5  section 5: the play routine refuses unless emitter byte +0 is 1, 00237420 answers 0, and the owner record (word +8
      into the 0x740-stride array 022C6F28) is live with +0x284 bit 4
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
A = lambda fa: {x.address: (S(x), rip(x)) for x in body(fa)}
u32 = lambda va: struct.unpack("<I", blob[OFF(va):OFF(va) + 4])[0]
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]


def eq(m, a, text, target=None):
    g = m.get(a)
    return g is not None and g[0] == text and (target is None or target in g[1])


SZ = {0x00520C50: 43, 0x00520D00: 37, 0x0046C250: 1090, 0x0046C6E0: 438, 0x0046CC70: 1069, 0x0046CBA0: 8, 0x003A6E60: 345}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("S0", not bad, "sizes %s" % (bad or "all seven as cited"))
H5, H29, W = A(0x00520C50), A(0x00520D00), A(0x0046CBA0)
check("S1", eq(H5, 0x00520C58, "add rcx, 0x5f0") and eq(H5, 0x00520C65, "and r8d, 0xfff") and eq(H5, 0x00520C6C, "shr edx, 0xc")
      and eq(H5, 0x00520C6F, "call 0x46cba0") and eq(W, 0x0046CBA0, "xor r9d, r9d") and eq(W, 0x0046CBA3, "jmp 0x46cc70")
      and eq(H29, 0x00520D04, "movsx r9d, word ptr [rdx + 2]") and eq(H29, 0x00520D10, "xor edx, edx")
      and eq(H29, 0x00520D12, "lea r8d, [rdx + 1]") and eq(H29, 0x00520D16, "call 0x46cc70"),
      "0x05 -> 0046CBA0 (volume 0) -> 0046CC70; 0x29 -> mode 0, type 1, signed volume; emitter +0x5F0")
PK = body(0x0046C250)
draws = sorted(set(x.op_str for x in PK if x.mnemonic == "call" and x.op_str.startswith("0x3a6e6")))
other_calls = sorted(set(x.op_str for x in PK if x.mnemonic == "call"))
R = A(0x003A6E60)
state = [a for a, (t, r) in R.items() if 0x01EF93E8 in r]
check("S2", draws == ["0x3a6e60"] and eq(R, 0x003A6E60, "mov r8d, dword ptr [rip + 0x1f322d1]", 0x022D9138)
      and eq(R, 0x003A6F0C, "mov dword ptr [rip + 0x1b524d6], edx", 0x01EF93E8) and len(state) >= 4
      and other_calls == ["0x2ed500", "0x3326c0", "0x3a6e60", "0x808c40"],
      "CON-190: the picker's only draw is 003A6E60, the presentation bit-feedback PRNG (01EF93E8, mode 022D9138); calls %s"
      % ",".join(other_calls))
arm = [0x00120000 + u32(0x0046C694 + 4 * i) for i in range(12)]
P = A(0x0046C250)
t3 = [S(x) for x in PK if arm[2] <= x.address < arm[2] + 0x17]
t8 = [S(x) for x in PK if arm[7] <= x.address < arm[7] + 0x15]
t9 = [S(x) for x in PK if arm[8] <= x.address < arm[8] + 0x15]
t10 = [S(x) for x in PK if arm[9] <= x.address < arm[9] + 0x15]
t11 = [S(x) for x in PK if arm[10] <= x.address < arm[10] + 0x14]
t12 = [S(x) for x in PK if arm[11] <= x.address < arm[11] + 0x14]
check("S3", arm[0] == 0x0046C29C and "mov edx, 0xa" in t3 and "mov edx, 0x15" in t8 and "mov edx, 0x17" in t9
      and "mov edx, 0x19" in t10 and "mov edx, 0xe" in t11 and "mov edx, 0xf" in t12
      and eq(P, 0x0046C569, "mov ecx, ebx") and eq(P, 0x0046C597, "add edx, 8")
      and eq(P, 0x0046C5A5, "dec byte ptr [rcx + 4]") and eq(P, 0x0046C5B9, "lea ecx, [rbx + 7]") and eq(P, 0x0046C5C1, "add al, 3")
      and eq(P, 0x0046C5C3, "lea ecx, [rbx + 2]") and eq(P, 0x0046C5F9, "add edx, 0xa")
      and eq(P, 0x0046C42B, "call 0x3326c0") and eq(P, 0x0046C433, "je 0x46c66d") and eq(P, 0x0046C507, "call 0x3326c0")
      and eq(P, 0x0046C50F, "je 0x46c66d"),
      "the type table; 6 -> 8 or 9; 7's countdown; 4 and 5 silent when 003326C0 finds nothing")
pt = [0x00120000 + u32(0x0046C898 + 4 * i) for i in range(12)]
Q = A(0x0046C6E0)
check("S4", pt[0] == pt[7] and pt[1] == pt[2] and len({pt[3], pt[4], pt[5], pt[6]}) == 1 and len({pt[8], pt[9], pt[10], pt[11]}) == 1
      and eq(Q, pt[0], "mov edx, 0x101") and eq(Q, 0x0046C790, "mov edx, 0x200") and eq(Q, pt[3], "mov edx, 0xc")
      and eq(Q, pt[8], "mov edx, 0x100") and eq(Q, 0x0046C7EE, "mov edx, 0x9001d1e") and f32(0x01CEBB70) == 0.5,
      "point table 1,8 / 2,3 / 4-7 / 9-12; radius = FCP 0x9001D1E x 0.5")
C = A(0x0046CC70)
check("S5", eq(C, 0x0046CC9A, "cmp byte ptr [rcx], 1") and eq(C, 0x0046CCAE, "call 0x237420") and eq(C, 0x0046CCB5, "jne 0x46d076")
      and eq(C, 0x0046CCC9, "mov r8, qword ptr [rip + 0x1e5a258]", 0x022C6F28) and eq(C, 0x0046CCD4, "imul rax, rax, 0x740")
      and eq(C, 0x0046CCF1, "test byte ptr [rax + 0x284], 0x10"),
      "enabled emitter, mute test 00237420, live owner record with +0x284 bit 4")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
