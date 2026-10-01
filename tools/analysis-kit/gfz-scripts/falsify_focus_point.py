"""Falsification pass 1 on the-focus-point-of-a-character (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  K1  (REFUTES the SWE2-EC7-83 note: "`0046FAA0` ... cvtsi2ss(word[01EFAB4C]-1) ... returns float[01EFAC80 + i*4]") 0046FAA0 loads a
      DWORD count from 01F2053C (= 60) and indexes the float table at 01F20C80 (0.0097 .. 1.0), as section 3 says; 01EFAB4C and
      01EFAC80 hold zeros in the image and neither sampler reads them (the sibling 0046FBB0 reads 01F20538 / 01F20AA0)
  F0  section 7 sizes: 003E43D0 814, 003E5ED0 201, 003E5FA0 201, 003E6070 211, 0046FAA0 60, 004234B0 96, 00423510 85, 003E5810 160,
      004288E0 87
  F1  section 2: 004234B0 resolves [rcx + 0xF0], passes the tag 0x4D524640 ('@FRM') to 00408F90 and reads [rec + 0x30] + 0x10;
      00423510 reads + 0xC instead
  F2  section 2: 003E5FA0 tests the version against 3 and takes the first non-0xFFFF of +0x3A / +0x3C / +0x3E, calling 003710E0
  F3  section 3: 003E43D0 stores the transformed point at +0x670, blends toward +0x690 (kind 1) and +0x660 (kind 0), reloads the
      other nibble of +0x66C from 8 * [01DFE0B4], and stores 003E6070's result at +0x6A8
  F4  section 3: every return of 003E6070 leaves eax = 0
  F5  section 3: 004288E0 calls 003E43D0 only for records whose +0x290 bit 1 is clear
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
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
anyop = lambda I, pred: [a for a, x in sorted(I.items()) if pred(x)]

E = body(0x0046FAA0); E2 = body(0x0046FBB0)
refsE = sorted({r for x in E.values() for r in rip(x)}); refs2 = sorted({r for x in E2.values() for r in rip(x)})
cnt = struct.unpack("<I", blob[OFF(0x01F2053C):OFF(0x01F2053C) + 4])[0]
tab = struct.unpack("<60f", blob[OFF(0x01F20C80):OFF(0x01F20C80) + 240])
wrong_cnt = struct.unpack("<I", blob[OFF(0x01EFAB4C):OFF(0x01EFAB4C) + 4])[0]
wrong_tab0 = struct.unpack("<f", blob[OFF(0x01EFAC80):OFF(0x01EFAC80) + 4])[0]
zeros = wrong_cnt != 60 and abs(wrong_tab0 - tab[0]) > 1e-3
load = S(E[0x0046FAA0])
check("K1", set(refsE) == {0x01F2053C, 0x01F20C80} and load.startswith("mov r8d, dword ptr") and cnt == 60 and abs(tab[0] - 0.0097) < 1e-3 and tab[59] == 1.0
      and zeros and not ({0x01EFAB4C, 0x01EFAC80} & (set(refsE) | set(refs2))) and set(refs2) == {0x01F20538, 0x01F20AA0},
      "(REFUTES the EC7-83 addresses) 0046FAA0 reads %s (%s), count %d, table %.4f..%.4f; 01EFAB4C holds %d and 01EFAC80 is not the ease table, and neither sampler reads them; 0046FBB0 reads %s"
      % (["%08X" % r for r in refsE], load, cnt, tab[0], tab[59], wrong_cnt, ["%08X" % r for r in refs2]))
SZ = {0x003E43D0: 814, 0x003E5ED0: 201, 0x003E5FA0: 201, 0x003E6070: 211, 0x0046FAA0: 60, 0x004234B0: 96, 0x00423510: 85, 0x003E5810: 160, 0x004288E0: 87}
check("F0", all(sizes.get(a) == n for a, n in SZ.items()), "%s" % {("%08X" % a): sizes.get(a) for a in SZ})
L1, L2 = body(0x004234B0), body(0x00423510)
tag = anyop(L1, lambda x: any(o.type == X86_OP_IMM and o.imm == 0x4D524640 for o in x.operands))
check("F1", tag and any("+ 0xf0]" in S(x) for x in L1.values()) and S(L1[0x004234F3]) == "add rcx, 0x30" and S(L1[0x004234F9]) == "mov eax, dword ptr [rcx + 0x10]"
      and any("+ 0xc]" in S(x) for x in L2.values()) and struct.pack("<I", 0x4D524640) == b"@FRM",
      "tag 0x4D524640 ('@FRM') at %s; +0xF0, +0x30, +0x10 in 004234B0; +0xC in 00423510" % ["%08X" % a for a in tag])
M = body(0x003E5FA0)
check("F2", any(x.mnemonic == "cmp" and x.op_str.endswith(", 3") for x in M.values()) and all(any("+ 0x%x]" % d in S(x) for x in M.values()) for d in (0x3A, 0x3C, 0x3E))
      and any(x.mnemonic == "call" and imm(x) == 0x003710E0 for x in M.values()), "version test, the three bone ids, the bone-matrix call")
P = body(0x003E43D0)
st = lambda d: anyop(P, lambda x: x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == d and x.mnemonic.startswith(("mov", "movss", "movups", "movaps", "movq")))
mul = anyop(P, lambda x: 0x01DFE0B4 in rip(x))
via = anyop(P, lambda x: S(x) == "lea rdi, [rcx + 0x670]")
viast = anyop(P, lambda x: x.operands and x.operands[0].type == X86_OP_MEM and x.reg_name(x.operands[0].mem.base) == "rdi" and x.mnemonic.startswith(("mov", "movss", "movups", "movaps", "movq", "movdqa")))
check("F3", via and viast and any(anyop(P, lambda x, d=d: any(o.type == X86_OP_MEM and o.mem.disp == d for o in x.operands)) for d in (0x690, 0x660)) and st(0x66C) and mul and st(0x6A8),
      "+0x670 through rdi (%s), stores %s; +0x66C %s, +0x6A8 %s; multiplier 01DFE0B4 read at %s" % (["%08X" % a for a in via], ["%08X" % a for a in viast][:4], ["%08X" % a for a in st(0x66C)], ["%08X" % a for a in st(0x6A8)], ["%08X" % a for a in mul]))
V = sorted(body(0x003E6070).items())
rets = [k for k, (a, x) in enumerate(V) if x.mnemonic == "ret"]
zero_before = []
for k in rets:
    prior = [S(V[j][1]) for j in range(max(0, k - 8), k)]
    zero_before.append(any(p == "xor eax, eax" for p in prior) and not any(p.startswith(("mov eax,", "mov rax,", "movzx eax")) and p != "xor eax, eax" for p in prior[prior.index("xor eax, eax") + 1:] if "xor eax, eax" in prior))
check("F4", rets and all(zero_before), "%d returns, each after xor eax, eax: %s" % (len(rets), zero_before))
W = body(0x004288E0)
calls = anyop(W, lambda x: x.mnemonic == "call" and imm(x) == 0x003E43D0)
gate = anyop(W, lambda x: "+ 0x290]" in S(x))
check("F5", calls and gate and min(gate) < min(calls), "gate on +0x290 at %s precedes the call at %s" % (["%08X" % a for a in gate], ["%08X" % a for a in calls]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
