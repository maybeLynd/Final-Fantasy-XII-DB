"""Falsification pass 1 on CONTRACT-separation-pass (OPUS, 2026-09-29), from the shipping image. Killers first.

  S0  section 2: sizes 108 / 131 / 155 / 283 / 1,080 / 35
  S1  P-1: 003DAA40 zeroes 512 bytes (32 x 16) at 02B57CE0 and clears +7 on 128 bodies of 0x130
  S2  P-2: 003DAAB0 ORs the masks of the body's cells into 02B57EE0, then clears the body's own bit and every lower bit
  S3  P-4: the refusal chain at the cited sites, the mode test at 00314FD2 skipping the activity test, and the callers' modes -
      00314F30 passes 1, 00313F80 passes 0
  S4  (scope P-4 / P-5 did not state) a second mode test at 00315084 sends query mode past the push geometry. That geometry
      reads positions (003DAE00), refuses bodies whose vertical spans [y + E4, y + E4 + E0] do not overlap (003150CA /
      003150DB) - a push-only seventh refusal - and only then adds the accumulated pushes (P-5)
  S5  P-6: 003DA9F0 zeroes +0x100/+0x104 (qword), +0x108, +0xEC/+0xED (word), +0xE8 and +0xEE
  S6  P-7: the three outcomes 3 / 4 / 1 and their counters, each behind `test esi, esi / je 00315377`; in query mode the
      resolver writes only the out-parameter [r15] (A's share) and no body field
  S7  section 5: the resolver and the split write only +0xE8, +0xEC..+0xEE, +0x100 and +0x108 of either body - never radii,
      margins, layer, owner, weights or masks
"""
import io, os
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
E = [0x003DAA40, 0x003DAC70, 0x003DAAB0, 0x003DAB50, 0x00314F50, 0x003DA9F0]
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in E + [0x00314E10, 0x00314F30, 0x00313F80]}
T = {fa: [S(x) for x in b] for fa, b in B.items()}
at = lambda fa, va: next(S(x) for x in B[fa] if x.address == va)
run = lambda fa, lo, hi: [S(x) for x in B[fa] if lo <= x.address <= hi]
cell = lambda fa, va: rip(next(x for x in B[fa] if x.address == va))[0]
R = 0x00314F50

# S0
check("S0", [sizes[f] for f in E] == [108, 131, 155, 283, 1080, 35], "%s" % [sizes[f] for f in E])
# S1
check("S1", cell(0x003DAA40, 0x003DAA43) == 0x02B57CE0 and "lea ecx, [r8 + 8]" in T[0x003DAA40] and "lea rax, [rax + 0x40]" in T[0x003DAA40]
      and "imul rdx, rax, 0x130" in T[0x003DAA40] and "mov byte ptr [rdx + 7], r8b" in T[0x003DAA40] and "cmp ecx, 0x80" in T[0x003DAA40],
      "8 x 0x40 = 512 bytes at 02B57CE0; +7 cleared on 128 bodies of 0x130")
# S2
p2 = T[0x003DAAB0]
check("S2", cell(0x003DAAB0, 0x003DAAED) == 0x02B57EE0 and "por xmm0, xmm1" in p2 and "shr ecx, 1" in p2
      and p2[p2.index("lea rax, [rdx - 1]"):p2.index("lea rax, [rdx - 1]") + 4] == ["lea rax, [rdx - 1]", "or rax, rdx", "not rax", "and qword ptr [rcx], rax"]
      and "mov qword ptr [r10 + rcx*8], r9" in p2,
      "OR of the cell masks into 02B57EE0; own bit and all lower bits cleared (the own qword masked, lower qwords zeroed)")
