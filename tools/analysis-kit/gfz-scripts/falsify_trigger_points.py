"""Falsification pass 1 on CONTRACT-authored-trigger-points (OPUS, 2026-09-29), from the shipping image. Killers first.

  P0  section 2: 002F8060 is 648 B
  P1  TP-1: two `divss` by 10.0 (002F81D0, 002F81E5); 002F81F4 `comiss xmm7, xmm0` with xmm7 = [00901B34] = 1.2999999523162842
  P2  TP-2: the unit's height is overwritten with edi = 0 at 002F8150 and the point's is written 0 at 002F81C1
  P3  TP-3: 002F8231 `cmp r8d, 0x4b`
  P4  TP-5: 002F80BC `mov ebx, 0x20`
  P5  TP-6: 002F80DA / 002F80E4 test bit 0x20 of +0x6C and +0x7C; 002F8113 `cmp al, 0xc`
  P6  TP-7: image-wide, the bodies that call both 00379CD0 and one of the seven PersistentFlag_Set* entries are exactly
      002F8060 and 002FAFD0
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
callees = collections.defaultdict(set)
F = 0x002F8060
body = None
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    if fa == F:
        body = ins
    for x in ins:
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            callees[fa].add(T(x))
I = {x.address: x for x in body}
at = lambda va: S(I[va]) if va in I else "?"
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]

check("P0", sizes[F] == 648, "%d B" % sizes[F])
ten = rip(I[0x002F818D])[0] if 0x002F818D in I and rip(I[0x002F818D]) else None
thr = [t for x in body if x.mnemonic == "movss" and x.op_str.startswith("xmm7,") for t in rip(x)]
check("P1", ten and f32(ten) == 10.0 and at(0x002F81D0).startswith("divss") and at(0x002F81E5).startswith("divss") and at(0x002F81F4) == "comiss xmm7, xmm0"
      and thr == [0x00901B34] and repr(f32(0x00901B34)) == "1.2999999523162842",
      "10.0 at %s; threshold [%s] = %r" % ("%08X" % ten if ten else "?", ["%08X" % t for t in thr], f32(0x00901B34)))
check("P2", at(0x002F8150) == "mov dword ptr [rsp + 0x54], edi" and at(0x002F81C1) != "?" and (", 0" in at(0x002F81C1) or "edi" in at(0x002F81C1)),
      "unit height %s; point height %s" % (at(0x002F8150), at(0x002F81C1)))
check("P3", at(0x002F8231) == "cmp r8d, 0x4b", at(0x002F8231))
check("P4", at(0x002F80BC) == "mov ebx, 0x20", at(0x002F80BC))
check("P5", "0x20" in at(0x002F80DA) and "+ 0x6c]" in at(0x002F80DA) and "0x20" in at(0x002F80E4) and "+ 0x7c]" in at(0x002F80E4) and at(0x002F8113) == "cmp al, 0xc",
      "%s / %s / %s" % (at(0x002F80DA), at(0x002F80E4), at(0x002F8113)))
setters = {a for a, n in names.items() if n.startswith("PersistentFlag_Set")}
both = sorted("%08X" % f for f, cs in callees.items() if 0x00379CD0 in cs and cs & setters)
check("P6", len(setters) == 7 and both == ["002F8060", "002FAFD0"], "%d setters; bodies drawing and setting: %s" % (len(setters), both))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
