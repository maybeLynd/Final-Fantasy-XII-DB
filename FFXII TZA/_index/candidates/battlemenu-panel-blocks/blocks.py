"""BattleMenuPanelWidget3010 +0xC0..+0x1BF: four copied 0x40-byte blocks of one layout (OPUS, 2026-09-27). Control.
  B1 the handler 00276D30 copies a whole 0x40-byte template into +0xC0, +0x100, +0x140 and +0x180 (four 16-byte moves
     each: 00277101-00277122, 002771B7-002771D8 and 00277505-00277526, 002771F3-00277214, 00277230-00277251)
  B2 the reader 0029F5D0 takes a block's base (00276D30 passes rdi + 0xC0 at 0027779D) and reads its +0x0A as a
     sign-extended word, +0x0C / +0x0E / +0x10 / +0x12 as words, +0x18 and +0x20 as qwords and +0x39 as a byte
  B3 four blocks tile +0xC0..+0x1BF exactly; the next declared row is +0x1C0 (a separate 0x30 copy)
  B4 STORE REGRESSION: +0xC0 is BattleMenuPanelWidget3010Block[4] and no parent row starts inside it
Not claimed: what the block describes (0029F5D0's use of it is a draw call, not traced further); +0x14, +0x28 and
+0x3A spans stay unobserved; +0x30 (9 bytes) is covered only by the copy.
"""
import os, re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sizes[f]], f)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
H = I(0x276D30)
copies = collections.defaultdict(set)
for a, s in H.items():
    m = re.match(r"movups xmmword ptr \[rdi \+ (0x[0-9a-f]+)\], xmm\d$", s)
    if m: copies[int(m.group(1), 16)].add(a)
blocks = {b: all(copies.get(b + k) for k in (0, 0x10, 0x20, 0x30)) for b in (0xC0, 0x100, 0x140, 0x180)}
check("B1 each of +0xC0 / +0x100 / +0x140 / +0x180 receives a whole 0x40-byte copy", all(blocks.values()), str(blocks))
R = I(0x29F5D0)
acc = collections.defaultdict(set)
for a, s in R.items():
    m = re.search(r"(byte|word|dword|qword) ptr \[(rcx|rbx)(?: \+ (0x[0-9a-f]+|\d+))?\]", s)
    if m: acc[int(m.group(3), 0) if m.group(3) else 0].add((m.group(1), s.split()[0]))
check("B2 the reader takes a block base and reads +0x0A (movsx word), +0x0C..+0x12 words, +0x18 / +0x20 qwords, +0x39 byte",
      H.get(0x27779D) == "lea rcx, [rdi + 0xc0]" and R.get(0x29F5DF) == "mov rbx, rcx"
      and ("word", "movsx") in acc[0xA] and all(("word", "movzx") in acc[o] for o in (0xC, 0xE, 0x10, 0x12))
      and ("qword", "mov") in acc[0x18] and ("qword", "mov") in acc[0x20] and ("byte", "movzx") in acc[0x39],
      str({hex(k): sorted(v) for k, v in sorted(acc.items())}))
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "BattleMenuPanelWidget3010": rows.append((int(c[1], 16), int(c[2]), c[3], c[4]))
check("B3 four blocks end at +0x1C0, where the next declared row starts", 0xC0 + 4 * 0x40 == 0x1C0 and any(r[0] == 0x1C0 for r in rows))
inside = [r[2] for r in rows if 0xC0 < r[0] < 0x1C0]
check("B4 STORE REGRESSION: +0xC0 is BattleMenuPanelWidget3010Block[4], nothing starts inside it",
      any(r[0] == 0xC0 and r[3] == "BattleMenuPanelWidget3010Block[4]" for r in rows) and not inside, "%d rows inside" % len(inside))
print("FAILS", fails)
sys.exit(1 if fails else 0)
