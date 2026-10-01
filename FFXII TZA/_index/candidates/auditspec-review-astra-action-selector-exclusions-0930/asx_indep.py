"""asx_indep.py - SWE2-AUDIT-SPEC independent re-derivation for ASTRA action-selector-local-exclusions (2026-09-30).

Not the packet's drivers. Image via ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha asserted). Tables
from the D:/FFXII_TZA_extract copies (byte-equal to the install archive, see the action-preconditions review).

  A  rows 511..534: category byte +0x1E and word +0x24 in all nine tables
  B  references: callers of 003060E0 / 00306480 / 002FFCF0 / 0030DB70 / 002F8D60 (E8/E9, jcc, data)
  C  jump table of 00306760 at 00306AF0: the guard, the six targets, and what the next four dwords are
  D  EMULATION (isolated original code, unicorn), all with INJECTED state (named per case):
     D1 003060E0(id, raw, 0) for id 511..534, raw+5 in 0..255 and raw+4 in 0..255, real us table as the descriptor
     D2 00306480(id, raw) for the same ids: raw+5==0 must return 0x0F without reaching 00323EC0; raw+5!=0 must reach
        00323EC0 (stopped there)
     D3 002F8D60 with the file value of 01EEBAF0 (negative) over 2000 random threshold tables/inputs: return values
     D4 0030DB70 null-record arm (rcx=0): the value stored to 022C2178 for the negative-override fallback and, as a
        SENSITIVITY control, for a nonnegative override whose word is 511
"""
import os, random, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_UNMAPPED, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RAX, UC_X86_REG_R8, \
    UC_X86_REG_RIP
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXTRACT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle"
LANGS = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]


def p(*a):
    print(" ".join(str(x) for x in a))


def table(lang):
    b = open(os.path.join(EXTRACT, lang, "binaryfile", "battle_pack.bin"), "rb").read()
    t = struct.unpack_from("<I", b, 0x3C)[0]
    c, s, o = struct.unpack_from("<III", b, t + 4)
    return b[t:t + o + c * s], c, s, o


p("== A rows 511..534")
for lang in LANGS:
    tb, c, s, o = table(lang)
    cats = sorted(set(tb[o + i * s + 0x1E] for i in range(511, 535)))
    words = sorted(set(struct.unpack_from("<H", tb, o + i * s + 0x24)[0] for i in range(511, 535)))
    p("   %s: categories %s words %s ; rows with category 7 in the whole table: %d" %
      (lang, cats, ["%04X" % w for w in words], sum(1 for i in range(c) if tb[o + i * s + 0x1E] == 7)))

p("== B references")
for tgt in (0x3060E0, 0x306480, 0x2FFCF0, 0x30DB70, 0x2F8D60):
    rc = T.rel32_callers(tgt)
    p("   %08X rel32 %d %s jcc %s abs64 %s" % (tgt, len(rc), rc if len(rc) <= 12 else rc[:12] + ["..."],
                                            T.jcc_callers(tgt), T.data_refs(tgt)["abs64"]))
p("   rip address-taken of 002F8D60:", ["%08X %s %s" % h[:3] for h in T.rip_refs(0x2F8D60, 0x2F8D61)])

p("== C 00306760 dispatch")
for i in T.dis(0x3067AA, 0x3067D5):
    p("   %08X %-7s %s" % (i.address, i.mnemonic, i.op_str))
dw = struct.unpack("<10I", T.rd(0x306AF0, 40))
p("   dwords at 00306AF0:", ["%08X" % d for d in dw])
p("   first six + image base:", ["%08X" % (d + 0x120000) for d in dw[:6]])
md = Cs(CS_ARCH_X86, CS_MODE_64)
p("   bytes after the six entries:", T.rd(0x306B08, 16).hex(), "->",
  [(hex(i.address), i.mnemonic, i.op_str) for i in md.disasm(T.rd(0x306B08, 16), 0x306B08)][:5])

# ---------------- D emulation
PAGE = 0x1000
mu = Uc(UC_ARCH_X86, UC_MODE_64)
for n, v, vs, po, rs, x in T.SECS:
    lo = v & ~(PAGE - 1); hi = (v + max(vs, rs) + PAGE - 1) & ~(PAGE - 1)
    mu.mem_map(lo, hi - lo); mu.mem_write(v, T.raw[po:po + min(vs, rs)])
PRISTINE = {0x1EEBAF0: T.rd(0x1EEBAF0, 4)}
STACK = 0x70000000; mu.mem_map(STACK, 0x10000)
DESC = 0x71000000; mu.mem_map(DESC, 0x20000)
THR = 0x73000000; mu.mem_map(THR, 0x10000)
RAW = 0x74000000; mu.mem_map(RAW, 0x1000)
INP = 0x75000000; mu.mem_map(INP, 0x1000)
RET = 0x72000000; mu.mem_map(RET, 0x1000); mu.mem_write(RET, b"\xf4")
bad = []
mu.hook_add(UC_HOOK_MEM_UNMAPPED, lambda uc, acc, addr, size, val, ud: bad.append(hex(addr)) or False)
STOPS = set()
hit = []


def on_code(uc, addr, size, ud):
    if addr in STOPS:
        hit.append(addr)
        uc.emu_stop()


mu.hook_add(UC_HOOK_CODE, on_code)
mu.mem_write(0x1F83530, struct.pack("<Q", 0))  # INJECTED: arena base 0, so +0xC offsets are absolute low32 addresses
tb, c, s, o = table("us")
hdr = bytearray(tb[:16]); struct.pack_into("<I", hdr, 12, DESC + o)
mu.mem_write(DESC, bytes(hdr) + tb[16:])
mu.mem_write(0x2EBF138, struct.pack("<Q", DESC))  # INJECTED: action descriptor = the shipped us table


