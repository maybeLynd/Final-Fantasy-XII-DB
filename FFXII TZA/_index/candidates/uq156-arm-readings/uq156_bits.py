"""uq156_bits.py - control for the container flag word +0x179D2 (FABLE, Claude Opus 5.5, 2026-09-26).

Domain: every .text instruction whose memory operand carries the displacement 0x179D2, found by a raw byte search for
the disp32; the instruction is the one a linear decode of the containing function (functions.tsv) places over the hit,
and hits that fall inside no such instruction are printed (they would be data or misaligned code). The count is
checked against tools/dispscan.py (109 both, 2026-09-26). Register-base accesses without that displacement
(pointer arithmetic, block copies) are outside the domain.

Checks:
  E1 every WRITE (or/mov/xor/and with the operand as destination) is listed with its source. A register source is
     resolved to the nearest earlier `mov reg, imm` in linear order within the function, and the distance is printed.
  E2 the only write whose source can carry bit 11 (0x800) is 002BAA79 in the location container 002BA700. Its r14 is
     loaded with 0x800 at 002BA927, and nothing between them writes r14.
  E3 the three full-word stores preserve bit 11: two flip bit 2 (not/xor/and 4/xor), and one ORs 3 into the loaded word.
  E4 the track container 002B7590 has the same guard block as the location container (bits 3|11 clear, bit 13 set,
     slot ready, 003C0CC0), but no write to +0x179D2 follows it inside the block.
Sensitivity: E2 is also run against a planted site (the location setter itself), which must be reported as a bit-11
source; if the resolver misses it, the check fails instead of reporting "no other setter".
"""
import re, struct, sys
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
    name = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, va, rs, ro))
text = [s for s in secs if s[0] == ".text"][0]
def off(v):
    for _, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
funcs = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
               errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
import bisect
def func_of(a): return funcs[bisect.bisect_right(funcs, a) - 1]

DISP = struct.pack("<I", 0x179D2)
_, va, rs, ro = text
sites, lin, unaligned = {}, {}, []
p = ro
while True:
    p = d.find(DISP, p, ro + rs)
    if p < 0: break
    # boundaries come from a linear decode of the containing function, never from a guessed start: a backwards guess
    # drops 66/REX prefixes or swallows the previous instruction's immediate as a REX byte (both happened here)
    hit = BASE + va + p - ro
    f = func_of(hit)
    if f not in lin:
        lin[f] = list(cs.disasm(d[off(f):off(f) + 0x3000], f))
    cover = [x for x in lin[f] if x.address <= hit < x.address + x.size]
    if cover and "0x179d2]" in cover[0].op_str:
        sites[cover[0].address] = cover[0]
    else:
        unaligned.append(hit)
    p += 1

WRITES = ("or", "mov", "xor", "and")
REG = re.compile(r"^(?:word|byte|dword) ptr \[\w+ \+ 0x179d2\], (\w+)$")
FAM = {}
for g in (("eax", "ax", "rax", "al"), ("ebx", "bx", "rbx", "bl"), ("ecx", "cx", "rcx", "cl"), ("edx", "dx", "rdx", "dl"),
          ("esi", "si", "rsi", "sil"), ("edi", "di", "rdi", "dil")):
    for r in g: FAM[r] = g[0]
for i in range(8, 16):
    for r in ("r%d" % i, "r%dd" % i, "r%dw" % i, "r%db" % i): FAM[r] = "r%d" % i
NOWRITE = ("test", "cmp", "push", "bt")
def before(site, k):
    """the k instructions before site, decoded linearly from its function's start (never from a guessed byte)."""
    f = func_of(site)
    return list(cs.disasm(d[off(f):off(site)], f))[-k:]
def resolve(site, reg):
    f = func_of(site)
    last = None
    for x in cs.disasm(d[off(f):off(site)], f):
        dst = x.op_str.split(", ")[0]
        if x.mnemonic not in NOWRITE and FAM.get(dst) == FAM[reg]:
            m = re.match(r"\w+, (0x[0-9a-f]+|\d+)$", x.op_str)
            last = (x.address, int(m.group(1), 0) if x.mnemonic == "mov" and m else None, x.mnemonic + " " + x.op_str)
    return last

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

writes = [x for a, x in sorted(sites.items()) if x.mnemonic in WRITES and x.op_str.split(", ")[0].endswith("0x179d2]")]
print("sites %d, writes %d, raw hits off an instruction boundary %d %s" % (len(sites), len(writes), len(unaligned), [hex(u) for u in unaligned]))
bit11, fullword = [], []
for x in writes:
    src = x.op_str.split(", ")[1]
    if src in FAM:
        r = resolve(x.address, src)
        val = r[1] if r else None
        how = "%s <- %s @%08X (%d B back)" % (src, r[2] if r else "?", r[0] if r else 0, x.address - r[0] if r else 0)
    else:
        val = int(src, 0); how = "imm"
    print("  %08X %-32s %-44s in %08X" % (x.address, x.mnemonic + " " + x.op_str, how, func_of(x.address)))
    if x.mnemonic == "mov": fullword.append(x)
    elif x.mnemonic in ("or", "xor") and (val is None or val & 0x800): bit11.append((x, val, r if src in FAM else None))

# E2
check("E2 sensitivity: the planted location setter 002BAA79 is reported as a bit-11 source",
      any(x.address == 0x2BAA79 and v == 0x800 for x, v, _ in bit11))
others = [(hex(x.address), v) for x, v, _ in bit11 if x.address != 0x2BAA79 and x.mnemonic != "xor"]
check("E2 no other or-write can carry bit 11", not others, str(others))
xors = [(x, r) for x, v, r in bit11 if x.mnemonic == "xor"]
xor_ok = True
for x, r in xors:   # the computed xor-copies: the source's last writer is `and ax, 0x30|0x40`, confining them to bits 4..6
    m = re.match(r"and \w+, (0x[0-9a-f]+)$", r[2]) if r else None
    xor_ok &= bool(m) and int(m.group(1), 16) & 0x800 == 0
check("E2 every xor-write is a masked copy of bits 4..6 (the and just before it has no bit 11)", xor_ok, "(%d xor-writes)" % len(xors))
seg = list(cs.disasm(d[off(0x2BA927):off(0x2BAA79)], 0x2BA927))
check("E2 r14d = 0x800 at 002BA927 and nothing writes r14 before 002BAA79",
      seg[0].op_str == "r14d, 0x800" and not [y for y in seg[1:] if y.mnemonic not in NOWRITE
                                                 and FAM.get(y.op_str.split(", ")[0]) == "r14"])
# E3
ok3 = True
for x in fullword:
    txt = " | ".join(y.mnemonic + " " + y.op_str for y in before(x.address, 8))
    good = ("and cx, 4" in txt and "not cx" in txt) or "or ax, 3" in txt
    print("  full-word %08X: %s" % (x.address, "flip bit 2" if "and cx, 4" in txt else "or 3" if good else txt))
    ok3 &= good
check("E3 every full-word store preserves bit 11", ok3 and len(fullword) == 3, "(%d stores)" % len(fullword))
# E4
blk = list(cs.disasm(d[off(0x2B776A):off(0x2B77C7)], 0x2B776A))
has_guard = any(y.op_str == "ecx, 0x808" for y in blk) and any(y.op_str == "0x3c0cc0" for y in blk)
wr = [y for y in blk if y.mnemonic in WRITES and "0x179d2]" in y.op_str.split(", ")[0]]
check("E4 track container guard block present with no flag write", has_guard and not wr)
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
