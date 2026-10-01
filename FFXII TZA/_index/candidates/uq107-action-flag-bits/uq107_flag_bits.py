"""uq107_flag_bits.py - UQ-107: every provenance-verified read of the action row's flag dword +0x0C, and the bits each
tests (FABLE, Claude Opus 5.5, 2026-09-27). Static; runs action_row_follower.py and classifies each read.
  F1 the follower reports 60 reads of +0x0C, and they include all 23 sites of the 2026-09-18 table
     07-Combat-Action/Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv (control).
  F2 the bits each read tests: an immediate at the site, or the `bt` / `shr` + `and` / `test` applied to the loaded
     register. Bits 12..31 with a reader: 12, 13, 14, 16, 17, 19, 21, 24, 25, 26, 27, 28, 29, 30, 31; with none: 15, 18,
     20, 22, 23.
  F3 the 2026-09-18 claim is refuted: the immediates it called "not the action row's" - 0x200000, 0x3000000,
     0x10000000, 0x20000000 - are tested on provenance-verified action rows (0030D271, 0030D2C0, 0031F0EF, 0031F000),
     none of those four sites is in its table, and 0031A990 tests bits 21 and 25 by `bt` (0031A9F4, 0031A9E5), which
     its row for 0031A99A (bits 12 and 24 only) did not follow.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, subprocess, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

out = subprocess.run([sys.executable, str(HERE / "action_row_follower.py")], capture_output=True, text=True).stdout
sites = []
for l in out.splitlines():
    m = re.match(r"\+0x0C w(\d+) ([0-9A-F]{8}) in ([0-9A-F]{8})", l.strip())
    if m: sites.append((int(m.group(2), 16), int(m.group(3), 16), int(m.group(1))))
old = set()
for l in open(DB / "07-Combat-Action/Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv", encoding="utf-8"):
    q = l.rstrip("\n").split("\t")
    if len(q) > 3 and re.fullmatch(r"[0-9A-F]{8}", q[3]): old.add(int(q[3], 16))
found = {s for s, f, w in sites}
check("F1 60 reads of +0x0C; the 2026-09-18 table's 23 sites are among them", len(sites) == 60 and len(old) == 23 and old <= found,
      "reads %d; old %d; old missing %s" % (len(sites), len(old), sorted("%08X" % a for a in old - found)))

R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", **{"r%dd" % j: "r%d" % j for j in range(8, 16)}}
def regs(s): return {R64.get(t, t) for t in re.findall(r"\b(r\w+|e[a-z]{2})\b", s)}
bits_at = {}
for site, f, w in sites:
    L = list(cs.disasm(d[off(f):off(f) + SIZES[f]], f)); i = next(k for k, x in enumerate(L) if x.address == site); x = L[i]
    bits = set()
    m = re.search(r", (0x[0-9a-f]+|\d+)$", x.op_str)
    if x.mnemonic in ("test", "and") and "ptr" in x.op_str.split(",")[0] and m:
        v = int(m.group(1), 0); bits = {b for b in range(32) if v >> b & 1}
    elif x.mnemonic == "cmp" and m and int(m.group(1), 0) == 0x80000000:
        bits = {31}
    else:
        r = R64.get(x.op_str.split(",")[0].strip(), x.op_str.split(",")[0].strip()); shift = 0
        for y in L[i + 1:i + 25]:
            s = y.op_str
            if r not in regs(s): continue
            dst = R64.get(s.split(",")[0].strip(), s.split(",")[0].strip()); m2 = re.search(r", (0x[0-9a-f]+|\d+)$", s)
            if y.mnemonic in ("shr", "sar") and dst == r and m2: shift += int(m2.group(1), 0); continue
            if y.mnemonic == "bt" and dst == r and m2: bits.add(int(m2.group(1), 0) + shift); continue
            if y.mnemonic in ("and", "test") and dst == r and m2:
                v = int(m2.group(1), 0) << shift; bits |= {b for b in range(32) if v >> b & 1}; continue
            if y.mnemonic == "mov" and dst == r: break
    bits_at[site] = bits
readers = collections.defaultdict(set)
for s, b in bits_at.items():
    for x in b: readers[x].add(s)
hi = sorted(b for b in readers if b >= 12)
none = [b for b in range(12, 32) if b not in readers]
for b in range(12, 32):
    print("   bit %2d: %s" % (b, " ".join("%08X" % s for s in sorted(readers.get(b, ())))))
check("F2 bits 12..31 read: 12 13 14 16 17 19 21 24 25 26 27 28 29 30 31; unread: 15 18 20 22 23",
      hi == [12, 13, 14, 16, 17, 19, 21, 24, 25, 26, 27, 28, 29, 30, 31] and none == [15, 18, 20, 22, 23], "read %s unread %s" % (hi, none))
f3 = {0x30D271: {21}, 0x30D2C0: {24, 25}, 0x31F0EF: {28}, 0x31F000: {29}}
oldbits = collections.defaultdict(set)
for l in open(DB / "07-Combat-Action/Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv", encoding="utf-8"):
    q = l.rstrip("\n").split("\t")
    if len(q) > 5 and re.fullmatch(r"[0-9A-F]{8}", q[3]) and q[5].isdigit(): oldbits[int(q[3], 16)].add(int(q[5]))
ok3 = (all(bits_at.get(s) == b for s, b in f3.items()) and not any(s in old for s in f3)
       and {21, 25} <= bits_at.get(0x31A99A, set()) and not ({21, 25} & oldbits[0x31A99A]))
check("F3 the immediates called 'not the action row's' on 2026-09-18 are tested on action rows; 0031A990 tests bits 21 and 25",
      ok3, str({"%08X" % s: sorted(bits_at.get(s, ())) for s in list(f3) + [0x31A99A]}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
