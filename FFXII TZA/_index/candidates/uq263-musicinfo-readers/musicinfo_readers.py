"""musicinfo_readers.py - control for UQ-263 (FABLE, Claude Opus 5.5, 2026-09-26): who reads musicinfo.bin's entries.

Domain: every .text instruction whose rip-relative operand resolves into the pointer cell 022CBA50..022CBA57, found by
a disp32 search and confirmed as an instruction by a linear decode of its function.
  M1 the non-lea accesses are exactly: writes 00360B42 (in 00360B40) and 00360CAE (in 00360C70), read 00361014 (in
     00361010). Planted positive: the loader's clear at 00360CAE must be found.
  M2 the three `lea`s at 022CBA51 are the end bound of the 4 x 0x18 track table at 022CB9F0 (walked from base + 1), not
     accesses to the pointer: 022CB9F0 + 4 * 0x18 + 1 == 022CBA51, and 00360D70 walks rbx = 022CB9F1 in 0x18 steps.
  M3 the one reader, 00361010, loads the entry's first byte ([rdx + rax*2]) and keeps bit 0 (`and eax, 1`); it never
     touches the second byte.
  M4 the loader 00360C70 hands its arena buffer (rbx from 0036A190) to exactly one call, the resource request 0032E620:
     as r8, and as the dword in the request's completion descriptor ([rsp+0x38]), which is how the callback 00360B40
     receives it and stores the pointer. 00360B40 has no direct caller.
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
def func_of(a): return STARTS[bisect.bisect_right(STARTS, a) - 1]
def whole(a):
    i = bisect.bisect_right(STARTS, a)
    return list(cs.disasm(d[off(a):off(STARTS[i])], a))
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
tva, trs, tro = [(va, rs, ro) for vs, va, rs, ro in secs if va <= 0x1000 < va + rs][0]
def rip_sites(lo, hi):
    want = {}
    for cell in range(lo, hi):
        for k in (0, 1, 2, 4): want[cell - 4 - k - (BASE + tva) + tro] = cell
    cand = set()
    for s in range(4):
        a = array("i"); a.frombytes(d[tro + s: tro + s + ((trs - s) // 4) * 4])
        for i, v in enumerate(a):
            if v + tro + s + 4 * i in want: cand.add(BASE + tva + s + 4 * i)
    hits = {}
    for c in cand:
        f = func_of(c)
        for x in cs.disasm(d[off(f):off(c) + 16], f):
            if x.address <= c < x.address + x.size and rip(x) is not None and lo <= rip(x) < hi: hits[x.address] = x
    return [hits[k] for k in sorted(hits)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

S = rip_sites(0x22CBA50, 0x22CBA58)
nonlea = [(x.address, x.mnemonic, x.op_str.split(",")[0].startswith("qword ptr [rip")) for x in S if x.mnemonic != "lea"]
writes = sorted(a for a, m, w in nonlea if w); reads = sorted(a for a, m, w in nonlea if not w)
check("M1 planted positive: the loader's clear 00360CAE is found", 0x360CAE in writes)
check("M1 non-lea accesses: writes 00360B42 / 00360CAE, one read 00361014",
      writes == [0x360B42, 0x360CAE] and reads == [0x361014], "writes %s reads %s" % ([hex(v) for v in writes], [hex(v) for v in reads]))
leas = [x for x in S if x.mnemonic == "lea"]
check("M2 every lea resolves to 022CBA51 = 022CB9F0 + 4*0x18 + 1",
      leas and all(rip(x) == 0x22CB9F0 + 4 * 0x18 + 1 for x in leas), "%d leas in %s" % (len(leas), sorted({"%08X" % func_of(x.address) for x in leas})))
W = ["%s %s" % (x.mnemonic, x.op_str) for x in whole(0x360D70)]
check("M2 00360D70 walks base+1 in 0x18 steps up to that bound",
      any(x.mnemonic == "lea" and rip(x) == 0x22CB9F1 for x in whole(0x360D70)) and "add rbx, 0x18" in W and "cmp rbx, rdi" in W)
R = ["%s %s" % (x.mnemonic, x.op_str) for x in whole(0x361010)]
check("M3 00361010 reads the entry's first byte and keeps bit 0 only",
      "movzx eax, byte ptr [rdx + rax*2]" in R and "and eax, 1" in R and not any("rax*2 + 1]" in s for s in R), str(R[4:8]))
L = whole(0x360C70)
k = next(i for i, x in enumerate(L) if x.mnemonic == "call" and x.op_str == "0x36a190")
uses = [("%08X %s %s" % (x.address, x.mnemonic, x.op_str)) for x in L[k + 1:] if re.search(r"\brbx\b|\bebx\b", x.op_str)]
check("M4 the buffer (rbx from 0036A190) goes to 0032E620 only (r8 and the completion descriptor), callback 00360B40",
      any(x.mnemonic == "lea" and rip(x) == 0x360B40 for x in L)
      and [u.split(" ", 1)[1] for u in uses] == ["mov rbx, rax", "mov dword ptr [rsp + 0x38], ebx", "mov r8, rbx", "mov rbx, qword ptr [rsp + 0x70]"],
      str(uses))
callers = []
p = tro
while True:
    p = d.find(b"\xe8", p, tro + trs)
    if p < 0: break
    if BASE + tva + p - tro + 5 + struct.unpack_from("<i", d, p + 1)[0] == 0x360B40: callers.append(BASE + tva + p - tro)
    p += 1
check("M4 00360B40 has no direct call site (it is reached as the callback)", not callers, str([hex(c) for c in callers]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
