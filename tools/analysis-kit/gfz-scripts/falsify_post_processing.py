"""Falsification pass 1 on CONTRACT-post-processing-subsystem (OPUS, 2026-09-29), from the shipping image, using the contract's
own "Falsified by" tests. Every edge census is a raw E8/E9 sweep of .text plus an 8-byte stored-address search.

  Q1  I-1: 0070BA00's only inbound edge is from 006DB660, whose only one is from 006CBEA0, whose only one is the thunk
      0065E5C0, whose only caller is 00193DA0 at 00193F58; no stored copy of any of the four addresses; 00193DFC (the
      no-library-object return) precedes 00193F58
  Q2  I-2 / section 3: 0065E5A0's only caller is 00193DE8; 006CBD20's only inbound edge is 0065E5A0's jump; 006DAA70's only caller
      is 006CBE0A, which passes 0x20001 (006CBE02); Initialize 006FF900 is reached from 006DAA70 and 006DE950 only, and 006DE950
      has no inbound edge and no stored address; 006FFB8C stores the fifth argument at +0x20C; no instruction in the image
      inside the library (006C0000..00760000) writes (mov/or/xor/add/bts) an immediate carrying 0x40000, 0x4000000 or 0x8000000
      to a +0x20C displacement
  Q3  I-4: 00193E42 / 00193EC0 are the Glare (+0x34) and DepthofField (+0x30) option tests; 00193DA0 calls 0065E670 and
      0065E610 once each (00193E6C, 00193F40), and no conditional jump after 00193DFC jumps over either call
  Q4  I-5: after 006CBEA0's call to 006DB660 nothing tests eax / rax before the body's next call or return
  Q5  I-5's bound: 00708110 tests +0x147 before dereferencing +0x108 (00708186); on its object (rsi) Initialize writes +0x108
      only at 007009BB and +0x147 only at 00700083, behind the 0x800 flag test at 00700077 (its [rbp + 0x108] stores are a stack local)
"""
import collections, io, os, struct
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
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]
TARGETS = [0x0070BA00, 0x006DB660, 0x006CBEA0, 0x0065E5C0, 0x0065E5A0, 0x006CBD20, 0x006DAA70, 0x006FF900, 0x006DE950]
edges = collections.defaultdict(list)
for k in range(len(raw) - 5):
    if raw[k] in (0xE8, 0xE9):
        t = text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0]
        if t in TARGETS:
            edges[t].append((text[1] + k, "call" if raw[k] == 0xE8 else "jmp"))
stored = {t: blob.count(struct.pack("<Q", t)) for t in TARGETS}
check("Q1", [a for a, _ in edges[0x0070BA00]] and all(0x006DB660 <= a < 0x006DB660 + sizes[0x006DB660] for a, _ in edges[0x0070BA00])
      and all(0x006CBEA0 <= a < 0x006CBEA0 + sizes[0x006CBEA0] for a, _ in edges[0x006DB660]) and edges[0x006DB660]
      and all(0x0065E5C0 <= a < 0x0065E5C0 + sizes[0x0065E5C0] for a, _ in edges[0x006CBEA0]) and edges[0x006CBEA0]
      and edges[0x0065E5C0] == [(0x00193F58, "call")] and not any(stored[t] for t in TARGETS[:4]) and 0x00193DFC < 0x00193F58,
      "edges: 0070BA00 %s; 006DB660 %s; 006CBEA0 %s; 0065E5C0 %s; stored copies %s" % tuple(
          [["%08X %s" % e for e in edges[t]] for t in TARGETS[:4]] + [{"%08X" % t: stored[t] for t in TARGETS[:4]}]))
C = body(0x006CBD20)
i20c = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0x20C and len(x.operands) > 1 and x.operands[1].type == X86_OP_IMM                     and x.mnemonic in ("mov", "or", "xor", "add", "bts") and 0x006C0000 <= fa < 0x00760000:
                if x.operands[1].imm & (0x40000 | 0x4000000 | 0x8000000):
                    i20c.append(x.address)
    except ValueError:
        continue
