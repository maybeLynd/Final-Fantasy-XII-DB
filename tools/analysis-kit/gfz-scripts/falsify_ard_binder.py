"""Falsification pass 1 on CONTRACT-ard-area-binder (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  D0  section 2: 49 / 43 / 476 / 267 / 22 B
  D1  AB-1: 003EA840 `mov ecx, 0x15`, 003EA845 `lea esi, [r14 + r14]`; the request (003EA97A/003EA97F) and the size query
      (003EA863/003EA868) both take namespace 0x15
  D2  AB-2: 002DF980 is exactly the six quoted instructions - two dependent loads, no compare, no test
  D3  AB-3: 003EA852 `lea r8d, [rsi + 1]`, passed to 0032EB40
  D4  AB-4: the only two stores to 0215F0A8 (namespace 21) are 002DFA9E and 002DFE66, installing 01EDC280 and 01E0CFA0; over 642
      slots each array starts non-NULL at index 24 and holds 215 `.ard` at even and 215 `.fpk` at odd indices, with no
      crossover; the two arrays together reach all `.ard` strings in the image
  D5  AB-6: 003EA710 makes nine calls to ImageAddress_ResolveRuntimePointer (0020E600)
  D6  AB-7 (as corrected 2026-09-25): the binder calls the category setter 0023A160 five times, categories 0-2 unconditionally
      and 3-4 with `xor edx, edx` on a null resolve (003EA7CA, 003EA7F3), hands [rbp + 0x2C] to 003DCF00, and stores the buffer
      at 02B5E0C0; the reader calls the setter fifteen times in three groups of five, each (N, 0) for N = 0..4, and never
      with a non-zero second argument
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

check("D0", [sizes[a] for a in (0x00264ED0, 0x003EA6E0, 0x003EA820, 0x003EA710, 0x002DF980)] == [49, 43, 476, 267, 22],
      "%s" % [sizes[a] for a in (0x00264ED0, 0x003EA6E0, 0x003EA820, 0x003EA710, 0x002DF980)])
Rd = body(0x003EA820); Bd = body(0x003EA710)
check("D1", at(Rd, 0x003EA840) == "mov ecx, 0x15" and at(Rd, 0x003EA845) == "lea esi, [r14 + r14]" and at(Rd, 0x003EA863) == "mov ecx, 0x15"
      and at(Rd, 0x003EA868) == "call 0x32e400" and at(Rd, 0x003EA97A) == "mov ecx, 0x15" and at(Rd, 0x003EA97F) == "call 0x32e620" and at(Rd, 0x003EA974) == "mov edx, esi",
      "namespace 0x15, index 2i; size and request both on (21, 2i)")
P = [S(x) for x in md.disasm(blob[OFF(0x002DF980):OFF(0x002DF980) + 22], 0x002DF980)]
check("D2", P == ["movsxd rax, ecx", "lea r8, [rip + 0x1e7f676]", "movsxd rcx, edx", "mov rax, qword ptr [r8 + rax*8]", "mov rax, qword ptr [rax + rcx*8]", "ret"],
      "%s" % P)
check("D3", at(Rd, 0x003EA852) == "lea r8d, [rsi + 1]" and at(Rd, 0x003EA85B) == "call 0x32eb40", "%s -> %s" % (at(Rd, 0x003EA852), at(Rd, 0x003EA85B)))

NS = 0x0215F0A8
w = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        ins = list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
    except ValueError:
        continue
    for k, x in enumerate(ins):
        if NS in rip(x) and x.operands[0].type == X86_OP_MEM:
            src = x.op_str.split(", ")[-1]
            val = None
            for y in reversed(ins[max(0, k - 6):k]):
                if y.mnemonic == "lea" and y.op_str.startswith(src + ",") and rip(y):
                    val = rip(y)[0]; break
            w.append((x.address, val))


def cstr(va):
    try:
        o = OFF(va)
    except ValueError:
        return None
    e = blob.find(b"\0", o, o + 260)
    return blob[o:e].decode("latin-1") if e > o else ""


res = {}
reach = set()
for base in (0x01E0CFA0, 0x01EDC280):
    q = struct.unpack("<642Q", blob[OFF(base):OFF(base) + 642 * 8])
    first = next(i for i, v in enumerate(q) if v)
    ard_e = sum(1 for i, v in enumerate(q) if v and i % 2 == 0 and (cstr(v) or "").lower().endswith(".ard"))
    fpk_o = sum(1 for i, v in enumerate(q) if v and i % 2 == 1 and (cstr(v) or "").lower().endswith(".fpk"))
    cross = sum(1 for i, v in enumerate(q) if v and ((i % 2 == 1 and (cstr(v) or "").lower().endswith(".ard")) or (i % 2 == 0 and (cstr(v) or "").lower().endswith(".fpk"))))
    reach |= {v for i, v in enumerate(q) if v and (cstr(v) or "").lower().endswith(".ard")}
    res[base] = (first, ard_e, fpk_o, cross)
rd = next(x for x in SECS if x[0] == ".rdata")
rraw = blob[rd[3]:rd[3] + rd[4]]
allard = set()
k = 0
while True:
    k = rraw.find(b".ard\0", k)
    if k < 0:
        break
    s0 = rraw.rfind(b"\0", 0, k) + 1
    allard.add(rd[1] + s0); k += 1
check("D4", sorted(w) == [(0x002DFA9E, 0x01EDC280), (0x002DFE66, 0x01E0CFA0)] and all(v == (24, 215, 215, 0) for v in res.values()) and allard <= reach,
      "stores to 0215F0A8 %s; arrays (first, .ard even, .fpk odd, crossovers) %s; .ard strings in .rdata %d, reached %d"
      % ([("%08X" % a, "%08X" % v if v else None) for a, v in sorted(w)], {("%08X" % b_): v for b_, v in res.items()}, len(allard), len(allard & reach)))
check("D5", sum(1 for x in Bd.values() if x.mnemonic == "call" and imm(x) == 0x0020E600) == 9, "%d resolves" % sum(1 for x in Bd.values() if x.mnemonic == "call" and imm(x) == 0x0020E600))
bset = sorted(a for a, x in Bd.items() if x.mnemonic == "call" and imm(x) == 0x0023A160)
rset = sorted(a for a, x in Rd.items() if x.mnemonic == "call" and imm(x) == 0x0023A160)


def arg(I, a):
    ins = [I[b_] for b_ in sorted(I) if b_ < a][-4:]
    ecx = edx = None
    for y in ins:
        s = S(y)
        if s == "xor edx, edx":
            edx = 0
        elif s.startswith("lea ecx, [rdx + "):
            ecx = int(s.split("+ ")[1].rstrip("]"), 0)
        elif s.startswith("mov ecx, ") and s[9:].isdigit():
            ecx = int(s[9:])
        elif s == "xor ecx, ecx":
            ecx = 0
    return ecx, edx


rargs = [arg(Rd, a) for a in rset]
groups = [rset[i:i + 5] for i in range(0, len(rset), 5)]
check("D6", len(bset) == 5 and at(Bd, 0x003EA7CA) == "xor edx, edx" and at(Bd, 0x003EA7F3) == "xor edx, edx" and at(Bd, 0x003EA789) == "mov ecx, dword ptr [rbp + 0x2c]"
      and at(Bd, 0x003EA7A8) == "call 0x3dcf00" and rip(Bd[0x003EA809]) == [0x02B5E0C0]
      and len(rset) == 15 and [g[0] for g in groups] == [0x003EA8AD, 0x003EA8E5, 0x003EA9B7] and all(e == 0 for _c, e in rargs)
      and [c for c, _e in rargs] == [0, 1, 2, 3, 4] * 3,
      "binder setter calls %s; reader %d calls in groups starting %s, (ecx, edx) %s" % (["%08X" % a for a in bset], len(rset), ["%08X" % g[0] for g in groups], rargs))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
