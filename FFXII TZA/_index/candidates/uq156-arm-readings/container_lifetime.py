"""container_lifetime.py - control for UQ-156's container lifetime (FABLE, Claude Opus 5.5, 2026-09-26).

Checks:
  L1 each map container's arm 1 stores its continuation at widget +8: location 002BA700 -> 002BA6B0, track
     002B7590 -> 002B7540.
  L2 each continuation clears its container global (0209E5F0 / 0209E5C0), tests its sibling global
     (0209E5F8 / 0209E5C8) and 00402220, then passes its saved record (0209E608 / 0209E5D0) to 00285F00 and tail-jumps
     to 002814E0 with 0x417 / 0x4EA.
  L3 the two globals have exactly two rip-relative writes each: one store in the creator (002B9D30 / 002B6350) and
     the continuation's clear. Domain: every .text instruction whose rip-relative operand resolves to the cell.
  L4 container flag +0x179D2 bit 3 (8) is set only by the two closers, 002B62CE (002B6260) and 002B9B7C (002B9B30).
     Domain: every instruction carrying the displacement 0x179D2 (raw disp32 search, linear decode of the containing
     function, as in uq156_bits.py); a register source is resolved to the nearest earlier `mov reg, imm`, and the
     three full-word stores are checked by their masks. Sensitivity: the two closers must be REPORTED as bit-3
     setters (planted positives), and 002BA011 (0x400) must not be.
  L5 each container's per-frame arm (message 2) tests bit 3, releases the child at +0xC0 through 00244F00 while it
     lives, and otherwise calls 00245020 on itself.
  L6 the release 002482E0 reads [+8] before freeing, skips a null one, and tail-jumps to it through rax.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, o + 8)[1:])
text = [s for s in secs if s[0] == ".text"][0]
def off(v):
    for _, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
funcs = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
               errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def func_of(a): return funcs[bisect.bisect_right(funcs, a) - 1]
def dis(a, b): return list(cs.disasm(d[off(a):off(b)], a))
def txt(x): return "%s %s" % (x.mnemonic, x.op_str)
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

# L1
for name, a, b, cont in (("location", 0x2BA74B, 0x2BA75B, 0x2BA6B0), ("track", 0x2B75D0, 0x2B75EA, 0x2B7540)):
    I = dis(a, b)
    lea = [x for x in I if x.mnemonic == "lea" and rip(x) == cont]
    st = [x for x in I if x.mnemonic == "mov" and re.fullmatch(r"qword ptr \[r(di|bx) \+ 8\], rax", x.op_str)]
    check("L1 %s arm 1 stores %08X at +8" % (name, cont), bool(lea) and bool(st) and st[0].address > lea[0].address)

# L2
for name, f, g, side, saved, code in (("location", 0x2BA6B0, 0x209E5F0, 0x209E5F8, 0x209E608, 0x417),
                                      ("track", 0x2B7540, 0x209E5C0, 0x209E5C8, 0x209E5D0, 0x4EA)):
    I = dis(f, f + 0x42); T = [txt(x) for x in I]
    check("L2 %s continuation clears %08X" % (name, g), any(x.mnemonic == "mov" and rip(x) == g and x.op_str.endswith(", 0") for x in I))
    check("L2 %s tests sibling %08X and 00402220" % (name, side),
          any(x.mnemonic == "cmp" and rip(x) == side for x in I) and "call 0x402220" in T)
    check("L2 %s posts %08X through 00285F00, then 002814E0(%#x)" % (name, saved, code),
          any(x.mnemonic == "lea" and rip(x) == saved for x in I) and "call 0x285f00" in T
          and "mov ecx, %#x" % code in T and "jmp 0x2814e0" in T)

# L3
_, va, rs, ro = text
from array import array
def rip_sites(cell):
    """every instruction whose rip-relative operand resolves to cell: a disp32 at file offset p with k immediate bytes
    after it satisfies disp + p == cell - 4 - k - (BASE + va) + ro; each candidate is confirmed by a linear decode of
    its function, so a coincidental byte pattern that is not an operand is dropped."""
    want = {cell - 4 - k - (BASE + va) + ro: k for k in (0, 1, 2, 4)}
    cand = set()
    for s in range(4):
        a = array("i"); a.frombytes(d[ro + s: ro + s + ((rs - s) // 4) * 4])
        for i, v in enumerate(a):
            if v + ro + s + 4 * i in want: cand.add(BASE + va + s + 4 * i)
    hits = {}
    for c in cand:
        f = func_of(c)
        for x in cs.disasm(d[off(f):off(c) + 16], f):
            if x.address <= c < x.address + x.size and "rip" in x.op_str and rip(x) == cell: hits[x.address] = x
    return list(hits.values())
for name, g, creator, clear in (("location", 0x209E5F0, 0x2B9D85, 0x2BA6BC), ("track", 0x209E5C0, 0x2B63A8, 0x2B754C)):
    S = rip_sites(g)
    w = sorted(x.address for x in S if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip"))
    check("L3 %s global %08X: writes are exactly the create store and the clear" % (name, g), w == [creator, clear],
          "%d sites, writes %s" % (len(S), [hex(v) for v in w]))

# L4
DISP = struct.pack("<I", 0x179D2)
sites, lin = {}, {}
p = ro
while True:
    p = d.find(DISP, p, ro + rs)
    if p < 0: break
    hit = BASE + va + p - ro; f = func_of(hit)
    if f not in lin: lin[f] = list(cs.disasm(d[off(f):off(f) + 0x3000], f))
    cover = [x for x in lin[f] if x.address <= hit < x.address + x.size]
    if cover and "0x179d2]" in cover[0].op_str: sites[cover[0].address] = cover[0]
    p += 1
FAM = {}
for grp in (("eax", "ax", "rax", "al"), ("ebx", "bx", "rbx", "bl"), ("ecx", "cx", "rcx", "cl"), ("edx", "dx", "rdx", "dl"),
            ("esi", "si", "rsi", "sil"), ("edi", "di", "rdi", "dil")):
    for r in grp: FAM[r] = grp[0]
for i in range(8, 16):
    for r in ("r%d" % i, "r%dd" % i, "r%dw" % i, "r%db" % i): FAM[r] = "r%d" % i
def resolve(site, reg):
    last = None
    for x in cs.disasm(d[off(func_of(site)):off(site)], func_of(site)):
        dst = x.op_str.split(", ")[0]
        if x.mnemonic not in ("test", "cmp", "push", "bt") and FAM.get(dst) == FAM[reg]:
            m = re.match(r"\w+, (0x[0-9a-f]+|\d+)$", x.op_str)
            last = (x.address, int(m.group(1), 0) if x.mnemonic == "mov" and m else None, txt(x))
    return last
bit3, unresolved = [], []
for a, x in sorted(sites.items()):
    if x.mnemonic not in ("or", "xor", "mov") or not x.op_str.split(", ")[0].endswith("0x179d2]"): continue
    src = x.op_str.split(", ")[1]
    if x.mnemonic == "mov":   # full-word stores: checked by the mask of the op that built the value
        prev = [txt(y) for y in cs.disasm(d[off(func_of(a)):off(a)], func_of(a))][-8:]
        if any(re.fullmatch(r"and cx, 4", s) for s in prev) or any(re.fullmatch(r"or ax, 3", s) for s in prev): continue
        unresolved.append(a); continue
    val = int(src, 0) if src not in FAM else (resolve(a, src) or (0, None, ""))[1]
    if x.mnemonic == "xor":
        r = resolve(a, src); m = re.match(r"and \w+, (0x[0-9a-f]+)$", r[2]) if r else None
        if m and int(m.group(1), 16) & 8 == 0: continue
        unresolved.append(a); continue
    if val is None: unresolved.append(a)
    elif val & 8: bit3.append(a)
check("L4 planted positives: both closers reported as bit-3 setters", 0x2B62CE in bit3 and 0x2B9B7C in bit3, str([hex(v) for v in bit3]))
check("L4 planted negative: 002BA011 (0x400) not reported", 0x2BA011 not in bit3 and 0x2BA011 in sites)
check("L4 no other bit-3 setter and nothing unresolved", sorted(bit3) == [0x2B62CE, 0x2B9B7C] and not unresolved,
      "sites %d, unresolved %s" % (len(sites), [hex(v) for v in unresolved]))

# L5
for name, a, b, reg in (("location", 0x2BABEE, 0x2BAC73, "rdi"), ("track", 0x2B7850, 0x2B78D0, "rbx")):
    T = [txt(x) for x in dis(a, b)]
    check("L5 %s per-frame arm: bit-3 test, child +0xC0 release, self 00245020" % name,
          "test al, 8" in T and "lea rcx, [%s + 0xc0]" % reg in T and "call 0x244f00" in T
          and "mov rcx, %s" % reg in T and "call 0x245020" in T
          and T.index("call 0x244f00") < T.index("call 0x245020"))

# L6
T = [txt(x) for x in dis(0x2482E0, 0x24840E)]
seq = ["test rbx, rbx", "je 0x248408", "mov rax, rbx", "add rsp, 0x20", "pop rbx", "jmp rax"]
j = T.index("mov rbx, qword ptr [rdi + 8]") if "mov rbx, qword ptr [rdi + 8]" in T else 0
k = T.index("test rbx, rbx", j) if "test rbx, rbx" in T[j:] else -1
check("L6 002482E0 reads [+8], skips a null one, and tail-jumps to it through rax",
      "mov rbx, qword ptr [rdi + 8]" in T and k > T.index("mov rbx, qword ptr [rdi + 8]") and T[k:k + 6] == seq, str(T[k:k + 6]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
