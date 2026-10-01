import pefile, hashlib, bisect, collections
from capstone import *
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
raw = open(EXE, "rb").read(); assert hashlib.sha256(raw).hexdigest().startswith("73461d08")
pe = pefile.PE(data=raw); img = pe.get_memory_mapped_image(); ib = 0x120000
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
from capstone.x86 import X86_OP_MEM
starts = sorted(int(l.split("\t")[0], 16) for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8", errors="replace") if l[:8].strip() and all(c in "0123456789abcdefABCDEF" for c in l.split("	")[0]))
def fn(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 else None
WRITES = {"mov", "add", "sub", "inc", "dec", "and", "or", "xor"}
hits = collections.defaultdict(list)
for s in pe.sections:
    if not (s.Characteristics & 0x20000000): continue
    base = s.VirtualAddress; data = img[base:base + s.Misc_VirtualSize]
    off = 0
    while off < len(data):
        got = False
        for i in md.disasm(data[off:off + 0x4000], ib + base + off):
            got = True
            if i.mnemonic in WRITES and len(i.operands) >= 1 and i.operands[0].type == X86_OP_MEM:
                m = i.operands[0].mem
                if m.disp in (0x100, 0x102) and m.base != 0 and i.operands[0].size in (2, 4, 8):
                    hits[fn(i.address)].append((i.address, i.mnemonic, i.op_str, i.operands[0].size, m.disp))
            last = i.address + i.size
        off = (last - ib - base) if got else off + 1
both = {f: v for f, v in hits.items() if any(x[4] == 0x100 and x[3] == 2 for x in v) and any(x[4] == 0x102 and x[3] == 2 for x in v)}
dw = {f: v for f, v in hits.items() if any(x[4] == 0x100 and x[3] >= 4 for x in v)}
print("functions with word writes to BOTH +0x100 and +0x102:", len(both))
for f, v in sorted(both.items()):
    print(" %08X" % f, [("%08X" % a, m, o) for a, m, o, sz, d in v if sz == 2])
only102 = {f: v for f, v in hits.items() if any(x[4] == 0x102 and x[3] == 2 for x in v) and f not in both}
print("word writes to +0x102 ONLY (not +0x100 word):", len(only102))
for f, v in sorted(only102.items())[:20]:
    print(" %08X" % f, [("%08X" % a, m, o) for a, m, o, sz, d in v if d == 0x102])
print("dword/qword writes at +0x100 (clear both words at once or unrelated):", len(dw))
for f in sorted(dw)[:40]:
    if 0x630000 <= f < 0x640000 or f in both: print(" %08X" % f, [("%08X" % a, m, o) for a, m, o, sz, d in dw[f] if d == 0x100])
