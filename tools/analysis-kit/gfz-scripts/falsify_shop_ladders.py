"""Falsification pass 1 on CONTRACT-shop-stock-ladders (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  G0  section 2: 002FAD40 251 B, 002FA920 676 B, 002536F0 17 B
  G1  SG-1: 002FAD40 has exactly one call site image-wide (002FA9AE, in 002FA920); it returns rbx (002FAE2D `mov rax, rbx`);
      002FA9B3 stores the result; 002FAABF `cmp rsi, qword ptr [rsp + 0x30]` / 002FAAC4 jne
  G2  SG-2: rbx is 0 at 002FAD4F, set per entry at 002FADB0/002FADBF, and every exit (002FAD75 exhausted, the kind-0 pass, the
      three jge passes) reaches the one epilogue 002FAE28 that returns it; the body has one ret
  G3  SG-3: 002FAD71 `xor ecx, ecx` on an unresolved section; 002FADC3 `xor ebx, ebx` then 002FADC5 `movzx eax, byte ptr [rbx]`
  G4  SG-4: kinds 1 and 2 call AiTargetSelector_ResolveOperandValue (00321190) with ecx = 3, edx = 0; r8 = byte [rbx+1] at
      002FADD0 against `xor r8d, r8d` at 002FADFA; nothing else differs between the two argument set-ups
  G5  SG-5: [rbx] is read at 002FADC5, 002FADEE and 002FAE0F; a kind outside 0..3 reaches 002FAE21 `inc esi`
  G6  SG-6: 00315390 has exactly three call sites (002536F4, 0056F482, 00583F2A); 002536F9 `movzx eax, al`
  G7  SG-7: six resolves of [rdi + 4] per pass (including the count at the loop top, 002FAD56); 002FADB0 `mov rbx, rax`,
      002FADBF `add ebx, ecx`
  G8  section 10: the three threshold compares are `jge` after `movzx` of word [rbx + 2] (002FADE4, 002FAE05, 002FAE19)
  G9  section 14: 00315390 starts at rung 12 (00D1062D), steps 8 bytes per rung, stops at rung 1; rung 1 at 00D105D0 is
      {0, 0, 0}; the fall-through stores 1 (003153E1)
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
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None

text = next(x for x in SECS if x[0] == ".text")
sites = {0x002FAD40: [], 0x00315390: []}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.mnemonic in ("call", "jmp") and imm(x) in sites:
                sites[imm(x)].append((x.address, fa))
    except ValueError:
        continue

G = body(0x002FAD40); L = body(0x002FA920)
check("G0", [sizes[a] for a in (0x002FAD40, 0x002FA920, 0x002536F0)] == [251, 676, 17], "%s" % [sizes[a] for a in (0x002FAD40, 0x002FA920, 0x002536F0)])
check("G1", sites[0x002FAD40] == [(0x002FA9AE, 0x002FA920)] and at(G, 0x002FAE2D) == "mov rax, rbx" and at(L, 0x002FA9AE) == "call 0x2fad40"
      and L[0x002FA9B3].operands[0].type == X86_OP_MEM and at(L, 0x002FA9B3).endswith(", rax")
      and at(L, 0x002FAABF) == "cmp rsi, qword ptr [rsp + 0x30]" and L[0x002FAAC4].mnemonic == "jne",
      "call sites %s; store %s; match %s / %s" % (["%08X" % s for s, _ in sites[0x002FAD40]], at(L, 0x002FA9B3), at(L, 0x002FAABF), at(L, 0x002FAAC4)))
exits = sorted({imm(x) for x in G.values() if x.mnemonic.startswith("j") and imm(x) and not (0x002FAD40 <= imm(x) < 0x002FAD40 + sizes[0x002FAD40])})
to_epi = sorted(a for a, x in G.items() if x.mnemonic.startswith("j") and imm(x) == 0x002FAE28)
rets = [a for a, x in G.items() if x.mnemonic == "ret"]
check("G2", at(G, 0x002FAD4F) == "xor ebx, ebx" and at(G, 0x002FADB0) == "mov rbx, rax" and at(G, 0x002FADBF) == "add ebx, ecx"
      and to_epi == [0x002FAD75, 0x002FADCA, 0x002FADEC, 0x002FAE0D, 0x002FAE1F] and not exits and len(rets) == 1
      and not any(x.operands and x.operands[0].type != X86_OP_MEM and x.reg_name(x.operands[0].reg) in ("rbx", "ebx") for a, x in G.items()
                  if a > 0x002FADC5 and a < 0x002FAE2D and x.mnemonic in ("mov", "xor", "add", "lea") and x.operands[0].type == 1),
      "jumps to the epilogue from %s; exits outside the body %s; rets %s" % (["%08X" % a for a in to_epi], exits, ["%08X" % a for a in rets]))
check("G3", at(G, 0x002FAD71) == "xor ecx, ecx" and at(G, 0x002FADC3) == "xor ebx, ebx" and at(G, 0x002FADC5) == "movzx eax, byte ptr [rbx]"
      and at(G, 0x002FAD86) == "je 0x2fadc3" and at(G, 0x002FAD9B) == "je 0x2fadc3",
      "%s | %s -> %s" % (at(G, 0x002FAD71), at(G, 0x002FADC3), at(G, 0x002FADC5)))
k1 = sorted(S(G[a]) for a in G if 0x002FADD0 <= a <= 0x002FADDF)
k2 = sorted(S(G[a]) for a in G if 0x002FADF3 <= a <= 0x002FAE00)
d1, d2 = set(k1) - set(k2), set(k2) - set(k1)
check("G4", d1 == {"movzx r8d, byte ptr [rbx + 1]"} and d2 == {"xor r8d, r8d"} and "call 0x321190" in k1 and "lea ecx, [rdx + 3]" in k1 and "xor edx, edx" in k1,
      "only in kind 1 %s; only in kind 2 %s" % (sorted(d1), sorted(d2)))
check("G5", at(G, 0x002FADC5) == "movzx eax, byte ptr [rbx]" and at(G, 0x002FADEE) == "cmp byte ptr [rbx], 2" and at(G, 0x002FAE0F) == "cmp byte ptr [rbx], 3"
      and at(G, 0x002FAE12) == "jne 0x2fae21" and at(G, 0x002FAE21) == "inc esi", "%s | %s | %s -> %s" % (at(G, 0x002FADC5), at(G, 0x002FADEE), at(G, 0x002FAE0F), at(G, 0x002FAE21)))
check("G6", sorted(s for s, _ in sites[0x00315390]) == [0x002536F4, 0x0056F482, 0x00583F2A] and at(body(0x002536F0), 0x002536F9) == "movzx eax, al",
      "call sites %s" % ["%08X" % s for s, _ in sorted(sites[0x00315390])])
res = [a for a in sorted(G) if 0x002FAD56 <= a < 0x002FADC5 and at(G, a) == "mov ecx, dword ptr [rdi + 4]"]
check("G7", len(res) == 6 and res[0] == 0x002FAD56 and at(G, 0x002FAE23) == "jmp 0x2fad56", "[rdi + 4] resolves per pass at %s" % ["%08X" % a for a in res])
check("G8", all(at(G, a) == "movzx %s, word ptr [rbx + 2]" % r for a, r in ((0x002FADE4, "eax"), (0x002FAE05, "eax"), (0x002FAE19, "ecx")))
      and [G[a].mnemonic for a in (0x002FADEC, 0x002FAE0D, 0x002FAE1F)] == ["jge", "jge", "jge"], "three movzx + jge")
K = body(0x00315390)
rung1 = struct.unpack("<IBB", blob[OFF(0x00D105D0):OFF(0x00D105D0) + 6])
check("G9", rip(K[0x003153B5]) == [0x00D1062D] and at(K, 0x003153BC) == "mov eax, 0xc" and at(K, 0x003153D8) == "sub rcx, 8"
      and at(K, 0x003153DC) == "cmp eax, 1" and at(K, 0x003153E1) == "mov al, 1" and 0x00D1062D - 8 * 11 - 5 == 0x00D105D0 and rung1 == (0, 0, 0),
      "rung 12 at 00D1062D, 8 B per rung, rung 1's fields at 00D105D0 = %s; fall-through %s" % (rung1, at(K, 0x003153E1)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
