"""uq322_families.py - UQ-322: the fourteen residue bodies of the 007EF000-007F8000 audio span, placed by their direct
call edges against the two declared families (FABLE, Claude Opus 5.5, 2026-09-27). Static.

Families: 23-Third-Party-Libraries/members/tremor-vorbisfile.tsv (Xiph Tremor + vorbisfile) and
18-Audio/members/sead-library-span.tsv (SQEX SEAD, span 007A4380-007F41A0). A residue body is placed in a family when
every family-member neighbour it has (callee or caller, direct E8/E9, following residue-to-residue edges) is in that one
family.

  F1 11 bodies place in SEAD: 007F25E0 007F0820 007F1340 007F0320 007F1A50 007EF790 007EF630 007EF3B0 007EF1E0
     007F1670 007F1960.
  F2 1 body places in Tremor: 007F7FF0 (called by Tremor 007F4A80, calls five Tremor bodies).
  F3 2 bodies stay unplaced: 007F6FB0 and 007F7350 have no family neighbour of their own; their only callers are
     007EAA60 / 007EBAD0, which are themselves called by SEAD members (007ED4C0, 007EDA60, 007B5D20), yet both bodies
     lie past the SEAD span's end 007F41A0.
  F4 (same day) the two are SEAD's own MS-ADPCM codec: 007F7350 computes 2*blockAlign/channels - 12, MS-ADPCM's
     samples per block, and 007F6FB0 reads the MS-ADPCM adaptation table (lane order 768/614/512/409,
     307/409/512/614, 307/230/230/230), the first predictor coefficient pairs (256,512,0,192 / 0,-256,0,64) and the
     -8..-1 nibble sign table; both are called only from SEAD's Voice::Initialize (007EBAD0) and 007EAA60.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"; W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def addrs(p):
    s = set()
    for l in open(p, encoding="utf-8", errors="replace"):
        m = re.match(r"\s*`?([0-9A-Fa-f]{8})`?\b", l.split("\t")[0])
        if m: s.add(int(m.group(1), 16))
    return s
tremor = addrs(DB / "23-Third-Party-Libraries/members/tremor-vorbisfile.tsv")
sead = addrs(DB / "18-Audio/members/sead-library-span.tsv")
funcs = {}
for l in (W / "graph/functions.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    f = l.split("\t"); funcs[int(f[0], 16)] = int(f[2])
RES = [0x7F25E0, 0x7F0820, 0x7F6FB0, 0x7F1340, 0x7F0320, 0x7F1A50, 0x7EF3B0, 0x7EF1E0, 0x7EF790, 0x7EF630, 0x7F7FF0, 0x7F1670, 0x7F1960, 0x7F7350]
calls = collections.defaultdict(set)
for a, sz in funcs.items():
    if not (0x780000 <= a < 0x860000): continue
    o = off(a)
    if o is None: continue
    for x in cs.disasm(d[o:o + sz], a):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"): calls[a].add(int(x.op_str, 16))
callers = collections.defaultdict(set)
for a, cc in calls.items():
    for c in cc: callers[c].add(a)
place = {}
for _ in range(4):
    for r in RES:
        nb = (calls[r] | callers[r])
        fams = {"SEAD" for c in nb if c in sead} | {"Tremor" for c in nb if c in tremor} | {place[c] for c in nb if place.get(c)}
        if len(fams) == 1: place[r] = next(iter(fams))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
S = sorted(r for r in RES if place.get(r) == "SEAD"); T = sorted(r for r in RES if place.get(r) == "Tremor")
U = sorted(r for r in RES if r not in place)
check("F1 eleven bodies place in SEAD", S == sorted([0x7F25E0, 0x7F0820, 0x7F1340, 0x7F0320, 0x7F1A50, 0x7EF790, 0x7EF630, 0x7EF3B0, 0x7EF1E0, 0x7F1670, 0x7F1960]), " ".join("%08X" % x for x in S))
check("F2 one body places in Tremor", T == [0x7F7FF0] and 0x7F4A80 in callers[0x7F7FF0] and len(calls[0x7F7FF0] & tremor) == 5)
cl = {c for r in U for c in callers[r]}
check("F3 two stay unplaced: called only from SEAD-called bodies, past the SEAD span's end",
      U == [0x7F6FB0, 0x7F7350] and cl == {0x7EAA60, 0x7EBAD0}
      and callers[0x7EAA60] <= sead and callers[0x7EBAD0] <= sead and all(r > 0x7F41A0 for r in U),
      "callers %s" % sorted("%08X" % c for c in cl))
# F4 (added 2026-09-27, same session): the two unplaced bodies are SEAD's MS-ADPCM codec.
dd = dict((x.address, ("%s %s" % (x.mnemonic, x.op_str)).strip()) for x in cs.disasm(d[off(0x7F7350):off(0x7F735F)], 0x7F7350))
spb = dd.get(0x7F7353) == "lea eax, [rcx + rcx]" and dd.get(0x7F7358) == "div r8d" and dd.get(0x7F735B) == "sub eax, 0xc"
i32 = lambda va, k: list(struct.unpack_from("<%di" % k, d, off(va)))
tables = (i32(0x1CBAB20, 4) == [768, 614, 512, 409] and i32(0x1CBAB30, 4) == [307, 409, 512, 614]
          and i32(0x1CBAB10, 4) == [307, 230, 230, 230] and i32(0x1CBAB00, 4) == [256, 512, 0, 192]
          and i32(0x1CBAAF0, 4) == [0, -256, 0, 64] and i32(0x1CBAB40, 8) == [-8, -7, -6, -5, -4, -3, -2, -1])
refs = set()
for x in cs.disasm(d[off(0x7F6FB0):off(0x7F6FB0) + funcs[0x7F6FB0]], 0x7F6FB0):
    m = re.search(r"\[rip \+ 0x([0-9a-f]+)\]", x.op_str)
    if m: refs.add(x.address + x.size + int(m.group(1), 16))
check("F4 the two are SEAD's MS-ADPCM codec: samples per block = 2*blockAlign/ch - 12, and the decoder reads the MS-ADPCM adaptation and coefficient tables",
      spb and tables and {0x1CBAB00, 0x1CBAB10, 0x1CBAB20, 0x1CBAB30, 0x1CBAB40, 0x1CBAAF0} <= refs
      and 0x7F7350 in calls[0x7EBAD0] and 0x7F7350 in calls[0x7EAA60] and 0x7F6FB0 in calls[0x7EAA60])
print("FAILS", fails)
sys.exit(1 if fails else 0)
