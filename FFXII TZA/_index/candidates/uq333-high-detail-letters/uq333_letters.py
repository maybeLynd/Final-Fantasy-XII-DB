"""uq333_letters.py - UQ-333: in the engine's model-id format the letters C, N and S select the HIGH-DETAIL model tables
(FABLE, Claude Opus 5.5, 2026-09-26). The decoder 002ED6F0 is executed under Unicorn; the path arrays are read from the
lea/store pairs of ResourcePath_Init (002DF9A0) into g_pathTables (0215F000).

  L1 a section-012 entry {u16 id, u16 letter}, read as a little-endian u32, is (letter << 16) | id - the format the
     decoder reads (number in bits 0-15, letter in bits 16-23).
  L2 decoder: c -> (14, n x 25), C -> (15, n); n -> (19, n x 25), N -> (20, n); s -> (23, n x 25), S -> (24, n).
  L3 path arrays: kind 15 entries are obj_finish\\in\\high\\...\\hc*.cm, kind 20 hn*.cm, kind 24 hs*.cm (every entry
     checked from index 0 until the first entry that is not a high-detail .cm); kinds 14, 19, 23 are the
     chara, npc and summon trees in 25-slot blocks (a .cm and its .ca takes).
  L4 sensitivity: the lowercase kinds' block order is NOT model-number order (kind 14: c1004, c1029, c1010 at 0, 25,
     50), so a section-012 lowercase id (model - 1000 per section 012) cannot be the decoder's number directly - the
     section's reader must translate, and the same caution applies to C/N/S. The index rule is NOT claimed.
  L5 data fit: every section-012 C / N / S id (section012-model-ids.tsv) lies inside its high-detail table, and the N and
     S maxima are exactly the tables' last indices (86 of 87, 4 of 5).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RSP
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
entry = struct.pack("<HH", 7, ord("C"))
check("L1 a {u16 id, u16 letter} entry is the decoder's u32", struct.unpack("<I", entry)[0] == (ord("C") << 16) | 7)
mu = Uc(UC_ARCH_X86, UC_MODE_64)
for vs, va, rs, ro in secs:
    a = BASE + va; size = (max(vs, rs) + 0xFFF) & ~0xFFF
    mu.mem_map(a, size); mu.mem_write(a, d[ro:ro + min(rs, vs if vs else rs)])
mu.mem_map(BASE, 0x1000); mu.mem_write(BASE, d[:0x1000])
STK, RET = 0x70000000, 0x60000000
mu.mem_map(STK, 0x10000); mu.mem_map(RET, 0x1000); mu.mem_write(RET, b"\xC3")
def dec(i):
    mu.mem_write(STK + 0x100, struct.pack("<II", 0xAAAAAAAA, 0xBBBBBBBB))
    mu.reg_write(UC_X86_REG_RCX, i); mu.reg_write(UC_X86_REG_RDX, STK + 0x100); mu.reg_write(UC_X86_REG_R8, STK + 0x104)
    mu.reg_write(UC_X86_REG_RSP, STK + 0x8000); mu.mem_write(STK + 0x8000, struct.pack("<Q", RET))
    mu.emu_start(0x2ED6F0, RET, count=200)
    return struct.unpack("<II", bytes(mu.mem_read(STK + 0x100, 8)))
got = {ch: dec((ord(ch) << 16) | 7) for ch in "cCnNsS"}
check("L2 the decoder: c/C -> 14/15, n/N -> 19/20, s/S -> 23/24; lowercase x25, uppercase direct",
      got == {"c": (14, 175), "C": (15, 7), "n": (19, 175), "N": (20, 7), "s": (23, 175), "S": (24, 7)}, repr(got))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
ins = list(cs.disasm(d[off(0x2DF9A0):off(0x2DF9A0) + 2831], 0x2DF9A0))
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return None if not m else x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
arr = {}
for i, x in enumerate(ins):
    if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip"):
        t = rip(x)
        if t is not None and 0x215F000 <= t < 0x215F200:
            src = x.op_str.split(",")[1].strip()
            for y in reversed(ins[max(0, i - 6):i]):
                if y.mnemonic == "lea" and y.op_str.startswith(src + ","):
                    arr.setdefault((t - 0x215F000) // 8, rip(y)); break
def s_at(p):
    o = off(p) if p else None
    return None if o is None else d[o:d.find(b"\0", o)].decode("latin-1")
def entries(k, stop_pat):
    out = []
    for j in range(400):
        s = s_at(struct.unpack_from("<Q", d, off(arr[k]) + 8 * j)[0])
        if s is None or not re.search(stop_pat, s): break
        out.append(s)
    return out
hi = {k: entries(k, r"\\high\\.*\\h[cns]\d{4}_\d\d\.cm$") for k in (15, 20, 24)}
pref = {15: "hc", 20: "hn", 24: "hs"}
ok3 = all(len(v) >= 5 and all(("\\" + pref[k]) in e for e in v) for k, v in hi.items())
lo = {k: s_at(struct.unpack_from("<Q", d, off(arr[k]))[0]) for k in (14, 19, 23)}
ok3 = ok3 and "\\chara\\" in lo[14] and "\\npc\\" in lo[19] and "\\summon\\" in lo[23]
check("L3 kinds 15/20/24 hold the high-detail hc/hn/hs models; 14/19/23 the chara/npc/summon trees", ok3,
      "high-detail runs: 15=%d 20=%d 24=%d entries" % (len(hi[15]), len(hi[20]), len(hi[24])))
b0, b25, b50 = (s_at(struct.unpack_from("<Q", d, off(arr[14]) + 8 * j)[0]) for j in (0, 25, 50))
check("L4 sensitivity: kind 14's blocks are not in model-number order, so the index rule is not claimed",
      b0.endswith("c1004.cm") and b25.endswith("c1029.cm") and b50.endswith("c1010.cm"), "%s | %s | %s" % (b0[-9:], b25[-9:], b50[-9:]))
import csv, collections
tsv = ROOT / "Database/FFXII TZA/25-EBP-Script-Container/Sections/members/section012-model-ids.tsv"
ids = collections.defaultdict(list)
for r in csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"): ids[r["letter"]].append(int(r["id"]))
rng = {L: (min(ids[L]), max(ids[L]), len(set(ids[L]))) for L in "CNS"}
check("L5 data fit: every section-012 C / N / S id lies inside its high-detail table (N and S reach its last index)",
      rng["C"][0] >= 0 and rng["C"][1] < len(hi[15]) and rng["N"][1] == len(hi[20]) - 1 and rng["S"] == (0, len(hi[24]) - 1, len(hi[24])),
      "C %s of %d, N %s of %d, S %s of %d" % (rng["C"], len(hi[15]), rng["N"], len(hi[20]), rng["S"], len(hi[24])))
print("FAILS", fails)
sys.exit(1 if fails else 0)
