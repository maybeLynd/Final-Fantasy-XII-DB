"""Falsification pass 1 on CONTRACT-stat-derivation (OPUS, 2026-09-29), from the shipping image. Killers first.

  D0  section 2: 002FEF30 is 2,859 B and decodes to 735 instructions
  D2  D-2: the six cap immediates sit at the cited sites (0x270F, 0x3B9ACA00, 0x7FFF, 0x3E7, 0x63, 0xFF)
  D3  D-3: `test edi, edi / mov r8d, 0x270f / mov eax, 0x3b9aca00 / cmove eax, r8d`, then the store to [rsi] at 002FF7E2
  D4  D-4: 002FF7E5 `cmp [rsp + 0x5c], ebp / je 002FF808`; then `cmovg r15, r9` and a second store to [rsi] at 002FF805
  D5  D-5: the three sites each read two effect-layer displacements, the same pair at all three
  D7  D-7: the cancel 003105D0 is called; the tail's guards (002FF970 jne 002FFA45, 002FF978 je, 002FF982..002FF98E the
      0x8000020 mask) precede the writes at 002FFA14 / 002FFA22 / 002FFA38 (0x200000) and the call 00307D10 at 002FFA40
"""
import io, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

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
F = 0x002FEF30
b = list(md.disasm(blob[OFF(F):OFF(F) + sizes[F]], F))
at = lambda va: next((S(x) for x in b if x.address == va), "?")
run = lambda lo, hi: [S(x) for x in b if lo <= x.address <= hi]

check("D0", sizes[F] == 2859 and len(b) == 735, "%d B, %d instructions" % (sizes[F], len(b)))
caps = {0x002FF7BD: "0x270f", 0x002FF7C3: "0x3b9aca00", 0x002FF7F5: "0x7fff", 0x002FF817: "0x3e7", 0x002FF829: "0x63", 0x002FF8D6: "0xff"}
got = {("%08X" % a): at(a) for a in caps}
check("D2", all(at(a).endswith(v) for a, v in caps.items()), "%s" % got)
check("D3", run(0x002FF7BB, 0x002FF7C8) == ["test edi, edi", "mov r8d, 0x270f", "mov eax, 0x3b9aca00", "cmove eax, r8d"]
      and at(0x002FF7E2) == "mov dword ptr [rsi], r8d", "one cmove picks the cap; store at 002FF7E2")
check("D4", run(0x002FF7E5, 0x002FF7E9) == ["cmp dword ptr [rsp + 0x5c], ebp", "je 0x2ff808"] and at(0x002FF801) == "cmovg r15, r9"
      and at(0x002FF805) == "mov dword ptr [rsi], r15d", "conditional recomputation overwrites [rsi] at 002FF805")
pairs = []
for a, c in ((0x002FF5CA, 0x002FF5D1), (0x002FF668, 0x002FF66F), (0x002FF708, 0x002FF70F)):
    xa = next(x for x in b if x.address == a); xc = next(x for x in b if x.address == c)
    da = [o.mem.disp for o in xa.operands if o.type == X86_OP_MEM]; dc = [o.mem.disp for o in xc.operands if o.type == X86_OP_MEM]
    pairs.append((tuple(da), tuple(dc)))
check("D5", len(set(pairs)) == 1 and all(p[0] and p[1] and p[0] != p[1] for p in pairs), "displacement pairs %s" % [(tuple(hex(d) for d in p[0]), tuple(hex(d) for d in p[1])) for p in pairs])
calls = [S(x) for x in b if x.mnemonic == "call"]
tail = run(0x002FF970, 0x002FF98E)
check("D7", "call 0x3105d0" in calls and any(s == "jne 0x2ffa45" for s in tail) and any("0x8000020" in s for s in tail)
      and at(0x002FFA38).endswith("0x200000") and at(0x002FFA40) == "call 0x307d10" and at(0x002FFA14) != "?" and at(0x002FFA22) != "?",
      "cancel called; guards %s; tail %s / %s" % (tail[:6], at(0x002FFA38), at(0x002FFA40)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