I = body(0x006FF900)
init_callers = sorted(a for a, _ in edges[0x006FF900])
check("Q2", edges[0x0065E5A0] == [(0x00193DE8, "call")] and [m for _a, m in edges[0x006CBD20]] == ["jmp"] and 0x0065E5A0 <= edges[0x006CBD20][0][0] < 0x0065E5A0 + 8
      and edges[0x006DAA70] == [(0x006CBE0A, "call")] and "0x20001" in at(C, 0x006CBE02)
      and all(0x006DAA70 <= a < 0x006DAA70 + sizes[0x006DAA70] or 0x006DE950 <= a < 0x006DE950 + sizes[0x006DE950] for a in init_callers)
      and not edges[0x006DE950] and stored[0x006DE950] == 0 and "+ 0x20c]" in at(I, 0x006FFB8C) and not i20c,
      "route single at every link; 0x20001 at %s; Initialize callers %s; 006DE950 edges %d, stored %d; %s; forbidden-bit stores to +0x20C %s"
      % (at(C, 0x006CBE02), ["%08X" % a for a in init_callers], len(edges[0x006DE950]), stored[0x006DE950], at(I, 0x006FFB8C), i20c))
F = body(0x00193DA0)
c1 = [a for a, x in F.items() if x.mnemonic == "call" and imm(x) == 0x0065E670]
c2 = [a for a, x in F.items() if x.mnemonic == "call" and imm(x) == 0x0065E610]
jumps_over = [a for a, x in F.items() if a > 0x00193DFC and x.mnemonic.startswith("j") and x.mnemonic != "jmp" and imm(x)
              and any(a < c < imm(x) for c in c1 + c2)]
check("Q3", at(F, 0x00193E42) == "cmp dword ptr [rax + 0x34], 0" and at(F, 0x00193EC0) == "cmp dword ptr [rax + 0x30], 0"
      and c1 == [0x00193E6C] and c2 == [0x00193F40] and not jumps_over,
      "option tests %s (Glare) / %s (DepthofField); the calls follow at %s / %s; conditional jumps over them %s"
      % (at(F, 0x00193E42), at(F, 0x00193EC0), ["%08X" % a for a in c1], ["%08X" % a for a in c2], ["%08X" % a for a in jumps_over]))
E = sorted(body(0x006CBEA0).items())
k0 = next(k for k, (a, x) in enumerate(E) if x.mnemonic in ("call", "jmp") and imm(x) == 0x006DB660)
after = []
for a, x in E[k0 + 1:]:
    if x.mnemonic in ("call", "ret") or (x.mnemonic == "jmp" and imm(x) and not (0x006CBEA0 <= imm(x) < 0x006CBEA0 + sizes[0x006CBEA0])):
        break
    after.append(S(x))
tested = any(s.startswith(("test eax", "test rax", "cmp eax", "cmp rax")) for s in after)
check("Q4", not tested, "after the 006DB660 call: %s" % after[:6])
Y = body(0x00708110)
# `this` is rsi (006FF981 mov rsi, rcx); rbp is the stack frame (006FF90F lea rbp, [rax - 0xa98]), so [rbp + 0x108] is a local
objw = lambda d: sorted(a for a, x in I.items() if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == d
                        and x.mnemonic.startswith("mov") and x.reg_name(x.operands[0].mem.base) == "rsi")
w108, w147 = objw(0x108), objw(0x147)
assert at(I, 0x006FF981) == "mov rsi, rcx" and at(I, 0x006FF90F) == "lea rbp, [rax - 0xa98]"
t147 = [a for a, x in Y.items() if "0x147]" in S(x) and x.mnemonic in ("cmp", "test")]
check("Q5", w108 == [0x007009BB] and w147 == [0x00700083] and "0x800" in at(I, 0x00700077) and t147 and min(t147) < 0x00708186 and "0x108]" in " ".join(S(Y[a]) for a in Y if a <= 0x00708186),
      "Initialize writes +0x108 at %s and +0x147 at %s (gate %s); 00708110 tests +0x147 at %s before 00708186"
      % (["%08X" % a for a in w108], ["%08X" % a for a in w147], at(I, 0x00700077), ["%08X" % a for a in t147]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
