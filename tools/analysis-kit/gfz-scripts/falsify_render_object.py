"""Falsification pass 1 on CONTRACT-character-render-object (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. Displacement censuses decode
every function to the larger of its catalogue size and its .pdata chain union, so the catalogue's short tails are included.

  O0  section 2: 001F4DA0 516 B, 001F6E70 2,328 B, 001FB120 496 B, each equal to its chain union
  O1  R-1: exactly three instructions LOAD the immediate 0x668 (mov): 001BD527 (allocation), 001F5309 (sized delete) and
      00897C19; two unrelated instructions use it as an arithmetic operand (add/adc) and are reported
  O2  R-2: 00903B68 is referenced only from 001F4DA0 and 001F51E0 (bounded census plus a linear rip-window sweep)
  O3  R-3: 001F4DDF `xor esi, esi`, 001F4EC9 `mov byte ptr [rdi + 0x4b4], sil`, 001F7729 `mov byte ptr [r8 + 0x4b4], 1` at
      +2,233 of 001F6E70; image-wide, stores at displacement 0x4B4 number 13, of which exactly these two are byte-width
  O4  R-4: byte-width reads of +0x4B4 number 17 in 16 functions
  O5  R-5: 0x584 - 0x4C4 = 0xC0 (three 64-byte matrices); 001FB1AC calls the accessor and 001FB1B1 tests byte [rax + 0x1C];
      00189120 is one instruction plus ret, loading the singleton [01F7F598]
  O6  R-6: 001FB120 decodes to 105 instructions, 48 of them movups, with no backward jump
  O7  R-7: 001FB126 reads +0x4B4 and 001FB13A leaves on zero before the first store to memory
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
pd = next(x for x in SECS if x[0] == ".pdata"); praw = blob[pd[3]:pd[3] + pd[4]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    if b_:
        pent[BASE + b_] = (BASE + e_, BASE + u_)
rootc = {}


def root(bg):
    if bg in rootc:
        return rootc[bg]
    seen, r = set(), bg
    while r in pent and r not in seen:
        seen.add(r); u = pent[r][1]; h = blob[OFF(u):OFF(u) + 4]
        if not (h[0] >> 3) & 4:
            break
        c = OFF(u) + 4 + 2 * ((h[2] + 1) & ~1); r = BASE + struct.unpack("<I", blob[c:c + 4])[0]
    rootc[bg] = r
    return r


uend = collections.defaultdict(int)
for b_ in pent:
    r = root(b_)
    uend[r] = max(uend[r], pent[b_][0])
ext = {fa: max(sizes[fa], uend.get(fa, 0) - fa) for fa in sizes}
text = next(x for x in SECS if x[0] == ".text")
bodies = {}
for fa in sorted(sizes):
    if text[1] <= fa < text[1] + text[2]:
        try:
            bodies[fa] = list(md.disasm(blob[OFF(fa):OFF(fa) + ext[fa]], fa))
        except ValueError:
            pass
B = lambda fa: {x.address: x for x in bodies[fa]}
at = lambda I, a: S(I[a]) if a in I else "?"
check("O0", [(sizes[f], uend.get(f, f + sizes[f]) - f) for f in (0x001F4DA0, 0x001F6E70, 0x001FB120)] == [(516, 516), (2328, 2328), (496, 496)],
      "(catalogue, chain union) %s" % [(sizes[f], uend.get(f, f + sizes[f]) - f) for f in (0x001F4DA0, 0x001F6E70, 0x001FB120)])
raw = blob[text[3]:text[3] + text[4]]
imm668 = set()
k = raw.find(struct.pack("<I", 0x668))
while k >= 0:
    pos = text[1] + k
    for L in range(1, 12):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and any(o.type == X86_OP_IMM and o.imm == 0x668 for o in x.operands):
            imm668.add((x.address, x.mnemonic)); break
    k = raw.find(struct.pack("<I", 0x668), k + 1)
loads = sorted(a for a, m in imm668 if m == "mov"); other = sorted((a, m) for a, m in imm668 if m != "mov")
check("O1", loads == [0x001BD527, 0x001F5309, 0x00897C19], "0x668 loaded (mov) at %s; also used as an arithmetic operand at %s"
      % (["%08X" % a for a in loads], ["%08X %s" % o for o in other]))
vt = sorted({fa for fa, ins in bodies.items() for x in ins if 0x00903B68 in rip(x)})
want = {0x00903B68 - t for t in (0, 1, 2, 4)}
lin = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        if base + 4 * kk + d in want:
            lin.add(text[1] + s + 4 * kk)
check("O2", vt == [0x001F4DA0, 0x001F51E0] and len(lin) == 2, "functions referencing 00903B68 %s; linear windows %d" % (["%08X" % f for f in vt], len(lin)))
W, R = [], []
for fa, ins in bodies.items():
    for x in ins:
        for n_, o in enumerate(x.operands):
            if o.type == X86_OP_MEM and o.mem.disp == 0x4B4 and x.reg_name(o.mem.base) not in ("rip", "rsp"):
                if n_ == 0 and x.mnemonic.startswith(("mov", "and", "or", "add", "sub", "inc", "dec", "set")) and len(x.operands) >= 1 and not x.mnemonic.startswith("movzx"):
                    W.append((x.address, fa, o.size))
                elif o.size == 1:
                    R.append((x.address, fa))
S_ = body0 = B(0x001F4DA0); T6 = B(0x001F6E70)
bw = sorted(a for a, f, sz in W if sz == 1)
check("O3", at(S_, 0x001F4DDF) == "xor esi, esi" and at(S_, 0x001F4EC9) == "mov byte ptr [rdi + 0x4b4], sil" and at(T6, 0x001F7729) == "mov byte ptr [r8 + 0x4b4], 1"
      and 0x001F7729 - 0x001F6E70 == 2233 and len(W) == 13 and bw == [0x001F4EC9, 0x001F7729],
      "%d stores at +0x4B4 image-wide (widths %s); byte-width %s" % (len(W), dict(collections.Counter(sz for _a, _f, sz in W)), ["%08X" % a for a in bw]))
check("O4", len(R) == 17 and len({f for _a, f in R}) == 16, "%d byte reads in %d functions" % (len(R), len({f for _a, f in R})))
P = B(0x001FB120)
acc = [S(x) for x in md.disasm(blob[OFF(0x00189120):OFF(0x00189120) + 16], 0x00189120)][:2]
check("O5", 0x584 - 0x4C4 == 0xC0 == 3 * 64 and at(P, 0x001FB1AC).startswith("call") and at(P, 0x001FB1B1) == "cmp byte ptr [rax + 0x1c], 0"
      and acc[1] == "ret" and rip(next(md.disasm(blob[OFF(0x00189120):OFF(0x00189120) + 16], 0x00189120))) == [0x01F7F598],
      "%s / %s; accessor %s" % (at(P, 0x001FB1AC), at(P, 0x001FB1B1), acc))
ins = bodies[0x001FB120]
back = [x.address for x in ins if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm <= x.address]
check("O6", len(ins) == 105 and sum(1 for x in ins if x.mnemonic == "movups") == 48 and not back,
      "%d instructions, %d movups, backward jumps %s" % (len(ins), sum(1 for x in ins if x.mnemonic == "movups"), back))
first_store = min(x.address for x in ins if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov")
                  and x.reg_name(x.operands[0].mem.base) != "rsp")
check("O7", "+ 0x4b4]" in at(P, 0x001FB126) and P[0x001FB13A].mnemonic.startswith("j") and 0x001FB13A < first_store,
      "%s; %s; first non-stack store %08X" % (at(P, 0x001FB126), at(P, 0x001FB13A), first_store))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
