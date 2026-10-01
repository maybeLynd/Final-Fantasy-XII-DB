"""jumptables.py FUNC...: decode MSVC x64 RVA jump tables inside each function.
Pattern: `lea rB, [rip - X]` (rB = image base 00120000), optional `movzx eax, byte [rB + rax + IDX]` (index table),
`mov ecx|eax|edx, dword [rB + rax*4 + TAB]`, `add rC, rB`, `jmp rC`; the case count comes from the nearest preceding
`cmp eREG, N` + `ja`. Prints per function: table address, cases, distinct targets, and each target with its case list."""
import struct, sys, re, collections, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0]) for i in range(ns)]
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
def decode(f):
    o = off(f); ins = list(md.disasm(d[o:o + sizes[f]], f)); res = []
    for k, x in enumerate(ins):
        m = re.match(r"(\w+), dword ptr \[(\w+) \+ (\w+)\*4 \+ (0x[0-9a-f]+)\]$", x.op_str)
        if not m or x.mnemonic not in ("mov", "movsxd"): continue
        tab = BASE + int(m.group(4), 16)
        idx = None; n = None
        for y in reversed(ins[max(0, k - 12):k]):
            mi = re.match(r"\w+, byte ptr \[\w+ \+ \w+ \+ (0x[0-9a-f]+)\]$", y.op_str)
            if mi and y.mnemonic == "movzx" and idx is None: idx = BASE + int(mi.group(1), 16)
            mc = re.match(r"e?\w+, (0x[0-9a-f]+|\d+)$", y.op_str)
            if y.mnemonic == "cmp" and mc and n is None: n = int(mc.group(1), 0) + 1
        if n is None or n > 512: continue
        if idx is not None:
            sel = list(d[off(idx):off(idx) + n]); ntab = max(sel) + 1
            ents = [struct.unpack_from("<I", d, off(tab) + 4 * j)[0] + BASE for j in range(ntab)]
            cases = collections.defaultdict(list)
            for c, s in enumerate(sel): cases[ents[s]].append(c)
        else:
            ents = [struct.unpack_from("<I", d, off(tab) + 4 * j)[0] + BASE for j in range(n)]
            cases = collections.defaultdict(list)
            for c, t in enumerate(ents): cases[t].append(c)
        res.append((x.address, tab, n, cases))
    return res
if __name__ == "__main__":
    for a in sys.argv[1:]:
        f = int(a, 16)
        for site, tab, n, cases in decode(f):
            print("%08X %s  jump at %08X table %08X  cases %d  targets %d" % (f, names.get(f, ""), site, tab, n, len(cases)))
            for t, cs in sorted(cases.items()):
                print("    %08X  cases %s" % (t, ",".join(map(str, cs[:12])) + ("…" if len(cs) > 12 else "")))
