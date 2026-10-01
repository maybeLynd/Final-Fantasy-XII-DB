"""uc1_band_checks.py - two of the checks the 65-256 B package lists as missing, run on its 100 clean rows, with the
listed 65-256 B functions as control (FABLE, Claude Opus 5.5, 2026-09-28). Static.
  T   tail: after trailing int3 / nop padding is stripped, the block decodes linearly to exactly its end and the last
      instruction is a terminal (ret, jmp, int3-free) - otherwise the block ends in bytes that are not its own code
  P   interior pointers: no u64 VA or u32 RVA anywhere outside .text points strictly inside the block (a stored function
      pointer or table entry into the interior would make it an alternative entry or a fragment)
  X   .pdata: whether a RUNTIME_FUNCTION begins at the block's start (and ends at its code end), and that none begins inside
Control: the same three measures over listed functions of 65-256 B (functions.tsv).
"""
import os, re, sys, struct, bisect, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, "../uc1-band-65-256/uc1-band-65-256-rows.tsv")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
FUNCS = os.environ.get("FUNCS_TSV", "")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    name = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((name, va, vs, ra, rs)); o += 40
BASE = 0x120000
def foff(rva):
    for n, va, vs, ra, rs in secs:
        if va <= rva < va + rs: return ra + rva - va
md = Cs(CS_ARCH_X86, CS_MODE_64)
def tail_ok(start, size):
    b = d[foff(start - BASE): foff(start - BASE) + size]
    end = len(b)
    while end > 0 and b[end - 1] in (0xCC, 0x90): end -= 1
    pos = 0; last = None
    for x in md.disasm(b[:end], start):
        pos = x.address - start + x.size; last = x
    if last is None or pos != end: return "does-not-decode-to-end"
    if last.mnemonic in ("ret", "jmp") or last.mnemonic.startswith("ret"): return "ok"
    return "ends-with-" + last.mnemonic
# pointer targets outside .text: every u64 and u32 at 4-byte alignment in non-.text sections
tgt = []
for n, va, vs, ra, rs in secs:
    if n == ".text" or rs == 0: continue
    blob = d[ra:ra + rs]
    for k in range(0, len(blob) - 3, 4):
        v = struct.unpack_from("<I", blob, k)[0]
        if 0x1000 <= v < 0x2000000: tgt.append(v + BASE)          # an RVA
        if k + 8 <= len(blob):
            q = struct.unpack_from("<Q", blob, k)[0]
            if BASE < q < BASE + 0x2000000: tgt.append(q)          # a VA
tgt.sort()
def interior_hits(start, size):
    i = bisect.bisect_right(tgt, start); n = 0
    while i < len(tgt) and tgt[i] < start + size: n += 1; i += 1
    return n
# .pdata
pn, pva, pvs, pra, prs = next(s for s in secs if s[0] == ".pdata")
pdata = [struct.unpack_from("<III", d, pra + k) for k in range(0, pvs - 11, 12)]
pbeg = {b + BASE: e + BASE for b, e, u in pdata if b}
pb_sorted = sorted(pbeg)
def pdata_state(start, size):
    at = start in pbeg
    inside = [b for b in pb_sorted[bisect.bisect_right(pb_sorted, start):bisect.bisect_left(pb_sorted, start + size)]]
    return ("begins-here" if at else "none"), len(inside)
rows = [l.split("\t") for l in open(ROWS, encoding="utf-8").read().split("\n")[1:] if l.strip()]
clean = [(int(r[0], 16), int(r[1])) for r in rows if r[-1] == "clean"]
res = {}
for s, n in clean:
    res[s] = (tail_ok(s, n), interior_hits(s, n), pdata_state(s, n))
