"""surfaces.py - control for D-5 (FABLE, Claude Opus 5.5, 2026-09-26): what the three reserved 512x448 surfaces are.

  S1 0036D280 seeds width 0x200 (022D8EAC), height 0x1C0 (022D8EB4) and the frame index 0 (022D8EA8); 0036D2F0 computes
     pages-per-surface = (height * width) >> 11 into 022D8EB8 (a GS page is 2048 words): 512*448/2048 = 112.
  S2 0036D400 composes FRAME_1 = index * pages | (width >> 6) << 16 (FBP, FBW; PSM 0 = PSMCT32) into 022D8EC8 and
     ZBUF_1 = (2 * pages) | 1 << 24 (ZBP = the THIRD surface, PSM 1 = Z24) into 022D8ED0, and emits them as GS register
     records 0x4C and 0x4E.
  S3 the frame index 022D8EA8 has exactly one rip-relative write, the seed's 0 (0036D290), so FRAME_1 targets the
     first surface; the second is selected only by an index of 1, which nothing in that domain stores.
Planted negative: S2 asserts ZBP is NOT index-scaled (a matcher that credited any imul would fail).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
from array import array
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
STARTS = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
                errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def whole(a):
    i = bisect.bisect_right(STARTS, a)
    return list(cs.disasm(d[off(a):off(STARTS[i])], a))
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
def T(a): return ["%s %s" % (x.mnemonic, x.op_str) for x in whole(a)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

seed = {rip(x): x.op_str.split(", ")[1] for x in whole(0x36D280) if x.mnemonic == "mov" and rip(x)}
check("S1 seed: width 0x200, height 0x1c0, frame index 0",
      seed.get(0x22D8EAC) == "0x200" and seed.get(0x22D8EB4) == "0x1c0" and seed.get(0x22D8EA8) == "eax"
      and "xor eax, eax" in T(0x36D280), str({hex(k): v for k, v in seed.items() if k in (0x22D8EAC, 0x22D8EB4, 0x22D8EA8)}))
P = whole(0x36D2F0); PT = ["%s %s" % (x.mnemonic, x.op_str) for x in P]
loads = {rip(x): x.op_str.split(",")[0] for x in P if x.mnemonic == "mov" and rip(x) in (0x22D8EB4, 0x22D8EAC)}
check("S1 pages = (h * w) >> 11 into 022D8EB8",
      loads == {0x22D8EB4: "edi", 0x22D8EAC: "ebx"} and "imul edi, ebx" in PT and "sar eax, 0xb" in PT
      and any(x.mnemonic == "mov" and rip(x) == 0x22D8EB8 for x in P) and (512 * 448) >> 11 == 112)
F = whole(0x36D400); FT = ["%s %s" % (x.mnemonic, x.op_str) for x in F]
def seq(lst, s):
    i = 0
    for v in lst:
        if i < len(s) and v == s[i]: i += 1
    return i == len(s)
check("S2 FRAME_1 = idx*pages | (w>>6)<<16",
      seq(FT, ["mov edi, dword ptr [rip + 0x1f6ba7d]", "mov eax, dword ptr [rip + 0x1f6ba50]", "mov r8d, dword ptr [rip + 0x1f6ba41]",
               "imul eax, r8d", "movsxd rdx, eax", "sar eax, 6", "shl rcx, 0x10", "or rdx, rcx"]))
check("S2 ZBUF_1 = 2*pages | 1<<24 (planted negative: not index-scaled)",
      seq(FT, ["lea eax, [r8 + r8]", "movsxd rcx, eax", "bts rcx, 0x18"]) and not seq(FT, ["imul eax, r8d", "lea eax, [rax + rax]"]))
stores = {rip(x): x.op_str.split(", ")[1] for x in F if x.mnemonic == "mov" and rip(x) in (0x22D8EC8, 0x22D8ED0)
          and x.op_str.startswith("qword ptr [rip")}   # stores only; the later r8 loads read them back
check("S2 stored to 022D8EC8 (rdx) / 022D8ED0 (rcx) and emitted as tags 0x4C / 0x4E",
      stores.get(0x22D8EC8) == "rdx" and stores.get(0x22D8ED0) == "rcx"
      and "mov qword ptr [rdx + 8], 0x4c" in FT and "mov qword ptr [rdx + 8], 0x4e" in FT)
_, va, rs, ro = [s for s in [(0,) + secs[i][1:] for i in range(n)] if s[1] <= 0x1000 < s[1] + s[2]][0]
cell = 0x22D8EA8
want = {cell - 4 - k - (BASE + va) + ro: k for k in (0, 1, 2, 4)}
cand = set()
for sft in range(4):
    a = array("i"); a.frombytes(d[ro + sft: ro + sft + ((rs - sft) // 4) * 4])
    for i, v in enumerate(a):
        if v + ro + sft + 4 * i in want: cand.add(BASE + va + sft + 4 * i)
writes = []
for c in cand:
    f = STARTS[bisect.bisect_right(STARTS, c) - 1]
    for x in cs.disasm(d[off(f):off(c) + 16], f):
        if x.address <= c < x.address + x.size and rip(x) == cell and x.op_str.startswith("dword ptr [rip"):
            writes.append(x.address)
check("S3 the frame index has one rip-relative write, the seed (0036D290)", sorted(set(writes)) == [0x36D290],
      str([hex(w) for w in sorted(set(writes))]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
