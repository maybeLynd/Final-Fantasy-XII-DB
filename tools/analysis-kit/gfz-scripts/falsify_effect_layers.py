"""Falsification pass 1 on CONTRACT-effect-layers (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. Layer censuses count every byte
of each 16-byte layer ([0x68, 0x78) and [0x78, 0x88)), not only the first displacement, over each body's chained extent.

  V0  section 2: 553 / 1,787 / 273 B, and each body's .pdata chain union equals its catalogue size
  V1  addressing: 0030E19C `shr rbx, 3`, 0030E1A4 `and r15d, 7`; the mode (edi) selects the layer: 0 clears +0x68, 1 clears
      +0x78, 2 sets +0x68, 3 sets +0x78 (0030E1EB..0030E24E)
  K1  (REFUTES L-1's "never touches the mutable one" and its census "+0x78 at 3 sites, +0x68 at zero") the rebuild reads
      effect id 39 of BOTH layers - `movzx edx, byte ptr [rbx + 0x6c]` / `js` at 0031050B and 00310541 (mutable byte 4, bit 7)
      and `cmp byte ptr [rbx + 0x7c], r14b` / `jl` at 00310513, 0031052E, 00310549, 00310572 (derived byte 4, bit 7), with rbx
      the record (0030FF0F) - as the gate that zeroes the clamp bound for the record words +0x4C (0031053D) and +0x06
  V2  L-1's write side survives: the rebuild stores nothing into [rbx + 0x68, rbx + 0x88); its reconcile loop (00310303..00310336)
      writes only the two stack buffers; it changes the derived layer only through 0030E130 with modes 3 (00310366) and 1
      (00310387) and flags r15 = edx | 0x202 (0030FEFB)
  V3  L-2: 0030E130 reaches the mutable layer at 5 sites and the derived at 6; 0030E269..0030E275 recompute "in either layer"
      and 0030E27B compares it with the value before
  V4  L-3: 00384851 `cmp r10d, 0x80`; 00384827 tests [r9 + r11 + 0x68], 00384831 tests [r9 + r11 + 0x78]; 0038484C ORs into ctx
  V5  L-5: the asm block at 0038488C..003848B8 as quoted
  V6  section 5: 00384870 stores the target's owning unit into 02EBF188
  V7  L-6, now measured: the loop forms diff = desired XOR current, add = diff & desired (rsp + 0x50), remove = diff & current
      (rsp + 0x60), and the id loop to 0x80 calls mode 3 for each add bit and mode 1 for each remove bit
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
at = lambda I, a: S(I[a]) if a in I else "?"
pd = next(x for x in SECS if x[0] == ".pdata"); praw = blob[pd[3]:pd[3] + pd[4]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    if b_:
        pent[BASE + b_] = (BASE + e_, BASE + u_)


def root(bg):
    seen = set()
    while bg in pent and bg not in seen:
        seen.add(bg); u = pent[bg][1]; h = blob[OFF(u):OFF(u) + 4]
        if not (h[0] >> 3) & 4:
            return bg
        c = OFF(u) + 4 + 2 * ((h[2] + 1) & ~1); bg = BASE + struct.unpack("<I", blob[c:c + 4])[0]
    return bg


def extent(fa):
    fr = [(b_, pent[b_][0]) for b_ in pent if fa <= b_ < fa + 0x4000 and root(b_) == fa]
    return (max(e for _, e in fr) - fa) if fr else sizes[fa]


MUT, REB, MRG = 0x0030E130, 0x0030FED0, 0x003847C0
ext = {f: extent(f) for f in (MUT, REB, MRG)}
body = {f: {x.address: x for x in md.disasm(blob[OFF(f):OFF(f) + ext[f]], f)} for f in (MUT, REB, MRG)}


def layer_hits(I, base):
    h = {"mut": [], "der": []}
    for a, x in sorted(I.items()):
        for o in x.operands:
            if o.type == X86_OP_MEM and x.reg_name(o.mem.base) == base and not o.mem.index:
                if 0x68 <= o.mem.disp < 0x78:
                    h["mut"].append(a)
                elif 0x78 <= o.mem.disp < 0x88:
                    h["der"].append(a)
    return h


check("V0", [sizes[f] for f in (MUT, REB, MRG)] == [553, 1787, 273] and all(ext[f] == sizes[f] for f in ext), "sizes %s; chain unions %s" % ([sizes[f] for f in (MUT, REB, MRG)], [ext[f] for f in (MUT, REB, MRG)]))
M = body[MUT]
check("V1", at(M, 0x0030E19C) == "shr rbx, 3" and at(M, 0x0030E1A4) == "and r15d, 7" and at(M, 0x0030E24A) == "btr eax, r15d" and at(M, 0x0030E24E) == "mov byte ptr [rbx + 0x68], al"
      and at(M, 0x0030E202) == "movzx eax, byte ptr [rbx + 0x78]" and at(M, 0x0030E212) == "mov byte ptr [rbx + 0x78], al" and at(M, 0x0030E217) == "movzx eax, byte ptr [rbx + 0x68]"
      and at(M, 0x0030E235) == "btr eax, r15d" and at(M, 0x0030E239) == "mov byte ptr [rbx + 0x78], al",
      "mode 0 clears +0x68, 1 clears +0x78, 2 sets +0x68, 3 sets +0x78")
R = body[REB]
h = layer_hits(R, "rbx")
check("K1", at(R, 0x0030FF0F) == "mov rbx, rcx" and h["mut"] == [0x0031050B, 0x00310541] and all(at(R, a) == "movzx edx, byte ptr [rbx + 0x6c]" for a in h["mut"])
      and [R[a + 4].mnemonic if a + 4 in R else "?" for a in h["mut"]] == ["test", "test"] and at(R, 0x00310511) == "js 0x31051f"
      and all(at(R, a) == "cmp byte ptr [rbx + 0x7c], r14b" for a in (0x00310513, 0x0031052E, 0x00310549, 0x00310572)) and at(R, 0x0031053D) == "mov word ptr [rbx + 0x4c], ax",
      "(REFUTES 'never touches the mutable one' and '+0x68 at zero') record-based layer accesses: mutable %s, derived %s; the id-39 gate zeroes "
      "the bound for +0x4C (%s)" % (["%08X" % a for a in h["mut"]], ["%08X" % a for a in h["der"]], at(R, 0x0031053D)))
stores = [a for a, x in R.items() if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov")
          and x.reg_name(x.operands[0].mem.base) == "rbx" and 0x68 <= x.operands[0].mem.disp < 0x88]
loop_st = [S(R[a]) for a in sorted(R) if 0x00310310 <= a <= 0x00310336 and R[a].operands and R[a].operands[0].type == X86_OP_MEM and R[a].mnemonic == "mov"]
mcalls = [a for a, x in R.items() if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == MUT]
check("V2", not stores and loop_st == ["mov byte ptr [r11 + r9 - 0x79], al", "mov byte ptr [rsi + r9 - 0x79], dl"]
      and at(R, 0x003102E5) == "lea r11, [rsp + 0x50]" and at(R, 0x003102FB) == "lea rsi, [rsp + 0x60]"
      and at(R, 0x00310366) == "mov dword ptr [rsp + 0x20], 3" and at(R, 0x00310387) == "mov dword ptr [rsp + 0x20], r13d" and at(R, 0x0030FF12) == "lea r13d, [rax + 1]"
      and at(R, 0x0030FEFB) == "or r15d, 0x202" and sorted(mcalls) == [0x00310378, 0x00310396],
      "direct stores into either layer %s; loop stores %s (stack buffers); mutate calls %s with modes 3 and 1, flags | 0x202" % (stores, loop_st, ["%08X" % a for a in sorted(mcalls)]))
hm = layer_hits(M, "rbx")
check("V3", len(hm["mut"]) == 5 and len(hm["der"]) == 6 and at(M, 0x0030E269) == "test byte ptr [rbx + 0x68], sil" and at(M, 0x0030E26F) == "test byte ptr [rbx + 0x78], sil"
      and at(M, 0x0030E27B) == "cmp r13d, dword ptr [rsp + 0x30]", "mutable %d, derived %d; either-layer recompute and compare" % (len(hm["mut"]), len(hm["der"])))
G = body[MRG]
check("V4", at(G, 0x00384851) == "cmp r10d, 0x80" and at(G, 0x00384827) == "test byte ptr [r9 + r11 + 0x68], dl" and at(G, 0x00384831) == "test byte ptr [r9 + r11 + 0x78], dl"
      and G[0x0038484C].mnemonic == "or" and "0x1a" in G[0x0038484C].op_str, "%s | %s | %s | %s" % (at(G, 0x00384851), at(G, 0x00384827), at(G, 0x00384831), at(G, 0x0038484C)))
check("V5", at(G, 0x0038488C) == "call 0x31b860" and at(G, 0x00384894) == "jne 0x3848a1" and at(G, 0x00384896) == "and dword ptr [rbx + 8], 0xffffefff"
      and at(G, 0x0038489D) == "and byte ptr [rbx + 0x1b], 0x7f" and at(G, 0x003848A1) == "test byte ptr [rsi], 0x20" and at(G, 0x003848A6) == "and dword ptr [rbx + 8], 0xff7eefff"
      and at(G, 0x003848AD) == "cmp word ptr [rbx + 0x18], 0xd" and at(G, 0x003848B8) == "and byte ptr [rbx + 0x1b], 0x7f", "both revocation conditions as quoted")
check("V6", rip(G[0x00384870]) == [0x02EBF188] and G[0x00384870].operands[0].type == X86_OP_MEM, at(G, 0x00384870))
ls = [S(R[a]) for a in sorted(R) if 0x00310310 <= a < 0x00310324]
check("V7", ls == ["movzx edx, byte ptr [rdi + r9 - 0x78]", "xor dl, byte ptr [r9]", "lea r9, [r9 + 1]", "movzx eax, dl", "and dl, byte ptr [r9 - 1]"]
      and at(R, 0x00310324) == "and al, byte ptr [rdi + r9 - 0x79]" and at(R, 0x003102F0) == "lea rdi, [rsp + 0x40]" and at(R, 0x0031035C) == "test byte ptr [rsp + rbp + 0x50], sil"
      and at(R, 0x0031037D) == "test byte ptr [rsp + rbp + 0x60], sil" and at(R, 0x0031039D) == "cmp edi, 0x80",
      "diff = desired (rsp+0x40) ^ current; add = diff & desired -> rsp+0x50 (mode 3); remove = diff & current -> rsp+0x60 (mode 1); ids to 0x80")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
