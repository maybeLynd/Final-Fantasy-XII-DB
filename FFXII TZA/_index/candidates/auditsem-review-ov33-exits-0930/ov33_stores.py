"""SWE2-AUDIT-SEM OV-33 store census (own code, independent of e1_mode_writers.py / e3_readlayer_ptr.py).
Every instruction in .text whose memory operand is rip-relative or absolute (no base, no index) and covers
  MODE  02ADD930 / 02ADD931 (the two bytes 0037B330 reads), and
  RL    01F81160 (the qword 001A1220 returns),
is listed with its access (write if it is the destination of a writing mnemonic). Found by scanning every disp32 whose
rip-relative target lands within 8 bytes below each cell, decoding the longest instruction that ends on it.
Then the callers of each writing function, and the value each 0037B450 call site passes."""
import struct, bisect
import img
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
pd = [s for s in img.secs if s[0].startswith(".pdata")][0]
funcs = []
for i in range(0, pd[2], 12):
    b, e, u = struct.unpack_from("<III", img.raw, pd[3] + i)
    if b:
        funcs.append((img.BASE + b, img.BASE + e))
funcs.sort()
fs = [f[0] for f in funcs]
def fn(a):
    k = bisect.bisect_right(fs, a) - 1
    return "%08X" % funcs[k][0] if k >= 0 and funcs[k][0] <= a < funcs[k][1] else "(no pdata)"

CELLS = {"MODE": (0x02ADD930, 0x02ADD932), "RL": (0x01F81160, 0x01F81168)}
WRITE = ("mov", "and", "or", "xor", "add", "sub", "inc", "dec", "xchg", "cmpxchg", "setne", "sete", "movb", "not",
         "neg", "bts", "btr", "btc", "movaps", "movups", "movdqa", "movdqu", "movq", "movd", "shl", "shr", "sar")
found = {k: [] for k in CELLS}
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for name, (lo, hi) in CELLS.items():
        # target = end_of_insn + d; end_of_insn is i+4+tail with tail in 0..4 (immediates)
        for tail in (0, 1, 2, 4):
            tgt = va0 + i + 4 + tail + d
            if lo - 16 < tgt < hi:
                for L in range(15, 4, -1):
                    st = i + 4 + tail - L
                    if st < 0:
                        continue
                    xs = list(MD.disasm(text[st:st + L], va0 + st, 1))
                    if not xs or xs[0].size != L:
                        continue
                    x = xs[0]
                    for k, op in enumerate(x.operands):
                        if op.type == 3 and MD.reg_name(op.mem.base) == "rip":
                            a = x.address + x.size + op.mem.disp
                            if a < hi and a + op.size > lo:
                                w = (k == 0 and x.mnemonic in WRITE) or x.mnemonic == "xchg"
                                found[name].append((x.address, "W" if w else "r", x.mnemonic, x.op_str, a, op.size))
                    break
for name in CELLS:
    rows = sorted(set(found[name]))
    print("%s: %d accesses, %d writes" % (name, len(rows), sum(1 for r in rows if r[1] == "W")))
    for a, w, mn, ops, tgt, sz in rows:
        if w == "W":
            print("  W %08X %-6s %-40s -> %08X/%d in %s" % (a, mn, ops, tgt, sz, fn(a)))

def rel_sites(t):
    return ["%08X" % (va0 + i) for i in range(len(text) - 5)
            if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t]
for f in (0x0037B450, 0x0037B390, 0x0037B2F0, 0x001A11B0, 0x001A11F0, 0x0024AB60, 0x0024ACF0):
    print("callers of %08X:" % f, rel_sites(f), "qwords", img.raw.count(struct.pack("<Q", f)))
print("0037B450 call sites, the ecx each passes:")
for s in rel_sites(0x0037B450):
    a = int(s, 16)
    for back in range(40, 0, -1):
        xs = list(img.md.disasm(img.rd(a - back, back + 5), a - back))
        if any(x.address == a for x in xs):
            break
    pre = [x for x in xs if x.address < a][-5:]
    print("  %s:" % s, " | ".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in pre if "cx" in x.op_str))
print("E3 consumers: callers of the two read-layer job builders and of the two issuers")
for f in (0x001D6D90, 0x001D6FB0, 0x002DF780, 0x002DF6C0, 0x0046E030):
    print("  callers of %08X:" % f, rel_sites(f), "qwords", img.raw.count(struct.pack("<Q", f)))
