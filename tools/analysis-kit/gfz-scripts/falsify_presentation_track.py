"""Falsification pass 1 on how-a-presentation-entry-picks-its-track (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  T0  sizes: 0041CD30 357, 0041CFC0 325, 0041C9A0 203, 00417920 349, 00417110 703, 0041CEC0 63, 00417CC0 58, 00418600 69,
      00417A80 72, 00417D00 219, 0051B970 96
  T1  section 2: 0041CD30 bounds the index by the stream's track count (+0x0C of [+0x368]), walks headers by their word +4,
      scans for a 0xFFFF command word, and stores the index at state +0x80
  T2  section 4: 0041C9A0 starts at state 1 (entry + 0xD0 = 0x30 + 0xA0) and steps 0xA0 - state 0 is never handed out
  T3  section 5: 00417920 splits word +2 into track (>> 4) and mode (& 0xF), and mode 1 tests the state word against 2
  T4  section 6: 00417110 tests entry bit 18 and the 0xFF selector kind at +0x2DC, calls through the table [02CA4668], reads the
      parent's cached bytes +0x4B8..+0x4BB, and synthesises the 0x0201 header
  T5  section 6a: 00418600 copies command bytes +2..+5 to entry +0x2DC..+0x2DF and sets the state word to 1
  T6  section 7: 0041CEC0 calls [02CA4470] with +0x2C0 and &+0x31C and ORs 0x200 into +0x0C on both paths; 00417CC0 calls
      [02CA4440] and sets bit 6 of +0x2C8
  T7  section 7a: 00417A80 multiplies by the word at 01DFE0B4; 00417D00 stores 1/(n+1) at +0x354 and 0x10 at +0x358
  T8  section 7b: 0051B970 sets the phase word 02CA83F4 to 1, then 2, then 0 around its three walks
  T9  the SWE2-EC7-60 note: 00417D00 makes one call, to 002ED570 at 00417DC6, and reads the constant at 01CEBBA8
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
txt = lambda fa: [S(x) for x in body(fa)]
has = lambda fa, *subs: all(any(sub in s for s in txt(fa)) for sub in subs)
imms = lambda fa: {o.imm & 0xFFFFFFFF for x in body(fa) for o in x.operands if o.type == X86_OP_IMM}
rips = lambda fa: {r for x in body(fa) for r in rip(x)}

SZ = {0x0041CD30: 357, 0x0041CFC0: 325, 0x0041C9A0: 203, 0x00417920: 349, 0x00417110: 703, 0x0041CEC0: 63, 0x00417CC0: 58,
      0x00418600: 69, 0x00417A80: 72, 0x00417D00: 219, 0x0051B970: 96}
check("T0", all(sizes.get(a) == n for a, n in SZ.items()), "%s" % {("%08X" % a): sizes.get(a) for a in SZ})
T = {x.address: S(x) for x in body(0x0041CD30)}
check("T1", T.get(0x0041CD34) == "mov r10, qword ptr [rcx + 0x368]" and T.get(0x0041CD4B) == "cmp r11d, dword ptr [r10 + 0xc]" and T.get(0x0041CD61) == "movzx eax, word ptr [r9 + 4]"
      and T.get(0x0041CDC8) == "mov dword ptr [rdx + 0x80], r11d" and T.get(0x0041CDE4) == "cmp byte ptr [r9], 1" and T.get(0x0041CDEA) == "cmp dword ptr [r10 + 0xc], 1"
      and T.get(0x0041CE31) == "mov r11d, 0xffff" and T.get(0x0041CE37) == "cmp word ptr [rcx], r11w",
      "count bound, header walk by word +4, state +0x80, primary when kind 1 or one track, the 0xFFFF marker scan")
F = txt(0x0041C9A0)
check("T2", "lea rax, [rcx + 0xd0]" in F and "mov r8d, 1" in F and "add rbx, 0xa0" in F, "first state inspected at +0xD0 (state 1), stride 0xA0")
C1 = txt(0x00417920)
check("T3", any(s.startswith(("shr", "sar")) and s.endswith(", 4") for s in C1) and any(s.startswith("and") and s.endswith(", 0xf") for s in C1)
      and any(s.startswith("cmp") and s.endswith(", 2") for s in C1), "track = word >> 4, mode = word & 0xF, the word == 2 test for mode 1")
C6 = txt(0x00417110)
check("T4", 0x02CA4668 in rips(0x00417110) and has(0x00417110, "+ 0x2dc]") and any(s.startswith("cmp") and s.endswith(", 0xff") for s in C6)
      and all(has(0x00417110, "+ 0x%x]" % d) for d in (0x4B8, 0x4B9, 0x4BA, 0x4BB)) and 0x0201 in imms(0x00417110)
      and (0x40000 in imms(0x00417110) or any("0x12" in s and s.startswith("bt") for s in C6)),
      "table [02CA4668], the 0xFF kind, parent bytes +0x4B8..+0x4BB, header 0x0201, entry bit 18")
C6a = txt(0x00418600)
check("T5", [s for s in C6a if s.startswith("mov byte ptr [r8 + 0x2d")] == ["mov byte ptr [r8 + 0x%x], al" % d for d in (0x2DC, 0x2DD, 0x2DE, 0x2DF)]
      and "mov eax, 1" in C6a and "mov word ptr [rdx + 4], ax" in C6a and "or word ptr [rdx + 8], 2" in C6a and "mov eax, dword ptr [r8 + 0x340]" in C6a,
      "command bytes into +0x2DC..; state word = 1: %s" % [s for s in C6a if "0x2dc" in s or "+ 4]" in s][:4])
check("T6", 0x02CA4470 in rips(0x0041CEC0) and has(0x0041CEC0, "+ 0x2c0]", "+ 0x31c]") and sum(1 for s in txt(0x0041CEC0) if s.endswith("+ 0xc], 0x200")) == 2
      and 0x02CA4440 in rips(0x00417CC0) and has(0x00417CC0, "+ 0x2c8]"),
      "dirty callback with +0x2C0 / &+0x31C, bit 9 raised on both paths; the class-0x06 sibling's callback and +0x2C8")
check("T7", 0x01DFE0B4 in rips(0x00417A80) and has(0x00417D00, "+ 0x354]", "+ 0x358]") and 0x10 in imms(0x00417D00),
      "00417A80 reads the frames-per-tick word 01DFE0B4; 00417D00 stores the factor at +0x354 and 0x10 at +0x358")
W = [(x.address, S(x)) for x in body(0x0051B970) if 0x02CA83F4 in rip(x)]
check("T8", [s.split(", ")[-1] for _a, s in W] == ["1", "2", "0"], "phase word stores %s" % W)
D = [(x.address, S(x)) for x in body(0x00417D00) if x.mnemonic == "call"]
check("T9", D == [(0x00417DC6, "call 0x2ed570")] and 0x01CEBBA8 in rips(0x00417D00), "the EC7-60 note: calls %s; reads 01CEBBA8" % D)
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
