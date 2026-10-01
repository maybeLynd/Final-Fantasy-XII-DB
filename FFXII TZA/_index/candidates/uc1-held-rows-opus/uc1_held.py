"""uc1_held.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Evidence for UC-1's HELD rows; it
proposes nothing about the population and changes no ledger. The held rows are read from the two applied-population files
(99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-1-64.tsv and -65-256.tsv, 4 + 21 = 25); the listed bodies
come from FABLE's instrument through uc1_band_65_256.py's own prefix, unchanged.

  H  THE POPULATION: 25 held rows, 4 + 21, as the applied files declare them
  T  SWITCH DATA OF THE LISTED BODY BEFORE IT: the listed body ending at (or just before) the held start dispatches with
     `movzx eax, byte ptr [base + rax + IDX]` then `mov r32, dword ptr [base + rax*4 + TAB]`, where TAB is the held start
     rounded up to 4 and IDX = TAB + 4 * n; the n dwords at TAB are image-base RVAs back into that listed body (the case
     targets), and the byte table at IDX holds only values below n. For 7 rows the index table runs exactly to the held
     block's end, so the whole block is that function's switch data, not code: 00253BF5, 003222C2, 003A9350, 00441A8F,
     004FF3CD, 005FD624, 007298DD. For 00208628 the same two tables cover only its first 60 of 168 bytes; the rest stays open
  M  MID-INSTRUCTION SLICES: 8 rows (001358E0, 00135EC0, 00136DB0, 00137390, 00138280, 00138860, 0013A660, 0013B5D0) begin
     at the imm8 byte of a 6-byte `palignr xmm1, xmm4, imm` at start - 5 (imm = the block's first byte: 0, 1, 5, 6, 10, 11,
     5, 12), in the 00125740..00158DA0 stretch that has no unwind entries at all
  C  CONTROL for M: every linear decode begun at each of the 0x200 - 5 offsets before a slice either fails or lands on
     start - 5; none lands on the held start itself
  R  THE REST, named: the 9 rows neither T nor M decides - 00125770 (non-leaf, no unwind, as FABLE held it), 00148BB3,
     00148D64, 001491CE, 001492FF, 00158C97 (all in the unwind-free stretch), 007137BC, 0071B6B0, 00809D65 - plus 00208628's
     remaining 108 bytes
Not claimed: the routines the slices belong to, their true entries, or anything about the 257+ band's held rows.
Usage: python uc1_held.py
"""
import bisect, collections, io, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); CAND = os.path.abspath(os.path.join(HERE, ".."))
DB = os.path.abspath(os.path.join(CAND, "..", ".."))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
BAND = os.path.join(CAND, "uc1-band-65-256", "uc1_band_65_256.py")
g = {"__file__": BAND, "__name__": "uc1_band_prefix"}
exec(compile(io.open(BAND, encoding="utf-8").read().split("rows = [l.rstrip")[0], BAND, "exec"), g)   # FABLE's listed set and the certified image
d, off, B, listed = g["d"], g["off"], g["B"], g["listed"]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
UC = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code")
held = []
for f in ("uc1-applied-population-1-64.tsv", "uc1-applied-population-65-256.tsv"):
    for l in io.open(os.path.join(UC, f), encoding="utf-8"):
        c = l.rstrip("\n").split("\t")
        if c[0] == "held": held.append((int(c[1], 16), int(c[3], 16), f))
check("H", len(held) == 25 and collections.Counter(f for *_, f in held) == {"uc1-applied-population-1-64.tsv": 4, "uc1-applied-population-65-256.tsv": 21},
      "25 held rows (4 + 21) read from the applied files")
L = sorted(listed); st = [a for a, s in L]
def body_before(h): return L[bisect.bisect_right(st, h) - 1]
Tres = {}
for h, e, f in held:
    a, s = body_before(h)
    tab = (h + 3) & ~3; n = 0
    while tab + 4 * (n + 1) <= e and a <= struct.unpack_from("<I", d, off(tab + 4 * n))[0] + B < h: n += 1
    if n < 2: continue
    idx = tab + 4 * n; rest = d[off(idx):off(e)]; run = 0
    for b in rest:
        if b < n: run += 1
        else: break
    xs = list(cs.disasm(d[off(a):off(a + s)], a))
    ui = [x for x in xs if x.mnemonic == "movzx" and re.search(r"\+ rax \+ 0x%x\]" % (idx - B), x.op_str)]
    ut = [x for x in xs if x.mnemonic == "mov" and re.search(r"\+ rax\*4 \+ 0x%x\]" % (tab - B), x.op_str)]
    if ui and ut: Tres[h] = (n, run, len(rest), ui[0].address, ut[0].address)
whole = sorted(h for h, v in Tres.items() if v[1] == v[2])
check("T", whole == [0x253BF5, 0x3222C2, 0x3A9350, 0x441A8F, 0x4FF3CD, 0x5FD624, 0x7298DD] and 0x208628 in Tres and Tres[0x208628][1] == 52
      and all(v[0] == 2 for v in Tres.values()),
      "switch data read by the listed body's own dispatch (movzx at / mov at): %s; whole block for %d, 00208628 tables = %d of %d bytes" %
      ({"%08X" % h: ("%08X" % v[3], "%08X" % v[4]) for h, v in sorted(Tres.items())}, len(whole), 8 + Tres[0x208628][1], 8 + Tres[0x208628][2]))
SL = [0x1358E0, 0x135EC0, 0x136DB0, 0x137390, 0x138280, 0x138860, 0x13A660, 0x13B5D0]
mid = []
for h in SL:
    x = next(cs.disasm(d[off(h - 5):off(h + 11)], h - 5), None)
    mid.append(x is not None and x.mnemonic == "palignr" and x.size == 6 and x.op_str == "xmm1, xmm4, %s" % (hex(d[off(h)]) if d[off(h)] > 9 else str(d[off(h)])))
import pefile
pe = pefile.PE(g["EXE"] if "EXE" in g else os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"))
ex = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]; pd = pe.get_data(ex.VirtualAddress, ex.Size)
pstarts = sorted(struct.unpack_from("<I", pd, i)[0] + B for i in range(0, len(pd) - 11, 12))
k = bisect.bisect_right(pstarts, 0x125740)
nopdata = all(not (0x125740 < p < 0x158DA0) for p in pstarts)
check("M", all(mid) and set(h for h, e, f in held) >= set(SL) and nopdata,
      "8 slices begin at the imm8 of palignr xmm1, xmm4, imm at start - 5 (imms %s); no unwind entry begins inside 00125740..00158DA0" % [d[off(h)] for h in SL])
conv = collections.Counter()
for h in SL:
    for s in range(h - 0x200, h - 5):
        land = "fail"
        for x in cs.disasm(d[off(s):off(h + 8)], s):
            if x.address == h - 5: land = "start-5"; break
            if x.address == h: land = "start"; break
            if x.address > h: land = "past"; break
        conv[land] += 1
check("C", conv["start"] == 0 and conv["past"] == 0 and conv["start-5"] > 2 * conv["fail"],
      "decode convergence over 8 x 0x1FB offsets: %s" % dict(conv))
decided = set(whole) | set(SL)
rest = sorted(h for h, e, f in held if h not in decided)
check("R", [("%08X" % h) for h in rest] == ["00125770", "00148BB3", "00148D64", "001491CE", "001492FF", "00158C97", "00208628", "007137BC", "0071B6B0", "00809D65"],
      "undecided here: %s (00208628 only past its tables)" % ["%08X" % h for h in rest])
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
