"""WidgetSingleton02AED490 (0x5F0): its +0xEE..+0x5EF is two counted, keyed tables, not a word, a few qwords and 1.2 KB
of "unobserved" span (OPUS, 2026-09-27). Control. Static.
  T1 table A: entries of 0x18 from +0xF0, count byte +0xEE - the release 0037FA00 walks it (0037FA37 lea rbx, [rsi+0xF0];
     0037FA4C add 0x18), releases each entry's +0x10 through 003697F0 (0037FA40 / 0037FA44), clears its +0x00 byte
     (0037FA49) and zeroes the count (0037FA62)
  T2 table B: entries of 0x10 from +0x3F0, count byte +0xEF - 0037FBA0 walks it (0037FC07 lea rcx, [rsi+0x3F0];
     0037FC2F add 0x10) and appends at rsi + (count + 0x3F) * 0x10 = +0x3F0 + count * 0x10 (0037FC4E-0037FC6A)
  T3 both are looked up by the same key: byte +1, and byte +2 as well when +1 is 2 (0037FBD0-0037FBE4; 0037FC11-0037FC26)
  T4 their removals shift the tail down by the stride: count * 3 qwords for A (0037F99A-0037F9AD), count * 2 for B
     (00380074-00380088)
  T5 the layout closes exactly: 0xF0 + 32 * 0x18 = 0x3F0 and 0x3F0 + 32 * 0x10 = 0x5F0, the type's size - so 32 entries
     each. NOT CLAIMED: that an append checks the bound (no compare against 32 is on the append path read here)
  T6 STORE REGRESSION: +0xEE / +0xEF are two uint8 counts, +0xF0 is EntryA[32] and +0x3F0 is EntryB[32]
Not claimed: what the keys, entry A's +0x08 or entry B's +0x08 mean; entry bytes +0x03..+0x07 (no access found).
"""
import os, re, struct, sys
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

R, L, Ra, Rb = I(0x37FA00), I(0x37FBA0), I(0x37F860), I(0x37FFD0)
check("T1 table A: 0x18 entries from +0xF0, count +0xEE; the release frees each +0x10 and clears each +0x00",
      R.get(0x37FA27) == "movzx eax, byte ptr [rsi + 0xee]" and R.get(0x37FA37) == "lea rbx, [rsi + 0xf0]"
      and R.get(0x37FA40) == "mov rcx, qword ptr [rbx + 0x10]" and R.get(0x37FA44) == "call 0x3697f0"
      and R.get(0x37FA49) == "mov byte ptr [rbx], 0" and R.get(0x37FA4C) == "lea rbx, [rbx + 0x18]"
      and R.get(0x37FA62) == "mov byte ptr [rsi + 0xee], 0")
check("T2 table B: 0x10 entries from +0x3F0, count +0xEF; append at +0x3F0 + count * 0x10",
      L.get(0x37FBF7) == "movzx eax, byte ptr [rsi + 0xef]" and L.get(0x37FC07) == "lea rcx, [rsi + 0x3f0]"
      and L.get(0x37FC2F) == "add rcx, 0x10" and L.get(0x37FC4E) == "movzx eax, byte ptr [rsi + 0xef]"
      and L.get(0x37FC5F) == "add rax, 0x3f" and L.get(0x37FC63) == "add rax, rax"
      and L.get(0x37FC66) == "movups xmmword ptr [rsi + rax*8], xmm0" and L.get(0x37FC6A) == "inc byte ptr [rsi + 0xef]")
check("T3 both tables key on byte +1, and on byte +2 when +1 is 2",
      L.get(0x37FBC0) == "lea rbx, [rcx + 0xf0]" and L.get(0x37FBD0) == "movzx eax, byte ptr [rbx + 1]" and L.get(0x37FBD8) == "cmp al, 2"
      and L.get(0x37FBE4) == "cmp byte ptr [rbx + 2], al" and L.get(0x37FBED) == "add rbx, 0x18"
      and L.get(0x37FC11) == "movzx eax, byte ptr [rcx + 1]" and L.get(0x37FC1A) == "cmp al, 2" and L.get(0x37FC26) == "cmp byte ptr [rcx + 2], al")
check("T4 removals shift by the stride: count * 3 qwords (A), count * 2 qwords (B)",
      Ra.get(0x37F987) == "dec byte ptr [r14 + 0xee]" and Ra.get(0x37F99A) == "lea rcx, [rax + rax*2]" and Ra.get(0x37F9A5) == "lea rsi, [rbx + 0x18]"
      and Ra.get(0x37F9AD) == "rep movsq qword ptr [rdi], qword ptr [rsi]"
      and Rb.get(0x380061) == "dec byte ptr [rbx + 0xef]" and Rb.get(0x380074) == "lea rsi, [rdi + 0x10]" and Rb.get(0x380085) == "add rcx, rcx"
      and Rb.get(0x380088) == "rep movsq qword ptr [rdi], qword ptr [rsi]")
hdr = None; size = None
for l in open(DB / "_types/types.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if hdr is None: hdr = c; continue
    if c[0] == "WidgetSingleton02AED490": size = int(c[1], 16)
check("T5 the layout closes: 0xF0 + 32 * 0x18 = 0x3F0, 0x3F0 + 32 * 0x10 = the type's size",
      0xF0 + 32 * 0x18 == 0x3F0 and 0x3F0 + 32 * 0x10 == size == 0x5F0, hex(size or 0))
rows = {}
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "WidgetSingleton02AED490": rows[int(c[1], 16)] = c
g = lambda o, k: rows.get(o, [None] * 9)[k]
check("T6 STORE REGRESSION: two uint8 counts, EntryA[32] at +0xF0, EntryB[32] at +0x3F0",
      g(0xEE, 4) == "uint8" and g(0xEF, 4) == "uint8" and g(0xF0, 4) == "WidgetSingleton02AED490EntryA[32]"
      and g(0x3F0, 4) == "WidgetSingleton02AED490EntryB[32]" and not [o for o in rows if 0xF0 < o < 0x3F0 or 0x3F0 < o < 0x5F0],
      "%s / %s / %s / %s" % (g(0xEE, 4), g(0xEF, 4), g(0xF0, 4), g(0x3F0, 4)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