tc = collections.Counter(v[0] for v in res.values()); pc = sum(1 for v in res.values() if v[1]); xc = collections.Counter(v[2][0] for v in res.values()); xi = sum(1 for v in res.values() if v[2][1])
print("clean rows: %d" % len(clean))
print("  T tail: %s" % dict(tc))
print("  P rows with an interior pointer: %d" % pc)
print("  X pdata at start: %s; rows with a pdata entry beginning inside: %d" % (dict(xc), xi))
# control: listed functions of 65-256 B
CAND = os.path.join(HERE, "..")
src = open(os.path.join(CAND, "fable_uc1_band_ruling.py"), encoding="utf-8").read().split("\nif not listed:")[0]
g = {"__file__": os.path.join(CAND, "fable_uc1_band_ruling.py")}
exec(compile(src, "fable_uc1_band_ruling.py[prefix]", "exec"), g)
listed = g["listed"]                                    # the same listed population the band's instruments use
ctrl = [(int(s, 16) if isinstance(s, str) else s, n) for s, n in listed if 65 <= n <= 256]
if ctrl:
    cr = [(tail_ok(s, n), interior_hits(s, n), pdata_state(s, n)) for s, n in ctrl]
    print("control (listed 65-256 B, %d): T %s; P %d (%.1f%%); X %s; inside %d" % (len(cr), dict(collections.Counter(v[0] for v in cr)), sum(1 for v in cr if v[1]), 100.0 * sum(1 for v in cr if v[1]) / len(cr), dict(collections.Counter(v[2][0] for v in cr)), sum(1 for v in cr if v[2][1])))
with open(os.path.join(HERE, "uc1-band-65-256-clean-checks.tsv"), "w", encoding="utf-8", newline="\n") as h:
    h.write("start_va\tbytes\ttail\tinterior_pointers\tpdata_at_start\tpdata_inside\n")
    for s, n in clean:
        t, p, (x, xin) = res[s]; h.write("%08X\t%d\t%s\t%d\t%s\t%d\n" % (s, n, t, p, x, xin))
# U: unwind. MSVC x64 emits a RUNTIME_FUNCTION for every function that is not a leaf (a call, a push, a stack
# allocation or a nonvolatile save). A block with any of those and no .pdata entry, begun at it or covering it, is not a
# standalone compiled function. Covered = some entry's [begin, end) contains the block start.
pr = sorted((b + BASE, e + BASE) for b, e, u in pdata if b)
prb = [b for b, e in pr]
def covered(start):
    i = bisect.bisect_right(prb, start) - 1
    return i >= 0 and pr[i][0] <= start < pr[i][1]
def nonleaf(start, size):
    b = d[foff(start - BASE): foff(start - BASE) + size]
    for x in md.disasm(b, start):
        if x.mnemonic in ("call", "push") or (x.mnemonic in ("sub", "add") and x.op_str.startswith("rsp")) or re.match(r"mov qword ptr \[rsp", x.mnemonic + " " + x.op_str):
            return x.mnemonic + " " + x.op_str
    return None
u_clean = collections.Counter(("nonleaf" if nonleaf(s, n) else "leaf", "covered" if covered(s) else "uncovered") for s, n in clean)
ctrl_nop = [(s, n) for s, n in ctrl if s not in pbeg]
u_ctrl = collections.Counter(("nonleaf" if nonleaf(s, n) else "leaf", "covered" if covered(s) else "uncovered") for s, n in ctrl_nop)
print("  U clean rows (no .pdata at start): %s" % dict(u_clean))
print("  U control, listed 65-256 B with no .pdata at start (%d): %s" % (len(ctrl_nop), dict(u_ctrl)))
with open(os.path.join(HERE, "uc1-band-65-256-unwind.tsv"), "w", encoding="utf-8", newline="\n") as h:
    h.write("start_va\tbytes\tfirst_nonleaf_instruction\tpdata_covers\n")
    for s, n in clean: h.write("%08X\t%d\t%s\t%s\n" % (s, n, nonleaf(s, n) or "-", "yes" if covered(s) else "no"))
ok("C", len(clean) == 100, "the package's 100 clean rows read")
print("FAILS", fails)
