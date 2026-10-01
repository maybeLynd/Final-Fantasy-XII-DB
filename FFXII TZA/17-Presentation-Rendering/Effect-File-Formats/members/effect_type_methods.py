"""effect_type_methods.py: the effect element type x method matrix.
Decodes the MSVC x64 jump tables of the type dispatchers - step 002F3BC0, update 002F3910, walk 002F4020 (type byte at
element +0), setup 005004C0 (type byte at +0x44), a seventh method 002F31C0, and their 0x42.. sub-range dispatchers
0043EBF0 / 00538910 / 0043EAB0 / 0043ED30 / 0043E9C0 - then follows
each non-default arm (`mov rcx, reg; jmp handler` or a call) to its handler function.
Writes effect-type-methods.tsv beside this script: type, then per dispatcher the handler (or `default` / `-`).
Run from the repository root (needs capstone and the image under Database/Tools/work/exe)."""
import os, re, struct, bisect, collections
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
sizes = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
ks = sorted(sizes)
def own(s):
    i = bisect.bisect_right(ks, s) - 1
    return ks[i] if i >= 0 and ks[i] <= s < ks[i] + sizes[ks[i]] else None
md = Cs(CS_ARCH_X86, CS_MODE_64)
def table(f):
    o = off(f); ins = list(md.disasm(d[o:o + sizes[f]], f))
    for k, x in enumerate(ins):
        m = re.match(r"(\w+), dword ptr \[\w+ \+ \w+\*4 \+ (0x[0-9a-f]+)\]$", x.op_str)
        if not m or x.mnemonic not in ("mov", "movsxd"): continue
        tab = BASE + int(m.group(2), 16); idx = n = None
        for y in reversed(ins[max(0, k - 12):k]):
            mi = re.match(r"\w+, byte ptr \[\w+ \+ \w+ \+ (0x[0-9a-f]+)\]$", y.op_str)
            if mi and y.mnemonic == "movzx" and idx is None: idx = BASE + int(mi.group(1), 16)
            mc = re.match(r"\w+, (0x[0-9a-f]+|\d+)$", y.op_str)
            if y.mnemonic == "cmp" and mc and n is None: n = int(mc.group(1), 0) + 1
        sel = list(d[off(idx):off(idx) + n])
        ents = [struct.unpack_from("<I", d, off(tab) + 4 * j)[0] + BASE for j in range(max(sel) + 1)]
        return [ents[s] for s in sel]
def handler(arm):
    o = off(arm)
    for x in md.disasm(d[o:o + 48], arm):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if own(t) != own(arm) or t in sizes: return t
        if x.mnemonic == "ret": return None
DISP = [("step 002F3BC0", 0x2F3BC0, 0), ("update 002F3910", 0x2F3910, 0), ("walk 002F4020 (type - 1)", 0x2F4020, 1),
        ("setup 005004C0 (+0x44)", 0x5004C0, 0), ("sub-step 0043EBF0", 0x43EBF0, 0x42), ("sub-setup 00538910 (+0x44)", 0x538910, 0x42),
        ("sub-update 0043EAB0", 0x43EAB0, 0x42), ("sub-walk 0043ED30", 0x43ED30, 0x42),
        ("seventh 002F31C0", 0x2F31C0, 0x40), ("sub-seventh 0043E9C0", 0x43E9C0, 0x42)]
cols = {}
for name, f, base in DISP:
    arms = table(f); dflt = collections.Counter(arms).most_common(1)[0][0]
    cols[name] = {c + base: (None if a == dflt else a) for c, a in enumerate(arms)}
with open(os.path.join(HERE, "effect-type-methods.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("type\t" + "\t".join(n for n, _, _ in DISP) + "\n")
    for t in range(0xD2):
        row = []
        for name, _, _ in DISP:
            if t not in cols[name]: row.append("-")
            elif cols[name][t] is None: row.append("default")
            else:
                h = handler(cols[name][t]); row.append("%08X" % h if h else "inline")
        fo.write("0x%02X\t%s\n" % (t, "\t".join(row)))
print("written")
