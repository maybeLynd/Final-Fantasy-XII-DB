"""uc1_held2.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Part 2 of the held-row evidence: the nine rows
Part 1 (uc1_held.py R) left open, and the last 108 bytes of 00208628. Evidence only: it changes no population, ledger or
denominator, and proposes nothing FABLE has not ruled.

  P  PADDING BEFORE ROUTINES: 00148D64, 00148BB3, 001491CE, 001492FF, 00809D65 each begin where the previous listed
     function ends. The block decodes contiguously into NOP-class fill and routines; every routine starts on a 16-byte
     boundary, is unlisted, and ends in `ret` / `repz ret`. The first routine starts at the first boundary (00148D70,
     00148BC0, 001491D0, 00149300, 00809D70), not at the held start, and two blocks hold a second routine (00148C00,
     00149220)
  E  AN ENTRY AT THE HELD START: 00125770 and 0071B6B0 follow int3 fill and are 16-aligned; 00158C97 follows the previous
     function's `ret` directly and opens with `push rbp / mov rbp, rsp`; 00125770 and 00158C97 keep an rbp frame (00125770
     also saves xmm6 / xmm7) with no unwind entry and no call - leaf routines in the hand-written-assembly shape
  S  SWITCH ARMS AND TABLE OF THE PREVIOUS FUNCTION: 007137BC follows 00713760's `jmp rcx`; 00713760 loads
     `mov ecx, [r8 + rax*4 + TAB]` for an index of 0..0xD, and TAB = 007137E0 inside the block holds 14 RVAs running exactly to
     the block's end, every one landing on the arms before it (`xor eax, eax / ret`, `mov eax, 3 / ret`, ...): arms and data
     of 00713760, no entry of its own
  T  A SECOND SWITCH TABLE: 002085B0 dispatches a second time with TAB = 00208664 (4 RVAs into 002085B0) and IDX =
     00208674, whose values are all below 4 and which runs to 002086D0, the held block's end - so all 168 bytes of
     00208628 are 002085B0's data
  R  REFERENCES to each entry E / P names: rel32 call / jmp, RIP-relative lea, absolute qword, 4-byte RVA (reported, not
     required - leaf SIMD routines are typically reached through function-pointer tables)
Not claimed: what the routines compute, who calls them at run time, or any disposition of the rows (FABLE rules, FRONTIER GOs).
Usage: python uc1_held2.py
"""
import bisect, hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
# the held rows, from the applied files
UC = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code")
held = {}
for f in ("uc1-applied-population-1-64.tsv", "uc1-applied-population-65-256.tsv"):
    for l in open(os.path.join(UC, f), encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if c[0] == "held": held[int(c[2], 16)] = int(c[3], 16)
LIST = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    if c[0][:1].isdigit(): LIST[int(c[0], 16)] = int(c[2])
KS = sorted(LIST)
def prev_listed(a):
    i = bisect.bisect_right(KS, a - 1) - 1; return KS[i], KS[i] + LIST[KS[i]]
def insns(lo, hi): return list(cs.disasm(d[off(lo):off(hi)], lo))
def nopclass(x): return x.mnemonic in ("nop", "int3")
# P
P = {0x148D64: 0x148D70, 0x148BB3: 0x148BC0, 0x1491CE: 0x1491D0, 0x1492FF: 0x149300, 0x809D65: 0x809D70}
pres = {}
for s, entry in P.items():
    e = held.get(s); ok = e is not None and entry == (s + 15) & ~15 and prev_listed(s)[1] == s
    xs = insns(s, e); ok &= bool(xs) and all(xs[i].address + xs[i].size == xs[i + 1].address for i in range(len(xs) - 1)) and xs[-1].address + xs[-1].size == e
    runs, cur = [], None       # the block, cut into fill and the routines between fills
    for x in xs:
        if nopclass(x):
            if cur: runs.append(cur); cur = None
        else:
            cur = (cur or []) + [x]
    if cur: runs.append(cur)
    # every routine starts 16-aligned, is not listed, and ends with a return (ret / repz ret)
    ok &= bool(runs) and runs[0][0].address == entry and all(r[0].address % 16 == 0 and r[0].address not in LIST and r[-1].mnemonic.endswith("ret") for r in runs)
    pres[s] = (ok, [r[0].address for r in runs])
check("P", len(pres) == 5 and all(v[0] for v in pres.values()),
      "fill, then routines on 16-byte boundaries, each ending in a return: %s" % ", ".join("%08X -> %s" % (s, " + ".join("%08X" % a for a in v[1])) for s, v in pres.items()))
# E
E = {}
for s in (0x125770, 0x71B6B0, 0x158C97):
    first = insns(s, s + 8)[:2]; before = d[off(s) - 1]
    E[s] = (s in held and s not in LIST, before, [(x.mnemonic, x.op_str) for x in first])
e_ok = (E[0x125770][0] and E[0x125770][1] == 0xCC and 0x125770 % 16 == 0 and E[0x125770][2][:2] == [("push", "rbp"), ("mov", "rbp, rsp")]
        and E[0x71B6B0][0] and E[0x71B6B0][1] == 0xCC and 0x71B6B0 % 16 == 0
        and E[0x158C97][0] and E[0x158C97][1] == 0xC3 and prev_listed(0x158C97)[1] == 0x158C97 and E[0x158C97][2][:2] == [("push", "rbp"), ("mov", "rbp, rsp")])
calls_in = {s: [x for x in insns(s, held[s]) if x.mnemonic == "call"] for s in (0x125770, 0x158C97)}
e_ok &= not any(calls_in.values()) and any(x.op_str == "xmmword ptr [rsp], xmm6" for x in insns(0x125770, held[0x125770]))
check("E", e_ok, "entries at the held start: 00125770 (int3 fill, 16-aligned, rbp frame, saves xmm6/xmm7, no call), 0071B6B0 (int3 fill, 16-aligned), "
      "00158C97 (right after 00158C09's ret, rbp frame, no call)")
# S
pv = 0x713760; S0, SE = 0x7137BC, held.get(0x7137BC)
pi = insns(pv, S0); jr = pi[-1] if pi else None
disp = [x for x in pi if x.mnemonic == "mov" and re.search(r"dword ptr \[r8 \+ rax\*4 \+ (0x[0-9a-f]+)\]", x.op_str)]
bound = [x for x in pi if (x.mnemonic, x.op_str) == ("cmp", "ecx, 0xd")]
s_ok = jr is not None and (jr.mnemonic, jr.op_str) == ("jmp", "rcx") and len(disp) == 1 and len(bound) == 1 and prev_listed(S0) == (0x713760, 0x7137BC)
if s_ok:
    tab = B + int(re.search(r"\+ (0x[0-9a-f]+)\]", disp[0].op_str).group(1), 16)
    n = (SE - tab) // 4; rv = [B + struct.unpack_from("<I", d, off(tab) + 4 * k)[0] for k in range(n)]
    arms = insns(S0, tab)
    s_ok = S0 < tab < SE and (SE - tab) % 4 == 0 and n == 0xE and all(S0 <= t < tab or 0x713760 <= t < S0 for t in rv) and S0 in rv and arms[-1].mnemonic == "nop"            and all(x.mnemonic in ("xor", "mov", "ret", "nop") for x in arms)
    s_txt = "00713760 ends `jmp rcx` after `mov ecx, [r8 + rax*4 + TAB]` (index 0..0xD); TAB %08X..%08X is %d RVAs, each landing on an arm in %08X..%08X or in 00713760 itself (its default, 00713782: %d)" % (tab, SE, n, S0, tab, sum(t == 0x713782 for t in rv))
else:
    s_txt = "dispatch not found"
check("S", s_ok, s_txt)
# T
T0, TE = 0x208628, held.get(0x208628)
fi = insns(0x2085B0, 0x208628)
movs = [x for x in fi if x.mnemonic == "mov" and "dword ptr [" in x.op_str and "*4 + " in x.op_str]
mzx = [x for x in fi if x.mnemonic == "movzx" and "byte ptr [" in x.op_str]
tabs = sorted(B + int(re.search(r"\+ (0x[0-9a-f]+)\]$", x.op_str).group(1), 16) for x in movs)
idxs = sorted(B + int(re.search(r"\+ (0x[0-9a-f]+)\]$", x.op_str).group(1), 16) for x in mzx)
t_ok = TE == 0x2086D0 and 0x208664 in tabs and 0x208674 in idxs
if t_ok:
    rv2 = [B + struct.unpack_from("<I", d, off(0x208664) + 4 * k)[0] for k in range(4)]
    ib2 = d[off(0x208674):off(TE)]
    t_ok = all(0x2085B0 <= t < 0x208628 for t in rv2) and set(ib2) <= {0, 1, 2, 3}
check("T", t_ok, "002085B0's second dispatch: tables %s, index tables %s; 00208664 holds 4 RVAs into 002085B0, 00208674..002086D0 values < 4"
      % (["%08X" % t for t in tabs], ["%08X" % t for t in idxs]))
# R
text = [s for s in pe.sections if s.Name.startswith(b".text")][0]; ts, tb = text.VirtualAddress, text.get_data()
ENT = [0x148D70, 0x148BC0, 0x148C00, 0x1491D0, 0x149220, 0x149300, 0x809D70, 0x125770, 0x71B6B0, 0x158C97]
rel = {a: 0 for a in ENT}; leas = {a: 0 for a in ENT}
for i in range(len(tb) - 5):
    if tb[i] in (0xE8, 0xE9):
        t = B + ts + i + 5 + struct.unpack_from("<i", tb, i + 1)[0]
        if t in rel: rel[t] += 1
for m in re.finditer(b"[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", tb):
    i = m.start()
    if i + 7 <= len(tb):
        t = B + ts + i + 7 + struct.unpack_from("<i", tb, i + 3)[0]
        if t in leas: leas[t] += 1
qw = {a: 0 for a in ENT}; rva = {a: 0 for a in ENT}
for i in range(0, len(d) - 8, 8):
    v = struct.unpack_from("<Q", d, i)[0]
    if v in qw: qw[v] += 1
for i in range(0, len(d) - 4, 4):
    v = struct.unpack_from("<I", d, i)[0] + B
    if v in rva: rva[v] += 1
check("R", True, "references per entry (rel32 / lea / qword / rva): %s" % ", ".join("%08X %d/%d/%d/%d" % (a, rel[a], leas[a], qw[a], rva[a]) for a in ENT))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
