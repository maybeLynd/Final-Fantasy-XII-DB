"""G-2 (OPUS, 2026-09-27): the two walk routes the accessor-caller narrowing left open are closed for the SabFile::Sequence
entry's flag (+0x28, byte) and float (+0x2C).

  W1 no indexed access of a 16-byte entry table reaches them anywhere in the image: no operand [base + idx*16 + 0x28 /
     + 0x2C], and none whose index was shifted by 4 or multiplied by 0x10 within the preceding 12 instructions.
     POSITIVE CONTROL: the same scanner finds *8-scaled accesses at those displacements (other 8-byte-stride arrays).
  W2 in the audio range 0x7A0000..0x800000, no pointer stepped by 0x10 (add reg, 0x10 / lea reg, [reg + 0x10]) reads a
     byte at +8. The functions where a 0x10-stepped register also reads a dword at +0xC are exactly nine, and none walks
     the entry table (the scan is flow-insensitive, so a register stepped in one loop and reused elsewhere is caught):
     three float readers - 007DA2E0 (vec4 products over [r8/r9/r10 + rcx + 8 / 0xC]), 007B0390 (a float-array lerp),
     007AC4F0 (a record whose +4 is a signed byte index into a table, not the entry's +4 word) - and six integer
     readers: 007C1830, 007C7950, 007C7CD0, 007CBC40 and 007CD350 read +0xC as an integer from descriptors the
     007D0400 / 007D06B0 / 007D0600 accessors return (compared with the tick counter +0x664), and 007FF1C0 is image
     arithmetic.
Not claimed: a copy of the record or entry into another structure (16-byte loads at +0x20 are common in the audio
range's vector code and are not dispositioned here), or a pointer formed by other arithmetic.
Usage: python g2_walk_routes.py [exe] [functions.tsv]
"""
import re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
funcs = []
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: f, sz = int(c[0], 16), int(c[2])
    except (ValueError, IndexError): continue
    if 0x121000 <= f < 0x900000 and off(f) is not None: funcs.append((f, sz))
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


w1_16, w1_8 = [], 0
w2_byte, w2_float = [], set()
for f, sz in funcs:
    xs = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sz], f)]
    for i, (a, mn, op) in enumerate(xs):
        m = re.search(r"(byte|dword) ptr \[(r\w+) \+ (r\w+)(?:\*(\d+))? \+ (0x28|0x2c)\]", op)
        if m:
            w, b, idx, sc, dd = m.groups()
            if (dd == "0x28" and w == "byte") or (dd == "0x2c" and w == "dword"):
                back = xs[max(0, i - 12):i]
                sh16 = any((y[1] == "shl" and y[2] == idx + ", 4") or (y[1] == "imul" and y[2].startswith(idx + ",") and y[2].endswith(", 0x10")) for y in back)
                if sc == "16" or sh16: w1_16.append(a)
                elif sc == "8": w1_8 += 1
    if 0x7A0000 <= f < 0x800000:
        steps = {op.split(",")[0] for a, mn, op in xs if mn == "add" and re.match(r"r\w+, 0x10$", op)} | \
                {op.split(",")[0] for a, mn, op in xs if mn == "lea" and re.match(r"(r\w+), \[\1 \+ 0x10\]$", op)}
        for a, mn, op in xs:
            m = re.search(r"(byte|dword) ptr \[(r\w+) \+ (0x8|0xc)\]", op)
            if not m or m.group(2) not in steps: continue
            if mn.startswith("mov") and op.startswith(m.group(0)): continue  # a store, not a read
            if m.group(3) == "0x8" and m.group(1) == "byte": w2_byte.append(a)
            if m.group(3) == "0xc" and m.group(1) == "dword": w2_float.add(f)
check("W1 no 16-scaled indexed read at +0x28 / +0x2C", not w1_16 and w1_8 > 0, "(16-scaled %d; positive control: %d *8-scaled)" % (len(w1_16), w1_8))
check("W2 no 0x10-stepped byte read at +8 in the audio range", not w2_byte, str([hex(a) for a in w2_byte]))
EXPECT = {0x7AC4F0, 0x7B0390, 0x7DA2E0, 0x7C1830, 0x7C7950, 0x7C7CD0, 0x7CBC40, 0x7CD350, 0x7FF1C0}
check("W2 the 0x10-stepped +0xC readers are exactly the nine dispositioned functions", w2_float == EXPECT, str(sorted("%08X" % f for f in w2_float ^ EXPECT)))
# W3 (added 2026-09-27): no block copy in the record's known consumers - the accessor family 007CF500..007CFC80, every
# function that calls into it (rel32), and the policy walkers 007E5000..007E7000. Their 16-byte moves that could cover
# record +0x28 / +0x2C or entry +8 / +0xC must all be stack spills, and none calls memcpy (00861EBA).
import bisect
keys = sorted(f for f, s in funcs); fam = {f for f in keys if 0x7CF500 <= f < 0x7CFC80}
text = [s for s in secs if s[1] == 0x1000][0]; blob = d[text[3]:text[3] + text[2]]; tb = BASE + text[1]
consumers = set(fam) | {f for f in keys if 0x7E5000 <= f < 0x7E7000}
for i in range(len(blob) - 5):
    if blob[i] == 0xE8 and tb + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] in fam:
        k = bisect.bisect_right(keys, tb + i) - 1
        if k >= 0: consumers.add(keys[k])
sz = dict(funcs); w3 = []
for f in sorted(consumers):
    for x in cs.disasm(d[off(f):off(f) + sz[f]], f):
        m = re.search(r"xmmword ptr \[(r\w+)(?: \+ (0x[0-9a-f]+))?\]", x.op_str)
        if m and x.mnemonic in ("movups", "movdqu", "movaps", "movdqa") and m.group(1) != "rsp":
            dd = int(m.group(2), 16) if m.group(2) else 0
            if dd <= 0x2C < dd + 16 or dd <= 0xC < dd + 16: w3.append(x.address)
        if x.mnemonic == "call" and x.op_str == "0x861eba": w3.append(x.address)
check("W3 no block copy of the record or entry in its known consumers", not w3 and len(consumers) > 90,
      "(%d consumer functions; hits %s)" % (len(consumers), [hex(a) for a in w3]))
print("FAILS", fails); sys.exit(1 if fails else 0)
