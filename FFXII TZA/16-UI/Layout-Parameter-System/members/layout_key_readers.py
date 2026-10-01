"""layout_key_readers.py: for every uisize.json layout key, the functions that read its value global.
Input: layout-key-slots.tsv beside this script (key, slot, global; from layout_key_slots.py). One pass over every
function in functions.tsv, collecting rip-relative memory operands (and rip-relative lea) that resolve exactly to a
key's global, excluding the slot installers 001AF470 and 001B44A0 and the key reader 001CA600 themselves.
Writes layout-key-readers.tsv: key, global, reader function, reader name, first site, site count.
Run from the repository root."""
import os, struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
keys = collections.defaultdict(list)
for l in open(os.path.join(HERE, "layout-key-slots.tsv"), encoding="utf-8"):
    k, slot, g = l.rstrip("\r\n").split("\t")[:3]   # a fourth column names the slot's installer (2026-09-27)
    if g != "?": keys[int(g, 16)].append(k)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        va = struct.unpack_from("<I", d, o + 12)[0]; ro = struct.unpack_from("<I", d, o + 20)[0]
funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
hits = collections.defaultdict(list)   # (global, function) -> sites
names = {}
for e, n, sz in funcs:
    if e in (0x1AF470, 0x1B44A0, 0x1CA600) or sz <= 0: continue
    off = ro + (e - BASE - va)
    if off < 0 or off + sz > len(d): continue
    for ins in md.disasm(d[off:off + sz], e):
        for op in ins.operands:
            if op.type != X86_OP_MEM or not op.mem.base or ins.reg_name(op.mem.base) != "rip": continue
            tgt = ins.address + ins.size + op.mem.disp
            if tgt in keys:
                hits[(tgt, e)].append(ins.address); names[e] = n
with open(os.path.join(HERE, "layout-key-readers.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("key\tglobal\treader\treader_name\tfirst_site\tsites\n")
    for (g, fn), sites in sorted(hits.items(), key=lambda kv: (keys[kv[0][0]][0], kv[0][1])):
        for k in keys[g]:
            f.write("%s\t%08X\t%08X\t%s\t%08X\t%d\n" % (k, g, fn, names[fn], min(sites), len(sites)))
print("globals", len(keys), "with readers", len(set(g for g, _ in hits)), "reader functions", len(set(fn for _, fn in hits)))
