"""dirty_bits.py [FUNC ...]: the bit -> handler table of a flag-word processor (default RenderRecords_ProcessDirtyState 00427DE0).
For every `test <width> ptr [reg + OFF], MASK` (or `bt eax, N` after `mov eax, [reg + OFF]`) followed by a conditional jump,
the calls made before the matching clear (`and [reg + OFF], ~MASK` / `btr`) or before the jump target are collected.
Writes dirty-bits.tsv beside this script: function, word offset, bit, test site, handlers (call targets), clear site."""
import os, re, struct, sys, collections, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0]) for i in range(ns)]
def off(va):
    r = va - BASE
    for a, vs, ro in secs:
        if a <= r < a + vs: return ro + r - a
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def bits_of(mask, width):
    return [b for b in range(width) if mask >> b & 1]
rows = []
for a in (sys.argv[1:] or ["00427DE0"]):
    f = int(a, 16); o = off(f); ins = list(md.disasm(d[o:o + sizes[f]], f))
    for k, x in enumerate(ins):
        m = re.match(r"(byte|dword|word) ptr \[(\w+) \+ (0x[0-9a-f]+)\], (0x[0-9a-f]+|\d+)$", x.op_str)
        bt = None
        if x.mnemonic == "test" and m:
            width = {"byte": 8, "word": 16, "dword": 32}[m.group(1)]
            word = int(m.group(3), 16); mask = int(m.group(4), 0); bitlist = bits_of(mask, width)
        elif x.mnemonic == "bt" and re.match(r"eax, (0x[0-9a-f]+|\d+)$", x.op_str) and k > 0:
            prev = [y for y in ins[max(0, k - 3):k] if re.match(r"eax, dword ptr \[\w+ \+ (0x[0-9a-f]+)\]$", y.op_str)]
            if not prev: continue
            word = int(re.search(r"\+ (0x[0-9a-f]+)\]", prev[-1].op_str).group(1), 16); bitlist = [int(x.op_str.split(", ")[1], 0)]
        else:
            continue
        if len(bitlist) != 1 or k + 1 >= len(ins) or ins[k + 1].mnemonic not in ("je", "jae", "jnb"): continue   # the block runs when the bit is set
        jt = ins[k + 1]
        target = int(jt.op_str, 16) if jt.op_str.startswith("0x") else None
        calls = []; clear = None
        for y in ins[k + 2:k + 40]:
            if target and y.address >= target and jt.mnemonic in ("je", "jae", "jnb"): break
            if y.mnemonic == "call" and y.op_str.startswith("0x"): calls.append(int(y.op_str, 16))
            if y.mnemonic in ("and", "btr") and ("+ 0x%x]" % word) in y.op_str:
                clear = y.address; break
        rows.append((f, word, bitlist[0], x.address, calls, clear))
with open(os.path.join(HERE, "dirty-bits.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("function\tword\tbit\ttest_site\thandlers\tclear_site\n")
    for f, w, b, s, calls, clear in rows:
        fo.write("%08X\t+0x%X\t%d\t%08X\t%s\t%s\n" % (f, w, b, s, " ".join("%08X" % c for c in calls) or "-", "%08X" % clear if clear else "-"))
print(len(rows), "bit tests;", sum(1 for r in rows if r[5]), "with a matching clear;", len(set(c for r in rows for c in r[4])), "distinct handlers")
