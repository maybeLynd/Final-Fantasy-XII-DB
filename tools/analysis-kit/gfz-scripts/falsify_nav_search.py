"""Falsification pass 1 on CONTRACT-navigation-search-and-follow (OPUS, 2026-09-29), from the shipping image. Killers first.

  N0  section 2: sizes 1,575 / 204 / 632 / 40 / 84 for 00382FF0, 00383670, 00383C90, 0030A130, 003278D0
  N1  NV-1: 003839F0 (route wipe) has three calling sites and 003839C0 (dead-end wipe) two; 003291B0 calls only 003839F0 (003291CF)
  N2  NV-2: 003278D0 tests `byte ptr [rax], 0x10` (003278F2), calls both wipers (00327901, 00327909) and calls the slot count
      inside the loop (00327910)
  N3  NV-4: 003842E0 has exactly two call sites, 0038351C (in 00382FF0) and 00383EB1 (in 00383C90); 00382EA0 has four sites in
      three functions, two of them in 00383C90
  N4  NV-5: 0030A130 is `maxss` of two radii with no multiply; its callers multiply by the f32 at 00D10818 = 0x3FB4FDF4 (1.414),
      at 00325BFA and 00325C49
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
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
calls_to = collections.defaultdict(list)
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    bodies[fa] = list(md.disasm(code, fa))
    for x in bodies[fa]:
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address))
at = lambda fa, va: next(S(x) for x in bodies[fa] if x.address == va)
sites = lambda t: sorted((("%08X" % f), ("%08X" % a)) for f, a in calls_to[t])

# N0
sz = [sizes.get(f) for f in (0x00382FF0, 0x00383670, 0x00383C90, 0x0030A130, 0x003278D0)]
check("N0", sz == [1575, 204, 632, 40, 84], "%s" % sz)
# N1
r, d = sites(0x003839F0), sites(0x003839C0)
check("N1", len(r) == 3 and len(d) == 2 and ("003291B0", "003291CF") in r and "003291B0" not in {f for f, _a in d}, "route wipe <- %s; dead-end wipe <- %s" % (r, d))
# N2
w = bodies[0x003278D0]
cs = [(x.address, T(x)) for x in w if x.mnemonic == "call"]
back = [x for x in w if x.mnemonic.startswith("j") and T(x) is not None and T(x) < 0x003278F2 and x.address > 0x00327910]
check("N2", at(0x003278D0, 0x003278F2) == "test byte ptr [rax], 0x10"
      and {t for a, t in cs if a in (0x00327901, 0x00327909)} == {0x003839F0, 0x003839C0} and any(a == 0x00327910 for a, _t in cs) and back,
      "flag test, both wipers %s, slot count re-read at 00327910 inside the loop" % [("%08X" % a, "%08X" % t) for a, t in cs])
# N3
c = sites(0x003842E0); e = calls_to[0x00382EA0]
check("N3", c == [("00382FF0", "0038351C"), ("00383C90", "00383EB1")] and len(e) == 4 and len({f for f, _a in e}) == 3
      and sum(1 for f, _a in e if f == 0x00383C90) == 2, "003842E0 <- %s; 00382EA0 %d sites in %d functions" % (c, len(e), len({f for f, _a in e})))
# N4
g = [S(x) for x in bodies[0x0030A130]]
mul = [(("%08X" % x.address), S(x)) for f in {f for f, _a in calls_to[0x0030A130]} for x in bodies[f] if x.mnemonic == "mulss" and 0x00D10818 in rip(x)]
raw = struct.unpack("<I", blob[OFF(0x00D10818):OFF(0x00D10818) + 4])[0]
check("N4", any(s.startswith("maxss") for s in g) and not any(s.startswith("mulss") for s in g) and raw == 0x3FB4FDF4
      and [a for a, _s in sorted(mul)] == ["00325BFA", "00325C49"], "0030A130 %s; multipliers %s; [00D10818] = %08X" % (g, mul, raw))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
