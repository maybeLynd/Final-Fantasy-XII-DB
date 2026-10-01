"""bl8_walkers.py - BL-8: who WALKS the class descriptor's intrusive lists (FABLE, Claude Opus 5.5, 2026-09-27).
Image-wide over every listed body: the sentinel-walk idiom 'lea rH, [rB + D]' then, within 12 instructions, a load
'mov rN, qword ptr [rH]' and a compare of rN against rH (either order). Counted per displacement D in {0x60, 0x80,
0x90, 0xA0, 0xB0}; each hit is reported with its function so descriptor walkers can be told from coincidences.
Known positive: the descriptor destructor 00633390 walks +0x80, +0x90, +0xA0 and +0xB0 to unlink them.
Two more shapes are printed: a direct head load compared against a lea of the same head, and the head passed in
an argument register to a call within 5 instructions (reported by callee; not selective at these offsets)."""
import re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
DS = (0x60, 0x80, 0x90, 0xA0, 0xB0)
hits = collections.defaultdict(list); argpass = collections.defaultdict(list); direct = collections.defaultdict(list)
ARGS = ("rcx", "rdx", "r8", "r9")
for f, sz in SIZES.items():
    o = off(f)
    if o is None or sz <= 0 or not 0x121000 <= f < 0x8C0000: continue
    b = list(cs.disasm(d[o:o + sz], f))
    for k, x in enumerate(b):
        m = re.fullmatch(r"(r\w+), \[(r\w+) \+ (0x[0-9a-f]+)\]", x.op_str) if x.mnemonic == "lea" else None
        md = re.fullmatch(r"(r\w+), qword ptr \[(r\w+) \+ (0x[0-9a-f]+)\]", x.op_str) if x.mnemonic == "mov" else None
        if md and int(md.group(3), 16) in DS:
            D2 = int(md.group(3), 16); win = b[max(0, k - 16):k + 17]
            heads = {y.op_str.split(",")[0] for y in win if y.mnemonic == "lea" and y.op_str.endswith("[%s + %s]" % (md.group(2), md.group(3)))}
            if any(y.mnemonic == "cmp" and md.group(1) in y.op_str.split(", ") and (set(y.op_str.split(", ")) - {md.group(1)}) & heads for y in win):
                direct[D2].append(("%08X" % f, "%08X" % x.address))
        if not m or int(m.group(3), 16) not in DS: continue
        h = m.group(1); D = int(m.group(3), 16); loaded = None
        if h in ARGS:
            for y in b[k + 1:k + 6]:
                if y.mnemonic == "call": argpass[D].append(("%08X" % f, "%08X" % x.address, y.op_str)); break
                if y.op_str.startswith(h + ","): break
        for y in b[k + 1:k + 13]:
            if y.mnemonic == "mov" and y.op_str.endswith("qword ptr [%s]" % h) and loaded is None:
                loaded = y.op_str.split(",")[0]
            elif loaded and y.mnemonic == "cmp" and set(y.op_str.split(", ")) == {loaded, h}:
                hits[D].append(("%08X" % f, "%08X" % x.address)); break
            if y.op_str.startswith(h + ",") and y.mnemonic in ("mov", "lea", "xor", "pop"): break
fails = 0
for D in DS:
    fs = sorted({f for f, a in hits[D]})
    print("D=0x%X  %d sites in %d functions: %s" % (D, len(hits[D]), len(fs), " ".join(fs[:40])))
for D in DS:
    fs = sorted({f for f, a in direct[D]})
    print("direct-load walk D=0x%X  %d sites: %s" % (D, len(direct[D]), " ".join(fs[:30])))
for D in DS:
    cal = collections.Counter(c for f, a, c in argpass[D])
    print("head passed to a call D=0x%X  %d sites; callees: %s" % (D, len(argpass[D]), dict(cal.most_common(12))))
ok = all(any(f == "00633390" for f, a in hits[D]) for D in (0x80, 0x90, 0xA0, 0xB0))
print("%s  known positive: 00633390 walks +0x80/+0x90/+0xA0/+0xB0" % ("PASS" if ok else "FAIL")); fails += not ok
print("FAILS", fails); sys.exit(1 if fails else 0)
