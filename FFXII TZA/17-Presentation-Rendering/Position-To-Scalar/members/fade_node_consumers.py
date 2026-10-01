"""What the callers of the distance-fade node 002F1F40 do with the colour it returns.

For every `call 002F1F40` site in .text: decode forward up to 24 instructions (stopping at ret / int3) and record the
first later call. The question is whether that call is the workbench colour multiply 0026EE00 - i.e. whether the
caller multiplies the node's colour with a colour of its own before using it.
Control: the number of sites must equal the 76 E8 sites the position-to-scalar page records (75 functions, one twice).
"""
import struct, bisect, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
NODE, MUL = 0x2F1F40, 0x26EE00
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try:
        funcs.append(int(p[0], 16))
    except (ValueError, IndexError):
        pass
funcs.sort()
code = d[ro:ro + vs]
base = 0x120000 + va
md = Cs(CS_ARCH_X86, CS_MODE_64)
sites = []
for i in range(len(code) - 5):
    if code[i] == 0xE8 and base + i + 5 + struct.unpack_from("<i", code, i + 1)[0] == NODE:
        sites.append(base + i)
rows = []
for s in sites:
    off = s - base + 5
    nxt, dist = None, 0
    for ins in md.disasm(code[off:off + 160], s + 5):
        dist += 1
        if ins.mnemonic in ("ret", "int3") or dist > 24:
            break
        if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
            nxt = int(ins.op_str, 16)
            break
    f = funcs[bisect.bisect_right(funcs, s) - 1]
    rows.append((f, s, nxt, dist))
tally = collections.Counter("multiply 0026EE00" if n == MUL else ("no call within 24 instructions" if n is None else "other call first") for _, _, n, _ in rows)
print("# call sites %d in %d functions (control: 76 in 75)" % (len(rows), len({r[0] for r in rows})))
for k, v in tally.most_common():
    print("# %s\t%d" % (k, v))
print("caller\tsite\tfirst_call_after\tinstructions_between")
for f, s, n, dist in rows:
    print("%08X\t%08X\t%s\t%d" % (f, s, ("%08X" % n) if n else "-", dist))