def call(fn, rcx, rdx=0, r8=0, stops=()):
    STOPS.clear(); STOPS.update(stops); del hit[:]
    rsp = STACK + 0x8000; mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp); mu.reg_write(UC_X86_REG_RCX, rcx); mu.reg_write(UC_X86_REG_RDX, rdx)
    mu.reg_write(UC_X86_REG_R8, r8)
    mu.emu_start(fn, RET, count=200000)
    return mu.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, list(hit)


p("== D1 003060E0(id 511..534, raw, 0); INJECTED: descriptor, arena base, raw object bytes +4/+5")
res = {}
for idv in range(511, 535):
    for r5 in range(256):
        for r4 in (0, 0x1B, 0x27, 0xFF):
            mu.mem_write(RAW, bytes([0] * 4 + [r4, r5]))
            v, h = call(0x3060E0, idv, RAW, 0)
            res.setdefault((r5 == 0), set()).add(v)
p("   raw+5 == 0 -> results", sorted(res[True]), "; raw+5 != 0 -> results", sorted(res[False]))
v, h = call(0x3060E0, 511, 0, 0); p("   null raw -> result", v)
v, h = call(0x3060E0, 543, RAW, 0); p("   control id 543 (class20 reject) -> result", v)
mu.mem_write(RAW, bytes([0] * 6))
v, h = call(0x3060E0, 0, RAW, 0); p("   control id 0 (category %d) raw+5=0 -> result %d" % (tb[o + 0x1E], v))

p("== D2 00306480(id, raw) for id 511..534; stop at the licence leg 00323EC0")
out = {}
for idv in range(511, 535):
    for r5 in (0, 1, 2, 0x80, 0xFF):
        mu.mem_write(RAW, bytes([0] * 5 + [r5]))
        v, h = call(0x306480, idv, RAW, 0, stops=(0x323EC0,))
        out.setdefault(r5 == 0, set()).add("reached 00323EC0" if h else "returned %X" % v)
p("   raw+5 == 0:", sorted(out[True]), "; raw+5 != 0:", sorted(out[False]))
v, h = call(0x306480, 511, 0, 0, stops=(0x323EC0,)); p("   null raw -> returned %X" % v)

p("== D3 002F8D60, 01EEBAF0 = file value %s; INJECTED: threshold descriptor 02EBF0A0 (random rows), input bytes"
  % PRISTINE[0x1EEBAF0].hex())
mu.mem_write(0x1EEBAF0, PRISTINE[0x1EEBAF0])
rnd = random.Random(20260930)
vals = set(); miss = 0; match = 0
for trial in range(2000):
    n = rnd.randint(0, 40); stride = rnd.choice([4, 8, 12])
    rows = bytes(rnd.randrange(256) for _ in range(n * stride))
    mu.mem_write(THR, b"st2e" + struct.pack("<IHHI", n, stride, 0, THR + 16) + rows)
    mu.mem_write(0x2EBF0A0, struct.pack("<Q", THR if trial % 97 else 0))
    mu.mem_write(INP, bytes(rnd.randrange(256) for _ in range(4)))
    v, h = call(0x2F8D60, INP)
    vals.add(v)
    if v == 0xFFFFFFFF:
        miss += 1
    else:
        match += 1
p("   returns: %d matches, %d misses; max match value %s; any value in 256..0xFFFFFFFE: %s" %
  (match, miss, max([x for x in vals if x != 0xFFFFFFFF] or [None]), any(255 < x < 0xFFFFFFFF for x in vals)))

p("== D4 0030DB70(rcx=0) null-record arm -> dword 022C2178; INJECTED: word 022C2190, override index/array")


def null_arm(word2190, idx, arrword):
    mu.mem_write(0x22C2190, struct.pack("<H", word2190))
    mu.mem_write(0x1EEBAF0, struct.pack("<i", idx))
    mu.mem_write(0x22BE930, struct.pack("<8H", *([arrword] * 8)))
    mu.mem_write(0x22C2178, b"\xAA" * 4)
    call(0x30DB70, 0)
    return struct.unpack("<i", bytes(mu.mem_read(0x22C2178, 4)))[0]


stored = set()
for trial in range(300):
    n = rnd.randint(1, 30)
    mu.mem_write(THR, b"st2e" + struct.pack("<IHHI", n, 4, 0, THR + 16) + bytes(rnd.randrange(256) for _ in range(4 * n)))
    mu.mem_write(0x2EBF0A0, struct.pack("<Q", THR))
    mu.mem_write(0x22C2192, bytes(rnd.choice([rnd.randrange(256), 0xFF]) for _ in range(3)))  # INJECTED input bytes
    stored.add(null_arm(0x100, -1, 0))
p("   negative override (-1), random fallback tables: %d distinct stored values, span %d..%d; any in 303..326 (=511..534-0xD0): %s"
  % (len(stored), min(stored), max(stored), any(303 <= x <= 326 for x in stored)))
p("   control E2 in 022C2190 -> stored", null_arm(0xE2, -1, 0), "; F2 ->", null_arm(0xF2, -1, 0))
p("   SENSITIVITY: override index 0, word 511 -> stored", null_arm(0x100, 0, 511), "(511-0xD0 = %d)" % (511 - 0xD0))
p("   SENSITIVITY: override index 0, word 543 -> stored", null_arm(0x100, 0, 543), "(class20 must reject)")
p("   unmapped accesses:", sorted(set(bad))[:8])