# S3
check("S3", at(R, 0x00314F78) == "test rcx, rcx" and at(R, 0x00314F97) == "comiss xmm7, dword ptr [rcx + 0xf0]" and at(R, 0x00314FA0) == "comiss xmm7, dword ptr [rcx + 0xf4]"
      and at(R, 0x00314FB0) == "comiss xmm7, dword ptr [rdx + 0xf0]" and at(R, 0x00314FC5) == "comiss xmm7, dword ptr [rdx + 0xf4]"
      and run(R, 0x00314FD2, 0x00314FE4) == ["test esi, esi", "je 0x314fea", "cmp byte ptr [rcx + 7], 0", "je 0x315381", "cmp byte ptr [rdx + 7], 0", "je 0x315381"]
      and run(R, 0x00314FEA, 0x00315008) == ["movzx eax, byte ptr [rdx + 6]", "cmp byte ptr [rcx + 6], al", "jne 0x315381", "movzx eax, byte ptr [rcx + 0x119]",
                                             "test al, al", "je 0x31500e", "cmp al, byte ptr [rdx + 0x119]", "je 0x315381"]
      and at(0x00314F30, 0x00314F39) == "mov r8d, 1" and at(0x00313F80, 0x00313FB4) == "xor r8d, r8d",
      "the six refusals at their sites; activity test only when mode != 0; 00314F30 mode 1, 00313F80 mode 0")
# S4
check("S4", run(R, 0x00315084, 0x00315086) == ["test esi, esi", "je 0x315220"] and "call 0x3dae00" in run(R, 0x00315091, 0x0031509E)
      and run(R, 0x003150A3, 0x003150DE) == ["movss xmm2, dword ptr [rsp + 0x44]", "addss xmm2, dword ptr [rdi + 0xe4]", "movss xmm1, dword ptr [rsp + 0x54]",
                                             "addss xmm1, dword ptr [rbx + 0xe4]", "movaps xmm0, xmm2", "addss xmm0, dword ptr [rdi + 0xe0]", "comiss xmm1, xmm0",
                                             "ja 0x31515c", "addss xmm1, dword ptr [rbx + 0xe0]", "comiss xmm2, xmm1", "ja 0x31515c"]
      and at(R, 0x003150F8) == "addss xmm0, dword ptr [rbx + 0x100]",
      "query mode jumps to 00315220 past the push geometry; push mode refuses non-overlapping vertical spans before adding the accumulators")
# S5
check("S5", T[0x003DA9F0] == ["xor eax, eax", "mov qword ptr [rcx + 0x100], rax", "mov dword ptr [rcx + 0x108], eax", "mov word ptr [rcx + 0xec], ax",
                              "mov dword ptr [rcx + 0xe8], eax", "mov byte ptr [rcx + 0xee], al", "ret"], "seven fields in five stores")
# S6
check("S6", run(R, 0x00315250, 0x00315263) == ["mov eax, 3", "test esi, esi", "je 0x315377", "inc byte ptr [rdi + 0xed]", "mov byte ptr [rdi + 0xee], 1"]
      and run(R, 0x00315274, 0x00315287) == ["mov eax, 4", "test esi, esi", "je 0x315377", "inc byte ptr [rbx + 0xed]", "mov byte ptr [rbx + 0xee], 1"]
      and run(R, 0x00315290, 0x003152AB) == ["test esi, esi", "je 0x315377", "inc byte ptr [rbx + 0xed]", "inc byte ptr [rdi + 0xed]",
                                             "mov byte ptr [rdi + 0xee], 0", "mov byte ptr [rbx + 0xee], 0"]
      and at(R, 0x00315377) == "movss dword ptr [r15], xmm4"
      and not [x for x in B[R] if x.address < 0x0031525D and x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "movss", "inc")
               and ("[rbx +" in S(x).split(",")[0] or "[rdi +" in S(x).split(",")[0])],
      "outcomes 3 / 4 / 1; each body write behind the mode test; query mode writes only [r15]")
# S7
bw = sorted({x.operands[0].mem.disp for f in (R, 0x00314E10) for x in B[f] if x.operands and x.operands[0].type == X86_OP_MEM
             and x.mnemonic in ("mov", "movss", "inc", "or", "and", "add", "sub") and x.reg_name(x.operands[0].mem.base) in ("rbx", "rdi")})
check("S7", bw == [0xE8, 0xEC, 0xED, 0xEE, 0x100, 0x108], "body fields written: %s" % ["0x%X" % d for d in bw])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
